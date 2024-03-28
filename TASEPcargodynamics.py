import numpy as np
import random as random
import sys
import time

def print_info():
 print("Parameters")
 print("l = ",l)
 print("u = ",u)
 print("b = ",b)
 print("N = ",N)
 print("m0 = ",m0)
 print()
 print("ms = ",ms)
 print("B = ",B)
 print("cs = ",cs)
 print("C = ",C)
 print("A = ",A)
 print("S = ",S)
def Ncomputer():
 temp = 0
 for k in S:
  if ms[k] != 0 and cs[k] < Nb and cs[k] >0:
   temp += ms[k]*(Nb - cs[k])
 return temp
def initialize_motor_distributions(M,L):
 global u
 m = [0 for i in range(L)]
 temp = M
 if M < L:
  for i in range(L):
   if temp == 0:
    break
   temp -=1
   m[i] = 1
 else:
  m = [int(M/L) for i in range(L)]
  temp -= L*int(M/L)
  if temp > 0:
   for i in range(L):
    if temp == 0:
     break
    temp -=1
    m[i] += 1
 b = [i for i,j in enumerate(m) if j != 0 and i > 0 and i < L-1]
 u = sum(m[1:L-1])
 if m[0] > 0:
  global m0
  m0 = 1
 return m,b
def initialize_cargo_distributions(L):
 global l,b
 c = np.zeros(L,int)
 C = [i for i,j in enumerate(c) if j > 0]
 A = []
 for index in C:
  if (index + 1 < L) and (index + 1 not in C):
   A.append(index)
 b = len(C)
 l = len(A)
 c0 = 0
 if c[0] > 0:
  c0 = 1
 return c,C,A,c0
def initialize_S_distributions():
 global N
 S = []
 if len(ms) >= len(C):
  for ind in C:
   if ms[ind] > 0 and cs[ind] < Nb:
    S.append(ind)
    N += ms[ind]*(Nb - cs[ind])
 else:
  for ind,val in enumerate(ms):
   if val > 0 and ind in C and cs[ind] < Nb:
    S.append(ind)
    N += val*(Nb - cs[ind])
 return S
def add_cargo():
 global b,N,m0,l,c0
 motors_to_bind = random.choice(range(np.minimum(ms[0],Nb))) + 1
 ms[0] -= motors_to_bind
 cs[0] = motors_to_bind
 C.append(0)
 c0 = 1
 b += motors_to_bind
 if cs[1] == 0:
  A.append(0)
  l += 1
 if ms[0] == 0:
  m0 = 0
  return
 if ms[0] > 0 and motors_to_bind < Nb:
  S.append(0)
def move_bulk_motor_left(x):  
 ms[x] -= 1
 ms[x-1] += 1
 if x == 1:
  global u,m0
  u -= 1
  m0 = 1   
 if ms[x] == 0:
  B.remove(x)
 if x > 1 and x-1 not in B:
  B.append(x-1)
 global N
 if x in S:  
  if ms[x] == 0:
   S.remove(x)
 if cs[x-1] > 0 and cs[x-1] < Nb:
  if x-1 not in S:
   S.append(x-1)
def move_bulk_motor_right(x): 
 ms[x] -= 1
 ms[x+1] += 1
 if x == L-2:
  global u
  u -= 1 
 if ms[x] == 0:
  B.remove(x)
 if x < L-2 and x+1 not in B:
  B.append(x+1)
 global N
 if x in S:  
  if ms[x] == 0:
   S.remove(x)
 if cs[x+1] > 0 and cs[x+1] < Nb:
  if x+1 not in S:
   S.append(x+1)
def diffuse_unbound_bulk_motor():
 const1 = R
 const2 = P
 for val in B:
  temp = 2*p*ms[val]/D
  if const1 < const2 + temp:
   if bool(random.getrandbits(1)):
    move_bulk_motor_left(val)
    return
   move_bulk_motor_right(val)
   return
  const2 += temp
