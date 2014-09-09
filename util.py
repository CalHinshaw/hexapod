from math import cos, sin, pi

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


def norm(v):
    return scale(1.0/sum((x*x for x in v)), v)


def rotate(p, angle, c = (0, 0)):
    return (p[0]-c[0])*cos(angle) - (p[1]-c[1])*sin(angle) + c[0],\
           (p[0]-c[0])*sin(angle) + (p[1]-c[1])*cos(angle)+c[1]


def robot_to_world(center, angle, p):
    """p is the point we're converting in the robot's coordinate system
       center is the robot's center of rotation in the world's coordinate system
       angle is the robot's angle of rotation in the world's coordinate system"""
    rx, ry = rotate(p, angle)
    return (center[0]+rx, center[1]+ry)


def world_to_robot(center, angle, p):
    rx, ry = rotate(p, -angle, center)
    return (rx-center[0], ry-center[1])
    
    
def forward_vec(yaw, pitch):
    uv = (cos(pitch)*sin(yaw),
          sin(pitch),
          cos(pitch)*cos(yaw))
    
    return norm(uv)
    
    
def right_vec(yaw, pitch):
    return cross(forward_vec(yaw, pitch), (0, 1, 0))
