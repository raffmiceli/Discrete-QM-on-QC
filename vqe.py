# Import QISKit

from qiskit_acqua import Operator, run_algorithm
from qiskit_acqua.input import get_input_instance
from ckalgomethds import get_algorithm_ck

# Import variational form to be used

vf_name = 'SIMPLE' # Input the name of the variational form, all uppercase.
imp_vf = 'from qiskit_acqua.utils.variational_forms.' \
+ vf_name.lower() + ' import VarForm' + vf_name
exec(imp_vf)

# Import useful packages

from qiskit.tools.visualization import circuit_drawer
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
from datetime import datetime

matplotlib.use('TkAgg')

# Set variables

ham_name = 'SS' # Input the name of the Hamiltonian you used when exporting
op_file = 'paulis_'+ham_name+'.txt'
file_id = ham_name
device = 'local_qasm_simulator'
depth = 3
max_trials = 100

# Make directory for storing output (if necessary)

if not os.path.exists(file_id):
    os.makedirs(file_id)

# Load Hamiltonian operator from file

qubitOp = Operator.load_from_file(op_file)
qubits = qubitOp.num_qubits

os.chdir(file_id)

startTime = datetime.now()

# Get exact energy

algorithm_cfg = {
    'name': 'ExactEigensolver',
}

params = {
    'algorithm': algorithm_cfg
}

algo_input = get_input_instance('EnergyInput')
algo_input.qubit_op = qubitOp
result_exact = run_algorithm(params,algo_input)

# Run VQE algorithm

algorithm_cfg = {
    'name': 'VQE',
    'operator_mode': 'matrix'
}

optimizer_cfg = {
    'name': 'SPSA',
    'max_trials': max_trials
}

var_form_cfg = {
    'name': vf_name,
    'depth': depth,
    'entanglement': 'linear'
}

params = {
    'algorithm': algorithm_cfg,
    'optimizer': optimizer_cfg,
    'variational_form': var_form_cfg,
    'backend': {'name': device }
}

algo_input = get_input_instance('EnergyInput')
algo_input.qubit_op = qubitOp
result_vqe = run_algorithm(params,algo_input)
timediff = datetime.now() - startTime

# Output results to plot and log files

exact_energy = result_exact['energies'][0]
vqe_energy = result_vqe['energy']

percent_error = percent_e = (abs((vqe_energy-exact_energy)/exact_energy)*100)
info_string_1 = 'Date: ' + datetime.today().strftime('%m-%d-%Y %H:%M') + '\n' \
+ 'Variaional form: ' + vf_name + '\n' \
+ 'Qubits used: ' + str(qubits) + '\n' \
+ 'Quantum Depth: ' + str(depth) +'\n' \
+ 'Number of trials: ' + str(max_trials)+ '\n' \
+ 'Exact Energy: ' + str(exact_energy) + '\n' \
+ 'Final Energy: ' + str(vqe_energy) + '\n' \
+ 'Percent Error: ' + str(percent_error) + '%\n' \
+ 'Time Elapsed: ' + str(timediff)

info_string_2 = file_id + '_' + vf_name + '_qb' + str(qubits) + '_qd' + str(depth) + '_mt' + str(max_trials) + '_' + datetime.today().strftime('%m_%d_%y_%H.%M')

plt.figure(1)
plt.plot(result_vqe['cplus'],label='c+')
plt.plot(result_vqe['cminus'],label='c-')
plt.plot(vqe_energy*np.ones(np.array(result_vqe['cminus']).shape),label='VQE Prediction')
plt.plot(exact_energy*np.ones(np.array(result_vqe['cminus']).shape),label='Exact Energy')
plt.xlabel('Optimization Steps')
plt.ylabel('Energy')
plt.legend()

file = open(file_id + '_stats.txt', 'a')
file.write(info_string_1 + '\n \n')
file.close()
plt.savefig(info_string_2 + '_plot.png')
print(info_string_1)

exec('vf = VarForm'+vf_name+'()')
vf.init_args(qubits,depth)
circ = vf.construct_circuit(result_vqe['opt_params'])
im = circuit_drawer(circ)
# im.show()
im.save(info_string_2 + '_circuit.png')