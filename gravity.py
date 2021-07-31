import pygame
from sys import exit
from random import randint, choice
import json

# Constants
WIDTH, HEIGHT = 1000, 580
NAME = "Gravity run"
FPS = 60

GRAVITY = 5
MIN_SPAWN_TIME, MAX_SPAWN_TIME = 2000, 3000
BOX_SPAWN_TIME = 20
COIN_SPAWN_TIME = 15
DEMAGE = 10
HEALTH, MAX_HEALTH = 100, 100
SHOOT_COOLDOWN = 30
AMMO_BOX = 5
HEAL_BOX = 10
PRICE = 20
ACTIVE_LASER = 700
SLEEP_LASER = -1500

LIGTH_BLUE = (111, 196, 169)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 255)
GREY = (170, 170, 170)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
WHITE = (255, 255, 255)

HITBOX = False
MUSIC = True

# Start pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption(NAME)

# Music
bg_music = pygame.mixer.Sound('music/music.wav')
if MUSIC:
    bg_music.play(loops=-1)

# Load images
bg = pygame.image.load("images/factory.png")

player_walk_1 = pygame.image.load('images/run/0.png').convert_alpha()
player_walk_2 = pygame.image.load('images/run/1.png').convert_alpha()
player_walk_3 = pygame.image.load('images/run/2.png').convert_alpha()
player_walk_4 = pygame.image.load('images/run/3.png').convert_alpha()
player_walk_5 = pygame.image.load('images/run/4.png').convert_alpha()
player_walk_6 = pygame.image.load('images/run/5.png').convert_alpha()
player_jump = pygame.image.load('images/run/jump.png').convert_alpha()
player_death_1 = pygame.image.load('images/death/0.png').convert_alpha()
player_death_2 = pygame.image.load('images/death/1.png').convert_alpha()
player_death_3 = pygame.image.load('images/death/2.png').convert_alpha()
player_death_4 = pygame.image.load('images/death/3.png').convert_alpha()
player_death_5 = pygame.image.load('images/death/4.png').convert_alpha()
player_death_6 = pygame.image.load('images/death/5.png').convert_alpha()
player_death_7 = pygame.image.load('images/death/6.png').convert_alpha()
player_death_8 = pygame.image.load('images/death/7.png').convert_alpha()

enemy_1 = pygame.image.load('images/enemy1.png').convert_alpha()
enemy_2 = pygame.image.load('images/enemy2.png').convert_alpha()

bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullet_logo = pygame.image.load('images/bullet_logo.png').convert_alpha()

explosion_1 = pygame.image.load('images/explosion/exp1.png').convert_alpha()
explosion_2 = pygame.image.load('images/explosion/exp2.png').convert_alpha()
explosion_3 = pygame.image.load('images/explosion/exp3.png').convert_alpha()
explosion_4 = pygame.image.load('images/explosion/exp4.png').convert_alpha()
explosion_5 = pygame.image.load('images/explosion/exp5.png').convert_alpha()

ammo_box = pygame.image.load('images/ammo_box.png').convert_alpha()
health_box = pygame.image.load('images/health_box.png').convert_alpha()

coin_1 = pygame.image.load('images/coins/coin_1.png').convert_alpha()
coin_2 = pygame.image.load('images/coins/coin_2.png').convert_alpha()
coin_3 = pygame.image.load('images/coins/coin_3.png').convert_alpha()
coin_4 = pygame.image.load('images/coins/coin_4.png').convert_alpha()
coin_5 = pygame.image.load('images/coins/coin_5.png').convert_alpha()
coin_6 = pygame.image.load('images/coins/coin_6.png').convert_alpha()

cannon_1 = pygame.image.load('images/cannon/cannon1.png').convert_alpha()
cannon_2 = pygame.image.load('images/cannon/cannon2.png').convert_alpha()
cannon_3 = pygame.image.load('images/cannon/cannon3.png').convert_alpha()
cannon_4 = pygame.image.load('images/cannon/cannon4.png').convert_alpha()
cannon_5 = pygame.image.load('images/cannon/cannon5.png').convert_alpha()
cannon_6 = pygame.image.load('images/cannon/cannon6.png').convert_alpha()
cannon_7 = pygame.image.load('images/cannon/cannon7.png').convert_alpha()

