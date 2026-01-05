import pygame
import random

# 版本信息
__version__ = "2.1"
__version_history__ = """
2.1 - 2026-01-05 - 添加英雄上下移动功能,已经对应边缘检测等
1.0 - 2026-01-03 - 初始版本，基本运行游戏
"""

# 屏幕大小
SCREEN_RECT = pygame.Rect(0, 0, 480, 600)
# 刷新帧率
FRAME_PER_SEC = 60
# 创建敌机定时器
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1

class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=1, speed_x=0, speed_y=0):

        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.speed_x = speed_x
        self.speed_y = speed_y


    def update(self):
        # 在屏幕垂直方向移动
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):
        # 调用父类方法实现精灵的创建
        super().__init__("./images/background.png")

        if is_alt:
            self.rect.y = -self.rect.height


    def update(self):
        super().update()

        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):

    def __init__(self):
        # 调用父类方法，创建敌机精灵，指定敌机图片
        super().__init__("./images/enemy1.png")
        # 指定敌机初始随机速度
        self.speed = random.randint(1,5)
        # 指定随机位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)


    def update(self):
        # 调用父类保持垂直方向飞行
        super().update()
        # 判断是否飞出屏幕
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()


    def __del__(self):
        pass


class Hero(GameSprite):

    def __init__(self):
        # 设置image和speed
        super().__init__("./images/me1.png", 0, 0, 0)
        # 设置初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 创建子弹精灵组
        self.bullets = pygame.sprite.Group()


    def update(self):
        # 水平方向移动
        self.rect.x += self.speed_x

        # 垂直方向移动
        self.rect.y += self.speed_y

        # 控制左右移动边界
        if self.rect.x < 0:
            self.rect.x = 0

        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

        # 控制上下移动边界
        if self.rect.y < 0:
            self.rect.y = 0

        elif self.rect.bottom >SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom


    def fire(self):
        # 创建子弹精灵
        bullet = Bullet()
        # 设置精灵组位置
        bullet.rect.bottom = self.rect.y - 20
        bullet.rect.centerx = self.rect.centerx
        # 将精灵添加到精灵组
        self.bullets.add(bullet)


class Bullet(GameSprite):

    def __init__(self):
        # 设置子弹图片，设置初始速度
        super().__init__("./images/bullet1.png", -4)
        pass


    def update(self):
        # 让子弹沿垂直方向飞行
        super().update()

        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()


    def __del__(self):
        pass
