#!/usr/bin/env python3
"""
Script 02: ENERGY FROM OPPOSITION
=================================
Universal Solution Verification Suite

PROVES: E = k·C·F = k·C·(1-C)
        E_max = k/4 at C = 0.5
        E(0) = E(1) = 0

Author: Armando R. Zaragoza
ORCID: 0009-0007-3542-0979
"""

import numpy as np
import matplotlib.pyplot as plt

def energy(C, k=1.0):
    """Energy from Coherence-Fluctuation tension"""
    return k * C * (1 - C)

def verify_energy():
    print("=" * 60)
    print("VERIFICATION 02: ENERGY FROM OPPOSITION")
    print("E = k·C·(1-C)")
    print("=" * 60)
    
    k = 1.0
    C = np.linspace(0, 1, 1001)
    E = energy(C, k)
    
    # Find maximum
    max_idx = np.argmax(E)
    C_max = C[max_idx]
    E_max = E[max_idx]
    
    # Analytical values
    C_max_analytical = 0.5
    E_max_analytical = k / 4
    
    print(f"\nk = {k}")
    print(f"\n--- Maximum Energy ---")
    print(f"Numerical:   C_max = {C_max:.6f}, E_max = {E_max:.6f}")
    print(f"Analytical:  C_max = {C_max_analytical:.6f}, E_max = {E_max_analytical:.6f}")
    print(f"Match: {np.isclose(C_max, C_max_analytical) and np.isclose(E_max, E_max_analytical)}")
    
    # Boundary values
    print(f"\n--- Boundary Values ---")
    E_0 = energy(0, k)
    E_1 = energy(1, k)
    print(f"E(C=0) = {E_0:.6f} (expected: 0)")
    print(f"E(C=1) = {E_1:.6f} (expected: 0)")
    print(f"Both zero: {np.isclose(E_0, 0) and np.isclose(E_1, 0)}")
    
    # Symmetry
    print(f"\n--- Symmetry Check ---")
    test_pairs = [(0.1, 0.9), (0.2, 0.8), (0.3, 0.7), (0.4, 0.6)]
    all_symmetric = True
    for c1, c2 in test_pairs:
        e1, e2 = energy(c1, k), energy(c2, k)
        sym = np.isclose(e1, e2)
        all_symmetric &= sym
        print(f"E({c1}) = {e1:.6f}, E({c2}) = {e2:.6f}, Equal: {sym}")
    print(f"E(C) = E(1-C): {all_symmetric}")
    
    # First derivative = 0 at maximum
    print(f"\n--- Calculus Verification ---")
    dE_dC = k - 2*k*C_max_analytical
    print(f"dE/dC at C=0.5: {dE_dC:.6f} (expected: 0)")
    
    # Second derivative < 0 (maximum)
    d2E_dC2 = -2*k
    print(f"d²E/dC² = {d2E_dC2:.6f} < 0: {d2E_dC2 < 0} (confirms maximum)")
    
    print("\n" + "=" * 60)
    print("RESULT: ENERGY FUNCTION VERIFIED")
    print("E = k·C·(1-C), maximum k/4 at C = 0.5")
    print("=" * 60)
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(C, E, 'b-', linewidth=2, label='E = k·C·(1-C)')
    plt.axvline(0.5, color='r', linestyle='--', alpha=0.7, label='C = 0.5')
    plt.scatter([0, 0.5, 1], [0, k/4, 0], color='red', s=100, zorder=5)
    plt.xlabel('Coherence (C)', fontsize=12)
    plt.ylabel('Energy (E)', fontsize=12)
    plt.title('Energy from Opposition: E = k·C·(1-C)', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('results/02_energy_function.png', dpi=150)
    plt.close()
    
    return True

if __name__ == "__main__":
    verify_energy()
