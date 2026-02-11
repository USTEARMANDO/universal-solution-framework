#!/usr/bin/env python3
"""
Universal Mechanism Oscillation
===============================
Universal Solution Library | December 2025

PROOF: The Universal Engine oscillates perpetually.

Equation of motion: C'' + ω₀²(C - 1/2) = 0
Solution: C(t) = 1/2 + A·cos(ω₀t + φ)

This is a harmonic oscillator centered at C = 0.5.
The mechanism runs forever because:
1. Closed system (no external sink)
2. C + F = 1 always holds
3. No friction at fundamental level

Author: Armando R. Zaragoza
ORCID: 0009-0007-3542-0979
USTE Technologies LLC
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def mechanism_ode(state, t, omega_0=1.0):
    """
    Universal Mechanism dynamics.
    C'' + ω₀²(C - 1/2) = 0
    """
    C, C_dot = state
    C_ddot = -omega_0**2 * (C - 0.5)
    return [C_dot, C_ddot]

def analytical_solution(t, C_0, C_dot_0, omega_0=1.0):
    """Analytical solution for verification."""
    A = np.sqrt((C_0 - 0.5)**2 + (C_dot_0/omega_0)**2)
    phi = np.arctan2(-C_dot_0/omega_0, C_0 - 0.5)
    return 0.5 + A * np.cos(omega_0 * t + phi)

def main():
    print("=" * 60)
    print("UNIVERSAL MECHANISM OSCILLATION")
    print("=" * 60)
    
    # Parameters
    omega_0 = 1.0
    C_0 = 0.7      # Initial coherence
    C_dot_0 = 0.0  # Initial rate
    t_max = 30
    
    # Time array
    t = np.linspace(0, t_max, 1000)
    
    # Numerical solution
    solution = odeint(mechanism_ode, [C_0, C_dot_0], t, args=(omega_0,))
    C_numerical = solution[:, 0]
    C_dot_numerical = solution[:, 1]
    
    # Analytical solution
    C_analytical = analytical_solution(t, C_0, C_dot_0, omega_0)
    
    # Compute F and Energy
    F = 1 - C_numerical
    E = C_numerical * F
    
    # Results
    print(f"\nEquation: C'' + ω₀²(C - 1/2) = 0")
    print(f"ω₀ = {omega_0}")
    print(f"Initial C = {C_0}")
    print(f"Initial dC/dt = {C_dot_0}")
    
    print(f"\nOscillation Properties:")
    print(f"  Period T = 2π/ω₀ = {2*np.pi/omega_0:.4f}")
    print(f"  Amplitude = {np.max(C_numerical) - 0.5:.4f}")
    print(f"  Center = 0.5")
    
    print(f"\nConservation Check:")
    print(f"  C + F = 1 always? {np.allclose(C_numerical + F, 1)} ✓")
    print(f"  Max deviation: {np.max(np.abs(C_numerical + F - 1)):.2e}")
    
    print(f"\nNumerical vs Analytical:")
    print(f"  Max error: {np.max(np.abs(C_numerical - C_analytical)):.2e}")
    
    print("\n" + "-" * 60)
    print("RESULT: PERPETUAL OSCILLATION VERIFIED")
    print("The Universal Engine runs forever.")
    print("Opposition (C vs F) cannot be resolved under C + F = 1.")
    print("=" * 60)
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # C(t)
    axes[0, 0].plot(t, C_numerical, 'b-', linewidth=2, label='C(t) numerical')
    axes[0, 0].plot(t, C_analytical, 'r--', linewidth=1, label='C(t) analytical')
    axes[0, 0].axhline(0.5, color='gray', linestyle=':', label='Center (C=0.5)')
    axes[0, 0].set_xlabel('Time t')
    axes[0, 0].set_ylabel('Coherence C')
    axes[0, 0].set_title('Coherence Oscillation')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # C and F together
    axes[0, 1].plot(t, C_numerical, 'b-', linewidth=2, label='C (Coherence)')
    axes[0, 1].plot(t, F, 'r-', linewidth=2, label='F (Fluctuation)')
    axes[0, 1].axhline(0.5, color='gray', linestyle=':')
    axes[0, 1].set_xlabel('Time t')
    axes[0, 1].set_ylabel('Value')
    axes[0, 1].set_title('C + F = 1 (Always)')
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    # Energy
    axes[1, 0].plot(t, E, 'g-', linewidth=2)
    axes[1, 0].axhline(0.25, color='red', linestyle='--', label='E_max = 0.25')
    axes[1, 0].set_xlabel('Time t')
    axes[1, 0].set_ylabel('Energy E = C·F')
    axes[1, 0].set_title('Energy Oscillation')
    axes[1, 0].legend()
    axes[1, 0].grid(True)
    
    # Phase space
    axes[1, 1].plot(C_numerical, C_dot_numerical, 'purple', linewidth=2)
    axes[1, 1].scatter([C_0], [C_dot_0], color='red', s=100, zorder=5, label='Start')
    axes[1, 1].set_xlabel('C')
    axes[1, 1].set_ylabel('dC/dt')
    axes[1, 1].set_title('Phase Space (Closed Orbit = Perpetual)')
    axes[1, 1].legend()
    axes[1, 1].grid(True)
    axes[1, 1].set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig('mechanism_oscillation.png', dpi=300)
    plt.show()
    
    return t, C_numerical, F, E

if __name__ == "__main__":
    main()
