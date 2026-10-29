import math

def polar_to_cartesian(cx, cy, radius, angle_deg):
    # angle_deg: 0 at 12 o'clock, clockwise
    rad = math.radians(angle_deg - 90)
    x = cx + radius * math.cos(rad)
    y = cy + radius * math.sin(rad)
    return x, y

def describe_arc(cx, cy, radius, start_angle, end_angle, clockwise=True):
    # start_angle, end_angle in degrees (0 at 12 o'clock)
    x1, y1 = polar_to_cartesian(cx, cy, radius, start_angle)
    x2, y2 = polar_to_cartesian(cx, cy, radius, end_angle)
    
    diff = (end_angle - start_angle) % 360
    if not clockwise:
        diff = (start_angle - end_angle) % 360
    
    large_arc = 1 if diff > 180 else 0
    sweep_flag = 1 if clockwise else 0
    
    d = f"M {x1:.2f} {y1:.2f} A {radius} {radius} 0 {large_arc} {sweep_flag} {x2:.2f} {y2:.2f}"
    return d

def describe_sector(cx, cy, radius, start_angle, end_angle, clockwise=True):
    x1, y1 = polar_to_cartesian(cx, cy, radius, start_angle)
    x2, y2 = polar_to_cartesian(cx, cy, radius, end_angle)
    
    diff = (end_angle - start_angle) % 360
    if not clockwise:
        diff = (start_angle - end_angle) % 360
        
    large_arc = 1 if diff > 180 else 0
    sweep_flag = 1 if clockwise else 0
    
    d = f"M {cx} {cy} L {x1:.2f} {y1:.2f} A {radius} {radius} 0 {large_arc} {sweep_flag} {x2:.2f} {y2:.2f} Z"
    return d

# Clock positions: 12=0 deg, 1=30, 2=60, 3=90, 4=120, 5=150, 6=180, 7=210, 8=240, 9=270, 10=300, 11=330
print("12 to 1 CW sector (30 deg):", describe_sector(150, 150, 100, 0, 30, True))
print("9 to 12 CW sector (90 deg):", describe_sector(150, 150, 100, 270, 0, True))
print("9 to 12 CCW sector (270 deg):", describe_sector(150, 150, 100, 270, 0, False))
