import random
import time
import multiprocessing
import json
import datetime
import subprocess
import signal
import guidepy
import hashlib

OFFSETS = [(0, 0), (0, -1), (0, 1), (1, 0), (-1, 0)]


class Car:
    def __init__(self, t_move_avg, t_move_std):
        self.t_move_avg = t_move_avg
        self.t_move_std = t_move_std

    def move(self, step_code):
        t_move = max(random.gauss(self.t_move_avg, self.t_move_std), 0)
        time.sleep(t_move)


class ClientProcess(multiprocessing.Process):
    def __init__(self, guide, car, car_id, src_pos, dst_pos,
                 t_retry_min, t_retry_mul, t_retry_max, t_stop, t_recover, log_filename):
        super(ClientProcess, self).__init__()
        
        self.guide = guide
        self.car = car

        self.car_id = car_id
        self.seq = 0
        self.src_pos = src_pos
        self.dst_pos = dst_pos
        self.cur_pos = src_pos
        self.last_pos = src_pos

        self.t_retry_min = t_retry_min
        self.t_retry_mul = t_retry_mul
        self.t_retry_max = t_retry_max
        self.t_stop = t_stop
        self.t_recover = t_recover

        self.log_filename = log_filename

    def run(self):
        log_file = open(self.log_filename, 'w')

        def log(msg_type, msg):
            log_file.write('[{}] {} {}\n'.format(msg_type, datetime.datetime.now(), msg))
            log_file.flush()

        def sigterm_handler(signum, stack_frame):
            log(' Info', '<  Crash>')
            exit(0)

        signal.signal(signal.SIGTERM, sigterm_handler)

        def get_next_step():
            t_retry = self.t_retry_min
            while True:
                try:
                    dt_begin = datetime.datetime.now()
                    step_code = guidepy.get_next_step(
                        self.guide,
                        self.car_id,
                        self.seq,
                        self.cur_pos[0],
                        self.cur_pos[1],
                        self.last_pos[0],
                        self.last_pos[1],
                        self.dst_pos[0],
                        self.dst_pos[1],
                    )
                    dt_end = datetime.datetime.now()
                    latency = (dt_end - dt_begin).total_seconds() * 1000
                    log(' Info', '<Latency> {:.2f}'.format(latency))
                    return step_code
                except grpc.RpcError as err:
                    log('Error', err.details())
                    time.sleep(t_retry)
                t_retry = min(t_retry * self.t_retry_mul, self.t_retry_max)

        log(' Info', '< Arrive> {}'.format(self.cur_pos))
        while True:
            step_code = get_next_step()
            if step_code < 0:
                if self.seq == step_code:
                    time.sleep(self.t_recover)
                else:
                    self.seq = step_code
                log(' Info', '<  Nonce> {}'.format(step_code))
            elif step_code == 5:
                self.seq = 0
                self.last_pos = self.cur_pos
                log(' Info', '<  Reset>')
            else:
                offset = OFFSETS[step_code]
                next_pos = (self.cur_pos[0] + offset[0], self.cur_pos[1] + offset[1])
                if step_code == 0:
                    time.sleep(self.t_stop)
                else:
                    log(' Info', '<   Move> {} {}'.format(self.cur_pos, next_pos))
                    self.car.move(step_code)
                self.seq += 1
                self.last_pos = self.cur_pos
                self.cur_pos = next_pos
                if self.cur_pos == self.dst_pos:
                    self.src_pos, self.dst_pos = self.dst_pos, self.src_pos                    
                log(' Info', '< Arrive> {}'.format(self.cur_pos))


if __name__ == '__main__':
    config = json.load(open('config.json', 'r'))
    car_tasks = config['car_tasks']
    t_move_avg = config['t_move_avg']
    t_move_std = config['t_move_std']
    t_retry_min = config['t_retry_min']
    t_retry_max = config['t_retry_max']
    t_retry_mul = config['t_retry_mul']
    t_stop = config['t_stop']
    t_recover = config['t_recover']
    duration = config['duration']
    car_num = len(car_tasks)
    row_num = config['row_num']
    col_num = config['col_num']
    redis_addr = config['redis_addr']

    get_lock_script = open('get_lock.lua', 'r').read().encode('utf8')
    commit_script = open('commit.lua', 'r').read().encode('utf8')
    recover_script = open('recover.lua', 'r').read().encode('utf8')
    get_lock_sha = hashlib.sha1(get_lock_script).hexdigest()
    commit_sha = hashlib.sha1(commit_script).hexdigest()
    recover_sha = hashlib.sha1(recover_script).hexdigest()
    guide = guidepy.make_guide(
        car_num,
        row_num,
        col_num,
        redis_addr['host'],
        redis_addr['port'],
        get_lock_sha,
        commit_sha,
        recover_sha,
    )

    client_processes = [
        ClientProcess(
            guide,
            Car(
                t_move_avg,
                t_move_std,
            ),
            car_id,
            tuple(car_task['src_pos']),
            tuple(car_task['dst_pos']),
            t_retry_min,
            t_retry_mul,
            t_retry_max,
            t_stop,
            t_recover,
            'logs/client{}.log'.format(car_id),
        )
        for car_id, car_task in enumerate(car_tasks)
    ]

    locator = subprocess.Popen(['python3', 'locator.py'])
    for car_id, client_process in enumerate(client_processes):
        client_process.start()
        print('Client {}\'s PID: {}'.format(car_id, client_process.pid))
    time.sleep(duration)
    for client_process in client_processes:
        client_process.kill()
    locator.kill()
