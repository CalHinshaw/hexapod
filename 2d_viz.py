from pyglet import window, gl, graphics, app
from math import sin, cos
import ik

config = gl.Config(sample_buffers=1, samples=8)
win = window.Window(700, 500, config=config, resizable=False)
win.set_caption("2D IK Visualizer")

RED   = (1, 0, 0, 1)
BLUE  = (0, 0, 1, 1)
WHITE = (0, 0, 0, 1)

target = [20, 20]
angle = 0

actuator = [{"len": 100, "anchor": (350, 250)},
            {"len": 60}]

robot = {"width": 100, "height": 200,
         "actuators": [[{"len": 100, "anchor": (350, 250)}, {"len": 60, "mount": (0, 0)}],
                       [{"len": 100, "anchor": (350, 250)}, {"len": 60, "mount": (100, 200)}]]}


def draw_point(p, rad, color):
    gl.glPointSize(rad)
    graphics.draw(1, gl.GL_POINTS, ('v2f', p), ('c4f', color))
    

def draw_line(b, e, rad=2):
    gl.glLineWidth(rad)
    graphics.draw(2, gl.GL_LINES, ('v2f', b+e))
    

def draw_rect(w, h, center, angle):
    l, r = center[0]-w/2, center[0]+w/2
    b, t = center[1]-h/2, center[1]+h/2
    graphics.draw(4, gl.GL_QUADS, ('v2f',
        (ik.rotate((l, t), angle, center)+
         ik.rotate((r, t), angle, center)+
         ik.rotate((r, b), angle, center)+
         ik.rotate((l, b), angle, center))))


def draw_actuator(actuator, angles):
    pos = list(actuator[0]["anchor"])
    ang = 0
    for seg, angle in zip(actuator, angles):
        ang += angle
        new_pos = [pos[0]+seg["len"]*cos(ang), pos[1]+seg["len"]*sin(ang)]
        draw_line(pos, new_pos)
        pos = new_pos
        
    draw_point(actuator[0]["anchor"], 5, BLUE)


def draw_robot(robot, center, angle, angles):
    # Draw the robot
    draw_rect(robot["width"], robot["height"], center, angle)
    for actuator, angles in zip(robot["actuators"], ik.position_body(center, angle, robot)):
        draw_actuator(actuator, angles)
    
    # for each actuator draw the actuators


@win.event
def on_draw():
    win.clear()
    
    #draw_actuator(actuator, ik.two_joint(actuator, target))
    
    draw_robot(robot, target, angle, ik.position_body(target, angle, robot))
    
    # Draw target
    draw_point(target, 5, RED)


@win.event
def on_mouse_press(x, y, button, modifiers):
    target[0], target[1] = x, y


@win.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    target[0], target[1] = x, y
    

@win.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global angle
    angle += scroll_y*0.05
    print angle


app.run()
