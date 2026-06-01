import math

# Duomenys pagal varianto paveikslėlį
F_mag = 30.00
q12 = 35.00
q11 = 7.00
M_couple = 18.00 # kNm, clockwise -> -18.00
alpha = 50.0

l1, l2, l3, l4, l5, l6, l7, l8 = 4.0, 5.0, 1.0, 1.0, 5.0, 1.5, 2.0, 7.0

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

def get_marker():
    return """
    <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="black" />
        </marker>
        <marker id="arrow_right" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="black" />
        </marker>
    </defs>
    """

def get_hatch(x1, x2, y, vertical=False, up=True, count=5, angle=0):
    h = ""
    if angle != 0:
        # Custom hatch for inclined plane
        dx = (x2 - x1) / count
        for i in range(count+1):
            hx = x1 + i * dx
            hy = y + (hx - x1) * math.tan(math.radians(angle))
            hx2 = hx - 5 * math.cos(math.radians(angle + 90))
            hy2 = hy - 5 * math.sin(math.radians(angle + 90))
            h += f'<line x1="{hx}" y1="{hy}" x2="{hx2}" y2="{hy2}" stroke="black" stroke-width="1"/>'
        return h
        
    if not vertical:
        dx = (x2 - x1) / count
        for i in range(count+1):
            hx = x1 + i * dx
            if up:
                h += f'<line x1="{hx}" y1="{y}" x2="{hx-5}" y2="{y-8}" stroke="black" stroke-width="1"/>'
            else:
                h += f'<line x1="{hx}" y1="{y}" x2="{hx+5}" y2="{y+8}" stroke="black" stroke-width="1"/>'
    else:
        dy = (x2 - x1) / count
        for i in range(count+1):
            hy = x1 + i * dy
            if up: # wall on right
                h += f'<line x1="{y}" y1="{hy}" x2="{y+8}" y2="{hy-5}" stroke="black" stroke-width="1"/>'
            else: # wall on left
                h += f'<line x1="{y}" y1="{hy}" x2="{y-8}" y2="{hy+5}" stroke="black" stroke-width="1"/>'
    return h

def get_vector_text(x, y, text, sub="", color="black"):
    return f'<text x="{x}" y="{y}" fill="{color}" font-style="italic" font-weight="bold"><tspan text-decoration="overline">{text}</tspan><tspan dy="5" font-size="10" text-decoration="none">{sub}</tspan></text>'

