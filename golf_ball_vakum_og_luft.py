# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 18:15:22 2020

@author: Kristian
"""

import numpy, pylab
import matplotlib
h = 0.01 # Time step (s)
g = 9.8 # Gravity (m/s^2)
dens = 1.2 # Air density (kg/m^3)
m = 45.93e-3 # Mass of golf ball (kg)
d = 42.67e-3 # Ball diameter (m)
A = numpy.pi*(d/2.)**2 # Cross-sectional area of golf ball (m^2)
x0 = 0.0 # Initial horizontal distance (m)
z0 = 0.0 # Initial altitude (m)
V0 = 70.0 # Launch speed (m/s)
theta0 = numpy.radians(15) # Launch angle (radians)
u0 = V0 * numpy.cos(theta0) # Initial horizontal speed (m/s)
w0 = V0 * numpy.sin(theta0) # Initial vertical speed (m/s)
# Perform the finite difference calculation
def get_trajectory(Vc):
# Create lists to store the trajectory
x = [x0, u0*h + x0] # Horizontal distances (m)
z = [z0, w0*h + z0] # Altitudes (m)
while z[-1] > 0:
# Get the speeds
u = (x[-1]-x[-2]) / h
w = (z[-1]-z[-2]) / h
V = numpy.sqrt(u**2 + w**2)
# Determine the drag coefficient
if V<Vc:
Cd = 0.5
else:
Cd = max(0.5*Vc/V,0.25)
# Determine the next point in the trajectory
xnext = -dens*A*V/(2*m)*Cd*u*h**2 + 2*x[-1] - x[-2]
znext = -(g+dens*A*V/(2*m)*Cd*w)*h**2 + 2*z[-1] - z[-2]
# Store the values
x.append(xnext)
z.append(znext)
# Convert lists to arrays and return
return numpy.array(x), numpy.array(z)
# Get trajectories for different Vc values
x1,z1 = get_trajectory(100.) # Smooth ball
x2,z2 = get_trajectory(14.) # Golf ball
# Get the trajectory without drag for comparison
x3 = numpy.arange(0,300.)
z3 = z0 + (w0/u0)*(x3-x0) - g/(2*u0**2)*(x3-x0)**2
# Select above-ground points only
x3 = x3.compress(z3>=0.)
z3 = z3.compress(z3>=0.)
# Plotting
pylab.plot(x1,z1,label=’Smooth sphere’)
pylab.plot(x2,z2,label=’Golf ball’)
pylab.plot(x3,z3,label=’Vacuum’)
pylab.xlabel(’x’)
pylab.ylabel(’z’)
font = matplotlib.font_manager.FontProperties(size=’small’)
legend = pylab.legend(loc=’upper left’,prop=font)
legend.draw_frame(False)
pylab.ylim(0.,25.)
pylab.subplots_adjust(left=0.3,right=0.7,top=0.7,bottom=0.3)
pylab.show()
