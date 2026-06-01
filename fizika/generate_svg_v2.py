import math

def get_marker():
    return """
    <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="black" />
        </marker>
        <marker id="arrow_red" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="red" />
        </marker>
        <marker id="arrow_blue" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="blue" />
        </marker>
    </defs>
    """

def generate():
    scale = 40
    A_x, A_y = 150, 450
    
    # AE
    alfa = 330.0
    l1, l2 = 6.0, 3.0
    E_x = A_x + l1 * scale * math.cos(math.radians(alfa))
    E_y = A_y - l1 * scale * math.sin(math.radians(alfa))
    B_x = A_x + l2 * scale * math.cos(math.radians(alfa))
    B_y = A_y - l2 * scale * math.sin(math.radians(alfa))
    
    # BD
    l3, l4 = 8.0, 4.0
    D_x = B_x + l3 * scale
    D_y = B_y
    C_x = B_x + (l3 - l4) * scale # Wait, distance from D is l4=4.0. So C is exactly at l3-l4 = 4 from B.
    # Ah, D is at x = B_x + 8*scale. C is at D_x - 4*scale = B_x + 4*scale.
    C_y = B_y
    
    # Forces
    delta = 90.0
    gamma = 100.0
    F1_x = E_x + 50 * math.cos(math.radians(delta))
    F1_y = E_y - 50 * math.sin(math.radians(delta))
    
    F2_base_x = D_x - 2.0 * scale
    F2_base_y = D_y
    F2_x = F2_base_x + 60 * math.cos(math.radians(gamma))
    F2_y = F2_base_y - 60 * math.sin(math.radians(gamma))

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body{{font-family:'Times New Roman',serif;margin:40px;font-size:15px;line-height:1.6}}
.eq{{margin-left: 20px;}}
.schema-container{{text-align:center; margin: 30px 0; page-break-inside: avoid;}}
svg text{{font-family: 'Times New Roman', serif; font-size: 14px;}}
</style>
</head>
<body>

