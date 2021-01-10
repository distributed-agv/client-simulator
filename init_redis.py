import redis
import json


if __name__ == '__main__':
    config = json.load(open('config.json', 'r'))

    r = redis.Redis(config['redis_addr']['host'], config['redis_addr']['port'])
    r.flushall()
    for car_id, car_prop in enumerate(config['car_props']):
        r.set(f'seq:{car_id}', '0')
        r.hset('owner_map', f"({car_prop['src_pos'][0]},{car_prop['src_pos'][1]})", str(car_id))
