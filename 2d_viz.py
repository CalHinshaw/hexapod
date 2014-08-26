from pyglet import window, gl, graphics, app
from math import sin, cos

config = gl.Config(sample_buffers=1, samples=8)
win = window.Window(700, 500, config=config, resizable=False)
win.set_caption("2D IK Visualizer")

RED   = (1, 0, 0, 1)
WHITE = (0, 0, 0, 1)

target = [20, 20]

mid = (350, 250)
actuator = [{"length": 100, "angle": 2},
            {"length": 60, "angle": 2}]

def draw_point(p, rad, color):
    gl.glPointSize(rad)
    graphics.draw(1, gl.GL_POINTS, ('v2f', target), ('c4f', color))
    

def draw_line(b, e, rad=2):
    gl.glLineWidth(rad)
    graphics.draw(2, gl.GL_LINES, ('v2f', b+e))

def draw_actuator(actuator):
    pos = list(mid)
    ang = 0
    for seg in actuator:
        ang += seg["angle"]
        new_pos = [pos[0]+seg["length"]*cos(ang), pos[1]+seg["length"]*sin(ang)]
        draw_line(pos, new_pos)
        pos = new_pos


@win.event
def on_draw():
    win.clear()
    
    draw_actuator(actuator)
    
    # Draw target
    draw_point(target, 5, RED)
    


@win.event
def on_mouse_press(x, y, button, modifiers):
    target[0], target[1] = x, y

app.run()
