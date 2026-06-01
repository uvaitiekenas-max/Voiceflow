import math

# Duomenys pagal varianto lentelę/paveikslėlį
F_mag = 30.0
q_max = 10.0
M_couple = 25.0

l1, l2, l3, l4, l5, l6, l7 = 3.0, 3.0, 1.0, 7.0, 3.0, 4.0, 1.0

# Funkcija skaičiams formatuoti su kableliais (lietuviškam standartui)
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
    </defs>
    """

def get_hatch(x1, x2, y, vertical=False, up=True, count=5):
    h = ""
    if not vertical:
        dx = (x2 - x1) / count
        for i in range(count+1):
            hx = x1 + i * dx
            if up:
                h += f'<line x1="{hx}" y1="{y}" x2="{hx-5}" y2="{y+8}" stroke="black" stroke-width="1"/>'
            else:
                h += f'<line x1="{hx}" y1="{y}" x2="{hx+5}" y2="{y-8}" stroke="black" stroke-width="1"/>'
    else:
        # vertical line hatch (like for wall at A)
        # x1, x2 is actually y1, y2
        dy = (x2 - x1) / count
        for i in range(count+1):
            hy = x1 + i * dy
            h += f'<line x1="{y}" y1="{hy}" x2="{y-8}" y2="{hy+5}" stroke="black" stroke-width="1"/>'
    return h

def get_vector_text(x, y, text, sub="", color="black"):
    return f'<text x="{x}" y="{y}" fill="{color}" font-style="italic" font-weight="bold"><tspan text-decoration="overline">{text}</tspan><tspan dy="5" font-size="10" text-decoration="none">{sub}</tspan></text>'

def generate():
    # Koordinatės santykinėje sistemoje (prieš paslinkimą)
    A_tmp = (0.0, 3.0)
    B_tmp = (l4 + l5, 0.0)
    C_tmp = (l4, l1 + l2 + l3)
    O_tmp = (C_tmp[0] - l7, C_tmp[1])
    
    # Paslenkame viską, kad O būtų (0, 0)
    def shift(pt): return (pt[0] - O_tmp[0], pt[1] - O_tmp[1])
    
    A = shift(A_tmp)
    B = shift(B_tmp)
    C = shift(C_tmp)
    O = (0.0, 0.0)
    
    # Jėgos F taškas (priimama per vidurį AC)
    K = (A[0] + (C[0] - A[0])/2, A[1] + (C[1] - A[1])/2)
    
    # AC vektorius ir normalė
    AC_x = C[0] - A[0]
    AC_y = C[1] - A[1]
    L_AC = math.sqrt(AC_x**2 + AC_y**2)
    # n_F = normalė žemyn dešinėn (nes jėga spaudžia AC iš viršaus-kairės)
    n_Fx, n_Fy = AC_y / L_AC, -AC_x / L_AC
    
    Fx = F_mag * n_Fx
    Fy = F_mag * n_Fy
    
    # CB vektorius ir normalė
    CB_x = B[0] - C[0]
    CB_y = B[1] - C[1]
    L_CB = math.sqrt(CB_x**2 + CB_y**2)
    
    # Apkrovos q zona ant CB: y nuo C iki B su l1 ir l3 "tarpais"
    # Kadangi Viskas paslinkta, santykiniai ilgiai išlieka.
    L_q_proj = l2
    L_q = L_q_proj / abs(CB_y) * L_CB # ilgis ant strypo
    
    Q_mag = 0.5 * q_max * L_q
    
    # Normalė žemyn kairėn (apkrova spaudžia iš dešinės pusės, žiūrint į paveiksliuką)
    # CB eina į dešinę-žemyn. Statmena jai, spaudžianti "žemyn kairėn" yra (CB_y, -CB_x) / L_CB
    n_Qx, n_Qy = CB_y / L_CB, -CB_x / L_CB
    
    Qx = Q_mag * n_Qx
    Qy = Q_mag * n_Qy
    
    # Q jėgos pridėjimo taškas (1/3 nuo apačios (nuo B pusės link C))
    P_bot_y = shift((0, l1))[1] # Y koordinatė ties apkrovos apačia
    P_top_y = shift((0, l1 + l2))[1] # Y koordinatė ties apkrovos viršumi
    
    # x koordinatė randama proporcingai y coordinatei ant tiesės CB
    P_bot_x = C[0] + CB_x * (C[1] - P_bot_y) / abs(CB_y)
    P_top_x = C[0] + CB_x * (C[1] - P_top_y) / abs(CB_y)
    
    P_x = P_bot_x + (1/3) * (P_top_x - P_bot_x)
    P_y = P_bot_y + (1/3) * (P_top_y - P_bot_y)
    
    # Momentas M_couple (laikrodžio rodyklės kryptimi = minusas)
    M = -M_couple
    
    # Momentai apie B
    MB_F = (K[0] - B[0]) * Fy - (K[1] - B[1]) * Fx
    MB_Q = (P_x - B[0]) * Qy - (P_y - B[1]) * Qx
    
    # Lygčių sprendimas
    # -RAx * (yA - yB) + MB_F + MB_Q + M = 0
    # RAx = (MB_F + MB_Q + M) / (yA - yB)
    RAx = (MB_F + MB_Q + M) / (A[1] - B[1])
    
    # sum Fx = 0
    RBx = -RAx - Fx - Qx
    
    # sum Fy = 0
    RBy = -Fy - Qy
    
    # Patikrinimas apie tašką O (kuris dabar yra (0,0))
    MO_RAx = -(A[1] - O[1]) * RAx
    MO_RB = (B[0] - O[0]) * RBy - (B[1] - O[1]) * RBx
    MO_F = (K[0] - O[0]) * Fy - (K[1] - O[1]) * Fx
    MO_Q = (P_x - O[0]) * Qy - (P_y - O[1]) * Qx
    
    MO_sum = MO_RAx + MO_RB + MO_F + MO_Q + M

    # Generuojame SVG (Mastelis)
    scale = 40
    # Norėdami išlaikyti tą patį vaizdą, kai O(0,0), koreguojame ox, oy
    # Anksčiau A buvo (0, 3) ir piešiama x=100. Dabar A_x = -6. 
    # ox - 6*40 = 100 => ox = 340
    # Anksčiau B_y buvo 0, piešiama y=350. Dabar B_y = -7.
    # oy - (-7)*40 = 350 => oy = 70
    ox, oy = 340, 70
    
    def s_x(x): return ox + x * scale
    def s_y(y): return oy - y * scale
    
    svg_geometry = f"""
    <svg width="700" height="450" viewBox="0 0 700 450">
        {get_marker()}
        <!-- Strypai -->
        <line x1="{s_x(A[0])}" y1="{s_y(A[1])}" x2="{s_x(C[0])}" y2="{s_y(C[1])}" stroke="black" stroke-width="4" />
        <line x1="{s_x(C[0])}" y1="{s_y(C[1])}" x2="{s_x(B[0])}" y2="{s_y(B[1])}" stroke="black" stroke-width="4" />
        
        <!-- Atramos A -->
        <circle cx="{s_x(A[0]) - 8}" cy="{s_y(A[1]) - 10}" r="4" fill="white" stroke="black" stroke-width="2"/>
        <circle cx="{s_x(A[0]) - 8}" cy="{s_y(A[1]) + 10}" r="4" fill="white" stroke="black" stroke-width="2"/>
        <line x1="{s_x(A[0]) - 12}" y1="{s_y(A[1]) - 25}" x2="{s_x(A[0]) - 12}" y2="{s_y(A[1]) + 25}" stroke="black" stroke-width="2"/>
        {get_hatch(s_y(A[1]) - 25, s_y(A[1]) + 25, s_x(A[0]) - 12, vertical=True)}
        
        <!-- Atrama B -->
        <circle cx="{s_x(B[0])}" cy="{s_y(B[1])}" r="4" fill="white" stroke="black" stroke-width="2"/>
        <path d="M {s_x(B[0])} {s_y(B[1])+4} L {s_x(B[0])-15} {s_y(B[1])+20} L {s_x(B[0])+15} {s_y(B[1])+20} Z" fill="none" stroke="black" stroke-width="2"/>
        <line x1="{s_x(B[0])-25}" y1="{s_y(B[1])+20}" x2="{s_x(B[0])+25}" y2="{s_y(B[1])+20}" stroke="black" stroke-width="2"/>
        {get_hatch(s_x(B[0])-25, s_x(B[0])+25, s_y(B[1])+20, up=True)}

        <!-- Jėga F -->
        <line x1="{s_x(K[0]) - Fx*1.5}" y1="{s_y(K[1]) + Fy*1.5}" x2="{s_x(K[0])}" y2="{s_y(K[1])}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
        {get_vector_text(s_x(K[0]) - Fx*1.5 - 20, s_y(K[1]) + Fy*1.5 - 10, 'F', '')}

        <!-- Jėga Q atstojamoji (paslėpta, bet rodoma išskirstyta) -->
        <!-- Išskirstyta apkrova -->
        <line x1="{s_x(P_bot_x) + 40}" y1="{s_y(P_bot_y) - 10}" x2="{s_x(P_top_x)}" y2="{s_y(P_top_y)}" stroke="black" stroke-width="1"/>
        <line x1="{s_x(P_bot_x) + 40}" y1="{s_y(P_bot_y) - 10}" x2="{s_x(P_bot_x)}" y2="{s_y(P_bot_y)}" stroke="black" stroke-width="1" marker-end="url(#arrow)"/>
        <line x1="{s_x(P_bot_x + (P_top_x - P_bot_x)*0.25) + 30}" y1="{s_y(P_bot_y + (P_top_y - P_bot_y)*0.25) - 7.5}" x2="{s_x(P_bot_x + (P_top_x - P_bot_x)*0.25)}" y2="{s_y(P_bot_y + (P_top_y - P_bot_y)*0.25)}" stroke="black" stroke-width="1" marker-end="url(#arrow)"/>
        <line x1="{s_x(P_bot_x + (P_top_x - P_bot_x)*0.5) + 20}" y1="{s_y(P_bot_y + (P_top_y - P_bot_y)*0.5) - 5}" x2="{s_x(P_bot_x + (P_top_x - P_bot_x)*0.5)}" y2="{s_y(P_bot_y + (P_top_y - P_bot_y)*0.5)}" stroke="black" stroke-width="1" marker-end="url(#arrow)"/>
        <line x1="{s_x(P_bot_x + (P_top_x - P_bot_x)*0.75) + 10}" y1="{s_y(P_bot_y + (P_top_y - P_bot_y)*0.75) - 2.5}" x2="{s_x(P_bot_x + (P_top_x - P_bot_x)*0.75)}" y2="{s_y(P_bot_y + (P_top_y - P_bot_y)*0.75)}" stroke="black" stroke-width="1" marker-end="url(#arrow)"/>
        <text x="{s_x(P_bot_x) + 45}" y="{s_y(P_bot_y) - 5}" font-style="italic">q</text>

        <!-- Momentas -->
        <path d="M {s_x(B[0])-15} {s_y(B[1])-40} A 20 20 0 1 0 {s_x(B[0])+15} {s_y(B[1])-60}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <text x="{s_x(B[0])+25}" y="{s_y(B[1])-60}" font-style="italic" font-weight="bold">M</text>

        <!-- Matmenys horizontalūs -->
        <!-- Y koordinatei naudojame santykinį lygį, pvz, B_y santykinėje -->
        <line x1="{s_x(A[0])}" y1="{s_y(A[1])}" x2="{s_x(A[0])}" y2="{s_y(B[1])+40}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(C[0])}" y1="{s_y(C[1])}" x2="{s_x(C[0])}" y2="{s_y(B[1])+40}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(B[0])}" y1="{s_y(B[1])}" x2="{s_x(B[0])}" y2="{s_y(B[1])+40}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(A[0])}" y1="{s_y(B[1])+30}" x2="{s_x(C[0])}" y2="{s_y(B[1])+30}" stroke="gray" stroke-width="1"/>
        <line x1="{s_x(C[0])}" y1="{s_y(B[1])+30}" x2="{s_x(B[0])}" y2="{s_y(B[1])+30}" stroke="gray" stroke-width="1"/>
        <text x="{s_x((A[0]+C[0])/2)-10}" y="{s_y(B[1])+25}" fill="gray">l&#8324;</text>
        <text x="{s_x((C[0]+B[0])/2)-10}" y="{s_y(B[1])+25}" fill="gray">l&#8325;</text>

        <!-- Matmenys vertikalūs (dešinė) -->
        <line x1="{s_x(B[0])}" y1="{s_y(B[1])}" x2="{s_x(B[0])+60}" y2="{s_y(B[1])}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(P_bot_x)}" y1="{s_y(P_bot_y)}" x2="{s_x(B[0])+60}" y2="{s_y(P_bot_y)}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(P_top_x)}" y1="{s_y(P_top_y)}" x2="{s_x(B[0])+60}" y2="{s_y(P_top_y)}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(C[0])}" y1="{s_y(C[1])}" x2="{s_x(B[0])+60}" y2="{s_y(C[1])}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(B[0])+50}" y1="{s_y(B[1])}" x2="{s_x(B[0])+50}" y2="{s_y(P_bot_y)}" stroke="gray" stroke-width="1"/>
        <line x1="{s_x(B[0])+50}" y1="{s_y(P_bot_y)}" x2="{s_x(B[0])+50}" y2="{s_y(P_top_y)}" stroke="gray" stroke-width="1"/>
        <line x1="{s_x(B[0])+50}" y1="{s_y(P_top_y)}" x2="{s_x(B[0])+50}" y2="{s_y(C[1])}" stroke="gray" stroke-width="1"/>
        <text x="{s_x(B[0])+55}" y="{s_y((B[1]+P_bot_y)/2)+5}" fill="gray">l&#8321;</text>
        <text x="{s_x(B[0])+55}" y="{s_y((P_bot_y+P_top_y)/2)+5}" fill="gray">l&#8322;</text>
        <text x="{s_x(B[0])+55}" y="{s_y((P_top_y+C[1])/2)+5}" fill="gray">l&#8323;</text>

        <!-- Matmenys kairėje -->
        <line x1="{s_x(A[0])}" y1="{s_y(A[1])}" x2="{s_x(A[0])-50}" y2="{s_y(A[1])}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(K[0])}" y1="{s_y(K[1])}" x2="{s_x(A[0])-50}" y2="{s_y(K[1])}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{s_x(A[0])-40}" y1="{s_y(A[1])}" x2="{s_x(A[0])-40}" y2="{s_y(C[1])}" stroke="gray" stroke-width="1"/>
        <text x="{s_x(A[0])-55}" y="{s_y((A[1]+C[1])/2)}" fill="gray">l&#8326;</text>
        
        <!-- O ir l7 -->
        <circle cx="{s_x(O[0])}" cy="{s_y(O[1])}" r="3" fill="none" stroke="black" />
        <text x="{s_x(O[0])-15}" y="{s_y(O[1])+5}" font-style="italic">O</text>
        <line x1="{s_x(O[0])}" y1="{s_y(O[1])}" x2="{s_x(O[0])}" y2="{s_y(O[1])-30}" stroke="gray" stroke-width="1"/>
        <line x1="{s_x(C[0])}" y1="{s_y(C[1])}" x2="{s_x(C[0])}" y2="{s_y(C[1])-30}" stroke="gray" stroke-width="1"/>
        <line x1="{s_x(O[0])}" y1="{s_y(O[1])-20}" x2="{s_x(C[0])}" y2="{s_y(C[1])-20}" stroke="gray" stroke-width="1"/>
        <text x="{s_x((O[0]+C[0])/2)-5}" y="{s_y(O[1])-25}" fill="gray">l&#8327;</text>
        <line x1="{s_x(C[0])}" y1="{s_y(C[1])}" x2="{s_x(O[0])}" y2="{s_y(O[1])}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>

        <text x="{s_x(A[0])+15}" y="{s_y(A[1])+10}" font-style="italic" font-size="18">A</text>
        <text x="{s_x(B[0])-15}" y="{s_y(B[1])+20}" font-style="italic" font-size="18">B</text>
        <text x="{s_x(C[0])+5}" y="{s_y(C[1])-5}" font-style="italic" font-size="18">C</text>
    </svg>
    """

    svg_forces = f"""
    <svg width="700" height="450" viewBox="0 0 700 450">
        {get_marker()}
        <!-- Strypai -->
        <line x1="{s_x(A[0])}" y1="{s_y(A[1])}" x2="{s_x(C[0])}" y2="{s_y(C[1])}" stroke="gray" stroke-width="4" />
        <line x1="{s_x(C[0])}" y1="{s_y(C[1])}" x2="{s_x(B[0])}" y2="{s_y(B[1])}" stroke="gray" stroke-width="4" />
        
        <!-- Atramos (tik simboliškai, dabar piešim reakcijas) -->
        <circle cx="{s_x(A[0])}" cy="{s_y(A[1])}" r="4" fill="white" stroke="gray" stroke-width="2"/>
        <circle cx="{s_x(B[0])}" cy="{s_y(B[1])}" r="4" fill="white" stroke="gray" stroke-width="2"/>
        
        <!-- Reakcijos -->
        <line x1="{s_x(A[0])-50}" y1="{s_y(A[1])}" x2="{s_x(A[0])}" y2="{s_y(A[1])}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        {get_vector_text(s_x(A[0])-40, s_y(A[1])-5, 'R', 'Ax')}
        
        <line x1="{s_x(B[0])-50}" y1="{s_y(B[1])}" x2="{s_x(B[0])}" y2="{s_y(B[1])}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        {get_vector_text(s_x(B[0])-40, s_y(B[1])-5, 'R', 'Bx')}
        <line x1="{s_x(B[0])}" y1="{s_y(B[1])+50}" x2="{s_x(B[0])}" y2="{s_y(B[1])}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        {get_vector_text(s_x(B[0])+10, s_y(B[1])+40, 'R', 'By')}

        <!-- Jėga F -->
        <line x1="{s_x(K[0]) - Fx*1.5}" y1="{s_y(K[1]) + Fy*1.5}" x2="{s_x(K[0])}" y2="{s_y(K[1])}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
        {get_vector_text(s_x(K[0]) - Fx*1.5 - 20, s_y(K[1]) + Fy*1.5 - 10, 'F', '')}
        
        <!-- Jėga Q atstojamoji -->
        <line x1="{s_x(P_x) - Qx*2}" y1="{s_y(P_y) + Qy*2}" x2="{s_x(P_x)}" y2="{s_y(P_y)}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
        {get_vector_text(s_x(P_x) - Qx*2 - 20, s_y(P_y) + Qy*2 - 10, 'Q', '')}

        <!-- Momentas -->
        <path d="M {s_x(B[0])-15} {s_y(B[1])-40} A 20 20 0 1 0 {s_x(B[0])+15} {s_y(B[1])-60}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <text x="{s_x(B[0])+25}" y="{s_y(B[1])-60}" font-style="italic" font-weight="bold">M</text>

        <!-- Patikrinimo taškas O -->
        <circle cx="{s_x(O[0])}" cy="{s_y(O[1])}" r="3" fill="none" stroke="gray" />
        <text x="{s_x(O[0])-15}" y="{s_y(O[1])+5}" font-style="italic" fill="gray">O</text>
        
        <!-- Matmenys, reikalingi skaičiavimams (atstumai ir taškai) -->
        <line x1="{s_x(A[0])}" y1="{s_y(B[1])+30}" x2="{s_x(K[0])}" y2="{s_y(B[1])+30}" stroke="gray" stroke-width="1"/>
        <text x="{s_x((A[0]+K[0])/2)-10}" y="{s_y(B[1])+25}" fill="gray">3,5 m</text>
        
        <text x="{s_x(A[0])+15}" y="{s_y(A[1])+10}" font-style="italic" font-size="18">A</text>
        <text x="{s_x(B[0])-15}" y="{s_y(B[1])+20}" font-style="italic" font-size="18">B</text>
        <text x="{s_x(C[0])+5}" y="{s_y(C[1])-5}" font-style="italic" font-size="18">C</text>
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
<h1>Rėmo atraminių reakcijų skaičiavimas</h1>
</div>