laser_1 = pygame.image.load('images/laser/laser1.png').convert_alpha()
laser_2 = pygame.image.load('images/laser/laser2.png').convert_alpha()
laser_3 = pygame.image.load('images/laser/laser3.png').convert_alpha()


# Load fonts
font_type = 'font/Pixeltype.ttf'

# Other
item_boxes_img = {
    "Ammo": ammo_box,
    "Health": health_box,
}


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_walk = [player_walk_1, player_walk_2,
                            player_walk_3, player_walk_4, player_walk_5]

        self.player_jump = player_jump
        self.player_death = [player_death_1, player_death_2, player_death_3,
                             player_death_4, player_death_5, player_death_6, player_death_7, player_death_8]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.reverse = True
        self.hp = HEALTH
        self.max_hp = MAX_HEALTH
        self.shoot_cooldown = 0
        self.ammo = AMMO_BOX
        self.jump_sound = pygame.mixer.Sound('music/audio_jump.mp3')
        self.jump_sound.set_volume(0.5)
        self.shoot_sound = pygame.mixer.Sound('music/img_laser.wav')
        self.shoot_sound.set_volume(0.8)
        self.particle_timer = 0
        self.number_coins = 0
        self.upgrades = []
        self.shop = False
        self.cannon_active = False

    def animation(self):
        self.player_index += 0.1
        if self.rect.y < 350 and self.rect.y > 150:
            self.image = self.player_jump

        elif self.hp <= 0:
            if self.player_index >= len(self.player_death):
                self.player_index = len(self.player_death) - 1
            self.reverse = True
            self.image = self.player_death[int(self.player_index)]

        else:
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def number_of_ammo(self):
        self.ammo_img = bullet_logo
        self.ammo_img = pygame.transform.scale(self.ammo_img, (15, 20))

        for num_ammo in range(self.ammo):
            if num_ammo < 15:
                screen.blit(self.ammo_img, ((WIDTH - 30) - num_ammo * 11, 15))
            elif num_ammo < 30:
                screen.blit(self.ammo_img, ((WIDTH - 30) -
                                            (num_ammo - 15) * 11, 40))
            else:
                screen.blit(self.ammo_img, ((WIDTH - 30) -
                                            (num_ammo - 30) * 11, 65))

    def apply_gravity(self, gravity, particle):
        if not self.reverse:
            self.gravity = -gravity
            self.image = pygame.transform.flip(self.image, False, True)
        else:
            self.gravity = gravity

        self.rect.y += self.gravity

        if self.reverse:
            if self.rect.y >= 350:
                self.rect.y = 350
                if self.particle_timer > 0:
                    self.particle_timer -= 1
                    particle.add_particles(self)

        else:
            if self.rect.y <= 130:
                self.rect.y = 130
                if self.particle_timer > 0:
                    self.particle_timer -= 1
                    particle.add_particles(self)

    def shoot(self, bullets):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            if MUSIC:
                self.shoot_sound.play()
            self.shoot_cooldown = SHOOT_COOLDOWN
            self.ammo -= 1
            bullet = Bullet(self.rect.centerx + 55, self.rect.centery)
            bullets.append(bullet)

    def draw(self):
        self.image = pygame.transform.scale(self.image, (80, 100))
        if HITBOX:
            pygame.draw.rect(screen, RED, self.rect, 2)
        screen.blit(self.image, self.rect)

    def update(self, particle):
        self.draw()
        self.animation()
        self.apply_gravity(GRAVITY, particle)
        self.number_of_ammo()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.enemy_walk = [enemy_1, enemy_2]
        self.enemy_index = 0
        self.image = self.enemy_walk[self.enemy_index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.health = 2
        self.max_health = 2
        self.death_sound = pygame.mixer.Sound('music/audio_end.wav')

    def animation(self):
        self.enemy_index += 0.1

        if self.enemy_index >= len(self.enemy_walk):
            self.enemy_index = 0
        self.image = self.enemy_walk[int(self.enemy_index)]

    def health_bar(self, health):
        self.health = health
        ratio = self.health / self.max_health
        if ratio < 0:
            ratio = 0

        pygame.draw.rect(screen, RED,
                         (self.rect.x + 25, self.rect.y - 10, 35, 3))
        pygame.draw.rect(screen, GREEN,
                         (self.rect.x + 25, self.rect.y - 10, 35 * ratio, 3))

    def move(self):
        self.rect.x -= self.speed

    def collision(self, player, explosions, enemies):
        if self.rect.colliderect(player.rect):
            player.hp -= DEMAGE
            explosion = Explosion(self.rect.x, self.rect.y)
            explosions.append(explosion)
            enemies.remove(self)

    def collision_bullet(self, bullets):
        for bullet in bullets:
            if bullet.rect.colliderect(self.rect):
                self.health -= 1
                bullets.remove(bullet)
                if self.health <= 0:
                    if MUSIC:
                        self.death_sound.play()

    def draw(self):
        if HITBOX:
            pygame.draw.rect(screen, RED, self.rect, 2)
        screen.blit(self.image, self.rect)

    def update(self):
        self.draw()
        self.animation()
        self.move()


class Background:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = bg
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.shake_timer = 100
        self.shift = 0

    def move(self):
        self.x -= 2
        self.shift = self.x
        if self.x <= 0:
            self.x = self.image.get_width()

    def shake(self):
        self.shake_timer -= 1
        self.y = randint(0, 8)
        self.x = randint(0, 8) - self.shift

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        screen.blit(self.image, (self.x + self.image.get_width(), self.y))
        screen.blit(self.image, (self.x - self.image.get_width(), self.y))


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.image = bullet
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        self.rect.x += self.speed

    def draw(self):
        if HITBOX:
            pygame.draw.rect(screen, RED, self.rect, 2)
        screen.blit(self.image, self.rect)

    def update(self):
        self.draw()
        self.move()


class HealthBar:
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        self.health = health
        ratio = self.health / self.max_health
        if ratio < 0:
            ratio = 0
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN,
                         (self.x, self.y, 150 * ratio, 20))


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.explosion_imgs = [explosion_1, explosion_2,
                               explosion_3, explosion_4, explosion_5]
        self.explosion_index = 0
        self.image = self.explosion_imgs[self.explosion_index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.explosion_sound = pygame.mixer.Sound("music/audio_grenade.wav")

    def animation(self, explosions):
        self.explosion_index += 0.1
        if MUSIC:
            self.explosion_sound.play()
        if self.explosion_index >= len(self.explosion_imgs):
            self.explosion_index = len(self.explosion_imgs) - 1
            explosions.remove(self)
        self.image = self.explosion_imgs[int(self.explosion_index)]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self, explosions):
        self.draw()
        self.animation(explosions)


