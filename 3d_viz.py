# See original source and C based tutorial at http://nehe.gamedev.net

import pyglet
from pyglet.gl import *
from pyglet.window import key


# A general OpenGL initialization function.  Sets all of the initial parameters.
def init_gl():
    glClearColor(0.0, 0.0, 0.0, 0.0)	    # This Will Clear The Background Color To Black
    glClearDepth(1.0)					    # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				    # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)			    	# Enables Depth Testing
    glShadeModel(GL_SMOOTH)			   	    # Enables Smooth Color Shading
    glMatrixMode(GL_MODELVIEW)


# The main drawing function.
def draw_gl_scene(x, y, z):
    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Set perspective matrix
    glLoadIdentity()
    gluLookAt(x, y, z, 0, 0, 0, 0, 1, 0)

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
        self.x = 0
        self.y = 0
        self.z = -6.0
        init_gl()


    def on_draw(self):
        draw_gl_scene(self.x, self.y, self.z)


    def on_resize(self, w ,h):
        resize_gl(w, h)
        
    
    def on_key_press(self, symbol, modifiers):
       if symbol == key.UP:
           self.y += 0.1
       elif symbol == key.DOWN:
           self.y -= 0.1
       elif symbol == key.LEFT:
           self.x -= 0.1
       elif symbol == key.RIGHT:
           self.x += 0.1
       elif symbol == key.R:
           self.z += 0.1
       elif symbol == key.F:
           self.z -= 0.1
       elif symbol == key.ESCAPE:
           self.dispatch_event('on_close')


if __name__ == "__main__":
    window = World()
    pyglet.app.run()






