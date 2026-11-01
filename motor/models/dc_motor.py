
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

# Motor parameters (illustrative values)
R = 3.0        # Armature resistance [Ohm]
L = 0.002      # Armature inductance [H]
Ke = 0.02      # Back EMF constant [V*s/rad]
Kt = 0.02      # Torque constant [N*m/A]
J = 0.0001     # Moment of inertia [kg*m^2]
b = 0.00001    # Viscous friction coefficient [N*m*s/rad]

# Input parameters
V = 6.0        # Applied voltage [V]
T_load = 0.0   # Load torque [N*m]



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
t_end = 4.0

t_eval = np.linspace(t_start, t_end, 2000)

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
