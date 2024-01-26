from skimage.feature import match_template
import numpy as np

def correlacao(f, filtro, best=True):
    g = match_template(f, filtro)
    if not best:
        return g
    
    max = np.max(g)

    y = np.zeros(g.shape)
    for i in range(0, g.shape[0]):
        for j in range(g.shape[1]):
            if g[i,j] == max:
                y[i,j] = 1

    return y

def correlacao2(f, filtro):
    s, t = filtro.shape

    a = int((s - 1) / 2)
    b = int((t - 1) / 2)

    w = np.mean(filtro)
    filtro_var = np.sum(filtro - w)

    f2 = np.zeros((f.shape[0]+2*a, f.shape[1]+2*b))
    f2[a-1:-a-1:,b-1:-b-1] = f
    f = f2

    g = np.zeros(f.shape)
    for i in range(a-1, f.shape[0] - a-1):
        for j in range(b-1, f.shape[1] - b-1):
            fxy = np.mean(f[i:i+a, j:j+b])
            
            kernel_var = np.sum(f[i:i+a, j:j+b] - fxy)
            if kernel_var == 0:
                kernel_var = 0.00000001

            g[i,j] = (filtro_var * kernel_var) / ((filtro_var ** 2 * kernel_var ** 2) ** 0.5)

    g = g[a-1:-a-1:,b-1:-b-1]
    g2 = np.zeros(g.shape)
    
    y = int(np.max(g))
    for i in range(0, g.shape[0]):
        for j in range(g.shape[1]):
            if int(g[i,j]) == y:
                g2[i,j] = 1

    return g2
