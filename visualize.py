import json
import datetime
import ast
import matplotlib.pyplot as plt
import matplotlib.animation as ani


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


if __name__ == '__main__':
    config = json.load(open('config.json', 'r'))
    car_num = len(config['car_props'])

    pos_log_entries = [
        (car_id, *entry)
        for car_id in range(car_num)
        for entry in get_pos_log(open(f'logs/client{car_id}.log', 'r'))
    ]
    pos_log_entries.sort(key=lambda entry: entry[1])

    fig, ax = plt.subplots()
    ax.axis([-1, config['row_num'], -1, config['col_num']])
    
    texts = [
        ax.text(car_prop['src_pos'][1], car_prop['src_pos'][0], str(car_id), color='r')
        for car_id, car_prop in enumerate(config['car_props'])
    ]

    def update(entry):
        texts[entry[0]].set_x(entry[2][1])
        texts[entry[0]].set_y(entry[2][0])
        if entry[2] == tuple(config['car_props'][entry[0]]['src_pos']) or \
                entry[2] == tuple(config['car_props'][entry[0]]['dst_pos']):
            texts[entry[0]].set_color('r')
        else:
            texts[entry[0]].set_color('b')
        return [texts[entry[0]]]

    animation = ani.FuncAnimation(fig, update, frames=pos_log_entries, interval=800)

    plt.show()
