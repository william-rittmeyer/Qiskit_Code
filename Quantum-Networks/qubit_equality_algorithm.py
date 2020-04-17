# importing Qiskit package

import qiskit
import math

from qiskit import Aer, IBMQ
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute

#defining number of qubits

N = 5 
qr = QuantumRegister(N)

#defining classical bit for "referee"

cr = ClassicalRegister(1)

#create quantum circuit

circuit = QuantumCircuit(qr,cr)

%matplotlib inline

#initialize qubit values

circuit.h(qr[1])
circuit.h(qr[2])
circuit.h(qr[3])
circuit.h(qr[4])


circuit.draw(output = 'mpl')


#equality algorthim between N qubits


circuit.barrier()


circuit.h(qr[0])


circuit.barrier()


for i in range(1,N-1):
    
    circuit.cx(qr[i+1],qr[i])
    circuit.ccx(qr[0],qr[i],qr[i+1])
    circuit.cx(qr[i],qr[i+1])
    
    circuit.barrier()
    

circuit.h(qr[0])

circuit.barrier()
    
circuit.measure(0,0)

circuit.draw(output = 'mpl')

#run on local machine

simulator = Aer.get_backend('qasm_simulator')
result = execute(circuit,backend = simulator).result()
from qiskit.tools.visualization import plot_histogram
plot_histogram(result.get_counts())

#run on IBM simulator and/or quantum computer (this example shows simulator)

IBMQ.load_account()
provider = IBMQ.get_provider('ibm-q')
qcomp = provider.get_backend('ibmq_qasm_simulator')
job = execute(circuit, backend= qcomp)
from qiskit.tools.monitor import job_monitor
job_monitor(job)
result = job.result()
plot_histogram(result.get_counts(circuit))
