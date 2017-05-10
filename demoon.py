#!/usr/bin/python
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy


G = 6.67408*10**-11
step = 200
endtime = 2368140
N = 4.5*10**16

# UNITS KM, KG, N, S

class Body(object):
    def __init__(self, pos0, mass0, V0, R0):
        self.pos = pos0
        self.mass = mass0
        self.V = V0
        self.R = R0
    def __call__(self):
        print self.pos, self.mass, self.V

def DistBetween(obj1, obj2):
    return math.sqrt((obj1.pos[0]-obj2.pos[0])**2+(obj1.pos[1]-obj2.pos[1])**2)


Earth = Body([0,0], 5.97237*10**24, [0,0], 6371)
Moon = Body([0,405400], 7.341*10**22, [0.963553002013,0], 1737)

Anim = [plt.Circle((Moon.pos[0], Moon.pos[1]), Moon.R, color='grey')]
Moonposplot = [Moon.pos]

for t in numpy.linspace(0,endtime,endtime/step):
    Dist = DistBetween(Earth, Moon)
    MoonToEarth = numpy.divide([Earth.pos[0]-Moon.pos[0], Earth.pos[1]-Moon.pos[1]], Dist)
    FgravMag = G*Earth.mass*Moon.mass/(Dist*10**3)**2
    FgravVct = numpy.multiply(MoonToEarth, FgravMag)
    if t >= 180.0:
        Fr = [0,0]
    else:
        Mvvct = numpy.divide(Moon.V, math.sqrt(Moon.V[0]**2+Moon.V[1]**2))
        Fr = numpy.multiply(Mvvct,-1) * 5885000 * N
    Ftot = numpy.add(FgravVct, Fr)
    A = (numpy.divide(Ftot,Moon.mass)/1000)
    Moon.V = [Moon.V[0] + A[0]*step, Moon.V[1] + A[1]*step]
    Moon.pos = [Moon.pos[0] + Moon.V[0]*step, Moon.pos[1] + Moon.V[1]*step]
    Moonposplot.append(Moon.pos)
    Anim.append(plt.Circle((Moon.pos[0], Moon.pos[1]), Moon.R, color='grey'))

Moon()

Ecircle = plt.Circle((Earth.pos[0], Earth.pos[1]), Earth.R, color='g')
Mcircle = plt.Circle((Moon.pos[0], Moon.pos[1]), Moon.R, color='grey')
Esphere = plt.Circle((Earth.pos[0], Earth.pos[1]), Earth.R+10000, color=(0,0,0.5,0.1))
Thsphere = plt.Circle((Earth.pos[0], Earth.pos[1]), Earth.R+700, color=(0,0,0.6,0.15))
Msphere = plt.Circle((Earth.pos[0], Earth.pos[1]), Earth.R+80, color=(0,0,0.7,0.2))
Ssphere = plt.Circle((Earth.pos[0], Earth.pos[1]), Earth.R+50, color=(0,0,0.8,0.25))
Trsphere = plt.Circle((Earth.pos[0], Earth.pos[1]), Earth.R+12, color=(0,0,0.9,0.3))

fig = plt.figure()
ax = plt.axes(xlim=(-415.4*10**3, 415.4*10**3),ylim=(-415.4*10**3, 415.4*10**3))
line, = ax.plot(map(list, zip(*Moonposplot))[0],map(list, zip(*Moonposplot))[1], lw=0.5)

def init():
    ax.add_artist(Esphere)
    ax.add_artist(Thsphere)
    ax.add_artist(Msphere)
    ax.add_artist(Ssphere)
    ax.add_artist(Trsphere)
    ax.add_artist(Ecircle)
    ax.add_artist(Mcircle)
    return Mcircle, Esphere, Thsphere, Msphere, Ssphere, Trsphere, Ecircle, line

def anim(i):
    Mcircle.center = (Moonposplot[i][0], Moonposplot[i][1])
    return Mcircle, Esphere, Thsphere, Msphere, Ssphere, Trsphere, Ecircle, line

ani = animation.FuncAnimation(fig, anim, init_func=init, frames=int(endtime/step), interval=1, blit=True)
plt.show()
