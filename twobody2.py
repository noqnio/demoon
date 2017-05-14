#!/usr/bin/python
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy


G = 6.67408*10**-11
step = 200
endtime = 23681400

# UNITS KM, KG, N, S

class Body(object):
    def __init__(self, Pos0, mass0, V0, A0, R0, F0=[0,0]):
        self.Pos = Pos0
        self.mass = mass0
        self.V = V0
        self.A = A0
        self.R = R0
        self.F = F0
    def __call__(self):
        print self.Pos, self.V, self.A, self.F
    def updateAcc(self):
        self.A = numpy.divide(self.F, self.mass)/1000
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
def SpdUnitDirVct(body1):
    return numpy.divide(body1.V, math.sqrt(body1.V[0]**2+body1.V[1]**2))
def FgravMag(body1, body2):
    return G*body1.mass*body2.mass/(DistBetween(body1, body2)*10**3)**2
def FgravVct(body1, body2):
    return numpy.multiply(PosUnitDirVct(body1, body2), FgravMag(body1, body2))

Earth = Body([0,0], 5*10**24, [1.6,0], [0,0], 5000)
Moon = Body([0,100000], 5*10**24, [-1.604,0], [0,0], 5000)

Moonposplot = [Moon.Pos]
Earthposplot = [Earth.Pos]

for t in numpy.linspace(0,endtime,endtime/step):
    Moon.F = FgravVct(Moon, Earth)
    Earth.F = FgravVct(Earth, Moon)
    Moon.Move(step)
    Earth.Move(step)
    Moonposplot.append(Moon.Pos)
    Earthposplot.append(Earth.Pos)

Ecircle = plt.Circle((Earth.Pos[0], Earth.Pos[1]), Earth.R, color='g')
Mcircle = plt.Circle((Moon.Pos[0], Moon.Pos[1]), Moon.R, color='grey')

fig = plt.figure()
ax = plt.axes(xlim=(-200*10**3, 200*10**3),ylim=(-150*10**3, 250*10**3))
Mline, = ax.plot(map(list, zip(*Moonposplot))[0],map(list, zip(*Moonposplot))[1], lw=0.5)
Eline, = ax.plot(map(list, zip(*Earthposplot))[0],map(list, zip(*Earthposplot))[1], lw=0.5)

def init():
    ax.add_artist(Ecircle)
    ax.add_artist(Mcircle)
    return Mcircle, Ecircle

def anim(i):
    Mcircle.center = (Moonposplot[i][0], Moonposplot[i][1])
    Ecircle.center = (Earthposplot[i][0], Earthposplot[i][1])
    return Mcircle, Ecircle, Mline, Eline

ani = animation.FuncAnimation(fig, anim, init_func=init, frames=int(endtime/step), interval=1, blit=True)
plt.show()
