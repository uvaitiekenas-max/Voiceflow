import math

VAR = 1298
EO2 = 0.65
OA = 0.45
alfa = 120.0
beta = 120.0
gamma = 30.0
phi = -60.0
delta = -30.0
AD = 0.90
EB = 1.30
W1 = -2.00
AB = AD / 2

def norm_deg(d): return d % 360
def rad(d): return math.radians(d)
def add(v1, v2): return (v1[0]+v2[0], v1[1]+v2[1])
def sub(v1, v2): return (v1[0]-v2[0], v1[1]-v2[1])
def mult(v, s): return (v[0]*s, v[1]*s)
def mag(v): return math.hypot(v[0], v[1])
def solve_2x2(a, b, c, d, e, f):
    det = a*d - b*c
    if abs(det) < 1e-9: return 0, 0
    x = (e*d - b*f) / det
    y = (a*f - e*c) / det
    return x, y

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

def draw_arrow_def():
    return """
    <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="black" />
        </marker>
        <marker id="arrow-blue" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="blue" />
        </marker>
        <marker id="arrow-red" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="red" />
        </marker>
    </defs>
    """

def vector_text(x, y, text, sub="", color="black"):
    return f'<text x="{x}" y="{y}" fill="{color}" font-style="italic" font-weight="bold"><tspan text-decoration="overline">{text}</tspan><tspan dy="5" font-size="10" text-decoration="none">{sub}</tspan></text>'

def draw_point(p, label, ox=10, oy=-10):
    return f'<circle cx="{p[0]}" cy="{p[1]}" r="4" fill="white" stroke="black" stroke-width="2"/><text x="{p[0]+ox}" y="{p[1]+oy}" font-style="italic" font-size="16">{label}</text>'

O = (0.0, 0.0)
A = (OA * math.cos(rad(alfa)), OA * math.sin(rad(alfa)))
theta_AD = alfa + 180.0 + beta
AD_vec = (AD * math.cos(rad(theta_AD)), AD * math.sin(rad(theta_AD)))
D = add(A, AD_vec)
B = add(A, mult(AD_vec, 0.5))
theta_BE = theta_AD + gamma
BE_vec = (EB * math.cos(rad(theta_BE)), EB * math.sin(rad(theta_BE)))
E = add(B, BE_vec)
O2 = add(E, (EO2 * math.cos(rad(delta)), EO2 * math.sin(rad(delta))))

SCALE = 150
OFFSET_X = 150
OFFSET_Y = 250
def tf(p): return (OFFSET_X + p[0]*SCALE, OFFSET_Y - p[1]*SCALE)

theta_VA = alfa + (90 if W1 > 0 else -90)
vA_mag = abs(W1) * OA
vA = (vA_mag * math.cos(rad(theta_VA)), vA_mag * math.sin(rad(theta_VA)))
theta_VDA_base = theta_AD + 90
vD_mag_alg, vDA_mag_alg = solve_2x2(math.cos(rad(phi)), -math.cos(rad(theta_VDA_base)), math.sin(rad(phi)), -math.sin(rad(theta_VDA_base)), vA[0], vA[1])
vD = (vD_mag_alg * math.cos(rad(phi)), vD_mag_alg * math.sin(rad(phi)))
vDA = (vDA_mag_alg * math.cos(rad(theta_VDA_base)), vDA_mag_alg * math.sin(rad(theta_VDA_base)))
w2 = vDA_mag_alg / AD 
vBA = mult(vDA, 0.5)
vB = add(vA, vBA)
theta_VE_base = delta + 90
theta_VEB_base = theta_BE + 90
vE_mag_alg, vEB_mag_alg = solve_2x2(math.cos(rad(theta_VE_base)), -math.cos(rad(theta_VEB_base)), math.sin(rad(theta_VE_base)), -math.sin(rad(theta_VEB_base)), vB[0], vB[1])
vE = (vE_mag_alg * math.cos(rad(theta_VE_base)), vE_mag_alg * math.sin(rad(theta_VE_base)))
vEB = (vEB_mag_alg * math.cos(rad(theta_VEB_base)), vEB_mag_alg * math.sin(rad(theta_VEB_base)))
w3 = vEB_mag_alg / EB
w4 = vE_mag_alg / EO2

