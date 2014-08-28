from math import pi, sin, cos, asin, acos

def two_joint(l1, l2, mount, target):
    dx, dy = target[0]-mount[0], target[1]-mount[1]
    d = (dx**2 + dy**2)**0.5
    
    # Special cases for when we can't reach the target
    if l1+l2 <= d:
        return ((asin(dy/d), pi-asin(dy/d))[dx <= 0], 0)
    elif d <= abs(l1-l2):
        return ((asin(dy/d), pi-asin(dy/d))[dx <= 0], pi)
    
    a2 = acos((l1**2+l2**2-d**2)/(2*l1*l2))
    a1 = asin(dy/d) + asin(l2*sin(a2)/d)
    
    # Accounting for the quadrants in a way that always keeps the joint
    # above the foot
    return ((a1, pi-a1)[dx<0], (pi-a2, a2+pi)[dx > 0])


def position_body(center, angle, robot):
    """Takes the robot spec and calculates the optimal angle for the actuators.
    Returns a list of lists of angles that correspond with the actuators in the
    robot spec."""
    angles = []
    for actuator in robot["actuators"]:
        mount = robot_to_world(center, angle, actuator[1]["mount"])
        angles.append(two_joint(actuator[0]["len"], actuator[1]["len"], mount, actuator[0]["anchor"]))
    return angles


def robot_to_world(center, angle, p):
    rx, ry = rotate(p, angle)
    return (rx-center[0], ry-center[1])


def world_to_robot(center, angle, p):
    return rotate((p[0]-center[0], p[1]-center[1]), -angle)

    
def rotate(p, angle, c = (0, 0)):
    return (p[0]-c[0])*cos(angle) - (p[1]-c[1])*sin(angle) + c[0], (p[0]-c[0])*sin(angle) + (p[1]-c[1])*cos(angle)+c[1]
