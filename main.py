import random
import sys
import pygame as pg

from constants import WIDTH, HEIGHT, FPS
from objects import Bird, Wall, Enemy, Barrel
from ui import Score, Timer
from utils import score_screen, game_end
from scene import TitleScene,HowScene

def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    title = TitleScene()
    how = HowScene()

    while True:
        result = title.run(screen)

        if result == "start":
            break

        elif result == "how":

            result =  how.run(screen)

            if result == "exit":
                return 0

        elif result == "exit":
            return 0
    
    stage = 2

    while stage <= 10:
        result = game(screen, stage)

        if result == "clear":
            stage += 1
        
        elif result == "gameover":
            return 0


def game(screen, stage):
    """ステージを3つ作成"""
    bg_img = pg.transform.scale(pg.image.load(f"fig/back.webp"),(WIDTH, HEIGHT))
    walls = pg.sprite.Group()
    clock = pg.time.Clock()
    bird = Bird((100, 605))  #100 605
    score = Score()
    hashigo = pg.transform.rotozoom(pg.image.load(f"fig/hashigo4.png"), 0, 0.085)  # 梯子を獲得
    takara = pg.transform.rotozoom(pg.image.load(f"fig/takara.png"), 0, 0.05)  # 宝を獲得
    takara_rect = takara.get_rect()
    #宝の配置場所
    if stage == 1:
        takara_rect.center = (295,65)
    elif stage == 2:
        takara_rect.center = (445,65)
    elif stage == 3:
        takara_rect.center = (360,40)
    
    #ゴリラの配置場所
    if stage == 1:
        gorilla = Enemy((50,170))
    elif stage == 2:
        gorilla = Enemy((600, 170))
    elif stage == 3:
        gorilla = Enemy((360,170))

    tarus = pg.sprite.Group()
    if stage == 1:
        direction = 1
    elif stage == 2:
        direction = -1
    if stage == 3:
        direction = random.choice([-1,1])
    tarus.add(Barrel(gorilla, direction, stage))
    tmr1 = 0
    tmr2 = 0 
    timer = Timer()  
    it = 200 #樽の間隔200

    #ステージの梯子
    if stage == 1:
        ladder_rects = [
            hashigo.get_rect(topleft=(430, 500)),
            hashigo.get_rect(topleft=(200, 365)),
            hashigo.get_rect(topleft=(430, 225)),
            hashigo.get_rect(topleft=(250, 90))
        ]
    
    elif stage == 2:
        ladder_rects = [
            hashigo.get_rect(topleft=(600,500)),
            hashigo.get_rect(topleft=(350,365)),
            hashigo.get_rect(topleft=(200,225)),
            hashigo.get_rect(topleft=(400,90))
        ]

    elif stage == 3:
        ladder_rects = [
            #1段目
            hashigo.get_rect(topleft=(200,500)),
            hashigo.get_rect(topleft=(540,500)),
            #2段目
            hashigo.get_rect(topleft=(270,365)),
            #3段目
            hashigo.get_rect(topleft=(0,225)),
            hashigo.get_rect(topleft=(630,225)),
            #4段目
            hashigo.get_rect(topleft=(180,90)),
            hashigo.get_rect(topleft=(450,90)),
            

        ]


    #ステージのブロック
    if stage == 1:
        for i in range(8):
            walls.add(Wall(i*90,630))
        for i in range(6):
            walls.add(Wall(i*90,500))
        for i in range(7):
            walls.add(Wall(120+i*90,360))
        for i in range(6):
            walls.add(Wall(i*90,220))
        walls.add(Wall(250,90))


    elif stage == 2:
        # 一番下
        for i in range(8):
            walls.add(Wall(i*90,630))
        # 2段目（右寄り）
        for i in range(7):
            walls.add(Wall(120+i*90,500))
        # 3段目（左寄り）
        for i in range(6):
            walls.add(Wall(i*90,360))
        # 4段目（右寄り）
        for i in range(7):
            walls.add(Wall(120+i*90,220))
        # ゴール手前
        walls.add(Wall(400,90))

    elif stage == 3:
        #1段目
        for i in range(8):
            walls.add(Wall(i*90,630))
        #2段目
        for i in range(8):
            if i not in [0,4]:
                walls.add(Wall(i*90,500))
        #3段目
        for i in range(8):
            if i not in [2,5]:
                walls.add(Wall(i*90,360))
        #4段目
        for i in range(8):
            if i not in [1,6]:
                walls.add(Wall(i*90,220))        
        #5段目（宝）
        for i in range(8):
            walls.add(Wall(i*90,90))

    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0

        screen.blit(bg_img, [0, 0])
        screen.blit(takara, takara_rect)
        for lad in ladder_rects:
            screen.blit(hashigo, lad.topleft)


        bird.sky_state = False
        for i,wall in enumerate(walls):  # 床の情報を取得
            if wall.rect.colliderect(bird.rct):  # 床のrectとこうかとんのrectのが重なっているのかの判定
                # print(i)
                if wall.wall_bound(bird.rct):  # 床にいるのか判定
                    bird.jump_high = -4
                    bird.jump_state = False
                    bird.sky_state = True
        
        for i, taru_x in enumerate(tarus):
            taru_x.sky_state = False
            for i,wall in enumerate(walls):  # 床の情報を取得
                for i, taru_y in enumerate(tarus):
                    if wall.rect.colliderect(taru_y.rct) and taru_y.vy > 0 and taru_y.rct.bottom <= wall.rect.top + 20:
                        taru_y.rct.bottom = wall.rect.top
                        taru_y.sky_state = True


        for i, taru1 in enumerate(tarus):  # 樽とあたったら終了
            if taru1.rct.colliderect(bird.rct):
                score_screen("a", score.value, screen, timer.value)
                return "gameover"
        if takara_rect.colliderect(bird.rct):
            return "clear"
        if tmr2 == it:  # 100~250フレーム(2~5秒)に1回，ゴリラの攻撃(樽)を出現させる
            if stage == 1:
                direction = 1
            elif stage == 2:
                direction = -1
            elif stage == 3:
                direction = random.choice([-1, 1])
            tarus.add(Barrel(gorilla, direction, stage))
            it = random.randrange(100, 250, 50)
            tmr2 = 0
        if gorilla.rct.colliderect(bird.rct):  # ゴリラとあたったら終了
            score_screen("a", score.value, screen, timer.value)
            game_end(screen, "Game Over", (255, 0, 0)) #oキーを押すとゲームオーバー
            return 0 
        
        tarus.update(screen)
        screen.blit(gorilla.image, gorilla.rct)
        walls.draw(screen)
        bird.update(key_lst, screen, ladder_rects)
        score.update(screen)
        timer.update(screen)
        pg.display.update()
        tmr1 += 1
        tmr2 += 1
        if tmr1 % 50 == 0:
            score.value += 1
            timer.value -= 1
        if timer.value < 0:
            score_screen("a", score.value, screen, timer.value)
            game_end(screen, "Game Over", (255, 0, 0)) #oキーを押すとゲームオーバー
            return 0

        clock.tick(FPS)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