class ItemBox:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.item_type = item_type
        self.image = item_boxes_img[item_type]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.y_speed = 1

    def move(self):
        self.rect.x -= 4
        self.rect.y -= self.y_speed

        if self.rect.y >= 350:
            self.y_speed *= -1
        elif self.rect.y <= 130:
            self.y_speed *= -1

    def update(self, player, item_boxes):
        screen.blit(self.image, self.rect)
        if HITBOX:
            pygame.draw.rect(screen, RED, self.rect, 2)
        self.move()

        if self.rect.colliderect(player.rect):
            if self.item_type == "Ammo":
                player.ammo += AMMO_BOX

            if self.item_type == "Health":
                if player.hp < player.max_hp - HEAL_BOX:
                    player.hp += HEAL_BOX
                else:
                    player.hp = player.max_hp
            item_boxes.remove(self)

        if self.rect.x <= -100:
            item_boxes.remove(self)


class Particle:
    def __init__(self):
        self.particles = []
        self.laser_particles = []

    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                particle[1] -= 0.2
                pygame.draw.circle(screen, GREY, particle[0], int(particle[1]))

    def emit_laser(self):
        if self.laser_particles:
            self.delete_particles()
            for particle in self.laser_particles:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                particle[1] -= 0.2
                pygame.draw.circle(
                    screen, choice([ORANGE, YELLOW, RED]), particle[0], int(particle[1]))

    def add_particles(self, player):
        if not player.reverse:
            pos_x = player.rect.centerx
            pos_y = player.rect.centery - 50
            direction_x = randint(0, 3)
        else:
            pos_x = player.rect.centerx
            pos_y = player.rect.centery + 50
            direction_x = randint(-3, 0)

        radius = 5
        direction_y = randint(-3, 3)
        particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
        self.particles.append(particle_circle)

    def add_laser_particles(self, cannons):
        for cannon in cannons:
            if cannon.rect.x > WIDTH / 2:
                pos_x = cannon.rect.centerx - 30
                direction_y = randint(0, 3)
            else:
                pos_x = cannon.rect.centerx + 30
                direction_y = randint(-3, 0)

            radius = 4
            direction_x = randint(-3, 3)
            pos_y = cannon.rect.centery
            particle_circle = [[pos_x, pos_y],
                               radius, [direction_x, direction_y]]
            self.laser_particles.append(particle_circle)

    def delete_particles(self):
        particle_copy = [
            particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy

        laser_particle_copy = [
            particle for particle in self.laser_particles if particle[1] > 0]
        self.laser_particles = laser_particle_copy


class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coin_img = [coin_1, coin_2, coin_3, coin_4, coin_5, coin_6]
        self.coin_index = 0
        self.image = self.coin_img[self.coin_index]
        self.image = pygame.transform.scale(
            self.image, (int(self.image.get_width() - self.image.get_width() / 2), 55))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.sound = pygame.mixer.Sound("music/img_coin.wav")

    def animations(self):
        self.coin_index += 0.1
        if self.coin_index >= len(self.coin_img):
            self.coin_index = 0
        self.image = self.coin_img[int(self.coin_index)]

    def move(self):
        self.rect.x -= 2

    def draw(self):
        self.image = pygame.transform.scale(
            self.image, (int(self.image.get_width() - self.image.get_width() / 2), 55))
        if HITBOX:
            pygame.draw.rect(screen, RED, self.rect, 2)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, player, coins):
        self.draw()
        self.animations()
        self.move()
        if self.rect.colliderect(player.rect):
            if MUSIC:
                self.sound.play()
            player.number_coins += 1
            coins.remove(self)

        if self.rect.x <= -100:
            coins.remove(self)


