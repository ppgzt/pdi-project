import pandas as pd
import numpy as np

from pdi import transformation as t

def equalizacao(f):
    f_ajustada = t.adjust_scale(f)

    levels = pd.DataFrame(f_ajustada.flatten(), columns=['level'])
    group = levels.groupby(by='level').size().reset_index(name='nk')
    group['pk'] = group['nk'].apply(lambda x: x / (f.shape[0] * f.shape[1]))

    bind = {}

    def cdf(serie):
        prob = group.iloc[:serie.name+1]['pk'].sum()
        s = round(255 * prob)
        bind[serie['level']] = s
        return s

    group['s'] = group.apply(cdf, axis=1)
    g = np.zeros(f.shape)
    for i in range(0, f.shape[0]):
        for j in range(0, f.shape[1]):
            g[i, j] = bind[f_ajustada[i, j]]

    return t.adjust_scale(g)
