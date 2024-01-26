import numpy as np
import cv2

from skimage.feature import corner_harris, corner_peaks, canny
from skimage import img_as_ubyte
from skimage.morphology import skeletonize


def dcanny(f):
    return canny(f)


def region(f, t=50, seeds=[(2, 1, 100), (2, 3, 200)]): 
    seeds = [(seeds[0][0],seeds[0][1],1), (seeds[1][0],seeds[1][1],2)]
    g = np.zeros(f.shape)

    processed = []
    points = seeds

    while len(points) > 0:
        temp = []
        for point in points:
            if point[0] < 1 or point[0] >= f.shape[0]-1 or point[1] < 1 or point[1] >= f.shape[1]-1:
                continue

            x = point[0]
            y = point[1]

            neighbors_4 = [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]
            for n4 in neighbors_4:
                if n4 not in processed and abs(f[n4] - f[x,y]) <= t:
                    g[n4] = point[2]
                    temp.append((n4[0],n4[1], point[2]))
                    
                    processed.append(n4)
        points = temp

    return g

def esqueletizacao(f):
    return skeletonize(f)

def hs(f, k=0.17, t=0.05):
    cv_image = img_as_ubyte(f)

    Ix = cv2.Sobel(cv_image, cv2.CV_64F, 1, 0, ksize=3)
    Iy = cv2.Sobel(cv_image, cv2.CV_64F, 0, 1, ksize=3)

    Ixx = Ix * Ix
    Iyy = Iy * Iy
    Ixy = Ix * Iy

    sigma = 2
    k_size = int(6 * sigma + 1)

    Ixx = cv2.GaussianBlur(Ixx, (k_size, k_size), sigma)
    Iyy = cv2.GaussianBlur(Iyy, (k_size, k_size), sigma)
    Ixy = cv2.GaussianBlur(Ixy, (k_size, k_size), sigma)

    det_M = Ixx * Iyy - Ixy**2
    trace_M = Ixx + Iyy

    R = det_M - k * (trace_M**2)

    R_normalized = cv2.normalize(R, 0, 255, norm_type=cv2.NORM_MINMAX)

    corners = np.where(R > t * R.max())

    result_image = cv_image.copy()
    for y, x in zip(*corners):
        cv2.circle(result_image, (x, y), 2, (0, 0, 0), -1)

    return result_image


def mser(f, t=0, delta=5, min_area=10000, max_area=30000):
    mser = cv2.MSER_create()
    mser.setDelta(delta)

    cv_image = img_as_ubyte(f)
    regioes, _ = mser.detectRegions(cv_image)

    imagem_destaque = np.zeros_like(cv_image)
    for regiao in regioes:
        area = cv2.contourArea(regiao)
        if min_area < area < max_area:
            cor_regiao = 255 - t if t > 0 else 255
            cv2.drawContours(imagem_destaque, [regiao], -1, (cor_regiao), -1)

    return imagem_destaque
