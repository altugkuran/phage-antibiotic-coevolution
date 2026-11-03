# Mathematical specification (prototype)

Let x=(x1,x2) and y=(y1,y2) be bacterial and phage strategy frequencies (each summing to 1). Let S=(1,0.2) be illustrative antibiotic susceptibilities and H a 2x2 interaction matrix. Antibiotic exposure C(t) is an externally set periodic on/off schedule, independent of biological evolution. Payoffs f(x,y,C) and g(x,y) are defined explicitly in `models/model.py`. Frequency dynamics use replicator selection:

 dx_i/dt = x_i (f_i - sum_j x_j f_j) + alpha_mut m_B (x_other - x_i)
 dy_i/dt = y_i (g_i - sum_j y_j g_j) + alpha_mut m_P (y_other - y_i)

An optional stochastic perturbation is included in the Euler discretization; the resulting noise is an exploratory numerical device, not a calibrated diffusion process. Weights alpha_k in [0,1] scale selected payoff contributions. Zero switches off a contribution; one enables its chosen reference coefficient. These are not biological probabilities. Euler steps are projected onto the probability simplex by clipping and renormalization. This is a computational approximation and not an exact solver.

## Next research steps

1. Derive a dimensionally consistent birth–death–mutation process with explicit bacterial and phage abundance, infection and burst dynamics.
2. Separate per-base mutation rate, genome size, and phenotype transition probabilities; include neutral lineages and epistasis.
3. Add mechanism modules for biofilm, immunity, HGT, spatial heterogeneity and bottlenecks; do not claim implementation until tested.
4. Perform parameter sensitivity, convergence checks and validation against licensed published aggregate experimental results.
5. Compare model predictions with null and alternate models; document failures and uncertainty.
