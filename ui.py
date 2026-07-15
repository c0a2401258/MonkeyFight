import pygame as pg

from constants import HEIGHT

class Score:
    """
    スコアを表示するクラス
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (255, 255, 0)
        self.value = 0
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        self.rct = self.image.get_rect()
        self.rct.center = 100, HEIGHT-630

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        screen.blit(self.image, self.rct)

class Timer:
    """
    残り時間を表示するクラス
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (255, 255, 0)
        self.value = 180
        self.image = self.font.render(f"time: {self.value}", 0, self.color)
        self.rct = self.image.get_rect()
        self.rct.center = 500, HEIGHT-630

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"time: {self.value}", 0, self.color)
        screen.blit(self.image, self.rct)
