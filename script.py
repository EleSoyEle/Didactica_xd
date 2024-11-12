import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,FFMpegWriter,writers
from scipy.constants import G

#Posicion inicial
xi = [0,10]
yi = [0,0]

vxi = [0,0,]
vyi = [0,10]

m = [100000,10]
q = [1,-1]
n = len(m)
assert len(xi)==len(yi)==n==len(vxi)==len(vyi)
h=0.01
traza = 2000

k=9e3

def x_2(xt,yt):
    ax = []
    ay = []
    for i in range(n):
        xa = 0
        ya = 0
        for p in range(0,n):
            if not p==i:
                dx = xt[i]-xt[p]
                dy = yt[i]-yt[p]
                d = pow(dx**2+dy**2,3/2)
                xa += k*q[p]*q[i]*dx/(d*m[i])
                ya += k*q[p]*q[i]*dy/(d*m[i])
        ax.append(xa)
        ay.append(ya)

    return ax,ay

def x_1(xt,yt,xt1,yt1):
    ax = []
    ay = []
    x2a,y2a = x_2(xt,yt)
    for i in range(n):
        ax.append(xt1[i]+h*x2a[i])
        ay.append(yt1[i]+h*y2a[i])
    return ax,ay

def x_0(xt,yt,vx,vy):
    ax = []
    ay = []
    for i in range(n):
        ax.append(xt[i]+h*vx[i])
        ay.append(yt[i]+h*vy[i])
    
    return ax,ay


x = [xi]
y = [yi]

vx = [vxi]
vy = [vyi]

fig = plt.figure()
plt.style.use("dark_background")
ax = fig.add_subplot()
inter = 10
def animate(i):
    global x, y, vx, vy,lx,ly,lvx,lvy
    print(i)
    for i in range(inter):
        vxt,vyt = x_1(x[-1],y[-1],vx[-1],vy[-1])
        xt,yt = x_0(x[-1],y[-1],vxt,vyt)
        x.append(xt)
        y.append(yt)
        vx.append(vxt)
        vy.append(vyt)

    del x[-9:-1],y[-9:-1]
    del vx[-9:-1],vy[-9:-1]
    
    xa = np.array(x)
    ya = np.array(y)
    ax.clear()
    #ax.set_xlim(-40+x[-1][2],40+x[-1][2])
    #ax.set_ylim(-40+y[-1][2],40+y[-1][2])
    for i in range(n):
        ax.plot(xa[-traza:,i],ya[-traza:,i],c="w",linewidth=0.5)
    ax.scatter(xt,yt,s=np.sqrt(m),c="w")

ani = FuncAnimation(fig,animate,frames=5000,interval=0.1)
#ffmpeg_writer = writers['ffmpeg']
#writer = ffmpeg_writer(fps=64, codec='mpeg4')
#ani.save("video1.mp4", writer=writer,dpi=400)
plt.show()