# Acce
aA_mag = W1**2 * OA
theta_aA = alfa + 180
aA = (aA_mag * math.cos(rad(theta_aA)), aA_mag * math.sin(rad(theta_aA)))
theta_aDAn = theta_AD + 180
aDAn_mag = w2**2 * AD
aDAn = (aDAn_mag * math.cos(rad(theta_aDAn)), aDAn_mag * math.sin(rad(theta_aDAn)))
theta_aDAt_base = theta_AD + 90
b_vec_a = add(aA, aDAn)
aD_mag_alg, aDAt_mag_alg = solve_2x2(math.cos(rad(phi)), -math.cos(rad(theta_aDAt_base)), math.sin(rad(phi)), -math.sin(rad(theta_aDAt_base)), b_vec_a[0], b_vec_a[1])
aD = (aD_mag_alg * math.cos(rad(phi)), aD_mag_alg * math.sin(rad(phi)))
aDAt = (aDAt_mag_alg * math.cos(rad(theta_aDAt_base)), aDAt_mag_alg * math.sin(rad(theta_aDAt_base)))
eps2 = aDAt_mag_alg / AD

aBAn = mult(aDAn, 0.5)
aBAt = mult(aDAt, 0.5)
aB = add(add(aA, aBAn), aBAt)

theta_aEn = delta
aEn_mag = w4**2 * EO2
aEn = (aEn_mag * math.cos(rad(theta_aEn)), aEn_mag * math.sin(rad(theta_aEn)))
theta_aEt_base = delta + 90
theta_aEBn = theta_BE + 180
aEBn_mag = w3**2 * EB
aEBn = (aEBn_mag * math.cos(rad(theta_aEBn)), aEBn_mag * math.sin(rad(theta_aEBn)))
theta_aEBt_base = theta_BE + 90
b_vec_a2 = sub(add(aB, aEBn), aEn)
aEt_mag_alg, aEBt_mag_alg = solve_2x2(math.cos(rad(theta_aEt_base)), -math.cos(rad(theta_aEBt_base)), math.sin(rad(theta_aEt_base)), -math.sin(rad(theta_aEBt_base)), b_vec_a2[0], b_vec_a2[1])
aEt = (aEt_mag_alg * math.cos(rad(theta_aEt_base)), aEt_mag_alg * math.sin(rad(theta_aEt_base)))
aEBt = (aEBt_mag_alg * math.cos(rad(theta_aEBt_base)), aEBt_mag_alg * math.sin(rad(theta_aEBt_base)))
aE = add(aEn, aEt)
eps3 = aEBt_mag_alg / EB
eps4 = aEt_mag_alg / EO2

# Draw velocity plans helper
def draw_vec(start, vec, color, label, label_pos, scale=100):
    sx, sy = start
    ex, ey = sx + vec[0]*scale, sy - vec[1]*scale
    return f"""
    <line x1="{sx}" y1="{sy}" x2="{ex}" y2="{ey}" stroke="{color}" stroke-width="2" marker-end="url(#{'arrow-blue' if color=='blue' else 'arrow'})"/>
    {vector_text(ex+label_pos[0], ey+label_pos[1], label[0], label[1:], color)}
    """

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
.schema-container {{ margin: 30px 0; text-align: center; }}
svg text {{ font-family: 'Times New Roman', serif; font-size: 14px; }}
.title-page {{ text-align: center; margin-bottom: 50px; position: relative; }}
.title-page h1 {{ font-size: 20px; margin: 10px; }} 
.title-page p {{ margin: 5px; }}
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
<h1 style="margin-top: 40vh;">Namų darbas Nr.2</h1>
<h1>Plokščiojo keturių grandžių mechanizmo kinematinė analizė</h1>
<p>Varianto Nr.{VAR}</p>
</div>

