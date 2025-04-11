import pygame as pg

class InputHandler:
    def __init__(self):
        self.exit = False
        self.click_on = False
        self.new = False

    def get_mouse_event(self):
        self.new = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit = True
            if event.type == pg.MOUSEBUTTONDOWN:
                self.click_on = True
            if event.type == pg.MOUSEBUTTONUP:
                self.click_on = False
        
        pressed = pg.key.get_pressed()
        if pressed[pg.K_n]:
            self.new = True

    @staticmethod
    def get_mouse_pos():
        return pg.mouse.get_pos()

    def get_mouse_grid_pos(self, cellsize: tuple) -> tuple:
        mouse_pos = self.get_mouse_pos()
        gridx = mouse_pos[0] // cellsize[0]
        gridy = mouse_pos[1] // cellsize[1]
        return (gridx, gridy)