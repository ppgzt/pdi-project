import pandas as pd
import numpy as np

from pdi import transformation as t


def fft(f):
    return np.fft.fftshift(
        np.fft.fft2(t.adjust_scale(f)))


def ifft(z):
    return t.adjust_scale(abs(np.fft.ifft2(z)))