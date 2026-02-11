#!/usr/bin/env python3
"""
Script 04: UNIVERSAL TIME (Beta Function)
=========================================
Universal Solution Verification Suite

PROVES: T_s = ∫₀¹ √[u(1-u)] du = B(3/2, 3/2) = π/8

This is THE CORE RESULT.

Author: Armando R. Zaragoza
ORCID: 0009-0007-3542-0979
"""

import numpy as np
from scipy.integrate import quad
from scipy.special import beta, gamma

def integrand(u):
    """The Universal Time integrand: √[u(1-u)]"""
    return np.sqrt(u * (1 - u))

def verify_universal_time():
    print("=" * 60)
    print("VERIFICATION 04: UNIVERSAL TIME")
    print("T_s = ∫₀¹ √[u(1-u)] du = π/8")
    print("=" * 60)
    
    # Method 1: Numerical integration
    T_s_numerical, error = quad(integrand, 0, 1)
    
    # Method 2: Beta function
    # B(a,b) = ∫₀¹ t^(a-1)(1-t)^(b-1) dt
    # Our integral: ∫₀¹ u^(1/2)(1-u)^(1/2) du
    # So a-1 = 1/2 → a = 3/2, b-1 = 1/2 → b = 3/2
    T_s_beta = beta(3/2, 3/2)
    
    # Method 3: Gamma function
    # B(a,b) = Γ(a)Γ(b)/Γ(a+b)
    # B(3/2, 3/2) = Γ(3/2)²/Γ(3) = (√π/2)²/2 = (π/4)/2 = π/8
    gamma_3_2 = gamma(3/2)  # = √π/2
    gamma_3 = gamma(3)      # = 2! = 2
    T_s_gamma = (gamma_3_2 ** 2) / gamma_3
    
    # Method 4: Exact analytical
    T_s_exact = np.pi / 8
    
    print(f"\n--- Method 1: Numerical Integration ---")
    print(f"T_s = {T_s_numerical:.15f}")
    print(f"Error: {error:.2e}")
    
    print(f"\n--- Method 2: Beta Function ---")
    print(f"B(3/2, 3/2) = {T_s_beta:.15f}")
    
    print(f"\n--- Method 3: Gamma Function ---")
    print(f"Γ(3/2) = √π/2 = {gamma_3_2:.15f}")
    print(f"Γ(3) = 2! = {gamma_3:.15f}")
    print(f"Γ(3/2)²/Γ(3) = {T_s_gamma:.15f}")
    
    print(f"\n--- Method 4: Exact Analytical ---")
    print(f"π/8 = {T_s_exact:.15f}")
    
    # Comparison
    print(f"\n--- Comparison ---")
    print(f"{'Method':<25} {'Value':<20} {'Error from π/8':<15}")
    print("-" * 60)
    print(f"{'Numerical':<25} {T_s_numerical:<20.15f} {abs(T_s_numerical - T_s_exact):<15.2e}")
    print(f"{'Beta function':<25} {T_s_beta:<20.15f} {abs(T_s_beta - T_s_exact):<15.2e}")
    print(f"{'Gamma function':<25} {T_s_gamma:<20.15f} {abs(T_s_gamma - T_s_exact):<15.2e}")
    print(f"{'π/8':<25} {T_s_exact:<20.15f} {'(exact)':<15}")
    
    # All match?
    all_match = (np.isclose(T_s_numerical, T_s_exact) and 
                 np.isclose(T_s_beta, T_s_exact) and 
                 np.isclose(T_s_gamma, T_s_exact))
    
    print(f"\n--- Verification ---")
    print(f"All methods agree with π/8: {all_match}")
    print(f"Maximum deviation: {max(abs(T_s_numerical - T_s_exact), abs(T_s_beta - T_s_exact), abs(T_s_gamma - T_s_exact)):.2e}")
    
    # Physical interpretation
    print(f"\n--- Physical Interpretation ---")
    print(f"Universal Time through singularity: {T_s_exact:.6f} Planck units")
    print(f"This is FINITE, not infinite.")
    print(f"The singularity is a DOORWAY, not a wall.")
    
    print("\n" + "=" * 60)
    print("RESULT: T_s = π/8 VERIFIED")
    print("Four independent methods confirm the exact result.")
    print("=" * 60)
    
    return all_match

if __name__ == "__main__":
    verify_universal_time()
