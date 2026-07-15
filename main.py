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

    bg_img = pg.transform.rotozoom(pg.image.load(f"fig/back.webp"), 0, 1.3)
    walls = pg.sprite.Group()
    clock = pg.time.Clock()
    bird = Bird((100, 605))  #100 605
    score = Score()
    hashigo = pg.transform.rotozoom(pg.image.load(f"fig/hashigo4.png"), 0, 0.085)  # 梯子を獲得
    takara = pg.transform.rotozoom(pg.image.load(f"fig/takara.png"), 0, 0.05)  # 宝を獲得
    takara_rect = takara.get_rect()
    takara_rect.center = 220, 40
    #print(takara_rect)
    gorilla = Enemy()
    tarus = pg.sprite.Group()
    tarus.add(Barrel(gorilla))
    tmr1 = 0
    tmr2 = 0 
    timer = Timer()  
    it = 200

    ladder_rects = [
        hashigo.get_rect(topleft=(480, 500)),
        hashigo.get_rect(topleft=(200, 365)),
        hashigo.get_rect(topleft=(480, 225)),
        hashigo.get_rect(topleft=(210, 90))
    ]

    for i in range(8):
        walls.add(Wall(i*90, 630))
    for i in range(6):
        walls.add(Wall(i*90, 500))
    for i in range(6):
        walls.add(Wall(120+i*90, 360))
    for i in range(6):
        walls.add(Wall(i*90, 220))
    walls.add(Wall(200, 90))

    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0

        screen.blit(bg_img, [0, 0])
        screen.blit(takara, [220, 40])
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
                    if wall.rect.colliderect(taru_y.rct):
                        taru_y.sky_state = True


        for i, taru1 in enumerate(tarus):  # 樽とあたったら終了
            if taru1.rct.colliderect(bird.rct):
                score_screen("a", score.value, screen, timer.value)
                game_end(screen, "Game Over",(255, 0, 0)) #oキーを押すとゲームオーバー
                return 0
        if takara_rect.colliderect(bird.rct):
            #print("a")
            score_screen("Clear", score.value, screen, timer.value)
            game_end(screen, "Game Clear", (0, 255, 0)) #cキーを押すとゲームクリア
            return 0
        if tmr2 == it:  # 100~250フレーム(2~5秒)に1回，ゴリラの攻撃(樽)を出現させる
            tarus.add(Barrel(gorilla))
            it = random.randrange(100, 250, 50)
            tmr2 = 0
        if gorilla.rct.colliderect(bird.rct):  # ゴリラとあたったら終了
            score_screen("a", score.value, screen, timer.value)
            game_end(screen, "Game Over", (255, 0, 0)) #oキーを押すとゲームオーバー
            return 0 
        
        tarus.update(screen)
        screen.blit(gorilla.image, [15, 63])
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
