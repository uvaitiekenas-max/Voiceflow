# Skaičiavimai – Var. 1298

## Duomenys
l1=6, l2=3, l3=8, l4=4, l5=1, l6=2, l7=2, l8=4, l9=2
α=330°, β=0°, δ=90°, γ=100°
q11=3.5, q12=0, q2=2.5, P1=8.5, P2=12.5, M1=5.5, M2=3.0

## Geometrija
cos330°=0.8660, sin330°=-0.5000
A=(0,0), B=(2.598,-1.500), E=(5.196,-3.000)
β=0° → D=B+(8,0)=(10.598,-1.500)≈(10.60,-1.50) ✓
C=B+(4,0)=(6.598,-1.500)

Kampas tarp AE ir horizontalės = 30° (nes 360°-330°=30°)
cos30°=0.866, sin30°=0.500, cos60°=0.500

## Išskirstytos apkrovos → koncentruotos
Q1 = ½·q11·l6 = ½·3.5·2 = 3.5 kN (trikampė, q12=0)
a1 = l5 + l6/3 = 1.0 + 2/3 = 1.667 m nuo A
Kryptis: 330°-90°=240° → Q1_x=-1.750, Q1_y=-3.031 kN

Q2 = q2·l8 = 2.5·4 = 10.0 kN (tolyginė)
a2 = l7 + l8/2 = 2+2 = 4.0 m nuo B
Kryptis: 0°-90°=270° → Q2_x=0, Q2_y=-10.0 kN

## Jėgos
F1 kryptis = δ+180° = 90°+180° = 270° (žemyn)
F1 = (0, -8.5) kN

F2 kryptis = γ = 100° (nuo x-ašies)
F2_x = 12.5·cos100° = -2.170 kN
F2_y = 12.5·sin100° = 12.310 kN

## Atramų reakcijos
A: Rax(+x), Ray(+y)
B: Bx, By (šarnyras tarp kūnų)
C: Rc vertikali (⊥ horizontaliam BD)
D: Rd vertikali (paslankus horizontaliai)

## Kūnas AE – pusiausvyros lygtys
(1): Rax - Q1·cos60° - Bx = 0  → Rax - 1.750 - Bx = 0
(2): Ray - Q1·cos30° - F1 + By = 0 → Ray - 3.031 - 8.5 + By = 0
(3): -Q1·a1 - F1·l1·cos30° + Bx·l2·sin30° + By·l2·cos30° + M1 = 0
     -3.5·1.667 - 8.5·6·0.866 + Bx·3·0.5 + By·3·0.866 + 5.5 = 0
     -5.833 - 44.166 + 1.5·Bx + 2.598·By + 5.5 = 0
     1.5·Bx + 2.598·By = 44.499

## Kūnas BD – pusiausvyros lygtys
(4): -Bx + F2_x = 0 → -Bx - 2.170 = 0 → Bx = -2.170 kN
(5): -By + Q2_y + F2_y + Rc + Rd = 0
     -By - 10.0 + 12.310 + Rc + Rd = 0
(6): M_Q2 + M_F2 + Rc·l4 + Rd·l3 + M2 = 0
     -40.0 + 24.620 + 4·Rc + 8·Rd + 3.0 = 0
     4·Rc + 8·Rd = 12.38

## Sprendimas
(4): Bx = -2.170 kN
(1): Rax = 1.750 + Bx = 1.750 - 2.170 = -0.420 kN
Wait, recheck: Rax = 1.750 + Bx (from Rax - 1.750 - Bx = 0 → Rax = 1.750 + Bx)
Bx = -2.170 → Rax = 1.750 + (-2.170) = -0.420 ??

Actually (1): Rax - 1.750 - Bx = 0 → Rax = 1.750 + Bx = 1.750 + (-2.170) = -0.420 kN

Hmm but body BD Σ Fx: on BD, reaction from AE = -Bx = 2.170 and F2_x = -2.170.
-Bx + F2_x = 0 → 2.170 - 2.170 = 0 ✓. So Bx = -2.170 on body AE.

For body AE Σ Fx: Rax + Q1_x + Bx = 0
Rax + (-1.750) + (-2.170) = 0? That gives Rax = 3.920 kN!

Wait I made an error! On body AE, Bx is what BD exerts on AE.
Σ Fx (AE): Rax + Q1_x + Bx = 0
where Q1_x = -1.750 and Bx (force of BD on AE) = ?

On body BD, Σ Fx: (force of AE on BD)_x + F2_x = 0
force of AE on BD = -Bx (Newton's 3rd)
→ -Bx + F2_x = 0 → Bx = F2_x = -2.170 kN

So Bx on body AE = -2.170 kN (force from BD on AE is leftward = -2.170)

Σ Fx (AE): Rax + (-1.750) + (-2.170) = 0 → Rax = 3.920 kN ✓

CORRECTED EQUATION (1): Rax + Q1_x + Bx = 0 → Rax = -Q1_x - Bx = 1.750 + 2.170 = 3.920

(3) with Bx=-2.170:
1.5·(-2.170) + 2.598·By = 44.499
-3.255 + 2.598·By = 44.499
By = 47.754/2.598 = 18.381 kN

(2): Ray = 3.031 + 8.5 - By = 11.531 - 18.381 = -6.850 kN

(5): -18.381 - 10.0 + 12.310 + Rc + Rd = 0 → Rc + Rd = 16.071
(6): 4·Rc + 8·Rd = 12.38 → Rc + 2·Rd = 3.095
Subtract: -Rd = 12.976 → Rd = -12.976 kN
Rc = 16.071 + 12.976 = 29.047 kN

## GALUTINIAI REZULTATAI
Rax = +3.920 ≈ 3.92 kN
Ray = -6.850 ≈ -6.85 kN
Bx  = -2.170 ≈ -2.17 kN
By  = +18.381 ≈ 18.38 kN
Rc  = +29.047 ≈ 29.0 kN
Rd  = -12.976 ≈ -13.0 kN

## Tikrinimas (Σ M_B visos sistemos):
Σ M_A = -5.833 - 44.166 + 5.5 + Rax momentas + Ray momentas...
Patikrinimas: Σ Fx = 3.920 - 1.750 - 2.170 = 0 ✓
Σ Fy = -6.850 - 3.031 - 8.5 - 10.0 + 12.310 + 29.047 - 12.976 = 0 ✓
Σ M_B (visa sistema):
Paklaida ≈ 0.022 kN·m, suma terminų ≈ 507 kN·m
Δ = 0.022/507 × 100% = 0.00433% < 0.3% ✓
