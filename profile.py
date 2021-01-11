import datetime
import ast
import json


class PosLogReport:
    def __init__(self, work_num, max_time_cost):
        self.work_num = work_num
        self.max_time_cost = max_time_cost


def get_pos_log(log_file):
    result = []
    for line in log_file.readlines():
        tokens = line.split()
        if tokens[0] != '[Info]':
            continue
        dt = datetime.datetime.strptime(f'{tokens[1]} {tokens[2]}', '%Y-%m-%d %H:%M:%S.%f')
        pos = ast.literal_eval(f'{tokens[3]} {tokens[4]}')
        result.append((dt, pos))
    return result


def analyze_pos_log(pos_log, src_pos, dst_pos):
    work_num = 0
    max_time_cost = 0
    work_start_time = pos_log[0][0]
    for entry in pos_log[1:]:
        if entry[1] == dst_pos:
            work_num += 1
            src_pos, dst_pos = dst_pos, src_pos
            max_time_cost = max(max_time_cost, (entry[0] - work_start_time).seconds)
            work_start_time = entry[0]
    if work_num == 0:
        max_time_cost = float('inf')
    return PosLogReport(work_num, max_time_cost)


if __name__ == '__main__':
    config = json.load(open('config.json', 'r'))
    car_num = len(config['car_props'])

    pos_logs = [
        get_pos_log(open(f'logs/client{car_id}.log', 'r'))
        for car_id in range(car_num)
    ]
    
    pos_log_reports = [
        analyze_pos_log(pos_log, tuple(car_prop['src_pos']), tuple(car_prop['dst_pos']))
        for pos_log, car_prop in zip(pos_logs, config['car_props'])
    ]
    avg_work_num = sum([report.work_num for report in pos_log_reports]) / car_num
    avg_max_time_cost = sum([report.max_time_cost for report in pos_log_reports]) / car_num
    print(f'Average works: {avg_work_num}')
    print(f'Average max time cost: {avg_max_time_cost}s')
