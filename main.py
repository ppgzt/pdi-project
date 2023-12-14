import tkinter as tk
import skimage as sk
import numpy as np

from tkinter import filedialog
from tkinter.filedialog import askopenfile

from skimage.color import rgb2gray
from PIL import Image, ImageTk

from pdi import transformation as t
from pdi import histograma as h
from pdi import pseudocores as p
from pdi import filtragem as filt
from pdi import fourier

# Functions


def adjust_height(size, max_height=350):
    return tuple([int(max_height/size[1] * x) for x in size])


def upload_file():
    global src_img, file_array
    types = [('Tif Files', '*.tif'), ('Webp', '*.webp')]

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

# Fourier #

fourier_y = fpseudo + 65
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
