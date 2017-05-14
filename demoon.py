#!/usr/bin/python
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy


G = 6.67408*10**-11
step = 60
endtime = 950000 #2368140
N = 5*10**16
F9thrust = 5885000

# UNITS KM, KG, N, S

class Body(object):
    def __init__(self, Pos0, Mass0, V0, A0, R0, F0=[0,0]):
        self.Pos = Pos0
        self.Mass = Mass0
        self.V = V0
        self.A = A0
        self.R = R0
        self.F = F0
    def __call__(self):
        print self.Pos, self.V, self.A, self.F
    def updateAcc(self):
        self.A = numpy.divide(self.F, self.Mass)/10**3
    def updateVel(self, time):
        self.V = [self.V[0] + self.A[0]*time, self.V[1] + self.A[1]*time]
    def updatePos(self, time):
        self.Pos = [self.Pos[0] + self.V[0]*time, self.Pos[1] + self.V[1]*time]
    def Move(self, time):
        self.updateAcc()
        self.updateVel(time)
        self.updatePos(time)


def DistBetween(body1, body2):
    return math.sqrt((body1.Pos[0]-body2.Pos[0])**2+(body1.Pos[1]-body2.Pos[1])**2)
def PosUnitDirVct(body1, body2):
    return numpy.divide([body2.Pos[0]-body1.Pos[0], body2.Pos[1]-body1.Pos[1]], DistBetween(body1, body2))
def VelUnitDirVct(body):
    return numpy.divide(body.V, math.sqrt(body.V[0]**2+body.V[1]**2))
def FgravMag(body1, body2):
    return G*body1.Mass*body2.Mass/(DistBetween(body1, body2)*10**3)**2
def FgravVct(body1, body2):
    return numpy.multiply(PosUnitDirVct(body1, body2), FgravMag(body1, body2))


Earth = Body([0,0], 5.97237*10**24, [0,0], [0,0], 6371)
Moon = Body([0,405400], 7.341*10**22, [0.963553002013,0], [0,0], 1737)

Moonposplot = [Moon.Pos]

for t in numpy.linspace(0,endtime,endtime/step):
    if t >= 180:
        Moon.F = FgravVct(Moon, Earth)
    else:
        Fr = numpy.multiply(VelUnitDirVct(Moon),-1) * F9thrust * N
        Moon.F = numpy.add(FgravVct(Moon, Earth), Fr)
    Moon.Move(step)
    Moonposplot.append(Moon.Pos)

Ecircle = plt.Circle((Earth.Pos[0], Earth.Pos[1]), Earth.R, color='g')
Mcircle = plt.Circle((Moon.Pos[0], Moon.Pos[1]), Moon.R, color='grey')
Esphere = plt.Circle((Earth.Pos[0], Earth.Pos[1]), Earth.R+10000, color=(0,0,0.5,0.1))
Thsphere = plt.Circle((Earth.Pos[0], Earth.Pos[1]), Earth.R+700, color=(0,0,0.6,0.15))
Msphere = plt.Circle((Earth.Pos[0], Earth.Pos[1]), Earth.R+80, color=(0,0,0.7,0.2))
Ssphere = plt.Circle((Earth.Pos[0], Earth.Pos[1]), Earth.R+50, color=(0,0,0.8,0.25))
Trsphere = plt.Circle((Earth.Pos[0], Earth.Pos[1]), Earth.R+12, color=(0,0,0.9,0.3))

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
