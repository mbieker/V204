# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 22:54:05 2013

@author: martin
"""

from pylab import *
from scipy import  *

run1 = loadtxt('Messwerte/run1', unpack='true')

run1[0] *= 5  # Abtastrate von 1 Meswert pro 5sec
liney = linspace(20,50)
linex = 700*ones(50)
print([len(linex),len(liney)])
#Set Up Plot
xlabel(r'Zeit - [s]')
ylabel(r'Temperatur - [$^\circ C$]')
plot(run1[0],run1[1] ,label = "T1 - Messingstab (breit)")
plot(run1[0], run1[2], label= "T4 - Messingstab (schmal)")
plot(linex,liney,'r--')
legend(loc='lower right')
show()
savefig('Diagramme/Abb1.eps')
close()
#Set Up Plot
xlabel(r'Zeit [s]')
ylabel(r'Temperatur - [$^\circ C$]')
plot(run1[0],run1[3] ,'y',label = "T5 - Aluminium")
plot(run1[0], run1[4],'', label= "T8 - Edelstal")
plot(linex,liney,'r--')
legend(loc='lower right')
show()
savefig('Diagramme/Abb2.eps')

close()
for i in range(0,5):    
    print(run1[i][139])
    
    