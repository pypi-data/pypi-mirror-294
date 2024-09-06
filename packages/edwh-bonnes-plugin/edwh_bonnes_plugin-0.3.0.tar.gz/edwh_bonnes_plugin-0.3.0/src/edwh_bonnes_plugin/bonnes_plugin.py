from time import sleep

from invoke import task
from PIL import Image, ImageTk
import tkinter as tk
import random
import webbrowser

@task()
def yell(c):
    print("AAAAAAAaaaafdffAHHH")


def open_image(file_path, x, y):
    # Maak een Tkinter-venster
    root = tk.Tk()

    # Open de afbeelding met Pillow
    img = Image.open(file_path)

    # Converteer de Pillow-afbeelding naar een Tkinter-compatibel formaat
    tk_img = ImageTk.PhotoImage(img)

    # Maak een label om de afbeelding weer te geven
    label = tk.Label(root, image=tk_img)
    label.pack()

    # Stel de venstergrootte in op basis van de afbeeldingsgrootte
    root.geometry(f"{img.width}x{img.height}+{x}+{y}")

    # Houd een referentie naar de afbeelding
    root.image = tk_img

    # Start de Tkinter-loop
    root.mainloop()

@task()
def image(c):
    for x in range(3):
        open_image('assets/300px-Pug_600.jpg', x=random.randint(200, 1400), y=random.randint(0, 1200))

@task()
def open(c, a_way):
    match a_way:
        case 'base':
            webbrowser.open_new('https://educationwarehouse.org/nextcloud/apps/spreed/')
            webbrowser.open('https://realpython.com/python-virtual-environments-a-primer/#how-can-you-work-with-a-python-virtual-environment')
            webbrowser.open('https://www.perplexity.ai/')
        case 'talk':
            link = 'https://educationwarehouse.org/nextcloud/apps/spreed/'
        case 'pp':
            link = 'https://www.perplexity.ai/'
        case _:
            link = 'https://www.' + a_way + '.com/'
    webbrowser.open(link)