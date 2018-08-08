# Discrete-QM-on-QC
These files can be used to create a basic quantum Hamiltonian from operators in either the position or energy basis, convert the matrix to its Pauli tensor representation, then run it through the variaitonal quantum eigensolver (VQE) algorithm using IBM's QISKit package.

Export Basic.nb - Implements basic QM operators and potentials, exports desired Hamiltonian as an array.

Make Paulis.nb - Takes output of previous file and returns a list of Pauli tensor products and coefficients.

vqe_aqua.py - Runs the VQE algorithm on the Pauli list, outputting a log file, a circuit diagram and a convergence plot.

simple.py - Example variational form. Variational form files need to be placed in a directory within the QISKit installation. For example, when installed using pip in an Anaconda environment, the path looks like this: *user_name_goes_here*/anaconda3/envs/QISKitenv/lib/python3.6/site-packages/qiskit_aqua/utils
