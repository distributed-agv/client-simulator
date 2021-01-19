mkdir -p logs
python3 init_redis.py
python2 simulate.py
python3 profile.py
python3 visualize.py
