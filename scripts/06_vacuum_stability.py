#!/usr/bin/env python3
"""
Script 06: VACUUM STABILITY
===========================
Universal Solution Verification Suite

PROVES: The vacuum at Φ = v is STABLE
        d²V/dΦ² > 0 at vacuum (positive mass squared)
        No tachyonic instabilities

Author: Armando R. Zaragoza
ORCID: 0009-0007-3542-0979
"""

import numpy as np
import matplotlib.pyplot as plt

def verify_vacuum_stability():
    print("=" * 60)
    print("VERIFICATION 06: VACUUM STABILITY")
    print("d²V/dΦ²|_v > 0 (stable ground state)")
    print("=" * 60)
    
    # Parameters
    mu_values = [0.5, 1.0, 2.0]
    lambda_values = [0.05, 0.1, 0.2]
    
    print(f"\n--- Testing multiple parameter combinations ---")
    print(f"{'μ':<10} {'λ':<10} {'v':<15} {'d²V/dΦ²|_v':<15} {'m²':<15} {'Stable?':<10}")
    print("-" * 75)
    
    all_stable = True
    
    for mu in mu_values:
        for lam in lambda_values:
            # VEV
            v = np.sqrt(mu**2 / lam)
            
            # Second derivative at v
            # d²V/dΦ² = -μ² + 3λΦ²
            d2V = -mu**2 + 3 * lam * v**2
            
            # Simplify: at v, d²V = -μ² + 3λ(μ²/λ) = -μ² + 3μ² = 2μ²
            d2V_analytical = 2 * mu**2
            
            # Mass squared
            m_squared = d2V
            
            # Stability check
            stable = d2V > 0
            all_stable &= stable
            
            status = "✓" if stable else "✗"
            print(f"{mu:<10.2f} {lam:<10.2f} {v:<15.6f} {d2V:<15.6f} {m_squared:<15.6f} {status:<10}")
    
    print(f"\n--- Analytical Verification ---")
    print(f"At Φ = v = √(μ²/λ):")
    print(f"d²V/dΦ² = -μ² + 3λv² = -μ² + 3λ(μ²/λ) = -μ² + 3μ² = 2μ²")
    print(f"Since μ² > 0 always, d²V/dΦ² = 2μ² > 0 always.")
    print(f"\nVacuum is UNCONDITIONALLY STABLE for any μ > 0, λ > 0.")
    
    # Tachyon check
    print(f"\n--- Tachyon Check ---")
    print(f"Tachyon exists if m² < 0")
    print(f"m² = d²V/dΦ²|_v = 2μ² > 0 for all μ > 0")
    print(f"Therefore: NO TACHYONS")
    
    # At origin (unstable)
    print(f"\n--- Origin Analysis (Φ = 0) ---")
    mu, lam = 1.0, 0.1
    d2V_origin = -mu**2  # d²V/dΦ² at Φ=0
    print(f"d²V/dΦ²|_0 = -μ² = {d2V_origin:.4f} < 0")
    print(f"Origin is UNSTABLE (local maximum)")
    print(f"This drives spontaneous symmetry breaking → rolls to v")
    
    print("\n" + "=" * 60)
    print("RESULT: VACUUM STABILITY VERIFIED")
    print("All parameter combinations give stable vacuum.")
    print("m² = 2μ² > 0, no tachyons.")
    print("=" * 60)
    
    # Plot
    mu, lam = 1.0, 0.1
    v = np.sqrt(mu**2 / lam)
    Phi = np.linspace(-5, 5, 1000)
    V = -0.5 * mu**2 * Phi**2 + (lam / 4) * Phi**4
    
    plt.figure(figsize=(10, 6))
    plt.plot(Phi, V, 'b-', linewidth=2, label='V(Φ)')
    plt.axvline(v, color='g', linestyle='--', label=f'+v = {v:.2f} (stable)')
    plt.axvline(-v, color='g', linestyle='--', label=f'-v = {-v:.2f} (stable)')
    plt.axvline(0, color='r', linestyle=':', label='Φ=0 (unstable)')
    plt.scatter([v, -v], [-mu**4/(4*lam)]*2, color='green', s=100, zorder=5)
    plt.scatter([0], [0], color='red', s=100, zorder=5)
    plt.xlabel('Φ', fontsize=12)
    plt.ylabel('V(Φ)', fontsize=12)
    plt.title('Vacuum Stability: Minima at ±v, Maximum at 0', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(-3, 5)
    plt.savefig('results/06_vacuum_stability.png', dpi=150)
    plt.close()
    
    return all_stable

if __name__ == "__main__":
    verify_vacuum_stability()
