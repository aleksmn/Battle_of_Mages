# Лука
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


class Enemy(pg.sprite.Sprite):
    def __init__(self, folder):
        super().__init__()

        self.folder = folder
        self.load_animations()

        self.hp = 200

        self.image = self.idle_animation_left[0]
        self.current_image = 0
        self.current_animation = self.idle_animation_left

        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)

        self.timer = pg.time.get_ticks()
        self.interval = 300
        self.side = "left"
        self.animation_mode = True

        self.magic_balls = pg.sprite.Group()

        self.attack_mode = False
        self.attack_interval = 500

        self.move_interval = 800
        self.move_duration = 0
        self.direction = 0
        self.move_timer = pg.time.get_ticks()

        self.charge_power = 0

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

    def update(self, player):
        self.handle_attack_mode(player)
        self.handle_movement()
        self.handle_animation()


    def handle_attack_mode(self, player):

        if not self.attack_mode:
            attack_probability = 1

            if player.charge_mode:
                attack_probability += 2

            if random.randint(1, 100) <= attack_probability:
                self.attack_mode = True
                self.charge_power = random.randint(1, 100)

                if player.rect.centerx < self.rect.centerx:
                    self.side = "left"
                else:
                    self.side = "right"

                self.animation_mode = False
                self.image = self.attack_right if self.side == "right" else self.attack_left

        if self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.attack_interval:
                self.attack_mode = False

                self.timer = pg.time.get_ticks()

    def handle_movement(self):
        if self.attack_mode:
            return

        now = pg.time.get_ticks()

        if now - self.move_timer < self.move_duration:
            self.animation_mode = True
            self.rect.x += self.direction
            self.current_animation = self.move_animation_left if self.direction == -1 else self.move_animation_right
        else:
            if random.randint(1, 100) == 1 and now - self.move_timer > self.move_interval:
                self.move_timer = pg.time.get_ticks()
                self.move_duration = random.randint(400, 1500)
                self.direction = random.choice([-1, 1])
            else:
                self.animation_mode = True
                self.current_animation = self.idle_animation_left if self.side == "left" else self.idle_animation_right

        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0

    def handle_animation(self):
        if self.animation_mode and not self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.interval:
                self.current_image += 1
                if self.current_image >= len(self.current_animation):
                    self.current_image = 0
                self.image = self.current_animation[self.current_image]
                self.timer = pg.time.get_ticks()

        if self.attack_mode and self.charge_power > 0:
            ball_position = self.rect.topright if self.side == "right" else self.rect.topleft
            self.magic_balls.add(MagicBall(ball_position, self.side, self.charge_power, self.folder))
            self.charge_power = 0
            self.image = self.attack_right if self.side == "right" else self.attack_left
            self.timer = pg.time.get_ticks()

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
            if self.charge_power == 100:
                self.attack_mode = True

        if self.attack_mode and self.charge_power > 0:
            # создаем объект фаерболл и добавялем его в группу спрайтов
            fireball_position = self.rect.topright if self.side == "right" else self.rect.topleft
            self.magic_balls.add(MagicBall(fireball_position, self.side, self.charge_power, self.folder))

            self.charge_power = 0
            self.charge_mode = False
            self.image = self.attack_left if self.side == "left" else self.attack_right
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

        self.handle_attack_mode()
        self.handle_movement(direction, keys)
        self.handle_animation()


    def handle_attack_mode(self):
        if self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.attack_interval:
                self.attack_mode = False
                self.timer = pg.time.get_ticks()

    def handle_movement(self, direction, keys):
        if self.attack_mode:
            return

        if direction != 0:
            self.animation_mode = True  #
            self.charge_mode = False
            self.rect.x += direction
            self.current_animation = self.move_animation_left if direction == -1 else self.move_animation_right
        elif keys[self.key_down]:
            self.down_mode = True
            self.animation_mode = False
            self.charge_mode = False
            self.image = self.down_right if self.side == "right" else self.down_left
        elif keys[self.key_charge]:
            self.animation_mode = False
            self.image = self.charge_right if self.side == "right" else self.charge_left
            self.charge_mode = True
        else:
            self.down_mode = False
            self.animation_mode = True
            self.charge_mode = False
            self.current_animation = self.idle_animation_left if self.side == "left" else self.idle_animation_right

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
        self.player = Player()
        self.enemy = Enemy("earth monk")


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

        if self.win:
            return

        self.player.update()
        self.enemy.update(self.player)


        self.enemy.magic_balls.update()
        self.player.magic_balls.update()

        # Урон от файерболов
        hits = pg.sprite.spritecollide(self.enemy, self.player.magic_balls, True, pg.sprite.collide_rect_ratio(0.3))
        for hit in hits:
            self.enemy.hp -= hit.power


        if not self.player.down_mode:

            hits = pg.sprite.spritecollide(self.player, self.enemy.magic_balls, True, pg.sprite.collide_rect_ratio(0.3))
            for hit in hits:
                self.player.hp -= hit.power

        if self.player.hp <= 0:
            self.win = self.enemy
        elif self.enemy.hp <= 0:
            self.win = self.player

        
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


