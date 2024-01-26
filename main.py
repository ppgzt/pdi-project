import tkinter as tk
import skimage as sk
import numpy as np

from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkinter import messagebox

from skimage.color import rgb2gray
from PIL import Image, ImageTk

from pdi import transformation as t
from pdi import histograma as h
from pdi import pseudocores as p
from pdi import filtragem as filt
from pdi import fourier
from pdi import ruido
from pdi import morfologia as m
from pdi import reconhecimentodepadroes as rec

# Functions


def adjust_height(size, max_height=350):
    return tuple([int(max_height/size[1] * x) for x in size])


def upload_file():
    global src_img, file_array
    types = [('Tif Files', '*.tif'), ('Webp', '*.webp'),
             ('Png', '*.png'), ('Jpg', '*.jpg')]

    filename = filedialog.askopenfilename(filetypes=types)

    file_array = sk.io.imread(filename)
    if len(file_array.shape) > 2:
        file_array = t.adjust_scale(rgb2gray(file_array))

    img_file = Image.fromarray(file_array)
    src_img = ImageTk.PhotoImage(
        img_file.resize((adjust_height(img_file.size))))
    content.itemconfig(image1_id, image=src_img)


def display_result(img_array_1):
    global prc_img_1

    img_file = Image.fromarray(img_array_1)
    prc_img_1 = ImageTk.PhotoImage(
        img_file.resize((adjust_height(
            img_file.size))))
    content.itemconfig(image2_id, image=prc_img_1)


def to_float(str, default):
    try:
        return float(str)
    except:
        return default


def set_element(index):
    global elemento
    elements = {
        1: np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]),
        2: np.array([
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]),
        3: np.array([
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0]
        ]),
        4: np.array([
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ])
    }
    elemento = elements[index]


window = tk.Tk()

window.geometry("1440x1024")
window.configure(bg="#FFFFFF")

# Theme

bg_color = "#FEFEFE"

# Divs

