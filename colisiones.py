import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation,FFMpegWriter,writers


g = 9.8
l=7
theta_i = float(input("Ingresa el angulo inicial de theta: "))
dtheta_i = 0
phi_i = float(input("Ingresa el angulo inicial de phi: "))
dphi_i = 0

ti = 0
h=0.005
k=0.01
n=7
m=10
p = 0

vmax = 0.5

def dtheta2(theta,dtheta,phi,dphi,t):
    dif = (phi-theta)/2
    return -g/l*np.sin(theta)+k*np.cos(dif)/(2*m*l**2*(2*l*np.sin(dif))**(n+1))-p*dtheta

def dtheta1(theta,dtheta,phi,dphi,t):
    return dtheta 


def dphi2(theta,dtheta,phi,dphi,t):
    dif = (phi-theta)/2
    return -g/l*np.sin(phi)-k*np.cos(dif)/(2*m*l**2*(2*l*np.sin(dif))**(n+1))-p*dphi

def dphi1(theta,dtheta,phi,dphi,t):
    return dphi


def calc_rk_coefs(theta,dtheta,phi,dphi,t):
    k1thetav = dtheta2(theta,dtheta,phi,dphi,t)
    k1thetax = dtheta1(theta,dtheta,phi,dphi,t)
    k1phiv = dphi2(theta,dtheta,phi,dphi,t)
    k1phix = dphi1(theta,dtheta,phi,dphi,t)

    k2thetav = dtheta2(theta+h*k1thetax/2,dtheta+h*k1thetav/2,phi+h*k1phix/2,dphi+h*k1phiv/2,t+h/2)
    k2thetax = dtheta1(theta+h*k1thetax/2,dtheta+h*k1thetav/2,phi+h*k1phix/2,dphi+h*k1phiv/2,t+h/2)
    k2phiv = dphi2(theta+h*k1thetax/2,dtheta+h*k1thetav/2,phi+h*k1phix/2,dphi+h*k1phiv/2,t+h/2)
    k2phix = dphi1(theta+h*k1thetax/2,dtheta+h*k1thetav/2,phi+h*k1phix/2,dphi+h*k1phiv/2,t+h/2)

    k3thetav = dtheta2(theta+h*k2thetax/2,dtheta+h*k2thetav/2,phi+h*k2phix/2,dphi+h*k2phiv/2,t+h/2)
    k3thetax = dtheta1(theta+h*k2thetax/2,dtheta+h*k2thetav/2,phi+h*k2phix/2,dphi+h*k2phiv/2,t+h/2)
    k3phiv = dphi2(theta+h*k2thetax/2,dtheta+h*k2thetav/2,phi+h*k2phix/2,dphi+h*k2phiv/2,t+h/2)
    k3phix = dphi1(theta+h*k2thetax/2,dtheta+h*k2thetav/2,phi+h*k2phix/2,dphi+h*k2phiv/2,t+h/2)

    k4thetav = dtheta2(theta+h*k3thetax,dtheta+h*k3thetav,phi+h*k3phix,dphi+h*k3phiv,t+h)
    k4thetax = dtheta1(theta+h*k3thetax,dtheta+h*k3thetav,phi+h*k3phix,dphi+h*k3phiv,t+h)
    k4phiv = dphi2(theta+h*k3thetax,dtheta+h*k3thetav,phi+h*k3phix,dphi+h*k3phiv,t+h)
    k4phix = dphi1(theta+h*k3thetax,dtheta+h*k3thetav,phi+h*k3phix,dphi+h*k3phiv,t+h)

    ntheta = theta + h*(k1thetax+2*k2thetax+2*k3thetax+k4thetax)/6
    ndtheta = dtheta + h*(k1thetav+2*k2thetav+2*k3thetav+k4thetav)/6
    #Para evitar un desborde en la velocidad de theta
    if not (-vmax<=ndtheta and ndtheta<=vmax):
        ndtheta = vmax if ndtheta>0 else -vmax

    nphi = phi + h*(k1phix+2*k2phix+2*k3phix+k4phix)/6
    ndphi = dphi + h*(k1phiv+2*k2phiv+2*k3phiv+k4phiv)/6
    #Para evitar un desborde en la velocidad de phi
    if not (-vmax<=ndphi and ndphi<=vmax):
        ndphi = vmax if ndphi>0 else -vmax

    return ntheta,ndtheta,nphi,ndphi


fig = plt.figure()
ax = fig.add_subplot()


def animate(i):
    global theta_i,dtheta_i,phi_i,dphi_i

    print(i)
    theta_i,dtheta_i,phi_i,dphi_i = calc_rk_coefs(theta_i,dtheta_i,phi_i,dphi_i,ti)

    x1 = l*np.sin(theta_i)
    y1 = -l*np.cos(theta_i)
    x2 = l*np.sin(phi_i)
    y2 = -l*np.cos(phi_i)

    
    ax.clear()
    ax.set_xlim(-10,10)
    ax.set_ylim(-10,10)
    ax.plot((0,x1),(0,y1))
    ax.plot((0,x2),(0,y2))
    ax.scatter((x1,x2),(y1,y2))


ani = FuncAnimation(fig,animate,frames=1000,interval=0.001)
#ffmpeg_writer = writers['ffmpeg']
#writer = ffmpeg_writer(fps=32, codec='mpeg4')
#ani.save("colision.mp4", writer=writer,dpi=500)
plt.show()