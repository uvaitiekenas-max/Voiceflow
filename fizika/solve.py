import math

# Duomenys
l1, l2, l3, l4, l5, l6, l7, l8, l9 = 6.0, 3.0, 8.0, 4.0, 1.0, 2.0, 2.0, 4.0, 2.0
alfa_deg, beta_deg, delta_deg, gamma_deg = 330.0, 0.0, 90.0, 100.0
q11, q12, q2 = 3.5, 0.0, 2.5
F1_val, F2_val = 8.5, 12.5
M1, M2 = 5.5, 3.0

alfa = math.radians(alfa_deg)
beta = math.radians(beta_deg)
delta = math.radians(delta_deg)
gamma = math.radians(gamma_deg)

# Kūno AE jėgos ir momentai
Q1 = 0.5 * q11 * l6
a1 = l5 + l6 / 3.0
# Q1 kryptis statmena AE (prieš laikrodžio rodyklę nuo AE).
# Brėžinyje q11 rodyklės nukreiptos į AE, tad Q1 jėga veikia į AE.
# Iš pavyzdžio matome, kad rodyklės veikia iš kairės/apačios į dešinę/viršų?
# Pavyzdyje alfa=120, strypas eina į viršų-kairę. Q1 rodyklės nukreiptos į viršų-dešinę (statmenai strypui).
# T.y. kampas alfa - 90 deg.
# Mūsų atveju alfa=330. Statmena į strypą bus 330 - 90 = 240 deg (žemyn-kairėn) arba 330 + 90 = 60 deg (aukštyn-dešinėn).
# Paprastai gravitacijos ar apkrovos spaudžia iš viršaus. Jei 1 pav neturime, imsime standartą: jėga veikia statmenai išorėn arba vidinėn. Pavyzdyje matome Q1_y < 0, reiškia spaudžia žemyn.
# Pavyzdyje kampas 120. Q1_y < 0 => kampas 120 + 90 = 210 or 120 - 90 = 30?
# Q1_x = Q1 * cos(30) > 0, Q1_y = -Q1 * sin(30) < 0? No, in sample: Q1_x = Q1 * cos(30) and Q1_y = -Q1 * sin(30) is not what they used.
# Let's check sample: Rax + Q1*cos(30) - Rbx = 0; Ray + Q1*cos(60) + F1...
# So Q1_x = -Q1*cos(30) in sum? No, +Q1*cos(30). Q1_y = +Q1*cos(60) = +Q1*sin(30).
# Let's just use my previous angles which gave Q1_x = -1.75, Q1_y = -3.03. (Angle 240 deg).

Q1_ang = math.radians(alfa_deg - 90)
Q1_x = Q1 * math.cos(Q1_ang)
Q1_y = Q1 * math.sin(Q1_ang)

F1_ang = delta # 90 degrees
F1_x = F1_val * math.cos(F1_ang)
F1_y = F1_val * math.sin(F1_ang) # 8.5

# Kūno BD jėgos ir momentai
Q2 = q2 * l8
a2 = l7 + l8 / 2.0
# Q2 veikia vertikaliai žemyn
Q2_x = 0
Q2_y = -Q2

# F2 kampas = gamma = 100 nuo BD (BD yra beta = 0). Tad F2 kampas = 100 deg
F2_ang = beta + gamma
F2_x = F2_val * math.cos(F2_ang)
F2_y = F2_val * math.sin(F2_ang)

print(f"Q1_x: {Q1_x:.3f}, Q1_y: {Q1_y:.3f}")
print(f"F1_x: {F1_x:.3f}, F1_y: {F1_y:.3f}")
print(f"F2_x: {F2_x:.3f}, F2_y: {F2_y:.3f}")

# Equations for BD
# Sum Fx = 0 -> -Bx + F2_x = 0 -> Bx = F2_x
Bx = F2_x

