from main_menu import MainMenu
from random import randint
from dic_models import models, unpack
from draw import draw_grid
from input_handler import InputHandler
from renderer import Renderer

def get_grid_dims(screen_dims, cellsize):
    nb_col = screen_dims[0] // cellsize[0]
    nb_row = screen_dims[1] // cellsize[1]
    return nb_col, nb_row

def empty_grid(grid_dims: tuple[int, int]):
    return [[0 for _ in range(grid_dims[0])] for _ in range(grid_dims[1])]

def random_grid(grid_dims: tuple[int, int]):
    return [[randint(0, 1) for _ in range(grid_dims[0])] for _ in range(grid_dims[1])]

def get_model_list(model_name, grid_dims):

    marge_gauche = models[model_name][2][0]  # marge de "confort"
    marge_haut = models[model_name][2][1]

    list_cells = empty_grid(grid_dims)

    largeur_max = models[model_name][1][0] + marge_gauche
    hauteur_max = models[model_name][1][1] + marge_haut

    # marge_gauche = marge_defaut + round(largeur_max / 2)  # => glider gun : trop large pour ces conneries
    # marge_haut = marge_defaut + round(
    #    hauteur_max / 2)  # => j'ai très peur dans les futus ajouts, mieux vaut garder juste une marge de 2 en haut

    if largeur_max > grid_dims[0] or hauteur_max > grid_dims[1]:
        print(
            f"Les dimensions de l'écran sont trop petites pour le {model_name}: \n"
            f"{largeur_max}x{hauteur_max} requérits, contre : \n"
            f"{grid_dims[0]}x{grid_dims[1]} présentés \n"
            f"Veuillez augmenter les dimensions de l'écran ou diminuer "
            f"la taille des cellules "
        )

    model_data = unpack(model_name)

    for row_idx, row in enumerate(model_data):
        for cell_idx, cell in enumerate(row):
            list_cells[row_idx + marge_haut][cell_idx + marge_gauche] = cell
    return list_cells



def get_starting_grid_cells(menu: MainMenu):
    if menu.game_mode == "random":
        return random_grid(menu.grid_dims)
    if menu.game_mode == "model":
        return get_model_list(menu.selected_model, menu.grid_dims)
    if menu.game_mode == "draw":
        return draw_grid(menu.cellsize, menu.grid_dims, menu.screen_dims)


def main():
    menu = MainMenu()
    menu.show()
    cells_state = get_starting_grid_cells(menu)

    input_handler = InputHandler()
    renderer = Renderer(menu.screen_dims)

    running = True
    while running:
        
        input_handler.get_mouse_event()
        if input_handler.exit:
            running = False
        renderer.draw_cells(cells_state, menu.cellsize)
        renderer.blit_cell_surface()
        renderer.update(menu.delay)
        cells_state = get_next_gen(cells_state)



def get_next_gen(input_list_cells):
    output_list_cells = []

    # Précalcul des sommes des voisins pour toutes les cellules
    list_sum_neighbours = []
    for row_idx, row in enumerate(input_list_cells):
        output_row = []
        for cell_row_idx, cell in enumerate(row):
            live_neighbors = 0

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue

                    neighbor_row_idx = (row_idx + i) % len(input_list_cells)
                    neighbor_cell_row_idx = (cell_row_idx + j) % len(row)
                    live_neighbors += input_list_cells[neighbor_row_idx][neighbor_cell_row_idx]

            list_sum_neighbours.append(live_neighbors)

            # Application des règles du jeu de la vie de Conway
            if live_neighbors == 2:
                output_row.append(cell)

            elif live_neighbors == 3:
                output_row.append(1)

            else:
                output_row.append(0)

        output_list_cells.append(output_row)

    return output_list_cells
        
    





if __name__ == "__main__":
    print(True)
    main()