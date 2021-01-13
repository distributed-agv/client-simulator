import grpc
import guide_pb2
import guide_pb2_grpc
import multiprocessing
import json
import time
import random
import datetime

OFFSETS = [(0, 0), (0, -1), (0, 1), (1, 0), (-1, 0)]


class Car:
    def __init__(self, car_id, src_pos, dst_pos, t_move_avg, t_move_std, t_stop):
        self.car_id = car_id
        self.seq = 0
        self.src_pos = src_pos
        self.dst_pos = dst_pos
        self.cur_pos = src_pos
        self.last_pos = src_pos
        self.t_move_avg = t_move_avg
        self.t_move_std = t_move_std
        self.t_stop = t_stop

    def move(self, step_code):
        if step_code != 0:
            time.sleep(random.gauss(self.t_move_avg, self.t_move_std))
        else:
            time.sleep(self.t_stop)
        self.seq += 1
        self.last_pos = self.cur_pos
        offset = OFFSETS[step_code]
        self.cur_pos = (self.cur_pos[0] + offset[0], self.cur_pos[1] + offset[1])
        if self.cur_pos == self.dst_pos:
            self.src_pos, self.dst_pos = self.dst_pos, self.src_pos

    def reset(self):
        self.seq = 0
        self.last_pos = self.cur_pos

    def enter_recovery_mode(self, nonce):
        self.seq = nonce

    def in_recovery_mode(self):
        return self.seq < 0


class ClientProcess(multiprocessing.Process):
    def __init__(self, car, server_addrs, t_retry_base, t_retry_ai, t_retry_md,
                 t_recover_avg, t_recover_std, log_filename):
        super(ClientProcess, self).__init__()
        self.car = car
        self.server_addrs = server_addrs
        self.log_filename = log_filename
        self.t_retry_base = t_retry_base
        self.t_retry = t_retry_base
        self.t_retry_ai = t_retry_ai
        self.t_retry_md = t_retry_md
        self.t_recover_avg = t_recover_avg
        self.t_recover_std = t_recover_std

    def run(self):
        log_file = open(self.log_filename, 'w')

        def log(msg_type, msg):
            log_file.write(f'[{msg_type}] {datetime.datetime.now()} {msg}\n')
            log_file.flush()

        def make_stub(server_addr):
            channel = grpc.insecure_channel(f"{server_addr['host']}:{server_addr['port']}")
            return guide_pb2_grpc.GuideStub(channel)

        def make_car_state(car):
            return guide_pb2.CarState(
                car_id=car.car_id,
                seq=car.seq,
                cur_pos=guide_pb2.CarState.Position(
                    row_idx=car.cur_pos[0],
                    col_idx=car.cur_pos[1],
                ),
                last_pos=guide_pb2.CarState.Position(
                    row_idx=car.last_pos[0],
                    col_idx=car.last_pos[1],
                ),
                dst_pos=guide_pb2.CarState.Position(
                    row_idx=car.dst_pos[0],
                    col_idx=car.dst_pos[1],
                ),
            )

        def get_next_step(stub, car_state):
            while True:
                try:
                    step = stub.GetNextStep(car_state)
                    self.t_retry = max(self.t_retry - self.t_retry_ai, self.t_retry_base)
                    return step
                except grpc.RpcError as err:
                    log('Error', err.details())
                    time.sleep(self.t_retry)
                    self.t_retry *= self.t_retry_md

        server_addr = random.choice(self.server_addrs)
        stub = make_stub(server_addr)
        log('Info', f'Arrive at {self.car.cur_pos}')
        while True:
            car_state = make_car_state(self.car)
            step = get_next_step(stub, car_state)
            if self.car.in_recovery_mode():
                time.sleep(random.gauss(self.t_recover_avg, self.t_recover_std))
            if step.step_code < 0:
                log('Info', f'Get nonce {step.step_code}')
                self.car.enter_recovery_mode(step.step_code)
            elif step.step_code == 5:
                self.car.reset()
                log('Info', 'Reset')
            else:
                self.car.move(step.step_code)
                log('Info', f'Arrive at {self.car.cur_pos}')


if __name__ == '__main__':
    config = json.load(open('config.json', 'r'))
    
    client_processes = []
    for car_id, car_prop in enumerate(config['car_props']):
        car = Car(
            car_id,
            tuple(car_prop['src_pos']),
            tuple(car_prop['dst_pos']),
            config['t_move_avg'],
            config['t_move_std'],
            config['t_stop'],
        )
        client_process = ClientProcess(
            car,
            config['server_addrs'],
            config['t_retry_base'],
            config['t_retry_ai'],
            config['t_retry_md'],
            config['t_recover_avg'],
            config['t_recover_std'],
            f'logs/client{car_id}.log'
        )
        client_processes.append(client_process)
        client_process.start()
    
    time.sleep(config['duration'])
    for client_process in client_processes:
        client_process.kill()
