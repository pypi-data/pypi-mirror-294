from pygame import *
from math import *
import random
global a,v
a=4000
v=10

    
def new():
    global game
    global R
    global P
    global color
    game=Star()
    surface.fill((0,0,0))
    R=random.randint(20,40)
    P=[random.randint(400,600),random.randint(250,350)]
    color=(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    draw.circle(surface, color, P, R)
    display.flip()

class Planet:
    def __init__(self):
        self.A=[0,0]
        self.V=[random.randint(-v,v), random.randint(-v,v)]
        self.P=[random.randint(250,750), random.randint(225,370)]
        self.existence=True
        self.radius=random.randint(5,20)
        self.color=(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    
    def next(self):
        if not self.P[0]-P[0]==0:
            theta=atan(abs((self.P[1]-P[1])/(self.P[0]-P[0])))
        else:
            theta=pi/2
        self.A[0]=a*(cos(theta))/(dist(P,self.P)**2)
        self.A[1]=a*(sin(theta))/(dist(P,self.P)**2)
        for i in [0,1]:
            if self.P[i]<=P[i]:
                self.A[i]=abs(self.A[i])
            else:
                self.A[i]=-abs(self.A[i])
            self.V[i]=self.V[i]+self.A[i]
            self.P[i]=self.P[i]+self.V[i]
        if  (self.radius+R)>=dist(self.P,P):
            self.existence=False


class Star:
    def __init__(self):
        self.planets=[]

    def new(self):
        self.planets.append(Planet())

    def update(self):
        surface.fill((0,0,0))
        draw.circle(surface, color , P, R)
        for planet in self.planets:
            if planet.existence:
                planet.next()
                x=int(planet.P[0])
                y=int(planet.P[1])
                draw.circle(surface, planet.color, (x,y), planet.radius)
        display.flip()

surface=display.set_mode((1000,600))
clock=time.Clock()
game=Star()
new()
def main():
    while True:
        clock.tick(60)
        game.update()
        for e in event.get():
            if e.type==KEYDOWN:
                if e.key==K_n:
                    new()
                if e.key==K_p:
                    game.new()
                if e.key==K_ESCAPE:
                    quit()
                    return


                