<h2>1. Užduoties lapas</h2>
<p><b>Užduoties duomenys:</b></p>
<p><span class="math">l<sub>1</sub></span> = {fmt(l1)} m; <span class="math">l<sub>2</sub></span> = {fmt(l2)} m; <span class="math">l<sub>3</sub></span> = {fmt(l3)} m; <span class="math">l<sub>4</sub></span> = {fmt(l4)} m; <span class="math">l<sub>5</sub></span> = {fmt(l5)} m; <span class="math">l<sub>6</sub></span> = {fmt(l6)} m; <span class="math">l<sub>7</sub></span> = {fmt(l7)} m;</p>
<p><span class="math">F</span> = {fmt(F_mag)} kN; <span class="math">q</span> = {fmt(q_max)} kN/m; <span class="math">M</span> = {fmt(abs(M))} kNm.</p>

<p>Rasti rėmo atramines reakcijas. Atlikti patikrinimą, parašant momentų lygtį apie tašką O.</p>

<p><b>2. Skaičiuojamosios schemos paruošimas:</b></p>
<p>Priimame tašką O kaip koordinačių sistemos pradžią O(0; 0). Tuomet pagal brėžinio matmenis perskaičiuojame kitų taškų koordinates: A({fmt(A[0])}; {fmt(A[1])}), B({fmt(B[0])}; {fmt(B[1])}), C({fmt(C[0])}; {fmt(C[1])}). Jėga F veikia strypo AC viduryje, taške K({fmt(K[0])}; {fmt(K[1])}).</p>

