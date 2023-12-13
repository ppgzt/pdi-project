import numpy as np
from pdi import transformation as t

def fatiamento(f, levels):
    g = np.zeros((f.shape[0], f.shape[1], 3))
    g.shape
    
    for i in range(0, f.shape[0]):
        for j in range(0, f.shape[1]):
            rgb = (f[i, j], f[i, j], f[i, j])
            for key, value in levels.items():
                if f[i, j] < key:
                    rgb = value
                    break
            g[i, j, 0] = rgb[0]
            g[i, j, 1] = rgb[1]
            g[i, j, 2] = rgb[2]

    return t.adjust_scale(g)