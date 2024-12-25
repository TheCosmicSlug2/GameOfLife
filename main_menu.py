import tkinter as tk
from tkinter import ttk
from dic_models import models

class MainMenu:
    def __init__(self):
        self.game_mode = None
        self.cellsize = None
        self.screen_dims = None
        self.delay = None
        self.selected_model = None
    
    def random(self):
        self.game_mode = "random"
        self.get_widget_values()
        self.root.destroy()
    
    def draw(self):
        self.game_mode = "draw"
        self.get_widget_values()
        self.root.destroy()
    
    def model(self):
        self.game_mode = "model"
        self.get_widget_values()
        self.selected_model = self.model_combobox.get()
        self.root.destroy()

    def get_widget_values(self):
        self.cellsize = (self.slider_cell_size.get(), self.slider_cell_size.get())
        self.screen_dims = (self.slider_screen_dims.get(), self.slider_screen_dims.get())
        self.delay = self.slider_delay.get()
        self.grid_dims = (self.screen_dims[0] // self.cellsize[0], self.screen_dims[1] // self.cellsize[1])
    

    def show(self):
        # Création de la fenêtre
        self.root = tk.Tk()
        self.root.title("Menu")

        # Frame pour les boutons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Bouton "Random"
        random_button = tk.Button(button_frame, text="Random", command=self.random)
        random_button.grid(row=0, column=0, padx=5)

        # Bouton "Empty"s
        empty_button = tk.Button(button_frame, text="draw", command=self.draw)
        empty_button.grid(row=0, column=1, padx=5)

        or_label = tk.Label(button_frame, text="or")
        or_label.grid(row=0, column=2, padx=5)

        # Frame pour le menu déroulant
        model_frame = tk.Frame(self.root)
        model_frame.pack(pady=10)

        # Liste de modèles
        combo_values = list(models.keys())

        # Menu déroulant (combobox)
        self.model_combobox = ttk.Combobox(model_frame, values=combo_values)
        self.model_combobox.set("Select Model")
        self.model_combobox.grid(row=0, column=0, padx=5)

        # Bouton de sélection de modèle
        select_button = tk.Button(model_frame, text="Select", command=self.model)
        select_button.grid(row=0, column=1, padx=5)

        # frame pour taille cellule

        frame_cell_size = tk.Frame(self.root)
        frame_cell_size.pack(pady=10)

        # label et slider
        label_cell_size = tk.Label(frame_cell_size, text="taille cellule")
        label_cell_size.grid(row=0, column=0, padx=5)
        self.slider_cell_size = tk.Scale(frame_cell_size, from_=1, to=10, orient="horizontal")
        self.slider_cell_size.set(10)
        self.slider_cell_size.grid(row=0, column=1, padx=5)

        # frame pour size fenêtre

        frame_grid_size = tk.Frame(self.root, pady=10)
        frame_grid_size.pack()

        # label et slider
        label_grid_size = tk.Label(frame_grid_size, text="largeur/hauteur")
        label_grid_size.grid(row=0, column=0, padx=5)
        self.slider_screen_dims = tk.Scale(frame_grid_size, from_=200, to=600, orient="horizontal")
        self.slider_screen_dims.grid(row=0, column=1, padx=5)
        self.slider_screen_dims.set(400)

        # frame pour delay
        frame_delay = tk.Frame(self.root, pady=10)
        frame_delay.pack()

        label_delay = tk.Label(frame_delay, text="delai (1/100s)")
        label_delay.grid(row=0, column=0, padx=5)

        self.slider_delay = tk.Scale(frame_delay, from_=0, to=100, orient="horizontal")
        self.slider_delay.grid(row=0, column=1, padx=5)

        self.root.mainloop()