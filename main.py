import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image

# --------------- GUI window

root = tk.Tk();

# --------------- STYLING

styles = ttk.Style()
styles.configure('mainFrame.TFrame', background='#e9ecef')
styles.configure('loadImageFrame.TFrame', background='#e9ecef', height=420)
styles.configure('buttonsFrame.TFrame', background='#e9ecef')
styles.configure('originalPhotosFrame.TFrame', background='blue')
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

loadFileButton = ttk.Button(loadImageFrame, text="Wczytaj zdjęcie", style='custom.TButton')
def load_image_to_container():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        resized_image = image.resize((400, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        image_label = ttk.Label(originalPhotoFrame, image=photo)
        image_label.photo = photo
        image_label.pack(fill='both', expand=True)

loadFileButton.config(command=load_image_to_container)
loadFileButton.grid(row=1, column=1, padx=10, pady=10)

saveFileButton = ttk.Button(loadImageFrame, text="Zapisz zdjęcie", style='custom.TButton')
saveFileButton.grid(row=2, column=1, padx=10, pady=10)

changToEnglishButton = ttk.Button(buttonsFrame, text="Angielski", style='custom.TButton')
changToEnglishButton.grid(row=1, column=1, padx=10, pady=10)

blackAndWhiteButton = ttk.Button(buttonsFrame, text="Czarno-Białe", style='custom.TButton')
blackAndWhiteButton.grid(row=1, column=2, padx=10, pady=10)

normalizeButton = ttk.Button(buttonsFrame, text="Normalizacja", style='custom.TButton')
normalizeButton.grid(row=1, column=3, padx=10, pady=10)

# --------------- GRID CONFIGURATIONS




root.resizable(width = False, height = False)
root.mainloop()