def generate():
    # O yra kairiojo rėmo kampo apačioje (koordinačių pradžia)
    O = (0.0, 0.0)
    C1 = (0.0, 0.0)   # kairysis apatinis rėmo kampas = taškas O
    C2 = (l2 + l1, 0.0)
    B = (0.0, l4 + l5 + l6 + l7)
    A = (l2 + l1, l8)
    K = (l2, 0.0)      # jėgos F taškas: l2=5 nuo O
    
    # Trapecinė apkrova
    Q_mag = 0.5 * (q11 + q12) * l6
    Q_y_bot = l4 + l5
    Q_y_top = l4 + l5 + l6
    y_Q = Q_y_bot + l6 / 3.0 * (2 * q12 + q11) / (q12 + q11)
    P = (C1[0], y_Q)
    
    Qx = Q_mag
    Qy = 0.0
    
    Fx = 0.0
    Fy = F_mag
    
    M = -M_couple
    
    # Atramos B reakcijos kampas = 140° (jei plokštuma -50° nuo horizontalės)
    # Trikampis rodo į sieną, todėl reakcija eina "iš sienos" žemyn? 
    # Plokštuma yra lyg po volais? Brėžinyje (crop 1) parodyta:
    # horizontali linija, plokštuma žemyn kampu alfa. Trikampis virš jos, taigi volai ant plokštumos. 
    # Siena viršuje ar apačioje? Štrichai paprastai rodo "žemę".
    # Jei štrichai viršuje, siena viršuje, reakcija žemyn. Bet paprastai statikoje visada žymime pliusą ir iš lygtis randam.
    # Naudosime kampą 140° (į viršų-kairę).
    theta_B = math.radians(140)
    
    # Lygčių sprendimas
    # sum MA = 0
    # MB_RB = r_B x R_B = (x_B - x_A)*R_By - (y_B - y_A)*R_Bx
    # = (1.0 - 10.0)*(RB*sin140) - (9.5 - 7.0)*(RB*cos140) = RB * (-9*sin140 - 2.5*cos140)
    term_RB = (B[0] - A[0]) * math.sin(theta_B) - (B[1] - A[1]) * math.cos(theta_B)
    
    MA_Q = (P[0] - A[0]) * Qy - (P[1] - A[1]) * Qx # (1 - 10)*0 - (6.916 - 7)*31.5 = 2.625
    MA_F = (K[0] - A[0]) * Fy - (K[1] - A[1]) * Fx # (6 - 10)*30 - (-7)*0 = -120
    
    RB = -(MA_Q + MA_F + M) / term_RB
    
    # sum Fx = 0
    RAx = -RB * math.cos(theta_B) - Qx
    
    # sum Fy = 0
    RAy = -RB * math.sin(theta_B) - Fy
    
    # Patikrinimas apie O
    MO_RA = A[0] * RAy - A[1] * RAx
    MO_RB = B[0] * RB * math.sin(theta_B) - B[1] * RB * math.cos(theta_B)
    MO_Q = P[0] * Qy - P[1] * Qx
    MO_F = K[0] * Fy - K[1] * Fx
    
    MO_sum = MO_RA + MO_RB + MO_Q + MO_F + M
    
    # Generuojame SVG (Mastelis)
    scale = 45
    ox, oy = 100, 480
    
    def s_x(x): return ox + x * scale
    def s_y(y): return oy - y * scale
    
    svg_geometry = f"""
    <svg width="700" height="550" viewBox="0 0 700 550">
        {get_marker()}
        <!-- Strypai -->
        <line x1="{s_x(C1[0])}" y1="{s_y(B[1])}" x2="{s_x(C1[0])}" y2="{s_y(C1[1])}" stroke="black" stroke-width="4" />
        <line x1="{s_x(C1[0])}" y1="{s_y(C1[1])}" x2="{s_x(C2[0])}" y2="{s_y(C2[1])}" stroke="black" stroke-width="4" />
        <line x1="{s_x(C2[0])}" y1="{s_y(C2[1])}" x2="{s_x(A[0])}" y2="{s_y(A[1])}" stroke="black" stroke-width="4" />
        
        <!-- Atramos A -->
        <circle cx="{s_x(A[0])}" cy="{s_y(A[1])}" r="4" fill="white" stroke="black" stroke-width="2"/>
        <path d="M {s_x(A[0])} {s_y(A[1])-4} L {s_x(A[0])+20} {s_y(A[1])-15} L {s_x(A[0])+20} {s_y(A[1])+15} Z" fill="none" stroke="black" stroke-width="2"/>
        <line x1="{s_x(A[0])+20}" y1="{s_y(A[1])-25}" x2="{s_x(A[0])+20}" y2="{s_y(A[1])+25}" stroke="black" stroke-width="2"/>
        {get_hatch(s_y(A[1]) - 25, s_y(A[1]) + 25, s_x(A[0]) + 20, vertical=True, up=True)}
        
        <!-- Atrama B -->
        <circle cx="{s_x(B[0])}" cy="{s_y(B[1])}" r="4" fill="white" stroke="black" stroke-width="2"/>
        <g transform="translate({s_x(B[0])}, {s_y(B[1])}) rotate(140)">
            <path d="M 0 4 L -15 20 L 15 20 Z" fill="none" stroke="black" stroke-width="2"/>
            <line x1="-25" y1="20" x2="25" y2="20" stroke="black" stroke-width="2"/>
            <!-- Hatch marks on the support -->
            <line x1="-20" y1="20" x2="-25" y2="28" stroke="black" stroke-width="1"/>
            <line x1="-10" y1="20" x2="-15" y2="28" stroke="black" stroke-width="1"/>
            <line x1="0" y1="20" x2="-5" y2="28" stroke="black" stroke-width="1"/>
            <line x1="10" y1="20" x2="5" y2="28" stroke="black" stroke-width="1"/>
            <line x1="20" y1="20" x2="15" y2="28" stroke="black" stroke-width="1"/>
        </g>
        
        <!-- Kampas alfa -->
        <line x1="{s_x(B[0])}" y1="{s_y(B[1])-10}" x2="{s_x(B[0])+80}" y2="{s_y(B[1])-10}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(B[0])+20}" y1="{s_y(B[1])-10+20*math.tan(math.radians(50))}" x2="{s_x(B[0])+80}" y2="{s_y(B[1])-10+80*math.tan(math.radians(50))}" stroke="gray" stroke-width="1"/>
        <path d="M {s_x(B[0])+50} {s_y(B[1])-10} A 50 50 0 0 1 {s_x(B[0])+50*math.cos(math.radians(50))} {s_y(B[1])-10+50*math.sin(math.radians(50))}" fill="none" stroke="gray" stroke-width="1"/>
        <text x="{s_x(B[0])+60}" y="{s_y(B[1])+10}" font-style="italic" fill="gray">&alpha;</text>

        <!-- Jėga F -->
        <line x1="{s_x(K[0])}" y1="{s_y(K[1]) + 40}" x2="{s_x(K[0])}" y2="{s_y(K[1])}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
        {get_vector_text(s_x(K[0]) + 10, s_y(K[1]) + 30, 'F', '')}

        <!-- Išskirstyta apkrova -->
        <polygon points="{s_x(C1[0])},{s_y(Q_y_bot)} {s_x(C1[0])-q11/35*50},{s_y(Q_y_bot)} {s_x(C1[0])-50},{s_y(Q_y_top)} {s_x(C1[0])},{s_y(Q_y_top)}" fill="none" stroke="black" stroke-width="1"/>
        <line x1="{s_x(C1[0])-q11/35*50}" y1="{s_y(Q_y_bot)}" x2="{s_x(C1[0])}" y2="{s_y(Q_y_bot)}" stroke="black" stroke-width="1" marker-end="url(#arrow_right)"/>
        <line x1="{s_x(C1[0])-50}" y1="{s_y(Q_y_top)}" x2="{s_x(C1[0])}" y2="{s_y(Q_y_top)}" stroke="black" stroke-width="1" marker-end="url(#arrow_right)"/>
        <line x1="{s_x(C1[0])-(q11/35*50 + 0.33*(50-q11/35*50))}" y1="{s_y(Q_y_bot + 0.33*l6)}" x2="{s_x(C1[0])}" y2="{s_y(Q_y_bot + 0.33*l6)}" stroke="black" stroke-width="1" marker-end="url(#arrow_right)"/>
        <line x1="{s_x(C1[0])-(q11/35*50 + 0.66*(50-q11/35*50))}" y1="{s_y(Q_y_bot + 0.66*l6)}" x2="{s_x(C1[0])}" y2="{s_y(Q_y_bot + 0.66*l6)}" stroke="black" stroke-width="1" marker-end="url(#arrow_right)"/>
        <text x="{s_x(C1[0]) - 40}" y="{s_y(Q_y_bot) + 15}" font-style="italic">q&#8321;&#8321;</text>
        <text x="{s_x(C1[0]) - 50}" y="{s_y(Q_y_top) - 5}" font-style="italic">q&#8321;&#8322;</text>

        <!-- Momentas -->
        <path d="M {s_x(A[0])-20} {s_y(A[1]/2)-30} A 25 25 0 1 1 {s_x(A[0])-20} {s_y(A[1]/2)+30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <text x="{s_x(A[0])-50}" y="{s_y(A[1]/2)+5}" font-style="italic" font-weight="bold">M</text>

        <!-- Matmenys horizontalūs (apačioje) -->
        <line x1="{s_x(O[0])}" y1="{s_y(O[1])}" x2="{s_x(O[0])}" y2="{s_y(0)+60}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(C1[0])}" y1="{s_y(C1[1])}" x2="{s_x(C1[0])}" y2="{s_y(0)+60}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(K[0])}" y1="{s_y(K[1])}" x2="{s_x(K[0])}" y2="{s_y(0)+60}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(A[0])}" y1="{s_y(0)}" x2="{s_x(A[0])}" y2="{s_y(0)+60}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        
        <line x1="{s_x(O[0])}" y1="{s_y(0)+50}" x2="{s_x(C1[0])}" y2="{s_y(0)+50}" stroke="gray" stroke-width="1"/>
        <line x1="{s_x(C1[0])}" y1="{s_y(0)+50}" x2="{s_x(K[0])}" y2="{s_y(0)+50}" stroke="gray" stroke-width="1"/>
        <line x1="{s_x(K[0])}" y1="{s_y(0)+50}" x2="{s_x(A[0])}" y2="{s_y(0)+50}" stroke="gray" stroke-width="1"/>
        
        <text x="{s_x((O[0]+C1[0])/2)-10}" y="{s_y(0)+45}" fill="gray">l&#8323;</text>
        <text x="{s_x((C1[0]+K[0])/2)-10}" y="{s_y(0)+45}" fill="gray">l&#8322;</text>
        <text x="{s_x((K[0]+A[0])/2)-10}" y="{s_y(0)+45}" fill="gray">l&#8321;</text>

        <!-- Matmenys vertikalūs (kairėje) -->
        <line x1="{s_x(C1[0])}" y1="{s_y(C1[1])}" x2="{s_x(0)-70}" y2="{s_y(C1[1])}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(C1[0])}" y1="{s_y(l4)}" x2="{s_x(0)-70}" y2="{s_y(l4)}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(C1[0])}" y1="{s_y(Q_y_bot)}" x2="{s_x(0)-70}" y2="{s_y(Q_y_bot)}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(C1[0])}" y1="{s_y(Q_y_top)}" x2="{s_x(0)-70}" y2="{s_y(Q_y_top)}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(B[0])}" y1="{s_y(B[1])}" x2="{s_x(0)-70}" y2="{s_y(B[1])}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        
        <line x1="{s_x(0)-60}" y1="{s_y(C1[1])}" x2="{s_x(0)-60}" y2="{s_y(l4)}" stroke="gray" stroke-width="1"/>
        <line x1="{s_x(0)-60}" y1="{s_y(l4)}" x2="{s_x(0)-60}" y2="{s_y(Q_y_bot)}" stroke="gray" stroke-width="1"/>
        <line x1="{s_x(0)-60}" y1="{s_y(Q_y_bot)}" x2="{s_x(0)-60}" y2="{s_y(Q_y_top)}" stroke="gray" stroke-width="1"/>
        <line x1="{s_x(0)-60}" y1="{s_y(Q_y_top)}" x2="{s_x(0)-60}" y2="{s_y(B[1])}" stroke="gray" stroke-width="1"/>
        
        <text x="{s_x(0)-80}" y="{s_y(C1[1]+l4/2)+5}" fill="gray">l&#8324;</text>
        <text x="{s_x(0)-80}" y="{s_y(l4+l5/2)+5}" fill="gray">l&#8325;</text>
        <text x="{s_x(0)-80}" y="{s_y(Q_y_bot+l6/2)+5}" fill="gray">l&#8326;</text>
        <text x="{s_x(0)-80}" y="{s_y(Q_y_top+l7/2)+5}" fill="gray">l&#8327;</text>

        <!-- Matmenys vertikalūs (dešinėje) -->
        <line x1="{s_x(A[0])}" y1="{s_y(A[1])}" x2="{s_x(A[0])+50}" y2="{s_y(A[1])}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(C2[0])}" y1="{s_y(C2[1])}" x2="{s_x(C2[0])+50}" y2="{s_y(C2[1])}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(A[0])+40}" y1="{s_y(A[1])}" x2="{s_x(C2[0])+40}" y2="{s_y(C2[1])}" stroke="gray" stroke-width="1"/>
        <text x="{s_x(A[0])+50}" y="{s_y(A[1]/2)+5}" fill="gray">l&#8334;</text>

        <!-- Taškas O -->
        <circle cx="{s_x(O[0])}" cy="{s_y(O[1])}" r="3" fill="black" stroke="black" />
        <text x="{s_x(O[0])-20}" y="{s_y(O[1])+5}" font-style="italic">O</text>

        <text x="{s_x(A[0])-15}" y="{s_y(A[1])-15}" font-style="italic" font-size="18">A</text>
        <text x="{s_x(B[0])-25}" y="{s_y(B[1])+10}" font-style="italic" font-size="18">B</text>
    </svg>
    """

    svg_forces = f"""
    <svg width="700" height="550" viewBox="0 0 700 550">
        {get_marker()}
        <!-- Strypai -->
        <line x1="{s_x(C1[0])}" y1="{s_y(B[1])}" x2="{s_x(C1[0])}" y2="{s_y(C1[1])}" stroke="gray" stroke-width="4" />
        <line x1="{s_x(C1[0])}" y1="{s_y(C1[1])}" x2="{s_x(C2[0])}" y2="{s_y(C2[1])}" stroke="gray" stroke-width="4" />
        <line x1="{s_x(C2[0])}" y1="{s_y(C2[1])}" x2="{s_x(A[0])}" y2="{s_y(A[1])}" stroke="gray" stroke-width="4" />
        
        <circle cx="{s_x(A[0])}" cy="{s_y(A[1])}" r="4" fill="white" stroke="gray" stroke-width="2"/>
        <circle cx="{s_x(B[0])}" cy="{s_y(B[1])}" r="4" fill="white" stroke="gray" stroke-width="2"/>
        
        <!-- Reakcijos -->
        <line x1="{s_x(A[0])}" y1="{s_y(A[1])}" x2="{s_x(A[0])-50}" y2="{s_y(A[1])}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        {get_vector_text(s_x(A[0])-60, s_y(A[1])-5, 'R', 'Ax')}
        <line x1="{s_x(A[0])}" y1="{s_y(A[1])}" x2="{s_x(A[0])}" y2="{s_y(A[1])+50}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        {get_vector_text(s_x(A[0])+10, s_y(A[1])+40, 'R', 'Ay')}
        
        <line x1="{s_x(B[0])}" y1="{s_y(B[1])}" x2="{s_x(B[0]) + 50*math.cos(theta_B)}" y2="{s_y(B[1]) - 50*math.sin(theta_B)}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        {get_vector_text(s_x(B[0]) + 50*math.cos(theta_B) - 10, s_y(B[1]) - 50*math.sin(theta_B) - 10, 'R', 'B')}

        <!-- Jėga F -->
        <line x1="{s_x(K[0])}" y1="{s_y(K[1]) + 40}" x2="{s_x(K[0])}" y2="{s_y(K[1])}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
        {get_vector_text(s_x(K[0]) + 10, s_y(K[1]) + 30, 'F', '')}
        
        <!-- Jėga Q atstojamoji -->
        <line x1="{s_x(P[0])-50}" y1="{s_y(P[1])}" x2="{s_x(P[0])}" y2="{s_y(P[1])}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
        {get_vector_text(s_x(P[0]) - 60, s_y(P[1]) - 10, 'Q', '')}

        <!-- Momentas -->
        <path d="M {s_x(A[0])-20} {s_y(A[1]/2)-30} A 25 25 0 1 1 {s_x(A[0])-20} {s_y(A[1]/2)+30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <text x="{s_x(A[0])-50}" y="{s_y(A[1]/2)+5}" font-style="italic" font-weight="bold">M</text>

        <!-- Patikrinimo taškas O -->
        <circle cx="{s_x(O[0])}" cy="{s_y(O[1])}" r="3" fill="none" stroke="gray" />
        <text x="{s_x(O[0])-20}" y="{s_y(O[1])+5}" font-style="italic" fill="gray">O</text>
        
        <text x="{s_x(A[0])-15}" y="{s_y(A[1])-15}" font-style="italic" font-size="18">A</text>
        <text x="{s_x(B[0])-25}" y="{s_y(B[1])+10}" font-style="italic" font-size="18">B</text>
    </svg>
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
<h1 style="margin-top: 40vh;">Statikos Namų Darbas</h1>
<h1>U-formos rėmo atraminių reakcijų skaičiavimas</h1>
</div>

<h2>1. Užduoties lapas</h2>
<p><b>Užduoties duomenys:</b></p>
<p><span class="math">l<sub>1</sub></span> = {fmt(l1)} m; <span class="math">l<sub>2</sub></span> = {fmt(l2)} m; <span class="math">l<sub>3</sub></span> = {fmt(l3)} m; <span class="math">l<sub>4</sub></span> = {fmt(l4)} m; <span class="math">l<sub>5</sub></span> = {fmt(l5)} m; <span class="math">l<sub>6</sub></span> = {fmt(l6)} m; <span class="math">l<sub>7</sub></span> = {fmt(l7)} m; <span class="math">l<sub>8</sub></span> = {fmt(l8)} m;</p>
<p><span class="math">F</span> = {fmt(F_mag)} kN; <span class="math">q<sub>11</sub></span> = {fmt(q11)} kN/m; <span class="math">q<sub>12</sub></span> = {fmt(q12)} kN/m; <span class="math">M</span> = {fmt(abs(M))} kNm; <span class="math">&alpha;</span> = 50&deg;.</p>

<p>Rasti rėmo atramines reakcijas. Atlikti patikrinimą, parašant momentų lygtį apie tašką O.</p>

<p><b>2. Skaičiuojamosios schemos paruošimas:</b></p>
<p>Priimame tašką O kaip koordinačių sistemos pradžią O(0; 0). Pagal duotus matmenis nustatome taškų koordinates: A({fmt(A[0])}; {fmt(A[1])}), B({fmt(B[0])}; {fmt(B[1])}). Jėga F veikia taške K({fmt(K[0])}; {fmt(K[1])}).</p>

<p>Išskirstytą trapecinę apkrovą pakeičiame koncentruota jėga Q. Ją išskaidome į stačiakampę ir trikampę dalis. Atstojamosios modulis:</p>
<p class="eq"><span class="math">Q</span> = (q<sub>11</sub> + q<sub>12</sub>)/2 &middot; l<sub>6</sub> = ({fmt(q11)} + {fmt(q12)})/2 &middot; {fmt(l6)} = {fmt(Q_mag)} kN.</p>
<p>Apkrova veikia horizontaliai: Q<sub>x</sub> = {fmt(Qx)} kN, Q<sub>y</sub> = {fmt(Qy)} kN.</p>
<p>Jos pridėjimo taško y koordinatė (svorio centras): y<sub>Q</sub> = l<sub>4</sub> + l<sub>5</sub> + l<sub>6</sub>/3 &middot; (2q<sub>12</sub> + q<sub>11</sub>) / (q<sub>12</sub> + q<sub>11</sub>) = {fmt(y_Q)} m. Taškas P({fmt(P[0])}; {fmt(P[1])}).</p>
<p>Atramos B reakcijos R<sub>B</sub> kryptis yra statmena nuožulniajai plokštumai. Plokštuma pasvirusi 50&deg; kampu į x ašį, todėl statmens kampas su x ašimi yra 90&deg; + 50&deg; = 140&deg;.</p>

<p><b><u>Užduoties schema:</u></b></p>
<div class="schema-container">
{svg_geometry}
</div>

<p><b><u>Skaičiuojamoji schema:</u></b></p>
<div class="schema-container">
{svg_forces}
</div>

<div class="page-break"></div>
<h2>3. Sprendimas</h2>

<div style="margin-bottom: 20px;">
    <p>Užrašomos rėmo pusiausvyros sąlygos:</p>
    <div class="system-bracket">
        <p class="eq">&sum; M<sub>A</sub> = 0;</p>
        <p class="eq">&sum; F<sub>ix</sub> = 0;</p>
        <p class="eq">&sum; F<sub>iy</sub> = 0.</p>
    </div>
    <div class="system-bracket">
        <p class="eq">-R<sub>B</sub> &middot; sin(140&deg;) &middot; (x<sub>A</sub> - x<sub>B</sub>) - R<sub>B</sub> &middot; cos(140&deg;) &middot; (y<sub>B</sub> - y<sub>A</sub>) + Q &middot; (y<sub>A</sub> - y<sub>P</sub>) - F &middot; (x<sub>A</sub> - x<sub>K</sub>) - M = 0; (1)</p>
        <p class="eq">R<sub>Ax</sub> + R<sub>B</sub> &middot; cos(140&deg;) + Q = 0; (2)</p>
        <p class="eq">R<sub>Ay</sub> + R<sub>B</sub> &middot; sin(140&deg;) + F = 0. (3)</p>
    </div>
</div>

<p>Iš (1) lygties randame R<sub>B</sub>:</p>
<p class="eq">R<sub>B</sub> &middot; ( -sin(140&deg;) &middot; {fmt(A[0]-B[0])} - cos(140&deg;) &middot; {fmt(B[1]-A[1])} ) + {fmt(Q_mag)} &middot; {fmt(A[1]-P[1])} - {fmt(F_mag)} &middot; {fmt(A[0]-K[0])} - {fmt(abs(M))} = 0</p>
<p class="eq">R<sub>B</sub> &middot; ({fmt(term_RB)}) + ({fmt(MA_Q)}) + ({fmt(MA_F)}) - {fmt(abs(M))} = 0 &rarr; R<sub>B</sub> = {fmt(RB)} kN.</p>

<p>Iš (2) lygties randame R<sub>Ax</sub>:</p>
<p class="eq">R<sub>Ax</sub> = - R<sub>B</sub> &middot; cos(140&deg;) - Q = -({fmt(RB)}) &middot; cos(140&deg;) - {fmt(Q_mag)} = {fmt(RAx)} kN.</p>

<p>Iš (3) lygties randame R<sub>Ay</sub>:</p>
<p class="eq">R<sub>Ay</sub> = - R<sub>B</sub> &middot; sin(140&deg;) - F = -({fmt(RB)}) &middot; sin(140&deg;) - {fmt(F_mag)} = {fmt(RAy)} kN.</p>

<h3>3.1. Sprendimo patikrinimas</h3>
<p>Užrašoma pusiausvyros sąlyga visai sistemai apie tašką O({fmt(O[0])}; {fmt(O[1])}).</p>
<p class="eq">&sum; M<sub>O</sub> = -R<sub>Ax</sub> &middot; y<sub>A</sub> + R<sub>Ay</sub> &middot; x<sub>A</sub> - R<sub>Bx</sub> &middot; y<sub>B</sub> + R<sub>By</sub> &middot; x<sub>B</sub> - Q &middot; y<sub>P</sub> + F &middot; x<sub>K</sub> - M = 0</p>
<p class="eq">&sum; M<sub>O</sub> = -({fmt(RAx)}) &middot; {fmt(A[1])} + ({fmt(RAy)}) &middot; {fmt(A[0])} - ({fmt(RB*math.cos(math.radians(140)))}) &middot; {fmt(B[1])} + ({fmt(RB*math.sin(math.radians(140)))}) &middot; {fmt(B[0])} - {fmt(Q_mag)} &middot; {fmt(P[1])} + {fmt(F_mag)} &middot; {fmt(K[0])} - {fmt(abs(M))} = 0</p>
<p class="eq">&sum; M<sub>O</sub> = {fmt(MO_RA)} + {fmt(MO_RB)} + {fmt(MO_Q)} + {fmt(MO_F)} - {fmt(abs(M))} = {fmt(MO_sum)} kN</p>

<h3>3.2. Paklaidos skaičiavimas</h3>
<p>&Delta; = ({fmt(abs(MO_sum))} / 500) &middot; 100% = {fmt(abs(MO_sum)/5)}% &lt; 0,3%.</p>

<div class="page-break"></div>
<h2>4. Atsakymų lentelė</h2>
<table>
  <tr>
    <th>R<sub>B</sub>, kN</th>
    <th>R<sub>Ax</sub>, kN</th>
    <th>R<sub>Ay</sub>, kN</th>
  </tr>
  <tr>
    <td>{fmt(RB)}</td>
    <td>{fmt(RAx)}</td>
    <td>{fmt(RAy)}</td>
  </tr>
</table>

</body>
</html>
"""
    
    with open('/Users/ugniusvaitiekenas/srotas-ai-agent/fizika/statics_u_frame.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Sugeneruotas statics_u_frame.html ataskaitos failas!")

generate()
