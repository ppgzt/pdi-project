import numpy as np
import enum
from pdi import transformation as t
 
class Filtro(enum.Enum):
    max = 1
    min = 2
    media = 3
    mediana = 4,
    laplaciano = 5

def filtragem(f, filtro=Filtro.media, shape=(3,3)):
    g = np.zeros(f.shape)
    for i in range(1, f.shape[0]-1):
        for j in range(1, f.shape[1]-1):
            neigbors = f[i-1:i+2,j-1:j+2]
            match filtro:
                case Filtro.max:
                    g[i,j] = np.max(neigbors)
                case Filtro.min:
                    g[i,j] = np.min(neigbors)
                case Filtro.media:
                    g[i,j] = np.mean(neigbors)
                case Filtro.mediana:
                    g[i,j] = np.median(neigbors)
                case Filtro.laplaciano:
                    kernel = np.array([[0,-1,0], [-1,4,-1], [0,-1,0]])
                    g[i,j] = np.sum(neigbors*kernel)

    return t.adjust_scale(g)