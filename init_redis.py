import redis
import json


if __name__ == '__main__':
    config = json.load(open('config.json', 'r'))

    r = redis.Redis(config['redis_addr']['host'], config['redis_addr']['port'])
    r.flushall()
