import os
import time
import pygame as pg

from constants import WIDTH, HEIGHT
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとんや爆弾，ビームなどのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def score_screen(msg: str, score: int, screen: pg.Surface, tmr: int):
    over = pg.Surface((WIDTH, HEIGHT))
    over.set_alpha(255)
    over.fill((0, 0, 0))
    screen.blit(over, (0, 0))

    font = pg.font.Font(None, 80)
    if msg == "Clear":
        score += 500*tmr
        txt = font.render(f"score: {score}", True, (0, 255, 0))
    else:
        txt = font.render(f"score: {score}", True, (255, 0, 0))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2 + 100
    screen.blit(txt, txt_rct)

    pg.display.update()

    
def game_end(screen: pg.Surface, msg: str, color: tuple[int, int, int]): # ゲームクリア、オーバー設定
    over = pg.Surface((WIDTH, HEIGHT))
    over.set_alpha(0)
    over.fill((0, 0, 0))
    screen.blit(over, (0, 0))

    font = pg.font.Font(None, 80)
    txt = font.render(msg, True, color)
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2-100
    screen.blit(txt, txt_rct)

    pg.display.update()
    time.sleep(3)
    pg.quit()
