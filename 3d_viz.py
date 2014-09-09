import pyglet
from pyglet.gl import *
from pyglet.window import key
from math import pi
from util import *

C_SPEED = 0.1
R_SPEED = 0.03

RED    = (1.0, 0.0, 0.0, 1.0)
GREEN  = (0.0, 1.0, 0.0, 1.0)
BLUE   = (0.0, 0.0, 1.0, 1.0)
WHITE  = (1.0, 1.0, 1.0, 1.0)
LTGREY = (0.5, 0.5, 0.5, 1.0)

# A general OpenGL initialization function.  Sets all of the initial parameters.
def init_gl(w, h):
    glClearColor(0.0, 0.0, 0.0, 0.0)	    # This Will Clear The Background Color To Black
    glClearDepth(1.0)					    # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				    # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)			    	# Enables Depth Testing
    glShadeModel(GL_SMOOTH)			   	    # Enables Smooth Color Shading
    glMatrixMode(GL_MODELVIEW)


def gl_rotate(x_ang, y_ang, z_ang):
    glRotatef(x_ang, 1.0, 0.0, 0.0)
    glRotatef(y_ang, 0.0, 1.0, 0.0)
    glRotatef(z_ang, 0.0, 0.0, 1.0)


def draw_test():
    # Draw some stuff
    glBegin(GL_POLYGON)
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.0)
    glEnd()

    glBegin(GL_QUADS)
    glVertex3f(2, 1.0, 0.0)
    glVertex3f(4, 1.0, 0.0)
    glVertex3f(4, -1.0, 0.0)
    glVertex3f(2, -1.0, 0.0)
    glEnd()
    
    glBegin(GL_LINES)
    glVertex3f(-1, 2, 0)
    glVertex3f(-1, 0, 0)
    glEnd()


def draw_unit_cube():
    glBegin(GL_QUADS);
    glVertex3f( -0.5, -0.5, -0.5)
    glVertex3f( -0.5,  0.5, -0.5)
    glVertex3f(  0.5,  0.5, -0.5)
    glVertex3f(  0.5, -0.5, -0.5)

    glVertex3f(  0.5, -0.5, 0.5 )
    glVertex3f(  0.5,  0.5, 0.5 )
    glVertex3f( -0.5,  0.5, 0.5 )
    glVertex3f( -0.5, -0.5, 0.5 )

    glVertex3f( 0.5, -0.5, -0.5 )
    glVertex3f( 0.5,  0.5, -0.5 )
    glVertex3f( 0.5,  0.5,  0.5 )
    glVertex3f( 0.5, -0.5,  0.5 )

    glVertex3f( -0.5, -0.5,  0.5 )
    glVertex3f( -0.5,  0.5,  0.5 )
    glVertex3f( -0.5,  0.5, -0.5 )
    glVertex3f( -0.5, -0.5, -0.5 )

    glVertex3f(  0.5,  0.5,  0.5 )
    glVertex3f(  0.5,  0.5, -0.5 )
    glVertex3f( -0.5,  0.5, -0.5 )
    glVertex3f( -0.5,  0.5,  0.5 )

    glVertex3f(  0.5, -0.5, -0.5 )
    glVertex3f(  0.5, -0.5,  0.5 )
    glVertex3f( -0.5, -0.5,  0.5 )
    glVertex3f( -0.5, -0.5, -0.5 )
    glEnd();


def draw_box(d, c, a, face_color = WHITE, edge_color = BLUE):
    '''d is the dimensions of the box
       c is the center of the box
       a is the angles the box is rotated around'''
    
    glPushMatrix()
    
    glTranslatef(*c)
    gl_rotate(*a)
    glScalef(*d)
    
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glColor4f(*face_color)
    draw_unit_cube()
    
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glLineWidth(3)
    glEnable(GL_POLYGON_OFFSET_LINE);
    glPolygonOffset(-1, -1);
    glColor4f(*edge_color)
    draw_unit_cube()
    glDisable(GL_POLYGON_OFFSET_LINE)
    
    glPopMatrix()
    

def draw_grid(color = LTGREY):
    glColor4f(*color)
    glLineWidth(2)
    
    glBegin(GL_LINES)
    for x in range(-20, 21, 4):
        glVertex3f(x, 0, -20)
        glVertex3f(x, 0, 20)
        
    for z in range(-20, 21, 4):
        glVertex3f(-20, 0, z)
        glVertex3f(20, 0, z)
    
    glEnd()


def draw_line(start, finish, color=WHITE, width=4):
    glColor4f(*color)
    glLineWidth(width)
    glBegin(GL_LINES)
    glVertex3f(*start)
    glVertex3f(*finish)
    glEnd()


def draw_actuator(act, angles, mount):
   '''mount is in global coordinates, not robot'''
   horiz_ang, vert_ang = 0, 0    # Used to rotate the (0, 0, 1) vector
   pos = mount
   for seg, angs in zip(act, angles):
       horiz_ang += angs[1]
       vert_ang += angs[2]
       new_pos = add(pos,
                     scale(seg["len"],
                           forward_vec(horiz_ang, vert_ang)))
       
       draw_line(pos, new_pos, BLUE)
       pos = new_pos
    
    
def resize_gl(w, h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)  # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(w)/float(h), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
    
class World(pyglet.window.Window):
    def __init__(self):
        config = Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True)
        super(World, self).__init__(700, 500, resizable=True, config=config)
        
        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keyboard)
        
        self.robot = {"body": (4, 2, 8),
                      "actuators": [[{"mount": (2, 0, 3.5), "axis": (0, 1, 0), "len": 0.5},
                                     {"axis": (0, 0, 1), "len": 3},
                                     {"axis": (0, 0, 1), "len": 3}]]}
        
        self.r_center = [0, 2.5, 0]
        self.r_angles = [0, 0, 0]
        
        self.pos = (0, 5, -20.0)
        self.yaw = 0
        self.pitch = 0
        
        init_gl(self.width, self.height)
        pyglet.clock.schedule_interval(self.update, 1/120.0)


    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glLoadIdentity()
        gluLookAt(*(self.pos + add(self.pos, forward_vec(self.yaw, self.pitch)) + (0, 1, 0)))
        
        draw_box(self.robot["body"], self.r_center, map(to_deg, self.r_angles))
        angles = ((0, pi/2, 0), (0, 0, pi/4), (0, 0, -pi/2))
        draw_actuator(self.robot["actuators"][0],
                      angles,
                      robot_to_world(self.robot["actuators"][0][0]["mount"],
                                     self.r_center,
                                     self.r_angles))
        
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
    window = World()
    pyglet.app.run()