<h2>1. Užduoties lapas</h2>
<p><b>Užduoties duomenys:</b></p>
<p>
<span class="math">EO<sub>2</sub></span> = {fmt(EO2)} m; 
<span class="math">OA</span> = {fmt(OA)} m; 
<span class="math">&alpha;</span> = {fmt(alfa)}&deg;; 
<span class="math">&beta;</span> = {fmt(beta)}&deg;; 
<span class="math">&gamma;</span> = {fmt(gamma)}&deg;; 
<span class="math">&phi;</span> = {fmt(phi)}&deg;; 
<span class="math">&delta;</span> = {fmt(delta)}&deg;; 
<span class="math">AD</span> = {fmt(AD)} m; 
<span class="math">EB</span> = {fmt(EB)} m; 
<span class="math">&omega;<sub>1</sub></span> = {fmt(W1)} rad/s.
</p>
<p>Rasti: V<sub>A</sub>, V<sub>B</sub>, V<sub>D</sub>, V<sub>E</sub>, &omega;<sub>2</sub>, &omega;<sub>3</sub>, &omega;<sub>4</sub>, a<sub>A</sub>, a<sub>B</sub>, a<sub>D</sub>, a<sub>E</sub>, &varepsilon;<sub>2</sub>, &varepsilon;<sub>3</sub>, &varepsilon;<sub>4</sub>.</p>

<p><b><u>Užduoties schema:</u></b></p>
<div class="schema-container">
<svg width="700" height="400" viewBox="0 0 700 400">
    {draw_arrow_def()}
    <!-- Fixed supports -->
    <path d="M {tf(O)[0]} {tf(O)[1]} L {tf(O)[0]-15} {tf(O)[1]+20} L {tf(O)[0]+15} {tf(O)[1]+20} Z" fill="none" stroke="black" stroke-width="2"/>
    <line x1="{tf(O)[0]-25}" y1="{tf(O)[1]+20}" x2="{tf(O)[0]+25}" y2="{tf(O)[1]+20}" stroke="black" stroke-width="2"/>
    
    <path d="M {tf(O2)[0]} {tf(O2)[1]} L {tf(O2)[0]-15} {tf(O2)[1]+20} L {tf(O2)[0]+15} {tf(O2)[1]+20} Z" fill="none" stroke="black" stroke-width="2"/>
    <line x1="{tf(O2)[0]-25}" y1="{tf(O2)[1]+20}" x2="{tf(O2)[0]+25}" y2="{tf(O2)[1]+20}" stroke="black" stroke-width="2"/>
    
    <!-- Slider at D -->
    <g transform="translate({tf(D)[0]}, {tf(D)[1]}) rotate({-phi})">
        <rect x="-15" y="-10" width="30" height="20" fill="none" stroke="black" stroke-width="2"/>
        <line x1="-30" y1="10" x2="30" y2="10" stroke="black" stroke-width="1"/>
        <line x1="-20" y1="10" x2="-25" y2="15" stroke="black"/><line x1="-10" y1="10" x2="-15" y2="15" stroke="black"/><line x1="0" y1="10" x2="-5" y2="15" stroke="black"/><line x1="10" y1="10" x2="5" y2="15" stroke="black"/><line x1="20" y1="10" x2="15" y2="15" stroke="black"/>
    </g>

    <!-- Links -->
    <line x1="{tf(O)[0]}" y1="{tf(O)[1]}" x2="{tf(A)[0]}" y2="{tf(A)[1]}" stroke="black" stroke-width="4" />
    <line x1="{tf(A)[0]}" y1="{tf(A)[1]}" x2="{tf(D)[0]}" y2="{tf(D)[1]}" stroke="black" stroke-width="4" />
    <line x1="{tf(B)[0]}" y1="{tf(B)[1]}" x2="{tf(E)[0]}" y2="{tf(E)[1]}" stroke="black" stroke-width="4" />
    <line x1="{tf(E)[0]}" y1="{tf(E)[1]}" x2="{tf(O2)[0]}" y2="{tf(O2)[1]}" stroke="black" stroke-width="4" />

    {draw_point(tf(O), 'O')}
    {draw_point(tf(A), 'A')}
    {draw_point(tf(B), 'B', 10, 15)}
    {draw_point(tf(D), 'D')}
    {draw_point(tf(E), 'E')}
    {draw_point(tf(O2), 'O2')}
    
    <path d="M {tf(O)[0]+40} {tf(O)[1]} A 40 40 0 1 0 {tf(O)[0] + 40*math.cos(rad(-alfa))} {tf(O)[1] - 40*math.sin(rad(-alfa))}" fill="none" stroke="black" marker-end="url(#arrow)"/>
    <text x="{tf(O)[0]+45}" y="{tf(O)[1]+20}">&omega;&#8321;</text>

    <!-- Coordinate check text -->
    <text x="400" y="30" font-style="italic">Koordinatės patikrinimui:</text>
    <text x="400" y="50">D(x; y) = ({fmt(D[0])}; {fmt(D[1])}) m</text>
    <text x="400" y="70">E(x; y) = ({fmt(E[0])}; {fmt(E[1])}) m</text>
    <text x="400" y="90">O2(x; y) = ({fmt(O2[0])}; {fmt(O2[1])}) m</text>
