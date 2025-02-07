from time import perf_counter
import random
import hashlib



def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, d):
    g, x, y = egcd(a, d)
    if g != 1:
        return 0 #raise Exception('modular inverse does not exist')
    else:
        return x % d  
    

# c1: r >> 
# c2: r1 <<   mod inverse of r (to process easier, it should be selected first)
# c3: p < k*r         
# c4: a*k < b        
# c5: r1*b < p      
# c6: e < a             
    

K = 145173047051377849223662959899216603567
R = 629926603567
A = 1451730470053236629598992166035061
B = 622288097498926496141095869268883569994445630555888889996063592498055290461
E = 521419622856657689423872613770

K2 = 2*K
R2 = 2*R
B2 = 2*B
A2 = 2*A
E2 = 2*E

p = 282755483533707287054752184321121345766861480697448703443857012153264407439766013042402571     


start_time = perf_counter()

# Alice
k = random.randrange(K, K2, 1)
r1 = random.randrange(R, R2, 1)
r = modinv(r1, p)
c1 = k*r %p                # send c1 to bob

# Bob
a = random.randrange(A, A2, 1)
b = random.randrange(B, B2, 1)
c2 = (c1*a + b) % p            # send c2 to alice


# -------------------- Round 2 --------------------------------


# Alice
e = random.randrange(E, E2, 1)
c3 = (c2*r1 + e) %p
ca = e*k %p
h = hashlib.sha256(str.encode(str(ca))).hexdigest()
ca = int(h,16) %p  # send c3 and ca to bob
                   # to prove legitimacy, in pratice, Alice signs "ca" and sends the signature instead

# Bob
ee = (c3 %b) %a
kk = (((c3 - ee) %b) * modinv(a, p)) %p

rr1 = (c3//b)
rr = modinv(rr1, p)
cb = ee*kk %p
h = hashlib.sha256(str.encode(str(cb))).hexdigest()
cb = int(h,16) %p

if ca == cb:                 # seccess, the secret key is k
    ccb = ee*rr %p 
    h = hashlib.sha256(str.encode(str(ccb))).hexdigest()
    ccb = int(h,16) %p     # send ccb to alice, to prove he has the valid numbers
    # to prove legitimacy, in pratice, Bob signs "ccb" and sends the signature instead
else: print('err bob')

# Alice
cca = e*r %p
h = hashlib.sha256(str.encode(str(cca))).hexdigest()
cca = int(h,16) %p
if ccb == cca: print('seccess ') # seccess, the secret key is k, bob has the same k
else: print('err alice')

end_time = perf_counter()

print('time ', end_time-start_time) 