def move_left_boundary_motor(): 
 ms[0] -= 1
 ms[1] += 1
 global u
 u += 1 
 if ms[0] == 0:
  global m0
  m0 = 0  
 if 1 not in B:
  B.append(1)   
 if 0 in S:
  if ms[0] == 0:
   S.remove(0)
 if cs[1] > 0 and cs[1] < Nb:
  if 1 not in S:
   S.append(1)
def move_right_boundary_motor():  
 global u
 ms[L-1] -= 1
 ms[L-2] += 1
 u += 1  
 if L-2 not in B:
  B.append(L-2)
 if L-1 in S:  
  if ms[L-1] == 0:
   S.remove(L-1)
 if cs[L-2] > 0 and cs[L-2] < Nb:
  if L-2 not in S:
   S.append(L-2)
def find_motor_to_unbind():
 const1 = R
 const2 = P
 for val in C:
  temp = ms[val]*k_off/D
  if const1 < const2 + temp:
   pass_val = unbind_motor(val)
   return pass_val
  const2 += temp
def unbind_motor(x):
 global b
 ms[x] += 1
 cs[x] -= 1
 b -= 1
 if x == 0:
  global m0
  m0 = 1
  if cs[0] == 0:
   global c0
   c0 = 0
 if x > 0 and x < L-1:
  global u
  u += 1
  if x not in B:
   B.append(x)
 if cs[x] == 0:
  C.remove(x)
  if x in A:
   global l
   l -= 1
   A.remove(x) 
  if x > 0 and cs[x-1] > 0 and (x-1 not in A):
   A.append(x-1)
   l += 1   
 if (cs[x] == 0 or ms[x] == 0) and x in S:
  S.remove(x)
 if cs[x] == 0:
  global relax_time,step
  if step >= relax_time:
   global num_of_fails
   num_of_fails += 1
   return x   
  return -1 
 if cs[x] < Nb and cs[x] > 0 and ms[x] != 0:      
  if x not in S:
   S.append(x)
def find_motor_to_bind():
 const1 = R*D/k_on
 const2 = P*D/k_on
 for val in S:
  temp = ms[val]*(Nb - cs[val])
  if const1 < const2 + temp:
   bind_motor(val)
   return
  const2 += temp
def bind_motor(x):
 global b
 ms[x] -= 1
 cs[x] += 1
 b += 1
 if cs[x] == Nb or ms[x] == 0:
  S.remove(x)
 if x == 0: 
  if ms[0] == 0:
   global m0
   m0 = 0
  return
 if x > 0 and x < L-1:
  global u
  u -= 1
  if ms[x] == 0:
   B.remove(x)
def move_a_cargo():
 global l,b
 x = random.choice(A)
 l -= 1
 C.remove(x)
 A.remove(x) 
    
 # If the site chosen to update is the left boundary.
 if x == 0:
  cs[x+1] = cs[x]
  C.append(x+1)
  if cs[x+2] == 0:
   A.append(x+1)
   l += 1
  if x in S:
   S.remove(x)
   if ms[x+1] > 0:
    S.append(x+1)
  cs[x] = 0
  global c0 
  c0 = 0
  return -1
 # If the site chosen to update is the bulk.
 if x > 0 and x < L - 1:
  cs[x+1] = cs[x]
  C.append(x+1)
  # If the site chosen is the second to last site.
  if x == L-2:
   A.append(x+1)
   l += 1
   if cs[x-1] != 0:
    A.append(x-1)
    l += 1
   if x in S:
    S.remove(x)
    if ms[x+1] > 0:
     S.append(x+1)
   cs[x] = 0
   return -1
  if x >= 1 and x < L - 2:
   if cs[x+2] == 0:
    A.append(x+1)
    l += 1
   if cs[x-1] != 0: 
    A.append(x-1)
    l += 1
   if x in S:
    S.remove(x)
    if ms[x+1] > 0:
     S.append(x+1)
   cs[x] = 0
   return -1
 if x == L - 1:
  global relax_time,step
  if step >= relax_time:
   global num_of_success
   num_of_success += 1
  b -= cs[x]
  if x in S:
   S.remove(x) 
  ms[x] += cs[x]
  cs[x] = 0
  if cs[x - 1] != 0:
   A.append(x-1)
   l += 1
  return 0
