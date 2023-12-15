import numpy as np

from PIL import Image, ImageFilter
from random import randrange

from pdi import transformation as t


def gauss(f):
    image = Image.fromarray(f)
    image = image.filter(ImageFilter.GaussianBlur)
    return np.asarray(image)


def s_p(f):
    largura, altura = f.shape
    f = t.adjust_scale(f)
    for x in range(largura * randrange(largura)):
        if (x % 2 == 0):
            f[randrange(largura), randrange(altura)] = 0
        else:
            f[randrange(largura), randrange(altura)] = 255
    return f