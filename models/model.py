"""Abstract, dimensionless coevolution game; not a clinical predictor."""
import numpy as np

def simulate(steps=400, dt=0.025, antibiotic=0.4, frequency=0.5, burst=1000,
             mutation_b=0.003, mutation_p=0.003, weights=None, seed=7):
    w = {'tradeoff':1., 'cost':1., 'mutation':1., 'phage':1., 'epistasis':0., 'noise':0.}
    if weights: w.update(weights)
    if any(not 0 <= v <= 1 for v in w.values()): raise ValueError('weights must be 0..1')
    if not 0 <= frequency <= 1 or dt <= 0 or steps < 1 or burst < 0: raise ValueError('invalid parameter')
    rng=np.random.default_rng(seed)
    x=np.array([0.5,0.5]); y=np.array([0.5,0.5]); out=[]
    # Dimensionless payoffs: not fitted to organisms or clinical doses.
    susceptibility=np.array([1.,0.2]); recognition=np.array([[0.85,0.2],[0.2,0.85]])
    for k in range(steps+1):
        t=k*dt
        exposure=antibiotic if (t % 1.0) < frequency else 0.
        out.append((t,*x,*y, float(x @ susceptibility),exposure))
        if k==steps: break
        infection=recognition @ y
        fb=1.0-exposure*susceptibility-w['phage']*0.45*infection-w['cost']*np.array([0.0,0.12])
        fb+=w['tradeoff']*np.array([0.03,-0.03])*infection
        fp=(x @ recognition)*np.log1p(burst)/np.log(1001) - np.array([0.08,0.08])
        fp+=w['epistasis']*0.08*np.array([x[0]*y[1],x[1]*y[0]])
        dx=x*(fb-x@fb); dy=y*(fp-y@fp)
        # Symmetric phenotypic transitions, scaled by mechanism weight.
        dx+=w['mutation']*mutation_b*np.array([x[1]-x[0],x[0]-x[1]])
        dy+=w['mutation']*mutation_p*np.array([y[1]-y[0],y[0]-y[1]])
        if w['noise']:
            dx+=w['noise']*0.02*rng.normal()*np.array([1.,-1.])
            dy+=w['noise']*0.02*rng.normal()*np.array([1.,-1.])
        x=np.maximum(x+dt*dx,0); y=np.maximum(y+dt*dy,0)
        x/=x.sum(); y/=y.sum()
    return np.array(out)
