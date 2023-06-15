import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from functools import partial
from PIL import Image, ImageOps

# --------------- NORMALIZATION

def applyTrimmedNormalization(image):
    width, height = image.size
    pixels = image.load()

    values = []
    for x in range(width):
        for y in range(height):
            pixel = pixels[x, y]
            if isinstance(pixel, int):
                # Obraz czarno-biały (tryb "L")
                values.append(pixel)
            else:
                # Obraz RGB
                values.extend(pixel)

    values.sort()
    trimmed_values = values[int(0.1 * len(values)):int(0.9 * len(values))]
    min_value = trimmed_values[0]
    max_value = trimmed_values[-1]

    normalized_image = Image.new('RGB', (width, height))

    for x in range(width):
        for y in range(height):
            pixel = pixels[x, y]
            if isinstance(pixel, int):
                # Obraz czarno-biały (tryb "L")
                normalized_pixel = int(255 * (pixel - min_value) / (max_value - min_value))
            else:
                # Obraz RGB
                normalized_pixel = tuple(int(255 * (channel - min_value) / (max_value - min_value)) for channel in pixel)
            normalized_image.putpixel((x, y), normalized_pixel)

    return normalized_image


def applyScaledNormalization(image):
    width, height = image.size
    pixels = image.load()

    min_value = float('inf')
    max_value = float('-inf')
    if image.mode == "L":
        # Obraz czarno-biały (tryb "L")
        for x in range(width):
            for y in range(height):
                pixel = pixels[x, y]
                min_value = min(min_value, pixel)
                max_value = max(max_value, pixel)
    elif image.mode == "RGB":
        # Obraz RGB
        for x in range(width):
            for y in range(height):
                pixel = pixels[x, y]
                min_value = min(min_value, min(pixel))
                max_value = max(max_value, max(pixel))

    normalized_image = Image.new(image.mode, (width, height))

    for x in range(width):
        for y in range(height):
            pixel = pixels[x, y]
            if image.mode == "L":
                normalized_pixel = int(255 * (pixel - min_value) / (max_value - min_value))
            elif image.mode == "RGB":
                normalized_pixel = tuple(int(255 * (channel - min_value) / (max_value - min_value)) for channel in pixel)
            normalized_image.putpixel((x, y), normalized_pixel)

    return normalized_image

def applyAbsoluteNormalization(image):
    width, height = image.size
    pixels = image.load()

    max_value = 0
    if image.mode == "L":
        # Obraz czarno-biały (tryb "L")
        for x in range(width):
            for y in range(height):
                pixel = pixels[x, y]
                max_value = max(max_value, pixel)
    elif image.mode == "RGB":
        # Obraz RGB
        for x in range(width):
            for y in range(height):
                pixel = pixels[x, y]
                max_value = max(max_value, max(pixel))

    normalized_image = Image.new(image.mode, (width, height))

    for x in range(width):
        for y in range(height):
            pixel = pixels[x, y]
            if image.mode == "L":
                normalized_pixel = int(255 * pixel / max_value)
            elif image.mode == "RGB":
                normalized_pixel = tuple(int(255 * channel / max_value) for channel in pixel)
            normalized_image.putpixel((x, y), normalized_pixel)

    return normalized_image


# --------------- OPTIONS MODEL

class FilterHandler:

    mask = None
    normalization = None

    def config(self, mask, norm):
        self.mask = mask
        self.normalization = norm

# --------------- GLOBAL

is_black_and_white = False
original_image = None
filterHandler = FilterHandler()

# --------------- FUNCTIONS

def loadFile(container):
    global original_image

    file_path = filedialog.askopenfilename()
    for widget in container.winfo_children():
        widget.destroy()
    if file_path:
        image = Image.open(file_path)
        resized_image = image.resize((400, 400), Image.LANCZOS)
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
        resized_image = grayscale_image.resize((400, 400), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        image_label.configure(image=photo)
        image_label.photo = photo
        is_black_and_white = True

def saveFile():
    global filtered_image

    if filtered_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".png")
        if save_path:
            filtered_image.save(save_path)

