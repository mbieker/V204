"""
Created on Mon Nov 11 22:54:05 2013

@author: martin
"""

from pylab import *
from scipy import *
from uncertainties import *
import uncertainties.umath as um
import scipy.signal as sig 
def make_LaTeX_table(data,header, flip= 'false', onedim = 'false'):
    output = '\\begin{tabular}{'
    #Get dimensions
    if(onedim == 'true'):
        if(flip == 'false'):
        
            data = array([[i] for i in data])
        
        else:
            data = array([data])
        

    row_cnt, col_cnt = data.shape
    header_cnt = len(header)
    
    if(header_cnt == col_cnt and flip== 'false'):
        #Make Format
        output += '|'
        for i in range(col_cnt):
            output += 'c|'
        output += '}\n\\hline\n'+ header[0]
        for i in range (1,col_cnt):
            output += ' & ' + header[i]
        output += ' \\\\\n\\hline\n'
        for i in data:
            output += str(i[0])
            for j in range(1,col_cnt):
                output += ' & ' + str( i[j])
            output += '\\\\\n'
        output += '\\hline\n\\end{tabular}\n'
                            
        return output
    else:
        if(row_cnt == header_cnt):
            output += '|c|' + (col_cnt)*'c' + '|}\n\\hline\n'
            for i in range(row_cnt):
                output += header[i]
                for j in range(col_cnt):
                    output += ' & ' + str(data[i][j])
                output += '\\\\\n\\hline\n'
                
            output += '\\end{tabular}\n'
            return output
        else:
            return 'ERROR'

    
def err(data):
    mean = data.mean()
    N = len(data)
    err = 0
    for i in data:
        err += (i - mean)**2
    err = sqrt(err/((N-1)*N))
    return ufloat(mean,err)


'''
run1 = loadtxt('Messwerte/run1', unpack='true')
t, T1,T2, T3, T4 = loadtxt('Messwerte/t1t4_run1', unpack="true")
t, T5, T6, T7, T8 = loadtxt('Messwerte/t5t8_run1', unpack = 'true')
run1[0] *= 5 # Abtastrate von 1 Meswert pro 5sec


liney = linspace(20,50)
linex = 700*ones(50)
print([len(linex),len(liney)])
#Set Up Plot
xlabel(r'Zeit - [s]')
ylabel(r'Temperatur - [$^\circ C$]')
plot(t,T1 ,label = "T1 - Messingstab (breit)")
plot(t,T4, label= "T4 - Messingstab (schmal)")
plot(linex,liney,'r--')
legend(loc='lower right')
show()
savefig('Diagramme/Abb1.eps')
close()
#Set Up Plot
xlabel(r'Zeit [s]')
ylabel(r'Temperatur - [$^\circ C$]')
plot(t,T5 ,'y',label = "T5 - Aluminium")
plot(t,T8,'', label= "T8 - Edelstal")
plot(linex,liney,'r--')
legend(loc='lower right')
show()
savefig('Diagramme/Abb2.eps')

close()
for i in range(0,5):
print(run1[i][139])

t, T1,T2, T3, T4 = loadtxt('Messwerte/t1t4_run1', unpack="true")
t, T5, T6, T7, T8 = loadtxt('Messwerte/t5t8_run1', unpack = 'true')
plot(t, T2- run1[1], label ='T2 - T1')
plot(t,T7-run1[4], label='T7-T8')
legend()
show()
'''

def maxmin(x,y, first_max = True):
    out_x = []
    out_y = []
    slope = 0
    old_slope = 0
    last_maximum = not first_max
    if(len(y) != len(x)):
        print("Error!")
        return

    for i in range(20,len(y)-1):
        if(y[i-1] < y[i]):
            slope = 1
        else:
            if(y[i-1] > + y[i]):
                slope = -1
            else:
                slope = 0
        
        if(slope > old_slope and last_maximum ):
            out_x.append(x[i])
            out_y.append(y[i])
            last_maximum = False
        if(slope < old_slope and not last_maximum ):
            out_x.append(x[i])
            out_y.append(y[i])
            last_maximum = True
            
        old_slope = slope
    output = [out_x,out_y]
    return output
    
            
t, T1,T2,T5,T6 = loadtxt('Messwerte/dyn1', unpack='true' )

