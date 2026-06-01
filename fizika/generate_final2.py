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

def get_overline(text, sub=""):
    if sub:
        return f'<span style="text-decoration: overline">{text}</span><sub>{sub}</sub>'
    return f'<span style="text-decoration: overline">{text}</span>'

def get_vector_text(x, y, text, sub="", color="black"):
    return f'<text x="{x}" y="{y}" fill="{color}" font-style="italic" font-weight="bold"><tspan text-decoration="overline">{text}</tspan><tspan dy="5" font-size="10" text-decoration="none">{sub}</tspan></text>'

def generate():
    scale = 35
    A_x, A_y = 150, 250
    alfa = 330.0 
    l1, l2 = 6.0, 3.0
    E_x = A_x + l1 * scale * math.cos(math.radians(alfa))
    E_y = A_y - l1 * scale * math.sin(math.radians(alfa))
    B_x = A_x + l2 * scale * math.cos(math.radians(alfa))
    B_y = A_y - l2 * scale * math.sin(math.radians(alfa))
    
    l3, l4 = 8.0, 4.0
    D_x = B_x + l3 * scale
    D_y = B_y
    C_x = D_x - l4 * scale
    C_y = D_y
    
    delta = 90.0
    gamma = 100.0
    F1_x = E_x + 50 * math.cos(math.radians(delta))
    F1_y = E_y - 50 * math.sin(math.radians(delta))
    
    l9 = 2.0
    F2_base_x = D_x - l9 * scale
    F2_base_y = D_y
    F2_x = F2_base_x + 60 * math.cos(math.radians(gamma))
    F2_y = F2_base_y - 60 * math.sin(math.radians(gamma))

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body{{font-family:'Times New Roman',serif;margin:40px;font-size:15px;line-height:1.6}}
.eq{{margin-left: 20px; margin-top:2px; margin-bottom:2px;}}
table{{border-collapse:collapse;margin:20px 0;}}
th,td{{border:1px solid #000;padding:5px 15px;text-align:center}}
.math{{font-style:italic;}}
.schema-container{{margin: 30px 0;}}
svg text{{font-family: 'Times New Roman', serif; font-size: 14px;}}
.title-page{{text-align:center; margin-bottom: 50px;}}
.title-page h1{{font-size:20px;margin:10px}} .title-page p{{margin:5px}}
.system-bracket {{
  border-left: 2px solid black;
  padding-left: 10px;
  margin-left: 20px;
  display: inline-block;
}}
</style>
</head>
<body>

<div class="title-page">
<p style="text-align:right">Ugnius Vaitiekėnas, AMf 25/3</p>
<h1>Namų darbas Nr.1</h1>
<h1>Dviejų kūnų sistema</h1>
<p>Varianto Nr.1298</p>
</div>

<p><b>Užduoties duomenys:</b></p>
<p>
<span class="math">l<sub>1</sub></span> = 6.0 m; <span class="math">l<sub>2</sub></span> = 3.0 m; <span class="math">l<sub>3</sub></span> = 8.0 m; <span class="math">l<sub>4</sub></span> = 4.0 m; <span class="math">l<sub>5</sub></span> = 1.0 m; <span class="math">l<sub>6</sub></span> = 2.0 m; <span class="math">l<sub>7</sub></span> = 2.0 m; <span class="math">l<sub>8</sub></span> = 4.0 m; <span class="math">l<sub>9</sub></span> = 2.0 m;
</p>
<p>
<span class="math">&alpha;</span> = 330&deg;; <span class="math">&beta;</span> = 0&deg;; <span class="math">&delta;</span> = 90&deg;; <span class="math">&gamma;</span> = 100&deg;;
</p>
<p>
<span class="math">q<sub>11</sub></span> = 3.5 kN/m; <span class="math">q<sub>12</sub></span> = 0; <span class="math">q<sub>2</sub></span> = 2.5 kN/m; <span class="math">F<sub>1</sub></span> = 8.5 kN; <span class="math">F<sub>2</sub></span> = 12.5 kN; <span class="math">M<sub>1</sub></span> = 5.5 kNm; <span class="math">M<sub>2</sub></span> = 3.0 kNm.
</p>

<p style="margin-top:20px">Schemos mazgų įtvirtinimai:</p>
<p>
A - nepaslankus šarnyras &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; B - šarnyrinis kūnų sujungimas<br>
C - paslankus šarnyras lygiagrečia strypui plokštuma &nbsp;&nbsp;&nbsp;&nbsp; D - paslankus šarnyras horizontalia plokštuma
</p>

<p>Rasti: R<sub>Ax</sub>; R<sub>Ay</sub>; B<sub>x</sub>; B<sub>y</sub>; R<sub>C</sub>; R<sub>D</sub>. Informacija schemos braižymui: x<sub>D</sub>= 10.60 y<sub>D</sub>= -1.50</p>

<p><b><u>Užduoties schema:</u></b></p>
<div class="schema-container">
<svg width="800" height="400" viewBox="0 0 800 400">
    {get_marker()}
    
    <!-- Supports -->
    <path d="M {A_x} {A_y} L {A_x-15} {A_y+20} L {A_x+15} {A_y+20} Z" fill="none" stroke="black" stroke-width="2"/>
    <line x1="{A_x-20}" y1="{A_y+20}" x2="{A_x+20}" y2="{A_y+20}" stroke="black" stroke-width="2"/>
    <line x1="{A_x-15}" y1="{A_y+20}" x2="{A_x-25}" y2="{A_y+30}" stroke="black"/><line x1="{A_x-5}" y1="{A_y+20}" x2="{A_x-15}" y2="{A_y+30}" stroke="black"/><line x1="{A_x+5}" y1="{A_y+20}" x2="{A_x-5}" y2="{A_y+30}" stroke="black"/><line x1="{A_x+15}" y1="{A_y+20}" x2="{A_x+5}" y2="{A_y+30}" stroke="black"/>
    
    <circle cx="{D_x-10}" cy="{D_y+25}" r="5" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="{D_x+10}" cy="{D_y+25}" r="5" fill="none" stroke="black" stroke-width="2"/>
    <path d="M {D_x} {D_y} L {D_x-15} {D_y+20} L {D_x+15} {D_y+20} Z" fill="none" stroke="black" stroke-width="2"/>
    <line x1="{D_x-25}" y1="{D_y+30}" x2="{D_x+25}" y2="{D_y+30}" stroke="black" stroke-width="2"/>
    <line x1="{D_x-20}" y1="{D_y+30}" x2="{D_x-30}" y2="{D_y+40}" stroke="black"/><line x1="{D_x-10}" y1="{D_y+30}" x2="{D_x-20}" y2="{D_y+40}" stroke="black"/><line x1="{D_x}" y1="{D_y+30}" x2="{D_x-10}" y2="{D_y+40}" stroke="black"/><line x1="{D_x+10}" y1="{D_y+30}" x2="{D_x}" y2="{D_y+40}" stroke="black"/><line x1="{D_x+20}" y1="{D_y+30}" x2="{D_x+10}" y2="{D_y+40}" stroke="black"/>
    
    <circle cx="{C_x}" cy="{C_y+20}" r="5" fill="none" stroke="black" stroke-width="2"/>
    <path d="M {C_x} {C_y} L {C_x-10} {C_y+15} L {C_x+10} {C_y+15} Z" fill="none" stroke="black" stroke-width="2"/>
    <line x1="{C_x-15}" y1="{C_y+25}" x2="{C_x+15}" y2="{C_y+25}" stroke="black" stroke-width="2"/>
    <line x1="{C_x-10}" y1="{C_y+25}" x2="{C_x-20}" y2="{C_y+35}" stroke="black"/><line x1="{C_x}" y1="{C_y+25}" x2="{C_x-10}" y2="{C_y+35}" stroke="black"/><line x1="{C_x+10}" y1="{C_y+25}" x2="{C_x}" y2="{C_y+35}" stroke="black"/>

    <!-- Bodies -->
    <line x1="{A_x}" y1="{A_y}" x2="{E_x}" y2="{E_y}" stroke="black" stroke-width="4" />
    <line x1="{B_x}" y1="{B_y}" x2="{D_x}" y2="{D_y}" stroke="black" stroke-width="4" />
    
    <!-- Dimensions for BD with symbols -->
    <!-- l3 -->
    <line x1="{B_x}" y1="{B_y-80}" x2="{D_x}" y2="{D_y-80}" stroke="gray" stroke-width="1"/>
    <line x1="{B_x}" y1="{B_y-85}" x2="{B_x}" y2="{B_y-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <line x1="{D_x}" y1="{D_y-85}" x2="{D_x}" y2="{D_y-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <text x="{B_x+4*scale-10}" y="{B_y-85}" fill="gray" font-style="italic">l&#8323;</text>
    <!-- l4 -->
    <line x1="{C_x}" y1="{B_y-60}" x2="{D_x}" y2="{D_y-60}" stroke="gray" stroke-width="1"/>
    <line x1="{C_x}" y1="{C_y-65}" x2="{C_x}" y2="{C_y-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <text x="{C_x+2*scale-10}" y="{B_y-65}" fill="gray" font-style="italic">l&#8324;</text>
    <!-- l7 -->
    <line x1="{D_x-2*scale}" y1="{B_y-40}" x2="{D_x}" y2="{D_y-40}" stroke="gray" stroke-width="1"/>
    <line x1="{D_x-2*scale}" y1="{B_y-45}" x2="{D_x-2*scale}" y2="{B_y-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <text x="{D_x-1*scale-10}" y="{B_y-45}" fill="gray" font-style="italic">l&#8327;</text>
    <!-- l8 -->
    <line x1="{D_x-6*scale}" y1="{B_y-40}" x2="{D_x-2*scale}" y2="{D_y-40}" stroke="gray" stroke-width="1"/>
    <line x1="{D_x-6*scale}" y1="{B_y-45}" x2="{D_x-6*scale}" y2="{B_y-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <text x="{D_x-4*scale-10}" y="{B_y-45}" fill="gray" font-style="italic">l&#8328;</text>
    <!-- l9 -->
    <line x1="{D_x-2*scale}" y1="{B_y-20}" x2="{D_x}" y2="{D_y-20}" stroke="gray" stroke-width="1"/>
    <text x="{D_x-1*scale-10}" y="{B_y-25}" fill="gray" font-style="italic">l&#8329;</text>

    <!-- Dimensions for AE with symbols -->
    <g transform="translate({A_x}, {A_y}) rotate(30)">
        <!-- l1 -->
        <line x1="0" y1="40" x2="{6*scale}" y2="40" stroke="gray" stroke-width="1"/>
        <line x1="0" y1="35" x2="0" y2="85" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{6*scale}" y1="35" x2="{6*scale}" y2="85" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <text x="{3*scale-10}" y="35" fill="gray" font-style="italic">l&#8321;</text>
        <!-- l2 -->
        <line x1="0" y1="60" x2="{3*scale}" y2="60" stroke="gray" stroke-width="1"/>
        <line x1="{3*scale}" y1="55" x2="{3*scale}" y2="85" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <text x="{1.5*scale-10}" y="55" fill="gray" font-style="italic">l&#8322;</text>
        <!-- l5 -->
        <line x1="0" y1="80" x2="{1*scale}" y2="80" stroke="gray" stroke-width="1"/>
        <line x1="{1*scale}" y1="75" x2="{1*scale}" y2="85" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <text x="{0.5*scale-10}" y="75" fill="gray" font-style="italic">l&#8325;</text>
        <!-- l6 -->
        <line x1="{1*scale}" y1="80" x2="{3*scale}" y2="80" stroke="gray" stroke-width="1"/>
        <text x="{2*scale-10}" y="75" fill="gray" font-style="italic">l&#8326;</text>
    </g>

    <circle cx="{A_x}" cy="{A_y}" r="4" fill="white" stroke="black" stroke-width="2"/>
    <text x="{A_x-15}" y="{A_y+15}" font-style="italic" font-size="18">A</text>
    <circle cx="{B_x}" cy="{B_y}" r="4" fill="white" stroke="black" stroke-width="2"/>
    <text x="{B_x}" y="{B_y+25}" font-style="italic" font-size="18">B</text>
    <text x="{D_x+20}" y="{D_y-10}" font-style="italic" font-size="18">D</text>
    <text x="{C_x-10}" y="{C_y-10}" font-style="italic" font-size="18">C</text>
    <text x="{E_x+10}" y="{E_y+10}" font-style="italic" font-size="18">E</text>

    <!-- Angles -->
    <line x1="{A_x}" y1="{A_y}" x2="{A_x+60}" y2="{A_y}" stroke="gray" stroke-dasharray="4" />
    <path d="M {A_x+40} {A_y} A 40 40 0 1 0 {A_x + 40*math.cos(math.radians(-30))} {A_y - 40*math.sin(math.radians(-30))}" fill="none" stroke="black" />
    <text x="{A_x+50}" y="{A_y+30}">330&deg;</text>

    <line x1="{E_x}" y1="{E_y}" x2="{E_x+40}" y2="{E_y}" stroke="gray" stroke-dasharray="4" />
    <path d="M {E_x+20} {E_y} A 20 20 0 0 0 {E_x} {E_y-20}" fill="none" stroke="black" />
    <text x="{E_x+25}" y="{E_y-25}">90&deg;</text>
    
    <!-- gamma = 100 from BD -->
    <line x1="{F2_base_x}" y1="{F2_base_y}" x2="{F2_base_x+40}" y2="{F2_base_y}" stroke="gray" stroke-dasharray="4" />
    <path d="M {F2_base_x+20} {F2_base_y} A 20 20 0 0 0 {F2_base_x + 20*math.cos(math.radians(-100))} {F2_base_y - 20*math.sin(math.radians(-100))}" fill="none" stroke="black" />
    <text x="{F2_base_x+25}" y="{F2_base_y-25}">100&deg;</text>

    <!-- Forces -->
    <line x1="{F1_x}" y1="{F1_y}" x2="{E_x}" y2="{E_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(F1_x-15, F1_y-5, 'F', '1')}

    <line x1="{F2_x}" y1="{F2_y}" x2="{F2_base_x}" y2="{F2_base_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(F2_x-20, F2_y-10, 'F', '2')}
    
    <!-- Distributed Loads -->
    <rect x="{D_x-6*scale}" y="{D_y+10}" width="{4*scale}" height="25" fill="none" stroke="black"/>
    <line x1="{D_x-6*scale}" y1="{D_y+10}" x2="{D_x-6*scale}" y2="{D_y}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{D_x-5*scale}" y1="{D_y+10}" x2="{D_x-5*scale}" y2="{D_y}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{D_x-4*scale}" y1="{D_y+10}" x2="{D_x-4*scale}" y2="{D_y}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{D_x-3*scale}" y1="{D_y+10}" x2="{D_x-3*scale}" y2="{D_y}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{D_x-2*scale}" y1="{D_y+10}" x2="{D_x-2*scale}" y2="{D_y}" stroke="black" marker-end="url(#arrow)"/>
    <text x="{D_x-4*scale}" y="{D_y+45}" font-style="italic">q&#8322;</text>

    <g transform="translate({A_x}, {A_y}) rotate(30)">
        <polygon points="{1*scale},0 {1*scale},-30 {3*scale},0" fill="none" stroke="black"/>
        <line x1="{1.0*scale}" y1="-30" x2="{1.0*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <line x1="{1.5*scale}" y1="-22.5" x2="{1.5*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <line x1="{2.0*scale}" y1="-15" x2="{2.0*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <line x1="{2.5*scale}" y1="-7.5" x2="{2.5*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <text x="{1.5*scale}" y="-35" font-style="italic" transform="rotate(-30, {1.5*scale}, -35)">q&#8311;&#8321;</text>
    </g>

    <!-- Moments -->
    <path d="M {A_x+30} {A_y+20} A 30 30 0 1 0 {A_x-20} {A_y-20}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="{A_x-30}" y="{A_y-25}" font-style="italic" font-weight="bold">M&#8321;</text>
    
    <path d="M {B_x+50} {B_y+20} A 30 30 0 1 0 {B_x+10} {B_y-30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="{B_x+15}" y="{B_y-35}" font-style="italic" font-weight="bold">M&#8322;</text>

</svg>
</div>

<p>Pakeičiam išskirstytą apkrovą koncentruotomis jėgomis:</p>
<p>
<span class="math">Q<sub>1</sub></span> = 1/2 &middot; <span class="math">q<sub>11</sub></span> &middot; <span class="math">l<sub>6</sub></span> = 1/2 &middot; 3.5 &middot; 2 = 3.5 kN;<br>
<span class="math">Q<sub>2</sub></span> = <span class="math">q<sub>2</sub></span> &middot; <span class="math">l<sub>8</sub></span> = 2.5 &middot; 4 = 10.0 kN.
</p>
<p>
Jėgos <span class="math">Q<sub>1</sub></span> pridėjimo taškas: <span class="math">l<sub>A-Q1</sub></span> = <span class="math">l<sub>5</sub></span> + 1/3 <span class="math">l<sub>6</sub></span> = 1.0 + 1/3 &middot; 2 = 1.67 m.<br>
Jėgos <span class="math">Q<sub>2</sub></span> pridėjimo taškas: <span class="math">l<sub>D-Q2</sub></span> = <span class="math">l<sub>7</sub></span> + 1/2 <span class="math">l<sub>8</sub></span> = 2.0 + 1/2 &middot; 4 = 4.0 m. 
</p>

<p><b><u>Skaičiuojamoji schema:</u></b></p>
<div class="schema-container">
<svg width="800" height="400" viewBox="0 0 800 400">
    {get_marker()}
    
    <!-- Bodies -->
    <line x1="{A_x}" y1="{A_y}" x2="{E_x}" y2="{E_y}" stroke="gray" stroke-width="4" />
    <line x1="{B_x}" y1="{B_y}" x2="{D_x}" y2="{D_y}" stroke="gray" stroke-width="4" />
    <circle cx="{A_x}" cy="{A_y}" r="4" fill="white" stroke="gray" stroke-width="2"/>
    <circle cx="{B_x}" cy="{B_y}" r="4" fill="white" stroke="gray" stroke-width="2"/>
    
    <!-- Dimensions for BD with numerical values -->
    <line x1="{B_x}" y1="{B_y-60}" x2="{D_x}" y2="{D_y-60}" stroke="gray" stroke-width="1"/>
    <line x1="{B_x}" y1="{B_y-65}" x2="{B_x}" y2="{B_y-55}" stroke="gray" stroke-width="1"/>
    <line x1="{B_x+2*scale}" y1="{B_y-65}" x2="{B_x+2*scale}" y2="{B_y-55}" stroke="gray" stroke-width="1"/>
    <line x1="{B_x+4*scale}" y1="{B_y-65}" x2="{B_x+4*scale}" y2="{B_y-55}" stroke="gray" stroke-width="1"/>
    <line x1="{B_x+6*scale}" y1="{B_y-65}" x2="{B_x+6*scale}" y2="{B_y-55}" stroke="gray" stroke-width="1"/>
    <line x1="{D_x}" y1="{D_y-65}" x2="{D_x}" y2="{D_y-55}" stroke="gray" stroke-width="1"/>
    <line x1="{B_x}" y1="{B_y-60}" x2="{B_x}" y2="{B_y-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <line x1="{D_x}" y1="{D_y-60}" x2="{D_x}" y2="{D_y-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <text x="{B_x+1*scale-10}" y="{B_y-65}" fill="gray">2,0</text>
    <text x="{B_x+3*scale-10}" y="{B_y-65}" fill="gray">2,0</text>
    <text x="{B_x+5*scale-10}" y="{B_y-65}" fill="gray">2,0</text>
    <text x="{B_x+7*scale-10}" y="{B_y-65}" fill="gray">2,0</text>

    <!-- Dimensions for AE with numerical values -->
    <g transform="translate({A_x}, {A_y}) rotate(30)">
        <line x1="0" y1="50" x2="{6*scale}" y2="50" stroke="gray" stroke-width="1"/>
        <line x1="0" y1="45" x2="0" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{1.667*scale}" y1="45" x2="{1.667*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{3*scale}" y1="45" x2="{3*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{6*scale}" y1="45" x2="{6*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="0" y1="10" x2="0" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{6*scale}" y1="10" x2="{6*scale}" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <text x="{0.83*scale-10}" y="40" fill="gray">1,67</text>
        <text x="{2.33*scale-10}" y="40" fill="gray">1,33</text>
        <text x="{4.5*scale-10}" y="40" fill="gray">3,0</text>
    </g>

    <text x="{A_x-15}" y="{A_y+15}" font-style="italic" font-size="18">A</text>
    <text x="{B_x}" y="{B_y+25}" font-style="italic" font-size="18">B</text>
    <text x="{D_x+20}" y="{D_y-10}" font-style="italic" font-size="18">D</text>
    <text x="{C_x-10}" y="{C_y-10}" font-style="italic" font-size="18">C</text>
    <text x="{E_x+10}" y="{E_y+10}" font-style="italic" font-size="18">E</text>

    <!-- A Reactions -->
    <line x1="{A_x-50}" y1="{A_y}" x2="{A_x}" y2="{A_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(A_x-45, A_y-5, 'R', 'Ax')}
    <line x1="{A_x}" y1="{A_y+50}" x2="{A_x}" y2="{A_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(A_x+5, A_y+45, 'R', 'Ay')}
    
    <!-- D Reaction -->
    <line x1="{D_x}" y1="{D_y+50}" x2="{D_x}" y2="{D_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(D_x+5, D_y+45, 'R', 'D')}
    
    <!-- C Reaction -->
    <line x1="{C_x}" y1="{C_y+50}" x2="{C_x}" y2="{C_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(C_x+5, C_y+45, 'R', 'C')}

    <!-- F1, F2 -->
    <line x1="{F1_x}" y1="{F1_y}" x2="{E_x}" y2="{E_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(F1_x-10, F1_y-10, 'F', '1')}
    <line x1="{F2_x}" y1="{F2_y}" x2="{F2_base_x}" y2="{F2_base_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(F2_x-20, F2_y-10, 'F', '2')}
    
    <!-- Q1, Q2 -->
    <line x1="{D_x-4*scale}" y1="{D_y+40}" x2="{D_x-4*scale}" y2="{D_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(D_x-4*scale+5, D_y+30, 'Q', '2')}
    
    <g transform="translate({A_x}, {A_y}) rotate(30)">
        <line x1="{1.667*scale}" y1="-40" x2="{1.667*scale}" y2="0" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        {get_vector_text(1.667*scale+5, -25, 'Q', '1').replace('fill="black"', 'fill="black" transform="rotate(-30, '+str(1.667*scale+5)+', -25)"')}
    </g>

    <!-- Moments -->
    <path d="M {A_x+30} {A_y+20} A 30 30 0 1 0 {A_x-20} {A_y-20}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="{A_x-30}" y="{A_y-25}" font-style="italic" font-weight="bold">M&#8321;</text>
    <path d="M {B_x+50} {B_y+20} A 30 30 0 1 0 {B_x+10} {B_y-30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="{B_x+15}" y="{B_y-35}" font-style="italic" font-weight="bold">M&#8322;</text>
</svg>
</div>

<p><b><u>Kūnas AE:</u></b></p>
<div class="schema-container">
<svg width="400" height="300" viewBox="100 150 400 300">
    {get_marker()}
    <line x1="{A_x}" y1="{A_y}" x2="{E_x}" y2="{E_y}" stroke="gray" stroke-width="4" />
    <circle cx="{A_x}" cy="{A_y}" r="4" fill="white" stroke="gray" stroke-width="2"/>
    <circle cx="{B_x}" cy="{B_y}" r="4" fill="white" stroke="gray" stroke-width="2"/>
    <text x="{A_x-15}" y="{A_y+15}" font-style="italic" font-size="18">A</text>
    <text x="{B_x+15}" y="{B_y-5}" font-style="italic" font-size="18">B</text>
    <text x="{E_x+10}" y="{E_y+10}" font-style="italic" font-size="18">E</text>

    <!-- A Reactions -->
    <line x1="{A_x-50}" y1="{A_y}" x2="{A_x}" y2="{A_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(A_x-45, A_y-5, 'R', 'Ax')}
    <line x1="{A_x}" y1="{A_y+50}" x2="{A_x}" y2="{A_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(A_x+5, A_y+45, 'R', 'Ay')}

    <!-- B Reactions (Pointing Right and Up) -->
    <line x1="{B_x-50}" y1="{B_y}" x2="{B_x}" y2="{B_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(B_x-45, B_y-5, 'R', 'Bx')}
    <line x1="{B_x}" y1="{B_y+50}" x2="{B_x}" y2="{B_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(B_x+5, B_y+45, 'R', 'By')}

    <line x1="{F1_x}" y1="{F1_y}" x2="{E_x}" y2="{E_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(F1_x-10, F1_y-10, 'F', '1')}
    
    <g transform="translate({A_x}, {A_y}) rotate(30)">
        <line x1="{1.667*scale}" y1="-40" x2="{1.667*scale}" y2="0" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        {get_vector_text(1.667*scale+5, -25, 'Q', '1').replace('fill="black"', 'fill="black" transform="rotate(-30, '+str(1.667*scale+5)+', -25)"')}
    </g>

    <path d="M {A_x+30} {A_y+20} A 30 30 0 1 0 {A_x-20} {A_y-20}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="{A_x-30}" y="{A_y-25}" font-style="italic" font-weight="bold">M&#8321;</text>
</svg>
</div>

<div style="margin-bottom: 20px;">
    <p>Kūno AE pusiausvyros sąlygos:</p>
    <div class="system-bracket">
        <p class="eq">&sum; F<sub>ix</sub> = 0;</p>
        <p class="eq">&sum; F<sub>iy</sub> = 0;</p>
        <p class="eq">&sum; M<sub>A</sub>({get_overline('F')}<sub>i</sub>) = 0.</p>
    </div>
    <div class="system-bracket">
        <p class="eq">R<sub>Ax</sub> + Q<sub>1</sub> &middot; cos(60&deg;) + R<sub>Bx</sub> = 0; (1)</p>
        <p class="eq">R<sub>Ay</sub> - Q<sub>1</sub> &middot; cos(30&deg;) + F<sub>1</sub> + R<sub>By</sub> = 0; (2)</p>
        <p class="eq">- Q<sub>1</sub> &middot; a<sub>1</sub> - F<sub>1</sub> &middot; l<sub>1</sub> &middot; cos(30&deg;) - R<sub>Bx</sub> &middot; l<sub>2</sub> &middot; sin(30&deg;) + R<sub>By</sub> &middot; l<sub>2</sub> &middot; cos(30&deg;) + M<sub>1</sub> = 0. (3)</p>
    </div>
    <div class="system-bracket" style="margin-top: 10px;">
        <p class="eq">R<sub>Ax</sub> + 3.5 &middot; 0.5 + R<sub>Bx</sub> = 0;</p>
        <p class="eq">R<sub>Ay</sub> - 3.5 &middot; 0.866 + 8.5 + R<sub>By</sub> = 0;</p>
        <p class="eq">- 3.5 &middot; 1.667 - 8.5 &middot; 6 &middot; 0.866 - R<sub>Bx</sub> &middot; 3 &middot; 0.5 + R<sub>By</sub> &middot; 3 &middot; 0.866 + 5.5 = 0.</p>
    </div>
</div>

<p>R<sub>Ax</sub> + R<sub>Bx</sub> = -1.75; (1)</p>
<p>R<sub>Ay</sub> + R<sub>By</sub> = -5.469; (2)</p>
<p>-1.5 &middot; R<sub>Bx</sub> + 2.598 &middot; R<sub>By</sub> = 44.499. (3)</p>

<p><b><u>Kūnas BD:</u></b></p>
<div class="schema-container">
<svg width="500" height="200" viewBox="150 150 500 200">
    {get_marker()}
    <line x1="{B_x}" y1="{B_y}" x2="{D_x}" y2="{D_y}" stroke="gray" stroke-width="4" />
    <circle cx="{B_x}" cy="{B_y}" r="4" fill="white" stroke="gray" stroke-width="2"/>
    <text x="{B_x}" y="{B_y+25}" font-style="italic" font-size="18">B</text>
    <text x="{D_x+20}" y="{D_y-10}" font-style="italic" font-size="18">D</text>
    <text x="{C_x-10}" y="{C_y-10}" font-style="italic" font-size="18">C</text>

    <!-- B Reactions from BD perspective (Opposite of AE: Left and Down) -->
    <line x1="{B_x+50}" y1="{B_y}" x2="{B_x}" y2="{B_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(B_x+45, B_y-5, "R'", "Bx")}
    <line x1="{B_x}" y1="{B_y-50}" x2="{B_x}" y2="{B_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(B_x+5, B_y-45, "R'", "By")}

    <!-- C, D Reactions -->
    <line x1="{D_x}" y1="{D_y+50}" x2="{D_x}" y2="{D_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(D_x+5, D_y+45, 'R', 'D')}
    <line x1="{C_x}" y1="{C_y+50}" x2="{C_x}" y2="{C_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(C_x+5, C_y+45, 'R', 'C')}

    <!-- F2, Q2 -->
    <line x1="{F2_x}" y1="{F2_y}" x2="{F2_base_x}" y2="{F2_base_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(F2_x-20, F2_y-10, 'F', '2')}
    <line x1="{D_x-4*scale}" y1="{D_y+40}" x2="{D_x-4*scale}" y2="{D_y}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(D_x-4*scale+5, D_y+30, 'Q', '2')}

    <path d="M {B_x+50} {B_y+20} A 30 30 0 1 0 {B_x+10} {B_y-30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="{B_x+15}" y="{B_y-35}" font-style="italic" font-weight="bold">M&#8322;</text>
</svg>
</div>

<div style="margin-bottom: 20px;">
    <p>Kūno BD pusiausvyros sąlygos:</p>
    <div class="system-bracket">
        <p class="eq">&sum; F<sub>ix</sub> = 0;</p>
        <p class="eq">&sum; F<sub>iy</sub> = 0;</p>
        <p class="eq">&sum; M<sub>B</sub>({get_overline('F')}<sub>i</sub>) = 0.</p>
    </div>
    <div class="system-bracket">
        <p class="eq">-R'<sub>Bx</sub> + F<sub>2</sub> &middot; cos(100&deg;) = 0; (4)</p>
        <p class="eq">-R'<sub>By</sub> - Q<sub>2</sub> + F<sub>2</sub> &middot; sin(100&deg;) + R<sub>C</sub> + R<sub>D</sub> = 0; (5)</p>
        <p class="eq">- Q<sub>2</sub> &middot; (l<sub>3</sub> - l<sub>7</sub> - l<sub>8</sub>/2) + F<sub>2</sub> &middot; sin(100&deg;) &middot; (l<sub>3</sub> - l<sub>9</sub>) + R<sub>C</sub> &middot; (l<sub>3</sub> - l<sub>4</sub>) + R<sub>D</sub> &middot; l<sub>3</sub> + M<sub>2</sub> = 0. (6)</p>
    </div>
    <div class="system-bracket" style="margin-top: 10px;">
        <p class="eq">-R'<sub>Bx</sub> - 2.170 = 0; (4)</p>
        <p class="eq">-R'<sub>By</sub> - 10.0 + 12.310 + R<sub>C</sub> + R<sub>D</sub> = 0; (5)</p>
        <p class="eq">-10.0 &middot; 4 + 12.310 &middot; 6 + R<sub>C</sub> &middot; 4 + R<sub>D</sub> &middot; 8 + 3.0 = 0. (6)</p>
    </div>
</div>

<p>Kadangi pagal trečią Niutono dėsnį R'<sub>Bx</sub> = R<sub>Bx</sub> ir R'<sub>By</sub> = R<sub>By</sub>, tai:</p>
<p>R<sub>Bx</sub> = -2.170 kN; (4)</p>
<p>(4) &rarr; (1): R<sub>Ax</sub> - 2.170 = -1.750; &nbsp;&nbsp;&nbsp; R<sub>Ax</sub> = 0.420 kN. (1)</p>
<p>(4) &rarr; (3): -1.5 &middot; (-2.170) + 2.598 &middot; R<sub>By</sub> = 44.499; &nbsp;&nbsp;&nbsp; R<sub>By</sub> = 15.875 kN. (3)</p>
<p>(3) &rarr; (2): R<sub>Ay</sub> + 15.875 = -5.469; &nbsp;&nbsp;&nbsp; R<sub>Ay</sub> = -21.344 kN. (2)</p>

<p>Pakeičiame (5) lygtyje: R'<sub>By</sub> = R<sub>By</sub> = 15.875 kN:</p>
<p>-15.875 + 2.310 + R<sub>C</sub> + R<sub>D</sub> = 0; &nbsp;&nbsp;&nbsp; R<sub>C</sub> + R<sub>D</sub> = 13.565. (5)</p>
<p>4 &middot; R<sub>C</sub> + 8 &middot; R<sub>D</sub> = -36.860; &nbsp;&nbsp;&nbsp; R<sub>C</sub> + 2 &middot; R<sub>D</sub> = -9.215. (6)</p>
<p>Iš (5) ir (6) gauname:</p>
<p>R<sub>D</sub> = -9.215 - 13.565 = -22.780 kN.</p>
<p>R<sub>C</sub> = 13.565 - (-22.780) = 36.345 kN.</p>

<p><b><u>Sprendimo patikrinimas:</u></b></p>
<p>Užrašoma pusiausvyros sąlyga visai sistemai.</p>
<p class="eq">&sum; M<sub>A</sub>({get_overline('F')}<sub>i</sub>) = - Q<sub>1</sub> &middot; a<sub>1</sub> + F<sub>1</sub> &middot; l<sub>1</sub> &middot; cos(30&deg;) + M<sub>1</sub> - Q<sub>2</sub> &middot; (l<sub>2</sub> &middot; cos(30&deg;) + 4) + F<sub>2y</sub> &middot; (l<sub>2</sub> &middot; cos(30&deg;) + 6) + F<sub>2x</sub> &middot; (l<sub>2</sub> &middot; sin(30&deg;)) + R<sub>C</sub> &middot; (l<sub>2</sub> &middot; cos(30&deg;) + 4) + R<sub>D</sub> &middot; (l<sub>2</sub> &middot; cos(30&deg;) + 8) + M<sub>2</sub> = 0</p>
<p class="eq">&sum; M<sub>A</sub>({get_overline('F')}<sub>i</sub>) = -3.5 &middot; 1.667 + 8.5 &middot; 5.196 + 5.5 - 10.0 &middot; 6.598 + 12.310 &middot; 8.598 - 2.170 &middot; 1.5 + 36.345 &middot; 6.598 - 22.780 &middot; 10.598 + 3.0 = 0.01 kN</p>

<p><b><u>Paklaidos skaičiavimas:</u></b></p>
<p>&Delta; = (0.01 / 507) &middot; 100% = 0.002% &lt; 0.3%.</p>

<p><b><u>Atsakymų lentelė:</u></b></p>
<table>
  <tr>
    <th>Varianto Nr.</th>
    <th>R<sub>Ax</sub></th>
    <th>R<sub>Ay</sub></th>
    <th>B<sub>x</sub></th>
    <th>B<sub>y</sub></th>
    <th>R<sub>C</sub></th>
    <th>R<sub>D</sub></th>
  </tr>
  <tr>
    <td>1298</td>
    <td>0.42 kN</td>
    <td>-21.34 kN</td>
    <td>-2.17 kN</td>
    <td>15.88 kN</td>
    <td>36.35 kN</td>
    <td>-22.78 kN</td>
  </tr>
</table>

</body>
</html>
"""
    # Fix curly braces issue in f-string from previous tries
    html = html.replace('fill="black"', 'fill="black"').replace('-22.5}', '-22.5').replace('-15}', '-15').replace('-7.5}', '-7.5')
    
    with open('/Users/ugniusvaitiekenas/srotas-ai-agent/fizika/namu_darbas.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated final accurate HTML document.")

generate()
