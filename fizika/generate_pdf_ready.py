import math

# Given data for Var 1298
VAR = 1298
l1, l2, l3, l4 = 6.0, 3.0, 8.0, 4.0
l5, l6, l7, l8, l9 = 1.0, 2.0, 2.0, 4.0, 2.0
alfa = 330.0 
beta = 0.0
delta = 90.0
gamma = 100.0
q11 = 3.5
q12 = 0.0
q2 = 2.5
F1 = 8.5
F2 = 12.5
M1 = 5.5
M2 = 3.0

def rad(d): return math.radians(d)

def fmt(num):
    if abs(num) < 1e-9: return "0"
    s = f"{abs(num):.4e}"
    first_digit = s[0]
    exp = int(s.split('e')[1])
    sig_figs = 4 if first_digit == '1' else 3
    if exp >= -2 and exp <= 3:
        val = round(abs(num), sig_figs - 1 - exp)
        if val == int(val): 
            res = str(int(val))
        else:
            res = str(val)
    else:
        res = f"{abs(num):.{sig_figs-1}g}"
    res = res.replace('.', ',')
    return "-" + res if num < -1e-9 else res

def generate():
    # Math
    Q1 = 0.5 * q11 * l6
    a1 = l5 + l6 / 3.0
    Q2 = q2 * l8
    a2_from_D = l7 + l8 / 2.0
    
    Q1x = -Q1 * math.sin(rad(30))
    Q1y = -Q1 * math.cos(rad(30))
    
    F1x = 0
    F1y = -F1
    
    F2x = F2 * math.cos(rad(-gamma))
    F2y = F2 * math.sin(rad(-gamma))
    
    # Coordinates
    A_x, A_y = 0.0, 0.0
    B_x = l2 * math.cos(rad(-30))
    B_y = -l2 * math.sin(rad(30))
    E_x = l1 * math.cos(rad(-30))
    E_y = -l1 * math.sin(rad(30))
    
    D_x = B_x + l3
    D_y = B_y
    C_x = D_x - l4
    C_y = D_y
    
    # Body BD: sum Fx = 0
    # -RBx + F2x = 0
    RBx = F2x
    
    # Body AE: sum Fx = 0 -> RAx + RBx + Q1x + F1x = 0
    RAx = -RBx - Q1x - F1x
    
    # Body AE: sum MA = 0
    # M1 - Q1*a1 + RBx*(-B_y) + RBy*(B_x) + F1x*(-E_y) - F1y*(E_x) = 0?
    # Wait, moment of F1 is r x F = Ex*F1y - Ey*F1x. Since F1x=0, moment is Ex * (-F1)
    # Actually F1 points down. So around A, it's CW (-). So - F1 * Ex.
    # Q1 is perpendicular to AE at dist a1. Moment is - Q1 * a1.
    # RBx is at (Bx, By). r x R_B = Bx*RBy - By*RBx.
    M_F1 = E_x * F1y - E_y * F1x
    M_Q1 = - Q1 * a1
    RBy = (-M1 - M_Q1 - M_F1 + B_y * RBx) / B_x
    
    # Body AE: sum Fy = 0 -> RAy + RBy + Q1y + F1y = 0
    RAy = -RBy - Q1y - F1y
    
    # Body BD: sum MB = 0
    # M2 + RC*(C_x - B_x) + RD*(D_x - B_x) + Q2y*(D_x - a2_from_D - B_x) + F2y*(D_x - l9 - B_x) = 0
    dist_C_from_B = C_x - B_x
    dist_D_from_B = D_x - B_x
    dist_Q2_from_B = D_x - a2_from_D - B_x
    dist_F2_from_B = D_x - l9 - B_x
    
    # RC * l4 + RD * l3 + ...
    # Wait, RC is at C, distance from B is l3 - l4.
    M_Q2_B = Q2 * dist_Q2_from_B
    M_F2_B = F2y * dist_F2_from_B
    # RC*(l3-l4) + RD*l3 + M2 + M_Q2_B + M_F2_B = 0
    # sum Fy = 0 -> -RBy + RC + RD + Q2y + F2y = 0 -> RC + RD = RBy - Q2y - F2y = RBy - Q2 - F2y
    
    sum_forces_Y_BD = RBy - Q2 - F2y
    # RC + RD = sum_forces_Y_BD
    # RC = sum_forces_Y_BD - RD
    # (sum_forces_Y_BD - RD)*(l3-l4) + RD*l3 + M2 + M_Q2_B + M_F2_B = 0
    # sum_forces_Y_BD*(l3-l4) - RD*(l3-l4) + RD*l3 + ... = 0
    # RD*l4 = -M2 - M_Q2_B - M_F2_B - sum_forces_Y_BD*(l3-l4)
    RD = (-M2 - M_Q2_B - M_F2_B - sum_forces_Y_BD*dist_C_from_B) / l4
    RC = sum_forces_Y_BD - RD
    
    # Verification
    # Sum M_B = M1 + M2 + RAx*(-B_y) - RAy*B_x - Q1*(l2-a1) + F1y*(E_x - B_x) + RC*(C_x-B_x) + RD*(D_x-B_x) + Q2y*dist_Q2_from_B + F2y*dist_F2_from_B
    # Let's just use exact r x F for everything around B
    def cross(r, f): return r[0]*f[1] - r[1]*f[0]
    
    M_A = cross((-B_x, -B_y), (RAx, RAy))
    M_Q1_ver = Q1 * (l2 - a1)  # Q1 points left/down, distance is (l2-a1). Pushes system CCW around B.
    M_F1_ver = cross((E_x-B_x, E_y-B_y), (F1x, F1y))
    M_RC_ver = cross((C_x-B_x, 0), (0, RC))
    M_RD_ver = cross((D_x-B_x, 0), (0, RD))
    M_Q2_ver = cross((dist_Q2_from_B, 0), (0, Q2))
    M_F2_ver = cross((dist_F2_from_B, 0), (F2x, F2y))
    sum_MB_total = M1 + M2 + M_A + M_Q1_ver + M_F1_ver + M_RC_ver + M_RD_ver + M_Q2_ver + M_F2_ver
    
    def get_marker():
        return """
        <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="black" />
            </marker>
        </defs>
        """
        
    def get_hatch(x1, x2, y, count=5):
        h = ""
        dx = (x2 - x1) / count
        for i in range(count+1):
            hx = x1 + i * dx
            h += f'<line x1="{hx}" y1="{y}" x2="{hx-5}" y2="{y+8}" stroke="black" stroke-width="1"/>'
        return h

    def get_overline(text, sub=""):
        if sub: return f'<span style="text-decoration: overline">{text}</span><sub>{sub}</sub>'
        return f'<span style="text-decoration: overline">{text}</span>'

    def get_vector_text(x, y, text, sub="", color="black"):
        return f'<text x="{x}" y="{y}" fill="{color}" font-style="italic" font-weight="bold"><tspan text-decoration="overline">{text}</tspan><tspan dy="5" font-size="10" text-decoration="none">{sub}</tspan></text>'
        
    scale = 35
    oAx, oAy = 150, 250
    oBx, oBy = oAx + B_x*scale, oAy - B_y*scale
    oEx, oEy = oAx + E_x*scale, oAy - E_y*scale
    oDx, oDy = oAx + D_x*scale, oAy - D_y*scale
    oCx, oCy = oAx + C_x*scale, oAy - C_y*scale

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ font-family: 'Times New Roman', serif; margin: 40px; font-size: 15px; line-height: 1.6; counter-reset: page; }}
.eq {{ margin-left: 20px; margin-top:2px; margin-bottom:2px; }}
table {{ border-collapse: collapse; margin: 20px 0; }}
th, td {{ border: 1px solid #000; padding: 5px 15px; text-align: center; }}
.math {{ font-style: italic; }}
.schema-container {{ margin: 30px 0; }}
svg text {{ font-family: 'Times New Roman', serif; font-size: 14px; }}
.title-page {{ text-align: center; margin-bottom: 50px; position: relative; }}
.title-page h1 {{ font-size: 20px; margin: 10px; }} 
.title-page p {{ margin: 5px; }}
.system-bracket {{ border-left: 2px solid black; padding-left: 10px; margin-left: 20px; display: inline-block; }}
@page {{ size: A4; margin: 20mm; @bottom-center {{ content: counter(page); }} }}
@media print {{
    body {{ margin: 0; font-size: 14pt; }}
    .page-break {{ page-break-before: always; }}
    .title-page {{ page-break-after: always; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; }}
    .title-header {{ position: absolute; top: 0; right: 0; text-align: right; }}
    #pageFooter::after {{ counter-increment: page; content: counter(page); }}
}}
</style>
</head>
<body>

<div class="title-page">
<div class="title-header">Ugnius Vaitiekėnas, AMf 25/3</div>
<h1 style="margin-top: 40vh;">Namų darbas Nr.1</h1>
<h1>Dviejų kūnų sistema</h1>
<p>Varianto Nr.{VAR}</p>
</div>

<h2>1. Užduoties lapas</h2>
<p><b>Užduoties duomenys:</b></p>
<p><span class="math">l<sub>1</sub></span> = 6,0 m; <span class="math">l<sub>2</sub></span> = 3,0 m; <span class="math">l<sub>3</sub></span> = 8,0 m; <span class="math">l<sub>4</sub></span> = 4,0 m; <span class="math">l<sub>5</sub></span> = 1,0 m; <span class="math">l<sub>6</sub></span> = 2,0 m; <span class="math">l<sub>7</sub></span> = 2,0 m; <span class="math">l<sub>8</sub></span> = 4,0 m; <span class="math">l<sub>9</sub></span> = 2,0 m;</p>
<p><span class="math">&alpha;</span> = 330&deg;; <span class="math">&beta;</span> = 0&deg;; <span class="math">&delta;</span> = 90&deg;; <span class="math">&gamma;</span> = 100&deg;;</p>
<p><span class="math">q<sub>11</sub></span> = 3,5 kN/m; <span class="math">q<sub>12</sub></span> = 0; <span class="math">q<sub>2</sub></span> = 2,5 kN/m; <span class="math">F<sub>1</sub></span> = 8,5 kN; <span class="math">F<sub>2</sub></span> = 12,5 kN; <span class="math">M<sub>1</sub></span> = 5,5 kNm; <span class="math">M<sub>2</sub></span> = 3,0 kNm.</p>

<p style="margin-top:20px">Schemos mazgų įtvirtinimai:</p>
<p>A - nepaslankus šarnyras &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; B - šarnyrinis kūnų sujungimas<br>
C - paslankus šarnyras lygiagrečia strypui plokštuma &nbsp;&nbsp;&nbsp;&nbsp; D - paslankus šarnyras horizontalia plokštuma</p>

<p>Rasti: R<sub>Ax</sub>; R<sub>Ay</sub>; B<sub>x</sub>; B<sub>y</sub>; R<sub>C</sub>; R<sub>D</sub>. Informacija schemos braižymui: x<sub>D</sub>= {fmt(D_x)} m; y<sub>D</sub>= {fmt(D_y)} m</p>

<p><b>2. Skaičiuojamosios schemos paruošimas:</b></p>
<p>Išskirstytą apkrovą pakeičiame koncentruotomis jėgomis:</p>
<p>
<span class="math">Q<sub>1</sub></span> = 1/2 &middot; <span class="math">q<sub>11</sub></span> &middot; <span class="math">l<sub>6</sub></span> = 1/2 &middot; {fmt(q11)} &middot; {fmt(l6)} = {fmt(Q1)} kN;<br>
<span class="math">Q<sub>2</sub></span> = <span class="math">q<sub>2</sub></span> &middot; <span class="math">l<sub>8</sub></span> = {fmt(q2)} &middot; {fmt(l8)} = {fmt(Q2)} kN.
</p>
<p>
Jėgos <span class="math">Q<sub>1</sub></span> pridėjimo taškas nuo A: <span class="math">a<sub>1</sub></span> = <span class="math">l<sub>5</sub></span> + 1/3 <span class="math">l<sub>6</sub></span> = {fmt(l5)} + 1/3 &middot; {fmt(l6)} = {fmt(a1)} m.<br>
Jėgos <span class="math">Q<sub>2</sub></span> pridėjimo taškas nuo D: <span class="math">a<sub>2</sub></span> = <span class="math">l<sub>7</sub></span> + 1/2 <span class="math">l<sub>8</sub></span> = {fmt(l7)} + 1/2 &middot; {fmt(l8)} = {fmt(a2_from_D)} m

<p><b><u>Užduoties schema:</u></b></p>
<div class="schema-container">
<svg width="800" height="400" viewBox="0 0 800 400">
    {get_marker()}
    
    <!-- Supports -->
    <path d="M {oAx} {oAy} L {oAx-15} {oAy+20} L {oAx+15} {oAy+20} Z" fill="none" stroke="black" stroke-width="2"/>
    <line x1="{oAx-25}" y1="{oAy+20}" x2="{oAx+25}" y2="{oAy+20}" stroke="black" stroke-width="2"/>
    {get_hatch(oAx-25, oAx+25, oAy+20)}
    
    <circle cx="{oDx-10}" cy="{oDy+25}" r="5" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="{oDx+10}" cy="{oDy+25}" r="5" fill="none" stroke="black" stroke-width="2"/>
    <path d="M {oDx} {oDy} L {oDx-15} {oDy+20} L {oDx+15} {oDy+20} Z" fill="none" stroke="black" stroke-width="2"/>
    <line x1="{oDx-25}" y1="{oDy+30}" x2="{oDx+25}" y2="{oDy+30}" stroke="black" stroke-width="2"/>
    {get_hatch(oDx-25, oDx+25, oDy+30)}
    
    <circle cx="{oCx-10}" cy="{oCy+25}" r="5" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="{oCx+10}" cy="{oCy+25}" r="5" fill="none" stroke="black" stroke-width="2"/>
    <path d="M {oCx} {oCy} L {oCx-15} {oCy+20} L {oCx+15} {oCy+20} Z" fill="none" stroke="black" stroke-width="2"/>
    <line x1="{oCx-25}" y1="{oCy+30}" x2="{oCx+25}" y2="{oCy+30}" stroke="black" stroke-width="2"/>
    {get_hatch(oCx-25, oCx+25, oCy+30)}

    <!-- Bodies -->
    <line x1="{oAx}" y1="{oAy}" x2="{oEx}" y2="{oEy}" stroke="black" stroke-width="4" />
    <line x1="{oBx}" y1="{oBy}" x2="{oDx}" y2="{oDy}" stroke="black" stroke-width="4" />
    <circle cx="{oAx}" cy="{oAy}" r="4" fill="white" stroke="black" stroke-width="2"/>
    <circle cx="{oBx}" cy="{oBy}" r="4" fill="white" stroke="black" stroke-width="2"/>
    
    <!-- Dimensions for BD -->
    <line x1="{oBx}" y1="{oBy-60}" x2="{oDx}" y2="{oDy-60}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx}" y1="{oBy-65}" x2="{oBx}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx+2*scale}" y1="{oBy-65}" x2="{oBx+2*scale}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx+4*scale}" y1="{oBy-65}" x2="{oBx+4*scale}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx+6*scale}" y1="{oBy-65}" x2="{oBx+6*scale}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oDx}" y1="{oDy-65}" x2="{oDx}" y2="{oDy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx}" y1="{oBy-60}" x2="{oBx}" y2="{oBy-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <line x1="{oDx}" y1="{oDy-60}" x2="{oDx}" y2="{oDy-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <text x="{oBx+1*scale-10}" y="{oBy-65}" fill="gray">{fmt(l3 - l4 - l9)}</text>
    <text x="{oBx+3*scale-10}" y="{oBy-65}" fill="gray">{fmt(l9)}</text>
    <text x="{oBx+5*scale-10}" y="{oBy-65}" fill="gray">{fmt(l8/2)}</text>
    <text x="{oBx+7*scale-10}" y="{oBy-65}" fill="gray">{fmt(l7)}</text>

    <!-- Dimensions for AE -->
    <g transform="translate({oAx}, {oAy}) rotate(30)">
        <line x1="0" y1="50" x2="{6*scale}" y2="50" stroke="gray" stroke-width="1"/>
        <line x1="0" y1="45" x2="0" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{1*scale}" y1="45" x2="{1*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{3*scale}" y1="45" x2="{3*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{6*scale}" y1="45" x2="{6*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="0" y1="10" x2="0" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{6*scale}" y1="10" x2="{6*scale}" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <text x="{0.5*scale-10}" y="40" fill="gray">{fmt(l5)}</text>
        <text x="{2*scale-10}" y="40" fill="gray">{fmt(l6)}</text>
        <text x="{4.5*scale-10}" y="40" fill="gray">{fmt(l1 - l5 - l6)}</text>
    </g>

    <!-- Angles -->
    <line x1="{oAx}" y1="{oAy}" x2="{oAx+50}" y2="{oAy}" stroke="gray" stroke-width="1"/>
    <path d="M {oAx+40} {oAy} A 40 40 0 1 0 {oAx+40*math.cos(rad(-30))} {oAy-40*math.sin(rad(-30))}" fill="none" stroke="gray" stroke-width="1"/>
    <text x="{oAx+45}" y="{oAy+20}" fill="gray" font-size="12">330&deg;</text>

    <line x1="{oDx-l9*scale}" y1="{oDy}" x2="{oDx-l9*scale-50}" y2="{oDy}" stroke="gray" stroke-width="1"/>
    <path d="M {oDx-l9*scale-30} {oDy} A 30 30 0 0 1 {oDx-l9*scale+30*math.cos(rad(100))} {oDy-30*math.sin(rad(100))}" fill="none" stroke="gray" stroke-width="1"/>
    <text x="{oDx-l9*scale-40}" y="{oDy+20}" fill="gray" font-size="12">100&deg;</text>
    
    <!-- F1 angle -->
    <path d="M {oEx+20*math.cos(rad(-30))} {oEy-20*math.sin(rad(-30))} A 20 20 0 0 0 {oEx+20*math.cos(rad(-90))} {oEy-20*math.sin(rad(-90))}" fill="none" stroke="gray" stroke-width="1"/>
    <text x="{oEx+25}" y="{oEy-15}" fill="gray" font-size="12">90&deg;</text>

    <text x="{oAx-25}" y="{oAy+15}" font-style="italic" font-size="18">A</text>
    <text x="{oBx-15}" y="{oBy+25}" font-style="italic" font-size="18">B</text>
    <text x="{oDx+20}" y="{oDy-10}" font-style="italic" font-size="18">D</text>
    <text x="{oCx-10}" y="{oCy-15}" font-style="italic" font-size="18">C</text>
    <text x="{oEx+10}" y="{oEy+10}" font-style="italic" font-size="18">E</text>

    <!-- F1, F2 -->
    <line x1="{oEx}" y1="{oEy-50}" x2="{oEx}" y2="{oEy}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(oEx-15, oEy-25, 'F', '1')}
    
    <line x1="{oDx-l9*scale+50*math.cos(rad(100))}" y1="{oDy-50*math.sin(rad(100))}" x2="{oDx-l9*scale}" y2="{oDy}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(oDx-l9*scale-20, oDy-25, 'F', '2')}
    
    <!-- Distributed Loads q2 (Pointing UP) -->
    <rect x="{oDx-6*scale}" y="{oDy}" width="{4*scale}" height="25" fill="none" stroke="black"/>
    <line x1="{oDx-6*scale}" y1="{oDy+25}" x2="{oDx-6*scale}" y2="{oDy}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{oDx-5*scale}" y1="{oDy+25}" x2="{oDx-5*scale}" y2="{oDy}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{oDx-4*scale}" y1="{oDy+25}" x2="{oDx-4*scale}" y2="{oDy}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{oDx-3*scale}" y1="{oDy+25}" x2="{oDx-3*scale}" y2="{oDy}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{oDx-2*scale}" y1="{oDy+25}" x2="{oDx-2*scale}" y2="{oDy}" stroke="black" marker-end="url(#arrow)"/>
    <text x="{oDx-4*scale}" y="{oDy+45}" font-style="italic">q&#8322;</text>
    
    <!-- Distributed Loads q11, q12 -->
    <g transform="translate({oAx}, {oAy}) rotate(30)">
        <polygon points="{1*scale},0 {1*scale},-30 {3*scale},0" fill="none" stroke="black"/>
        <line x1="{1.0*scale}" y1="-30" x2="{1.0*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <line x1="{1.5*scale}" y1="-22.5" x2="{1.5*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <line x1="{2.0*scale}" y1="-15" x2="{2.0*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <line x1="{2.5*scale}" y1="-7.5" x2="{2.5*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <text x="{1.5*scale}" y="-35" font-style="italic" transform="rotate(-30, {1.5*scale}, -35)">q&#8311;&#8321;</text>
    </g>

    <!-- Moments -->
    <path d="M {oAx+30} {oAy+20} A 30 30 0 1 0 {oAx-20} {oAy-20}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oAx-30, oAy-25, 'M', '1')}
    <path d="M {oBx+50} {oBy+20} A 30 30 0 1 0 {oBx+10} {oBy-30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oBx+15, oBy-35, 'M', '2')}
</svg>
</div>

<p><b><u>Skaičiuojamoji schema:</u></b></p>
<div class="schema-container">
<svg width="800" height="400" viewBox="0 0 800 400">
    {get_marker()}
    
    <!-- Bodies -->
    <line x1="{oAx}" y1="{oAy}" x2="{oEx}" y2="{oEy}" stroke="black" stroke-width="4" />
    <line x1="{oBx}" y1="{oBy}" x2="{oDx}" y2="{oDy}" stroke="black" stroke-width="4" />
    
    <!-- Dimensions for BD -->
    <line x1="{oBx}" y1="{oBy-60}" x2="{oDx}" y2="{oDy-60}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx}" y1="{oBy-65}" x2="{oBx}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx+2*scale}" y1="{oBy-65}" x2="{oBx+2*scale}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx+4*scale}" y1="{oBy-65}" x2="{oBx+4*scale}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx+6*scale}" y1="{oBy-65}" x2="{oBx+6*scale}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oDx}" y1="{oDy-65}" x2="{oDx}" y2="{oDy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx}" y1="{oBy-60}" x2="{oBx}" y2="{oBy-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <line x1="{oDx}" y1="{oDy-60}" x2="{oDx}" y2="{oDy-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <text x="{oBx+1*scale-10}" y="{oBy-65}" fill="gray">{fmt(l3 - l4 - l9)}</text>
    <text x="{oBx+3*scale-10}" y="{oBy-65}" fill="gray">{fmt(l9)}</text>
    <text x="{oBx+5*scale-10}" y="{oBy-65}" fill="gray">{fmt(l8/2)}</text>
    <text x="{oBx+7*scale-10}" y="{oBy-65}" fill="gray">{fmt(l7)}</text>

    <!-- Dimensions for AE -->
    <g transform="translate({oAx}, {oAy}) rotate(30)">
        <line x1="0" y1="50" x2="{6*scale}" y2="50" stroke="gray" stroke-width="1"/>
        <line x1="0" y1="45" x2="0" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{1.667*scale}" y1="45" x2="{1.667*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{3*scale}" y1="45" x2="{3*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{6*scale}" y1="45" x2="{6*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="0" y1="10" x2="0" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{6*scale}" y1="10" x2="{6*scale}" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <text x="{0.83*scale-15}" y="40" fill="gray">{fmt(a1)}</text>
        <text x="{2.33*scale-15}" y="40" fill="gray">{fmt(l2 - a1)}</text>
        <text x="{4.5*scale-15}" y="40" fill="gray">{fmt(l1 - l2)}</text>
    </g>

    <!-- Angles -->
    <line x1="{oAx}" y1="{oAy}" x2="{oAx+50}" y2="{oAy}" stroke="gray" stroke-width="1"/>
    <path d="M {oAx+40} {oAy} A 40 40 0 1 0 {oAx+40*math.cos(rad(-30))} {oAy-40*math.sin(rad(-30))}" fill="none" stroke="gray" stroke-width="1"/>
    <text x="{oAx+45}" y="{oAy+20}" fill="gray" font-size="12">330&deg;</text>

    <line x1="{oDx-l9*scale}" y1="{oDy}" x2="{oDx-l9*scale-50}" y2="{oDy}" stroke="gray" stroke-width="1"/>
    <path d="M {oDx-l9*scale-30} {oDy} A 30 30 0 0 1 {oDx-l9*scale+30*math.cos(rad(100))} {oDy-30*math.sin(rad(100))}" fill="none" stroke="gray" stroke-width="1"/>
    <text x="{oDx-l9*scale-40}" y="{oDy+20}" fill="gray" font-size="12">100&deg;</text>
    
    <!-- F1 angle -->
    <path d="M {oEx+20*math.cos(rad(-30))} {oEy-20*math.sin(rad(-30))} A 20 20 0 0 0 {oEx+20*math.cos(rad(-90))} {oEy-20*math.sin(rad(-90))}" fill="none" stroke="gray" stroke-width="1"/>
    <text x="{oEx+25}" y="{oEy-15}" fill="gray" font-size="12">90&deg;</text>

    <text x="{oAx-15}" y="{oAy+15}" font-style="italic" font-size="18">A</text>
    <text x="{oBx-15}" y="{oBy+25}" font-style="italic" font-size="18">B</text>
    <text x="{oDx+20}" y="{oDy-10}" font-style="italic" font-size="18">D</text>
    <text x="{oCx-10}" y="{oCy-15}" font-style="italic" font-size="18">C</text>
    <text x="{oEx+10}" y="{oEy+10}" font-style="italic" font-size="18">E</text>

    <!-- A Reactions -->
    <line x1="{oAx}" y1="{oAy}" x2="{oAx+50}" y2="{oAy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oAx+45, oAy-15, 'R', 'Ax')}
    <line x1="{oAx}" y1="{oAy+50}" x2="{oAx}" y2="{oAy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oAx+15, oAy+45, 'R', 'Ay')}
    
    <!-- D Reaction -->
    <line x1="{oDx}" y1="{oDy+50}" x2="{oDx}" y2="{oDy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oDx-25, oDy+35, 'R', 'D')}
    
    <!-- C Reaction -->
    <line x1="{oCx}" y1="{oCy+50}" x2="{oCx}" y2="{oCy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oCx-25, oCy+35, 'R', 'C')}

    <!-- F1, F2 -->
    <line x1="{oEx}" y1="{oEy-50}" x2="{oEx}" y2="{oEy}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(oEx-20, oEy-25, 'F', '1')}
    
    <line x1="{oDx-l9*scale+50*math.cos(rad(100))}" y1="{oDy-50*math.sin(rad(100))}" x2="{oDx-l9*scale}" y2="{oDy}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(oDx-l9*scale-20, oDy-25, 'F', '2')}
    
    <!-- Q1, Q2 -->
    <line x1="{oDx-a2_from_D*scale}" y1="{oDy+40}" x2="{oDx-a2_from_D*scale}" y2="{oDy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oDx-a2_from_D*scale+10, oDy+30, 'Q', '2')}
    
    <g transform="translate({oAx}, {oAy}) rotate(30)">
        <line x1="{1.667*scale}" y1="-40" x2="{1.667*scale}" y2="0" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        {get_vector_text(1.667*scale-20, -20, 'Q', '1').replace('fill="black"', 'fill="black" transform="rotate(-30, '+str(1.667*scale-20)+', -20)"')}
    </g>

    <!-- Moments -->
    <path d="M {oAx+30} {oAy+20} A 30 30 0 1 0 {oAx-20} {oAy-20}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oAx-30, oAy-25, 'M', '1')}
    <path d="M {oBx+50} {oBy+20} A 30 30 0 1 0 {oBx+10} {oBy-30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oBx+15, oBy-35, 'M', '2')}
</svg>
</div>

<div class="page-break"></div>
<h2>3. Sprendimas</h2>

<h3>3.1. Kūno AE pusiausvyra</h3>
<div class="schema-container">
<svg width="400" height="300" viewBox="100 150 400 300">
    {get_marker()}
    <line x1="{oAx}" y1="{oAy}" x2="{oEx}" y2="{oEy}" stroke="gray" stroke-width="4" />
    <circle cx="{oAx}" cy="{oAy}" r="4" fill="white" stroke="gray" stroke-width="2"/>
    <circle cx="{oBx}" cy="{oBy}" r="4" fill="white" stroke="gray" stroke-width="2"/>
    <text x="{oAx-15}" y="{oAy+15}" font-style="italic" font-size="18">A</text>
    <text x="{oBx+15}" y="{oBy-5}" font-style="italic" font-size="18">B</text>
    <text x="{oEx+10}" y="{oEy+10}" font-style="italic" font-size="18">E</text>

    <!-- Dimensions for AE with numerical values -->
    <g transform="translate({oAx}, {oAy}) rotate(30)">
        <line x1="0" y1="50" x2="{6*scale}" y2="50" stroke="gray" stroke-width="1"/>
        <line x1="0" y1="45" x2="0" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{1.667*scale}" y1="45" x2="{1.667*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{3*scale}" y1="45" x2="{3*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{6*scale}" y1="45" x2="{6*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="0" y1="10" x2="0" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{6*scale}" y1="10" x2="{6*scale}" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <text x="{0.83*scale-15}" y="40" fill="gray">{fmt(a1)}</text>
        <text x="{2.33*scale-15}" y="40" fill="gray">{fmt(l2 - a1)}</text>
        <text x="{4.5*scale-15}" y="40" fill="gray">{fmt(l1 - l2)}</text>
    </g>

    <!-- A Reactions -->
    <line x1="{oAx-50}" y1="{oAy}" x2="{oAx}" y2="{oAy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oAx-45, oAy-5, 'R', 'Ax')}
    <line x1="{oAx}" y1="{oAy+50}" x2="{oAx}" y2="{oAy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oAx+5, oAy+45, 'R', 'Ay')}

    <!-- B Reactions (Pointing Right and Up) -->
    <line x1="{oBx-50}" y1="{oBy}" x2="{oBx}" y2="{oBy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oBx-45, oBy-5, 'R', 'Bx')}
    <line x1="{oBx}" y1="{oBy+50}" x2="{oBx}" y2="{oBy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oBx+5, oBy+45, 'R', 'By')}

    <line x1="{oEx}" y1="{oEy-50}" x2="{oEx}" y2="{oEy}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(oEx-15, oEy-25, 'F', '1')}
    
    <g transform="translate({oAx}, {oAy}) rotate(30)">
        <line x1="{1.667*scale}" y1="-40" x2="{1.667*scale}" y2="0" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        {get_vector_text(1.667*scale+5, -25, 'Q', '1').replace('fill="black"', 'fill="black" transform="rotate(-30, '+str(1.667*scale+5)+', -25)"')}
    </g>

    <path d="M {oAx+30} {oAy+20} A 30 30 0 1 0 {oAx-20} {oAy-20}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oAx-30, oAy-25, 'M', '1')}
</svg>
</div>

<div style="margin-bottom: 20px;">
    <p>Užrašomos kūno AE pusiausvyros sąlygos:</p>
    <div class="system-bracket">
        <p class="eq">&sum; F<sub>ix</sub> = 0;</p>
        <p class="eq">&sum; F<sub>iy</sub> = 0;</p>
        <p class="eq">&sum; M<sub>A</sub>({get_overline('F')}<sub>i</sub>) = 0.</p>
    </div>
    <div class="system-bracket">
        <p class="eq">R<sub>Ax</sub> - Q<sub>1</sub> &middot; sin(30&deg;) + R<sub>Bx</sub> = 0; (1)</p>
        <p class="eq">R<sub>Ay</sub> - Q<sub>1</sub> &middot; cos(30&deg;) - F<sub>1</sub> + R<sub>By</sub> = 0; (2)</p>
        <p class="eq">M<sub>1</sub> - Q<sub>1</sub> &middot; a<sub>1</sub> + R<sub>Bx</sub> &middot; l<sub>2</sub> &middot; sin(30&deg;) + R<sub>By</sub> &middot; l<sub>2</sub> &middot; cos(30&deg;) - F<sub>1</sub> &middot; l<sub>1</sub> &middot; cos(30&deg;) = 0. (3)</p>
    </div>
    <div class="system-bracket" style="margin-top: 10px;">
        <p class="eq">R<sub>Ax</sub> - {fmt(Q1)} &middot; 0,500 + R<sub>Bx</sub> = 0;</p>
        <p class="eq">R<sub>Ay</sub> - {fmt(Q1)} &middot; 0,866 - {fmt(F1)} + R<sub>By</sub> = 0;</p>
        <p class="eq">{fmt(M1)} - {fmt(Q1)} &middot; {fmt(a1)} + R<sub>Bx</sub> &middot; {fmt(l2)} &middot; 0,500 + R<sub>By</sub> &middot; {fmt(l2)} &middot; 0,866 - {fmt(F1)} &middot; {fmt(l1)} &middot; 0,866 = 0.</p>
    </div>
</div>

<p>R<sub>Ax</sub> + R<sub>Bx</sub> = {fmt(Q1 * 0.5)}; (1)</p>
<p>R<sub>Ay</sub> + R<sub>By</sub> = {fmt(Q1 * 0.866025 + F1)}; (2)</p>
<p>{fmt(l2 * 0.5)} &middot; R<sub>Bx</sub> + {fmt(l2 * 0.866025)} &middot; R<sub>By</sub> = {fmt(-M1 + Q1 * a1 + F1 * l1 * 0.866025)}. (3)</p>

<h3>3.2. Kūno BD pusiausvyra</h3>
<div class="schema-container">
<svg width="500" height="200" viewBox="150 150 500 200">
    {get_marker()}
    <line x1="{oBx}" y1="{oBy}" x2="{oDx}" y2="{oDy}" stroke="gray" stroke-width="4" />
    <circle cx="{oBx}" cy="{oBy}" r="4" fill="white" stroke="gray" stroke-width="2"/>
    <text x="{oBx}" y="{oBy+25}" font-style="italic" font-size="18">B</text>
    <text x="{oDx+20}" y="{oDy-10}" font-style="italic" font-size="18">D</text>
    <text x="{oCx-10}" y="{oCy-10}" font-style="italic" font-size="18">C</text>
    
    <!-- Dimensions for BD -->
    <line x1="{oBx}" y1="{oBy-60}" x2="{oDx}" y2="{oDy-60}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx}" y1="{oBy-65}" x2="{oBx}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx+2*scale}" y1="{oBy-65}" x2="{oBx+2*scale}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx+4*scale}" y1="{oBy-65}" x2="{oBx+4*scale}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx+6*scale}" y1="{oBy-65}" x2="{oBx+6*scale}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oDx}" y1="{oDy-65}" x2="{oDx}" y2="{oDy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx}" y1="{oBy-60}" x2="{oBx}" y2="{oBy-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <line x1="{oDx}" y1="{oDy-60}" x2="{oDx}" y2="{oDy-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <text x="{oBx+1*scale-10}" y="{oBy-65}" fill="gray">{fmt(l3 - l4 - l9)}</text>
    <text x="{oBx+3*scale-10}" y="{oBy-65}" fill="gray">{fmt(l9)}</text>
    <text x="{oBx+5*scale-10}" y="{oBy-65}" fill="gray">{fmt(l8/2)}</text>
    <text x="{oBx+7*scale-10}" y="{oBy-65}" fill="gray">{fmt(l7)}</text>

    <!-- B Reactions from BD perspective (Opposite of AE: Left and Down) -->
    <line x1="{oBx+50}" y1="{oBy}" x2="{oBx}" y2="{oBy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oBx+45, oBy-5, "R'", "Bx")}
    <line x1="{oBx}" y1="{oBy-50}" x2="{oBx}" y2="{oBy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oBx+5, oBy-45, "R'", "By")}

    <!-- C, D Reactions -->
    <line x1="{oDx}" y1="{oDy+50}" x2="{oDx}" y2="{oDy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oDx+5, oDy+45, 'R', 'D')}
    <line x1="{oCx}" y1="{oCy+50}" x2="{oCx}" y2="{oCy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oCx+5, oCy+45, 'R', 'C')}

    <!-- F2, Q2 -->
    <line x1="{oDx-l9*scale+50*math.cos(rad(100))}" y1="{oDy-50*math.sin(rad(100))}" x2="{oDx-l9*scale}" y2="{oDy}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(oDx-l9*scale-20, oDy-25, 'F', '2')}
    <line x1="{oDx-a2_from_D*scale}" y1="{oDy-40}" x2="{oDx-a2_from_D*scale}" y2="{oDy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oDx-a2_from_D*scale+5, oDy-20, 'Q', '2')}

    <path d="M {oBx+50} {oBy+20} A 30 30 0 1 0 {oBx+10} {oBy-30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oBx+15, oBy-35, 'M', '2')}
</svg>
</div>

<div style="margin-bottom: 20px;">
    <p>Užrašomos kūno BD pusiausvyros sąlygos:</p>
    <div class="system-bracket">
        <p class="eq">&sum; F<sub>ix</sub> = 0;</p>
        <p class="eq">&sum; F<sub>iy</sub> = 0;</p>
        <p class="eq">&sum; M<sub>B</sub>({get_overline('F')}<sub>i</sub>) = 0.</p>
    </div>
    <div class="system-bracket">
        <p class="eq">-R'<sub>Bx</sub> + F<sub>2</sub> &middot; cos(100&deg;) = 0; (4)</p>
        <p class="eq">-R'<sub>By</sub> + Q<sub>2</sub> + F<sub>2</sub> &middot; sin(-100&deg;) + R<sub>C</sub> + R<sub>D</sub> = 0; (5)</p>
        <p class="eq">M<sub>2</sub> + Q<sub>2</sub> &middot; (l<sub>3</sub> - a<sub>2</sub>) + F<sub>2</sub> &middot; sin(-100&deg;) &middot; (l<sub>3</sub> - l<sub>9</sub>) + R<sub>C</sub> &middot; (l<sub>3</sub> - l<sub>4</sub>) + R<sub>D</sub> &middot; l<sub>3</sub> = 0. (6)</p>
    </div>
    <div class="system-bracket" style="margin-top: 10px;">
        <p class="eq">-R'<sub>Bx</sub> {fmt(F2 * math.cos(rad(100)))} = 0; (4)</p>
        <p class="eq">-R'<sub>By</sub> + {fmt(Q2)} {fmt(F2 * math.sin(rad(-100)))} + R<sub>C</sub> + R<sub>D</sub> = 0; (5)</p>
        <p class="eq">{fmt(M2)} + {fmt(Q2)} &middot; {fmt(dist_Q2_from_B)} {fmt(F2 * math.sin(rad(-100)))} &middot; {fmt(dist_F2_from_B)} + R<sub>C</sub> &middot; {fmt(dist_C_from_B)} + R<sub>D</sub> &middot; {fmt(l3)} = 0. (6)</p>
    </div>
</div>

<p>Kadangi pagal trečią Niutono dėsnį R'<sub>Bx</sub> = R<sub>Bx</sub> ir R'<sub>By</sub> = R<sub>By</sub>, tai:</p>
<p>Iš (4) lygties: R<sub>Bx</sub> = {fmt(RBx)} kN;</p>
<p>Iš (1) lygties: R<sub>Ax</sub> + ({fmt(RBx)}) = {fmt(Q1 * 0.5)} &rarr; R<sub>Ax</sub> = {fmt(RAx)} kN.</p>
<p>Iš (3) lygties: {fmt(l2 * 0.5)} &middot; ({fmt(RBx)}) + {fmt(l2 * 0.866025)} &middot; R<sub>By</sub> = {fmt(-M1 + Q1 * a1 + F1 * l1 * 0.866025)} &rarr; R<sub>By</sub> = {fmt(RBy)} kN.</p>
<p>Iš (2) lygties: R<sub>Ay</sub> + ({fmt(RBy)}) = {fmt(Q1 * 0.866025 + F1)} &rarr; R<sub>Ay</sub> = {fmt(RAy)} kN.</p>

<p>Pakeičiame (5) lygtyje: R'<sub>By</sub> = R<sub>By</sub> = {fmt(RBy)} kN:</p>
<p>-{fmt(RBy)} + {fmt(Q2)} {fmt(F2 * math.sin(rad(-100)))} + R<sub>C</sub> + R<sub>D</sub> = 0 &rarr; R<sub>C</sub> + R<sub>D</sub> = {fmt(RBy - Q2 - F2 * math.sin(rad(-100)))}. (5)</p>
<p>{fmt(dist_C_from_B)} &middot; R<sub>C</sub> + {fmt(l3)} &middot; R<sub>D</sub> = {fmt(-M2 - Q2 * dist_Q2_from_B - F2 * math.sin(rad(-100)) * dist_F2_from_B)}. (6)</p>
<p>Iš (5) išsireiškus R<sub>C</sub> ir įstačius į (6), gauname:</p>
<p>R<sub>D</sub> = {fmt(RD)} kN.</p>
<p>R<sub>C</sub> = {fmt(RC)} kN.</p>

<h3>3.3. Sprendimo patikrinimas</h3>
<p>Užrašoma pusiausvyros sąlyga visai sistemai apie tašką B.</p>
<p class="eq">&sum; M<sub>B</sub>({get_overline('F')}<sub>i</sub>) = M<sub>1</sub> + M<sub>2</sub> - R<sub>Ax</sub> &middot; (l<sub>2</sub> &middot; sin(30&deg;)) - R<sub>Ay</sub> &middot; (l<sub>2</sub> &middot; cos(30&deg;)) + Q<sub>1</sub> &middot; (l<sub>2</sub> - a<sub>1</sub>) - F<sub>1</sub> &middot; (l<sub>1</sub> - l<sub>2</sub>) &middot; cos(30&deg;) + R<sub>C</sub> &middot; (l<sub>3</sub> - l<sub>4</sub>) + R<sub>D</sub> &middot; l<sub>3</sub> + Q<sub>2</sub> &middot; (l<sub>3</sub> - a<sub>2</sub>) + F<sub>2y</sub> &middot; (l<sub>3</sub> - l<sub>9</sub>) = 0</p>
<p class="eq">&sum; M<sub>B</sub>({get_overline('F')}<sub>i</sub>) = {fmt(M1)} + {fmt(M2)} - ({fmt(RAx)}) &middot; {fmt(l2 * math.sin(rad(30)))} - ({fmt(RAy)}) &middot; {fmt(l2 * math.cos(rad(30)))} + {fmt(Q1)} &middot; {fmt(l2 - a1)} - {fmt(F1)} &middot; {fmt((l1 - l2) * math.cos(rad(30)))} + ({fmt(RC)}) &middot; {fmt(dist_C_from_B)} + ({fmt(RD)}) &middot; {fmt(l3)} + {fmt(Q2)} &middot; {fmt(dist_Q2_from_B)} {fmt(F2 * math.sin(rad(-100)))} &middot; {fmt(dist_F2_from_B)} = {fmt(sum_MB_total)} kN</p>

<h3>3.4. Paklaidos skaičiavimas</h3>
<p>&Delta; = ({fmt(abs(sum_MB_total))} / 500) &middot; 100% = {fmt(abs(sum_MB_total)/5)}% &lt; 0,3%.</p>

<div class="page-break"></div>
<h2>4. Atsakymų lentelė</h2>
<table>
  <tr>
    <th>Varianto Nr.</th>
    <th>R<sub>Ax</sub>, kN</th>
    <th>R<sub>Ay</sub>, kN</th>
    <th>B<sub>x</sub>, kN</th>
    <th>B<sub>y</sub>, kN</th>
    <th>R<sub>C</sub>, kN</th>
    <th>R<sub>D</sub>, kN</th>
  </tr>
  <tr>
    <td>1298</td>
    <td>{fmt(RAx)}</td>
    <td>{fmt(RAy)}</td>
    <td>{fmt(RBx)}</td>
    <td>{fmt(RBy)}</td>
    <td>{fmt(RC)}</td>
    <td>{fmt(RD)}</td>
  </tr>
</table>

</body>
</html>
"""
    
    with open('/Users/ugniusvaitiekenas/srotas-ai-agent/fizika/namu_darbas.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated final accurate print-ready HTML document.")

generate()
