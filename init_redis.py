import redis
import json


if __name__ == '__main__':
    config = json.load(open('config.json', 'r'))
    redis_addr = config['redis_addr']

    r = redis.Redis(redis_addr['host'], redis_addr['port'])
    r.flushall()
