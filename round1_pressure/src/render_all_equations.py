"""
Render all academic LaTeX equations to high-resolution PNGs for ReportLab embedding.
Uses Matplotlib's native Computer Modern mathtext engine.
"""

import os
import matplotlib
import matplotlib.pyplot as plt

os.makedirs('round1_pressure/reports/figures/equations', exist_ok=True)
plt.rcParams['mathtext.fontset'] = 'cm'

equations = {
    'eq1_leverage': (
        r'$\mathrm{LI}_d = \frac{\sigma(W(s_d))}{\mathbb{E}[\sigma(W(s))]}, \quad '
        r'\sigma(W(s)) = \sqrt{\sum_{o \in \Omega} p(o)\left[W(s_{d+1}(o)) - W(s_d)\right]^2} \quad (1)$'
    ),
    'eq2_acute_conditions': (
        r'$P_d = 1 \Longleftrightarrow (\mathrm{RRR}_d \ge 10.0 \;\mathrm{and}\; b \le 36) \;\mathrm{or}\; '
        r'(\mathrm{RRR}_d \ge 12.0) \;\mathrm{or}\; (b \le 18 \;\mathrm{and}\; r \le 36 \;\mathrm{and}\; w \ge 4) \quad (2)$'
    ),
    'eq3_differential_bat': (
        r'$\Delta_{i,d}^{\mathrm{bat}} = \mathrm{RunsOffBat}_{i,d} \times 100 - \bar{y}_{c(d)}^{\mathrm{SR}} \quad (3)$'
    ),
    'eq4_differential_bowl': (
        r'$\Delta_{i,d}^{\mathrm{bowl}} = \mathrm{RunsConceded}_{i,d} \times 6 - \bar{y}_{c(d)}^{\mathrm{Econ}} \quad (4)$'
    ),
    'eq5_vif': (
        r'$\sigma_i^2 = \frac{s_i^2}{n_i} \times \mathrm{VIF}_i, \quad '
        r'\mathrm{VIF}_i = 1 + (\bar{m}_i - 1)\hat{\rho} \quad (\hat{\rho} = 0.082) \quad (5)$'
    ),
    'eq6_prior_mle': (
        r'$\hat{\mu}_0 = \frac{\sum_i w_i \bar{\Delta}_i}{\sum_i w_i}, \quad w_i = \frac{1}{\sigma_i^2 + \hat{\tau}^2}, \quad '
        r'\hat{\tau}^2 = \max\left(0, \frac{\sum_i (\bar{\Delta}_i - \hat{\mu}_0)^2 - (K-1)}{\sum_i \sigma_i^{-2}}\right) \quad (6)$'
    ),
    'eq7_shrinkage': (
        r'$B_i = \frac{\sigma_i^2}{\sigma_i^2 + \hat{\tau}^2}, \quad '
        r'\hat{\theta}_i = B_i \hat{\mu}_0 + (1 - B_i)\bar{\Delta}_i, \quad '
        r'\mathrm{SE}_i = \sqrt{\frac{\sigma_i^2 \hat{\tau}^2}{\sigma_i^2 + \hat{\tau}^2}} \quad (7)$'
    ),
    'eq8_conservative_pri': (
        r'$\mathrm{PRI}_{\mathrm{cons}, i} = \hat{\theta}_i - 1.0 \times \mathrm{SE}_i, \quad '
        r'\mathrm{RunsSaved}_{\mathrm{cons}, i} = -\left(\hat{\theta}_i + 1.0 \times \mathrm{SE}_i\right) \quad (8)$'
    ),
    'eq9_var_confidence': (
        r'$P\left(\theta_i \ge \mathrm{PRI}_{\mathrm{cons}, i} \mid \mathrm{Data}\right) = \Phi(1.0) \approx 0.8413 \quad (84.13\% \text{ Downside Protection}) \quad (9)$'
    ),
    'eq10_qualification_gate': (
        r'$\mathrm{Qualified}_i = [n_i \ge 60 \text{ legal balls}] \;\mathrm{or}\; '
        r'[n_i \ge 50 \;\mathrm{and}\; m_i \ge 10 \text{ matches}] \quad (10)$'
    ),
    'eq11_venue_fit': (
        r'$\mathrm{VenueFit}_i = 0.40 \cdot \mathrm{PhaseMatch}_i + 0.30 \cdot \mathrm{SurfaceSkill}_i + 0.30 \cdot \mathrm{DewAdapt}_i \quad (11)$'
    ),
    'eq12_squad_fit': (
        r'$\mathrm{Fit}_{\mathrm{RR}, i} = 0.35 \cdot \mathrm{Pressure}_i + 0.25 \cdot \mathrm{Tactical}_i + 0.20 \cdot \mathrm{Venue}_i + 0.10 \cdot \mathrm{RoleStab}_i + 0.10 \cdot \mathrm{Value}_i \quad (12)$'
    ),
    'eq13_win_prob_logistic': (
        r'$W(s) = \frac{1}{1 + \exp\left(-\left(\beta_0 + \beta_1 \cdot \frac{r}{b} + \beta_2 \cdot w + \beta_3 \cdot b + \beta_4 \cdot \mathrm{Tier}\right)\right)} \quad (13)$'
    ),
    'eq14_loso_loss': (
        r'$\mathcal{L}_{\mathrm{LOSO}} = \frac{1}{K}\sum_{k=1}^K \sqrt{\frac{1}{N_k}\sum_{i \in \mathcal{S}_k} \left(\bar{\Delta}_{i, k}^{\mathrm{obs}} - \hat{\theta}_{i, -k}\right)^2} \quad (14)$'
    ),
}

for name, eq in equations.items():
    fig = plt.figure(figsize=(7.2, 0.60), dpi=300)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.patch.set_alpha(0.0)
    ax.text(0.5, 0.5, eq, fontsize=11.5, ha='center', va='center', color='#001D48')
    path = f'round1_pressure/reports/figures/equations/{name}.png'
    fig.savefig(path, bbox_inches='tight', transparent=True, pad_inches=0.04)
    plt.close(fig)
    print(f'Rendered: {path}')

print('All 14 LaTeX equations compiled successfully.')
