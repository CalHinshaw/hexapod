from math import pi, sin, cos, asin, acos

def sub(a, b):
    return tuple(x-y for x,y in zip(a,b))


def two_joint(act, target):
    """act is the actuator's specification
       target is the target position  for the last limb (index 1) in act"""
    l0, l1 = act[0]["len"], act[1]["len"]
    dx, dy = target
    d = (dx**2 + dy**2)**0.5
    
    # Special cases for when we can't reach the target
    if l0+l1 <= d:
        return ((asin(dy/d), pi-asin(dy/d))[dx <= 0], 0)
    elif d <= abs(l0-l1):
        return ((asin(dy/d), pi-asin(dy/d))[dx <= 0], pi)
    
    a1 = acos((l0**2+l1**2-d**2)/(2*l0*l1))
    a0 = asin(dy/d) + asin(l1*sin(a1)/d)
    
    # Accounting for the quadrants in a way that always keeps the joint
    # above the foot
    return ((a0, pi-a0)[dx<0], (pi-a1, a1+pi)[dx>=0])


def position_body(center, angle, robot, targets):
    """Takes the robot spec and calculates the optimal angle for the actuators.
    Returns a list of lists of angles that correspond with the actuators in the
    robot spec."""
    angles = []
    for actuator, target in zip(robot["actuators"], targets):
        mount = robot_to_world(center, angle, actuator[0]["mount"])
        angles.append(two_joint(actuator, sub(target, mount)))
    return angles


def robot_to_world(center, angle, p):
    """p is the point we're converting in the robot's coordinate system
       center is the robot's center of rotation in the world's coordinate system
       angle is the robot's angle of rotation in the world's coordinate system"""
    rx, ry = rotate(p, angle)
    return (center[0]+rx, center[1]+ry)


def world_to_robot(center, angle, p):
    rx, ry = rotate(p, -angle, center)
    return (rx-center[0], ry-center[1])

    
def rotate(p, angle, c = (0, 0)):
    return (p[0]-c[0])*cos(angle) - (p[1]-c[1])*sin(angle) + c[0], (p[0]-c[0])*sin(angle) + (p[1]-c[1])*cos(angle)+c[1]
