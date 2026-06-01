import math

# Given data for Var 1093
VAR = 1093
EO2 = 0.55
OA = 0.20
alfa = 270.0
beta = 210.0
gamma = -60.0
phi = 60.0
delta = -30.0
AD = 0.90
EB = 1.20
W1 = 10.00
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

class SVGBuilder:
    def __init__(self, scale=100):
        self.elements = []
        self.min_x = 100000
        self.max_x = -100000
        self.min_y = 100000
        self.max_y = -100000
        self.scale = scale

    def pt(self, math_p):
        return (math_p[0] * self.scale, -math_p[1] * self.scale)
        
    def add(self, svg_str, points=[]):
        self.elements.append(svg_str)
        for p in points:
            x, y = p
            if x < self.min_x: self.min_x = x
            if x > self.max_x: self.max_x = x
            if y < self.min_y: self.min_y = y
            if y > self.max_y: self.max_y = y

    def line(self, p1, p2, color="black", width=2, dash="", marker=""):
        p1s = self.pt(p1)
        p2s = self.pt(p2)
        style = f'stroke="{color}" stroke-width="{width}"'
        if dash: style += f' stroke-dasharray="{dash}"'
        if marker: style += f' marker-end="url(#{marker})"'
        self.add(f'<line x1="{p1s[0]}" y1="{p1s[1]}" x2="{p2s[0]}" y2="{p2s[1]}" {style}/>', [p1s, p2s])

    def text(self, p, text, offset=(0,0), color="black", is_vector=False, sub=""):
        ps = self.pt(p)
        x = ps[0] + offset[0]
        y = ps[1] + offset[1]
        if is_vector:
            s = vector_text(x, y, text, sub, color)
        else:
            s = f'<text x="{x}" y="{y}" fill="{color}" font-style="italic" font-size="16">{text}</text>'
        self.add(s, [ps])

    def circle(self, p, r=4, color="black", fill="white", label="", ox=10, oy=-10):
        ps = self.pt(p)
        self.add(f'<circle cx="{ps[0]}" cy="{ps[1]}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="2"/>', [(ps[0]-r, ps[1]-r), (ps[0]+r, ps[1]+r)])
        if label:
            self.text(p, label, offset=(ox, oy))

    def hatch(self, p, angle_deg, length=30):
        ps = self.pt(p)
        a = rad(-angle_deg)
        dx = math.cos(a) * length/2
        dy = math.sin(a) * length/2
        p1 = (ps[0]-dx, ps[1]-dy)
        p2 = (ps[0]+dx, ps[1]+dy)
        self.add(f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" stroke="black" stroke-width="2"/>', [p1, p2])
        for i in range(5):
            t = i / 4.0
            hx = p1[0] + (p2[0]-p1[0])*t
            hy = p1[1] + (p2[1]-p1[1])*t
            px = hx - math.sin(a) * 10
            py = hy + math.cos(a) * 10
            self.add(f'<line x1="{hx}" y1="{hy}" x2="{px}" y2="{py}" stroke="black" stroke-width="1"/>', [(px, py)])

    def slider(self, p, angle_deg):
        ps = self.pt(p)
        s = f'<g transform="translate({ps[0]}, {ps[1]}) rotate({-angle_deg})">'
        s += '<rect x="-15" y="-15" width="30" height="30" fill="white" stroke="black" stroke-width="2"/>'
        s += '<line x1="-35" y1="15" x2="35" y2="15" stroke="black" stroke-width="3"/>'
        for i in range(-30, 40, 10):
            s += f'<line x1="{i}" y1="15" x2="{i-5}" y2="25" stroke="black" stroke-width="1"/>'
        s += '</g>'
        self.add(s, [(ps[0]-40, ps[1]-40), (ps[0]+40, ps[1]+40)])

    def arc(self, p, r, start_ang, end_ang, label=""):
        ps = self.pt(p)
        sa = rad(-start_ang)
        ea = rad(-end_ang)
        x1 = ps[0] + r * math.cos(sa)
        y1 = ps[1] + r * math.sin(sa)
        x2 = ps[0] + r * math.cos(ea)
        y2 = ps[1] + r * math.sin(ea)
        large_arc = 1 if abs(end_ang - start_ang) > 180 else 0
        sweep = 0 if end_ang > start_ang else 1 # CCW
        
        path = f'<path d="M {x1} {y1} A {r} {r} 0 {large_arc} {sweep} {x2} {y2}" fill="none" stroke="gray" stroke-width="2" marker-end="url(#arrow)"/>'
        self.add(path, [(ps[0]-r, ps[1]-r), (ps[0]+r, ps[1]+r)])
        if label:
            mx = ps[0] + (r+15) * math.cos((sa+ea)/2)
            my = ps[1] + (r+15) * math.sin((sa+ea)/2)
            self.add(f'<text x="{mx-10}" y="{my+5}" font-style="italic" font-weight="bold">{label}</text>')

    def render(self, width=600, padding=50):
        if self.min_x > self.max_x: return "<svg></svg>"
        w = self.max_x - self.min_x
        h = self.max_y - self.min_y
        if w == 0: w = 1
        if h == 0: h = 1
        
        viewBox = f"{self.min_x - padding} {self.min_y - padding} {w + 2*padding} {h + 2*padding}"
        height = int(width * (h + 2*padding) / (w + 2*padding))
        
        res = f'<svg width="{width}" height="{height}" viewBox="{viewBox}">'
        res += draw_arrow_def()
        res += "".join(self.elements)
        res += '</svg>'
        return res

O = (0.0, 0.0)
A = (OA * math.cos(rad(alfa)), OA * math.sin(rad(alfa)))
theta_AD = norm_deg(alfa + 180.0 + beta)
AD_vec = (AD * math.cos(rad(theta_AD)), AD * math.sin(rad(theta_AD)))
D = add(A, AD_vec)
B = add(A, mult(AD_vec, 0.5))
theta_BE = norm_deg(theta_AD + gamma)
BE_vec = (EB * math.cos(rad(theta_BE)), EB * math.sin(rad(theta_BE)))
E = add(B, BE_vec)
O2 = add(E, (EO2 * math.cos(rad(delta)), EO2 * math.sin(rad(delta))))

# Velocities
theta_VA = norm_deg(alfa + (90 if W1 > 0 else -90))
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

# Accelerations
aA_mag = W1**2 * OA
theta_aA = norm_deg(alfa + 180)
aA = (aA_mag * math.cos(rad(theta_aA)), aA_mag * math.sin(rad(theta_aA)))

theta_aDAn = norm_deg(theta_AD + 180)
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

theta_aEn = norm_deg(delta)
aEn_mag = w4**2 * EO2
aEn = (aEn_mag * math.cos(rad(theta_aEn)), aEn_mag * math.sin(rad(theta_aEn)))
theta_aEt_base = delta + 90
theta_aEBn = norm_deg(theta_BE + 180)
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

def calc_text_offset(v_math, dist=20):
    v_svg = (v_math[0], -v_math[1])
    L = math.hypot(v_svg[0], v_svg[1])
    if L < 1e-5: return (dist, dist)
    nx, ny = -v_svg[1]/L, v_svg[0]/L
    if ny > 0:
        nx, ny = -nx, -ny
    return (nx * dist - 5, ny * dist + 5)

def draw_mech(svg, show_vel=False, show_acc=False):
    svg.slider(D, phi)
    svg.line(O, A, width=4)
    svg.line(A, D, width=4)
    svg.line(B, E, width=4)
    svg.line(E, O2, width=4)
    svg.hatch(O, 0)
    svg.hatch(O2, 0)
    svg.circle(O, label="O", ox=10, oy=15)
    svg.circle(O2, label="O2", ox=10, oy=-10)
    svg.circle(A, label="A", ox=-15, oy=-10)
    svg.circle(B, label="B", ox=10, oy=-10)
    svg.circle(D, label="D", ox=10, oy=-20)
    svg.circle(E, label="E", ox=-20, oy=10)
    
    # Angles on base schema
    svg.line(O, (O[0]+0.3, O[1]), dash="4,4")
    svg.arc(O, 40, 0, alfa, "&alpha;")
    
    A_ext = add(A, mult(sub(O, A), 0.3))
    svg.line(A, A_ext, dash="4,4")
    svg.arc(A, 40, alfa+180, alfa+180+beta, "&beta;")
    
    B_ext = add(B, mult(sub(A, B), 0.3))
    svg.line(B, B_ext, dash="4,4")
    svg.arc(B, 40, theta_AD+180, theta_AD+180+gamma, "&gamma;")
    
    svg.line(O2, (O2[0]-0.3, O2[1]), dash="4,4")
    svg.arc(O2, 40, 180, 180+delta, "&delta;")
    
    svg.line(D, (D[0]-0.3, D[1]), dash="4,4")
    svg.arc(D, 50, 180, 180+phi, "&phi;")

    if not show_vel and not show_acc:
        svg.arc(O, 50, alfa, alfa+50 if W1>0 else alfa-50, "&omega;&#8321;")

    if show_vel:
        vscale = 0.3
        def dv(start, vec, lbl, sublbl, color="blue", arrow="arrow-blue"):
            end = add(start, mult(vec, vscale))
            svg.line(start, end, color=color, marker=arrow)
            mid = add(start, mult(vec, vscale/2))
            svg.text(mid, lbl, offset=calc_text_offset(vec, 15), color=color, is_vector=True, sub=sublbl)

        dv(A, vA, "V", "A")
        dv(D, vD, "V", "D")
        endB = add(B, mult(vB, vscale))
        svg.line(B, endB, color="blue", marker="arrow-blue")
        svg.text(add(B, mult(vB, vscale)), "V", offset=(10, 20), color="blue", is_vector=True, sub="B")
        
        dv(E, vE, "V", "E")
        dv(D, vDA, "V", "DA", "black", "arrow")
        dv(B, vBA, "V", "BA", "black", "arrow")
        dv(E, vEB, "V", "EB", "black", "arrow")
        
        svg.arc(O, 50, alfa, alfa+50 if W1>0 else alfa-50, "&omega;&#8321;")
        svg.arc(A, 50, theta_AD, theta_AD+(50 if w2>0 else -50), "&omega;&#8322;")
        svg.arc(B, 50, theta_BE, theta_BE+(50 if w3>0 else -50), "&omega;&#8323;")
        svg.arc(E, 50, delta+180, delta+180+(50 if w4>0 else -50), "&omega;&#8324;")

    if show_acc:
        ascale = 0.05
        def da(start, vec, lbl, sublbl, color="red", arrow="arrow-red"):
            end = add(start, mult(vec, ascale))
            svg.line(start, end, color=color, marker=arrow)
            mid = add(start, mult(vec, ascale/2))
            svg.text(mid, lbl, offset=calc_text_offset(vec, 15), color=color, is_vector=True, sub=sublbl)

        da(A, aA, "a", "A")
        da(D, aD, "a", "D")
        da(B, aB, "a", "B")
        da(E, aE, "a", "E")
        
        svg.arc(O, 60, alfa, alfa+50 if W1>0 else alfa-50, "&omega;&#8321;")
        svg.arc(A, 60, theta_AD, theta_AD+(50 if eps2>0 else -50), "&varepsilon;&#8322;")
        svg.arc(B, 60, theta_BE, theta_BE+(50 if eps3>0 else -50), "&varepsilon;&#8323;")
        svg.arc(E, 60, delta+180, delta+180+(50 if eps4>0 else -50), "&varepsilon;&#8324;")

def build_polygon(origin, vectors, resultant, scale, title):
    svg = SVGBuilder(scale=scale)
    # Draw axes
    svg.line((-3, 0), (3, 0), color="lightgray")
    svg.line((0, -3), (0, 3), color="lightgray")
    svg.text((3, 0), "x", color="gray", offset=(-10, 15))
    svg.text((0, 3), "y", color="gray", offset=(5, -5))
    svg.circle((0,0), r=3)
    svg.text((0,0), origin, offset=(-20, 20))
    
    def draw_vec_angle(start, vec, idx):
        angle = math.degrees(math.atan2(vec[1], vec[0]))
        norm_ang = angle % 360
        if abs(norm_ang) < 1 or abs(norm_ang - 360) < 1: return
        # Draw reference dashed line from start
        ref_len = 0.4
        svg.line(start, (start[0]+ref_len, start[1]), color="gray", dash="3,3", width=1)
        # Arc with radius proportional to scale
        arc_r = 25 + idx * 8  # stagger arcs so labels don't overlap
        draw_ang = norm_ang if norm_ang <= 180 else norm_ang - 360
        svg.arc(start, arc_r, 0, draw_ang, f"{norm_ang:.0f}&deg;")

    cur = (0,0)
    for idx, (v, label, sub, offset) in enumerate(vectors):
        nxt = add(cur, v)
        svg.line(cur, nxt, color="black", marker="arrow")
        draw_vec_angle(cur, v, idx)
        # Place label at 60% along vector for better spacing
        mid = add(cur, mult(v, 0.6))
        svg.text(mid, label, offset=offset, is_vector=True, sub=sub)
        cur = nxt
    
    if resultant:
        v, label, sub, offset = resultant
        color = "blue" if label=="V" else "red"
        marker = "arrow-blue" if label=="V" else "arrow-red"
        svg.line((0,0), v, color=color, marker=marker)
        draw_vec_angle((0,0), v, len(vectors))
        mid = mult(v, 0.6)
        svg.text(mid, label, offset=offset, color=color, is_vector=True, sub=sub)
    
    return f'<div class="schema-container">{svg.render(width=400)}<p><i>{title}</i></p></div>'

main_svg = SVGBuilder(scale=150)
draw_mech(main_svg)
html_main = main_svg.render(width=600)

vel_svg = SVGBuilder(scale=150)
draw_mech(vel_svg, show_vel=True)
html_vel = vel_svg.render(width=600)

acc_svg = SVGBuilder(scale=150)
draw_mech(acc_svg, show_acc=True)
html_acc = acc_svg.render(width=600)

# Velocity polygons with wider scale for better label spacing
poly_D = build_polygon("D", [(vA, "V", "A", (15, -15)), (vDA, "V", "DA", (-30, -10))], (vD, "V", "D", (15, 20)), scale=150, title="Taško D greičio planas")
poly_B = build_polygon("B", [(vA, "V", "A", (15, -15)), (vBA, "V", "BA", (-30, -10))], (vB, "V", "B", (10, 20)), scale=150, title="Taško B greičio planas")
poly_E = build_polygon("E", [(vB, "V", "B", (15, 20)), (vEB, "V", "EB", (10, -25))], (vE, "V", "E", (-30, -10)), scale=150, title="Taško E greičio planas")

# Acceleration polygons with wider scale
poly_aD = build_polygon("D", [(aA, "a", "A", (-25, 15)), (aDAn, "a", "DA<tspan dy='-5'>n</tspan>", (10, -25)), (aDAt, "a", "DA<tspan dy='-5'>&tau;</tspan>", (10, 15))], (aD, "a", "D", (-30, -20)), scale=30, title="Taško D pagreičio planas")
poly_aB = build_polygon("B", [(aA, "a", "A", (-25, 15)), (aBAn, "a", "BA<tspan dy='-5'>n</tspan>", (10, -25)), (aBAt, "a", "BA<tspan dy='-5'>&tau;</tspan>", (10, 15))], (aB, "a", "B", (-30, -20)), scale=30, title="Taško B pagreičio planas")
poly_aE = build_polygon("E", [(aB, "a", "B", (-30, -20)), (aEBn, "a", "EB<tspan dy='-5'>n</tspan>", (10, 20)), (aEBt, "a", "EB<tspan dy='-5'>&tau;</tspan>", (10, -20))], (aE, "a", "E", (15, -25)), scale=30, title="Taško E pagreičio planas")

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
{html_main}

<div class="page-break"></div>
<h2>2. Greičių skaičiavimas</h2>

<h3>2.1. Mechanizmo greičių planas</h3>
{html_vel}

<h3>2.2. Taško A greičio nustatymas</h3>
<p class="eq">V<sub>A</sub> = |&omega;<sub>1</sub>| &middot; OA = {fmt(abs(W1))} &middot; {fmt(OA)} = {fmt(vA_mag)} m/s.</p>
<p>Kadangi &omega;<sub>1</sub> &lt; 0 (sukasi pagal laikrodžio rodyklę), greičio V<sub>A</sub> vektorius nukreiptas {fmt(norm_deg(alfa-90))}&deg; kampu.</p>

<h3>2.3. Taško D greičio nustatymas</h3>
<p>Vektorinė lygtis: {vector_text(0,0,'V','D')} = {vector_text(0,0,'V','A')} + {vector_text(0,0,'V','DA')}</p>
<p>Žinoma, kad {vector_text(0,0,'V','A')} &perp; (OA), {vector_text(0,0,'V','D')} &parallel; (k) ir {vector_text(0,0,'V','DA')} &perp; (DA). Randame V<sub>D</sub> ir V<sub>DA</sub> sprendžiant lygčių sistemą projekcijomis į x ir y ašis.</p>
<p>Projekcijų į x ir y ašis lygtys:</p>
<p class="eq"><b>x:</b> V<sub>D</sub> &middot; cos({fmt(phi)}&deg;) = V<sub>A</sub> &middot; cos({fmt(theta_VA)}&deg;) + V<sub>DA</sub> &middot; cos({fmt(theta_VDA_base)}&deg;)</p>
<p class="eq"><b>y:</b> V<sub>D</sub> &middot; sin({fmt(phi)}&deg;) = V<sub>A</sub> &middot; sin({fmt(theta_VA)}&deg;) + V<sub>DA</sub> &middot; sin({fmt(theta_VDA_base)}&deg;)</p>
<p>Įstatome skaitines reikšmes:</p>
<p class="eq"><b>x:</b> V<sub>D</sub> &middot; ({fmt(math.cos(rad(phi)))}) = {fmt(vA_mag)} &middot; ({fmt(math.cos(rad(theta_VA)))}) + V<sub>DA</sub> &middot; ({fmt(math.cos(rad(theta_VDA_base)))})</p>
<p class="eq"><b>y:</b> V<sub>D</sub> &middot; ({fmt(math.sin(rad(phi)))}) = {fmt(vA_mag)} &middot; ({fmt(math.sin(rad(theta_VA)))}) + V<sub>DA</sub> &middot; ({fmt(math.sin(rad(theta_VDA_base)))})</p>
<p>Išsprendę gauname:</p>
<p class="eq">V<sub>D</sub> = {fmt(abs(vD_mag_alg))} m/s, V<sub>DA</sub> = {fmt(abs(vDA_mag_alg))} m/s.</p>
<p>Grandies AD kampinis greitis:</p>
<p class="eq">&omega;<sub>2</sub> = V<sub>DA</sub> / AD = {fmt(abs(vDA_mag_alg))} / {fmt(AD)} = {fmt(abs(w2))} rad/s.</p>
{poly_D}

<h3>2.4. Taško B greičio nustatymas</h3>
<p>Vektorinė lygtis: {vector_text(0,0,'V','B')} = {vector_text(0,0,'V','A')} + {vector_text(0,0,'V','BA')}</p>
<p class="eq">V<sub>BA</sub> = |&omega;<sub>2</sub>| &middot; AB = {fmt(abs(w2))} &middot; {fmt(AB)} = {fmt(mag(vBA))} m/s.</p>
<p class="eq">V<sub>B</sub> = {fmt(mag(vB))} m/s.</p>
{poly_B}

<div class="page-break"></div>
<h3>2.5. Taško E greičio nustatymas</h3>
<p>Vektorinė lygtis: {vector_text(0,0,'V','E')} = {vector_text(0,0,'V','B')} + {vector_text(0,0,'V','EB')}</p>
<p>Žinoma, kad {vector_text(0,0,'V','E')} &perp; (O<sub>2</sub>E) ir {vector_text(0,0,'V','EB')} &perp; (BE).</p>
<p>Projekcijų į x ir y ašis lygtys:</p>
<p class="eq"><b>x:</b> V<sub>E</sub> &middot; cos({fmt(theta_VE_base)}&deg;) = V<sub>B,x</sub> + V<sub>EB</sub> &middot; cos({fmt(theta_VEB_base)}&deg;)</p>
<p class="eq"><b>y:</b> V<sub>E</sub> &middot; sin({fmt(theta_VE_base)}&deg;) = V<sub>B,y</sub> + V<sub>EB</sub> &middot; sin({fmt(theta_VEB_base)}&deg;)</p>
<p>Įstatome skaitines reikšmes (kur V<sub>B,x</sub>={fmt(vB[0])}, V<sub>B,y</sub>={fmt(vB[1])}):</p>
<p class="eq"><b>x:</b> V<sub>E</sub> &middot; ({fmt(math.cos(rad(theta_VE_base)))}) = {fmt(vB[0])} + V<sub>EB</sub> &middot; ({fmt(math.cos(rad(theta_VEB_base)))})</p>
<p class="eq"><b>y:</b> V<sub>E</sub> &middot; ({fmt(math.sin(rad(theta_VE_base)))}) = {fmt(vB[1])} + V<sub>EB</sub> &middot; ({fmt(math.sin(rad(theta_VEB_base)))})</p>
<p>Išsprendę gauname:</p>
<p class="eq">V<sub>E</sub> = {fmt(abs(vE_mag_alg))} m/s, V<sub>EB</sub> = {fmt(abs(vEB_mag_alg))} m/s.</p>
<p>Grandžių kampiniai greičiai:</p>
<p class="eq">&omega;<sub>3</sub> = V<sub>EB</sub> / EB = {fmt(abs(vEB_mag_alg))} / {fmt(EB)} = {fmt(abs(w3))} rad/s.</p>
<p class="eq">&omega;<sub>4</sub> = V<sub>E</sub> / EO<sub>2</sub> = {fmt(abs(vE_mag_alg))} / {fmt(EO2)} = {fmt(abs(w4))} rad/s.</p>
{poly_E}

<div class="page-break"></div>
<h2>3. Pagreičių skaičiavimas</h2>

<h3>3.1. Mechanizmo pagreičių planas</h3>
{html_acc}

<h3>3.2. Taško A pagreičio nustatymas</h3>
<p>Kadangi grandinės kampinis pagreitis &varepsilon;<sub>1</sub> = 0, tai tangentinis pagreitis lygus nuliui (a<sub>A</sub><sup>&tau;</sup> = 0).</p>
<p class="eq">a<sub>A</sub> = a<sub>A</sub><sup>n</sup> = &omega;<sub>1</sub><sup>2</sup> &middot; OA = {fmt(W1)}<sup>2</sup> &middot; {fmt(OA)} = {fmt(aA_mag)} m/s<sup>2</sup>.</p>
<p>Kryptis nuo A link O sukimosi centru ({fmt(theta_aA)}&deg;).</p>

<h3>3.3. Taško D pagreičio nustatymas</h3>
<p>Vektorinė lygtis: {vector_text(0,0,'a','D')} = {vector_text(0,0,'a','A')} + {vector_text(0,0,'a','DA<tspan dy="-5">n</tspan>')} + {vector_text(0,0,'a','DA<tspan dy="-5">&tau;</tspan>')}</p>
<p class="eq">a<sub>DA</sub><sup>n</sup> = &omega;<sub>2</sub><sup>2</sup> &middot; AD = {fmt(w2)}<sup>2</sup> &middot; {fmt(AD)} = {fmt(mag(aDAn))} m/s<sup>2</sup>.</p>
<p>Kryptis nuo D link A ({fmt(theta_aDAn)}&deg;).</p>
<p>Projekcijų į x ir y ašis lygtys (pažymėkime sumą b<sub>x</sub> = a<sub>Ax</sub> + a<sub>DA,x</sub><sup>n</sup> = {fmt(b_vec_a[0])}, b<sub>y</sub> = a<sub>Ay</sub> + a<sub>DA,y</sub><sup>n</sup> = {fmt(b_vec_a[1])}):</p>
<p class="eq"><b>x:</b> a<sub>D</sub> &middot; cos({fmt(phi)}&deg;) = b<sub>x</sub> + a<sub>DA</sub><sup>&tau;</sup> &middot; cos({fmt(theta_aDAt_base)}&deg;)</p>
<p class="eq"><b>y:</b> a<sub>D</sub> &middot; sin({fmt(phi)}&deg;) = b<sub>y</sub> + a<sub>DA</sub><sup>&tau;</sup> &middot; sin({fmt(theta_aDAt_base)}&deg;)</p>
<p>Įstatome skaitines reikšmes:</p>
<p class="eq"><b>x:</b> a<sub>D</sub> &middot; ({fmt(math.cos(rad(phi)))}) = {fmt(b_vec_a[0])} + a<sub>DA</sub><sup>&tau;</sup> &middot; ({fmt(math.cos(rad(theta_aDAt_base)))})</p>
<p class="eq"><b>y:</b> a<sub>D</sub> &middot; ({fmt(math.sin(rad(phi)))}) = {fmt(b_vec_a[1])} + a<sub>DA</sub><sup>&tau;</sup> &middot; ({fmt(math.sin(rad(theta_aDAt_base)))})</p>
<p>Sprendžiant lygčių sistemą randame:</p>
<p class="eq">a<sub>D</sub> = {fmt(abs(aD_mag_alg))} m/s<sup>2</sup>, a<sub>DA</sub><sup>&tau;</sup> = {fmt(abs(aDAt_mag_alg))} m/s<sup>2</sup>.</p>
<p>Grandies AD kampinis pagreitis:</p>
<p class="eq">&varepsilon;<sub>2</sub> = a<sub>DA</sub><sup>&tau;</sup> / AD = {fmt(abs(aDAt_mag_alg))} / {fmt(AD)} = {fmt(abs(eps2))} rad/s<sup>2</sup>.</p>
{poly_aD}

<div class="page-break"></div>
<h3>3.4. Taško B pagreičio nustatymas</h3>
<p>Kadangi taškas B yra grandies AD viduryje:</p>
<p class="eq">{vector_text(0,0,'a','B')} = {vector_text(0,0,'a','A')} + {vector_text(0,0,'a','BA<tspan dy="-5">n</tspan>')} + {vector_text(0,0,'a','BA<tspan dy="-5">&tau;</tspan>')}</p>
<p class="eq">a<sub>B</sub> = {fmt(mag(aB))} m/s<sup>2</sup>.</p>
{poly_aB}

<h3>3.5. Taško E pagreičio nustatymas</h3>
<p>Vektorinė lygtis: {vector_text(0,0,'a','E<tspan dy="-5">n</tspan>')} + {vector_text(0,0,'a','E<tspan dy="-5">&tau;</tspan>')} = {vector_text(0,0,'a','B')} + {vector_text(0,0,'a','EB<tspan dy="-5">n</tspan>')} + {vector_text(0,0,'a','EB<tspan dy="-5">&tau;</tspan>')}</p>
<p class="eq">a<sub>E</sub><sup>n</sup> = &omega;<sub>4</sub><sup>2</sup> &middot; EO<sub>2</sub> = {fmt(mag(aEn))} m/s<sup>2</sup>.</p>
<p class="eq">a<sub>EB</sub><sup>n</sup> = &omega;<sub>3</sub><sup>2</sup> &middot; EB = {fmt(mag(aEBn))} m/s<sup>2</sup>.</p>
<p>Projekcijų į x ir y ašis lygtys (pažymėkime laisvųjų narių sumą b<sub>x</sub> = a<sub>Bx</sub> + a<sub>EB,x</sub><sup>n</sup> - a<sub>E,x</sub><sup>n</sup> = {fmt(b_vec_a2[0])}, b<sub>y</sub> = a<sub>By</sub> + a<sub>EB,y</sub><sup>n</sup> - a<sub>E,y</sub><sup>n</sup> = {fmt(b_vec_a2[1])}):</p>
<p class="eq"><b>x:</b> a<sub>E</sub><sup>&tau;</sup> &middot; cos({fmt(theta_aEt_base)}&deg;) = b<sub>x</sub> + a<sub>EB</sub><sup>&tau;</sup> &middot; cos({fmt(theta_aEBt_base)}&deg;)</p>
<p class="eq"><b>y:</b> a<sub>E</sub><sup>&tau;</sup> &middot; sin({fmt(theta_aEt_base)}&deg;) = b<sub>y</sub> + a<sub>EB</sub><sup>&tau;</sup> &middot; sin({fmt(theta_aEBt_base)}&deg;)</p>
<p>Įstatome skaitines reikšmes:</p>
<p class="eq"><b>x:</b> a<sub>E</sub><sup>&tau;</sup> &middot; ({fmt(math.cos(rad(theta_aEt_base)))}) = {fmt(b_vec_a2[0])} + a<sub>EB</sub><sup>&tau;</sup> &middot; ({fmt(math.cos(rad(theta_aEBt_base)))})</p>
<p class="eq"><b>y:</b> a<sub>E</sub><sup>&tau;</sup> &middot; ({fmt(math.sin(rad(theta_aEt_base)))}) = {fmt(b_vec_a2[1])} + a<sub>EB</sub><sup>&tau;</sup> &middot; ({fmt(math.sin(rad(theta_aEBt_base)))})</p>
<p>Sprendžiant lygčių sistemą randame:</p>
<p class="eq">a<sub>E</sub><sup>&tau;</sup> = {fmt(abs(aEt_mag_alg))} m/s<sup>2</sup>, a<sub>EB</sub><sup>&tau;</sup> = {fmt(abs(aEBt_mag_alg))} m/s<sup>2</sup>.</p>
<p class="eq">a<sub>E</sub> = {fmt(mag(aE))} m/s<sup>2</sup>.</p>
<p>Grandžių kampiniai pagreičiai:</p>
<p class="eq">&varepsilon;<sub>3</sub> = a<sub>EB</sub><sup>&tau;</sup> / EB = {fmt(abs(eps3))} rad/s<sup>2</sup>.</p>
<p class="eq">&varepsilon;<sub>4</sub> = a<sub>E</sub><sup>&tau;</sup> / EO<sub>2</sub> = {fmt(abs(eps4))} rad/s<sup>2</sup>.</p>
{poly_aE}

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
print("Generated updated HTML with fixed vector labels and full equations!")
