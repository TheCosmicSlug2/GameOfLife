import time
import pygame as pg
import random as rd
import dic_models
import tkinter as tk
from tkinter import ttk

local_dic_models = dic_models.models

"""
1.5 fois plus rapide que Type2 => Un BIJOU malgré ses défauts
"""

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)

SCREEN: pg.surface


class DimensionTropPetites(Exception):
    pass


def main_menu():

    def select_random():
        pg.init()
        game(globalcellsize=int(slider_cell_size.get()),
             grid_dim=int(slider_grid_size.get()),
             delay=float(slider_delay.get() / 100),
             random=True)


    def select_draw():
        pg.init()
        game(globalcellsize=int(slider_cell_size.get()),
             grid_dim=int(slider_grid_size.get()),
             delay=float(slider_delay.get() / 100),
             draw=True)

    # Création de la fenêtre
    root = tk.Tk()
    root.title("Menu")

    # Frame pour les boutons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Bouton "Random"
    random_button = tk.Button(button_frame, text="Random", command=select_random)
    random_button.grid(row=0, column=0, padx=5)

    # Bouton "Empty"s
    empty_button = tk.Button(button_frame, text="draw", command=select_draw)
    empty_button.grid(row=0, column=1, padx=5)

    or_label = tk.Label(button_frame, text="or")
    or_label.grid(row=0, column=2, padx=5)

    # Frame pour le menu déroulant
    model_frame = tk.Frame(root)
    model_frame.pack(pady=10)

    # Liste de modèles
    combo_values = list(local_dic_models.keys())

    # Menu déroulant (combobox)
    model_combobox = ttk.Combobox(model_frame, values=combo_values)
    model_combobox.set("Select Model")
    model_combobox.grid(row=0, column=0, padx=5)


    def select_model():
        pg.init()
        selected_model = model_combobox.get()
        if selected_model in combo_values:  # On empêche l'user d'écrire de la merde et que ça fasse foirer le programme
            if selected_model.startswith("--"):
                return
            else:
                game(globalcellsize=int(slider_cell_size.get()),
                     grid_dim=int(slider_grid_size.get()),
                     delay=float(slider_delay.get() / 100),
                     model=selected_model)

    # Bouton de sélection de modèle
    select_button = tk.Button(model_frame, text="Select", command=select_model)
    select_button.grid(row=0, column=1, padx=5)

    # frame pour taille cellule

    frame_cell_size = tk.Frame(root)
    frame_cell_size.pack(pady=10)

    # label et slider
    label_cell_size = tk.Label(frame_cell_size, text="taille cellule")
    label_cell_size.grid(row=0, column=0, padx=5)
    slider_cell_size = tk.Scale(frame_cell_size, from_=1, to=10, orient="horizontal")
    slider_cell_size.set(10)
    slider_cell_size.grid(row=0, column=1, padx=5)

    # frame pour size fenêtre

    frame_grid_size = tk.Frame(root, pady=10)
    frame_grid_size.pack()

    # label et slider
    label_grid_size = tk.Label(frame_grid_size, text="largeur/hauteur")
    label_grid_size.grid(row=0, column=0, padx=5)
    slider_grid_size = tk.Scale(frame_grid_size, from_=200, to=600, orient="horizontal")
    slider_grid_size.grid(row=0, column=1, padx=5)
    slider_grid_size.set(400)

    # frame pour delay
    frame_delay = tk.Frame(root, pady=10)
    frame_delay.pack()

    label_delay = tk.Label(frame_delay, text="delai (1/100s)")
    label_delay.grid(row=0, column=0, padx=5)

    slider_delay = tk.Scale(frame_delay, from_=0, to=100, orient="horizontal")
    slider_delay.grid(row=0, column=1, padx=5)

    root.mainloop()


def game(globalcellsize, grid_dim, delay, draw=None, random=None, model=None):
    global SCREEN

    cellsize = globalcellsize

    grid_size = int(grid_dim / cellsize)

    SCREEN = pg.display.set_mode((grid_dim, grid_dim))

    if draw:
        list_cells = draw_grid(cellsize, grid_size)
    elif random:
        list_cells = random_grid(grid_size)
    elif model:
        list_cells = models_grid(local_dic_models, model, grid_size)
    else:
        print("Aucune valeur pour liste_cells")
        list_cells = [] # <- pour éviter les erreurs de pycharm

    gen_idx = 0
    start_time = time.time()
    time.sleep(0)


    def update_fps():
        time.sleep(delay)
        current_time = time.time()
        fps = gen_idx / (current_time - start_time)
        pg.display.set_caption(f"gen : {gen_idx} / fps : {fps:.2f}")

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False # changé pygame.quit() à ça, car s'il faut que ça plante quand on ferme la fenêtre, autant maîtriser le truc

        draw_cells(list_cells=list_cells, size=cellsize, unit_block_size=grid_size)
        update_fps()
        list_cells = get_next_gen(input_list_cells=list_cells)
        gen_idx += 1
    
    pg.quit()


