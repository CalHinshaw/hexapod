import pyglet
from pyglet.gl import *
from pyglet.window import key
from math import pi
from util import *
from glutil import *

C_SPEED = 0.25
R_SPEED = 0.03


def draw_actuator(act, joint_angles, mount, body_angles):
   '''mount is in global coordinates, not robot'''
   horiz_ang, vert_ang = 0, 0    # Used to rotate the (0, 0, 1) vector
   pos = (0, 0, 0)
   for seg, angs in zip(act, joint_angles):
       horiz_ang += angs[1]
       vert_ang += angs[2]
       new_pos = add(pos,
                     scale(seg["len"],
                           forward_vec(horiz_ang, vert_ang)))
       
       draw_line(robot_to_world(pos, mount, body_angles),
                 robot_to_world(new_pos, mount, body_angles),
                 BLUE)
       pos = new_pos


def draw_robot(robot, r_center, r_angles):
    draw_box(robot["body"], r_center, map(to_deg, r_angles))
    angles = ((0, pi/2, 0), (0, 0, pi/4), (0, 0, -pi/2))
    
    for actuator in robot["actuators"]:
        draw_actuator(actuator,
                      angles,
                      robot_to_world(actuator[0]["mount"],
                                     r_center,
                                     r_angles),
                      r_angles)


def draw_targets(targets):
    glColor4f(*RED)
    glLineWidth(3)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    for target in targets:
        glPushMatrix()
        glTranslatef(*target)
        glScalef(0.25, 0.25, 0.25)
        draw_unit_cube()
        glPopMatrix()

    
class RobotVisualizer(pyglet.window.Window):
    def __init__(self, robot_spec, init_targets):
        config = Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True)
        super(RobotVisualizer, self).__init__(700, 500, resizable=True, config=config)
        
        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keyboard)
        
        self.robot = robot_spec
        self.targets = init_targets
        
        self.r_center = [0, 2.5, 0]
        self.r_angles = [0, 0, 0]
        
        self.pos = (0, 5, -20.0)
        self.yaw = 0
        self.pitch = 0
        
        self.grabbed_target = None
        
        init_gl(self.width, self.height)
        pyglet.clock.schedule_interval(self.update, 1/120.0)


    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glLoadIdentity()
        gluLookAt(*(self.pos + add(self.pos, forward_vec(self.yaw, self.pitch)) + (0, 1, 0)))
        draw_robot(self.robot, self.r_center, self.r_angles)
        draw_targets(self.targets)
        draw_grid()


    def on_resize(self, w ,h):
        resize_gl(w, h)
        
    
    def on_key_press(self, symbol, modifiers):
       if symbol == key.SPACE:
           self.set_exclusive_mouse(True)
       elif symbol == key.ESCAPE:
           self.dispatch_event('on_close')
    
    
    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.set_exclusive_mouse(False)
    
    
    def on_mouse_motion(self, x, y, dx, dy):
        if not self.keyboard[key.SPACE]:
            return
        
        if dx != 0:
            self.yaw -= (dx*pi)/(self.width*2.0)
        
        if dy != 0:
            self.pitch += (dy*pi)/(self.width*2.0)
        
        if self.pitch < -(pi/2.0)*0.95:
            self.pitch = -(pi/2.0)*0.95
        elif self.pitch > (pi/2.0)*0.95:
            self.pitch = (pi/2.0)*0.95


    def on_mouse_press(self, x, y, button, modifiers):
        # calculate the ray
        dx, dy = dx - self.width, dy - self.width
        yaw = self.yaw - (dx*pi)/(self.width*2.0)
        pitch = self.pitch + (dy*pi)/(self.width*2.0)
        ray = forward_vec(yaw, pitch)
        
        # look for intersections with the list of targets
        
        
        # grab the target
    
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # if we're grabbing a target calculate the ray
        # calc intersections with the ground
        # move the target
    
    
    def on_mouse_release(self, x, y, button, modifiers):
        # release the target
        self.grabbed_target = None
    
    
    # Update function called by clock.schedule_interval
    def update(self, dt):
        # Move camera
        if self.keyboard[key.W]:
            self.pos = add(self.pos, scale(C_SPEED, forward_vec(self.yaw, self.pitch)))
        
        if self.keyboard[key.S]:
            self.pos = add(self.pos, scale(-C_SPEED, forward_vec(self.yaw, self.pitch)))
            
        if self.keyboard[key.D]:
            self.pos = add(self.pos, scale(C_SPEED, right_vec(self.yaw, self.pitch)))
            
        if self.keyboard[key.A]:
            self.pos = add(self.pos, scale(-C_SPEED, right_vec(self.yaw, self.pitch)))
        
        # Rotate robot body
        if self.keyboard[key.NUM_5]:
            self.r_angles[0] -= R_SPEED
            
        if self.keyboard[key.NUM_2]:
            self.r_angles[0] += R_SPEED
        
        if self.keyboard[key.NUM_1]:
            self.r_angles[2] -= R_SPEED
            
        if self.keyboard[key.NUM_3]:
            self.r_angles[2] += R_SPEED
        
        if self.keyboard[key.NUM_4]:
            self.r_angles[1] -= R_SPEED
            
        if self.keyboard[key.NUM_6]:
            self.r_angles[1] += R_SPEED


if __name__ == "__main__":
    robot = {"body": (4, 2, 8),
             "actuators": [[{"mount": (2, 0, 3.5), "axis": (0, 1, 0), "len": 0.5},
                            {"axis": (0, 0, 1), "len": 3},
                            {"axis": (0, 0, 1), "len": 3}],
                           [{"mount": (2, 0, 0), "axis": (0, 1, 0), "len": 0.5},
                            {"axis": (0, 0, 1), "len": 3},
                            {"axis": (0, 0, 1), "len": 3}],
                           [{"mount": (2, 0, -3.5), "axis": (0, 1, 0), "len": 0.5},
                            {"axis": (0, 0, 1), "len": 3},
                            {"axis": (0, 0, 1), "len": 3}],
                           [{"mount": (-2, 0, 3.5), "axis": (0, 1, 0), "len": 0.5},
                            {"axis": (0, 0, 1), "len": 3},
                            {"axis": (0, 0, 1), "len": 3}],
                           [{"mount": (-2, 0, 0), "axis": (0, 1, 0), "len": 0.5},
                            {"axis": (0, 0, 1), "len": 3},
                            {"axis": (0, 0, 1), "len": 3}],
                           [{"mount": (-2, 0, -3.5), "axis": (0, 1, 0), "len": 0.5},
                            {"axis": (0, 0, 1), "len": 3},
                            {"axis": (0, 0, 1), "len": 3}]]}
                            
    targets = [(4,  0, 3.5),
               (4,  0, 0),
               (4,  0, -3.5),
               (-4, 0, 3.5),
               (-4, 0, 0),
               (-4, 0, -3.5)]

    window = RobotVisualizer(robot, targets)
    pyglet.app.run()
