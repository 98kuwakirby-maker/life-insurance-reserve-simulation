import math
import numpy as np
import random

##############################
# the value of l_x and mu_x
##############################
l_tPLUS40 = [
96500, 96334, 96155, 95961, 95751,
95521, 95266, 94983, 94668, 94316,
93925, 93489, 93004, 92467, 91873,
91217, 90490, 89684, 88792, 87805,
86714, 85507, 84173, 82701, 81076,
79293, 77353, 75256, 73001, 70598,
68055, 65381, 62562, 59593, 56484,
53266, 49965, 46579, 43124, 39630,
36128, 32654, 29254, 25954, 22779,
19756, 16917, 14280, 11874, 9730,
7857, 6249, 4880, 3726, 2773,
2011, 1421, 979, 657, 428,
271, 166, 98, 56, 31,
16, 8, 4, 2, 1
]

mu_tPLUS40 = [
0.00166, 0.00179, 0.00193, 0.00210, 0.00229,
0.00253, 0.00281, 0.00314, 0.00352, 0.00393,
0.00440, 0.00492, 0.00549, 0.00610, 0.00679,
0.00757, 0.00845, 0.00945, 0.01057, 0.01182,
0.01323, 0.01483, 0.01664, 0.01870, 0.02101,
0.02348, 0.02610, 0.02893, 0.03192, 0.03505,
0.03833, 0.04198, 0.04626, 0.05105, 0.05609,
0.06123, 0.06694, 0.07352, 0.08068, 0.08840,
0.09675, 0.10544, 0.11464, 0.12491, 0.13627,
0.14857, 0.16208, 0.17689, 0.19190, 0.20647,
0.22114, 0.23754, 0.25793, 0.28226, 0.30837,
0.33424, 0.35974, 0.38579, 0.41313, 0.44216,
0.47312, 0.50609, 0.54117, 0.57832, 0.61901,
0.66418, 0.70630, 0.75111, 0.79741, 0.84499
]

#############################
# the value of i and delta
#############################

#-----HAVE A GOOD SIMULATION LIFE CHANGING THIS INTEREST VALUE :) -----#
i = 0.02 # constant
delta = math.log(1 + i)

#################$###############################################
# calculate the life insurance annual premium
# which the sum assured payable upon death is 1,
# the sum assured will be paid immediately after the death,
# the premiums are paid annually in advance
#################################################################

# P * ddota_40 = barA_40 = i / delta * A_40
# A_40 = 1 - d * ddota_40
# ddota_40 = (v**0)*(l_40+0/l_40) + (v**1)*(l_40+1/l_40) +...+ (v**69)*(l_40+69/l_40)

# calculate v and d
v = 1 / (1 + i)
d = i / (1 + i)

# Calculate ddota_40
ddota_40 = 0
for j in range(len(l_tPLUS40)):
    ddota_40 += (v**j) * (l_tPLUS40[j] / l_tPLUS40[0])

# Calculate A_40
A_40 = 1 - (d * ddota_40)

# Calculate barA_40 (using UDD approximation i/delta)
barA_40 = (i / delta) * A_40

# Calculate Annual Premium P
P = barA_40 / ddota_40





#######################################################################################
# simulation
#######################################################################################

############################################################
# initialize
############################################################

# the number of observation
N = 10000

# create the policyholder's state list
# 0 : ALIVE, 1 : DEAD
policy_holders = [0] * N

# define the infinitesimal interval : dt
fps = 100
dt = 1 / fps

# researve which is a list of a pair : (t, _t V)
V = []

# define the list needed for the Manim animation
ph_for_all_fps = [] # the list of policy_holders for all fps
res_for_all_fps = [] # the list of the value of researve for all fps

#initialize researve value
researve = 0

############################################################################
# define the function death_prob(t) which returns the probability that
# a policyholder dies at exact time t
############################################################################

# define mu_40+t which t is not always integers
def mu_40(t):
    floor_t = math.floor(t)
    ceil_t = math.ceil(t)
    
    # If t is an exact integer, return the lookup value directly
    if floor_t == ceil_t:
        return mu_tPLUS40[floor_t]
        
    # Standard linear interpolation: base + fraction * difference
    fraction = t - floor_t
    return mu_tPLUS40[floor_t] + fraction * (mu_tPLUS40[ceil_t] - mu_tPLUS40[floor_t])

# define _tp_x which t is not always integers
def p_40(t):
    # _tp_x = exp(-\int_0^t mu_40+s ds)
    #\int_0^t mu_40+s ds = (mu_40+mu_41)/2 +...+ (mu_{40+floor(t)-1}+mu_{40+floor(t)})/2
    # +(mu_{40+floor(t)} + mu_40(t))/2

    integral = (mu_tPLUS40[math.floor(t)] + mu_40(t)) / 2
    for j in range(math.floor(t)-1):
        term = (mu_tPLUS40[j+1] + mu_tPLUS40[j]) / 2
        integral += term

    return math.exp(integral * (-1))

def death_prob(t):
    # the probability that a policyholder dies at time interval [t, t + 0.01) is
    # approximated by t_p_40 * mu_40+t * 0.01
    return mu_40(t) * dt

# increment the time t in 1/fps steps
for step, t in enumerate(np.linspace(0, 68.99, fps * 69)):

    # premium income
    if step % fps == 0:
        researve += policy_holders.count(0) * P

    # Death processing
    for i in range(N):
        if policy_holders[i] == 0:  # Only check ALIVE policyholders
            x = random.uniform(0, 1)
            if x < death_prob(t):
                policy_holders[i] = 1  # Correctly update state in list
                researve -= 1

    # Earn interest on reserve balance over step dt
    if researve > 0:
        researve *= math.exp(delta * dt)

    V.append((t, researve))
    ph_for_all_fps.append(policy_holders)
    res_for_all_fps.append(researve)


#################################################################
# visualize
#################################################################

########################################
# preparation
########################################

# we visualize random sample which the size N = 100, 10 x 10
# we need t, policy_holders for all t, the value of researve for all t
t = np.linspace(0, 68.99, 69 * fps) # define t once again
# the remaining two lists has defined above

# just visualize the graph (t, _tV)
import matplotlib.pyplot as plt

# Separate the tuples into two lists: t (x-axis) and _tV (y-axis)
t, _tV = zip(*V)

# Create the plot
plt.figure(figsize=(8, 5))
plt.plot(t, _tV, marker='o', linestyle='-', color='b', label='_tV over time')

# Add labels and title
plt.xlabel('Time (t)')
plt.ylabel('Value (_tV)')
plt.title('Plot of _tV vs t')
plt.grid(True)
plt.legend()
plt.show()