import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6,6))
ax.axis('off'); ax.set_aspect('equal')
g = 2*np.pi*(np.sqrt(5)-1)/2
for n in range(150):
    r = 0.5*np.exp(-0.04*n)
    p = n*0.012
    v = [(p+np.cos(g*n+a))*r for a in (0,2*np.pi/3,4*np.pi/3)]
    w = [(p+np.sin(g*n+a))*r for a in (0,2*np.pi/3,4*np.pi/3)]
    ax.plot(v+[v[0]], w+[w[0]], c='forestgreen', lw=.4, alpha=.85)
plt.show()
