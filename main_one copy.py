# Андрей
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

        # клавиши управления
        self.key_right = pg.K_d
        self.key_left = pg.K_a
        self.key_down = pg.K_s
        self.key_charge = pg.K_SPACE


        self.current_animation = self.idle_animation_right
        self.side = "right"

        self.image = self.current_animation[0]
        self.current_image = 0

        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)


        self.timer = pg.time.get_ticks()
        self.interval = 300
        self.animation_mode = True
        self.attack_mode = False



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
        # Зарядка
        self.charge_right = load_image(f"images/{self.folder}/charge.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
        self.charge_left = pg.transform.flip(self.charge_right, True, False)




    def handle_animation(self):

        if self.animation_mode and not self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.interval:
                self.current_image += 1
                if self.current_image >= len(self.current_animation):
                    self.current_image = 0
                self.image = self.current_animation[self.current_image]
                self.timer = pg.time.get_ticks()


    def update(self):
        keys = pg.key.get_pressed()
        direction = 0

        if keys[self.key_left]:
            direction = -1
            self.side = "left"
        elif keys[self.key_right]:
            direction = 1
            self.side = "right"

        self.handle_animation()
        self.handle_movement(direction, keys)


    def handle_movement(self, direction, keys):
        if self.attack_mode:
            return

        if direction != 0:
            self.animation_mode = True 
            self.charge_mode = False
            self.rect.x += direction
            self.current_animation = self.move_animation_left if direction == -1 else self.move_animation_right
        elif keys[self.key_down]:

            self.image = self.down_right if self.side == "right" else self.down_left


        else:
            self.down_mode = False
            self.animation_mode = True
            self.charge_mode = False
            self.current_animation = self.idle_animation_left if self.side == "left" else self.idle_animation_right



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
        # Фон
        self.screen.blit(self.background, (0, 0))


        # Отрисовка персонажа
        self.screen.blit(self.player.image, self.player.rect)



        # Передний план
        self.screen.blit(self.foreground, (0, 0))



    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False


    def update(self):

        self.player.update()
        

    def run(self):
        while self.is_running:
            self.update()
            self.event()
            self.draw()
 
            self.clock.tick(FPS)
            pg.display.flip()





# Точка входа в программу
if __name__ == "__main__":
    # Запускаем игру
    game = Game()