</svg>
</div>

<div class="page-break"></div>
<h2>2. Greičių skaičiavimas</h2>

<h3>2.1. Taško A greičio nustatymas</h3>
<p class="eq">V<sub>A</sub> = |&omega;<sub>1</sub>| &middot; OA = {fmt(abs(W1))} &middot; {fmt(OA)} = {fmt(vA_mag)} m/s.</p>
<p>Kadangi &omega;<sub>1</sub> &lt; 0 (sukasi pagal laikrodžio rodyklę), greičio V<sub>A</sub> vektorius nukreiptas {fmt(norm_deg(alfa-90))}&deg; kampu.</p>

<h3>2.2. Taško D greičio nustatymas</h3>
<p>Vektorinė lygtis: {vector_text(0,0,'V','D')} = {vector_text(0,0,'V','A')} + {vector_text(0,0,'V','DA')}</p>
<p>Žinoma, kad {vector_text(0,0,'V','A')} &perp; (OA), {vector_text(0,0,'V','D')} &parallel; (k) ir {vector_text(0,0,'V','DA')} &perp; (DA). Randame V<sub>D</sub> ir V<sub>DA</sub> sprendžiant lygčių sistemą projekcijomis į x ir y ašis.</p>
<p class="eq">V<sub>D</sub> = {fmt(abs(vD_mag_alg))} m/s, V<sub>DA</sub> = {fmt(abs(vDA_mag_alg))} m/s.</p>
<p>Grandies AD kampinis greitis:</p>
<p class="eq">&omega;<sub>2</sub> = V<sub>DA</sub> / AD = {fmt(abs(vDA_mag_alg))} / {fmt(AD)} = {fmt(abs(w2))} rad/s.</p>
<div class="schema-container">
<svg width="400" height="200" viewBox="0 0 400 200">
    {draw_arrow_def()}
    <line x1="50" y1="100" x2="350" y2="100" stroke="gray" stroke-width="1"/>
    <line x1="200" y1="10" x2="200" y2="190" stroke="gray" stroke-width="1"/>
    {draw_vec((200, 100), vA, "black", "VA", (5, 5), 50)}
    {draw_vec((200+vA[0]*50, 100-vA[1]*50), vDA, "black", "VDA", (-20, 5), 50)}
    {draw_vec((200, 100), vD, "blue", "VD", (5, -5), 50)}
</svg>
<p><i>Taško D greičio planas</i></p>
</div>

<h3>2.3. Taško B greičio nustatymas</h3>
<p>Vektorinė lygtis: {vector_text(0,0,'V','B')} = {vector_text(0,0,'V','A')} + {vector_text(0,0,'V','BA')}</p>
<p class="eq">V<sub>BA</sub> = |&omega;<sub>2</sub>| &middot; AB = {fmt(abs(w2))} &middot; {fmt(AB)} = {fmt(mag(vBA))} m/s.</p>
<p>Sudedame vektorius pagal x ir y projekcijas ir gauname:</p>
<p class="eq">V<sub>B</sub> = {fmt(mag(vB))} m/s.</p>
<div class="schema-container">
<svg width="400" height="200" viewBox="0 0 400 200">
    {draw_arrow_def()}
    <line x1="50" y1="150" x2="350" y2="150" stroke="gray" stroke-width="1"/>
    <line x1="150" y1="10" x2="150" y2="190" stroke="gray" stroke-width="1"/>
    {draw_vec((150, 150), vA, "black", "VA", (5, 5), 80)}
    {draw_vec((150+vA[0]*80, 150-vA[1]*80), vBA, "black", "VBA", (-20, 5), 80)}
    {draw_vec((150, 150), vB, "blue", "VB", (5, -5), 80)}
