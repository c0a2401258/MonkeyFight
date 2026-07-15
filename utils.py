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

    
def game_end(screen, text, color):

    font_big = pg.font.Font(None, 100)
    font_mid = pg.font.Font(None, 45)

    # 暗い背景を重ねる
    overlay = pg.Surface(screen.get_size())
    overlay.set_alpha(180)
    overlay.fill((0,0,0))
    screen.blit(overlay, (0,0))


    # GAME OVER文字
    title = font_big.render(
        text,
        True,
        color
    )

    title_rect = title.get_rect(
        center=(WIDTH//2, 250)
    )

    screen.blit(title, title_rect)


    # 説明文
    sub = font_mid.render(
        "Press SPACE to return title",
        True,
        (255,255,255)
    )

    sub_rect = sub.get_rect(
        center=(WIDTH//2, 380)
    )

    screen.blit(sub, sub_rect)


    pg.display.update()


    while True:
        for event in pg.event.get():

            if event.type == pg.QUIT:
                return "exit"

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_SPACE:
                    return "title"