#*********************
# List of parameters *
#*********************

Motors = int(sys.argv[1])
alpha = int(sys.argv[2])

L = 100
Nb = 3

p = 654
k_walk = 1
k_on = 0.0125 
k_off = 0.00687

relax_time = 0
num_of_success = 0
num_of_fails = 0

step = 0

l = 0  # length of A
u = 0  # number of unbound motors in the bulk
b = 0  # number of bound motors
N = 0  # the sum of u_x(N_b - b_x)
m0 = 0 #indicates whether the site is occupied by unbound motors

fails_file = "fall_m_"+str(Motors)+"_alpha_"+str(alpha)+".txt"
success_file = "success_m_"+str(Motors)+"_alpha_"+str(alpha)+".txt"
ms_file = "ms_m_"+str(Motors)+"_alpha_"+str(alpha)+".txt"
cs_file = "cs_m_"+str(Motors)+"_alpha_"+str(alpha)+".txt"

file1 = open(fails_file, "w")
file2 = open(success_file, "w")
file3 = open(ms_file, "w")
file4 = open(cs_file, "w")

num_of_success = 0
num_of_fails = 0

relax_time = 100000000
next_meansurement = relax_time
measurements = 100000
measurement_interval = 100000
final_time = measurements*measurement_interval + relax_time
'''
# to test
relax_time = 10000
next_meansurement = relax_time
measurements = 100000
measurement_interval = 1000
final_time = measurements*measurement_interval + relax_time
'''
'''
relax_time = 1000
next_meansurement = relax_time
measurements = 1000

measurement_interval = 1000
final_time = measurements*measurement_interval + relax_time
'''

l = 0  # length of A
u = 0  # number of unbound motors in the bulk
b = 0  # number of bound motors
N = 0  # the sum of u_x(N_b - b_x)
m0 = 0 #indicates whether the site is occupied by unbound motors
ms,B = initialize_motor_distributions(Motors,L)    # Initialized unbound motor dist. and occupied site dist.
cs,C,A,c0 = initialize_cargo_distributions(L)      # Initialized cargo dist., occupied cargo dist, and empty adjacent site dist.
S = initialize_S_distributions()                   # Initialized S dist.
G = 0
   
step = 0
while step <= final_time:
 step += 1
 if step >= next_meansurement:
  next_meansurement += measurement_interval
  file3.write(' '.join(str(m) for m in ms))
  file3.write('\n')
  file4.write(' '.join(str(c) for c in cs))
  file4.write('\n')

 R = random.random()
 N = Ncomputer()
 D = alpha*m0*(1 - c0) + 2.*p*u + p*ms[0] + p*ms[L-1] + k_off*b + k_on*N + k_walk*l 
 P = alpha*m0*(1 - c0)/D 
 if R < P:
  # a cargo will step on microtubule.
  add_cargo()
  continue
 if R < P + 2.*p*u/D:
  # an unbound bulk motor will diffuse.
  diffuse_unbound_bulk_motor()
  continue
 P += 2.*p*u/D
 if R < P + p*ms[0]/D:
  # an unbound motor from the left boundary will diffuse.
  move_left_boundary_motor()
  continue
 P += p*ms[0]/D
 if R < P + p*ms[L-1]/D:
  # an unbound motor from the right boundary will diffuse.
  move_right_boundary_motor()
  continue
 P += p*ms[L-1]/D
 if R < P + k_off*b/D:
  # a bound motor will unbind.
  val = find_motor_to_unbind()
  if val == -1:
   continue
  else:
   file1.write(str(val)+' '+str(step))
   file1.write('\n')     
   continue
 P += k_off*b/D
 if R < P + k_on*N/D:
  # an unbound motor will attach.
  find_motor_to_bind()
  continue
 # an cargo will step forward if none of the above options were selected.
 val = move_a_cargo()
 if val == 0:
  file2.write(str(val))
  file2.write('\n')   
file1.close()
file2.close()
file3.close()
file4.close()