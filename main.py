import sys
from sprites import *


class PlaneGame(object):
    def __init__(self):
        # 创建窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 创建游戏时钟
        self.clock = pygame.time.Clock()
        # 调用私有方法
        self.__create_sprites()
        # 创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 500)
        pygame.time.set_timer(HERO_FIRE_EVENT, 300)


    def __create_sprites(self):
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)


    def __event_handler(self):
        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
                return True

            elif event.type == CREATE_ENEMY_EVENT:
                # 敌机出场
                enemy = Enemy()
                self.enemy_group.add(enemy)

            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        # 使用键盘提供的方法获取键盘按键
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2

        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2

        else:
            self.hero.speed_x = 0

        # 上下飞行
        if keys_pressed[pygame.K_UP] and keys_pressed[pygame.K_DOWN]:
            self.hero.speed_y = 0

        elif keys_pressed[pygame.K_UP]:
            self.hero.speed_y = -3

        elif keys_pressed[pygame.K_DOWN]:
            self.hero.speed_y = 3

        else:
            self.hero.speed_y = 0

        return False


    def __check_collide(self):
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)

        # 敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)

        # 判断列表是否有内容
        if len(enemies)> 0:
            # 让英雄牺牲
            self.hero.kill()

            # 结束游戏
            PlaneGame.__game_over()


    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)


    @staticmethod
    def __game_over():
        print("game over")
        pygame.quit()
        sys.exit()


    def start(self):
        print("begin")
        while True:
            # 刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 事件监听
            is_exit = self.__event_handler()
            if is_exit:
                break
            # 碰撞检测
            self.__check_collide()
            # 更新/绘制精灵组
            self.__update_sprites()
            # 更新显示
            pygame.display.update()


if __name__ == '__main__':
    plane = PlaneGame()
    plane.start()