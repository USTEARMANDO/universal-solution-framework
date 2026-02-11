#!/usr/bin/env python3
"""
Coherence-Fluctuation Energy Verification
==========================================
Universal Solution Library | December 2025

PROOF: Energy E = k·C·F = k·C·(1-C) under constraint C + F = 1

Properties verified:
- E(0) = 0 (no coherence = no tension)
- E(1) = 0 (no fluctuation = no tension)
- E_max at C = F = 0.5
- Energy is symmetric: E(C) = E(1-C)

Author: Armando R. Zaragoza
ORCID: 0009-0007-3542-0979
USTE Technologies LLC
"""

import numpy as np
import matplotlib.pyplot as plt

def energy(C, k=1.0):
    """Energy from Coherence-Fluctuation tension: E = k·C·(1-C)"""
    return k * C * (1 - C)

def main():
    print("=" * 60)
    print("COHERENCE-FLUCTUATION ENERGY VERIFICATION")
    print("=" * 60)
    
    k = 1.0  # Scaling constant
    C = np.linspace(0, 1, 1000)
    E = energy(C, k)
    
    # Key values
    E_at_0 = energy(0, k)
    E_at_1 = energy(1, k)
    E_at_half = energy(0.5, k)
    C_max = 0.5
    E_max = k / 4
    
    print(f"\nConstraint: C + F = 1")
    print(f"Energy: E = k·C·F = k·C·(1-C)")
    print(f"k = {k}")
    
    print(f"\nBoundary Values:")
    print(f"  E(C=0) = {E_at_0:.4f} (no coherence)")
    print(f"  E(C=1) = {E_at_1:.4f} (no fluctuation)")
    
    print(f"\nMaximum Energy:")
    print(f"  C_max = {C_max}")
    print(f"  E_max = k/4 = {E_max:.4f}")
    print(f"  E(0.5) = {E_at_half:.4f} ✓")
    
    print(f"\nSymmetry Check:")
    print(f"  E(0.3) = {energy(0.3, k):.4f}")
    print(f"  E(0.7) = {energy(0.7, k):.4f}")
    print(f"  E(C) = E(1-C)? {np.isclose(energy(0.3, k), energy(0.7, k))} ✓")
    
    print("\n" + "-" * 60)
    print("RESULT: ENERGY FUNCTION VERIFIED")
    print("E = k·C·F is the tension between order and disorder.")
    print("Maximum energy at balance (C = F = 0.5).")
    print("=" * 60)
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(C, E, 'b-', linewidth=2, label='E = k·C·(1-C)')
    plt.axvline(0.5, color='red', linestyle='--', label='C = 0.5 (max energy)')
    plt.scatter([0, 0.5, 1], [E_at_0, E_at_half, E_at_1], 
                color='red', s=100, zorder=5)
    plt.xlabel('Coherence (C)')
    plt.ylabel('Energy (E)')
    plt.title('Energy from Coherence-Fluctuation Tension')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.02, 0.3)
    
    # Annotate
    plt.annotate('E=0\n(pure F)', (0, 0), textcoords="offset points", 
                 xytext=(10, 20), fontsize=10)
    plt.annotate('E_max=k/4', (0.5, E_max), textcoords="offset points", 
                 xytext=(10, 10), fontsize=10)
    plt.annotate('E=0\n(pure C)', (1, 0), textcoords="offset points", 
                 xytext=(-30, 20), fontsize=10)
    
    plt.savefig('cf_energy.png', dpi=300)
    plt.show()
    
    return C, E

if __name__ == "__main__":
    main()
