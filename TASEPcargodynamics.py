import numpy as np
import random as random
import sys

def compute_N():
 Sum = 0
 for k in S:
  Sum += ms[k]*(Nb - cs[k])
 return Sum
def initialize_motor_distributions(M,L,name_of_ms_file):
 global u  
 m = np.loadtxt(name_of_ms_file,dtype = int)
 b = [ind for ind,val in enumerate(m) if val != 0 and ind > 0 and ind < L-1]
 u = sum(m[1:L-1])
 global m0
 m0 = 1 if m[0] > 0 else 0
 return m,b
def initialize_cargo_distributions(L,name_of_file):
 global l,b
 c = np.loadtxt(name_of_file,dtype = int)
 C = [ind for ind,val in enumerate(c) if val > 0]
 A = [ind for ind in C if ind+1 < L and ind + 1 not in C]
 b = len(C)
 l = len(A)
 c0 = 1 if c[0] > 0 else 0
 return c,C,A,c0
def initialize_S_distributions():
 if len(ms) >= len(C):
  S = [ind for ind in C if ms[ind] > 0 and cs[ind] < Nb]
  return S
 S = [ind for ind,val in enumerate(ms) if val > 0 and ind in C and cs[ind] < Nb]
 return S
def add_cargo():
 motors_to_bind = random.randint(1,np.minimum(ms[0],Nb))
 ms[0] -= motors_to_bind
 cs[0] = motors_to_bind
 C.append(0)
 global b,m0,l,c0
 c0 = 1
 b += motors_to_bind
 if cs[1] == 0:
  A.append(0)
  l += 1 
 if ms[0] > 0 and motors_to_bind < Nb:
  S.append(0)
  return
 elif ms[0] == 0: 
  m0 = 0
def move_bulk_motor_left(Site):  
 Left_site = Site - 1
 ms[Site] -= 1
 ms[Left_site] += 1
 if ms[Site] == 0:
  B.remove(Site)
  if Site in S:
   S.remove(Site)
 if cs[Left_site] > 0 and cs[Left_site] < Nb and Left_site not in S:
   S.append(Left_site)  
 if Site > 1:
  if Left_site not in B:
   B.append(Left_site)
  return 
 global u,m0
 u -= 1
 m0 = 1  
def move_bulk_motor_right(Site): 
 Right_site = Site + 1
 ms[Site] -= 1
 ms[Right_site] += 1
 if ms[Site] == 0:
  B.remove(Site)
  if Site in S:    
   S.remove(Site)
 if cs[Right_site] > 0 and cs[Right_site] < Nb and Right_site not in S:
   S.append(Right_site)
 if Right_site < L-2:
  if Right_site not in B:
   B.append(Right_site)
  return
 global u
 u -= 1 
def move_left_boundary_motor(): 
 ms[0] -= 1
 ms[1] += 1
 global u
 u += 1 
 if ms[0] == 0:
  global m0
  m0 = 0 
  if 0 in S:
   S.remove(0)
 if 1 in B:
  if cs[1] > 0 and cs[1] < Nb and 1 not in S:
   S.append(1)
  return
 B.append(1)
def move_right_boundary_motor():  
 Site = L-1
 Left_site = L-2 
 ms[Site] -= 1
 ms[Left_site] += 1
 global u
 u += 1
 if ms[Site] == 0 and Site in S:  
  S.remove(Site) 
 if Left_site in B:
  if cs[Left_site] > 0 and cs[Left_site] < Nb and Left_site not in S:
   S.append(Left_site)
  return  
 B.append(Left_site) 
# everything above this point seems okay.
def unbind_motor(x):   
 global b,u,l
 b -= 1
 ms[x] += 1
 cs[x] -= 1

 if x > 0:
  if x < L-1:
   u += 1
   if x not in B:
    B.append(x)  
  if cs[x] == 0:
   C.remove(x)      
   if x in S:
    S.remove(x) 
   if x in A:
    A.remove(x) 
    l -= 1 
   if x-1 in C and x-1 not in A:
    A.append(x-1)
    l += 1   
   return x if step >= relax_time else -1
  elif x not in S:
   S.append(x)
  return -1
 # The following will execute when x = 0.
 global m0
 m0 = 1
 if cs[0] == 0:
  global c0
  c0 = 0
  C.remove(0)
  if 0 in S:
   S.remove(0) 
  if x in A:
   A.remove(0) 
   l -= 1 
  return 0 if step >= relax_time else -1
 elif 0 not in S:
  S.append(0)
 return -1
def bind_motor(x):
 global b
 ms[x] -= 1
 cs[x] += 1
 b += 1
 if x > 0 and x < L-1:
  global u
  u -= 1
  if ms[x] == 0:
   B.remove(x)
   S.remove(x)
   return
  if cs[x] == Nb:
   S.remove(x)
  return
 if cs[x] == Nb or ms[x] == 0:
  S.remove(x)
  if x == 0 and ms[0] == 0: 
   global m0
   m0 = 0
  return
