import pyglet as pg
from datetime import datetime
import matplotlib.pyplot as plt

WAIT_TIME = 5 #Seconds
WINDOW_WIDTH = 600 #Pixels
WINDOW_HEIGHT = 500 #Pixels
WINDOW_TITLE = "Temperature"
MEMORY_PATH = 'memory.csv'

fig = plt.figure(num=1, facecolor="#E0E0E0", figsize=(8,5))
ax = plt.axes()
ax.set_facecolor("#E0E0E0")
icon = pg.image.load('images/icon.png')
graph = pg.image.load('images/graph.jpg')
sprite = pg.sprite.Sprite(graph, x=0, y=10)

batch = pg.graphics.Batch()

window = pg.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
pg.gl.glClearColor(0.8784313725490196, 0.8784313725490196, 0.8784313725490196, 1) #Background color to light grey


#Read data from .csv file where values are formatted inside,outside\ninside,outside ....
def read_memory(csv_path):
    global head_label
    out_data = []
    try:
        with open(csv_path, "r") as memory:
            content = memory.read()
    except FileNotFoundError:
        head_label.text = "ERROR: Memory file not found!"
        return
    content_rows = content.split('\n')
    content_rows.reverse()
    for val in content_rows:
        if val:
            values = val.split(",")
            out_data.append((float(values[0]), float(values[1])))
    #Return a list of tuples
    return out_data

#Input needs needed as a list of tuples,
#where each tuple(inside_temp, outside_temp)
def get_current_values(data):
    #Data format: [ inside_temp_value , outside_temp_value ]
    max = [-100, -100]
    min = [100, 100]
    avg = [0, 0]
    curr = [data[-1][0], data[-1][1]]
    length = len(data)
    #Loop through data to find the max, min and average values
    for values in data:
        for i, value in enumerate(values):
            if value > max[i]: max[i] = value
            if value < min[i]: min[i] = value
            avg[i] += (value / length)
    #Return 2 dicts. {inside_results}, {outside_results}
    return [{"max": max[x], "min": min[x], "avg": avg[x], "current": curr[x]} for x in range(2)]   

def data_to_graph(figure, data, hours):
    figure.clear()
    length = len(data)
    inside_data = [data[x][0] for x in range(length)]
    outside_data = [data[x][1] for x in range(length)]

    plt.plot(inside_data, color='r', label='Inside temp')
    plt.plot(outside_data, color='b', label='Outside temp')
    plt.xticks(ticks=[x for x in range(24)], labels=hours)
    plt.title("Temperature over the last 24 hours")
    plt.xlabel("Time (HH)")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    figure.savefig('images/graph.jpg', dpi=75)
    return figure


temp_data = read_memory(MEMORY_PATH)
in_data, out_data = get_current_values(temp_data)

head_label = pg.text.Label(text="Currently",
                           bold=True, 
                           color=(64, 64, 64, 255), 
                           font_name="Consolas", 
                           font_size=24, 
                           x=WINDOW_WIDTH//2, 
                           y=WINDOW_HEIGHT-26, 
                           anchor_x='center')

in_label = pg.text.Label(text=f"Inside: {in_data['current']}",
                         color=(64, 64, 64, 255),
                         bold=True, 
                         font_name="Consolas", 
                         font_size=20, 
                         x=WINDOW_WIDTH//2, 
                         y=WINDOW_HEIGHT-60, 
                         anchor_x='center', 
                         width=400, 
                         multiline=True, 
                         align='center')

out_label = pg.text.Label(text=f"Outside: {out_data['current']}",
                          color=(64, 64, 64, 255),
                          bold=True, 
                          font_name="Consolas", 
                          font_size=20, 
                          x=WINDOW_WIDTH//2, 
                          y=WINDOW_HEIGHT-88, 
                          anchor_x='center', 
                          width=400, 
                          multiline=True, 
                          align='center')

window.set_icon(icon)

@window.event
def on_draw():
    window.clear()
    head_label.draw()
    in_label.draw()
    out_label.draw()
    sprite.draw()

def update(dt):
    global sprite, fig, ax
    temp_data = read_memory(MEMORY_PATH)
    horizontal = [((datetime.now().hour - x) % 24) for x in range(24)]
    horizontal.reverse()
    fig = data_to_graph(fig, temp_data, horizontal)
    ax.set_facecolor("#E0E0E0")
    graph = pg.image.load('images/graph.jpg')
    sprite = pg.sprite.Sprite(graph, x=0, y=10)
    in_data, out_data = get_current_values(temp_data)
    in_label.text = f"Inside: {in_data['current']} °C"
    out_label.text = f"Outside: {out_data['current']} °C"

pg.clock.schedule_interval(update, WAIT_TIME)
pg.app.run()