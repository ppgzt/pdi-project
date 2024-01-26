import numpy as np
import cv2

from skimage.feature import corner_harris, corner_peaks, canny
from skimage import img_as_ubyte


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


def hs(f, k=0.17, t=0.05):
    cv_image = img_as_ubyte(f)

    # Calcula derivadas parciais usando filtro de Sobel
    Ix = cv2.Sobel(cv_image, cv2.CV_64F, 1, 0, ksize=3)
    Iy = cv2.Sobel(cv_image, cv2.CV_64F, 0, 1, ksize=3)

    # Calcula produtos das derivadas
    Ixx = Ix * Ix
    Iyy = Iy * Iy
    Ixy = Ix * Iy

    # Aplica janela gaussiana para suavização
    sigma = 2
    k_size = int(6 * sigma + 1)
    Ixx = cv2.GaussianBlur(Ixx, (k_size, k_size), sigma)
    Iyy = cv2.GaussianBlur(Iyy, (k_size, k_size), sigma)
    Ixy = cv2.GaussianBlur(Ixy, (k_size, k_size), sigma)

    # Calcula a matriz de covariância para cada pixel
    det_M = Ixx * Iyy - Ixy**2
    trace_M = Ixx + Iyy

    # Calcula a resposta do detector de cantos
    R = det_M - k * (trace_M**2)

    # Normaliza a resposta para valores entre 0 e 255
    R_normalized = cv2.normalize(R, 0, 255, norm_type=cv2.NORM_MINMAX)

    # Encontra os pontos que são cantos (onde R é maior que um limiar)
    corners = np.where(R > t * R.max())

    # Adiciona círculos nos pontos encontrados
    result_image = cv_image.copy()
    for y, x in zip(*corners):
        cv2.circle(result_image, (x, y), 2, (0, 0, 0), -1)

    return result_image


def mser(f, t=0, delta=5, min_area=10000, max_area=30000):
    # Criar um objeto MSER
    mser = cv2.MSER_create()

    # Configurar o parâmetro delta
    mser.setDelta(delta)

    # Detectar regiões MSER
    cv_image = img_as_ubyte(f)
    regioes, _ = mser.detectRegions(cv_image)

    # Criar uma imagem em branco do mesmo tamanho da imagem original
    imagem_destaque = np.zeros_like(cv_image)

    # Filtrar regiões com base nas áreas especificadas
    for regiao in regioes:
        area = cv2.contourArea(regiao)
        if min_area < area < max_area:
            # Inverter a cor com base no parâmetro T
            cor_regiao = 255 - t if t > 0 else 255
            # Desenhar as regiões na imagem de destaque com a cor especificada
            cv2.drawContours(imagem_destaque, [regiao], -1, (cor_regiao), -1)

    return imagem_destaque
