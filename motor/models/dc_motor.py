
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

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

# Input parameters
V = experiment_params["input"]["voltage"]       # Applied voltage [V]
T_load = experiment_params["input"]["load_torque"]  # Load torque [N*m]



def motor_dynamics(t, x):
    current, omega = x

    # Electrical dynamics
    dI_dt = (V - R * current - Ke * omega) / L

    # Mechanical dynamics
    domega_dt = (Kt * current - b * omega - T_load) / J

    return [dI_dt, domega_dt]



# Initial conditions
x0 = [0.0, 0.0]  # [Current, Angular velocity]

# Simulation settings
t_start = 0.0
t_end = experiment_params["simulation"]["duration"]

t_eval = np.linspace(t_start, t_end, experiment_params["simulation"]["samples"])

# Numerical integration
solution = solve_ivp(
    motor_dynamics,
    (t_start, t_end),
    x0,
    t_eval=t_eval,
    method="RK45",
    rtol=1e-7,
    atol=1e-9
)

if not solution.success:
    raise RuntimeError(solution.message)

# Extract results
time = solution.t
current = solution.y[0]
omega = solution.y[1]

# Convert rad/s to RPM
rpm = omega * 60 / (2 * np.pi)

fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

# Current response
axes[0].plot(time, current)
axes[0].set_ylabel("Armature Current [A]")
axes[0].set_title("DC Motor - Open-Loop Step Response")
axes[0].grid(True)

# Speed response
axes[1].plot(time, rpm)
axes[1].set_xlabel("Time [s]")
axes[1].set_ylabel("Motor Speed [RPM]")
axes[1].grid(True)

plt.tight_layout()
plt.savefig("motor_response.png", dpi=150)
