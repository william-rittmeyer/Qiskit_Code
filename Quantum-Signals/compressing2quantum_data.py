import qiskit
import math
import matplotlib.pyplot

# importing Qiskit
from qiskit import Aer, IBMQ
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute
x = 9  # of x bits
y = 9  # of y bits
a = x-1  # of working bits   this is x bits minus 1

N = x + y+ a # of number of qubits


qr = QuantumRegister(N)
cr = ClassicalRegister(N)
circuit = QuantumCircuit(qr,cr)

%matplotlib inline

def superposition():
    for p in range(N-x,N):
        circuit.h(qr[p])

def x_bits(p): #p is number of bits in x
    b = bin(p)[2:]
    t = len(b)

    for i in range(1,t+1):     #create x gates from inputting x bits
        
        if b[-i]=='0':
            circuit.x(qr[N-x-1+i])
            
    for i in range(1,x-t+1):   #inputs 0s for rest of bits
        circuit.x(qr[N-x-1+t+i])

def working_up(p,a):
    b = bin(p)[2:]
    t = len(b)
    
    if x>2:
        circuit.ccx(qr[N-1],qr[N-2],qr[y+a-1])    
        for i in range(1,a):
            circuit.ccx(qr[N-2-i],qr[y+a-i],qr[y+a-i-1])

def working_down(p,a):
    b = bin(p)[2:]
    t = len(b)
    
    if x>2:  
        for i in range(1,a):
            circuit.ccx(qr[y+a-1+i],qr[y+i],qr[y-1+i])
            
        circuit.ccx(qr[N-1],qr[N-2],qr[y+a-1])    

def plot(x_point,y_point):
    x_bits(x_point)
    circuit.barrier()
    
    y_binary = bin(y_point)[2:]
    t = len(y_binary)
    
    working_up(x_point,a)
    for j in range(1,t+1): 
        if y_binary[-j]=='1':
            circuit.cx(qr[y],qr[j-1])
            
            
    working_down(x_point,a)
    circuit.barrier()
    x_bits(x_point)
    circuit.barrier()
    

superposition()

for r in range(0,255):
    
    plot(r,round(60*math.sin(.03*r)+65))
    
    

for r in range(0,127):
    
    plot(2*r,15)
    plot(2*r+1,5)

circuit.measure(qr,cr)
simulator = Aer.get_backend('qasm_simulator')
result = execute(circuit,backend = simulator).result()
from qiskit.tools.visualization import plot_histogram
#plot_histogram(result.get_counts())


def quantum_plot():

    A = result.get_counts()
    K = list(A.keys())
    point = []
    y_plots = []
    
    for i in range(0,31):
        point.append((int(K[i][:x],2),int(K[i][x+a:],2)))
    
    point.sort(key=lambda tup: tup[0])
    x_val= [x_val[0] for x_val in point]
    y_val= [x_val[1] for x_val in point]
    
    matplotlib.pyplot.plot(x_val,y_val)
    display(point)
    
    
quantum_plot()


A = result.get_counts()
K = list(A.keys())
