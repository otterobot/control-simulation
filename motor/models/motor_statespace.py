import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import yaml
import yaml

with open("../parameters/example_motor.yaml", "r") as file:
    motor_params = yaml.safe_load(file)

with open("../experiments/step_response.yaml", "r") as file:
    experiment_params = yaml.safe_load(file)

# Motor parameters (illustrative values)
R = motor_params["R"]        # Armature resistance [Ohm]
L = motor_params["L"]      # Armature inductance [H]
Ke = motor_params["Ke"]      # Back EMF constant [V*s/rad]
Kt = motor_params["Kt"]      # Torque constant [N*m/A]
J = motor_params["J"]     # Moment of inertia [kg*m^2]
b = motor_params["b"]    # Viscous friction coefficient [N*m*s/rad]

A_matrix = np.array([[-R/L, -Ke/L], [Kt/J, -b/J]])
B_matrix = np.array([[1/L, 0], [0, -1/J]])
C_matrix = np.array([[0, 1]])
D_matrix = np.array([[0, 0]])

motor_system = signal.StateSpace(A_matrix, B_matrix, C_matrix, D_matrix)

t_start = 0.0
t_end = experiment_params["simulation"]["duration"]
samples = experiment_params["simulation"]["samples"]

V = experiment_params["input"]["voltage"]       # Applied voltage [V]
T_load = experiment_params["input"]["load_torque"]  # Load torque [N*m]

t_eval = np.linspace(t_start, t_end, samples)

voltage = np.ones_like(t_eval) * V
load_torque = np.zeros_like(t_eval)

U = np.column_stack((voltage, load_torque))


tout, yout, xout = signal.lsim(motor_system, U, t_eval)


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