class UpgradeBar:
    def __init__(self, x, item_type):
        self.x = x
        self.y = HEIGHT - 50
        self.item_type = item_type
        self.image = item_boxes_img[item_type]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.message_money = 0
        self.message_already_bought = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self, player):
        self.draw()
        point = pygame.mouse.get_pos()

        if self.rect.collidepoint(point) and player.shop:
            player.shop = False

            if self.item_type in player.upgrades:
                self.message_already_bought = 100
            elif player.number_coins >= PRICE and self.item_type not in player.upgrades:
                player.upgrades.append(self.item_type)
                player.number_coins -= PRICE
            else:
                self.message_money = 100

        if self.message_money > 0:
            self.message_money -= 1
            draw_text("You have no money for this", RED,
                      20, WIDTH - 80, HEIGHT - 60)

        if self.message_already_bought > 0:
            self.message_already_bought -= 1
            draw_text(f"You've already bought it", RED,
                      20, WIDTH - 80, HEIGHT - 80)


class Cannon:
    def __init__(self, x, y, flipx, flipy, end_pos, start_pos, speed):
        self.x = x
        self.y = y
        self.flipx = flipx
        self.flipy = flipy
        self.speed = speed
        self.end_pos = end_pos
        self.start_pos = start_pos
        self.cannon_imgs = [cannon_1, cannon_2, cannon_3,
                            cannon_4, cannon_5, cannon_6, cannon_7]
        self.cannon_index = 0
        self.image = self.cannon_imgs[self.cannon_index]
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.image = pygame.transform.flip(self.image, flipx, flipy)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.timer = ACTIVE_LASER - 1.5 * ACTIVE_LASER

    def animation(self):
        if self.speed > 0:
            if self.rect.x >= self.end_pos:
                self.cannon_index += 0.1
        else:
            if self.rect.x <= self.end_pos:
                self.cannon_index += 0.1

        if self.cannon_index >= len(self.cannon_imgs):
            self.cannon_index = len(self.cannon_imgs) - 1

        self.image = self.cannon_imgs[int(self.cannon_index)]

    def move(self, player):
        if self.speed < 0:
            if self.timer >= 0:
                if self.end_pos <= self.rect.x:
                    self.rect.x += self.speed
            else:
                if self.start_pos >= self.rect.x:
                    self.rect.x -= self.speed
            self.timer -= 1
        else:
            if self.timer >= 0:
                if self.end_pos >= self.rect.x:
                    self.rect.x += self.speed
            else:
                if self.start_pos <= self.rect.x:
                    self.rect.x -= self.speed
            self.timer -= 1

        if self.timer <= 100:
            self.cannon_index -= 0.2
            if self.cannon_index <= 0:
                self.cannon_index = 0

        if self.timer <= SLEEP_LASER:
            self.timer = ACTIVE_LASER

        # Stop spawning enemies
        if self.timer < SLEEP_LASER + 200:
            player.cannon_active = True
        elif self.timer < 0:
            player.cannon_active = False

    def draw(self):
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.image = pygame.transform.flip(self.image, self.flipx, self.flipy)
        screen.blit(self.image, self.rect)

    def update(self, player):
        self.draw()
        self.move(player)
        self.animation()