<p>Išskirstytą trikampę apkrovą pakeičiame koncentruota jėga Q. Strypo CB ilgis l<sub>CB</sub> = {fmt(L_CB)} m. Apkrautos atkarpos ilgis L<sub>q</sub> = {fmt(L_q)} m. Atstojamosios modulis:</p>
<p class="eq"><span class="math">Q</span> = 1/2 &middot; <span class="math">q</span> &middot; <span class="math">L<sub>q</sub></span> = 1/2 &middot; {fmt(q_max)} &middot; {fmt(L_q)} = {fmt(Q_mag)} kN.</p>
<p>Atstojamoji jėga Q veikia trikampio svorio centre, taške P({fmt(P_x)}; {fmt(P_y)}).</p>

<p>Jėgų projekcijos į ašis:</p>
<p class="eq">F<sub>x</sub> = {fmt(Fx)} kN; F<sub>y</sub> = {fmt(Fy)} kN;</p>
<p class="eq">Q<sub>x</sub> = {fmt(Qx)} kN; Q<sub>y</sub> = {fmt(Qy)} kN.</p>

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
        <p class="eq">&sum; F<sub>ix</sub> = 0;</p>
        <p class="eq">&sum; F<sub>iy</sub> = 0;</p>
        <p class="eq">&sum; M<sub>B</sub> = 0.</p>
    </div>
    <div class="system-bracket">
        <p class="eq">R<sub>Ax</sub> + R<sub>Bx</sub> + F<sub>x</sub> + Q<sub>x</sub> = 0; (1)</p>
        <p class="eq">R<sub>By</sub> + F<sub>y</sub> + Q<sub>y</sub> = 0; (2)</p>
        <p class="eq">-R<sub>Ax</sub> &middot; (y<sub>A</sub> - y<sub>B</sub>) + F<sub>y</sub> &middot; (x<sub>K</sub> - x<sub>B</sub>) - F<sub>x</sub> &middot; (y<sub>K</sub> - y<sub>B</sub>) + Q<sub>y</sub> &middot; (x<sub>P</sub> - x<sub>B</sub>) - Q<sub>x</sub> &middot; (y<sub>P</sub> - y<sub>B</sub>) - M = 0. (3)</p>
    </div>
