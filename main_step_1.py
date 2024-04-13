# Тимур

import random
import pygame as pg
import pygame_menu

# pip install pygame_menu

pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

CHARACTER_WIDTH = 300
CHARACTER_HEIGHT = 375

FPS = 60

font = pg.font.Font(None, 40)

def load_image(file, width, height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (width, height))
    return image

def text_render(text):
    return font.render(str(text), True, "black")


# Создадим класс персонажа игрока
class Player(pg.sprite.Sprite):
    def __init__(self, folder="fire wizard"):
        super().__init__()

        self.folder = folder

        self.load_animations()

        self.image = self.idle_animation_right[0]
        self.current_image = 0
        self.current_animation = self.idle_animation_right
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)

        self.timer = pg.time.get_ticks()
        self.interval = 300
        self.side = "right"
        self.animation_mode = True

        self.charge_power = 0


        self.charge_mode = False
        self.magic_balls = pg.sprite.Group()

        self.attack_mode = False
        self.attack_interval = 500



    def load_animations(self):

        self.idle_animation_right = []
        for i in range(1, 4):
            self.idle_animation_right.append(load_image(f"images/fire wizard/idle{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT))

        self.idle_animation_left = []
        for image in self.idle_animation_right:
            self.idle_animation_left.append(pg.transform.flip(image, True, False))

        # Анимация движения вправо
        self.move_animation_right = []
        for i in range(1, 4):
            self.move_animation_right.append(load_image(f"images/fire wizard/move{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT))

        # Анимация движения влево
        self.move_animation_left = []
        for image in self.move_animation_right:
            self.move_animation_left.append(pg.transform.flip(image, True, False))


        # Приседания
        self.down = [load_image(f"images/fire wizard/down.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.down.append(pg.transform.flip(self.down[0], True, False))

        # Подготовка к атаке
        self.charge = [load_image(f"images/fire wizard/charge.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.charge.append(pg.transform.flip(self.charge[0], True, False))

        # Атака
        self.attack = [load_image(f"images/fire wizard/attack.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.attack.append(pg.transform.flip(self.attack[0], True, False))



    def update(self):

        direction = 0

        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            direction = -1
            self.side = "left"
        elif keys[pg.K_d]:
            direction = 1
            self.side = "right"


        # Движение
        self.handle_movement(direction, keys)

        # Анимация персонажа
        self.handle_animation()

        # Режим атаки и возвращение в исходную позицию
        self.handle_attack_mode()
    

    def handle_attack_mode(self):
        if self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.attack_interval:
                self.attack_mode = False
                self.timer = pg.time.get_ticks()



    def handle_movement(self, direction, keys):
        if self.attack_mode:
            return


        if direction != 0:
            self.animation_mode = True
            self.charge_mode = False
            self.rect.x += direction
            # Сменяем анимацию
            self.current_animation = self.move_animation_left if direction == -1 else self.move_animation_right

        elif keys[pg.K_s]:
            self.animation_mode = False 
            self.charge_mode = False
            self.image = self.down[self.side != "right"]

        elif keys[pg.K_SPACE]:
            self.animation_mode = False
            self.charge_mode = True
            self.image = self.charge[self.side != "right"]


        else:
            self.animation_mode = True
            self.charge_mode = False
            self.current_animation = self.idle_animation_left if self.side == "left" else self.idle_animation_right
    
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0



    def handle_animation(self):

        if not self.charge_mode and self.charge_power > 0:
            self.attack_mode = True

        if self.animation_mode and not self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.interval:
                # переключаем анимацию на следующий кадр
                self.current_image += 1
                if self.current_image >= len(self.current_animation):
                    self.current_image = 0
                self.image = self.current_animation[self.current_image]
                self.timer = pg.time.get_ticks()

        if self.charge_mode:
            self.charge_power += 1
            # Изменяем индикатор зарядки
            print(self.charge_power)
            if self.charge_power == 100:
                self.attack_mode = True


        if self.attack_mode and self.charge_power > 0:
            fireball_position = self.rect.topright if self.side == "right" else self.rect.topleft
            # Создаем фаерболл
            print("FIREBALL!")
            self.magic_balls.add(MagicBall(fireball_position, self.side, self.charge_power, self.folder))

            self.charge_power = 0
            self.charge_mode = False
            self.image = self.attack[self.side != "right"]
            self.timer = pg.time.get_ticks()




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



class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Битва магов")

        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.foreground = load_image("images/foreground.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        # Создаем объект игрок
        self.player = Player()


        self.clock = pg.time.Clock()
        self.run()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

    def update(self):
        self.player.update()
        self.player.magic_balls.update()

    def draw(self):
        # Отрисовка интерфейса
        self.screen.blit(self.background, (0, 0))

        # Отрисовка персонажей

        self.screen.blit(self.player.image, self.player.rect)

        # Magic ball
        self.player.magic_balls.draw(self.screen)

        # передний план
        self.screen.blit(self.foreground, (0, 0))
        pg.display.flip()



# Точка входа в программу
if __name__ == "__main__":
    Game()