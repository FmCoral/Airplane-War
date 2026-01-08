import pygame
import random

# 版本信息
VERSION = "2.2"
VERSION_HISTORY = """
2.2 - 2026-01-06 - (1) 修复英雄牺牲后窗口无征兆关闭情况，替换为重新开始和结束游戏按钮\r(2) 添加暂停游戏逻辑
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

    def __init__(self, image_names, speed=1, speed_x=0, speed_y=0):

        super().__init__()
        # 1. 处理图片参数：兼容单图片和多图片
        if isinstance(image_names, str):  # 如果传入单图片路径
            self.image_names = [image_names]  # 转为列表，统一处理
        else:  # 如果传入多图片
            self.image_names = image_names

        # 2. 加载所有图片，存储在列表
        self.images = []
        for img_name in self.image_names:
            img = pygame.image.load(img_name)
            self.images.append(img)

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.speed = speed
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.index = 0


    def switch_image(self, index):
        """
        切换显示图片
        """
        if 0 <= index < len(self.images):
            self.index = index
            self.image = self.images[index]
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center


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
        self.bullets.add(bullet) # type:ignore


class Bullet(GameSprite):

    def __init__(self):
        # 设置子弹图片，设置初始速度
        super().__init__("./images/bullet1.png", -4)

    def update(self):
        # 让子弹沿垂直方向飞行
        super().update()

        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        pass


class Button(GameSprite):
    """单个按钮类"""
    def __init__(self, image_names, pos_x, pos_y):
        super().__init__(image_names)
        # 按钮位置
        self.rect.centerx = pos_x
        self.rect.centery = pos_y
        self.current_img_index = 0

    def is_clicked(self, mouse_pos):
        """检测当前按钮是否被点击"""
        return self.rect.collidepoint(mouse_pos)

    def update(self):
        pass


class AgainButton(Button):
    def __init__(self):
        # 重来按钮： 屏幕中间偏下位置
        super().__init__("./images/again.png", 240, 300)


class GameOverButton(Button):
    def __init__(self):
        # 结束按钮：屏幕中间位置
        super().__init__("./images/game_over.png", 240, 400)


class PauseButton(Button):
    def __init__(self):
        # 暂停按钮：屏幕右上角
        super().__init__(
            "./images/pause_nor.png",440, 30)


class ResumeButton(Button):
    def __init__(self):
        # 继续按钮：和暂停按钮同一位置
        super().__init__("./images/resume_nor.png", 440, 30)