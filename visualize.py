import json
import log_parser
import matplotlib.pyplot as plt
import matplotlib.animation as ani


if __name__ == '__main__':
    config = json.load(open('config.json', 'r'))
    row_num = config['row_num']
    col_num = config['col_num']
    car_tasks = config['car_tasks']
    car_num = len(car_tasks)

    frames = [
        (car_id, log_entry)
        for car_id in range(car_num)
        for log_entry in log_parser.parse_log(f'logs/client{car_id}.log')
    ]
    frames.sort(key=lambda frame: frame[1].dt)

    fig, ax = plt.subplots()
    ax.axis([-1, col_num, -1, row_num])
    
    for row_idx in range(row_num):
        ax.plot([0, col_num - 1], [row_idx, row_idx], color='black')
    for col_idx in range(col_num):
        ax.plot([col_idx, col_idx], [0, row_num - 1], color='black')
    
    annoations = [
        ax.annotate(
            str(car_id),
            car_task['src_pos'][::-1],
            bbox={
                'boxstyle': 'circle',
                'facecolor': 'white',
                'edgecolor': 'red',
            },
            ha='center',
            va='center',
        )
        for car_id, car_task in enumerate(car_tasks)
    ]

    def update(frame):
        if isinstance(frame[1], log_parser.ArriveEntry):
            annoations[frame[0]].set_x(frame[1].pos[1])
            annoations[frame[0]].set_y(frame[1].pos[0])
            if frame[1].pos == tuple(car_tasks[frame[0]]['src_pos']) or \
                frame[1].pos == tuple(car_tasks[frame[0]]['dst_pos']):
                annoations[frame[0]].set_color('red')
                annoations[frame[0]].get_bbox_patch().set_edgecolor('red')
            else:
                annoations[frame[0]].set_color('black')
                annoations[frame[0]].get_bbox_patch().set_edgecolor('black')
        elif isinstance(frame[1], log_parser.MoveEntry):
            annoations[frame[0]].set_x((frame[1].from_pos[1] + frame[1].to_pos[1]) / 2)
            annoations[frame[0]].set_y((frame[1].from_pos[0] + frame[1].to_pos[0]) / 2)
        return annoations

    animation = ani.FuncAnimation(fig, update, frames=frames)

    plt.gca().set_aspect('equal')
    plt.show()
