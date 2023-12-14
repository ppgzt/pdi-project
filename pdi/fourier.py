import pandas as pd
import numpy as np

from skimage.color import rgb2gray
from pdi import transformation as t


def fft(f):
    return np.fft.fftshift(
        np.fft.fft2(t.adjust_scale(rgb2gray(f))))