# Moment around D = 0 for BD
# B is at (0, 0) local for BD? D is at l3. 
# Sum M_D = 0: 
# -By * l3 - M_Q2 + M_F2 + Rc * l4 - M2 = 0?
# Let's use D as origin for BD just to be sure.
# B = (-8, 0). C = (-4, 0).
# q2 is from D: l7 to l7+l8 -> from x=0 to x=-4. Center is at x=-2 (or a2=4 from B)
# F2 is at l9 from D -> x=-2 (or 6 from B)
# Wait, my previous calculation: D is on the right. B is on the left.
# B_x = 2.598, D_x = 10.598.
# B is at local x=0. D is at local x=8.
# C is at local x = 8 - 4 = 4.
# q2 is from x = 8 - 2 = 6 to x = 6 - 4 = 2. Center of Q2 is at x = 4. (a2 = 4).
# F2 is at x = 8 - 2 = 6.
# By * 0 - Q2 * a2 + Rc * (8-4) + F2_y * (8-2) + Rd * 8 = 0 -> this is moment around B!
# My previous eq (6): M_B = -Q2 * a2 + F2_y * (8-l9) + Rc * (8-l4) + Rd * 8 + M2 = 0
# Let's re-verify:
# B is at 0.
# Q2 is at 4. Moment = -Q2 * 4 (clockwise, since Q2_y is negative)
# F2 is at 6. Moment = F2_y * 6 (F2_y is positive -> CCW -> +)
# Rc is at 4. Moment = Rc * 4 (if Rc is positive UP)
# Rd is at 8. Moment = Rd * 8
# M2 = 3.0 (positive -> CCW)
# Eq(6): -Q2*4 + F2_y*6 + Rc*4 + Rd*8 + M2 = 0
# 4*Rc + 8*Rd = Q2*4 - F2_y*6 - M2
const_6 = Q2*4 - F2_y*6 - M2
print(f"Eq 6: 4 Rc + 8 Rd = {const_6:.3f}")

# Eq(5): Sum Fy = 0 -> -By (force of AE on BD is -By) + Q2_y + F2_y + Rc + Rd = 0
# -By - 10 + 12.31 + Rc + Rd = 0
# Rc + Rd = By - 2.31

# Equations for AE
# Bx, By are forces from BD on AE.
# By Newton's third law, BD experiences -Bx, -By.
# So Sum Fx for BD: -Bx + F2_x = 0 => Bx = F2_x = -2.17
# For AE:
# Sum Fx = Rax + Q1_x + F1_x + Bx = 0
Rax = -Q1_x - F1_x - Bx

# Sum M_A = 0
# Q1 is at a1=1.667. Force is perpendicular. Moment = -Q1 * a1. (Clockwise)
# F1 is at E. E = (l1*cos330, l1*sin330). F1_x=0, F1_y=8.5.
# Moment of F1 = E_x * F1_y - E_y * F1_x = 5.196 * 8.5 - (-3) * 0 = 44.167. (CCW)
# B is at (l2*cos330, l2*sin330). B_x = 2.598, B_y = -1.5.
# Moment of B = B_x * By - B_y * Bx = 2.598 * By - (-1.5) * (-2.17) = 2.598 * By - 3.255
# M1 = 5.5
# Eq(3): -Q1 * a1 + 44.167 + 2.598 * By - 3.255 + 5.5 = 0
# 2.598 * By = Q1 * a1 - 44.167 + 3.255 - 5.5
By = (Q1 * a1 - 44.167 + 3.255 - 5.5) / 2.598

# Now back to BD to find Rc, Rd
# Rc + Rd = By - 2.31
const_5 = By - F2_y - Q2_y # By - 12.31 - (-10) = By - 2.31
# 4 Rc + 8 Rd = const_6
# 4 Rc + 4 Rd = 4 * const_5
# 4 Rd = const_6 - 4 * const_5
Rd = (const_6 - 4 * const_5) / 4.0
Rc = const_5 - Rd

# Finally Ray
# Sum Fy for AE: Ray + Q1_y + F1_y + By = 0
Ray = -Q1_y - F1_y - By

print(f"Rax = {Rax:.3f}")
print(f"Ray = {Ray:.3f}")
print(f"Bx  = {Bx:.3f}")
print(f"By  = {By:.3f}")
print(f"Rc  = {Rc:.3f}")
print(f"Rd  = {Rd:.3f}")

# Check global moment around A
# MA = -Q1*a1 + E_x*F1_y - E_y*F1_x + M1 - Q2_y*D_q2_x + Q2_x*D_q2_y + ...
# Let's just use the components
# D is at B + (8, 0) = (10.598, -1.5)
# C is at B + (4, 0) = (6.598, -1.5)
# Q2 is at B + (4, 0) = (6.598, -1.5)
# F2 is at B + (6, 0) = (8.598, -1.5)
MA_total = (-Q1 * a1) + (5.196 * F1_y - (-3.0) * F1_x) + M1 \
           + (6.598 * Q2_y - (-1.5) * Q2_x) \
           + (8.598 * F2_y - (-1.5) * F2_x) \
           + (6.598 * Rc - (-1.5) * 0) \
           + (10.598 * Rd - (-1.5) * 0) \
           + M2

print(f"Global MA check: {MA_total:.3f}")
