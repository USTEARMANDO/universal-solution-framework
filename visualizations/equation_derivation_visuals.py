#!/usr/bin/env python3
"""
EQUATION DERIVATION VISUALIZATION
=================================
Visual step-by-step showing how established equations → C + F = 1

USTE Technologies LLC | December 2025
Run on JARVIS for full visualization suite
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches

# Set style
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

def create_pythagorean_derivation():
    """Visual derivation: Pythagorean → C² + F² = 1"""
    
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    fig.suptitle('PYTHAGOREAN THEOREM → C² + F² = 1', fontsize=14, fontweight='bold', y=1.02)
    
    # Step 1: Standard form
    ax1 = axes[0]
    ax1.set_xlim(0, 5)
    ax1.set_ylim(0, 4)
    ax1.set_aspect('equal')
    
    # Draw right triangle
    triangle = plt.Polygon([[0.5, 0.5], [4, 0.5], [4, 3]], 
                           fill=False, edgecolor='blue', linewidth=2)
    ax1.add_patch(triangle)
    
    # Labels
    ax1.text(2.25, 0.2, 'a', fontsize=14, ha='center', fontweight='bold')
    ax1.text(4.3, 1.75, 'b', fontsize=14, ha='center', fontweight='bold')
    ax1.text(2, 2, 'c', fontsize=14, ha='center', fontweight='bold', rotation=35)
    
    # Right angle marker
    ax1.plot([3.7, 3.7, 4], [0.5, 0.8, 0.8], 'b-', linewidth=1)
    
    ax1.text(2.25, 3.5, r'$a^2 + b^2 = c^2$', fontsize=16, ha='center', 
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    ax1.set_title('Step 1: Standard Form', fontsize=11)
    ax1.axis('off')
    
    # Step 2: Divide by c²
    ax2 = axes[1]
    ax2.set_xlim(0, 5)
    ax2.set_ylim(0, 4)
    
    steps = [
        r'$a^2 + b^2 = c^2$',
        r'Divide by $c^2$:',
        r'$\frac{a^2}{c^2} + \frac{b^2}{c^2} = 1$',
        r'$\left(\frac{a}{c}\right)^2 + \left(\frac{b}{c}\right)^2 = 1$'
    ]
    
    for i, step in enumerate(steps):
        ax2.text(2.5, 3.2 - i*0.8, step, fontsize=12, ha='center', va='top')
    
    ax2.set_title('Step 2: Normalize', fontsize=11)
    ax2.axis('off')
    
    # Step 3: Substitute
    ax3 = axes[2]
    ax3.set_xlim(0, 5)
    ax3.set_ylim(0, 4)
    
    subs = [
        r'Let $\frac{a}{c} = C$ (Coherence)',
        r'Let $\frac{b}{c} = F$ (Fluctuation)',
        '',
        r'Then: $C^2 + F^2 = 1$'
    ]
    
    for i, sub in enumerate(subs):
        color = 'red' if 'C =' in sub else ('blue' if 'F =' in sub else 'black')
        ax3.text(2.5, 3.2 - i*0.8, sub, fontsize=12, ha='center', va='top', color=color)
    
    ax3.set_title('Step 3: Substitute', fontsize=11)
    ax3.axis('off')
    
    # Step 4: Final form
    ax4 = axes[3]
    ax4.set_xlim(0, 5)
    ax4.set_ylim(0, 4)
    
    # Unit circle
    theta = np.linspace(0, 2*np.pi, 100)
    ax4.plot(2.5 + 1.2*np.cos(theta), 2 + 1.2*np.sin(theta), 'purple', linewidth=2)
    ax4.plot([2.5, 2.5+0.85], [2, 2], 'r-', linewidth=2, label='C')
    ax4.plot([2.5+0.85, 2.5+0.85], [2, 2+0.85], 'b-', linewidth=2, label='F')
    ax4.plot([2.5, 2.5+0.85], [2, 2+0.85], 'purple', linewidth=2, linestyle='--')
    
    ax4.text(2.5, 3.7, r'$C^2 + F^2 = 1$', fontsize=16, ha='center',
             bbox=dict(boxstyle='round', facecolor='gold', alpha=0.8))
    ax4.text(2.9, 1.8, 'C', fontsize=12, color='red', fontweight='bold')
    ax4.text(3.5, 2.4, 'F', fontsize=12, color='blue', fontweight='bold')
    ax4.text(2.8, 2.55, '1', fontsize=10, color='purple')
    
    ax4.set_title('Step 4: Universal Solution!', fontsize=11)
    ax4.set_aspect('equal')
    ax4.axis('off')
    
    plt.tight_layout()
    plt.savefig('derivation_pythagorean.png', dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print("✓ Created: derivation_pythagorean.png")

def create_efficiency_derivation():
    """Visual derivation: Why C = 0.5 is optimal"""
    
    fig = plt.figure(figsize=(14, 5))
    gs = GridSpec(1, 3, figure=fig)
    
    fig.suptitle('EFFICIENCY PEAKS AT C = F = 0.5', fontsize=14, fontweight='bold', y=1.02)
    
    # Panel 1: The function
    ax1 = fig.add_subplot(gs[0])
    C_vals = np.linspace(0, 1, 100)
    E_vals = C_vals * (1 - C_vals)
    
    ax1.plot(C_vals, E_vals, 'purple', linewidth=3)
    ax1.axvline(0.5, color='gold', linestyle='--', linewidth=2, alpha=0.7)
    ax1.axhline(0.25, color='gold', linestyle='--', linewidth=2, alpha=0.7)
    ax1.scatter([0.5], [0.25], color='gold', s=200, zorder=5, edgecolor='black', linewidth=2)
    
    ax1.fill_between(C_vals, E_vals, alpha=0.3, color='purple')
    
    ax1.set_xlabel('C (Coherence)', fontsize=11)
    ax1.set_ylabel('E = C × F = C × (1-C)', fontsize=11)
    ax1.set_title('Efficiency Function', fontsize=12)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 0.3)
    
    ax1.annotate('MAXIMUM\nat C = 0.5', xy=(0.5, 0.25), xytext=(0.7, 0.2),
                fontsize=10, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='black'))
    
    # Panel 2: The calculus proof
    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    
    proof_steps = [
        (r'$E = k \cdot C \cdot (1-C)$', 'Given'),
        (r'$E = kC - kC^2$', 'Expand'),
        (r'$\frac{dE}{dC} = k - 2kC$', 'Differentiate'),
        (r'$k - 2kC = 0$', 'Set = 0'),
        (r'$C = \frac{1}{2} = 0.5$', 'Solve'),
        (r'$\frac{d^2E}{dC^2} = -2k < 0$', 'Second derivative'),
        (r'$\therefore$ Maximum at $C = 0.5$', 'Conclusion'),
    ]
    
    for i, (eq, note) in enumerate(proof_steps):
        y_pos = 9 - i * 1.2
        ax2.text(0.5, y_pos, eq, fontsize=11, va='center')
        ax2.text(7, y_pos, f'← {note}', fontsize=9, va='center', color='gray')
    
    ax2.set_title('Calculus Proof', fontsize=12)
    ax2.axis('off')
    
    # Panel 3: What this means
    ax3 = fig.add_subplot(gs[2])
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    
    meanings = [
        ('C = 0 (Pure Fluctuation)', 'E = 0 × 1 = 0', 'red'),
        ('C = 0.5 (Balance)', 'E = 0.5 × 0.5 = 0.25 MAX', 'gold'),
        ('C = 1 (Pure Coherence)', 'E = 1 × 0 = 0', 'blue'),
    ]
    
    ax3.text(5, 9.5, 'INTERPRETATION', fontsize=12, ha='center', fontweight='bold')
    
    for i, (state, result, color) in enumerate(meanings):
        y_pos = 7.5 - i * 2.5
        rect = FancyBboxPatch((0.5, y_pos-0.8), 9, 1.6, 
                              boxstyle="round,pad=0.1", 
                              facecolor=color, alpha=0.3, edgecolor=color)
        ax3.add_patch(rect)
        ax3.text(5, y_pos+0.3, state, fontsize=10, ha='center', fontweight='bold')
        ax3.text(5, y_pos-0.3, result, fontsize=10, ha='center')
    
    ax3.text(5, 1, 'Maximum efficiency requires BALANCE\nNot maximum of either extreme', 
             fontsize=10, ha='center', style='italic',
             bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray'))
    
    ax3.set_title('Physical Meaning', fontsize=12)
    ax3.axis('off')
    
    plt.tight_layout()
    plt.savefig('derivation_efficiency.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✓ Created: derivation_efficiency.png")

def create_uncertainty_derivation():
    """Visual derivation: Heisenberg → C + F = constant"""
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('HEISENBERG UNCERTAINTY → C + F CONSTRAINT', fontsize=14, fontweight='bold', y=1.02)
    
    # Panel 1: The uncertainty relation
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    
    ax1.text(5, 8, r'$\Delta x \cdot \Delta p \geq \frac{\hbar}{2}$', 
             fontsize=18, ha='center',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    ax1.text(5, 6, 'Position uncertainty × Momentum uncertainty', fontsize=10, ha='center')
    ax1.text(5, 5, '≥ minimum value', fontsize=10, ha='center')
    
    ax1.text(5, 3, 'You CANNOT know both precisely.\nIncreasing one decreases the other.', 
             fontsize=10, ha='center', style='italic')
    
    ax1.set_title('Standard Heisenberg', fontsize=12)
    ax1.axis('off')
    
    # Panel 2: The tradeoff visualization
    ax2 = axes[1]
    
    # Create tradeoff curve
    Cx = np.linspace(0.1, 0.9, 100)
    Fp = 1 - Cx  # Simplified: total certainty budget = 1
    
    ax2.plot(Cx, Fp, 'purple', linewidth=3)
    ax2.fill_between(Cx, Fp, alpha=0.2, color='purple')
    
    # Mark specific points
    points = [(0.2, 0.8, 'Know position well\n(high C_x)'), 
              (0.5, 0.5, 'Balanced'), 
              (0.8, 0.2, 'Know momentum well\n(high C_p)')]
    
    for x, y, label in points:
        ax2.scatter([x], [y], s=100, zorder=5, edgecolor='black')
        offset = (10, 10) if x < 0.5 else (-10, 10)
        ax2.annotate(label, xy=(x, y), xytext=offset, textcoords='offset points',
                    fontsize=8, ha='center')
    
    ax2.set_xlabel('C_position (certainty in x)', fontsize=10)
    ax2.set_ylabel('C_momentum (certainty in p)', fontsize=10)
    ax2.set_title('The Certainty Tradeoff', fontsize=12)
    
    ax2.text(0.5, 0.9, r'$C_x + C_p = constant$', fontsize=12, 
             transform=ax2.transAxes, ha='center',
             bbox=dict(boxstyle='round', facecolor='gold', alpha=0.8))
    
    # Panel 3: US interpretation
    ax3 = axes[2]
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    
    interpretations = [
        (r'$\Delta x$ = Fluctuation in position = $F_x$', 8),
        (r'$\Delta p$ = Fluctuation in momentum = $F_p$', 7),
        ('', 6),
        (r'High certainty in x = High $C_x$ = Low $F_x$', 5),
        (r'This REQUIRES low $C_p$ = High $F_p$', 4),
        ('', 3),
        (r'$C_x + F_x = 1$ (for position)', 2),
        (r'$C_p + F_p = 1$ (for momentum)', 1.5),
    ]
    
    for text, y in interpretations:
        ax3.text(5, y, text, fontsize=10, ha='center')
    
    ax3.text(5, 9, 'US TRANSLATION', fontsize=12, ha='center', fontweight='bold')
    
    ax3.text(5, 0.3, 'Uncertainty IS the C + F = 1 constraint\nat quantum scale', 
             fontsize=10, ha='center', style='italic',
             bbox=dict(boxstyle='round', facecolor='gold', alpha=0.5))
    
    ax3.set_title('Universal Solution Form', fontsize=12)
    ax3.axis('off')
    
    plt.tight_layout()
    plt.savefig('derivation_uncertainty.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✓ Created: derivation_uncertainty.png")

def create_gravity_emergence():
    """Visual showing gravity emerging from C concentration"""
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('GRAVITY EMERGES FROM COHERENCE CONCENTRATION', 
                 fontsize=14, fontweight='bold', y=1.02)
    
    # Timeline data
    times = ['10⁻⁴³ s', '1 s', '380K yr', '100M yr', '400M yr', 'Now']
    c_values = [1.0, 0.99, 0.95, 0.7, 0.5, 0.3]
    temps = [1.4e32, 1e10, 3000, 60, 20, 2.725]
    has_gravity = [False, False, False, False, True, True]
    
    # Panel 1: Early universe - uniform C
    ax1 = axes[0, 0]
    np.random.seed(42)
    x = np.random.uniform(0, 10, 500)
    y = np.random.uniform(0, 10, 500)
    ax1.scatter(x, y, s=5, c='red', alpha=0.5)
    ax1.set_title('Early Universe (~1 second)\nC distributed uniformly', fontsize=10)
    ax1.text(5, -1, '∇C ≈ 0 → NO GRAVITY', fontsize=10, ha='center', fontweight='bold', color='red')
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    
    # Panel 2: Slight variations
    ax2 = axes[0, 1]
    x = np.random.uniform(0, 10, 500)
    y = np.random.uniform(0, 10, 500)
    # Add slight clustering
    for _ in range(3):
        cx, cy = np.random.uniform(2, 8, 2)
        mask = np.sqrt((x-cx)**2 + (y-cy)**2) < 2
        x[mask] = x[mask] * 0.9 + cx * 0.1
        y[mask] = y[mask] * 0.9 + cy * 0.1
    ax2.scatter(x, y, s=5, c='orange', alpha=0.5)
    ax2.set_title('Dark Ages (~100M years)\nSlight C variations', fontsize=10)
    ax2.text(5, -1, '∇C ≈ small → WEAK EFFECT', fontsize=10, ha='center', fontweight='bold', color='orange')
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    
    # Panel 3: C concentration (stars form)
    ax3 = axes[0, 2]
    # Background sparse
    x_bg = np.random.uniform(0, 10, 200)
    y_bg = np.random.uniform(0, 10, 200)
    ax3.scatter(x_bg, y_bg, s=3, c='gray', alpha=0.3)
    # Concentrated regions
    for _ in range(5):
        cx, cy = np.random.uniform(2, 8, 2)
        n_points = np.random.randint(20, 50)
        x_cluster = np.random.normal(cx, 0.5, n_points)
        y_cluster = np.random.normal(cy, 0.5, n_points)
        ax3.scatter(x_cluster, y_cluster, s=10, c='gold', alpha=0.8)
    ax3.set_title('First Stars (~400M years)\nC concentrates locally', fontsize=10)
    ax3.text(5, -1, '∇C significant → GRAVITY EMERGES', fontsize=10, ha='center', fontweight='bold', color='green')
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.axis('off')
    
    # Panel 4: Timeline
    ax4 = axes[1, 0]
    ax4.set_xlim(0, 6)
    ax4.set_ylim(0, 1.2)
    
    ax4.barh(0.5, 6, height=0.3, color='lightgray', edgecolor='black')
    ax4.axvline(4, color='green', linewidth=3, linestyle='--')
    
    # Mark eras
    ax4.text(0, 0.9, 'Big Bang', fontsize=8, ha='left')
    ax4.text(4, 0.9, 'First Stars\n~400M yr', fontsize=8, ha='center', color='green')
    ax4.text(6, 0.9, 'Now\n~13.8B yr', fontsize=8, ha='right')
    
    ax4.text(2, 0.2, 'NO LARGE MASSES', fontsize=9, ha='center', color='red')
    ax4.text(5, 0.2, 'MASSES EXIST', fontsize=9, ha='center', color='green')
    
    ax4.set_title('Timeline: When Did "Gravity" Exist?', fontsize=10)
    ax4.axis('off')
    
    # Panel 5: The logic
    ax5 = axes[1, 1]
    ax5.set_xlim(0, 10)
    ax5.set_ylim(0, 10)
    
    logic = [
        ('Standard Physics Says:', 9, 'black', 'bold'),
        ('"Gravity is fundamental"', 8.2, 'gray', 'normal'),
        ('"Gravity existed from t=0"', 7.4, 'gray', 'normal'),
        ('', 6.5, 'black', 'normal'),
        ('The Problem:', 5.5, 'red', 'bold'),
        ('No masses for 400M years', 4.7, 'red', 'normal'),
        ('What was gravity "doing"?', 3.9, 'red', 'normal'),
        ('', 3, 'black', 'normal'),
        ('US Resolution:', 2, 'green', 'bold'),
        ('Gravity = ∇C (C gradient)', 1.2, 'green', 'normal'),
        ('No gradient = No gravity', 0.4, 'green', 'normal'),
    ]
    
    for text, y, color, weight in logic:
        ax5.text(5, y, text, fontsize=10, ha='center', color=color, fontweight=weight)
    
    ax5.set_title('The Logic', fontsize=10)
    ax5.axis('off')
    
    # Panel 6: Key equation
    ax6 = axes[1, 2]
    ax6.set_xlim(0, 10)
    ax6.set_ylim(0, 10)
    
    ax6.text(5, 8, 'GRAVITY IS NOT FUNDAMENTAL', fontsize=12, ha='center', fontweight='bold')
    
    ax6.text(5, 6, r'Gravity $\propto \nabla C$', fontsize=16, ha='center',
             bbox=dict(boxstyle='round', facecolor='gold', alpha=0.8))
    
    ax6.text(5, 4, 'Gradient of Coherence Density', fontsize=11, ha='center')
    
    conclusions = [
        'No C concentration → No gradient → No "gravity"',
        'Mass IS coherence density',
        'Spacetime curvature IS C topology',
        '"Gravitational constant" G = C-field coupling',
    ]
    
    for i, conc in enumerate(conclusions):
        ax6.text(5, 2.5 - i*0.6, f'• {conc}', fontsize=9, ha='center')
    
    ax6.set_title('The Answer', fontsize=10)
    ax6.axis('off')
    
    plt.tight_layout()
    plt.savefig('derivation_gravity_emergence.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✓ Created: derivation_gravity_emergence.png")

def create_master_derivation_chart():
    """Master chart showing all equation → C+F=1 derivations"""
    
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    
    # Title
    ax.text(8, 11.5, 'ALL EQUATIONS → C + F = 1', fontsize=18, ha='center', 
            fontweight='bold')
    ax.text(8, 11, 'Master Derivation Summary', fontsize=12, ha='center', style='italic')
    
    # Central node
    center_x, center_y = 8, 6
    circle = plt.Circle((center_x, center_y), 1.5, color='gold', alpha=0.8)
    ax.add_patch(circle)
    ax.text(center_x, center_y, 'C + F = 1', fontsize=16, ha='center', va='center', fontweight='bold')
    
    # Surrounding equations
    equations = [
        # (x, y, standard, arrow_direction, color)
        (2, 10, 'a² + b² = c²\nPythagorean', 'Geometry', 'blue'),
        (8, 10.5, 'sin²θ + cos²θ = 1\nTrigonometry', 'Trig', 'blue'),
        (14, 10, 'P(A) + P(Ā) = 1\nProbability', 'Probability', 'blue'),
        
        (1, 6, 'F = ma\nNewton', 'Mechanics', 'green'),
        (15, 6, 'E = mc²\nEinstein', 'Relativity', 'green'),
        
        (2, 2, 'Δx·Δp ≥ ℏ/2\nHeisenberg', 'Quantum', 'purple'),
        (8, 1, 'ΔS ≥ 0\nThermodynamics', 'Thermo', 'red'),
        (14, 2, 'G_μν = 8πGT_μν\nEinstein Field', 'Gravity', 'orange'),
    ]
    
    for x, y, eq_text, domain, color in equations:
        # Box
        rect = FancyBboxPatch((x-1.5, y-0.8), 3, 1.6,
                              boxstyle="round,pad=0.1",
                              facecolor=color, alpha=0.3, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, eq_text, fontsize=9, ha='center', va='center')
        
        # Arrow to center
        dx = center_x - x
        dy = center_y - y
        length = np.sqrt(dx**2 + dy**2)
        
        # Start arrow from edge of box, end at edge of circle
        start_x = x + dx/length * 1.5
        start_y = y + dy/length * 0.8
        end_x = center_x - dx/length * 1.5
        end_y = center_y - dy/length * 1.5
        
        ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                   arrowprops=dict(arrowstyle='->', color=color, lw=2))
    
    # Legend
    legend_items = [
        ('blue', 'Pure Math'),
        ('green', 'Classical Physics'),
        ('purple', 'Quantum'),
        ('red', 'Thermodynamics'),
        ('orange', 'General Relativity'),
    ]
    
    for i, (color, label) in enumerate(legend_items):
        ax.scatter([13.5], [4.5 - i*0.5], c=color, s=100, alpha=0.5)
        ax.text(14, 4.5 - i*0.5, label, fontsize=9, va='center')
    
    # Key insight box
    ax.text(8, 0.3, 'The Universal Constraint appears in EVERY domain.\n'
                    'Different notation. Same underlying reality.',
            fontsize=10, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='gray'))
    
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.savefig('master_derivation_chart.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✓ Created: master_derivation_chart.png")

# Run all visualizations
if __name__ == '__main__':
    print("=" * 50)
    print("EQUATION DERIVATION VISUALIZATIONS")
    print("=" * 50)
    print()
    
    create_pythagorean_derivation()
    create_efficiency_derivation()
    create_uncertainty_derivation()
    create_gravity_emergence()
    create_master_derivation_chart()
    
    print()
    print("=" * 50)
    print("ALL VISUALIZATIONS COMPLETE")
    print("=" * 50)
    print()
    print("Files created:")
    print("  • derivation_pythagorean.png")
    print("  • derivation_efficiency.png")
    print("  • derivation_uncertainty.png")
    print("  • derivation_gravity_emergence.png")
    print("  • master_derivation_chart.png")