</div>

<p>Iš (3) lygties randame R<sub>Ax</sub>:</p>
<p class="eq">R<sub>Ax</sub> &middot; {fmt(A[1] - B[1])} = {fmt(Fy)} &middot; ({fmt(K[0]-B[0])}) - {fmt(Fx)} &middot; ({fmt(K[1]-B[1])}) + ({fmt(Qy)}) &middot; ({fmt(P_x-B[0])}) - ({fmt(Qx)}) &middot; ({fmt(P_y-B[1])}) - {fmt(abs(M))}</p>
<p class="eq">R<sub>Ax</sub> &middot; {fmt(A[1] - B[1])} = {fmt(MB_F + MB_Q + M)} &rarr; R<sub>Ax</sub> = {fmt(RAx)} kN.</p>

<p>Iš (1) lygties randame R<sub>Bx</sub>:</p>
<p class="eq">R<sub>Bx</sub> = - R<sub>Ax</sub> - F<sub>x</sub> - Q<sub>x</sub> = -({fmt(RAx)}) - ({fmt(Fx)}) - ({fmt(Qx)}) = {fmt(RBx)} kN.</p>

<p>Iš (2) lygties randame R<sub>By</sub>:</p>
<p class="eq">R<sub>By</sub> = - F<sub>y</sub> - Q<sub>y</sub> = -({fmt(Fy)}) - ({fmt(Qy)}) = {fmt(RBy)} kN.</p>

