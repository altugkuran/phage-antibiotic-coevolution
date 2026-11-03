import csv
from pathlib import Path
from models.model import simulate
root=Path(__file__).resolve().parent
(root/'results').mkdir(exist_ok=True)
for name,weights in [('simple',{'tradeoff':0,'epistasis':0,'noise':0}),('extended',{'tradeoff':1,'epistasis':1,'noise':0.3})]:
    data=simulate(weights=weights)
    with (root/'results'/f'{name}.csv').open('w',newline='') as f:
        wr=csv.writer(f);wr.writerow(['time','b1','b2','p1','p2','mean_susceptibility','antibiotic_exposure']);wr.writerows(data)
    print(name,'final susceptibility',round(float(data[-1,5]),5))
