from typing import Any
import pygame
from random import randint, choice
from sys import exit


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha() # load an image of a player
        player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha() # load an image of a player
        self.player_walk = [player_walk1, player_walk2] # create a list of images of a player
        self.player_index = 0 # index of the player image
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha() # load an image of a player

        self.image = self.player_walk[self.player_index] # set the image of the player
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
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
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation_state(self):
        """Handle the animation of the player"""
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:   
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        """Update the player"""
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        # self.mask = pygame.mask.from_surface(self.image)
        screen.blit(self.image, self.rect)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type) -> None:
        super().__init__()

        if type == 'fly':
            fly1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly1, fly2]
            y_pos = 210
        elif type == 'snail':
            snail1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail1, snail2]
            y_pos = 300

        self.animation_index = 0
        
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomright = (randint(900,1100),y_pos))

    def animation_state(self):
        """Handle the animation of the obstacle"""
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        """Update the obstacle"""
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        """Destroy the obstacle if it is out of the screen"""
        if self.rect.x <= -100:
            self.kill()




def display_score() -> float:
    """Display the score on the screen and return the current time"""
    current_time = pygame.time.get_ticks() - start_time # get the time in milliseconds since pygame.init() was called
    current_score = int(current_time / 100)/10 # calculate the score
    score_surf = test_font.render(f'Score: {current_score}', False, (64,64,64)) # create a surface with a text
    score_rect = score_surf.get_rect(center = (400, 50)) # get the rectangle of the text to plqce rect of score to the middle of the screen
    screen.blit(score_surf, score_rect) # draw the text
    return current_score

def collision_sprite():
    """Check for collision between the player and the obstacles using sprite masks"""
    if pygame.sprite.spritecollide(player.sprite, obstacles_groups, False):
        obstacles_groups.empty()
        return False
    return True




pygame.init() # initialize and start pygame

game_active = False # state of the game

start_time = 0 # start time of the game
score = 0 # score of the game
bg_music = pygame.mixer.Sound('audio/music.wav') # load the background music
bg_music.set_volume(0.1) # set the volume of the background music
bg_music.play(loops = -1) # play the background music in a loop

# create a window
screen = pygame.display.set_mode((800, 400)) # width, height

pygame.display.set_caption("My first pygame game") # set the title of the window

clock = pygame.time.Clock() # create a clock object

test_font = pygame.font.Font('font/Pixeltype.ttf', 50) # load a font with a style and a size


# Groups
player = pygame.sprite.GroupSingle() # create a group of sprites
player.add(Player()) # add a sprite to the group

obstacles_groups = pygame.sprite.Group() # create a group of sprites


sky_surf = pygame.image.load('graphics/Sky.png').convert() # load an image
ground_surf = pygame.image.load('graphics/ground.png').convert() # load an image


player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha() # load an image of a player
player_stand = pygame.transform.rotozoom(player_stand,0,2) # scale the image of the player
player_stand_rect = player_stand.get_rect(center = (400,200)) # get the rectangle of the player

game_name = test_font.render('Pixel Runner', False, (111,196,169)) # create a surface with a text
game_name_rect = game_name.get_rect(center = (400,80)) # get the rectangle of the text to plqce rect of score to the middle of the screen

game_message = test_font.render('Press space to run', False, (255,196,169)) # create a surface with a text
game_message_rect = game_message.get_rect(center = (400,370)) # get the rectangle of the text to plqce rect of score to the middle of the screen

# Timer
obstacle_timer = pygame.USEREVENT + 1 # create a custom event
# we need to add +1 to the event to avoid collision with the pygame events
pygame.time.set_timer(obstacle_timer, 1500) # set the timer to 1500 milliseconds

snail_animation_timer = pygame.USEREVENT + 2 # create a custom event
pygame.time.set_timer(snail_animation_timer, 500) # set the timer to 500 milliseconds

fly_animation_timer = pygame.USEREVENT + 3 # create a custom event
pygame.time.set_timer(fly_animation_timer, 100) # set the timer to 200 milliseconds


# to keep the window open
while True:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # check if window closed, then quit the game
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacles_groups.add(Obstacle(choice(['fly','snail','snail','snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks() # get the time in milliseconds since pygame.init() was called



    if game_active:
        # draw all ou elements
        screen.blit(sky_surf, (0, 0)) # draw the sky on the top left corner
        screen.blit(ground_surf, (0, 300)) # draw the ground on the bottom left corner
        
        score = display_score()
        
        # one function to draw and one to update the player
        player.draw(screen) # draw the player
        player.update() # update the player

        # Obstacles
        obstacles_groups.draw(screen) # draw the obstacles
        obstacles_groups.update() # update the obstacles

        # Collision
        game_active = collision_sprite() # check if the player collides with the obstacles

    else: 
        screen.fill((94,129,162)) # fill the screen with a color
        screen.blit(player_stand, player_stand_rect) # draw the player

        score_message = test_font.render(f'Your score: {score}', False, (111,196,169)) # create a surface with a text
        score_message_rect = score_message.get_rect(center = (400,330)) # get the rectangle of the text to place rect of score to the middle of the screen

        screen.blit(game_name, game_name_rect) # draw the text
        if score != 0:
            screen.blit(score_message, score_message_rect) # draw the text
        screen.blit(game_message, game_message_rect) # draw the text

    # update everything
    pygame.display.update() # update the screen

    clock.tick(60) # impose to the while loop 60 fps


