# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 18:23:51 2020

@author: Kristian
"""

import numpy, pylab
import matplotlib

h = 0.01                                # Tidstrinn (s)
g = 9.8                                 # Gravitasjons kraft (m/s^2)
tetthet = 1.2                           # Luft tetthet (kg/m^3)

m = 45.93e-3                            # Masse golf ball (kg)
d = 42.67e-3                            # Diameter golf ball (m)
A = numpy.pi*(d/2.)**2                  # Areal golf ball (m^2)

x0 = 0.0                                # Start langs x-koordinat (m)
y0 = 0.0                                # start langs y-koordinat (m)

V0 = 70.0                               # Hastighet golf ball (m/s)
theta0 = numpy.radians(15)              # Utskytnings vinkel (radianer)

vx0 = V0 * numpy.cos(theta0)             # Start hastighet i x-retning (m/s)
vy0 = V0 * numpy.sin(theta0)             # Start hastighet i y-retning (m/s)

def get_trajectory(vc):
    
    x = [x0, vx0*h + x0]
    y = [y0, vy0*h + y0]
    
    while y[-1]>0:
        # neste fart x. Parabolic equation 
        # Får de forskjellige fartene ved 
        xnext = (x[-1]-x[-2]) / h
        ynext = (y[-1]-y[-2]) / h
        v = numpy.sqrt (xnext**2 + ynext**2)
        # Setter vedi for drag koeffisient
        if v<vc:
            drag_kof = 0.5
        else:
            drag_kof = max(0.5*vc/v,0.25)
        
        xnext_w_drag = -tetthet*A*v/(2*m)*drag_kof*xnext*h**2 + 2*x[-1] - x[-2]
        ynext_w_drag = -(g+tetthet*A*v/(2*m)*drag_kof*ynext)*h**2 + 2*y[-1] - y[-2]
        
        x.append(xnext_w_drag)
        y.append(ynext_w_drag)
    # Konverterer liste til array
    return numpy.array(x), numpy.array(y)

x1,y1 = get_trajectory(100.)
x2,y2 = get_trajectory(14.)

# kurve for ball uten luftmotstand
x3 = numpy.arange(0,300.)
y3 = y0 + (vy0/vx0)*(x3-x0) - g/(2*vx0**2)*(x3-x0)**2

x3 = x3.compress(y3>=0.)
y3 = y3.compress(y3>=0.)

# plotter graf
pylab.plot(x1,y1,label="Glatt ball")
pylab.plot(x2,y2,label="Golf ball")
pylab.plot(x3,y3,label="Golf ball i vakuum")

pylab.xlabel("Lengde (m)")
pylab.ylabel("Høyde (m)")

font = matplotlib.font_manager.FontProperties(size="small")
legend = pylab.legend(loc="upper left",prop=font)
legend.draw_frame(False)

pylab.ylim(0.,25.)


pylab.show()