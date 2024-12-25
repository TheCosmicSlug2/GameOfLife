import pygame as pg
from renderer import Renderer
from input_handler import InputHandler


def empty_grid(grid_dims: tuple[int, int]):
    return [[0 for _ in range(grid_dims[0])] for _ in range(grid_dims[1])]

def draw_grid(cellsize, grid_dims, screen_dims) ->list:

    renderer = Renderer(screen_dims)
    renderer.draw_hover(cellsize)
    input_handler = InputHandler()
    list_cells = empty_grid(grid_dims)
    last_click = (0, 0)

    running = True
    while running:

        mouse_gridx, mouse_gridy = input_handler.get_mouse_grid_pos(cellsize)

        input_handler.get_mouse_event()
        if input_handler.exit:
            running = False
        if input_handler.click_on and (mouse_gridx, mouse_gridy) != last_click:
            if 0 <= mouse_gridx < grid_dims[0] and 0 <= mouse_gridy < grid_dims[1]:
                new_state =  1 - list_cells[mouse_gridy][mouse_gridx]
                list_cells[mouse_gridy][mouse_gridx] = new_state
                renderer.update_cell_on_cell_surface((mouse_gridx, mouse_gridy), cellsize, new_state)

                last_click = (mouse_gridx, mouse_gridy)
                
        renderer.blit_cell_surface()
        renderer.blit_hover((mouse_gridx, mouse_gridy), cellsize)
        renderer.update(100)

    return list_cells