'''
Game Goals: move left and right to grab all 30 points with the most health possible
'''
# Sources: 
#  Mr. Cozort
#  http://kidscancode.org/blog/
#  https://www.w3schools.com
# Tech with Tim:https://www.youtube.com/watch?v=2BikxsbkuIU
# Coding With Russ https://www.youtube.com/watch?v=Ulp1Kimblg0
# BaralTech https://www.youtube.com/watch?v=GMBqjxcKogA

#imports libraries
import pygame as pg
from pygame.sprite import Sprite
from pygame import mixer
import random
from random import randint
import time
from settings import *
import os 
from Sound import *


# Setup asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'Images')

game_folder = os.path.dirname(__file__)
sound_folder = os.path.join(game_folder, 'Sound')

vec = pg.math.Vector2

# setting for the text
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

def colorbyte():
    return random.randint(0,255)
# sprites...
#player movement and size
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # makes the sprite as a image from images folder
        self.image = pg.image.load(os.path.join(img_folder, 'Basket.jpg')).convert()
        # removes black background
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT-40)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 100
# keyboard controls
    def controls(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
             self.acc.x = -5

        if keys[pg.K_d]:
            self.acc.x = 5
        
        if keys[pg.K_LEFT]:
            self.acc.x = -5

        if keys[pg.K_RIGHT]:
            self.acc.x = 5

    def draw(self):
        pass
    def inbounds(self):
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH  
#updates the player 
    def update(self):

        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # friction
        self.acc.x += self.vel.x * -0.40
        # self.acc.y += self.vel.y * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # self.rect.x += self.xvel
        # self.rect.y += self.yvel
        self.rect.midbottom = self.pos

# The chracteristics of the floor
class Boarder(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#mob size, color, speed
class Mob(Sprite):
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        # makes the sprite an image
        self.image = pg.image.load(os.path.join(img_folder, 'Bad_Apple.jpg')).convert()
        # Removes the black background
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.speed = 8
# Respawns mob whenever it leaves the boundary/ game screen
    def boundscheck(self):
        if not self.rect.x > 0 or not self.rect.x < WIDTH:
            self.kill()
            m = Mob(randint(0,WIDTH), randint(0,HEIGHT), 25, 25, (RED))
            all_sprites.add(m)
            mobs.add(m)   
            print(m)
        elif not self.rect.y > 0 or not self.rect.y < HEIGHT:
            self.kill()
            m = Mob(randint(0,WIDTH), randint(0,HEIGHT), 25, 25, (RED))
            all_sprites.add(m)
            mobs.add(m)
            print(m)  
    def update(self):
        #self.rect.x += self.speed
        #makes mobs move down
        self.rect.y += self.speed
        self.boundscheck()

#Points size, and color, speed
class Food(Sprite):
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        # makes the sprite as a image from images folder
        self.image = pg.image.load(os.path.join(img_folder, 'Good_Apple.jpg')).convert()
        # Removes the black background
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        print(self.rect.center)
        self.rect.x = x
        self.rect.y = 0
        self.speed = 10
        def update(self):
            self.rect.x += 5
            self.rect.y += 5
            if sef.rect.x > WIDTH:
                self.rect.x = 0
            if sef.rect.y > HEIGHT:
                self.rect.y = 0
# Respawns a point whenever it leaves the boundary/game screen
    def boundscheck(self):
        if not self.rect.x > 0 or not self.rect.x < WIDTH:
            self.kill()
            f = Food(randint(0,WIDTH), randint(0,HEIGHT), 25, 25, (GREEN))
            all_sprites.add(f)
            foods.add(f)
            print(f)
        elif not self.rect.y > 0 or not self.rect.y < HEIGHT:
            self.kill()
            f = Food(randint(0,WIDTH), randint(0,HEIGHT), 25, 25, (GREEN))
            all_sprites.add(f)
            foods.add(f)
            print(f)
    def update(self):
        # makes food move down
        self.rect.y += self.speed
        self.boundscheck()

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Apple Catch")
clock = pg.time.Clock()



# Button Class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # Get Mouse location 
        pos = pg.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                #moves the button out of the screen when clicked
                self.rect.x += 500
                action = True

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        # Draws the button on the screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

#load button images 
start_img = pg.image.load(os.path.join(img_folder, 'start_btn.jpeg')).convert_alpha()
exit_img = pg.image.load(os.path.join(img_folder, 'exit_btn.jpeg')).convert_alpha()

# Creates button instances
start_button = Button(30, HEIGHT/2, start_img, 1)
exit_button = Button(235, HEIGHT/2, exit_img, 1)

def move_exit_button():
    exit_button = Button(500, HEIGHT/2, exit_img, 1)

# Sound Variable
Mob_damage = pg.mixer.Sound(os.path.join(sound_folder, 'bad.wav'))
Point_catch = pg.mixer.Sound(os.path.join(sound_folder, 'good.wav'))

# Background Music
music = pg.mixer.music.load(os.path.join(sound_folder, 'background.wav'))
# loops the music
pg.mixer.music.play(-1)

# create groups
all_sprites = pg.sprite.Group()
all_grounds = pg.sprite.Group()
mobs = pg.sprite.Group()
foods = pg.sprite.Group()

# instantiate classes
player = Player()
# ground location
ground = Boarder(0, HEIGHT-40, WIDTH, 40)
ground2 = Boarder(0, -480, WIDTH, 40)

def sprite_spawn():
    # spawn in 5 mobs in random locations to start
    for i in range(5):
        m = Mob(randint(0,WIDTH), randint(0,HEIGHT), 25, 25, (RED))
        all_sprites.add(m)
        mobs.add(m)
        print(m)        
    # spwans in 2 points to start
    for i in range(2):
        f = Food(randint(0,WIDTH), randint(0,HEIGHT), 25, 25, (GREEN))
        all_sprites.add(f)
        foods.add(f)
        print(f)

# add things to groups...
all_sprites.add(player, ground, ground2)
all_grounds.add(ground, ground2)

# Game loop
running = True
while running:
    # keep the loop running using clock
        clock.tick(FPS)

        ###### Draw the background #######
        screen.fill(BLACK)

        # if the user preses the button it spawn in the point, and mob sprites
        if start_button.draw(screen):
            sprite_spawn() 
            move_exit_button()
            pg.display.update()
            print('Game Starting')

        # if the user hits exit it will close the game
        if exit_button.draw(screen):
            print('Game Ending')
            pg.QUIT() 
            


        hits = pg.sprite.spritecollide(player, all_grounds, False)

        mobhits = pg.sprite.spritecollide(player, mobs, True)
        # removes 10 health for every mob hit
        if mobhits:
            print("ive struck a mob")
            player.health -= 10
            Mob_damage.play()
            # respawns a new mob in when the player collides with it
            m = Mob(randint(0,WIDTH), randint(0,HEIGHT), 25, 25, (RED))
            all_sprites.add(m)
            mobs.add(m)
            print(m)
            
        # gives you 1 point per a food you catch
        foodhits = pg.sprite.spritecollide(player, foods, True)    
        if foodhits:
            print("ive earned a point")
            SCORE += 1
            Point_catch.play()
        # respawns a new apple in when the player collides with it
            f = Food(randint(0,WIDTH), randint(0,HEIGHT), 25, 25, (GREEN))
            all_sprites.add(f)
            foods.add(f)
            print(f) 
            
        ############ Update ##############
        # update all sprites
        all_sprites.update()

        # draw text
        # shows how many points and your health in the game
        # draw all sprites
        draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
        draw_text ("HEALTH: " + str(player.health), 22, WHITE, WIDTH / 2, HEIGHT / 10)
        all_sprites.draw(screen)


        # buffer - after drawing everything, flip display
        pg.display.flip()

        # If you close the game it will tell you your points and health
        for event in pg.event.get():
            # check for closed window
            if event.type == pg.QUIT:
                running = False
                print ("Why quit, your score was: " + str(SCORE) + " and your health was: " + str(player.health))


        # Prints your score once you die, and ends game
        if player.health == 0:
            print ("You died, your score is" + str(SCORE))
            pg.QUIT()

        pg.display.update()