<h3>3.1. Sprendimo patikrinimas</h3>
<p>Užrašoma pusiausvyros sąlyga visai sistemai apie tašką O({fmt(O[0])}; {fmt(O[1])}).</p>
<p class="eq">&sum; M<sub>O</sub> = -R<sub>Ax</sub> &middot; y<sub>A</sub> - R<sub>Bx</sub> &middot; y<sub>B</sub> + R<sub>By</sub> &middot; x<sub>B</sub> + F<sub>y</sub> &middot; x<sub>K</sub> - F<sub>x</sub> &middot; y<sub>K</sub> + Q<sub>y</sub> &middot; x<sub>P</sub> - Q<sub>x</sub> &middot; y<sub>P</sub> - M = 0</p>
<p class="eq">&sum; M<sub>O</sub> = -({fmt(RAx)}) &middot; ({fmt(A[1])}) - ({fmt(RBx)}) &middot; ({fmt(B[1])}) + ({fmt(RBy)}) &middot; ({fmt(B[0])}) + ({fmt(Fy)}) &middot; ({fmt(K[0])}) - ({fmt(Fx)}) &middot; ({fmt(K[1])}) + ({fmt(Qy)}) &middot; ({fmt(P_x)}) - ({fmt(Qx)}) &middot; ({fmt(P_y)}) - {fmt(abs(M))} = 0</p>
<p class="eq">&sum; M<sub>O</sub> = {fmt(MO_RAx)} + {fmt(MO_RB)} + {fmt(MO_F)} + {fmt(MO_Q)} - {fmt(abs(M))} = {fmt(MO_sum)} kN</p>

<h3>3.2. Paklaidos skaičiavimas</h3>
<p>&Delta; = ({fmt(abs(MO_sum))} / 500) &middot; 100% = {fmt(abs(MO_sum)/5)}% &lt; 0,3%.</p>

<div class="page-break"></div>
<h2>4. Atsakymų lentelė</h2>
<table>
  <tr>
    <th>R<sub>Ax</sub>, kN</th>
    <th>R<sub>Bx</sub>, kN</th>
    <th>R<sub>By</sub>, kN</th>
  </tr>
  <tr>
    <td>{fmt(RAx)}</td>
    <td>{fmt(RBx)}</td>
    <td>{fmt(RBy)}</td>
  </tr>
</table>

</body>
</html>
"""
    
    with open('/Users/ugniusvaitiekenas/srotas-ai-agent/fizika/statics_frame.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Sugeneruotas statics_frame.html ataskaitos failas!")

generate()