</svg>
<p><i>Taško B greičio planas</i></p>
</div>

<h3>2.4. Taško E greičio nustatymas</h3>
<p>Vektorinė lygtis: {vector_text(0,0,'V','E')} = {vector_text(0,0,'V','B')} + {vector_text(0,0,'V','EB')}</p>
<p>Žinoma, kad {vector_text(0,0,'V','E')} &perp; (O<sub>2</sub>E) ir {vector_text(0,0,'V','EB')} &perp; (BE).</p>
<p class="eq">V<sub>E</sub> = {fmt(abs(vE_mag_alg))} m/s, V<sub>EB</sub> = {fmt(abs(vEB_mag_alg))} m/s.</p>
<p>Grandžių kampiniai greičiai:</p>
<p class="eq">&omega;<sub>3</sub> = V<sub>EB</sub> / EB = {fmt(abs(vEB_mag_alg))} / {fmt(EB)} = {fmt(abs(w3))} rad/s.</p>
<p class="eq">&omega;<sub>4</sub> = V<sub>E</sub> / EO<sub>2</sub> = {fmt(abs(vE_mag_alg))} / {fmt(EO2)} = {fmt(abs(w4))} rad/s.</p>
<div class="schema-container">
<svg width="400" height="200" viewBox="0 0 400 200">
    {draw_arrow_def()}
    <line x1="50" y1="150" x2="350" y2="150" stroke="gray" stroke-width="1"/>
    <line x1="150" y1="10" x2="150" y2="190" stroke="gray" stroke-width="1"/>
    {draw_vec((150, 150), vB, "black", "VB", (5, 5), 100)}
    {draw_vec((150+vB[0]*100, 150-vB[1]*100), vEB, "black", "VEB", (5, 5), 100)}
    {draw_vec((150, 150), vE, "blue", "VE", (-20, -5), 100)}
</svg>
<p><i>Taško E greičio planas</i></p>
</div>

<div class="page-break"></div>
<h2>3. Pagreičių skaičiavimas</h2>

<h3>3.1. Taško A pagreičio nustatymas</h3>
<p>Kadangi grandinės kampinis pagreitis &varepsilon;<sub>1</sub> = 0, tai tangentinis pagreitis lygus nuliui (a<sub>A</sub><sup>&tau;</sup> = 0).</p>
<p class="eq">a<sub>A</sub> = a<sub>A</sub><sup>n</sup> = &omega;<sub>1</sub><sup>2</sup> &middot; OA = {fmt(W1)}<sup>2</sup> &middot; {fmt(OA)} = {fmt(aA_mag)} m/s<sup>2</sup>.</p>

<h3>3.2. Taško D pagreičio nustatymas</h3>
<p>Vektorinė lygtis: {vector_text(0,0,'a','D')} = {vector_text(0,0,'a','A')} + {vector_text(0,0,'a','DA<tspan dy="-5">n</tspan>')} + {vector_text(0,0,'a','DA<tspan dy="-5">&tau;</tspan>')}</p>
<p class="eq">a<sub>DA</sub><sup>n</sup> = &omega;<sub>2</sub><sup>2</sup> &middot; AD = {fmt(w2)}<sup>2</sup> &middot; {fmt(AD)} = {fmt(mag(aDAn))} m/s<sup>2</sup>.</p>
<p>Sprendžiant lygčių sistemą randame:</p>
<p class="eq">a<sub>D</sub> = {fmt(abs(aD_mag_alg))} m/s<sup>2</sup>, a<sub>DA</sub><sup>&tau;</sup> = {fmt(abs(aDAt_mag_alg))} m/s<sup>2</sup>.</p>
<p>Grandies AD kampinis pagreitis:</p>
<p class="eq">&varepsilon;<sub>2</sub> = a<sub>DA</sub><sup>&tau;</sup> / AD = {fmt(abs(aDAt_mag_alg))} / {fmt(AD)} = {fmt(abs(eps2))} rad/s<sup>2</sup>.</p>

<h3>3.3. Taško B pagreičio nustatymas</h3>
<p>Kadangi taškas B yra grandies AD viduryje:</p>
<p class="eq">{vector_text(0,0,'a','B')} = {vector_text(0,0,'a','A')} + {vector_text(0,0,'a','BA<tspan dy="-5">n</tspan>')} + {vector_text(0,0,'a','BA<tspan dy="-5">&tau;</tspan>')}</p>
<p class="eq">a<sub>B</sub> = {fmt(mag(aB))} m/s<sup>2</sup>.</p>

