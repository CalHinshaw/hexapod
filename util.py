from math import cos, sin

def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x,y in zip(a,b))


def cross(a, b):
    return (a[1]*b[2]-b[1]*a[2],
            b[0]*a[2]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


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
    
    
def unit_vec(yaw, pitch):
    uv =   (sin(pitch)*sin(yaw),
            cos(pitch)*cos(yaw),
            -sin(pitch)*cos(yaw))
    #print uv
    #print sum((x**2 for x in uv))**0.5
    
    return uv
    
    
    
    
    
    
    