def flat_maxmin(x,y):
    outputx = []
    outputy = []
    for i in range(25,len(y)-1):
        if(y[i-1]< y[i] and y[i] > y[i+1] or y[i-1]> y[i] and y[i]< y[i+1] ):
            outputx.append(x[i])
            outputy.append(y[i])
    return [outputx,outputy]

t =t*2 # Abtastrate voon 2 s secunden
T1_0= maxmin(t,T1)
T2_0= maxmin(t,T2)
T5_0= maxmin(t,T5)
T6_0= maxmin(t,T6)
"""
print(T1_0)
print(T2_0)

to_table = array([[T1_0[0][i+2],T1_0[1][i+2],T2_0[0][i],T2_0[1][i]] for i in range(0,19)])
print(make_LaTeX_table(to_table, ['cc','cdc','dsf','sdx'], ))

offset = []
for i in range(0,19):
    offset.append( T1_0[0][i+2]-T2_0[0][i])

offset = err(array(offset))
print('Phasenverschiebung Messing: %s' % offset)
waveleng = 0.03* 80/offset
print('Wellenlaenge Messing: %s' % waveleng)
amplitude = []
for i in range (3,len(T1_0[0])):
    amplitude.append(abs(T1_0[1][i-1]-T1_0[1][i]))
amplitude_f = 0.5* err(array(amplitude))
print('Amlitude fern : %s' % amplitude_f)
waveleng = 0.03* 80/offset
amplitude = []
for i in range (0,len(T2_0[0])):
    amplitude.append(abs(T2_0[1][i-1]-T2_0[1][i]))
amplitude_n = 0.5* err(array(amplitude))
print('Amlitude nah : %s' % amplitude_n)

kappa = 8520*385*(0.03)**2/(2*offset* um.math.log(amplitude_n.nominal_value/amplitude_f.nominal_value))
print('Kappa Messing = %s' % kappa)
"""
"""

print(T5_0)
print(T6_0)

to_table = array([[T6_0[0][i],T6_0[1][i],T5_0[0][i],T5_0[1][i]] for i in range(0,19)])
print(make_LaTeX_table(to_table, ['cc','cdc','dsf','sdx'], ))

offset = []
for i in range(0,19):
    offset.append( T5_0[0][i]-T6_0[0][i])

offset = err(array(offset))
print('Phasenverschiebung Alu: %s' % offset)
waveleng = 0.03* 80/offset
print('Wellenlaenge Alu: %s' % waveleng)
amplitude = []
for i in range (1,19):
    amplitude.append(abs(T5_0[1][i-1]-T5_0[1][i]))
amplitude_f = 0.5* err(array(amplitude))
print('Amlitude fern : %s' % amplitude_f)
waveleng = 0.03* 80/offset
amplitude = []
for i in range (0,19):
    amplitude.append(abs(T6_0[1][i-1]-T6_0[1][i]))
amplitude_n = 0.5* err(array(amplitude))
print('Amlitude nah : %s' % amplitude_n)

kappa = 2800*830*(0.03)**2/(2*offset* um.math.log(amplitude_n.nominal_value/amplitude_f.nominal_value))
print('Kappa Alu = %s' % kappa)
"""
plot(T1_0[0],T1_0[1], 'x' )
plot(T2_0[0],T2_0[1], 'o')
plot(t,T1, label='Messing fern')
plot(t,T2, label= 'Messing nah')
xlabel(r'Zeit - [s]')
ylabel(r'Temperatur - [$^\circ C$]')
legend()
show()
savefig('Diagramme/dyn_messing.png')
close()
plot(T5_0[0],T5_0[1], 'x' )
plot(T6_0[0],T6_0[1], 'o')
plot(t,T5, label='Aluminium fern')
plot(t,T6, label= 'Aluminium nah')
xlabel(r'Zeit - [s]')
ylabel(r'Temperatur - [$^\circ C$]')
legend()
savefig('Diagramme/dyn_alu.png')
close()
t,T7,T8 = loadtxt('Messwerte/dyn2', unpack='true')
t*= 2
T7_0 = maxmin(t,T7)


for i in sig.argrelextrema(T8,np.greater):
    print(t[i],T8[i])

#plot(t,T7, label="Edelstahl nah")
#plot(T7_0[0],T7_0[1],'x')
plot(t,T8, label= "Edelstahl fern")
plot(T8_0[0],array(T8_0[1]) ,'o')
xlabel(r'Zeit - [s]')
ylabel(r'Temperatur - [$^\circ C$]')
legend()
savefig('Diagramme/dyn_stahl.png')