def get_next_gen(input_list_cells):
    output_list_cells = []

    # Précalcul des sommes des voisins pour toutes les cellules
    list_sum_neighbours = []
    for row_idx, row in enumerate(input_list_cells):
        output_row = []
        for cell_row_idx, cell in enumerate(row):
            abs_state = cell[0]
            live_neighbors = 0

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue

                    neighbor_row_idx = (row_idx + i) % len(input_list_cells)
                    neighbor_cell_row_idx = (cell_row_idx + j) % len(row)
                    live_neighbors += input_list_cells[neighbor_row_idx][neighbor_cell_row_idx][1]

            list_sum_neighbours.append(live_neighbors)

            # Application des règles du jeu de la vie de Conway
            if live_neighbors == 2:
                output_row.append(cell)

            elif live_neighbors == 3:
                output_row.append((abs_state, 1))

            else:
                output_row.append((abs_state, 0))

        output_list_cells.append(output_row)

    return output_list_cells



def models_grid(models, model_name, win_size) ->list:
    marge_gauche = models[model_name][2][0]  # marge de "confort"
    marge_haut = models[model_name][2][1]

    list_cells = empty_grid(win_size)

    largeur_max = models[model_name][1][0] + marge_gauche
    hauteur_max = models[model_name][1][1] + marge_haut

    # marge_gauche = marge_defaut + round(largeur_max / 2)  # => glider gun : trop large pour ces conneries
    # marge_haut = marge_defaut + round(
    #    hauteur_max / 2)  # => j'ai très peur dans les futus ajouts, mieux vaut garder juste une marge de 2 en haut

    if largeur_max > win_size or hauteur_max > win_size:
        raise DimensionTropPetites(
            f"Les dimensions de l'écran sont trop petites pour le {model_name}: \n"
            f"{largeur_max}x{hauteur_max} requérits, contre : \n"
            f"{win_size}x{win_size} présentés \n"
            f"Veuillez augmenter les dimensions de l'écran ou diminuer "
            f"la taille des cellules "
        )

    idx_row = marge_haut
    for row in models[model_name][0]:

        if row[0] not in ["-", "*"]:  # dans le cas où il faut répéter la même ligne
            rep = int(row[0])
            row_a_rep = row[1:]

            for i in range(rep):

                idx_cell = 0
                for cell_state in row_a_rep:
                    if cell_state == "-":
                        list_cells[idx_row][idx_cell + marge_gauche][1] = 0
                    if cell_state == "*":
                        list_cells[idx_row][idx_cell + marge_gauche][1] = 1
                    idx_cell += 1

                idx_row += 1

        else:
            idx_cell = 0
            for cell_state in row:
                if cell_state == "-":
                    list_cells[idx_row][idx_cell + marge_gauche][1] = 0
                if cell_state == "*":
                    list_cells[idx_row][idx_cell + marge_gauche][1] = 1
                idx_cell += 1
            idx_row += 1

    return list_cells


def random_grid(win_size) ->list:
    list_cells = []
    inside = []

    for row in range(win_size):
        for col in range(win_size):
            inside.append([(row * win_size + col), rd.randint(0, 1)])
        list_cells.append(inside)
        inside = []

    return list_cells


def draw_grid(unit_cell, win_size) ->list:
    list_cells = empty_grid(win_size)
    grid_size = win_size

    running = True
    while running:

        cell_position = pg.mouse.get_pos()

        x = cell_position[0] // unit_cell
        y = cell_position[1] // unit_cell

        if 0 <= x < grid_size and 0 <= y < grid_size:  # pour créer un "hover" qui colorie la case en gris quand la souris passe dessus
            cell = pg.Rect(x * unit_cell, y * unit_cell, unit_cell, unit_cell)
            pg.draw.rect(SCREEN, GREY, cell, 10)
            pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # Si le bouton gauche de la souris est enfoncé
                if 0 <= x < grid_size and 0 <= y < grid_size:
                    list_cells[y][x][1] = 1 - list_cells[y][x][1]

        draw_cells(list_cells, unit_cell, grid_size)  # chiant parce qu'on doit draw ttes les cellules dcp

    return list_cells


def empty_grid(win_size) ->list:
    list_cells = []
    inside = []

    for row in range(win_size):
        for col in range(win_size):
            inside.append([(row * win_size + col), 0])
        list_cells.append(inside)
        inside = []

    return list_cells


"""
def draw_grid(unit, win_width, win_height):
    for x in range(0, win_width, unit):
        for y in range(0, win_height, unit):
            rect = pg.Rect(x, y, unit, unit)
            pg.draw.rect(SCREEN, WHITE, rect, 1)
"""


def draw_cells(list_cells, size, unit_block_size):
    for row in list_cells:
        for cell_stat in row:
            pos = cell_stat[0]

            # dessiner la cellule

            x = pos % unit_block_size
            y = pos // unit_block_size
            cell = pg.Rect(x * size, y * size, size, size)

            if cell_stat[1] == 0:
                pg.draw.rect(SCREEN, BLACK, cell, 10)
            else:
                pg.draw.rect(SCREEN, WHITE, cell, 10)
    pg.display.update()


main_menu()



"""
deepcopy est beacoup plus lente : dcp ne marche pas : obligé de rfaire une itération
"""