def move_a_cargo():
 global l
 x = random.choice(A) #Choosing which cargo to move.
 C.remove(x)
 A.remove(x) 
 l -= 1
 # At this point we have removed x from A and C since we
 # may be potentially removing it from the MT or moving it 
 # to a site with occupied adjacent neighbor.
 
 if x > 0 and x < L - 1:
  cs[x+1] = cs[x]
  C.append(x+1)
  if x < L - 2:
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
  #******************************************************
  # if the above if statement was not met then the only *
  # other option is that x = L-2.                       *
  #******************************************************    
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

 if x == L - 1:
  global b
  b -= cs[x]
  if x in S:
   S.remove(x) 
  ms[x] += cs[x]
  cs[x] = 0
  if cs[x - 1] != 0:
   A.append(x-1)
   l += 1
  return 0 if step >= relax_time else -1
def diffuse_unbound_bulk_motor():
 const1 = R
 const2 = P
 for indx in B:
  temp = 2*p*ms[indx]/D
  if const1 < const2 + temp:
   if bool(random.getrandbits(1)):
    move_bulk_motor_left(indx)
    return
   move_bulk_motor_right(indx)
  return
  const2 += temp
def find_motor_to_unbind():
 const1 = R*D/k_off
 const2 = P*D/k_off
 for indx in C:
  temp = ms[indx]
  if const1 < const2 + temp:
   pass_indx = unbind_motor(indx)
   return pass_indx
  const2 += temp  
def find_motor_to_bind():
 const1 = R*D/k_on
 const2 = P*D/k_on
 for indx in S:
  temp = ms[indx]*(Nb - cs[indx])
  if const1 < const2 + temp:
   bind_motor(indx)
   return
  const2 += temp    
#**************************************************  
# This is where the main part of the code starts. *
#**************************************************
Motors = int(sys.argv[1])
alpha = int(sys.argv[2])

L = 100
Nb = 3

p = 654
k_walk = 1.
k_on = 0.0125 
k_off = 0.00687

ms_file_to_import = "/Users/freddycisneros/Desktop/testingfaster/temp_ms_m_"+str(Motors)+"_alpha_"+str(alpha)+".txt"
cs_file_to_import = "/Users/freddycisneros/Desktop/testingfaster/temp_cs_m_"+str(Motors)+"_alpha_"+str(alpha)+".txt"

fails_file = "fast_fall_m_"+str(Motors)+"_alpha_"+str(alpha)+".txt"
success_file = "fast_success_m_"+str(Motors)+"_alpha_"+str(alpha)+".txt"
ms_file = "fast_ms_m_"+str(Motors)+"_alpha_"+str(alpha)+".txt"
cs_file = "fast_cs_m_"+str(Motors)+"_alpha_"+str(alpha)+".txt"

file1 = open(fails_file, "w")
file2 = open(success_file, "w")
file3 = open(ms_file, "w")
file4 = open(cs_file, "w")

relax_time = 0
next_meansurement = relax_time
measurements = 1000
measurement_interval = 100000
final_time = measurements*measurement_interval + relax_time

l = 0   # length of A
u = 0   # number of unbound motors in the bulk
b = 0   # number of bound motors
N = 0   # the sum of u_x(N_b - b_x)
m0 = 0  #indicates whether the site is occupied by unbound motors

ms,B = initialize_motor_distributions(Motors,L,ms_file_to_import)   # Initialized unbound motor dist. and occupied site dist.
cs,C,A,c0 = initialize_cargo_distributions(L,cs_file_to_import)     # Initialized cargo dist., occupied cargo dist, and empty adjacent site dist.
S = initialize_S_distributions()                                    # Initialized S dist.

step = 0
while step <= final_time:
 step += 1
 if step >= next_meansurement:
  next_meansurement += measurement_interval
  file3.write(' '.join(str(m) for m in ms))
  file3.write('\n')
  file3.flush()
  file4.write(' '.join(str(c) for c in cs))
  file4.write('\n')
  file4.flush()
  
 N = compute_N()
 D = alpha*m0*(1 - c0) + 2.*p*u + p*ms[0] + p*ms[L-1] + k_off*b + k_on*N + k_walk*l 
 P = alpha*m0*(1 - c0)/D 
 R = random.random()
 if R < P:
  # A cargo will step onto the MT.
  add_cargo()
  continue
 if R < P + 2.*p*u/D:
  # An unbound bulk-motor will diffuse.
  diffuse_unbound_bulk_motor()
  continue
 P += 2.*p*u/D
 if R < P + p*ms[0]/D:
  # An unbound motor from the left boundary will diffuse.
  move_left_boundary_motor()
  continue
 P += p*ms[0]/D
 if R < P + p*ms[L-1]/D:
  # An unbound motor from the right boundary will diffuse. 
  move_right_boundary_motor()
  continue
 P += p*ms[L-1]/D
 if R < P + k_off*b/D:
  # A bound motor will unbind.
  val = find_motor_to_unbind()
  if val == -1:
   continue
  file1.write(str(val)+' '+str(step))
  file1.write('\n') 
  file1.flush()    
  continue
 P += k_off*b/D
 if R < P + k_on*N/D:
  # An unbound motor will attach to a cargo.
  find_motor_to_bind()
  continue
 # A cargo will step forward if none of the above options were selected.
 val = move_a_cargo()
 if val == 0:
  file2.write(str(step))
  file2.write('\n')
  file2.flush()
  
file1.close()
file2.close()
file3.close()
file4.close()
