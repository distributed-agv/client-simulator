import grpc
import guide_pb2
import guide_pb2_grpc
import random
import time
import multiprocessing
import json
import datetime
import subprocess

OFFSETS = [(0, 0), (0, -1), (0, 1), (1, 0), (-1, 0)]


class Car:
    def __init__(self, t_move_avg, t_move_std):
        self.t_move_avg = t_move_avg
        self.t_move_std = t_move_std

    def move(self, step_code):
        t_move = max(random.gauss(self.t_move_avg, self.t_move_std), 0)
        time.sleep(t_move)


class ClientProcess(multiprocessing.Process):
    def __init__(self, car, car_id, src_pos, dst_pos, server_addrs,
                 t_retry_min, t_retry_mul, t_retry_max, t_stop, t_recover, log_filename):
        super(ClientProcess, self).__init__()
        
        self.car = car

        self.car_id = car_id
        self.seq = 0
        self.src_pos = src_pos
        self.dst_pos = dst_pos
        self.cur_pos = src_pos
        self.last_pos = src_pos
        
        self.server_addrs = server_addrs

        self.t_retry_min = t_retry_min
        self.t_retry_mul = t_retry_mul
        self.t_retry_max = t_retry_max
        self.t_stop = t_stop
        self.t_recover = t_recover

        self.log_filename = log_filename

    def run(self):
        log_file = open(self.log_filename, 'w')

        def log(msg_type, msg):
            log_file.write(f'[{msg_type}] {datetime.datetime.now()} {msg}\n')
            log_file.flush()

        def get_next_step(car_state):
            server_addr = random.choice(self.server_addrs)
            channel = grpc.insecure_channel(f"{server_addr['host']}:{server_addr['port']}")
            stub = guide_pb2_grpc.GuideStub(channel)

            t_retry = self.t_retry_min
            while True:
                try:
                    return stub.GetNextStep(car_state)
                except grpc.RpcError as err:
                    log('Error', err.details())
                    time.sleep(t_retry)
                t_retry = min(t_retry * self.t_retry_mul, self.t_retry_max)

        def make_car_state():
            def make_position(pos):
                return guide_pb2.CarState.Position(
                    row_idx=pos[0],
                    col_idx=pos[1],
                )

            return guide_pb2.CarState(
                car_id=self.car_id,
                seq=self.seq,
                cur_pos=make_position(self.cur_pos),
                last_pos=make_position(self.last_pos),
                dst_pos=make_position(self.dst_pos),
            )

        log(' Info', f'<Arrive> {self.cur_pos}')
        while True:
            car_state = make_car_state()
            step = get_next_step(car_state)
            if step.step_code < 0:
                if self.seq == step.step_code:
                    time.sleep(self.t_recover)
                else:
                    self.seq = step.step_code
                log(' Info', f'< Nonce> {step.step_code}')
            elif step.step_code == guide_pb2.Step.StepCode.RESET:
                self.seq = 0
                self.last_pos = self.cur_pos
                log(' Info', '< Reset>')
            else:
                offset = OFFSETS[step.step_code]
                next_pos = (self.cur_pos[0] + offset[0], self.cur_pos[1] + offset[1])
                if step.step_code == guide_pb2.Step.StepCode.STOP:
                    time.sleep(self.t_stop)
                else:
                    log(' Info', f'<  Move> {self.cur_pos} {next_pos}')
                    self.car.move(step.step_code)
                self.seq += 1
                self.last_pos = self.cur_pos
                self.cur_pos = next_pos
                if self.cur_pos == self.dst_pos:
                    self.src_pos, self.dst_pos = self.dst_pos, self.src_pos                    
                log(' Info', f'<Arrive> {self.cur_pos}')


if __name__ == '__main__':
    config = json.load(open('config.json', 'r'))
    server_addrs = config['server_addrs']
    car_tasks = config['car_tasks']
    t_move_avg = config['t_move_avg']
    t_move_std = config['t_move_std']
    t_retry_min = config['t_retry_min']
    t_retry_max = config['t_retry_max']
    t_retry_mul = config['t_retry_mul']
    t_stop = config['t_stop']
    t_recover = config['t_recover']
    duration = config['duration']

    client_processes = [
        ClientProcess(
            Car(
                t_move_avg,
                t_move_std,
            ),
            car_id,
            tuple(car_task['src_pos']),
            tuple(car_task['dst_pos']),
            server_addrs,
            t_retry_min,
            t_retry_mul,
            t_retry_max,
            t_stop,
            t_recover,
            f'logs/client{car_id}.log',
        )
        for car_id, car_task in enumerate(car_tasks)
    ]

    locator = subprocess.Popen(['python3', 'locator.py'])
    for car_id, client_process in enumerate(client_processes):
        client_process.start()
        print(f'Client {car_id}\'s PID: {client_process.pid}')
    time.sleep(duration)
    for client_process in client_processes:
        client_process.terminate()
    locator.terminate()
