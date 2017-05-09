#!/usr/bin/python
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy

#plt.plot([1,2,3,4,5])
#plt.show()
#xyz

G = 6.67408*10**-11

step = 0.1
endtime = 3000

# UNITS KM, KG

class Body(object):
    def __init__(self, pos0, mass0, V0, R0):
        self.pos = pos0
        self.mass = mass0
        self.V = V0
        self.R = R0
    def __call__(self):
        print self.pos, self.mass, self.V

def DistBetween(obj1, obj2):
    #print obj1.pos[2]
    return math.sqrt((obj1.pos[0]-obj2.pos[0])**2+(obj1.pos[1]-obj2.pos[1])**2)

Earth = Body([0,0], 5.97237*10**24, [0,0], 6371)
Moon = Body([0,405.4*10**3], 7.341*10**22, [5,0], 1737)

Moonposplot = [Moon.pos]


#print A

#print MoonToEarth, FgravMag, FgravVct, A 

for t in numpy.linspace(0,endtime,num=(endtime+2*step)/step):
    #print Earth.pos, Moon.pos
    MoonToEarth = numpy.divide([Earth.pos[0]-Moon.pos[0], Earth.pos[1]-Moon.pos[1]], DistBetween(Earth, Moon))
    FgravMag = G*Earth.mass*Moon.mass/(DistBetween(Earth, Moon)*10**3)**2
    FgravVct = numpy.multiply(MoonToEarth, FgravMag)
    A = numpy.divide(FgravVct,Moon.mass)
    Moon.V = [Moon.V[0] + A[0], Moon.V[1] + A[1]]
    Moon.pos = [Moon.pos[0] + Moon.V[0]/step, Moon.pos[1] + Moon.V[1]/step]
    #print MoonToEarth, FgravVct, Moon.pos, A
    Moonposplot.append(Moon.pos)

Earth()
#print Moonposplot

Ecircle = plt.Circle((Earth.pos[0], Earth.pos[1]), Earth.R, color='g')
Mcircle = plt.Circle((Moon.pos[0], Moon.pos[1]), Moon.R, color='grey')
Esphere = plt.Circle((Earth.pos[0], Earth.pos[1]), Earth.R+10000, color=(0,0,0.5,0.5))
Thsphere = plt.Circle((Earth.pos[0], Earth.pos[1]), Earth.R+700, color=(0,0,0.6,0.5))
Msphere = plt.Circle((Earth.pos[0], Earth.pos[1]), Earth.R+80, color=(0,0,0.7,0.5))
Ssphere = plt.Circle((Earth.pos[0], Earth.pos[1]), Earth.R+50, color=(0,0,0.8,0.5))
Trsphere = plt.Circle((Earth.pos[0], Earth.pos[1]), Earth.R+12, color=(0,0,0.9,0.5))

fig = plt.figure()
ax = fig.add_subplot(111)#, projection='3d')
ax.plot(map(list, zip(*Moonposplot))[0],map(list, zip(*Moonposplot))[1])
ax.add_artist(Esphere)
ax.add_artist(Thsphere)
ax.add_artist(Msphere)
ax.add_artist(Ssphere)
ax.add_artist(Trsphere)

ax.add_artist(Ecircle)
ax.add_artist(Mcircle)
ax.set_xlim(-415.4*10**3, 415.4*10**3)
ax.set_ylim(-415.4*10**3, 415.4*10**3)
plt.show()
