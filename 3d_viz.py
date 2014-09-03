import pyglet
from pyglet.gl import *
from pyglet.window import key
from math import pi
from util import *


# A general OpenGL initialization function.  Sets all of the initial parameters.
def init_gl():
    glClearColor(0.0, 0.0, 0.0, 0.0)	    # This Will Clear The Background Color To Black
    glClearDepth(1.0)					    # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				    # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)			    	# Enables Depth Testing
    glShadeModel(GL_SMOOTH)			   	    # Enables Smooth Color Shading
    glMatrixMode(GL_MODELVIEW)


# The main drawing function.
def draw_gl_scene(pos, yaw, pitch):
    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Set perspective matrix
    glLoadIdentity()
    gluLookAt(*(pos + add(pos, forward_vec(yaw, pitch)) + (0, 1, 0)))
    
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
        
        self.pos = (0, 0, -6.0)
        self.yaw = 0
        self.pitch = 0
        init_gl()
        pyglet.clock.schedule_interval(self.update, 1/120.0)


    def on_draw(self):
        draw_gl_scene(self.pos, self.yaw, self.pitch)


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
        if self.keyboard[key.W]:
            self.pos = add(self.pos, scale(0.1, forward_vec(self.yaw, self.pitch)))
        
        if self.keyboard[key.S]:
            self.pos = add(self.pos, scale(-0.1, forward_vec(self.yaw, self.pitch)))
            
        if self.keyboard[key.D]:
            self.pos = add(self.pos, scale(0.1, right_vec(self.yaw, self.pitch)))
            
        if self.keyboard[key.A]:
            self.pos = add(self.pos, scale(-0.1, right_vec(self.yaw, self.pitch)))


if __name__ == "__main__":
    window = World()
    pyglet.app.run()
