import pygame as pg
from settings import *

class Renderer:
    def __init__(self, screen_dims):
        self.SCREEN = pg.display.set_mode(screen_dims)
        pg.display.set_caption("Game Of Life")
        self.clock = pg.time.Clock()
        self.cell_surface = pg.Surface(screen_dims)
        self.hover = None
    
    def update(self, delay):
        pg.display.set_caption(f"{round(self.clock.get_fps())} fps")
        pg.display.flip()
        self.clock.tick(delay)

    def draw_cells(self, list_cells, cellsize):
        self.cell_surface.fill(BLACK)
        black_cell = pg.Surface(cellsize)
        black_cell.fill(BLACK)
        white_cell = pg.Surface(cellsize)
        white_cell.fill(WHITE)
        for row_idx, row in enumerate(list_cells):
            for cell_idx, cell_nature in enumerate(row):
                cell_pos = (cell_idx * cellsize[0], row_idx * cellsize[1])

                if cell_nature == 0:
                    self.cell_surface.blit(black_cell, cell_pos)
                else:
                    self.cell_surface.blit(white_cell, cell_pos)
    
    def draw_hover(self, dims):
        self.hover = pg.Surface(size=dims)
        self.hover.fill(GREY)
    
    def blit_hover(self, grid_pos, cellsize):
        posx = grid_pos[0] * cellsize[0]
        posy = grid_pos[1] * cellsize[1]
        self.SCREEN.blit(self.hover, (posx, posy))
    
    def blit_cell_surface(self):
        self.SCREEN.blit(self.cell_surface, (0, 0))

    def update_cell_on_cell_surface(self, cell_grid_pos, cellsize, state):
        cell_pos = (cell_grid_pos[0] * cellsize[0], cell_grid_pos[1] * cellsize[1])

        if state == 0:
            color = BLACK
        else:
            color = WHITE
        
        cell_surface = pg.Surface(cellsize)
        cell_surface.fill(color)
        self.cell_surface.blit(cell_surface, cell_pos)

    
