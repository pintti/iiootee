import pyglet as pg
from datetime import datetime
import matplotlib.pyplot as plt

WAIT_TIME = 1       #Seconds
WINDOW_WIDTH = 600  #Pixels
WINDOW_HEIGHT = 500 #Pixels
WINDOW_TITLE = "Temperature"

#Read data from .csv file where values are formatted inside,outside\ninside,outside ....
def read_memory(mem_path):
    out_data = []
    hours = []
    try:
        with open(mem_path, "r") as memory:
            content_rows = memory.readlines()
    except FileNotFoundError:
        return
    for val in content_rows:
        stripped = val.rstrip("\n")
        hour = stripped.split(" ")[0].rstrip(":")
        values = stripped.split(" ")[1]
        if stripped:
            out_data.append((float(values.split(",")[0]), float(values.split(",")[1])))
            hours.append(hour)
    #Return a list of tuples with data and a corresponding list of hours
    return out_data, hours

def get_mem_path():
    date = datetime.now().date()
    path = f"temp/{date}.txt"
    return path

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
        for i, value in enumerate(values[1:2]):
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
    plt.xticks(ticks=[x for x in range(length)], labels=hours)
    plt.title(f"Temperature over the last {length} hours")
    plt.xlabel("Time (H)")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    figure.savefig('images/graph.jpg', dpi=75)
    return figure

def initialize():
    fig = plt.figure(num=1, facecolor="#E0E0E0", figsize=(8,5))
    ax = plt.axes()
    ax.set_facecolor("#E0E0E0")
    icon = pg.image.load('images/icon.png')
    window = pg.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    pg.gl.glClearColor(0.8784313725490196, 0.8784313725490196, 0.8784313725490196, 1) #Background color to light grey
    
    temp_data, hours = read_memory(get_mem_path())
    window.set_icon(icon)
    in_data, out_data = get_current_values(temp_data)
    fig = data_to_graph(fig, temp_data, hours)
    graph = pg.image.load('images/graph.jpg')
    sprite = pg.sprite.Sprite(graph, x=0, y=10)
    return window, fig, ax, in_data, out_data, sprite


head_label = pg.text.Label(text="Currently",
                           bold=True, 
                           color=(64, 64, 64, 255), 
                           font_name="Consolas", 
                           font_size=24, 
                           x=WINDOW_WIDTH//2, 
                           y=WINDOW_HEIGHT-26, 
                           anchor_x='center')

def update(dt):
    #Update the sprites and labels according to the memory file
    global sprite, fig, ax
    temp_data, hours = read_memory(get_mem_path())                     #Read data from csv
    fig = data_to_graph(fig, temp_data, hours)                         #Update the existing figure and save as jpg
    ax.set_facecolor("#E0E0E0")                                        #Reset axis color to match bg
    graph = pg.image.load('images/graph.jpg')                          #Load graph
    sprite = pg.sprite.Sprite(graph, x=0, y=10)                        #Set graph as sprite
    in_data, out_data = get_current_values(temp_data)                  #Get max, min, avg and current values from memory contents
    in_label.text = f"Inside: {in_data['current']} °C"                 #Update labels
    out_label.text = f"Outside: {out_data['current']} °C"              #Update labels

window, fig, ax, in_data, out_data, sprite = initialize()
 
in_label = pg.text.Label(text=f"Inside: {in_data['current']} °C",
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

out_label = pg.text.Label(text=f"Outside: {out_data['current']} °C",
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


@window.event
def on_draw():
    window.clear()
    head_label.draw()
    in_label.draw()
    out_label.draw()
    sprite.draw()

pg.clock.schedule_interval(update, WAIT_TIME)
pg.app.run()