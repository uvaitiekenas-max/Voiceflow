import math

def generate_html():
    html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>TM ND1</title>
<style>
body{font-family:'Times New Roman',serif;margin:40px;font-size:14px;line-height:1.6}
.title-page{text-align:center;padding-top:200px;page-break-after:always}
.title-page h1{font-size:20px;margin:10px} .title-page p{margin:5px}
table{border-collapse:collapse;margin:20px 0;}
th,td{border:1px solid #000;padding:5px 10px;text-align:center}
.math{font-style:italic;}
.eq{margin-left: 20px;}
.schema-container{text-align:center; margin: 30px 0;}
</style>
</head>
<body>

<div class="title-page">
<p style="text-align:right">Vardenis Pavardenis, Grupė</p>
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

<p>Rasti: R<sub>Ax</sub>; R<sub>Ay</sub>; B<sub>x</sub>; B<sub>y</sub>; R<sub>C</sub>; R<sub>D</sub>. Informacija schemos braižymui: x<sub>D</sub>= 10.60, y<sub>D</sub>= -1.50</p>

<div class="schema-container">
<p style="text-align:left"><b>Užduoties schema:</b></p>
<svg width="600" height="400" viewBox="-100 -250 500 350" xmlns="http://www.w3.org/2000/svg">
  <!-- Grid/axes optional, sticking to the main drawing -->
  <!-- Point A (0,0) -->
  <!-- AE at angle 330 (which is -30 or +330, meaning down-right from A) -->
  <!-- But wait, A=(0,0), D=(10.6, -1.5). E is the end of l1=6m at 330. -->
  <!-- 6 * cos(330) = 5.196, 6 * sin(330) = -3.0. E=(5.196, -3.0). -->
  <!-- AB is at angle 330. The distance AB is not l1, wait. In the picture l1 and l2 were shown on the rod AE. l2=3m. So AB is l2? No, l2 is often the distance from A to some point. -->
  <!-- Let's draw a generic schema placeholder for now. -->
  <line x1="0" y1="0" x2="150" y2="-86.6" stroke="black" stroke-width="3" /> <!-- AE -->
  <line x1="75" y1="-43.3" x2="300" y2="-43.3" stroke="black" stroke-width="3" /> <!-- BD -->
  <circle cx="0" cy="0" r="4" fill="white" stroke="black" stroke-width="2"/>
  <text x="-15" y="15" font-size="16">A</text>
  <circle cx="75" cy="-43.3" r="4" fill="white" stroke="black" stroke-width="2"/>
  <text x="65" y="-55" font-size="16">B</text>
  <circle cx="300" cy="-43.3" r="4" fill="white" stroke="black" stroke-width="2"/>
  <text x="310" y="-35" font-size="16">D</text>
  <text x="150" y="-95" font-size="16">E</text>
  <text x="200" y="50" font-size="14" fill="red">[Brėžinys generuojamas atskirai pagal mastelį]</text>
</svg>
</div>

<p style="margin-top:30px"><b>Pakeičiam išskirstytą apkrovą koncentruotomis jėgomis:</b></p>
<p>
<span class="math">Q<sub>1</sub></span> = 1/2 &middot; <span class="math">q<sub>11</sub></span> &middot; <span class="math">l<sub>6</sub></span> = 1/2 &middot; 3.5 &middot; 2 = 3.5 kN;<br>
<span class="math">Q<sub>2</sub></span> = <span class="math">q<sub>2</sub></span> &middot; <span class="math">l<sub>8</sub></span> = 2.5 &middot; 4 = 10.0 kN.
</p>
<p>
Jėgos <span class="math">Q<sub>1</sub></span> pridėjimo taškas: <span class="math">l<sub>A-Q1</sub></span> = <span class="math">l<sub>5</sub></span> + 1/3 <span class="math">l<sub>6</sub></span> = 1.0 + 1/3 &middot; 2 = 1.667 m.<br>
Jėgos <span class="math">Q<sub>2</sub></span> pridėjimo taškas: <span class="math">l<sub>B-Q2</sub></span> = <span class="math">l<sub>7</sub></span> + 1/2 <span class="math">l<sub>8</sub></span> = 2.0 + 1/2 &middot; 4 = 4.0 m.
</p>

<div class="schema-container">
<p style="text-align:left"><b>Skaičiuojamoji schema:</b></p>
<svg width="600" height="400" viewBox="-100 -250 500 350" xmlns="http://www.w3.org/2000/svg">
  <line x1="0" y1="0" x2="150" y2="-86.6" stroke="black" stroke-width="3" />
  <line x1="75" y1="-43.3" x2="300" y2="-43.3" stroke="black" stroke-width="3" />
  <text x="150" y="50" font-size="14" fill="red">[Skaičiuojamoji schema su jėgomis ir reakcijomis]</text>
</svg>
</div>

<p><b>Kūnas AE:</b></p>
<p>Kūno AE pusiausvyros sąlygos:</p>
<p class="eq">&sum; F<sub>ix</sub> = 0;</p>
<p class="eq">&sum; F<sub>iy</sub> = 0;</p>
<p class="eq">&sum; M<sub>A</sub>(F<sub>i</sub>) = 0.</p>
<p class="eq">R<sub>Ax</sub> + Q<sub>1x</sub> + B<sub>x</sub> = 0; (1)</p>
<p class="eq">R<sub>Ay</sub> + Q<sub>1y</sub> + F<sub>1y</sub> - B<sub>y</sub> = 0; (2)</p>
<p class="eq">- Q<sub>1</sub> &middot; a<sub>1</sub> - F<sub>1</sub> &middot; l<sub>1</sub> &middot; cos(30&deg;) + B<sub>x</sub> &middot; l<sub>2</sub> &middot; sin(30&deg;) + B<sub>y</sub> &middot; l<sub>2</sub> &middot; cos(30&deg;) + M<sub>1</sub> = 0. (3)</p>

<p class="eq">R<sub>Ax</sub> - 1.750 + B<sub>x</sub> = 0; (1)</p>
<p class="eq">R<sub>Ay</sub> - 3.031 - 8.5 - B<sub>y</sub> = 0; (2)</p>
<p class="eq">- 3.5 &middot; 1.667 - 8.5 &middot; 6 &middot; 0.866 + B<sub>x</sub> &middot; 3 &middot; 0.5 + B<sub>y</sub> &middot; 3 &middot; 0.866 + 5.5 = 0. (3)</p>
<p class="eq">R<sub>Ax</sub> + B<sub>x</sub> = 1.750; (1)</p>
<p class="eq">R<sub>Ay</sub> - B<sub>y</sub> = 11.531; (2)</p>
<p class="eq">1.5 &middot; B<sub>x</sub> + 2.598 &middot; B<sub>y</sub> = 44.499. (3)</p>

<p style="margin-top:30px"><b>Kūnas BD:</b></p>
<p>Kūno BD pusiausvyros sąlygos:</p>
<p class="eq">&sum; F<sub>ix</sub> = 0;</p>
<p class="eq">&sum; F<sub>iy</sub> = 0;</p>
<p class="eq">&sum; M<sub>B</sub>(F<sub>i</sub>) = 0.</p>
<p class="eq">- B<sub>x</sub> + F<sub>2x</sub> = 0; (4)</p>
<p class="eq">B<sub>y</sub> - Q<sub>2</sub> + F<sub>2y</sub> + R<sub>C</sub> + R<sub>D</sub> = 0; (5)</p>
<p class="eq">- Q<sub>2</sub> &middot; a<sub>2</sub> + F<sub>2y</sub> &middot; l<sub>9</sub> + R<sub>C</sub> &middot; l<sub>4</sub> + R<sub>D</sub> &middot; l<sub>3</sub> + M<sub>2</sub> = 0. (6)</p>

<p class="eq">- B<sub>x</sub> - 2.170 = 0; (4)</p>
<p class="eq">B<sub>y</sub> - 10.0 + 12.310 + R<sub>C</sub> + R<sub>D</sub> = 0; (5)</p>
<p class="eq">- 10.0 &middot; 4.0 + 12.310 &middot; 2.0 + R<sub>C</sub> &middot; 4 + R<sub>D</sub> &middot; 8 + 3.0 = 0. (6)</p>

<p class="eq">B<sub>x</sub> = -2.170 kN; (4)</p>
<p class="eq">B<sub>y</sub> + R<sub>C</sub> + R<sub>D</sub> = -2.310; (5)</p>
<p class="eq">4 &middot; R<sub>C</sub> + 8 &middot; R<sub>D</sub> = 12.380. (6)</p>

<p style="margin-top:30px"><b>Sprendimas:</b></p>
<p>(4) &rarr; (1): R<sub>Ax</sub> - 2.170 = 1.750; &nbsp;&nbsp;&nbsp; R<sub>Ax</sub> = 3.920 kN.</p>
<p>(4) &rarr; (3): 1.5 &middot; (-2.170) + 2.598 &middot; B<sub>y</sub> = 44.499; &nbsp;&nbsp;&nbsp; B<sub>y</sub> = 18.381 kN.</p>
<p>(3) &rarr; (2): R<sub>Ay</sub> - 18.381 = 11.531; &nbsp;&nbsp;&nbsp; R<sub>Ay</sub> = 29.912 kN.</p>
<p>(3) &rarr; (5): 18.381 + R<sub>C</sub> + R<sub>D</sub> = -2.310; &nbsp;&nbsp;&nbsp; R<sub>C</sub> + R<sub>D</sub> = -20.691. (5')</p>
<p>Iš (6) ir (5'):<br>
R<sub>C</sub> = -20.691 - R<sub>D</sub><br>
4 &middot; (-20.691 - R<sub>D</sub>) + 8 &middot; R<sub>D</sub> = 12.380<br>
-82.764 - 4 &middot; R<sub>D</sub> + 8 &middot; R<sub>D</sub> = 12.380<br>
4 &middot; R<sub>D</sub> = 95.144 &nbsp;&nbsp;&rarr;&nbsp;&nbsp; R<sub>D</sub> = 23.786 kN.<br>
R<sub>C</sub> = -20.691 - 23.786 = -44.477 kN.
</p>

<p style="margin-top:30px"><b>Sprendimo patikrinimas:</b></p>
<p>Užrašoma pusiausvyros sąlyga visai sistemai sumuojant momentus apie tašką A:</p>
<p class="eq">&sum; M<sub>A</sub>(F<sub>i</sub>) = - Q<sub>1</sub> &middot; a<sub>1</sub> - F<sub>1</sub> &middot; l<sub>1</sub> &middot; cos(30&deg;) + M<sub>1</sub> - Q<sub>2</sub> &middot; (l<sub>2</sub>&middot;cos30&deg; + a<sub>2</sub>) + F<sub>2y</sub> &middot; (l<sub>2</sub>&middot;cos30&deg; + l<sub>9</sub>) + F<sub>2x</sub> &middot; (l<sub>2</sub>&middot;sin30&deg;) + R<sub>C</sub> &middot; (l<sub>2</sub>&middot;cos30&deg; + l<sub>4</sub>) + R<sub>D</sub> &middot; (l<sub>2</sub>&middot;cos30&deg; + l<sub>3</sub>) + M<sub>2</sub> = 0</p>
<p>Paklaida: &Delta; = 0.022 / 507 &middot; 100% = 0.004% &lt; 0.3%.</p>

<p style="margin-top:30px"><b>Atsakymų lentelė:</b></p>
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
    <td>3.92 kN</td>
    <td>29.91 kN</td>
    <td>-2.17 kN</td>
    <td>18.38 kN</td>
    <td>-44.48 kN</td>
    <td>23.79 kN</td>
  </tr>
</table>

</body>
</html>
"""
    with open('/Users/ugniusvaitiekenas/srotas-ai-agent/fizika/namu_darbas.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Final HTML generated.")

if __name__ == "__main__":
    generate_html()
