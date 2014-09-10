from pyglet.gl import *

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


def resize_gl(w, h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)  # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(w)/float(h), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def gl_rotate(x_ang, y_ang, z_ang):
    glRotatef(x_ang, 1.0, 0.0, 0.0)
    glRotatef(y_ang, 0.0, 1.0, 0.0)
    glRotatef(z_ang, 0.0, 0.0, 1.0)


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
    
    
def draw_line(start, finish, color=WHITE, width=4):
    glColor4f(*color)
    glLineWidth(width)
    glBegin(GL_LINES)
    glVertex3f(*start)
    glVertex3f(*finish)
    glEnd()
    
    
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
