import pygame as pg

from constants import WIDTH, HEIGHT
from utils import check_bound

class Bird:
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (1, 0),
        pg.K_SPACE: (0,),
        pg.K_UP: (0, -2),
        pg.K_DOWN: (0, 2)
    }
    img0 = pg.transform.rotozoom(pg.image.load("fig/2.png"), 0, 0.7)
    img = pg.transform.flip(img0, True, False)
    imgs = {
        (+1, 0): img0,
        (-1, 0): img,
    }

    gravity = +0.05

    def __init__(self, xy: tuple[int, int]):
        self.img = __class__.imgs[(+1, 0)]
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.jump_state = False
        self.sky_state = False
        self.jump_high = -1
        self.sky_high = 0
        self.on_ladder = False

    def change_img(self, num: int, screen: pg.Surface):
        self.img = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 0.9)
        screen.blit(self.img, self.rct)

    def update(self, key_lst: list[bool], screen: pg.Surface, ladder_rects: list[pg.Rect]):
        sum_mv = [0, 0]
    
    # 「↑キーが押されていて、かつはしごに重なっている」場合だけ登り判定を有効にする
        ladder_hit = any(
            self.rct.centerx >= lad.left and
            self.rct.centerx <= lad.right and
            self.rct.bottom >= lad.top and
            self.rct.top <= lad.bottom
            for lad in ladder_rects
        )
        
        if ladder_hit:
            if key_lst[pg.K_UP] or key_lst[pg.K_DOWN]:
                self.on_ladder = True
        elif not ladder_hit:
            self.on_ladder = False
            
        if self.on_ladder:
            #梯子の中での移動
            if key_lst[pg.K_LEFT]:
                sum_mv[0] -= 1
                self.img = __class__.img
            if key_lst[pg.K_RIGHT]:
                sum_mv[0] += 1
                self.img = __class__.img0
            #上下移動
            if key_lst[pg.K_UP]:
                sum_mv[1] = -2
            if key_lst[pg.K_DOWN]:
                sum_mv[1] = 2
            self.jump_state = False
            self.sky_state = True
            self.sky_high = 0
            self.jump_high = -1

            if not ladder_hit:
                self.on_ladder = False
        
        else:
            # 横移動と画像切替（通常どおり）
            for k, mv in __class__.delta.items():
                if key_lst[k] and k != pg.K_SPACE and k not in [pg.K_UP, pg.K_DOWN]:
                    sum_mv[0] += mv[0]
                    #print(mv)
                    if k == pg.K_RIGHT:
                        self.img = __class__.img0
                    if k == pg.K_LEFT:
                        self.img = __class__.img
                elif key_lst[k] and k == pg.K_SPACE:
                    self.jump_state = True
                    self.sky_state = False
            if self.jump_state:
                sum_mv[1] += self.jump_high
                self.jump_high += __class__.gravity
            if not self.sky_state and not self.on_ladder:  # 床にいるかの判定
                sum_mv[1] += self.sky_high
                self.sky_high += __class__.gravity
            else:
                self.sky_high = 0


        self.rct.move_ip(sum_mv)
    
        if check_bound(self.rct) != (True, True):  # 四方に飛んだ場合
            self.rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(self.img, self.rct)


class Wall(pg.sprite.Sprite):
    """
    足場に関するクラス    """
    def __init__(self, x: int, y: int):
        """
        引数1 x：足場を表示する左上x座標
        引数2 y：足場を表示する左上y座標
        """
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/brick_wall_3x.png"), 0, 0.08)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def wall_bound(self,obj_rct: pg.Rect) -> tuple[bool, bool]:
        """
        引数：こうかとんのRect
        戻り値：ブロックに乗っているのかの判定結果（画面内：True/画面外：False）
        """
        #print(obj_rct.bottom,self.rect.top)
        ue = False
        if obj_rct.bottom-self.rect.top<=5:
            ue = True
            # print(" obj_rct.bottom > self.rect.top")
        return ue


class Enemy:
    """
    敵に関するクラス
    """
    def __init__(self, pos=(50,100)):
        super().__init__()
        self.image = pg.transform.rotozoom(
            pg.image.load(f"fig/gorira.png"),0,0.12)
        self.rct = self.image.get_rect()
        self.rct.center = pos

class Barrel(pg.sprite.Sprite):
    """
    敵の攻撃(樽)に関するクラス
    """

    gravity = +0.2

    def __init__(self, gorilla: "Enemy",direction, stage):
        """
        引数1 gorilla：攻撃を出す対象
        """
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/taru.png"),0, 0.05)
        self.rct = self.image.get_rect()
        self.rct.centerx = gorilla.rct.centerx #敵の攻撃(樽)の初期位置
        self.rct.bottom = gorilla.rct.bottom+16
        self.vx = 3 * direction # 敵の攻撃(樽)の移動スピード3
        self.sky_state = False
        self.vy = 1
        self.sky_high = 0
        self.stage = stage

    def update(self, screen: pg.Surface):
        """
        引数1 screen：画面Surface
        """
        yoko, tate = check_bound(self.rct) # 講義で使ったチェックバウンドを横判定だけにしたもので判別
        if not yoko:
            self.vx *= -1
            if self.rct.bottom >= 630:
                #ステージ1　左端で消える
                if self.stage == 1:
                    if self.rct.left <= 0:
                        self.kill()

                #ステージ2　右端で消える
                elif self.stage == 2:
                    if self.rct.right >= WIDTH:
                        self.kill()

                #ステージ3　両端で消える
                elif self.stage == 3:
                    if self.rct.left <= 0 or self.rct.right >= WIDTH:
                        self.kill()

        

        if not self.sky_state:  # 床にいるかの判定
            self.vy += self.sky_high
            self.sky_high += __class__.gravity

            #落下速度上限
            if self.vy > 5:
                self.vy = 5
        else:
            self.vy = 1

        
        # 横移動
        self.rct.x += self.vx

        # 縦移動
        self.rct.y += self.vy
    

        screen.blit(self.image, self.rct)
