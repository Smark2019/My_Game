import pygame
import random,time

from pygame.locals import (
RLEACCEL,
K_UP,
K_DOWN,
K_LEFT,
K_RIGHT,
K_ESCAPE,
KEYDOWN,QUIT
)

pygame.init()

screen_w = 1200
screen_h = 600

screen = pygame.display.set_mode((screen_w,screen_h))

running_game = True


# Player class (extends pygame.sprite.Sprite):

class Player (pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        
        self.surface = pygame.image.load("/home/salih/Desktop/game/tank.png").convert()
        
        self.surface.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surface.get_rect()
       

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)

        if pressed_keys[K_LEFT]:

            self.rect.move_ip(-5, 0)

        if pressed_keys[K_RIGHT]:

            self.rect.move_ip(5, 0)
            
        if self.rect.left < 0:
            self.rect.left = 0
        
        if self.rect.right > screen_w:

            self.rect.right = screen_w

        if self.rect.top <= 0:

            self.rect.top = 0

        if self.rect.bottom >= screen_h:

            self.rect.bottom = screen_h

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.surface = pygame.image.load("/home/salih/Desktop/game/shuttle.png").convert()

        self.surface.set_colorkey((0,0,0), RLEACCEL)

        self.rect = self.surface.get_rect(center=(

                random.randint(screen_w + 20, screen_w + 100),

                random.randint(0, screen_h)))   
        self.speed = random.randint(1,5)

    def update(self):

        self.rect.move_ip(-self.speed, 0)

        if self.rect.right < 0:

            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud,self).__init__()
        self.surface = pygame.image.load("/home/salih/Desktop/game/clouds.png").convert()

        self.surface.set_colorkey((255, 255, 255), RLEACCEL)

        self.rect = self.surface.get_rect(center=(

                random.randint(screen_w + 20, screen_w + 100),

                random.randint(0, screen_h)))   
        self.speed = 2

    def update(self):

        self.rect.move_ip(-self.speed, 0)

        if self.rect.right < 0:

            self.kill()

class Explosion(pygame.sprite.Sprite):

	def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            for num in range(1, 6):
                path = "/home/salih/Desktop/game/img/exp{}.png".format(num)
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (100, 100))
                self.images.append(img)
            self.index = 0
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            self.counter = 0

	def update(self):
		explosion_speed = 4
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, reset animation index
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()



player = Player()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# Events in the game:
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)


clock = pygame.time.Clock()


exp_frame = 0

while running_game or exp_frame < 5:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running_game = False
    
        elif event.type ==  QUIT:

            running_game = False
        # Add a new enemy?

        elif event.type == ADDENEMY:

            # Create the new enemy and add it to sprite groups

            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD:

            # Create the new clouds and add it to sprite groups

            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
       
    pressed_keys = pygame.key.get_pressed()
    #print(pressed_keys)

    player.update(pressed_keys)
    enemies.update()
    clouds.update()
    screen.fill((39, 158, 232))
    #screen.fill((0, 0, 0))

    explosion_group.update()

    # Draw all sprites

    for entity in all_sprites:
        screen.blit(entity.surface, entity.rect)

    clock.tick(100)

    # player hits the rockets:
    if pygame.sprite.spritecollideany(player, enemies):
        global exp_frame
        new_explosion = Explosion(player.rect.centerx,player.rect.centery) 
        explosion_group.add(new_explosion)
        explosion_group.draw(screen)
        exp_frame = exp_frame + 1
        print(str(exp_frame) + "Explosion done !")
        if(exp_frame == 5):
            player.kill()
            print(" Player will be killed !")
        
        
        running_game = False


    pygame.display.flip()

exp_frame = 0

time.sleep(1)

pygame.quit()

        
