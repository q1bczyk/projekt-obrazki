import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from functools import partial
from gray_scale import convertToGrayscale, displayGrayscale
from PIL import Image, ImageOps

# --------------- GLOBAL

is_black_and_white = False
original_image = None

# --------------- FUNCTIONS

def loadFile(container):
    global original_image

    file_path = filedialog.askopenfilename()
    for widget in container.winfo_children():
        widget.destroy()
    if file_path:
        image = Image.open(file_path)
        resized_image = image.resize((400, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        image_label = ttk.Label(container, image=photo)
        image_label.photo = photo
        image_label.pack(fill='both', expand=True)
        original_image = resized_image.copy()

def convertToBlackAndWhite(container):
    global is_black_and_white, original_image

    if is_black_and_white:
        image_label = container.winfo_children()[0]
        photo = ImageTk.PhotoImage(original_image)
        image_label.configure(image=photo)
        image_label.photo = photo
        is_black_and_white = False
    else:
        image_label = container.winfo_children()[0]
        photo = image_label.photo
        image = ImageTk.getimage(photo)
        grayscale_image = ImageOps.grayscale(image)
        resized_image = grayscale_image.resize((400, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        image_label.configure(image=photo)
        image_label.photo = photo
        is_black_and_white = True

def changeLanguage():
    current_language = changeToEnglishButton['text']
    if current_language == "Angielski":
        changeToEnglishButton.config(text="Polski")
        loadFileButton.config(text="Load Image")
        filterButton.config(text="Filter")
        saveFileButton.config(text="Save Image")
        blackAndWhiteButton.config(text="Black & White")
        normalizeButton.config(text="Normalization")
        masksOptions = ["Masks", "Mask 1", "Mask 2", "Mask 3", "Mask 4"]
        choosenMasksOption.set(masksOptions[0])
        normalizationOptions = ["Normalization", "Absolute", "Scaled", "Trimmed"]
        choosenNormalizationOption.set(normalizationOptions[0])
        normalizeButton["menu"].delete(0, "end")
        for option in normalizationOptions:
            normalizeButton["menu"].add_command(label=option, command=tk._setit(choosenNormalizationOption, option))
    else:
        changeToEnglishButton.config(text="Angielski")
        loadFileButton.config(text="Wczytaj zdjęcie")
        filterButton.config(text="Filtruj")
        saveFileButton.config(text="Zapisz zdjęcie")
        blackAndWhiteButton.config(text="Czarno-Białe")
        normalizeButton.config(text="Normalizacja")
        masksOptions = ["Maski", "maska 1", "maska 2", "maska 3", "maska 4"]
        choosenMasksOption.set(masksOptions[0])
        normalizationOptions = ["Normalizacja", "Bezwzględna", "Skalowana", "Z obcięciem"]
        choosenNormalizationOption.set(normalizationOptions[0])
        normalizeButton["menu"].delete(0, "end")
        for option in normalizationOptions:
            normalizeButton["menu"].add_command(label=option, command=tk._setit(choosenNormalizationOption, option))

# --------------- GUI window

root = tk.Tk()

masksOptions = ["Maski", "maska 1", "maska 2", "maska 3", "maska 4"]
choosenMasksOption = tk.StringVar(root)
choosenMasksOption.set(masksOptions[0])

normalizationOptions = ["Normalizacja", "Bezwzględna", "Skalowana", "Z obcięciem"]
choosenNormalizationOption = tk.StringVar(root)
choosenNormalizationOption.set(normalizationOptions[0])

# --------------- STYLING

styles = ttk.Style()
styles.configure('mainFrame.TFrame', background='#e9ecef')
styles.configure('loadImageFrame.TFrame', background='#e9ecef', height=420)
styles.configure('buttonsFrame.TFrame', background='#e9ecef')
styles.configure('originalPhotosFrame.TFrame', background='#e9ecef')
styles.configure('filteredPhotosFrame.TFrame', background='green')
styles.configure('custom.TButton', bg='#c1121f', foreground='black', padding=5, border=10, width=20)

# --------------- WIDGETS

mainFrame = ttk.Frame(root, width=1280, height=720, style='mainFrame.TFrame')
mainFrame.grid(row=0, column=0)

loadImageFrame = ttk.Frame(mainFrame, width=124, height=420, style='loadImageFrame.TFrame')
loadImageFrame.grid(row=1, column=2, padx=10, pady=10, rowspan=3)

buttonsFrame = ttk.Frame(mainFrame, width=900, height=50, style='buttonsFrame.TFrame')
buttonsFrame.grid(row=1, column=1, padx=10, pady=10)

photosFrame = ttk.Frame(mainFrame, width=900, height=350)
photosFrame.grid(row=2, column=1, padx=10, pady=10)

originalPhotoFrame = ttk.Frame(photosFrame, width=420, height=350, style='originalPhotosFrame.TFrame')
originalPhotoFrame.grid(row=1, column=1, padx=10, pady=10)

filteredPhotoFrame = ttk.Frame(photosFrame, width=420, height=350, style='filteredPhotosFrame.TFrame')
filteredPhotoFrame.grid(row=1, column=2, padx=10, pady=10)

# --------------- BUTTONS

changeToEnglishButton = ttk.Button(loadImageFrame, text="Angielski", style='custom.TButton', command=changeLanguage)
changeToEnglishButton.grid(row=1, column=1, padx=10, pady=10)

loadFileButton = ttk.Button(loadImageFrame, text="Wczytaj zdjęcie", style='custom.TButton', command=partial(loadFile, originalPhotoFrame))
loadFileButton.grid(row=2, column=1, padx=10, pady=10)

filterButton = ttk.Button(loadImageFrame, text="Filtruj", style='custom.TButton')
filterButton.grid(row=3, column=1, padx=10, pady=10)

saveFileButton = ttk.Button(loadImageFrame, text="Zapisz zdjęcie", style='custom.TButton')
saveFileButton.grid(row=4, column=1, padx=10, pady=10)

blackAndWhiteButton = ttk.Button(buttonsFrame, text="Czarno-Białe", style='custom.TButton', command=partial(convertToBlackAndWhite, originalPhotoFrame))
blackAndWhiteButton.grid(row=2, column=1, padx=10, pady=10)

normalizeButton = ttk.OptionMenu(buttonsFrame, choosenNormalizationOption, *normalizationOptions, style='custom.TButton')
normalizeButton.grid(row=2, column=2, padx=10, pady=10)

masksMenu = ttk.OptionMenu(buttonsFrame, choosenMasksOption, *masksOptions, style='custom.TButton')
masksMenu.grid(row=2, column=3, padx=10, pady=10)

# --------------- GRID CONFIGURATIONS

root.resizable(width=False, height=False)
root.mainloop()
