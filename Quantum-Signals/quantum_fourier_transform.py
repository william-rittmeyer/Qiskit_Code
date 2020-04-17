import math

# importing Qiskit
from qiskit import Aer, IBMQ
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute

from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
from qiskit.tools.visualization import plot_histogram

def input_state(circ, q, n):
    """n-qubit input state for QFT that produces output 1."""
    for j in range(n):
        circ.h(q[j])
        circ.u1(-math.pi/float(2**(j)), q[j])
        
def qft(circ, q, n):
    """n-qubit QFT on q in circ."""
    for j in range(n):
        circ.h(q[j])
        for k in range(j+1,n):
            circ.cu1(math.pi/float(2**(k-j)), q[k], q[j])
        circ.barrier()


q = QuantumRegister(4, 'x')
c = ClassicalRegister(3, 'c')
qft3 = QuantumCircuit(q, c)

qft3.h(q[0])
qft3.h(q[1])

qft3.ccx(q[2],q[1],q[0])

qft3.x(q[0])
qft3.x(q[2])

qft3.ccx(q[2],q[1],q[0]) #001 is with 101  (0,5)




# first, prepare the state that should return 001 and draw that circuit

qft3.draw(output='mpl')


# next, do a qft on the prepared state and draw the entire circuit
qft(qft3, q, 3)
for i in range(3):
    qft3.measure(q[i], c[i])
    
qft3.draw(output='mpl')


# run on local simulator
from qiskit.tools.visualization import plot_histogram

backend = Aer.get_backend("qasm_simulator")

simulate = execute(qft3, backend=backend, shots=1024).result()
plot_histogram(simulate.get_counts())
