import numpy as np

def adjust_scale(img, k=255):
    fm = img - img.min()
    return np.rint(k * (fm / fm.max())).astype(np.uint8)

# s = cr^y
def transf_potencia(img, c=1, y=1):
    return adjust_scale(c*img**y)

def alargamento(f, lim0 = (0,0), limL = (0, 0)):
    g = np.zeros(f.shape)
    for i in range(0, f.shape[0]):
      for j in range(0, f.shape[1]):
        pos = (i,j)
        if f[pos] <= lim0[0]:
            g[pos] = lim0[1]
        elif f[pos] >= limL[1]:
            g[pos] = limL[1]
        else:
            g[pos] = f[pos]
    return g

def plano_bits(f, plan=1):
    max_len = len(bin(f.max()))
    g = np.zeros(f.shape)
    
    for i in range(0, f.shape[0]):
      for j in range(0, f.shape[1]):
        b_str = bin(f[i,j])
        b_str = b_str[0:2] + b_str[2:].rjust(max_len-2, '0')
        b_str = b_str[0:2] + b_str[-plan:].rjust(len(b_str[2:]),'0') 
        g[i,j] = int(b_str, base=2)

    return adjust_scale(g)