# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 18:23:51 2020

@author: Kristian
"""

import numpy, pylab
import matplotlib
from numpy import pi

h = 0.01                                # Tidstrinn (s)
g = 9.8                                 # Gravitasjons kraft (m/s^2)
tetthet = 1.2                           # Luft tetthet (kg/m^3)

m = 45.93e-3                            # Masse golf ball (kg)
d = 42.67e-3                            # Diameter golf ball (m)
A = pi*(d/2.)**2                        # Areal golf ball (m^2)

x0 = 0.0                                # Start langs x-koordinat (m)
y0 = 0.0                                # start langs y-koordinat (m)

v0 = 70.0                               # Hastighet golf ball (m/s)
theta0 = numpy.radians(15)              # Utskytnings vinkel (radianer)

vx0 = v0 * numpy.cos(theta0)            # Start hastighet i x-retning (m/s)
vy0 = v0 * numpy.sin(theta0)            # Start hastighet i y-retning (m/s)

#Sjekker om rotasjons raten er innenfor lovlig verdi. 

def get_spin_rotation(omega,hastighet):
    R = omega*(d/2.)/hastighet
    if R < 0.05 or R > 2:
        raise ValueError( "Spin ratio utenfor tillat verdi: %f" % (R,))
    else:
        return R
""" 

def get_spin_rotation(omega,hastighet):
    R = omega*(d/2.)/hastighet
    return R

Fjern de tre (") før def og etter return R for å kjøre utenfor tillat verdi.
Husk å kommenter ut funksjonen som er lik som inneholder if R < 0.05 or R > 2 
hvis denne ikke kommenteres ut vil programmet ikke kjøre riktig.
Hvs bruk av den andre så er ikke resultatene helt korekte da Drag og Lift vil få andre koeffisienter
"""

def get_drag(omega,hastighet):
    R = get_spin_rotation(omega,hastighet)
    return 0.1403 - 0.3406*R*numpy.log(R) + 0.3747*R**1.5

def get_lift(omega,hastighet):
    R = get_spin_rotation(omega,hastighet)
    return 0.3996 + 0.1583 * numpy.log(R) + 0.03790*R**(-0.5)

def get_trajectory(opm):
    
#lagrer verdiene i en liste
    omega = 2*pi * opm / 60.                # rotasjons fart (radianer/s)
    x = [x0, vx0*h + x0]                    # lengde i x- rettning (m)
    y = [y0, vy0*h + y0]                    # høyde målt i (m)
    
    while y[-1]>0:
        
        # Får de forskjellige fartene ved (sjekker at forrige punkt er over 0)
        
        xneste = (x[-1]-x[-2]) / h
        yneste = (y[-1]-y[-2]) / h
        hastighet = numpy.sqrt (xneste**2 + yneste**2)
        
        Cd = get_drag(omega,hastighet)
        Cl = get_lift(omega,hastighet)
        
        xnext_m_drag = -tetthet*A*hastighet/(2*m)*(Cd*xneste+Cl*yneste)*h**2 + 2*x[-1] - x[-2]
        ynext_m_drag = -(g+tetthet*A*hastighet/(2*m)*(Cd*yneste-Cl*xneste))*h**2 + 2*y[-1] - y[-2]
        
        x.append(xnext_m_drag)
        y.append(ynext_m_drag)
        
    # Konverterer liste til array
    
    return numpy.array(x), numpy.array(y), numpy.amax(y)

""" 
Endre verdiene under for å undersøke andre resultater! 
Husk noen verdier virker bare avhengi av hvilken get_spinn_rotation funksjon som er i bruk 
"""

opm_1 = 2000
opm_2 = 4000


x1,y1,top1 = get_trajectory(opm_1)
x2,y2,top2 = get_trajectory(opm_2)

# hard koder inn print top punkt (det ble sent)
def hvor_langt(akse):
    lengde = akse[akse != 0]
    print ("Lengden blir %.2f"%(lengde.max()))
    
#pointofint = x1[x1 != 0]
#print(pointofint.max())


# kurve for ball uten luftmotstand

x3 = numpy.arange(0,1000.)
y3 = y0 + (vy0/vx0)*(x3-x0) - g/(2*vx0**2)*(x3-x0)**2

# Beholder bare positive verdier

x3 = x3.compress(y3>=0.)
y3 = y3.compress(y3>=0.)

# Plotter graf

pylab.plot(x1,y1,label="%.0f opm"%(opm_1))
pylab.plot(x2,y2,label="%.0f opm"%(opm_2))
pylab.plot(x3,y3,label="Golf ball i vakuum")

pylab.xlabel("Lengde (m)")
pylab.ylabel("Høyde (m)")

font = matplotlib.font_manager.FontProperties(size="small")
legend = pylab.legend(loc="upper left",prop=font)
legend.draw_frame(False)

# Setter limit på høyde etter hva top punk ble i print

pylab.ylim(0,50)


pylab.show()

hvor_langt(x1)
print("Topp for %.f OPM %.2f" %(opm_1, top1))
hvor_langt(x2)
print("Topp for %.f OPM %.2f"%(opm_2, top2))