header = tk.Canvas(
    window,
    bg=bg_color,
    height=85,
    width=1440,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
header.place(x=0, y=0)

sidebar = tk.Canvas(
    window,
    bg=bg_color,
    height=850,
    width=400,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
sidebar.place(x=0, y=90)

content = tk.Canvas(
    window,
    bg='#FFFFAA',
    height=850,
    width=1020,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
content.place(x=405, y=90)

# Widgets - Header

header.create_text(
    14.0,
    28.0,
    anchor="nw",
    text="PDI",
    fill="#000000",
    font=("RobotoRoman Regular", 24 * -1)
)

btn_upload = tk.Button(header,
                       text='Upload',
                       width=6,
                       height=1,
                       bg="#5555FF",
                       fg="white",
                       command=upload_file)
btn_upload.place(x=1350, y=24)

header.create_rectangle(
    11.0030517578125,
    59.71754862938798,
    1425.9994711896288,
    63.3450927734375,
    fill="#000000",
    outline="")

# Widgets - Sidebar

fespacial_y = 5
sidebar.create_text(
    14.0,
    fespacial_y,
    anchor="nw",
    text="Filtragem (Espacial)",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

btn_gama = tk.Button(sidebar,
                     text='Gama',
                     width=6,
                     height=1,
                     bg="#5555FF",
                     fg="white",
                     command=lambda: display_result(t.transf_potencia(file_array, y=0.5)))
btn_gama.place(x=14, y=fespacial_y+20)

btn_contraste = tk.Button(sidebar,
                          text='Contraste',
                          width=6,
                          height=1,
                          bg="#5555FF",
                          fg="white",
                          command=lambda: display_result(t.alargamento(file_array, lim0=(50, 0), limL=(200, 255))))
btn_contraste.place(x=90, y=fespacial_y+20)

btn_planobits = tk.Button(sidebar,
                          text='Plano de Bits',
                          width=8,
                          height=1,
                          bg="#5555FF",
                          fg="white",
                          command=lambda: display_result(t.plano_bits(f=file_array, plan=5)))
btn_planobits.place(x=165, y=fespacial_y+20)

btn_hist = tk.Button(sidebar,
                     text='Histograma',
                     width=6,
                     height=1,
                     bg="#5555FF",
                     fg="white",
                     command=lambda: display_result(h.equalizacao(file_array)))
btn_hist.place(x=255, y=fespacial_y+20)

# PSEUDOCORES #

fpseudo = fespacial_y + 65
sidebar.create_text(
    14.0,
    fpseudo,
    anchor="nw",
    text="Pseudocores",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

btn_pseudo = tk.Button(sidebar,
                       text='Pseudocores',
                       width=8,
                       height=1,
                       bg="#5555FF",
                       fg="white",
                       command=lambda: display_result(
                           p.fatiamento(file_array,
                                        levels={
                                            50: (0, 255, 0),
                                            100: (0, 0, 255),
                                            150: (255, 0, 0),
                                            175: (255, 255, 0)})))
btn_pseudo.place(x=14, y=fpseudo+20)

# Estatísticas de Ordem #

fordem = fpseudo + 65
sidebar.create_text(
    14.0,
    fordem,
    anchor="nw",
    text="Estatísticas de Ordem",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

btn_media = tk.Button(sidebar,
                      text='Média',
                      width=6,
                      height=1,
                      bg="#5555FF",
                      fg="white",
                      command=lambda: display_result(filt.filtragem(file_array, filtro=filt.Filtro.media)))
btn_media.place(x=14, y=fordem+20)

btn_mediana = tk.Button(sidebar,
                        text='Mediana',
                        width=6,
                        height=1,
                        bg="#5555FF",
                        fg="white",
                        command=lambda: display_result(filt.filtragem(file_array, filtro=filt.Filtro.mediana)))
btn_mediana.place(x=90, y=fordem+20)

btn_max = tk.Button(sidebar,
                    text='Máx',
                    width=6,
                    height=1,
                    bg="#5555FF",
                    fg="white",
                    command=lambda: display_result(filt.filtragem(file_array, filtro=filt.Filtro.max)))
btn_max.place(x=165, y=fordem+20)

btn_min = tk.Button(sidebar,
                    text='Min',
                    width=6,
                    height=1,
                    bg="#5555FF",
                    fg="white",
                    command=lambda: display_result(filt.filtragem(file_array, filtro=filt.Filtro.min)))
btn_min.place(x=240, y=fordem+20)

btn_laplace = tk.Button(sidebar,
                        text='Laplace',
                        width=6,
                        height=1,
                        bg="#5555FF",
                        fg="white",
                        command=lambda: display_result(
                           t.adjust_scale(
                               file_array + filt.filtragem(file_array, filtro=filt.Filtro.laplaciano))))
btn_laplace.place(x=315, y=fordem+20)

# Fourier #

fourier_y = fordem + 65
sidebar.create_text(
    14.0,
    fourier_y,
    anchor="nw",
    text="Fourier",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

btn_dft = tk.Button(sidebar,
                    text='DFT',
                    width=6,
                    height=1,
                    bg="#5555FF",
                    fg="white",
                    command=lambda: display_result(t.adjust_scale(np.log(abs(fourier.fft(file_array))))))
btn_dft.place(x=14, y=fourier_y+20)

btn_idft = tk.Button(sidebar,
                     text='IDFT',
                     width=6,
                     height=1,
                     bg="#5555FF",
                     fg="white",
                     command=lambda: display_result(fourier.ifft(fourier.fft(file_array))))
btn_idft.place(x=90, y=fourier_y+20)

# Filtragem | Frequência #

frequencia_y = fourier_y+65
sidebar.create_text(
    14.0,
    frequencia_y,
    anchor="nw",
    text="Filtragem (Frequência)",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

btn_baixa = tk.Button(sidebar,
                      text='Passa Baixa',
                      width=8,
                      height=1,
                      bg="#5555FF",
                      fg="white",
                      command=lambda: display_result(
                          fourier.low_pass(fourier.fft(file_array), raio=to_float(e1.get(), 0.5))))
btn_baixa.place(x=14, y=frequencia_y+20)

btn_alta = tk.Button(sidebar,
                     text='Passa Alta',
                     width=8,
                     height=1,
                     bg="#5555FF",
                     fg="white",
                     command=lambda: display_result(
                         fourier.high_pass(fourier.fft(file_array), raio=to_float(e1.get(), 0.5))))
btn_alta.place(x=105, y=frequencia_y+20)

btn_notch = tk.Button(sidebar,
                      text='Rejeita Notch',
                      width=8,
                      height=1,
                      bg="#5555FF",
                      fg="white",
                      command=lambda: display_result(t.plano_bits(f=file_array, plan=5)))
btn_notch.place(x=195, y=frequencia_y+20)

tk.Label(sidebar, text="Raio: ", bg=bg_color).place(x=14, y=frequencia_y+55)

global e1
e1 = tk.Entry(sidebar, width=11)
e1.insert(0, "0.5")
e1.place(x=14, y=frequencia_y+75)

# Restauração de Imagens #

restaura_y = frequencia_y+110
sidebar.create_text(
    14.0,
    restaura_y,
    anchor="nw",
    text="Restauração de Imagens",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

btn_ruidogaus = tk.Button(sidebar,
                          text='Ruído Gaus',
                          width=8,
                          height=1,
                          bg="#5555FF",
                          fg="white",
                          command=lambda: display_result(ruido.gauss(file_array)))
btn_ruidogaus.place(x=14, y=restaura_y+20)

btn_ruidosal = tk.Button(sidebar,
                         text='Ruído S&P',
                         width=8,
                         height=1,
                         bg="#5555FF",
                         fg="white",
                         command=lambda: display_result(ruido.s_p(file_array)))
btn_ruidosal.place(x=105, y=restaura_y+20)

btn_mediageo = tk.Button(sidebar,
                         text='Média Geo.',
                         width=8,
                         height=1,
                         bg="#5555FF",
                         fg="white",
                         command=lambda: display_result(filt.filtragem(file_array, filtro=filt.Filtro.media_geo)))
btn_mediageo.place(x=14, y=restaura_y+50)

btn_mediaalfa = tk.Button(sidebar,
                          text='Média Alfa',
                          width=8,
                          height=1,
                          bg="#5555FF",
                          fg="white",
                          command=lambda: display_result(filt.filtragem(file_array, filtro=filt.Filtro.media_alfa)))
btn_mediaalfa.place(x=105, y=restaura_y+50)

# Morfologia #

morfologia_y = restaura_y+95
sidebar.create_text(
    14.0,
    morfologia_y,
    anchor="nw",
    text="Morfologia",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

btn_erosao = tk.Button(sidebar,
                       text='Erosão',
                       width=8,
                       height=1,
                       bg="#5555FF",
                       fg="white",
                       command=lambda: display_result(
                           t.adjust_scale(m.erosao(file_array, elemento))))
btn_erosao.place(x=14, y=morfologia_y+20)

btn_dilata = tk.Button(sidebar,
                       text='Dilatação',
                       width=8,
                       height=1,
                       bg="#5555FF",
                       fg="white",
                       command=lambda: display_result(
                           t.adjust_scale(m.dilatacao(file_array, elemento))))
btn_dilata.place(x=105, y=morfologia_y+20)

btn_abertura = tk.Button(sidebar,
                         text='Abertura',
                         width=8,
                         height=1,
                         bg="#5555FF",
                         fg="white",
                         command=lambda: display_result(
                             t.adjust_scale(m.abertura(file_array, elemento))))
btn_abertura.place(x=195, y=morfologia_y+20)

btn_fechamento = tk.Button(sidebar,
                           text='Fechamento',
                           width=8,
                           height=1,
                           bg="#5555FF",
                           fg="white",
                           command=lambda: display_result(
                               t.adjust_scale(m.fechamento(file_array, elemento))))
btn_fechamento.place(x=285, y=morfologia_y+20)

tk.Label(sidebar, text="Escolhe o filtro abaixo: ",
         bg=bg_color).place(x=14, y=morfologia_y+55)

elemento = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
])


es01_file = Image.fromarray(sk.io.imread("assets/images/es_01.jpeg"))
img_es01 = ImageTk.PhotoImage(es01_file.resize(
    adjust_height(es01_file.size, max_height=78)))

btn_es01 = tk.Button(sidebar,
                     relief='flat',
                     image=img_es01,
                     command=lambda: set_element(1))
btn_es01.place(x=14, y=morfologia_y+80)

es02_file = Image.fromarray(sk.io.imread("assets/images/es_02.jpeg"))
img_es02 = ImageTk.PhotoImage(es02_file.resize(
    adjust_height(es02_file.size, max_height=78)))

btn_es02 = tk.Button(sidebar,
                     relief='flat',
                     image=img_es02,
                     command=lambda: set_element(2))
btn_es02.place(x=105, y=morfologia_y+80)

es03_file = Image.fromarray(sk.io.imread("assets/images/es_03.jpeg"))
img_es03 = ImageTk.PhotoImage(es03_file.resize(
    adjust_height(es03_file.size, max_height=78)))

btn_es03 = tk.Button(sidebar,
                     relief='flat',
                     image=img_es03,
                     command=lambda: set_element(3))
btn_es03.place(x=195, y=morfologia_y+80)

es04_file = Image.fromarray(sk.io.imread("assets/images/es_04.jpeg"))
img_es04 = ImageTk.PhotoImage(es04_file.resize(
    adjust_height(es04_file.size, max_height=78)))

btn_es04 = tk.Button(sidebar,
                     relief='flat',
                     image=img_es04,
                     command=lambda: set_element(4))
btn_es04.place(x=285, y=morfologia_y+80)

# Bordas Canny

canny_y = morfologia_y+180
sidebar.create_text(
    14.0,
    canny_y,
    anchor="nw",
    text="Bordas Canny",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

btn_borda = tk.Button(sidebar,
                      text='Borda Canny',
                      width=8,
                      height=1,
                      bg="#5555FF",
                      fg="white",
                      command=lambda: display_result(ruido.gauss(file_array)))
btn_borda.place(x=14, y=canny_y+20)

btn_supressao = tk.Button(sidebar,
                          text='Supressão',
                          width=8,
                          height=1,
                          bg="#5555FF",
                          fg="white",
                          command=lambda: display_result(ruido.s_p(file_array)))
btn_supressao.place(x=105, y=canny_y+20)

btn_limiarbaixo = tk.Button(sidebar,
                            text='Limiar Baixo',
                            width=8,
                            height=1,
                            bg="#5555FF",
                            fg="white",
                            command=lambda: display_result(filt.filtragem(file_array, filtro=filt.Filtro.media_geo)))
btn_limiarbaixo.place(x=195, y=canny_y+20)

btn_limiaralto = tk.Button(sidebar,
                           text='Limiar Alto',
                           width=8,
                           height=1,
                           bg="#5555FF",
                           fg="white",
                           command=lambda: display_result(filt.filtragem(file_array, filtro=filt.Filtro.media_alfa)))
btn_limiaralto.place(x=285, y=canny_y+20)

# Reconhecimento de Padrões

rec_y = canny_y+65
sidebar.create_text(
    14.0,
    rec_y,
    anchor="nw",
    text="Rec. de Padrões",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

btn_correlacao = tk.Button(sidebar,
                           text='Coef. Correl.',
                           width=8,
                           height=1,
                           bg="#5555FF",
                           fg="white",
                           command=lambda: display_result(
                               t.adjust_scale(
                                   rec.correlacao(
                                       file_array,
                                       sk.io.imread(
                                           "images/praticas/14/b_eye_template.tif"),
                                       best=False)
                               )))
btn_correlacao.place(x=14, y=rec_y+20)

btn_melhor = tk.Button(sidebar,
                       text='Melhor',
                       width=8,
                       height=1,
                       bg="#5555FF",
                       fg="white",
                       command=lambda: display_result(
                           t.adjust_scale(
                               m.dilatacao(rec.correlacao(
                                   file_array,
                                   sk.io.imread("images/praticas/14/b_eye_template.tif"), best=True), elemento=elemento)

                           )))
btn_melhor.place(x=100, y=rec_y+20)

# Widgets - Content

content.create_text(
    20,
    5,
    anchor="nw",
    text="Uploaded Image",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

file_array = sk.io.imread("images/noimage.jpg")
if len(file_array.shape) > 2:
    file_array = t.adjust_scale(rgb2gray(file_array))
image_file = Image.fromarray(file_array)

src_img = ImageTk.PhotoImage(image_file.resize(adjust_height(image_file.size)))
image1_id = content.create_image(
    20,
    40,
    anchor=tk.NW,
    image=src_img)

content.create_text(
    20,
    440,
    anchor="nw",
    text="Processed Image",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

prc_img_1 = ImageTk.PhotoImage(
    image_file.resize(adjust_height(image_file.size)))
image2_id = content.create_image(
    20,
    480,
    anchor=tk.NW,
    image=prc_img_1)

window.mainloop()
