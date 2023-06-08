import os
import sys
from pathlib import Path
from random import choice, randint
from sys import exit

import pygame

# check if the program is running from a bundle
_RUNNING_FROM_BUNDLE = getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")
# if the program is running from a bundle, adapt the path
PATH_SAVED_ENV = (Path(sys._MEIPASS)) if _RUNNING_FROM_BUNDLE else Path.cwd()


class Player(pygame.sprite.Sprite):
    """Class that represent the player"""

    def __init__(self) -> None:
        super().__init__()
        # load the images of the player
        player_walk1 = pygame.image.load(
            os.path.join(PATH_SAVED_ENV, "graphics/bunny/bunny_1_2.png")
        ).convert_alpha()
        player_walk2 = pygame.image.load(
            os.path.join(PATH_SAVED_ENV, "graphics/bunny/bunny_2_2.png")
        ).convert_alpha()
        self.player_walk = [player_walk1, player_walk2]  # create a list of images of a player
        self.player_index = 0  # index of the player image
        self.player_jump = pygame.image.load(os.path.join(PATH_SAVED_ENV, "graphics/bunny/bunny_1_2.png")).convert_alpha()

        # set the image of the player
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        # load sound of the player
        self.jump_sound = pygame.mixer.Sound(os.path.join(PATH_SAVED_ENV, "audio/jump.mp3"))
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        """Handle the input of the player"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = -20

    def apply_gravity(self):
        """Apply gravity to the player"""
        self.gravity += 1
        self.rect.y += self.gravity
        # check if the player is on the ground
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        """Handle the animation of the player"""
        # check if the player is jumping
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            # animate the player
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        """Update the player"""
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        screen.blit(self.image, self.rect)


class Obstacle(pygame.sprite.Sprite):
    """Class that represent the obstacles"""

    def __init__(self, type) -> None:
        super().__init__()

        # load the images of the obstacles
        if type == "fly":
            fly1 = pygame.image.load(os.path.join(PATH_SAVED_ENV, "graphics/stork/stork_1.png")).convert_alpha()
            fly2 = pygame.image.load(os.path.join(PATH_SAVED_ENV, "graphics/stork/stork_2.png")).convert_alpha()
            self.frames = [fly1, fly2]
            y_pos = 210
        elif type == "fly_baby":
            flyb1 = pygame.image.load(os.path.join(PATH_SAVED_ENV, "graphics/stork/stork_baby_1.png")).convert_alpha()
            flyb2 = pygame.image.load(os.path.join(PATH_SAVED_ENV, "graphics/stork/stork_baby_2.png")).convert_alpha()
            self.frames = [flyb1, flyb2]
            y_pos = 210
        elif type == "snail":
            snail1 = pygame.image.load(os.path.join(PATH_SAVED_ENV, "graphics/hedgehog/hedgehog_1.png")).convert_alpha()
            snail2 = pygame.image.load(os.path.join(PATH_SAVED_ENV, "graphics/hedgehog/hedgehog_2.png")).convert_alpha()
            self.frames = [snail1, snail2]
            y_pos = 300

        self.animation_index = 0

        # set the image of the obstacle
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomright=(randint(900, 1100), y_pos))

    def animation_state(self):
        """Handle the animation of the obstacle"""
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        """Update the obstacle"""
        self.animation_state()
        self.rect.x -= 6*(1+display_score()/100)
        self.destroy()

    def destroy(self):
        """Destroy the obstacle if it is out of the screen"""
        if self.rect.x <= -200:
            self.kill()

class SkyBackground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        sky_image = pygame.image.load(os.path.join(PATH_SAVED_ENV, "graphics/sky.png")).convert()
        
        height_image = sky_image.get_height()
        width_image = sky_image.get_width()

        self.image = pygame.Surface((width_image*2, height_image))
        self.image.blit(sky_image, (0, 0))
        self.image.blit(sky_image, (width_image, 0))

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self):
        """Update the sky background"""
        self.pos.x -= 100 * (1+display_score()/100)/100
        if self.rect.centerx < 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
        screen.blit(self.image, self.rect)


def display_score() -> float:
    """Display the score on the screen and return the current score"""
    # get the time in milliseconds since pygame.init() was called
    current_time = pygame.time.get_ticks() - start_time
    current_score = int(current_time / 100) / 10
    # create a surface with a text
    score_surf = test_font.render(f"Score: {current_score}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    # draw the score on the screen
    screen.blit(score_surf, score_rect)
    return current_score


def collision_sprite():
    """Check for collision between the player and the obstacles, retun True if there is no collision"""
    if pygame.sprite.spritecollide(player.sprite, obstacles_groups, False):
        obstacles_groups.empty()
        return False
    return True


# initialize pygame
pygame.init()

game_active = False
start_time = 0
score = 0

# background music
bg_music = pygame.mixer.Sound(os.path.join(PATH_SAVED_ENV, "audio/music.wav"))
bg_music.set_volume(0.1)
bg_music.play(loops=-1)

# create a window
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Bunny Runner")
pygame_icon = pygame.image.load(os.path.join(PATH_SAVED_ENV, "graphics/bunny/bunny_0.png"))
pygame.display.set_icon(pygame_icon)

clock = pygame.time.Clock()
test_font = pygame.font.Font(os.path.join(PATH_SAVED_ENV, "font/Pixeltype.ttf"), 50)


# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles_groups = pygame.sprite.Group()

sky = pygame.sprite.GroupSingle()
sky.add(SkyBackground())

# Background
# sky_surf = pygame.image.load(os.path.join(PATH_SAVED_ENV, "graphics/Sky.png")).convert()
ground_surf = pygame.image.load(os.path.join(PATH_SAVED_ENV, "graphics/ground.png")).convert()

# Inactive game background
player_stand = pygame.image.load(os.path.join(PATH_SAVED_ENV, "graphics/bunny/bunny_0.png")).convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 0.5)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render("Bunny Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render("Press space to run", False, (255, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 370))


# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


# Game loop
while True:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacles_groups.add(Obstacle(choice(["fly_baby","fly", "snail", "snail", "snail","fly", "snail", "snail", "snail","fly", "snail", "snail", "snail"])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        # draw background
        # screen.blit(sky_surf, (0, 0))
        sky.draw(screen)
        sky.update()
        screen.blit(ground_surf, (0, 300))

        score = display_score()

        # Player
        player.draw(screen)
        player.update()

        # Obstacles
        obstacles_groups.draw(screen)
        obstacles_groups.update()

        # Collision
        game_active = collision_sprite()

    else:
        # draw game inactive screen
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))

        screen.blit(game_name, game_name_rect)
        if score != 0:
            screen.blit(score_message, score_message_rect)
        screen.blit(game_message, game_message_rect)

    # update everything
    pygame.display.update()

    # set the frame rate to 60 fps
    clock.tick(60)
