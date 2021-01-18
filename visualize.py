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
        def update_position(car_id, pos):
            annoations[car_id].set_x(pos[1])
            annoations[car_id].set_y(pos[0])
            if pos == tuple(car_tasks[car_id]['src_pos']) or pos == tuple(car_tasks[car_id]['dst_pos']):
                annoations[car_id].set_color('red')
                annoations[car_id].get_bbox_patch().set_edgecolor('red')
            else:
                annoations[car_id].set_color('black')
                annoations[car_id].get_bbox_patch().set_edgecolor('black')

        if isinstance(frame[1], log_parser.ArriveEntry):
            update_position(frame[0], frame[1].pos)
        elif isinstance(frame[1], log_parser.MoveEntry):
            pos = ((frame[1].from_pos[0] + frame[1].to_pos[0]) / 2, (frame[1].from_pos[1] + frame[1].to_pos[1]) / 2)
            update_position(frame[0], pos)
        return annoations

    animation = ani.FuncAnimation(fig, update, frames=frames)

    plt.gca().set_aspect('equal')
    plt.show()
