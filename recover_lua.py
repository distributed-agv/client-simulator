import redis
import json
import subprocess


if __name__ == '__main__':

    commit_script = open('commit.lua', 'r').read()
    recover_script = open('recover.lua', 'r').read()
    getlock_script = open('getLock.lua', 'r').read()
    

    r = redis.Redis("127.0.0.1", 6380)
    commit_script_sha = r.script_load(commit_script)
    recover_script_sha = r.script_load(recover_script)
    getlock_script_sha = r.script_load(getlock_script)
    

    