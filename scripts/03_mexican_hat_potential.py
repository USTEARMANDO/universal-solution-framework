#!/usr/bin/env python3
"""
Script 03: MEXICAN HAT POTENTIAL
================================
Universal Solution Verification Suite

PROVES: V(Φ) = -½μ²Φ² + (λ/4)Φ⁴
        VEV v = √(μ²/λ)
        d²V/dΦ²|_v = 2μ² > 0 (stable)

Author: Armando R. Zaragoza
ORCID: 0009-0007-3542-0979
"""

import numpy as np
import matplotlib.pyplot as plt

def V(Phi, mu=1.0, lam=0.1):
    """Mexican hat potential"""
    return -0.5 * mu**2 * Phi**2 + (lam / 4) * Phi**4

def dV_dPhi(Phi, mu=1.0, lam=0.1):
    """First derivative"""
    return -mu**2 * Phi + lam * Phi**3

def d2V_dPhi2(Phi, mu=1.0, lam=0.1):
    """Second derivative"""
    return -mu**2 + 3 * lam * Phi**2

def verify_mexican_hat():
    print("=" * 60)
    print("VERIFICATION 03: MEXICAN HAT POTENTIAL")
    print("V(Φ) = -½μ²Φ² + (λ/4)Φ⁴")
    print("=" * 60)
    
    mu = 1.0
    lam = 0.1
    
    # Vacuum expectation value
    v_analytical = np.sqrt(mu**2 / lam)
    
    print(f"\nParameters: μ = {mu}, λ = {lam}")
    print(f"\n--- Vacuum Expectation Value ---")
    print(f"v = √(μ²/λ) = √({mu**2}/{lam}) = {v_analytical:.6f}")
    
    # Verify dV/dΦ = 0 at Φ = ±v
    dV_at_v = dV_dPhi(v_analytical, mu, lam)
    dV_at_neg_v = dV_dPhi(-v_analytical, mu, lam)
    dV_at_0 = dV_dPhi(0, mu, lam)
    
    print(f"\n--- Critical Points (dV/dΦ = 0) ---")
    print(f"dV/dΦ at Φ = +v: {dV_at_v:.2e} ≈ 0: {np.isclose(dV_at_v, 0)}")
    print(f"dV/dΦ at Φ = -v: {dV_at_neg_v:.2e} ≈ 0: {np.isclose(dV_at_neg_v, 0)}")
    print(f"dV/dΦ at Φ = 0:  {dV_at_0:.2e} = 0: {np.isclose(dV_at_0, 0)}")
    
    # Stability check
    d2V_at_v = d2V_dPhi2(v_analytical, mu, lam)
    d2V_at_0 = d2V_dPhi2(0, mu, lam)
    d2V_analytical = 2 * mu**2
    
    print(f"\n--- Stability Analysis ---")
    print(f"d²V/dΦ² at Φ = ±v: {d2V_at_v:.6f}")
    print(f"Expected (2μ²):    {d2V_analytical:.6f}")
    print(f"Match: {np.isclose(d2V_at_v, d2V_analytical)}")
    print(f"d²V/dΦ² > 0 at v? {d2V_at_v > 0} ✓ (stable minimum)")
    print(f"\nd²V/dΦ² at Φ = 0: {d2V_at_0:.6f}")
    print(f"d²V/dΦ² < 0 at 0? {d2V_at_0 < 0} ✓ (unstable maximum)")
    
    # Potential values
    V_at_v = V(v_analytical, mu, lam)
    V_at_0 = V(0, mu, lam)
    V_min = -mu**4 / (4 * lam)
    
    print(f"\n--- Potential Values ---")
    print(f"V(0) = {V_at_0:.6f}")
    print(f"V(±v) = {V_at_v:.6f}")
    print(f"V_min analytical = -μ⁴/(4λ) = {V_min:.6f}")
    print(f"Match: {np.isclose(V_at_v, V_min)}")
    
    # Mass of fluctuations around vacuum
    m_squared = d2V_at_v
    print(f"\n--- Fluctuation Mass ---")
    print(f"m² = d²V/dΦ²|_v = {m_squared:.6f}")
    print(f"m = {np.sqrt(m_squared):.6f}")
    print(f"m² > 0? {m_squared > 0} ✓ (no tachyon)")
    
    print("\n" + "=" * 60)
    print("RESULT: MEXICAN HAT POTENTIAL VERIFIED")
    print(f"VEV v = {v_analytical:.4f}, stable minimum, m² = 2μ² > 0")
    print("=" * 60)
    
    # Plot
    Phi = np.linspace(-5, 5, 1000)
    V_vals = V(Phi, mu, lam)
    
    plt.figure(figsize=(10, 6))
    plt.plot(Phi, V_vals, 'b-', linewidth=2, label='V(Φ) = -½μ²Φ² + (λ/4)Φ⁴')
    plt.axvline(v_analytical, color='r', linestyle='--', alpha=0.7, label=f'v = ±{v_analytical:.2f}')
    plt.axvline(-v_analytical, color='r', linestyle='--', alpha=0.7)
    plt.axhline(0, color='gray', linestyle='-', alpha=0.3)
    plt.scatter([v_analytical, -v_analytical, 0], 
                [V_at_v, V_at_v, V_at_0], 
                color='red', s=100, zorder=5)
    plt.xlabel('Φ', fontsize=12)
    plt.ylabel('V(Φ)', fontsize=12)
    plt.title('Mexican Hat Potential (Spontaneous Symmetry Breaking)', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(-3, 5)
    plt.savefig('results/03_mexican_hat.png', dpi=150)
    plt.close()
    
    return True

if __name__ == "__main__":
    verify_mexican_hat()
