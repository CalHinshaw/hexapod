from math import cos, sin

def sub(a, b):
    return tuple(x-y for x,y in zip(a,b))


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
