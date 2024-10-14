# Максим
import random
import pygame as pg

pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

CHARACTER_WIDTH = 300
CHARACTER_HEIGHT = 375

FPS = 60

font = pg.font.Font(None, 40)

def load_image(file, width, height):
    image = pg.image.load(file)
    image = pg.transform.scale(image, (width, height))
    return image


def text_render(text):
    return font.render(str(text), True, "black")


class MagicBall(pg.sprite.Sprite):
    def __init__(self, coord, side, power, folder):
        super().__init__()

        self.side = side
        self.power = power / 2

        self.image = load_image(f"images/{folder}/magicball.png", 200, 150)
        if self.side == "right":
            self.image = pg.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()

        self.rect.center = coord[0], coord[1] + 120


    def update(self):
        if self.side == "right":
            self.rect.x += 4
            if self.rect.left >= SCREEN_WIDTH:
                self.kill()
        else:
            self.rect.x -= 4
            if self.rect.right <= 0:
                self.kill()




class Player(pg.sprite.Sprite):
    def __init__(self, folder="fire wizard"):
        super().__init__()

        self.folder = folder

        self.load_animations()

        self.coord = (100, SCREEN_HEIGHT // 2)
        self.current_animation = self.idle_animation_right
        self.side = "right"

        # клавиши управления
        self.key_right = pg.K_d
        self.key_left = pg.K_a
        self.key_down = pg.K_s
        self.key_charge = pg.K_SPACE

        
        self.image = self.current_animation[0]
        self.current_image = 0

        self.rect = self.image.get_rect()
        self.rect.center = self.coord

        self.timer = pg.time.get_ticks()
        self.interval = 300
        self.animation_mode = True
        self.charge_power = 0
        self.charge_mode = False
        self.attack_mode = False
        self.down_mode = False
        self.attack_interval = 500

        self.hp = 200

        # Группа спрайтов
        self.magic_balls = pg.sprite.Group()



    def update(self):
        self.handle_animation()
        self.handle_movement()
        self.handle_attack_mode()


    def handle_attack_mode(self):
        if self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.attack_interval:
                self.attack_mode = False
                self.timer = pg.time.get_ticks()


    def load_animations(self):

        self.idle_animation_right = [load_image(f"images/{self.folder}/idle{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT) for i in range(1, 4)]

        self.idle_animation_left = [pg.transform.flip(image, True, False) for image in self.idle_animation_right]

        self.move_animation_right = [load_image(f"images/{self.folder}/move{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT) for i in range(1, 5)]
        
        self.move_animation_left = [pg.transform.flip(image, True, False) for image in self.move_animation_right]

        # Приседения
        self.down_right = load_image(f"images/{self.folder}/down.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
        self.down_left = pg.transform.flip(self.down_right, True, False)
        # Атака
        self.attack_right = load_image(f"images/{self.folder}/attack.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
        self.attack_left = pg.transform.flip(self.attack_right, True, False)
        # Подзарядка
        self.charge_right = load_image(f"images/{self.folder}/charge.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
        self.charge_left = pg.transform.flip(self.charge_right, True, False)


    def handle_animation(self):
        print(self.charge_mode)

        if not self.charge_mode and self.charge_power > 0:
            self.attack_mode = True   


        if self.animation_mode and not self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.interval:
                self.current_image += 1
                if self.current_image >= len(self.current_animation):
                    self.current_image = 0

                self.image = self.current_animation[self.current_image]
                self.timer = pg.time.get_ticks()

        if self.charge_mode:
            self.charge_power += 1
            print(self.charge_power)       
            if self.charge_power == 100:
                self.attack_mode = True

        if self.attack_mode and self.charge_power > 0:
            
            # Запускаем Файербол
            fireball_position = self.rect.topright if self.side == "right" else self.rect.topleft
            self.magic_balls.add(MagicBall(fireball_position, self.side, self.charge_power, self.folder))

            self.charge_power = 0
            self.charge_mode = False
            self.image = self.attack_left if self.side == "left" else self.attack_right
            self.timer = pg.time.get_ticks()


    def handle_movement(self):
        keys = pg.key.get_pressed()
        direction = 0

        if keys[self.key_left]:
            direction = -1
            self.side = "left"
        elif keys[self.key_right]:
            direction = 1
            self.side = "right"


        if direction != 0:
            self.down_mode = False
            self.animation_mode = True
            self.charge_mode = False
            self.rect.x += direction
            self.current_animation = self.move_animation_right if self.side == "right" else self.move_animation_left

        elif keys[self.key_down]:
            self.down_mode = True
            self.animation_mode = False
            self.charge_mode = False
            self.image = self.down_right if self.side == "right" else self.down_left

        elif keys[self.key_charge]:
            self.down_mode = False
            self.animation_mode = False
            self.charge_mode = True
            self.image = self.charge_right if self.side == "right" else self.charge_left

        else:
            self.down_mode = False
            self.animation_mode = True
            self.charge_mode = False
            self.current_animation = self.idle_animation_left if self.side == "left" else self.idle_animation_right


        # Границы экрана
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0



class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Битва магов")

        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.foreground = load_image("images/foreground.png", SCREEN_WIDTH, SCREEN_HEIGHT)


        # Персонажи
        self.player = Player(folder="fire wizard")



        self.clock = pg.time.Clock()

        self.is_running = True
        self.win = None

        # Запуск игры
        self.run()



    def draw(self):
        # Отрисовка всей игры
        self.screen.blit(self.background, (0, 0))

        # отрисовка персонажей
        self.screen.blit(self.player.image, self.player.rect)

        self.player.magic_balls.draw(self.screen)


        self.screen.blit(self.foreground, (0, 0))

    def update(self):
        # обновряем состояние игры, вызывается каждый кадр
        self.player.update()

        self.player.magic_balls.update()


    def event(self):
        # события игры (нажатия на кнопки)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False



    def run(self):
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            pg.display.flip()



# Точка входа в программу
if __name__ == "__main__":
    # Запускаем игру
    game = Game()
