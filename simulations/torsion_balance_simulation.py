#!/usr/bin/env python3
"""
TORSION BALANCE SIMULATION v2 - Phenomenological Approach
==========================================================
For testing the Universal Solution / Scalar Field Framework
with Chameleon/Symmetron Screening Mechanism

Author: Armando Ray Zaragoza
        Founder, USTE Technologies LLC
        
Theory: Scalar Field Framework and Scalar Time Theory
        DeSci Labs dPID: 794

Key Insight: The Universal Solution potential already has symmetron form!
             V(Φ) = -½μ²Φ² + ¼λΦ⁴
             
This means US naturally incorporates a screening mechanism that could
make its fifth force detectable in laboratory vacuum.

Standard scalar-tensor:    α₅ ~ 10⁻²⁰ (UNDETECTABLE)
Chameleon/Symmetron:       α_eff ~ 10⁻² to 10⁻⁴ in vacuum (DETECTABLE!)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint, quad
from scipy.optimize import brentq, minimize_scalar
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, List
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# FUNDAMENTAL CONSTANTS (SI Units)
# =============================================================================

# Gravitational constant
G = 6.67430e-11  # m³ kg⁻¹ s⁻²

# Speed of light
c = 2.99792458e8  # m/s

# Reduced Planck constant
hbar = 1.054571817e-34  # J·s

# Planck mass
M_pl = np.sqrt(hbar * c / G)  # kg ≈ 2.176e-8 kg

# Reduced Planck mass (commonly used in scalar-tensor theories)
M_pl_reduced = M_pl / np.sqrt(8 * np.pi)  # kg

# Boltzmann constant
k_B = 1.380649e-23  # J/K

# Atmospheric pressure
P_atm = 101325  # Pa

# =============================================================================
# MATERIAL PROPERTIES
# =============================================================================

@dataclass
class Material:
    """Material properties for test masses and environment."""
    name: str
    density: float      # kg/m³
    atomic_mass: float  # kg (per atom)
    Z: int              # atomic number
    A: int              # mass number
    
# Common materials for torsion balance experiments
MATERIALS = {
    'tungsten': Material('Tungsten', 19300, 183.84 * 1.66054e-27, 74, 184),
    'gold': Material('Gold', 19320, 196.97 * 1.66054e-27, 79, 197),
    'copper': Material('Copper', 8960, 63.546 * 1.66054e-27, 29, 64),
    'aluminum': Material('Aluminum', 2700, 26.982 * 1.66054e-27, 13, 27),
    'beryllium': Material('Beryllium', 1850, 9.012 * 1.66054e-27, 4, 9),
    'lead': Material('Lead', 11340, 207.2 * 1.66054e-27, 82, 207),
}

# =============================================================================
# UNIVERSAL SOLUTION / SYMMETRON FIELD THEORY
# =============================================================================

@dataclass
class UniversalSolutionParams:
    """
    Parameters for the Universal Solution scalar field.
    
    The US potential has symmetron form:
        V(Φ) = -½μ²Φ² + ¼λΦ⁴
        
    With matter coupling:
        L_int = (Φ/M)² T^μ_μ
        
    Where M is the coupling scale.
    """
    mu: float           # Mass parameter (eV or kg·c²)
    lambda_4: float     # Quartic self-coupling (dimensionless)
    M_coupling: float   # Matter coupling scale (kg or GeV/c²)
    
    @property
    def vev(self) -> float:
        """Vacuum expectation value: v = μ/√λ"""
        return self.mu / np.sqrt(self.lambda_4)
    
    @property
    def field_mass_vacuum(self) -> float:
        """Field mass in vacuum: m = √2 μ"""
        return np.sqrt(2) * self.mu
    
    @property
    def compton_wavelength(self) -> float:
        """Compton wavelength in vacuum: λ_c = ħ/(m·c)"""
        # Convert mass parameter to kg
        m_kg = self.field_mass_vacuum * 1.783e-36  # eV to kg
        return hbar / (m_kg * c)


class SymmetronScreening:
    """
    Implements chameleon/symmetron screening mechanism.
    
    Key physics:
    - In high-density regions: field sits at Φ ≈ 0 (screened)
    - In low-density regions (vacuum): field rolls to VEV (unscreened)
    - Fifth force only operates where field has non-zero gradient
    
    The effective coupling strength depends on:
    1. Local matter density
    2. Object size relative to Compton wavelength
    3. Thin-shell parameter (how much of object is screened)
    """
    
    def __init__(self, params: UniversalSolutionParams):
        self.params = params
        
    def effective_density(self, pressure_pa: float, temperature_k: float = 300) -> float:
        """
        Calculate effective matter density from gas pressure.
        
        For residual gas (typically N2 or air):
        ρ = P·M / (R·T)
        
        Args:
            pressure_pa: Pressure in Pascals
            temperature_k: Temperature in Kelvin
            
        Returns:
            Effective density in kg/m³
        """
        # Mean molecular mass of air
        M_air = 28.97e-3  # kg/mol
        R = 8.314  # J/(mol·K)
        
        return pressure_pa * M_air / (R * temperature_k)
    
    def symmetry_breaking_density(self) -> float:
        """
        Critical density where symmetron transitions from Φ=0 to Φ=v.
        
        For PHENOMENOLOGICAL screening, we set this to a laboratory-accessible value.
        Typical target: ρ_crit ~ 10^-8 to 10^-5 kg/m³ (UHV to low vacuum)
        
        This is chosen so that:
        - In atmosphere (ρ ~ 1 kg/m³): fully screened
        - In rough vacuum (ρ ~ 10^-3 kg/m³): partially screened
        - In UHV (ρ ~ 10^-12 kg/m³): fully unscreened
        
        Phenomenological formula:
        ρ_crit ≈ 10^-6 kg/m³ × (μ / 10^-4 eV)² × (10^14 GeV / M)²
        """
        # Reference values
        mu_ref = 1e-4  # eV
        M_ref = 1e14 * 1e9 * 1.783e-36  # 10^14 GeV in kg
        rho_crit_ref = 1e-6  # kg/m³ - accessible in lab vacuum
        
        # Scale from reference
        mu_ratio = (self.params.mu / mu_ref)**2
        M_ratio = (M_ref / self.params.M_coupling)**2
        
        return rho_crit_ref * mu_ratio * M_ratio
    
    def local_vev(self, density: float) -> float:
        """
        Local vacuum expectation value accounting for density.
        
        For symmetron:
        Φ_local = v √(1 - ρ/ρ_crit)  if ρ < ρ_crit
                = 0                    if ρ ≥ ρ_crit
        """
        rho_crit = self.symmetry_breaking_density()
        
        if density >= rho_crit:
            return 0.0
        else:
            return self.params.vev * np.sqrt(1 - density / rho_crit)
    
    def thin_shell_factor(self, radius: float, density: float) -> float:
        """
        Calculate thin-shell suppression factor for a spherical object.
        
        PHENOMENOLOGICAL APPROACH:
        For objects much larger than Compton wavelength, the interior is screened
        and only a thin shell near the surface contributes to the fifth force.
        
        For chameleon-type screening:
        - Small objects (r < λ_c): Q ≈ 1 (fully unscreened)
        - Large objects (r >> λ_c): Q ≈ 3λ_c/r (thin-shell suppression)
        
        This gives the characteristic size-dependent screening that makes
        chameleon detection possible with small test masses.
        
        Args:
            radius: Object radius in meters
            density: Object density in kg/m³
            
        Returns:
            Thin-shell factor (0 to 1, where 1 = fully unscreened)
        """
        lambda_c = self.params.compton_wavelength
        
        # Ratio of Compton wavelength to object size
        ratio = lambda_c / radius
        
        if ratio >= 1:
            # Small object: fully unscreened
            return 1.0
        else:
            # Large object: thin-shell suppression
            # Q ≈ 3 × (λ_c / R) for R >> λ_c
            return min(1.0, 3 * ratio)
    
    def effective_coupling(self, 
                          source_radius: float, 
                          source_density: float,
                          test_radius: float,
                          test_density: float,
                          ambient_density: float) -> float:
        """
        Calculate effective fifth-force coupling α_eff between two objects.
        
        PHENOMENOLOGICAL APPROACH:
        
        α_eff = α_base × Q_source × Q_test × (1 - ρ/ρ_crit)
        
        Where:
        - α_base is the unscreened coupling (~10^-2 for strong chameleon)
        - Q factors are thin-shell suppressions
        - (1 - ρ/ρ_crit) accounts for ambient density screening
        
        Returns:
            Effective coupling strength relative to gravity
        """
        # Thin-shell factors for both objects
        Q_source = self.thin_shell_factor(source_radius, source_density)
        Q_test = self.thin_shell_factor(test_radius, test_density)
        
        # Ambient screening factor
        rho_crit = self.symmetry_breaking_density()
        if ambient_density >= rho_crit:
            ambient_factor = 0.0
        else:
            ambient_factor = (1 - ambient_density / rho_crit)**2
        
        # Base coupling - phenomenological value for chameleon-type theories
        # This represents the unscreened coupling in vacuum
        # Typical range: 10^-4 to 10^-1 for viable chameleon models
        alpha_base = 0.01  # Optimistic but not excluded
        
        # Effective coupling with all screening factors
        alpha_eff = alpha_base * Q_source * Q_test * ambient_factor
        
        return alpha_eff



# =============================================================================
# TORSION BALANCE EXPERIMENTAL GEOMETRY
# =============================================================================

@dataclass
class TorsionBalanceConfig:
    """
    Configuration for torsion balance experiment.
    
    Geometry: Two test masses on a horizontal bar, suspended by a thin fiber.
    Source masses are positioned to create maximum torque.
    """
    # Pendulum properties
    test_mass: float          # kg - mass of each test body
    test_radius: float        # m - radius of test body (assumed spherical)
    arm_length: float         # m - distance from fiber to test mass center
    fiber_kappa: float        # N·m/rad - torsion constant
    quality_factor: float     # Q factor of pendulum
    
    # Source mass properties  
    source_mass: float        # kg - mass of each source body
    source_radius: float      # m - radius of source body
    
    # Geometry
    separation: float         # m - center-to-center distance (test to source)
    
    # Environment
    pressure_pa: float        # Pa - chamber pressure
    temperature_k: float      # K - temperature
    
    # Materials
    test_material: str        # Material name for test masses
    source_material: str      # Material name for source masses
    
    @property
    def natural_frequency(self) -> float:
        """Natural oscillation frequency in Hz."""
        I = 2 * self.test_mass * self.arm_length**2  # moment of inertia
        omega = np.sqrt(self.fiber_kappa / I)
        return omega / (2 * np.pi)
    
    @property
    def period(self) -> float:
        """Oscillation period in seconds."""
        return 1 / self.natural_frequency
    
    @property
    def thermal_noise_torque(self) -> float:
        """
        Thermal noise torque spectral density.
        
        S_τ = 4 k_B T κ / (ω Q)
        
        Returns:
            Torque noise in N·m/√Hz
        """
        omega = 2 * np.pi * self.natural_frequency
        S_tau = 4 * k_B * self.temperature_k * self.fiber_kappa / (omega * self.quality_factor)
        return np.sqrt(S_tau)


class TorsionBalanceExperiment:
    """
    Complete torsion balance simulation with screened fifth force.
    """
    
    def __init__(self, 
                 config: TorsionBalanceConfig,
                 us_params: UniversalSolutionParams):
        self.config = config
        self.us_params = us_params
        self.screening = SymmetronScreening(us_params)
        
        # Get material densities
        self.test_density = MATERIALS[config.test_material].density
        self.source_density = MATERIALS[config.source_material].density
        
    def gravitational_force(self) -> float:
        """
        Newtonian gravitational force between test and source mass.
        
        F_grav = G × M₁ × M₂ / r²
        """
        return (G * self.config.test_mass * self.config.source_mass / 
                self.config.separation**2)
    
    def gravitational_torque(self) -> float:
        """
        Gravitational torque on pendulum from source masses.
        
        τ_grav = 2 × F_grav × L × sin(θ)
        
        For maximum torque configuration (θ = 90°, sources at quadrature).
        """
        F = self.gravitational_force()
        return 2 * F * self.config.arm_length
    
    def fifth_force(self, ambient_pressure: Optional[float] = None) -> float:
        """
        Screened fifth force between test and source mass.
        
        F_5 = α_eff × F_grav
        
        Args:
            ambient_pressure: Override chamber pressure (Pa)
            
        Returns:
            Fifth force magnitude in Newtons
        """
        pressure = ambient_pressure if ambient_pressure is not None else self.config.pressure_pa
        
        # Calculate ambient density from pressure
        ambient_density = self.screening.effective_density(pressure, self.config.temperature_k)
        
        # Get effective coupling
        alpha_eff = self.screening.effective_coupling(
            source_radius=self.config.source_radius,
            source_density=self.source_density,
            test_radius=self.config.test_radius,
            test_density=self.test_density,
            ambient_density=ambient_density
        )
        
        # Fifth force = α_eff × gravitational force
        F_grav = self.gravitational_force()
        F_fifth = alpha_eff * F_grav
        
        return F_fifth
    
    def fifth_force_torque(self, ambient_pressure: Optional[float] = None) -> float:
        """Torque from fifth force on pendulum."""
        F = self.fifth_force(ambient_pressure)
        return 2 * F * self.config.arm_length
    
    def total_torque(self, ambient_pressure: Optional[float] = None) -> float:
        """Total torque (gravitational + fifth force)."""
        return self.gravitational_torque() + self.fifth_force_torque(ambient_pressure)
    
    def angular_deflection(self, ambient_pressure: Optional[float] = None) -> float:
        """
        Equilibrium angular deflection from applied torque.
        
        θ = τ / κ
        
        Returns:
            Deflection angle in radians
        """
        tau = self.total_torque(ambient_pressure)
        return tau / self.config.fiber_kappa
    
    def signal_to_noise(self, 
                        integration_time: float,
                        ambient_pressure: Optional[float] = None) -> float:
        """
        Signal-to-noise ratio for fifth force detection.
        
        SNR = τ_fifth / (τ_noise / √(t × BW))
        
        Args:
            integration_time: Measurement time in seconds
            ambient_pressure: Override chamber pressure
            
        Returns:
            Signal-to-noise ratio
        """
        tau_fifth = self.fifth_force_torque(ambient_pressure)
        tau_noise = self.config.thermal_noise_torque
        
        # Effective bandwidth (for resonant detection)
        bandwidth = self.config.natural_frequency / self.config.quality_factor
        
        # Noise reduction from integration
        noise_reduction = np.sqrt(integration_time * bandwidth)
        
        return abs(tau_fifth) / (tau_noise / noise_reduction)


# =============================================================================
# EXPERIMENTAL PROTOCOLS
# =============================================================================

def pressure_scan(experiment: TorsionBalanceExperiment,
                  pressures: np.ndarray) -> Dict[str, np.ndarray]:
    """
    Perform a pressure scan to detect screening-dependent fifth force.
    
    Key signature of chameleon/symmetron:
    - At high pressure: field screened, no fifth force
    - At low pressure: field unscreened, maximum fifth force
    
    This pressure dependence is THE smoking gun for screened fifth forces.
    
    Args:
        experiment: Configured torsion balance experiment
        pressures: Array of pressures to scan (Pa)
        
    Returns:
        Dictionary with pressure, forces, torques, effective couplings
    """
    results = {
        'pressure_pa': pressures,
        'fifth_force_N': np.zeros_like(pressures),
        'fifth_torque_Nm': np.zeros_like(pressures),
        'alpha_eff': np.zeros_like(pressures),
        'total_torque_Nm': np.zeros_like(pressures),
        'deflection_rad': np.zeros_like(pressures),
        'deflection_nrad': np.zeros_like(pressures),
        'snr_1hour': np.zeros_like(pressures),
    }
    
    for i, P in enumerate(pressures):
        results['fifth_force_N'][i] = experiment.fifth_force(P)
        results['fifth_torque_Nm'][i] = experiment.fifth_force_torque(P)
        results['total_torque_Nm'][i] = experiment.total_torque(P)
        results['deflection_rad'][i] = experiment.angular_deflection(P)
        results['deflection_nrad'][i] = results['deflection_rad'][i] * 1e9
        results['snr_1hour'][i] = experiment.signal_to_noise(3600, P)
        
        # Calculate effective coupling
        ambient_density = experiment.screening.effective_density(P, experiment.config.temperature_k)
        results['alpha_eff'][i] = experiment.screening.effective_coupling(
            experiment.config.source_radius, experiment.source_density,
            experiment.config.test_radius, experiment.test_density,
            ambient_density
        )
    
    return results


def parameter_space_exploration(
    base_config: TorsionBalanceConfig,
    mu_range: Tuple[float, float] = (1e-6, 1e-2),    # eV
    M_range: Tuple[float, float] = (1e10, 1e18),      # GeV
    lambda_4: float = 0.1,
    n_points: int = 50
) -> Dict[str, np.ndarray]:
    """
    Explore the (μ, M) parameter space for detectability.
    
    Creates a 2D map of:
    - Which regions are detectable (SNR > 3)
    - Which regions are already excluded
    - Optimal parameter combinations
    
    Args:
        base_config: Base experimental configuration
        mu_range: Range of mass parameter μ in eV
        M_range: Range of coupling scale M in GeV
        lambda_4: Quartic coupling (fixed)
        n_points: Grid resolution per dimension
        
    Returns:
        Dictionary with parameter arrays and detectability map
    """
    # Create logarithmic grids
    mu_values = np.logspace(np.log10(mu_range[0]), np.log10(mu_range[1]), n_points)
    M_values = np.logspace(np.log10(M_range[0]), np.log10(M_range[1]), n_points)
    
    # Output arrays
    snr_map = np.zeros((n_points, n_points))
    alpha_map = np.zeros((n_points, n_points))
    compton_map = np.zeros((n_points, n_points))
    
    for i, mu in enumerate(mu_values):
        for j, M in enumerate(M_values):
            # Create US parameters
            M_kg = M * 1e9 * 1.783e-36  # GeV to kg
            us_params = UniversalSolutionParams(
                mu=mu,
                lambda_4=lambda_4,
                M_coupling=M_kg
            )
            
            # Run experiment
            experiment = TorsionBalanceExperiment(base_config, us_params)
            
            # Calculate at lowest pressure (best case)
            snr_map[i, j] = experiment.signal_to_noise(3600, 1e-8)  # 10 nPa
            
            ambient_density = experiment.screening.effective_density(1e-8)
            alpha_map[i, j] = experiment.screening.effective_coupling(
                base_config.source_radius, 
                MATERIALS[base_config.source_material].density,
                base_config.test_radius,
                MATERIALS[base_config.test_material].density,
                ambient_density
            )
            
            compton_map[i, j] = us_params.compton_wavelength
    
    return {
        'mu_eV': mu_values,
        'M_GeV': M_values,
        'snr_map': snr_map,
        'alpha_map': alpha_map,
        'compton_m': compton_map,
        'detectable': snr_map > 3,
    }


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_pressure_scan(results: Dict[str, np.ndarray], 
                       save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot results from pressure scan showing the screening transition.
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Convert pressure to more readable units
    pressure_mbar = results['pressure_pa'] / 100
    
    # 1. Fifth force vs pressure
    ax1 = axes[0, 0]
    ax1.loglog(pressure_mbar, np.abs(results['fifth_force_N']), 'b-', lw=2)
    ax1.set_xlabel('Pressure (mbar)')
    ax1.set_ylabel('Fifth Force (N)')
    ax1.set_title('Fifth Force vs Chamber Pressure')
    ax1.grid(True, alpha=0.3)
    ax1.axvline(1e-9, color='g', linestyle='--', label='UHV regime')
    ax1.legend()
    
    # 2. Effective coupling vs pressure
    ax2 = axes[0, 1]
    ax2.loglog(pressure_mbar, results['alpha_eff'], 'r-', lw=2)
    ax2.set_xlabel('Pressure (mbar)')
    ax2.set_ylabel(r'Effective coupling $\alpha_{eff}$')
    ax2.set_title('Screening Transition')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(1e-4, color='orange', linestyle=':', label='Eöt-Wash limit')
    ax2.legend()
    
    # 3. Angular deflection vs pressure
    ax3 = axes[1, 0]
    ax3.semilogx(pressure_mbar, results['deflection_nrad'], 'g-', lw=2)
    ax3.set_xlabel('Pressure (mbar)')
    ax3.set_ylabel('Deflection (nrad)')
    ax3.set_title('Angular Deflection from Fifth Force')
    ax3.grid(True, alpha=0.3)
    
    # 4. SNR vs pressure
    ax4 = axes[1, 1]
    ax4.loglog(pressure_mbar, results['snr_1hour'], 'm-', lw=2)
    ax4.axhline(3, color='k', linestyle='--', label='Detection threshold (SNR=3)')
    ax4.axhline(5, color='gray', linestyle=':', label='Strong detection (SNR=5)')
    ax4.set_xlabel('Pressure (mbar)')
    ax4.set_ylabel('SNR (1 hour integration)')
    ax4.set_title('Signal-to-Noise Ratio')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    return fig


def plot_parameter_space(param_results: Dict[str, np.ndarray],
                        save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot the (μ, M) parameter space detectability map.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    mu = param_results['mu_eV']
    M = param_results['M_GeV']
    
    # 1. SNR map
    ax1 = axes[0]
    pcm1 = ax1.pcolormesh(M, mu, np.log10(param_results['snr_map'] + 1e-10),
                          cmap='viridis', shading='auto')
    ax1.contour(M, mu, param_results['snr_map'], levels=[3, 5, 10], 
                colors=['white', 'yellow', 'red'], linestyles=['--', '-', '-'])
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Coupling Scale M (GeV)')
    ax1.set_ylabel(r'Mass parameter $\mu$ (eV)')
    ax1.set_title('log₁₀(SNR) after 1 hour')
    plt.colorbar(pcm1, ax=ax1, label='log₁₀(SNR)')
    
    # 2. Effective coupling map
    ax2 = axes[1]
    pcm2 = ax2.pcolormesh(M, mu, np.log10(param_results['alpha_map'] + 1e-30),
                          cmap='plasma', shading='auto')
    ax2.contour(M, mu, param_results['alpha_map'], 
                levels=[1e-10, 1e-6, 1e-4, 1e-2],
                colors='white', linestyles='--')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Coupling Scale M (GeV)')
    ax2.set_ylabel(r'Mass parameter $\mu$ (eV)')
    ax2.set_title(r'log₁₀($\alpha_{eff}$) at 10 nPa')
    plt.colorbar(pcm2, ax=ax2, label=r'log₁₀($\alpha_{eff}$)')
    
    # Add existing constraint regions (approximate)
    for ax in axes:
        # Eöt-Wash constraints (schematic)
        ax.fill_between([1e10, 1e12], 1e-6, 1e-2, alpha=0.2, color='red',
                       label='Eöt-Wash excluded')
        ax.legend(loc='upper right')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    return fig


def plot_screening_mechanism(us_params: UniversalSolutionParams,
                            save_path: Optional[str] = None) -> plt.Figure:
    """
    Illustrate how the chameleon/symmetron screening works.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    screening = SymmetronScreening(us_params)
    
    # 1. Potential shape
    ax1 = axes[0]
    phi = np.linspace(-1.5 * us_params.vev, 1.5 * us_params.vev, 200)
    V_vacuum = -0.5 * us_params.mu**2 * phi**2 + 0.25 * us_params.lambda_4 * phi**4
    
    # In matter: effective mass term changes sign
    rho_crit = screening.symmetry_breaking_density()
    V_matter = 0.5 * us_params.mu**2 * phi**2 + 0.25 * us_params.lambda_4 * phi**4
    
    ax1.plot(phi / us_params.vev, V_vacuum / us_params.mu**4, 'b-', lw=2, label='Vacuum')
    ax1.plot(phi / us_params.vev, V_matter / us_params.mu**4, 'r--', lw=2, label='In matter')
    ax1.axhline(0, color='gray', linestyle=':')
    ax1.axvline(0, color='gray', linestyle=':')
    ax1.set_xlabel(r'$\Phi / v$')
    ax1.set_ylabel(r'$V(\Phi) / \mu^4$')
    ax1.set_title('Symmetron Potential')
    ax1.legend()
    ax1.set_xlim(-1.5, 1.5)
    
    # 2. Local VEV vs density
    ax2 = axes[1]
    rho_range = np.logspace(-15, 5, 100)  # kg/m³
    vev_local = [screening.local_vev(rho) / us_params.vev for rho in rho_range]
    
    ax2.semilogx(rho_range, vev_local, 'g-', lw=2)
    ax2.axvline(rho_crit, color='red', linestyle='--', label=r'$\rho_{crit}$')
    ax2.set_xlabel(r'Density $\rho$ (kg/m³)')
    ax2.set_ylabel(r'$\Phi_{local} / v$')
    ax2.set_title('Screening Transition')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Annotate typical densities
    ax2.axvline(1e-10, color='blue', linestyle=':', alpha=0.5)
    ax2.text(1e-10, 0.5, 'UHV', rotation=90, va='center')
    ax2.axvline(1.2, color='orange', linestyle=':', alpha=0.5)
    ax2.text(1.2, 0.5, 'Air', rotation=90, va='center')
    ax2.axvline(2700, color='purple', linestyle=':', alpha=0.5)
    ax2.text(2700, 0.5, 'Al', rotation=90, va='center')
    
    # 3. Thin-shell factor vs radius
    ax3 = axes[2]
    radii = np.logspace(-4, 0, 100)  # m
    thin_shell = [screening.thin_shell_factor(r, 8000) for r in radii]  # Cu density
    
    ax3.loglog(radii * 100, thin_shell, 'purple', lw=2)  # Convert to cm
    ax3.axvline(us_params.compton_wavelength * 100, color='red', linestyle='--',
               label=r'$\lambda_C$')
    ax3.set_xlabel('Object radius (cm)')
    ax3.set_ylabel('Thin-shell factor')
    ax3.set_title('Size-dependent Screening')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    return fig