class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.laser_imgs = [laser_1, laser_2, laser_3]
        self.laser_index = 0
        self.image = self.laser_imgs[self.laser_index]
        self.image = pygame.transform.scale(self.image, (970, 20))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def animation(self):
        self.laser_index += 0.1
        if self.laser_index >= len(self.laser_imgs):
            self.laser_index = 0

        self.image = self.laser_imgs[int(self.laser_index)]

    def collision(self, player):
        if self.rect.colliderect(player.rect):
            if DEMAGE == 0:
                pass
            else:
                player.hp -= 0.1

    def draw(self):
        self.image = pygame.transform.scale(self.image, (970, 20))
        if HITBOX:
            pygame.draw.rect(screen, RED, self.rect, 2)
        screen.blit(self.image, self.rect)

    def update(self):
        self.draw()
        self.animation()


def open_json(mode, key_type, new_value=None):
    with open("./data/gravity_data.json", "r", encoding='utf-8') as f:
        data = json.load(f)

    if mode == "w":
        data[str(key_type)] = new_value
        with open("./data/gravity_data.json", mode, encoding='utf-8') as f:
            json.dump(data, f)

    return data[str(key_type)]


def draw_text(text, color, size, x, y):
    font = pygame.font.Font(font_type, size)
    text = font.render(text, False, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def paused(pause):
    draw_text("Paused", BLUE, 150, WIDTH / 2, HEIGHT / 2)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False

                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

        pygame.display.update()
        clock.tick(15)


def draw_window(player, health, enemies, bullets, explosions, item_boxes, background, particle, coins, upgrade_bar, cannons, lasers, score, hint):

    background.draw()
    player.update(particle)
    health.draw(player.hp)
    particle.emit()

    if hint:
        draw_text('Press "f" to shoot...',
                  BLUE, 50, 170, HEIGHT - 30)

    if player.hp > 0:
        background.move()
        for enemy in enemies:
            enemy.update()
            enemy.collision(player, explosions, enemies)
            enemy.collision_bullet(bullets)
            enemy.health_bar(enemy.health)

            if enemy.rect.x + enemy.image.get_width() < 0 or enemy.health <= 0:
                enemies.remove(enemy)

        for bullet in bullets:
            bullet.update()

            if bullet.rect.x + bullet.image.get_width() > WIDTH + 200:
                bullets.remove(bullet)

        for explosion in explosions:
            explosion.update(explosions)

        for item_box in item_boxes:
            item_box.update(player, item_boxes)

        for coin in coins:
            coin.update(player, coins)

        for upgrade_item in upgrade_bar:
            upgrade_item.update(player)

        for cannon in cannons:
            cannon.update(player)
            if int(cannon.cannon_index) == 6:
                for laser in lasers:
                    laser.update()
                    laser.collision(player)
                    particle.add_laser_particles(cannons)
        particle.emit_laser()
        draw_text(f"Score: {score}", BLUE, 50, WIDTH / 2, 30)
        draw_text(f"Coins: {player.number_coins}",
                  YELLOW, 50, WIDTH / 2, HEIGHT - 30)

    else:
        if background.shake_timer > 0:
            background.shake()
        hight_score = open_json("r", "hight_score")

        if score >= hight_score:
            hight_score = open_json("w", "hight_score", score)
            draw_text(
                f"New hight score: {hight_score}", BLUE, 90, WIDTH / 2, HEIGHT / 3)

        else:
            draw_text(
                f"Hight score: {hight_score}", BLUE, 90, WIDTH - 250, HEIGHT / 3)
            draw_text(f"Your score: {score}", BLUE, 90, 250, HEIGHT / 3)
        draw_text("Press enter....", LIGTH_BLUE, 50, WIDTH / 2, HEIGHT / 2)


def main():

    # Variables
    item_box_spawn_time = 0
    coin_spawn_time = 0
    score = 0
    hint = True
    pause = True

    # Call classes
    player = Player(100, 350)
    enemies = [Enemy(1000, 200, 3)]
    background = Background(0, 0)
    health = HealthBar(20, 20, HEALTH, MAX_HEALTH)
    bullets = []  # Bullet(10000, -1000)
    explosions = []  # Explosion(1000, 1000)
    item_boxes = []  # ItemBox(-100, -100, "Ammo")
    particle = Particle()
    coins = []  # Coin(200, 200)
    upgrade_bar = [UpgradeBar(
        (WIDTH - 50), "Ammo"), UpgradeBar((WIDTH - 100), "Health")]
    cannons = [Cannon(-170, 370, True, False, 10, -170, 1), Cannon(1100, 370, False, False, 920, 1100, -1), Cannon(
        1100, 120, False, True, 920, 1100, -1), Cannon(-170, 120, True, True, 10, -170, 1)]

    lasers = [Laser(15, 150), Laser(15, 390)]

    # Set timer
    enemies_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(enemies_timer, randint(
        MIN_SPAWN_TIME, MAX_SPAWN_TIME))

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.hp > 0:
                        if MUSIC:
                            player.jump_sound.play()
                        player.particle_timer = 20
                        if player.reverse:
                            player.reverse = False
                        else:
                            player.reverse = True

                if event.key == pygame.K_RETURN:  # Game restart
                    player.hp = MAX_HEALTH
                    background.shake_timer = 100
                    score = 0
                    enemies = []
                    explosions = []
                    bullets = []
                    player.ammo = AMMO_BOX
                    item_boxes = []
                    player.number_coins = 0
                    coins = []
                    player.upgrades = []
                    for cannon in cannons:
                        cannon.timer = ACTIVE_LASER - 1.5 * ACTIVE_LASER

                if event.key == pygame.K_f:
                    hint = False
                    if player.hp > 0:
                        player.shoot(bullets)

                if event.key == pygame.K_p:
                    paused(pause)

                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shop = True

            if event.type == enemies_timer:
                # print(int(clock.get_fps()))
                if not player.cannon_active:
                    enemies.append(Enemy(1000, randint(130, 390), 3))
                    if score > 10:
                        enemies.append(Enemy(1200, randint(130, 390), 3))
                if player.hp > 0:
                    score += 1

        item_box_spawn_time += 1
        if item_box_spawn_time >= BOX_SPAWN_TIME * FPS and len(player.upgrades) > 0:
            item_boxes.append(ItemBox(1000, randint(
                130, 350), choice(player.upgrades)))
            item_box_spawn_time = 0

        coin_spawn_time += 1
        if coin_spawn_time >= COIN_SPAWN_TIME * FPS:
            for i in range(randint(3, 10)):
                coins.append(Coin(1000 + 60 * i, choice([230, 290])))
            coin_spawn_time = 0

        draw_window(player, health, enemies, bullets,
                    explosions, item_boxes, background, particle, coins, upgrade_bar, cannons, lasers, score, hint)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
