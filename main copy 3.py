# Егор
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


class Game:
    def __init__(self):
        print("Игра")

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Битва магов")

        # Фон
        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)


        self.clock = pg.time.Clock()
        self.is_running = True

        # Запуск игры
        self.run()

    
    def draw(self):
        self.screen.blit(self.background, (0, 0))


    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False


    def run(self):
        while self.is_running:
            self.event()
            self.draw()


            self.clock.tick()
            pg.display.flip()




# Точка входа
if __name__ == "__main__":
    # Запускаем игру
    Game()
