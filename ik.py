from math import pi, asin, acos
from util import *


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
