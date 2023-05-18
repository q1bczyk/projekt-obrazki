import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

def wczytaj_obraz():
    # Otwórz okno dialogowe do wyboru pliku
    filepath = filedialog.askopenfilename(filetypes=[("Obrazy", "*.jpg;*.jpeg;*.png;*.gif")])

    # Sprawdź, czy plik został wybrany
    if filepath:
        # Wczytaj obraz przy użyciu biblioteki PIL
        obraz = Image.open(filepath)

        # Dostosuj szerokość obrazu
        szerokosc_obrazu = int(root.winfo_width() * 0.4)
        wysokosc_obrazu = int(szerokosc_obrazu * obraz.height / obraz.width)
        obraz = obraz.resize((szerokosc_obrazu, wysokosc_obrazu))

        # Konwertuj obraz do formatu obsługiwanego przez tkinter
        obraz_tk = ImageTk.PhotoImage(obraz)

        # Utwórz div obraz i umieść w nim dostosowany obraz
        div_obraz = tk.Label(root, image=obraz_tk)
        div_obraz.pack(side=tk.RIGHT, padx=10, pady=10)

        # Przechowaj referencję do obrazu, aby uniknąć problemów z garbage collectorem
        div_obraz.image = obraz_tk

        # Dodaj drugi obraz o tych samych rozmiarach
        drugi_obraz = ImageTk.PhotoImage(obraz)
        div_drugi_obraz = tk.Label(root, image=drugi_obraz)
        div_drugi_obraz.pack(side=tk.LEFT, padx=10, pady=10)
        div_drugi_obraz.image = drugi_obraz

root = tk.Tk()
root.geometry("800x600")

button = tk.Button(root, text="Wczytaj obraz", command=wczytaj_obraz)
button.pack()

div_pojemnik = tk.Frame(root, bg="red", height=200)
div_pojemnik.pack(fill=tk.X)

button_angielski = tk.Button(div_pojemnik, text="Angielski")
button_angielski.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

button_czarnoBialy = tk.Button(div_pojemnik, text="Czarno-biały")
button_czarnoBialy.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

button_czarnoBialy = tk.Button(div_pojemnik, text="Czarno-biały")
button_czarnoBialy.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

button_zaszumienie = tk.Button(div_pojemnik, text="Zaszumienie obrazu")
button_zaszumienie.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

button_normalizacja = tk.Button(div_pojemnik, text="Normalizacja")
button_normalizacja.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

button_maski = tk.Button(div_pojemnik, text="Maski")
button_maski.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

root.mainloop()