def changeLanguage():
    current_language = changeToEnglishButton['text']
    if current_language == "Angielski":
        changeToEnglishButton.config(text="Polski")
        loadFileButton.config(text="Load Image")
        filterButton.config(text="Filter")
        saveFileButton.config(text="Save Image")
        blackAndWhiteButton.config(text="Black & White")
        normalizeButton.config(text="Normalization")
        masksOptions = ["Masks", "Laplace 3x3", "Sobela poziomo", "Sobela poziomo", "Prewitta poziomo", "Prewitta pionowo", "Różnicowa"]
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
        masksOptions = ["Maski", "Laplace 3x3", "Sobela poziomo", "Sobela poziomo", "Prewitta poziomo", "Prewitta pionowo","Różnicowa",]
        choosenMasksOption.set(masksOptions[0])
        normalizationOptions = ["Normalizacja", "Bezwzględna", "Skalowana", "Z obcięciem"]
        choosenNormalizationOption.set(normalizationOptions[0])
        normalizeButton["menu"].delete(0, "end")
        for option in normalizationOptions:
            normalizeButton["menu"].add_command(label=option, command=tk._setit(choosenNormalizationOption, option))

def applyHighPassFilter(image, kernel):
    width, height = image.size
    pixels = image.load()

    if image.mode == "L":
        # Obraz czarno-biały
        filtered_image = Image.new('L', (width, height))
        for x in range(1, width - 1):
            for y in range(1, height - 1):
                intensity_sum = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        pixel = pixels[x + i, y + j]
                        intensity_sum += pixel * kernel[(i + 1) * 3 + (j + 1)]
                intensity_sum = max(min(int(intensity_sum), 255), 0)
                filtered_image.putpixel((x, y), intensity_sum)
    else:
        # Obraz RGB
        filtered_image = Image.new('RGB', (width, height))
        for x in range(1, width - 1):
            for y in range(1, height - 1):
                r_sum = 0
                g_sum = 0
                b_sum = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        pixel = pixels[x + i, y + j]
                        r_sum += pixel[0] * kernel[(i + 1) * 3 + (j + 1)]
                        g_sum += pixel[1] * kernel[(i + 1) * 3 + (j + 1)]
                        b_sum += pixel[2] * kernel[(i + 1) * 3 + (j + 1)]
                r_sum = max(min(int(r_sum), 255), 0)
                g_sum = max(min(int(g_sum), 255), 0)
                b_sum = max(min(int(b_sum), 255), 0)
                filtered_image.putpixel((x, y), (r_sum, g_sum, b_sum))

    return filtered_image

