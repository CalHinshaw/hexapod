from pyglet import window, gl, graphics, app
from math import sin, cos
import ik

RED    = (1.0, 0.0, 0.0, 1.0)
GREEN  = (0.0, 1.0, 0.0, 1.0)
BLUE   = (0.0, 0.0, 1.0, 1.0)
WHITE  = (1.0, 1.0, 1.0, 1.0)
LTGREY = (0.5, 0.5, 0.5, 1.0)


def draw_point(p, rad, color):
    gl.glPointSize(rad)
    gl.glColor4f(*color)
    graphics.draw(1, gl.GL_POINTS, ('v2f', p))
    

def draw_line(b, e, rad=2, color = WHITE):
    gl.glLineWidth(rad)
    gl.glColor4f(*color)
    graphics.draw(2, gl.GL_LINES, ('v2f', b+e))
    

def draw_rect(w, h, center, angle, color = LTGREY):
    l, r = center[0]-w/2, center[0]+w/2
    b, t = center[1]-h/2, center[1]+h/2
    gl.glColor4f(*color)
    graphics.draw(4,
                  gl.GL_QUADS,
                  ('v2f', ik.rotate((l, t), angle, center)+
                          ik.rotate((r, t), angle, center)+
                          ik.rotate((r, b), angle, center)+
                          ik.rotate((l, b), angle, center)))


def draw_actuator(actuator, angles, target, bod_center, bod_angle):
    mount = ik.robot_to_world(bod_center, bod_angle, actuator[0]["mount"])
    pos = list(mount)
    ang = 0
    for seg, angle in zip(actuator, angles):
        ang += angle
        new_pos = [pos[0]+seg["len"]*cos(ang), pos[1]+seg["len"]*sin(ang)]
        draw_line(pos, new_pos)
        pos = new_pos
    draw_point(mount, 5, BLUE)
    draw_point(target, 5, RED)


def draw_robot(robot, bod_center, bod_angle, angle_list_list, targets):
    draw_rect(robot["width"], robot["height"], bod_center, bod_angle)
    
    for actuator, angles, target in zip(robot["actuators"], angle_list_list, targets):
        draw_actuator(actuator, angles, target, bod_center, bod_angle)
        
    draw_point(bod_center, 10, GREEN)


class VizWindow(window.Window):
    def __init__(self):
        config = gl.Config(sample_buffers=1, samples=8)
        super(VizWindow, self).__init__(700, 500, config=config, resizable=False)
        self.set_caption("2D IK Visualizer")
        
        self.bod_center = [350, 250]
        self.bod_angle = 0
        
        self.robot = {"width": 100, "height": 200,
                      "actuators": [[{"len": 100, "mount": (-50, -100)}, {"len": 60}],
                                    [{"len": 100, "mount": (50, 100)}, {"len": 60}]]}
        
        self.targets = [(300, 200), (400, 300)]
        
        
    def on_draw(self):
        self.clear()
        draw_robot(self.robot,
                   self.bod_center,
                   self.bod_angle,
                   ik.position_body(self.bod_center, self.bod_angle, self.robot, self.targets),
                   self.targets)


    def on_mouse_press(self, x, y, button, modifiers):
        self.bod_center[0], self.bod_center[1] = x, y


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.bod_center[0], self.bod_center[1] = x, y
        

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.bod_angle += scroll_y*0.05


window = VizWindow()
app.run()
