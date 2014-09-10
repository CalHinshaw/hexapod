from math import cos, sin, pi
import numpy as np

def to_rad(angle):
    return angle * 0.0174532925
    

def to_deg(angle):
    return angle * 57.2957795
    
    
def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x,y in zip(a,b))


def scale(scalar, v):
    return tuple(scalar*x for x in v)


def cross(a, b):
    return (a[1]*b[2]-b[1]*a[2],
            b[0]*a[2]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def vecm(*vec):
    return np.matrix("; ".join(str(x) for x in vec) + "; 1")


def mvec(matrix):
    """Convert a numpy column vector with x, y, z, 1 values to a python tuple
       of the form (x, y, z). The one is stripped."""
    return tuple(matrix.getA1())[0:3]


def rotm(axis, angle):
    c, s = cos(angle), sin(angle)
    x, y, z = axis
    return np.matrix(((c+x*x*(1-c),   x*y*(1-c)-z*s, x*z*(1-c)+y*s, 0),
                      (y*x*(1-c)+z*s, c+y*y*(1-c),   y*z*(1-c)-x*s, 0),
                      (z*x*(1-c)-y*s, z*y*(1-c)+x*s, c+z*z*(1-c),   0),
                      (0,             0,             0,             1)))


def transm(x, y, z):
    return np.matrix(((1, 0, 0, x),
                      (0, 1, 0, y),
                      (0, 0, 1, z),
                      (0, 0, 0, 1)))


def norm(v):
    return scale(1.0/sum((x*x for x in v)), v)


def rotate(p, angle, c = (0, 0)):
    return (p[0]-c[0])*cos(angle) - (p[1]-c[1])*sin(angle) + c[0],\
           (p[0]-c[0])*sin(angle) + (p[1]-c[1])*cos(angle)+c[1]


def robot_to_world(p, center, angles):
    """p is the point we're converting in the robot's coordinate system
       center is the robot's center of rotation in the world's coordinate system
       angles are the robot's angles of rotation around the x, y, and z axies in
       the world's coordinate system"""
    return mvec(transm(*center) *
                rotm((1, 0, 0), angles[0]) *
                rotm((0, 1, 0), angles[1]) *
                rotm((0, 0, 1), angles[2]) *
                vecm(*p))
    
    
def forward_vec(yaw, pitch):
    uv = (cos(pitch)*sin(yaw),
          sin(pitch),
          cos(pitch)*cos(yaw))
    
    return norm(uv)
    
    
def right_vec(yaw, pitch):
    return cross(forward_vec(yaw, pitch), (0, 1, 0))
