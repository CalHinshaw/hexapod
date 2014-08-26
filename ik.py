from math import pi, sin, cos, asin, acos

def two_joint(actuator, target):
    l1, l2 = actuator[0]["len"], actuator[1]["len"]
    dx, dy = target[0]-actuator[0]["anchor"][0], target[1]-actuator[0]["anchor"][1]
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