# =============================================================================
# EXAMPLE CONFIGURATIONS
# =============================================================================

def create_standard_config() -> TorsionBalanceConfig:
    """
    Standard torsion balance configuration based on Eöt-Wash-style experiment.
    
    Optimized for chameleon detection:
    - Small test masses (better thin-shell conditions)
    - High Q fiber
    - UHV capability
    """
    return TorsionBalanceConfig(
        # Test masses - small spheres for minimal screening
        test_mass=0.050,          # 50g
        test_radius=0.010,        # 1 cm radius sphere
        arm_length=0.05,          # 5 cm arm
        
        # Fiber - high Q for low thermal noise
        fiber_kappa=1e-9,         # Very soft torsion fiber
        quality_factor=5000,      # High Q
        
        # Source masses
        source_mass=1.0,          # 1 kg
        source_radius=0.03,       # 3 cm radius
        
        # Geometry
        separation=0.05,          # 5 cm separation
        
        # Environment - UHV
        pressure_pa=1e-8,         # 10 nPa (UHV)
        temperature_k=300,        # Room temperature
        
        # Materials
        test_material='copper',
        source_material='tungsten',
    )


def create_phenomenological_us_params() -> UniversalSolutionParams:
    """
    Phenomenological parameters for Universal Solution.
    
    These are chosen to be:
    1. Consistent with symmetron form of US potential
    2. In potentially detectable range
    3. Not already excluded by existing experiments
    
    Note: These are PHENOMENOLOGICAL - not derived from first principles.
    The goal is to explore what parameter space might be detectable.
    """
    return UniversalSolutionParams(
        mu=1e-4,                  # 0.1 meV - gives ~mm Compton wavelength
        lambda_4=0.1,             # Moderate self-coupling
        M_coupling=1e14 * 1e9 * 1.783e-36,  # 10^14 GeV in kg
    )


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Run complete simulation and generate all plots.
    """
    print("=" * 70)
    print("TORSION BALANCE SIMULATION v2 - Phenomenological Approach")
    print("Testing Universal Solution with Chameleon/Symmetron Screening")
    print("=" * 70)
    print()
    
    # Create configuration
    config = create_standard_config()
    us_params = create_phenomenological_us_params()
    
    print("EXPERIMENTAL CONFIGURATION:")
    print(f"  Test masses:    {config.test_mass*1000:.1f} g × 2")
    print(f"  Test radius:    {config.test_radius*100:.1f} cm")
    print(f"  Source masses:  {config.source_mass:.1f} kg × 2")
    print(f"  Separation:     {config.separation*100:.1f} cm")
    print(f"  Pressure:       {config.pressure_pa:.1e} Pa")
    print(f"  Materials:      {config.test_material} / {config.source_material}")
    print()
    
    print("UNIVERSAL SOLUTION PARAMETERS:")
    print(f"  μ (mass param): {us_params.mu:.2e} eV")
    print(f"  λ (quartic):    {us_params.lambda_4}")
    print(f"  M (coupling):   {us_params.M_coupling / (1e9 * 1.783e-36):.2e} GeV")
    print(f"  VEV:            {us_params.vev:.2e} eV")
    print(f"  Compton λ:      {us_params.compton_wavelength*1000:.2f} mm")
    print()
    
    # Create experiment
    experiment = TorsionBalanceExperiment(config, us_params)
    
    print("CALCULATED VALUES:")
    print(f"  Natural freq:   {experiment.config.natural_frequency*1000:.2f} mHz")
    print(f"  Period:         {experiment.config.period:.1f} s")
    print(f"  Grav. force:    {experiment.gravitational_force():.2e} N")
    print(f"  Grav. torque:   {experiment.gravitational_torque():.2e} N·m")
    print(f"  Fifth force:    {experiment.fifth_force():.2e} N")
    print(f"  Fifth torque:   {experiment.fifth_force_torque():.2e} N·m")
    print(f"  Deflection:     {experiment.angular_deflection()*1e9:.2f} nrad")
    print(f"  SNR (1 hour):   {experiment.signal_to_noise(3600):.1f}")
    print()
    
    # Pressure scan
    print("Running pressure scan...")
    pressures = np.logspace(-10, 5, 100)  # 10^-10 to 10^5 Pa
    scan_results = pressure_scan(experiment, pressures)
    
    # Parameter space exploration
    print("Exploring parameter space (this may take a minute)...")
    param_results = parameter_space_exploration(
        config,
        mu_range=(1e-6, 1e-2),
        M_range=(1e10, 1e18),
        n_points=30  # Reduced for speed
    )
    
    # Generate plots
    print("\nGenerating plots...")
    
    fig1 = plot_pressure_scan(scan_results, 'pressure_scan_v2.png')
    fig2 = plot_parameter_space(param_results, 'parameter_space_v2.png')
    fig3 = plot_screening_mechanism(us_params, 'screening_mechanism_v2.png')
    
    print("\n" + "=" * 70)
    print("SUMMARY - HONEST ASSESSMENT")
    print("=" * 70)
    print()
    print("THE SITUATION:")
    print("  • Standard scalar-tensor coupling: α₅ ~ 10⁻²⁰ (UNDETECTABLE)")
    print("  • This is 16 orders of magnitude below current sensitivity")
    print()
    print("THE OPPORTUNITY:")
    print("  • Chameleon/Symmetron screening can boost α_eff to 10⁻² - 10⁻⁴")
    print("  • The Universal Solution potential IS a symmetron potential!")
    print("  • V(Φ) = -½μ²Φ² + ¼λΦ⁴ has the right structure")
    print()
    print("THE PATH FORWARD:")
    print("  1. Optimize for screened fifth force detection (UHV, small masses)")
    print("  2. Look for pressure-dependent force variations (smoking gun!)")
    print("  3. Either discover chameleon OR set new constraints")
    print("  4. Both outcomes are scientifically valuable")
    print()
    print("=" * 70)
    
    plt.show()
    
    return experiment, scan_results, param_results


if __name__ == '__main__':
    experiment, scan_results, param_results = main()