def applyFilter():
    global original_image, filtered_image, filterHandler

    filtered_image = original_image.copy()
    if(is_black_and_white == True):
        filtered_image = ImageOps.grayscale(filtered_image)

    mask = filterHandler.mask
    normalization = filterHandler.normalization
    if mask == "Laplace 3x3":
        kernel = [0,  1,  0,  1,  -4,  1,  0,  1,  0]
        filtered_image = applyHighPassFilter(filtered_image, kernel)
    elif mask == "Sobela poziomo":
        kernel = [-1, -2, -1,  0,  0,  0,  1,  2,  1]
        filtered_image = applyHighPassFilter(filtered_image, kernel)
    elif mask == "Sobela pionowo":
        kernel = [-1,  0,  1,  -2,  0,  2,  -1,  0,  1]
        filtered_image = applyHighPassFilter(filtered_image, kernel)
    elif mask == "Prewitta poziomo":
        kernel = [-1,  -1,  -1,  0,  0,  0,  1,  1,  1]
        filtered_image = applyHighPassFilter(filtered_image, kernel)
    elif mask == "Prewitta pionowo":
        kernel = [-1,  0,  1, -1,  0,  1, -1,  0,  1]
        filtered_image = applyHighPassFilter(filtered_image, kernel)
    elif mask == "Różnicowa":
        kernel = [-1, -1, -1, -1, 8, -1, -1, -1, -1]
        filtered_image = applyHighPassFilter(filtered_image, kernel)

    if (normalization == "Absolute" or normalization == "Bezwzględna"):
        filtered_image = applyAbsoluteNormalization(filtered_image)
    elif (normalization == "Scaled" or normalization == "Skalowana"):
        filtered_image = applyScaledNormalization(filtered_image)
    elif (normalization == "Trimmed" or normalization == "Z obcięciem"):
        filtered_image = applyTrimmedNormalization(filtered_image)

    for widget in filteredPhotoFrame.winfo_children():
        widget.destroy()

    if filtered_image:
        resized_image = filtered_image.resize((400, 400), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        image_label = ttk.Label(filteredPhotoFrame, image=photo)
        image_label.photo = photo
        image_label.pack(fill='both', expand=True)



def setFilter():
    mask = choosenMasksOption.get()
    norm = choosenNormalizationOption.get()
    filterHandler.config(mask, norm)
    applyFilter()

# --------------- GUI window

root = tk.Tk()
root.title("Filtr Górnoprzepustowy")
root.resizable(width=False, height=False)

masksOptions = ["Maski", "Laplace 3x3", "Sobela poziomo", "Sobela pionowo", "Prewitta poziomo","Prewitta pionowo", "Różnicowa"]
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
styles.configure('filteredPhotosFrame.TFrame', background='#e9ecef')
styles.configure('custom.TButton', bg='#c1121f', foreground='black', padding=5, border=10, width=20)

# --------------- WIDGETS
mainFrame = ttk.Frame(root, width=1280, height=720, style='mainFrame.TFrame')
mainFrame.grid(row=0, column=0)

title_label = ttk.Label(mainFrame, text="Filtr górnoprzepustowy", font=("Arial", 16), style='mainFrame.TLabel')
title_label.grid(row=0, column=2, padx=10, pady=10)

loadImageFrame = ttk.Frame(mainFrame, width=124, height=420, style='loadImageFrame.TFrame')
loadImageFrame.grid(row=3, column=4, padx=10, pady=10, rowspan=3)

buttonsFrame = ttk.Frame(mainFrame, width=900, height=50, style='buttonsFrame.TFrame')
buttonsFrame.grid(row=4, column=1, padx=10, pady=10, columnspan=3)

photosFrame = ttk.Frame(mainFrame, width=900, height=350)
photosFrame.grid(row=3, column=1, padx=10, pady=10, columnspan=3)

originalPhotoFrame = ttk.Frame(photosFrame, width=420, height=350, style='originalPhotosFrame.TFrame')
originalPhotoFrame.grid(row=1, column=1, padx=10, pady=10)

filteredPhotoFrame = ttk.Frame(photosFrame, width=420, height=350, style='filteredPhotosFrame.TFrame')
filteredPhotoFrame.grid(row=1, column=2, padx=10, pady=10)

# --------------- BUTTONS
changeToEnglishButton = ttk.Button(loadImageFrame, text="Angielski", style='custom.TButton', command=changeLanguage)
changeToEnglishButton.grid(row=1, column=1, padx=10, pady=10)

loadFileButton = ttk.Button(loadImageFrame, text="Wczytaj zdjęcie", style='custom.TButton', command=partial(loadFile, originalPhotoFrame))
loadFileButton.grid(row=2, column=1, padx=10, pady=10)

filterButton = ttk.Button(loadImageFrame, text="Filtruj", style='custom.TButton', command=setFilter)
filterButton.grid(row=3, column=1, padx=10, pady=10)

saveFileButton = ttk.Button(loadImageFrame, text="Zapisz zdjęcie", style='custom.TButton', command=saveFile)
saveFileButton.grid(row=4, column=1, padx=10, pady=10)

blackAndWhiteButton = ttk.Button(buttonsFrame, text="Czarno-Białe", style='custom.TButton', command=partial(convertToBlackAndWhite, originalPhotoFrame))
blackAndWhiteButton.grid(row=4, column=1, padx=10, pady=10)

normalizeButton = ttk.OptionMenu(buttonsFrame, choosenNormalizationOption, *normalizationOptions, style='custom.TButton')
normalizeButton.grid(row=4, column=2, padx=10, pady=10)

masksMenu = ttk.OptionMenu(buttonsFrame, choosenMasksOption, *masksOptions, style='custom.TButton')
masksMenu.grid(row=4, column=3, padx=10, pady=10)

root.mainloop()



# --------------- GRID CONFIGURATIONS

root.mainloop()

