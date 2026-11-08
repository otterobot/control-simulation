import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

R = 3.0
L = 0.002
Ke = 0.02
Kt = 0.02
J = 0.0001
b = 0.00001

A_matrix = np.array([[-R/L, -Ke/L], [Kt/J, -b/J]])
B_matrix = np.array([[1/L, 0], [0, -1/J]])
C_matrix = np.array([[0, 1]])
D_matrix = np.array([[0, 0]])

motor_system = signal.StateSpace(A_matrix, B_matrix, C_matrix, D_matrix)
print("State-space representation of the DC motor:")
print(motor_system)

t_start = 0.0
t_end = 4.0
V = 6.0

t_eval = np.linspace(t_start, t_end, 2000)

voltage = np.ones_like(t_eval) * 6.0
load_torque = np.zeros_like(t_eval)

U = np.column_stack((voltage, load_torque))


tout, yout, xout = signal.lsim(motor_system, U, t_eval)\


rpm = yout* 60 / (2 * np.pi)


fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

# Current response
axes[0].plot(tout, xout[:, 0])
axes[0].set_ylabel("Armature Current [A]")
axes[0].set_title("DC Motor - Open-Loop Step Response")
axes[0].grid(True)

# Speed response
axes[1].plot(tout, rpm)
axes[1].set_xlabel("Time [s]")
axes[1].set_ylabel("Motor Speed [RPM]")
axes[1].grid(True)

plt.tight_layout()
plt.savefig("motor_response_statespace.png", dpi=150)