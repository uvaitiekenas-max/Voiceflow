import math

def get_svg_arc(cx, cy, r, start_angle, end_angle):
    # Angles in degrees. SVG y is down, so we need to negate angles.
    # Start and end should be in standard math coordinates (y up).
    # But for SVG, drawing arc means computing points.
    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    x1 = cx + r * math.cos(start_rad)
    y1 = cy - r * math.sin(start_rad)
    x2 = cx + r * math.cos(end_rad)
    y2 = cy - r * math.sin(end_rad)
    large_arc = 1 if abs(end_angle - start_angle) > 180 else 0
    # Sweep flag depends on whether we draw CW or CCW. Usually CCW in math is CW in SVG (because y is flipped).
    # If start to end is CCW in math, it goes from larger angle to smaller in SVG, so sweep is 0.
    return f"M {x1} {y1} A {r} {r} 0 {large_arc} 0 {x2} {y2}"

def generate():
    scale = 40
    
    A_x, A_y = 150, 300
    
    # AE parameters
    l1 = 6.0
    l2 = 3.0
    alfa = 330.0 # Standard CCW math angle. Means -30 in math, or 30 degrees down-right.
    
    E_x = A_x + l1 * scale * math.cos(math.radians(alfa))
    E_y = A_y - l1 * scale * math.sin(math.radians(alfa))
    
    B_x = A_x + l2 * scale * math.cos(math.radians(alfa))
    B_y = A_y - l2 * scale * math.sin(math.radians(alfa))
    
    # BD parameters
    l3 = 8.0
    l4 = 4.0
    beta = 0.0 # Horizontal right
    
    D_x = B_x + l3 * scale
    D_y = B_y
    
    C_x = B_x + l4 * scale
    C_y = B_y
    
    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body{font-family:'Times New Roman',serif;margin:40px;font-size:14px;line-height:1.6}
.eq{margin-left: 20px;}
</style>
</head>
<body>
"""

    # Schema 1: Original
    svg1 = f"""
    <div style="text-align:center; margin-bottom:40px;">
    <h3>Užduoties schema:</h3>
    <svg width="800" height="400" viewBox="0 0 800 400" style="border: 1px solid #ccc;">
        <!-- Axes -->
        <line x1="{A_x}" y1="{A_y}" x2="{A_x+100}" y2="{A_y}" stroke="gray" stroke-dasharray="4" />
        <line x1="{A_x}" y1="{A_y}" x2="{A_x}" y2="{A_y-100}" stroke="gray" stroke-dasharray="4" />
        
        <!-- Angles -->
        <path d="{get_svg_arc(A_x, A_y, 40, 0, 330)}" fill="none" stroke="black" />
        <text x="{A_x+45}" y="{A_y-15}" font-size="12">&alpha;=330&deg;</text>
        
        <!-- AE -->
        <line x1="{A_x}" y1="{A_y}" x2="{E_x}" y2="{E_y}" stroke="black" stroke-width="4" />
        <circle cx="{A_x}" cy="{A_y}" r="5" fill="white" stroke="black" stroke-width="2"/>
        <text x="{A_x-15}" y="{A_y+15}" font-weight="bold">A</text>
        <text x="{E_x-15}" y="{E_y-15}" font-weight="bold">E</text>
        
        <!-- BD -->
        <line x1="{B_x}" y1="{B_y}" x2="{D_x}" y2="{D_y}" stroke="black" stroke-width="4" />
        <circle cx="{B_x}" cy="{B_y}" r="5" fill="white" stroke="black" stroke-width="2"/>
        <text x="{B_x-10}" y="{B_y+25}" font-weight="bold">B</text>
        
        <circle cx="{C_x}" cy="{C_y}" r="5" fill="white" stroke="black" stroke-width="2"/>
        <text x="{C_x}" y="{C_y-15}" font-weight="bold">C</text>
        
        <circle cx="{D_x}" cy="{D_y}" r="5" fill="white" stroke="black" stroke-width="2"/>
        <text x="{D_x+10}" y="{D_y-10}" font-weight="bold">D</text>
        
        <!-- F1 at E (90 deg = UP) -->
        <line x1="{E_x}" y1="{E_y+40}" x2="{E_x}" y2="{E_y}" stroke="red" stroke-width="2" marker-end="url(#arrow)" />
        <text x="{E_x+5}" y="{E_y+20}" fill="red" font-weight="bold">F&#8321;</text>
        
        <!-- F2 on BD -->
        <line x1="{D_x-2*scale}" y1="{D_y-40}" x2="{D_x-2*scale}" y2="{D_y}" stroke="red" stroke-width="2" marker-end="url(#arrow)" />
        <text x="{D_x-2*scale+5}" y="{D_y-20}" fill="red" font-weight="bold">F&#8322;</text>
        
        <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="red" />
            </marker>
        </defs>
    </svg>
    </div>
    """
    
    html += svg1 + "</body></html>"
    
    with open('/Users/ugniusvaitiekenas/srotas-ai-agent/fizika/namu_darbas2.html', 'w', encoding='utf-8') as f:
        f.write(html)

generate()
