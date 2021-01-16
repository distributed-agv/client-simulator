import ast
import datetime
import re


class LogEntry:
    def __init__(self, dt):
        self.dt = dt


class InfoEntry(LogEntry):
    def __init__(self, dt):
        super(InfoEntry, self).__init__(dt)


class ErrorEntry(LogEntry):
    def __init__(self, dt, msg):
        super(ErrorEntry, self).__init__(dt)
        self.msg = msg


class ArriveEntry(InfoEntry):
    def __init__(self, dt, pos):
        super(ArriveEntry, self).__init__(dt)
        self.pos = pos


class NonceEntry(InfoEntry):
    def __init__(self, dt, nonce):
        super(NonceEntry, self).__init__(dt)
        self.nonce = nonce


class ResetEntry(InfoEntry):
    def __init__(self, dt):
        super(ResetEntry, self).__init__(dt)


def parse_log(filename):
    file = open(filename, 'r')
    result = []
    for line in file.readlines():
        tokens = list(filter(bool, re.split('(\\[.*\\]|<.*>)| ', line)))
        dt = datetime.datetime.strptime(f'{tokens[1]} {tokens[2]}', '%Y-%m-%d %H:%M:%S.%f')
        if tokens[0] == '[ Info]':
            if tokens[3] == '<Arrive>':
                pos = ast.literal_eval(f'{tokens[4]} {tokens[5]}')
                result.append(ArriveEntry(dt, pos))
            elif tokens[3] == '< Nonce>':
                nonce = int(tokens[4])
                result.append(NonceEntry(dt, nonce))
            elif tokens[3] == '< Reset>':
                result.append(ResetEntry(dt))
        elif tokens[0] == '[Error]':
            msg = ' '.join(tokens[3:])
            result.append(ErrorEntry(dt, msg))
    return result