<h2 style="text-align:center;">Užduoties schema:</h2>
<div class="schema-container">
<svg width="700" height="500" viewBox="0 0 700 500">
    {get_marker()}
    
    <!-- Supports -->
    <!-- A: nepalsankus -->
    <path d="M {A_x} {A_y} L {A_x-15} {A_y+20} L {A_x+15} {A_y+20} Z" fill="none" stroke="black" stroke-width="2"/>
    <line x1="{A_x-20}" y1="{A_y+20}" x2="{A_x+20}" y2="{A_y+20}" stroke="black" stroke-width="2"/>
    <!-- lines under support -->
    <line x1="{A_x-15}" y1="{A_y+20}" x2="{A_x-25}" y2="{A_y+30}" stroke="black"/>
    <line x1="{A_x-5}" y1="{A_y+20}" x2="{A_x-15}" y2="{A_y+30}" stroke="black"/>
    <line x1="{A_x+5}" y1="{A_y+20}" x2="{A_x-5}" y2="{A_y+30}" stroke="black"/>
    <line x1="{A_x+15}" y1="{A_y+20}" x2="{A_x+5}" y2="{A_y+30}" stroke="black"/>
    
    <!-- D: paslankus horizontaliai -->
    <circle cx="{D_x-10}" cy="{D_y+25}" r="5" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="{D_x+10}" cy="{D_y+25}" r="5" fill="none" stroke="black" stroke-width="2"/>
    <path d="M {D_x} {D_y} L {D_x-15} {D_y+20} L {D_x+15} {D_y+20} Z" fill="none" stroke="black" stroke-width="2"/>
    <line x1="{D_x-25}" y1="{D_y+30}" x2="{D_x+25}" y2="{D_y+30}" stroke="black" stroke-width="2"/>
    
    <!-- C: paslankus lygiagretus BD -->
    <circle cx="{C_x}" cy="{C_y+20}" r="5" fill="none" stroke="black" stroke-width="2"/>
    <path d="M {C_x} {C_y} L {C_x-10} {C_y+15} L {C_x+10} {C_y+15} Z" fill="none" stroke="black" stroke-width="2"/>
    <line x1="{C_x-15}" y1="{C_y+25}" x2="{C_x+15}" y2="{C_y+25}" stroke="black" stroke-width="2"/>

    <!-- Bodies -->
    <line x1="{A_x}" y1="{A_y}" x2="{E_x}" y2="{E_y}" stroke="black" stroke-width="4" />
    <line x1="{B_x}" y1="{B_y}" x2="{D_x}" y2="{D_y}" stroke="black" stroke-width="4" />
    
    <circle cx="{A_x}" cy="{A_y}" r="4" fill="white" stroke="black" stroke-width="2"/>
    <text x="{A_x+15}" y="{A_y+10}" font-weight="bold" font-size="16">A</text>
    
    <circle cx="{B_x}" cy="{B_y}" r="4" fill="white" stroke="black" stroke-width="2"/>
    <text x="{B_x}" y="{B_y+20}" font-weight="bold" font-size="16">B</text>
    
    <circle cx="{D_x}" cy="{D_y}" r="4" fill="white" stroke="black" stroke-width="2"/>
    <text x="{D_x+20}" y="{D_y-10}" font-weight="bold" font-size="16">D</text>
    
    <text x="{C_x-10}" y="{C_y-10}" font-weight="bold" font-size="16">C</text>
    
    <text x="{E_x-20}" y="{E_y-10}" font-weight="bold" font-size="16">E</text>

    <!-- Angles -->
    <!-- Alfa 330 from A -->
    <line x1="{A_x}" y1="{A_y}" x2="{A_x+60}" y2="{A_y}" stroke="gray" stroke-dasharray="4" />
    <path d="M {A_x+40} {A_y} A 40 40 0 1 0 {A_x + 40*math.cos(math.radians(-30))} {A_y + 40*math.sin(math.radians(-30))}" fill="none" stroke="black" />
    <text x="{A_x+50}" y="{A_y-20}">&alpha;</text>

    <!-- Forces -->
    <line x1="{F1_x}" y1="{F1_y}" x2="{E_x}" y2="{E_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    <text x="{F1_x-10}" y="{F1_y-10}" font-style="italic" font-weight="bold">F&#8321;</text>

    <line x1="{F2_x}" y1="{F2_y}" x2="{F2_base_x}" y2="{F2_base_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    <text x="{F2_x-20}" y="{F2_y-10}" font-style="italic" font-weight="bold">F&#8322;</text>
    
    <!-- Distributed Loads -->
    <!-- q2 on BD from 2 to 6 from D -> x from D_x-6*scale to D_x-2*scale -->
    <!-- D is at right, B is at left. D_x = B_x + 320. q2 starts at D_x-2*40 = D_x-80, ends at D_x-6*40 = D_x-240 -->
    <rect x="{D_x-6*scale}" y="{D_y-30}" width="{4*scale}" height="30" fill="none" stroke="black"/>
    <line x1="{D_x-6*scale}" y1="{D_y-30}" x2="{D_x-6*scale}" y2="{D_y}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{D_x-5*scale}" y1="{D_y-30}" x2="{D_x-5*scale}" y2="{D_y}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{D_x-4*scale}" y1="{D_y-30}" x2="{D_x-4*scale}" y2="{D_y}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{D_x-3*scale}" y1="{D_y-30}" x2="{D_x-3*scale}" y2="{D_y}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{D_x-2*scale}" y1="{D_y-30}" x2="{D_x-2*scale}" y2="{D_y}" stroke="black" marker-end="url(#arrow)"/>
    <text x="{D_x-4*scale}" y="{D_y-35}" font-style="italic">q&#8322;</text>

    <!-- q11 on AE. From 1m to 3m from A. Triangle max at A+1m, 0 at A+3m (which is B). -->
    <!-- Wait, q11=3.5, q12=0. Base at l5 (1m), tip at l5+l6 (3m). -->
    <!-- Vectors perpendicular to AE. -->
    <g transform="translate({A_x}, {A_y}) rotate(30)">
        <polygon points="{1*scale},0 {1*scale},-40 {3*scale},0" fill="none" stroke="black"/>
        <line x1="{1.0*scale}" y1="-40" x2="{1.0*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <line x1="{1.5*scale}" y1="-30" x2="{1.5*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <line x1="{2.0*scale}" y1="-20" x2="{2.0*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <line x1="{2.5*scale}" y1="-10" x2="{2.5*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <text x="{1.5*scale}" y="-45" font-style="italic" transform="rotate(-30, {1.5*scale}, -45)">q&#8311;&#8321;</text>
    </g>

    <!-- Moments -->
    <!-- M1=5.5 positive CCW at A (or somewhere on AE) -->
    <!-- Draw curved arrow at A -->
    <path d="M {A_x+30} {A_y-10} A 30 30 0 1 0 {A_x-10} {A_y-30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="{A_x-25}" y="{A_y-35}" font-style="italic" font-weight="bold">M&#8321;</text>
    
    <!-- M2=3.0 positive CCW on BD (let's say near B) -->
    <path d="M {B_x+50} {B_y+10} A 30 30 0 1 0 {B_x+20} {B_y-30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="{B_x+20}" y="{B_y-35}" font-style="italic" font-weight="bold">M&#8322;</text>

</svg>
</div>

<h2 style="text-align:center;">Skaičiuojamoji schema:</h2>
<div class="schema-container">
<svg width="700" height="500" viewBox="0 0 700 500">
    {get_marker()}
    
    <!-- Bodies -->
    <line x1="{A_x}" y1="{A_y}" x2="{E_x}" y2="{E_y}" stroke="gray" stroke-width="4" />
    <line x1="{B_x}" y1="{B_y}" x2="{D_x}" y2="{D_y}" stroke="gray" stroke-width="4" />
    
    <!-- A Reactions -->
    <line x1="{A_x-50}" y1="{A_y}" x2="{A_x}" y2="{A_y}" stroke="blue" stroke-width="2" marker-end="url(#arrow_blue)"/>
    <text x="{A_x-45}" y="{A_y-5}" fill="blue" font-weight="bold">R<tspan dy="5" font-size="10">Ax</tspan></text>
    <line x1="{A_x}" y1="{A_y+50}" x2="{A_x}" y2="{A_y}" stroke="blue" stroke-width="2" marker-end="url(#arrow_blue)"/>
    <text x="{A_x+5}" y="{A_y+45}" fill="blue" font-weight="bold">R<tspan dy="5" font-size="10">Ay</tspan></text>
    
    <!-- D Reaction -->
    <line x1="{D_x}" y1="{D_y+50}" x2="{D_x}" y2="{D_y}" stroke="blue" stroke-width="2" marker-end="url(#arrow_blue)"/>
    <text x="{D_x+5}" y="{D_y+45}" fill="blue" font-weight="bold">R<tspan dy="5" font-size="10">D</tspan></text>
    
    <!-- C Reaction -->
    <line x1="{C_x}" y1="{C_y+50}" x2="{C_x}" y2="{C_y}" stroke="blue" stroke-width="2" marker-end="url(#arrow_blue)"/>
    <text x="{C_x+5}" y="{C_y+45}" fill="blue" font-weight="bold">R<tspan dy="5" font-size="10">C</tspan></text>

    <!-- F1, F2 -->
    <line x1="{F1_x}" y1="{F1_y}" x2="{E_x}" y2="{E_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    <text x="{F1_x-10}" y="{F1_y-10}" font-style="italic" font-weight="bold">F&#8321;</text>
    <line x1="{F2_x}" y1="{F2_y}" x2="{F2_base_x}" y2="{F2_base_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    <text x="{F2_x-20}" y="{F2_y-10}" font-style="italic" font-weight="bold">F&#8322;</text>
    
    <!-- Q1, Q2 -->
    <!-- Q2 at center of q2 -> D_x - 4*scale -->
    <line x1="{D_x-4*scale}" y1="{D_y-50}" x2="{D_x-4*scale}" y2="{D_y}" stroke="red" stroke-width="2" marker-end="url(#arrow_red)"/>
    <text x="{D_x-4*scale+5}" y="{D_y-30}" fill="red" font-style="italic" font-weight="bold">Q&#8322;</text>
    
    <!-- Q1 at a1 = 1.667 from A -->
    <g transform="translate({A_x}, {A_y}) rotate(30)">
        <line x1="{1.667*scale}" y1="-50" x2="{1.667*scale}" y2="0" stroke="red" stroke-width="2" marker-end="url(#arrow_red)"/>
        <text x="{1.667*scale+5}" y="-25" fill="red" font-style="italic" font-weight="bold" transform="rotate(-30, {1.667*scale+5}, -25)">Q&#8321;</text>
    </g>

    <!-- Moments -->
    <path d="M {A_x+30} {A_y-10} A 30 30 0 1 0 {A_x-10} {A_y-30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="{A_x-25}" y="{A_y-35}" font-style="italic" font-weight="bold">M&#8321;</text>
    <path d="M {B_x+50} {B_y+10} A 30 30 0 1 0 {B_x+20} {B_y-30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="{B_x+20}" y="{B_y-35}" font-style="italic" font-weight="bold">M&#8322;</text>
</svg>
</div>

</body>
</html>
"""
    
    with open('/Users/ugniusvaitiekenas/srotas-ai-agent/fizika/namu_darbas.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated full HTML with accurate SVGs.")

generate()
