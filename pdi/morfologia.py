import numpy as np
from pdi import transformation as t

def erosao(f, elemento):
    f = t.adjust_scale(f, k=1)
    shape = f.shape
    index = elemento.shape[0] // 2

    g = np.zeros(shape)

    for i in range(index, shape[0]-index):
        for j in range(index, shape[1]-index):
            neigbors = f[i-index:i+index+1, j-index:j+index+1]
            if (neigbors * elemento).sum() == elemento.sum():
                g[i, j] = f[i, j]
    return g


def dilatacao(f, elemento):
    f = t.adjust_scale(f, k=1)
    index = elemento.shape[0] // 2

    g = np.zeros((f.shape[0]+2*index, f.shape[1]+2*index))

    f_ = np.zeros((f.shape[0]+2*index, f.shape[1]+2*index))
    f_[index:-index, index:-index] = f

    for i in range(index, f_.shape[0]-index):
        for j in range(index, f_.shape[1]-index):
            neigbors = f_[i-index:i+index+1, j-index:j+index+1]
            if (neigbors * elemento).sum() > 0:
                g[i, j] = 1
    r = g[index:-index, index:-index]
    return r


def abertura(f, elemento):
    return dilatacao(erosao(f, elemento), elemento)


def fechamento(f, elemento):
    return erosao(dilatacao(f, elemento), elemento)
