import pandas as pd
import numpy as np

from scipy.fftpack import fftfreq
from pdi import transformation as t


def fft(f):
    return np.fft.fftshift(
        np.fft.fft2(f+0.1))


def ifft(z):
    return abs(np.fft.ifft2(z)-0.1)

def low_pass(z, raio=1):
    freq = fftfreq(len(z))#, d=1./2000
    z[np.abs(freq) > raio] = 0
    return ifft(z)

def high_pass(z, raio=1):
    freq = fftfreq(len(z))#, d=1./2000
    z[np.abs(freq) < raio] = 0
    return ifft(z)