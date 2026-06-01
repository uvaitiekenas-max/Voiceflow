import math

# Given data
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

# 1. Coordinates
O = (0.0, 0.0)
theta_OA = alfa
A = (OA * math.cos(rad(theta_OA)), OA * math.sin(rad(theta_OA)))

theta_AD = alfa + 180.0 + beta
AD_vec = (AD * math.cos(rad(theta_AD)), AD * math.sin(rad(theta_AD)))
D = add(A, AD_vec)

AB = AD / 2
B = add(A, mult(AD_vec, 0.5))

theta_BE = theta_AD + gamma
BE_vec = (EB * math.cos(rad(theta_BE)), EB * math.sin(rad(theta_BE)))
E = add(B, BE_vec)

O2 = add(E, (EO2 * math.cos(rad(delta)), EO2 * math.sin(rad(delta))))

print(f"A = {A}")
print(f"D = {D} (Expected: 0.23, 1.17)")
print(f"B = {B}")
print(f"E = {E} (Expected: 0.00, 2.08)")
print(f"O2 = {O2} (Expected: 0.56, 1.75)")

# 2. Velocities
theta_VA = theta_OA + (90 if W1 > 0 else -90)
vA_mag = abs(W1) * OA
vA = (vA_mag * math.cos(rad(theta_VA)), vA_mag * math.sin(rad(theta_VA)))
print(f"vA = {vA}, mag = {vA_mag}")

theta_VDA_base = theta_AD + 90
a = math.cos(rad(phi))
b = -math.cos(rad(theta_VDA_base))
c = math.sin(rad(phi))
d = -math.sin(rad(theta_VDA_base))
e, f = vA[0], vA[1]

vD_mag_alg, vDA_mag_alg = solve_2x2(a,b,c,d,e,f)
vD = (vD_mag_alg * math.cos(rad(phi)), vD_mag_alg * math.sin(rad(phi)))
vDA = (vDA_mag_alg * math.cos(rad(theta_VDA_base)), vDA_mag_alg * math.sin(rad(theta_VDA_base)))
print(f"vD = {vD}, mag = {mag(vD)}")
print(f"vDA = {vDA}, mag = {mag(vDA)}")

w2 = vDA_mag_alg / AD 
print(f"w2 = {w2}")

vBA = mult(vDA, AB/AD)
vB = add(vA, vBA)
print(f"vB = {vB}, mag = {mag(vB)}")

theta_VE_base = delta + 90
theta_VEB_base = theta_BE + 90
a2 = math.cos(rad(theta_VE_base))
b2 = -math.cos(rad(theta_VEB_base))
c2 = math.sin(rad(theta_VE_base))
d2 = -math.sin(rad(theta_VEB_base))
e2, f2 = vB[0], vB[1]

vE_mag_alg, vEB_mag_alg = solve_2x2(a2,b2,c2,d2,e2,f2)
vE = (vE_mag_alg * math.cos(rad(theta_VE_base)), vE_mag_alg * math.sin(rad(theta_VE_base)))
vEB = (vEB_mag_alg * math.cos(rad(theta_VEB_base)), vEB_mag_alg * math.sin(rad(theta_VEB_base)))
print(f"vE = {vE}, mag = {mag(vE)}")
print(f"vEB = {vEB}, mag = {mag(vEB)}")

w3 = vEB_mag_alg / EB
w4 = vE_mag_alg / EO2
print(f"w3 = {w3}")
print(f"w4 = {w4}")

# 3. Accelerations
aA_mag = W1**2 * OA
theta_aA = theta_OA + 180
aA = (aA_mag * math.cos(rad(theta_aA)), aA_mag * math.sin(rad(theta_aA)))
print(f"aA = {aA}, mag = {aA_mag}")

theta_aDAn = theta_AD + 180
aDAn_mag = w2**2 * AD
aDAn = (aDAn_mag * math.cos(rad(theta_aDAn)), aDAn_mag * math.sin(rad(theta_aDAn)))

theta_aDAt_base = theta_AD + 90
a3 = math.cos(rad(phi))
b3 = -math.cos(rad(theta_aDAt_base))
c3 = math.sin(rad(phi))
d3 = -math.sin(rad(theta_aDAt_base))
b_vec_a = add(aA, aDAn)
e3, f3 = b_vec_a[0], b_vec_a[1]

aD_mag_alg, aDAt_mag_alg = solve_2x2(a3,b3,c3,d3,e3,f3)
aD = (aD_mag_alg * math.cos(rad(phi)), aD_mag_alg * math.sin(rad(phi)))
aDAt = (aDAt_mag_alg * math.cos(rad(theta_aDAt_base)), aDAt_mag_alg * math.sin(rad(theta_aDAt_base)))
eps2 = aDAt_mag_alg / AD
print(f"aD = {aD}, mag = {mag(aD)}")
print(f"eps2 = {eps2}")

aBAn = mult(aDAn, AB/AD)
aBAt = mult(aDAt, AB/AD)
aB = add(add(aA, aBAn), aBAt)
print(f"aB = {aB}, mag = {mag(aB)}")

theta_aEn = delta
aEn_mag = w4**2 * EO2
aEn = (aEn_mag * math.cos(rad(theta_aEn)), aEn_mag * math.sin(rad(theta_aEn)))
theta_aEt_base = delta + 90

theta_aEBn = theta_BE + 180
aEBn_mag = w3**2 * EB
aEBn = (aEBn_mag * math.cos(rad(theta_aEBn)), aEBn_mag * math.sin(rad(theta_aEBn)))
theta_aEBt_base = theta_BE + 90

a4 = math.cos(rad(theta_aEt_base))
b4 = -math.cos(rad(theta_aEBt_base))
c4 = math.sin(rad(theta_aEt_base))
d4 = -math.sin(rad(theta_aEBt_base))
b_vec_a2 = sub(add(aB, aEBn), aEn)
e4, f4 = b_vec_a2[0], b_vec_a2[1]

aEt_mag_alg, aEBt_mag_alg = solve_2x2(a4,b4,c4,d4,e4,f4)
aEt = (aEt_mag_alg * math.cos(rad(theta_aEt_base)), aEt_mag_alg * math.sin(rad(theta_aEt_base)))
aEBt = (aEBt_mag_alg * math.cos(rad(theta_aEBt_base)), aEBt_mag_alg * math.sin(rad(theta_aEBt_base)))
aE = add(aEn, aEt)
eps3 = aEBt_mag_alg / EB
eps4 = aEt_mag_alg / EO2

print(f"aE = {aE}, mag = {mag(aE)}")
print(f"eps3 = {eps3}")
print(f"eps4 = {eps4}")
