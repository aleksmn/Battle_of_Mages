# Степан
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




class Player(pg.sprite.Sprite):
    def __init__(self, folder="fire wizard"):
        super().__init__()

        self.folder = folder

        self.load_animations()

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
        self.rect.center = (100, SCREEN_HEIGHT // 2)

        self.interval = 300
        self.timer = pg.time.get_ticks()

        self.animation_mode = True
        self.charge_mode = False
        self.attack_mode = False
        self.down_mode = False

        self.charge_power = 0
        self.hp = 200


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
        # Атака
        self.charge_right = load_image(f"images/{self.folder}/charge.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
        self.charge_left = pg.transform.flip(self.charge_right, True, False)


    def handle_animation(self):

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
            print("Fireball!")            

            self.charge_power = 0
            self.charge_mode = False
            self.image = self.attack_left if self.side == "left" else self.attack_right
            self.timer = pg.time.get_ticks()



class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Битва магов")


        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.foreground = load_image("images/foreground.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        # Персонажи
        self.player = Player()



        self.clock = pg.time.Clock()

        self.is_running = True
        self.win = None

        self.run()
   
    def draw(self):
        # Отрисовка интерфейса
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.player.image, self.player.rect)




        self.screen.blit(self.foreground, (0, 0))

    def update(self):
        self.player.update()


    def event(self):
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
    Game()


