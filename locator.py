import xmlrpc.server
import json
import log_parser


class LocatorService:
    def __init__(self, car_num):
        self.car_num = car_num

    def locate_cars(self):
        result = []
        for car_id in range(self.car_num):
            log_entries = log_parser.parse_log(f'logs/client{car_id}.log')
            log_entry = next(
                log_entry
                for log_entry in reversed(log_entries)
                if isinstance(log_entry, log_parser.ArriveEntry) or isinstance(log_entry, log_parser.MoveEntry)
            )
            if isinstance(log_entry, log_parser.ArriveEntry):
                result.append([log_entry.pos])
            else:
                result.append([log_entry.from_pos, log_entry.to_pos])
        return result


if __name__ == '__main__':
    config = json.load(open('config.json', 'r'))
    locator_addr = config['locator_addr']
    car_num = len(config['car_tasks'])

    service = LocatorService(car_num)
    server = xmlrpc.server.SimpleXMLRPCServer((locator_addr['host'], locator_addr['port']))
    server.register_instance(service)
    server.serve_forever()
