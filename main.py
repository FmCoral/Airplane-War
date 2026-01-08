import sys
from sprites import *

# 版本信息
__version__ = VERSION
__version_history__ = VERSION_HISTORY

class PlaneGame(object):
    def __init__(self):
        """
        初始化
        """
        # 创建窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 创建游戏时钟
        self.clock = pygame.time.Clock()
        # 调用私有方法
        self.__create_sprites()
        # 创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 500)
        # 创建英雄
        pygame.time.set_timer(HERO_FIRE_EVENT, 300)


    def __create_sprites(self):
        """
        创建精灵组
        :return:
        """
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2) # type:ignore

        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero) # type:ignore

        # 创建单个按钮实例
        self.pause_btn = PauseButton()
        self.resume_btn = ResumeButton()
        self.again_btn = AgainButton()
        self.game_over_btn = GameOverButton()

        # 初始只显示暂停按钮
        self.button_group = pygame.sprite.Group(self.pause_btn) # type:ignore
        # 游戏结束按钮组
        self.game_over_group = pygame.sprite.Group(self.game_over_btn, self.again_btn) # type:ignore
        self.is_paused = False  # 标记游戏是否暂停
        self.is_game_over = False  # 标记游戏是否结束


    def __event_handler(self):
        """
        事件监听
        :return: bool
        """
        need_restart = False
        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
                return True, False

            elif event.type == CREATE_ENEMY_EVENT and not self.is_paused and not self.is_game_over:
                 self.enemy_group.add(Enemy()) # type:ignore

            elif event.type == HERO_FIRE_EVENT and not self.is_paused and not self.is_game_over:
                self.hero.fire()

            # 检测按钮点击
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # 点击继续按钮
                if self.pause_btn.is_clicked(mouse_pos) and not self.is_paused:
                    self.is_paused = True
                    self.button_group.add(self.resume_btn)  # type:ignore
                    self.button_group.remove(self.pause_btn)  # type:ignore

                # 点击暂停按钮
                elif self.resume_btn.is_clicked(mouse_pos) and self.is_paused:
                    self.is_paused = False
                    self.button_group.remove(self.resume_btn)  # type:ignore
                    self.button_group.add(self.pause_btn)  # type:ignore

                # 点击重新开始
                elif self.again_btn.is_clicked(mouse_pos) and self.is_game_over:
                    need_restart = True  # 标记需要重启

                # 点击结束游戏
                elif self.game_over_btn.is_clicked(mouse_pos) and self.is_game_over:
                    PlaneGame.__game_over()

        if not self.is_paused and not self.is_game_over:
            keys_pressed = pygame.key.get_pressed()

            # 左右移动
            if keys_pressed[pygame.K_RIGHT] and keys_pressed[pygame.K_LEFT]:
                self.hero.speed_x = 0
            elif keys_pressed[pygame.K_RIGHT]:
                self.hero.speed_x = 4
            elif keys_pressed[pygame.K_LEFT]:
                self.hero.speed_x = -4
            else:
                self.hero.speed_x = 0

            # 上下移动
            if keys_pressed[pygame.K_UP] and keys_pressed[pygame.K_DOWN]:
                self.hero.speed_y = 0
            elif keys_pressed[pygame.K_UP]:
                self.hero.speed_y = -3
            elif keys_pressed[pygame.K_DOWN]:
                self.hero.speed_y = 3
            else:
                self.hero.speed_y = 0

        return False, need_restart


    def __check_collide(self):
        """
        碰撞检测
        :return:
        """
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)

        # 敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True) # type:ignore

        # 判断列表是否有内容
        if len(enemies)> 0:
            # 让英雄牺牲
            self.hero.kill()
            self.is_game_over = True


    def __update_sprites(self):
        """
        更新精灵组
        :return:
        """
        if not self.is_paused and not self.is_game_over:
            # 更新精灵组
            self.back_group.update()
            self.enemy_group.update()
            self.hero_group.update()
            self.hero.bullets.update()

        # 绘制精灵组
        self.back_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.hero_group.draw(self.screen)
        self.hero.bullets.draw(self.screen)

        # 绘制暂停/继续按钮
        self.button_group.update()
        self.button_group.draw(self.screen)

        # 游戏结束时绘制重来/结束按钮
        if self.is_game_over:
            self.enemy_group.empty()
            self.hero.bullets.empty()
            self.button_group.empty()
            self.game_over_group.draw(self.screen)


    @staticmethod
    def __game_over():
        print("游戏结束！")
        pygame.quit()
        sys.exit()


    def start(self):

        while True:
            # 刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 事件监听
            is_exit, need_restart = self.__event_handler()
            if is_exit:
                break
            if need_restart:
                return  # 退出当前实例的循环，准备重建新实例

            # 碰撞检测+更新绘制
            if not self.is_paused and not self.is_game_over:
                self.__check_collide()
                self.__update_sprites()
                pygame.display.update()
            else:
                # 暂停/结束时更新按钮、刷新显示
                self.__update_sprites()
                pygame.display.update()


if __name__ == '__main__':
    while True:
        plane = PlaneGame()
        plane.start()