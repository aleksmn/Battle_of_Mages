# Дмитрий
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

        self.coord = (100, SCREEN_HEIGHT // 2)
        self.current_animation = self.move_animation_left
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

        self.timer = pg.time.get_ticks()
        self.interval = 300
        self.animation_mode = True
        self.charge_power = 0
        self.charge_mode = False
        self.attack_mode = False
        self.down_mode = False
        self.attack_interval = 500

        self.magic_balls = pg.sprite.Group()

        self.hp = 200


    def load_animations(self):

    
        self.idle_animation_right = [load_image(f"images/{self.folder}/idle{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT) for i in range(1, 4)]
        self.idle_animation_left = [pg.transform.flip(image, True, False) for image in self.idle_animation_right]

        # Анимация движения
        self.move_animation_right = [load_image(f"images/{self.folder}/move{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT) for i in range(1, 5)]
        self.move_animation_left = [pg.transform.flip(image, True, False) for image in self.move_animation_right]






    def handle_animation(self):
     
        if self.animation_mode and not self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.interval:
                self.current_image += 1
                if self.current_image >= len(self.current_animation):
                    self.current_image = 0
                self.image = self.current_animation[self.current_image]
                self.timer = pg.time.get_ticks()



    def update(self):

        # Движение по клавишам

        self.handle_animation()




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
        self.screen.blit(self.enemy.image, self.enemy.rect)

        self.player.magic_balls.draw(self.screen)
        self.enemy.magic_balls.draw(self.screen)


        # Полоски здоровья
        pg.draw.rect(self.screen, pg.Color('green'), (10, 10, self.player.hp, 20))
        pg.draw.rect(self.screen, pg.Color('black'), (10, 10, 100 * 2, 20), 2)

        pg.draw.rect(self.screen, pg.Color('green'), (SCREEN_WIDTH - 210, 10, self.enemy.hp, 20))
        pg.draw.rect(self.screen, pg.Color('black'), (SCREEN_WIDTH - 210, 10, 100 * 2, 20), 2)

        if self.win == self.player:
            text = text_render("ПОБЕДА")
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            text2 = text_render("Маг в левом углу")
            text_rect2 = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(text2, text_rect2)
        elif self.win == self.enemy:
            text = text_render("ПОБЕДА")
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            text2 = text_render("Маг в правом углу")
            text_rect2 = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(text2, text_rect2)


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
    game = Game()


