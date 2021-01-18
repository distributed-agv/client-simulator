import json
import log_parser


def calc_average_latency(logs):
    latencies = [
        log_entry.latency
        for log in logs
        for log_entry in log
        if isinstance(log_entry, log_parser.LatencyEntry)
    ]
    return sum(latencies) / len(latencies)


if __name__ == '__main__':
    config = json.load(open('config.json', 'r'))
    car_num = len(config['car_tasks'])

    logs = [
        log_parser.parse_log(f'logs/client{car_id}.log')
        for car_id in range(car_num)
    ]

    print(f'Average latency: {calc_average_latency(logs):.2f}ms')
