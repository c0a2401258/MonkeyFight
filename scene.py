import sys
import pygame as pg

from constants import WIDTH, HEIGHT


class TitleScene:
    """ホーム画面"""
    def __init__(self):
        self.bg = pg.transform.scale(pg.image.load("fig/back.webp"),(WIDTH, HEIGHT))
        self.gorilla = pg.transform.rotozoom(
            pg.image.load("fig/gorira.png"),  # Enemyが使っている画像名に合わせて変更
            0,
            0.3
        )
        self.font_title = pg.font.Font("C:/Windows/Fonts/meiryo.ttc", 65)
        self.font_menu = pg.font.Font("C:/Windows/Fonts/meiryo.ttc", 30)
        self.font_small = pg.font.Font("C:/Windows/Fonts/meiryo.ttc", 22)

        self.menu = [
            "ゲーム開始",
            "遊び方",
            "終了"
        ]

        self.selected = 0

    def run(self, screen):
        clock = pg.time.Clock()

        while True:

            for event in pg.event.get():

                if event.type == pg.QUIT:
                    return "exit"

                if event.type == pg.KEYDOWN:

                    if event.key == pg.K_UP:
                        self.selected = (self.selected - 1) % len(self.menu)

                    elif event.key == pg.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.menu)

                    elif event.key == pg.K_RETURN:

                        if self.selected == 0:
                            return "start"

                        elif self.selected == 1:
                            return "how"

                        elif self.selected == 2:
                            return "exit"

            screen.blit(self.bg, (0, 0))

            # ゴリラ画像
            gorilla_rect = self.gorilla.get_rect(center=(WIDTH//2+10,200))
            screen.blit(self.gorilla, gorilla_rect)

            # 影
            shadow = self.font_title.render(
                "DONKEY CONDOR",
                True,
                (30,30,0)
            )
            screen.blit(shadow,(WIDTH//2-shadow.get_width()//2+5,95))

            #タイトル
            title = self.font_title.render(
                "DONKEY CONDOR",
                True,
                (255,255,0)
            )
            screen.blit(title,(WIDTH//2-title.get_width()//2,90))

            #サブタイトル
            sub = self.font_small.render(
                "Avoid barrels and reach the treasure!",
                True,
                (255,255,255)
            )
            screen.blit(sub, (WIDTH//2-sub.get_width()//2, 180))

            # メニュー
            for i, text in enumerate(self.menu):

                if i == self.selected:
                    color = (255,255,0)
                    draw_text = "> " + text
                else:
                    color = (255, 255, 255)
                    draw_text = "   " + text
                menu = self.font_menu.render(draw_text,True,color)

                screen.blit(
                    menu,
                    (WIDTH//2-menu.get_width()//2,
                    360+i*60)
                )

            #操作説明
            guide = self.font_small.render(
                "↑/↓ : 選ぶ   ENTER : 決定",
                True,
                (255,255,255)
            )     

            screen.blit(
                guide,
                (
                    WIDTH//2-guide.get_width()//2,
                    570
                )
            )

            # バージョン
            ver = self.font_small.render(
                "Version 2.0   Takumi Iki",
                True,
                (180,180,180)
            )

            screen.blit(ver,(15,630))


            pg.display.flip()

            clock.tick(60)



class HowScene:
    """操作方法画面"""

    def __init__(self):

        self.bg = pg.transform.scale(pg.image.load("fig/back.webp"),(WIDTH, HEIGHT))

        self.font_title = pg.font.Font("C:/Windows/Fonts/meiryo.ttc", 65)
        self.font_text = pg.font.Font("C:/Windows/Fonts/meiryo.ttc", 30)
        self.font_small = pg.font.Font("C:/Windows/Fonts/meiryo.ttc", 22)


    def run(self, screen):

        clock = pg.time.Clock()

        while True:

            for event in pg.event.get():

                if event.type == pg.QUIT:
                    return "exit"

                if event.type == pg.KEYDOWN:

                    if event.key == pg.K_RETURN:
                        return "title"


            screen.blit(self.bg, (0,0))


            title = self.font_title.render(
                "遊び方",
                True,
                (255,255,0)
            )

            screen.blit(
                title,
                (
                    WIDTH//2-title.get_width()//2,
                    80
                )
            )


            texts = [
                "宝を目指そう！",
                "",
                "ゴリラが投げる樽を避けよう",
                "",
                " ← → : 移動,",
                "SPACE : ジャンプ",
                "",
                "樽 : ダメージ",
                "宝 : ゴール"
            ]


            y = 220

            for text in texts:

                msg = self.font_text.render(
                    text,
                    True,
                    (255,255,255)
                )

                screen.blit(
                    msg,
                    (
                        WIDTH//2-msg.get_width()//2,
                        y
                    )
                )

                y += 40


            guide = self.font_small.render(
                "ENTER : 戻る",
                True,
                (255,255,255)
            )

            screen.blit(
                guide,
                (
                    WIDTH//2-guide.get_width()//2,
                    600
                )
            )


            pg.display.flip()

            clock.tick(60)

class ClearScene:
    def __init__(self):
        self.font = pg.font.Font(None, 70)
        self.small_font = pg.font.Font(None, 40)

    def run(self, screen, stage):

        while True:
            screen.fill((0,0,0))

            clear_text = self.font.render(
                "STAGE CLEAR",
                True,
                (255,255,255)
            )

            stage_text = self.small_font.render(
                f"STAGE {stage}",
                True,
                (255,255,255)
            )

            next_text = self.small_font.render(
                "N : Next Stage",
                True,
                (255,255,255)
            )

            home_text = self.small_font.render(
                "H : Home",
                True,
                (255,255,255)
            )


            screen.blit(
                clear_text,
                (WIDTH//2-180,150)
            )

            screen.blit(
                stage_text,
                (WIDTH//2-70,250)
            )

            screen.blit(
                next_text,
                (WIDTH//2-120,350)
            )

            screen.blit(
                home_text,
                (WIDTH//2-80,420)
            )


            for event in pg.event.get():

                if event.type == pg.QUIT:
                    return "exit"

                if event.type == pg.KEYDOWN:

                    if event.key == pg.K_n:
                        return "next"

                    if event.key == pg.K_h:
                        return "home"


            pg.display.update()

class ResultScene:
    def __init__(self):
        self.font = pg.font.Font(None, 50)

    def run(self, screen, stage_score):

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "exit"

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        return "exit"


            screen.fill((0,0,0))


            title = self.font.render(
                "RESULT",
                True,
                (255,255,255)
            )

            screen.blit(
                title,
                (250,80)
            )


            total = 0

            for i, score in enumerate(stage_score):

                text = self.font.render(
                    f"STAGE {i+1} : {score}",
                    True,
                    (255,255,255)
                )

                screen.blit(
                    text,
                    (200,180+i*70)
                )

                total += score


            total_text = self.font.render(
                f"TOTAL : {total}",
                True,
                (255,255,0)
            )

            screen.blit(
                total_text,
                (200,430)
            )


            end = self.font.render(
                "ENTER : END",
                True,
                (255,255,255)
            )

            screen.blit(
                end,
                (220,550)
            )


            pg.display.update()