<h3>3.4. Taško E pagreičio nustatymas</h3>
<p>Vektorinė lygtis: {vector_text(0,0,'a','E<tspan dy="-5">n</tspan>')} + {vector_text(0,0,'a','E<tspan dy="-5">&tau;</tspan>')} = {vector_text(0,0,'a','B')} + {vector_text(0,0,'a','EB<tspan dy="-5">n</tspan>')} + {vector_text(0,0,'a','EB<tspan dy="-5">&tau;</tspan>')}</p>
<p class="eq">a<sub>E</sub><sup>n</sup> = &omega;<sub>4</sub><sup>2</sup> &middot; EO<sub>2</sub> = {fmt(mag(aEn))} m/s<sup>2</sup>.</p>
<p class="eq">a<sub>EB</sub><sup>n</sup> = &omega;<sub>3</sub><sup>2</sup> &middot; EB = {fmt(mag(aEBn))} m/s<sup>2</sup>.</p>
<p>Sprendžiant lygčių sistemą randame:</p>
<p class="eq">a<sub>E</sub><sup>&tau;</sup> = {fmt(abs(aEt_mag_alg))} m/s<sup>2</sup>, a<sub>EB</sub><sup>&tau;</sup> = {fmt(abs(aEBt_mag_alg))} m/s<sup>2</sup>.</p>
<p class="eq">a<sub>E</sub> = {fmt(mag(aE))} m/s<sup>2</sup>.</p>
<p>Grandžių kampiniai pagreičiai:</p>
<p class="eq">&varepsilon;<sub>3</sub> = a<sub>EB</sub><sup>&tau;</sup> / EB = {fmt(abs(eps3))} rad/s<sup>2</sup>.</p>
<p class="eq">&varepsilon;<sub>4</sub> = a<sub>E</sub><sup>&tau;</sup> / EO<sub>2</sub> = {fmt(abs(eps4))} rad/s<sup>2</sup>.</p>

<div class="page-break"></div>
<h2>4. Atsakymų lentelė</h2>
<table>
  <tr>
    <th colspan="4">Greičiai, m/s</th>
    <th colspan="3">Kampiniai greičiai, rad/s</th>
  </tr>
  <tr>
    <td>V<sub>A</sub></td><td>V<sub>B</sub></td><td>V<sub>D</sub></td><td>V<sub>E</sub></td>
    <td>&omega;<sub>2</sub></td><td>&omega;<sub>3</sub></td><td>&omega;<sub>4</sub></td>
  </tr>
  <tr>
    <td>{fmt(mag(vA))}</td><td>{fmt(mag(vB))}</td><td>{fmt(mag(vD))}</td><td>{fmt(mag(vE))}</td>
    <td>{fmt(abs(w2))}</td><td>{fmt(abs(w3))}</td><td>{fmt(abs(w4))}</td>
  </tr>
</table>

<table style="margin-top:20px;">
  <tr>
    <th colspan="4">Pagreičiai, m/s<sup>2</sup></th>
    <th colspan="3">Kampiniai pagreičiai, rad/s<sup>2</sup></th>
  </tr>
  <tr>
    <td>a<sub>A</sub></td><td>a<sub>B</sub></td><td>a<sub>D</sub></td><td>a<sub>E</sub></td>
    <td>&varepsilon;<sub>2</sub></td><td>&varepsilon;<sub>3</sub></td><td>&varepsilon;<sub>4</sub></td>
  </tr>
  <tr>
    <td>{fmt(mag(aA))}</td><td>{fmt(mag(aB))}</td><td>{fmt(mag(aD))}</td><td>{fmt(mag(aE))}</td>
    <td>{fmt(abs(eps2))}</td><td>{fmt(abs(eps3))}</td><td>{fmt(abs(eps4))}</td>
  </tr>
</table>

</body>
</html>
"""

with open('/Users/ugniusvaitiekenas/srotas-ai-agent/fizika/namu_darbas_2.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Generated Namu Darbas 2 HTML with vector plans!")
