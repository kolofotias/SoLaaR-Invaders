# Modified and released by: Vaios "SoLaaR" Kolofotias 
# Author: Vaios Kolofotias,Dario "Riovandaino" Navoni
# Name: SoLaaR-Invaders
# Tested: Linux
#
# The script is published under GNU General Public License; you can redistribute it
# and/or modify it under the terms of GNU General Public License, specifying author
# and source. See the GNU General Public License for more details. To receive a copy of
# GNU GPL write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston,MA 02110-1301, USA.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

try:
    import pygame, random
    from pygame.locals import *
except ImportError:
     print "Some dependencies are not satisfied"
     exit()

################### T H E  G A M E  L I B R A R Y ####################

class GameEntity(pygame.sprite.Sprite):
    
    def __init__(self,x,y,image,life,speed):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect((x,y),(image.get_width(),image.get_height()))
        self.image = image
        self.life = life
        self.speed = speed

    def render(self,surface):
        surface.blit(self.image,(self.rect.x,self.rect.y))

class Enemy(GameEntity):

    def __init__(self,x,y,image,life,speed):
        GameEntity.__init__(self,x,y,image,life,speed)
        self.direction = 1
        self.bullets = pygame.sprite.Group()
        self.tot_life = life

    def update(self,time):
        self.rect.move_ip(self.direction*self.speed*time,0)

    def change_direction(self,speed,time):
        self.rect.move_ip(0,speed*time)
        self.direction = -self.direction

    def shoot(self,bullet_image,bullet_speed):
        self.bullets.add(Bullet(self.rect.x+self.image.get_width()/2,self.rect.y+self.image.get_height(),bullet_image,1,bullet_speed,1))

class Bullet(GameEntity):
    
    def __init__(self,x,y,image,life,speed,direction):
        GameEntity.__init__(self,x,y,image,life,speed)
        self.direction = direction

    def update(self,time):
        self.rect.move_ip(0,self.direction*self.speed*time)

class Ship(GameEntity):
    
    def __init__(self,x,y,image,life,speed):
        GameEntity.__init__(self,x,y,image,life,speed)
        self.bullets = pygame.sprite.Group()
        self.lives = 3
        self.weapons = 5
        self.hit = 0

    def update(self,direction,time):
        self.rect.move_ip(self.speed*direction*time,0)
        if self.rect.x <= 0: self.rect.x = 0
        elif self.rect.x >= 640 - self.image.get_width(): self.rect.x = 640 - self.image.get_width()

    def shoot(self,bullet_image,bullet_speed):
        if self.weapons > 0:
            self.bullets.add(Bullet(self.rect.x+self.image.get_width()/2,self.rect.y,bullet_image,1,bullet_speed,-1))
            self.weapons -= 1
  
class Explosion:
    def __init__(self,x,y): 
        self.center = (x,y)
        self.life = random.randint(10,30)
        self.r1 = 10
        self.r2 = 1

    def render(self,surface):
        if self.life > 0:
            pygame.draw.circle(surface,(255,255,0),self.center,int(self.r1))
            pygame.draw.circle(surface,(0,0,0),self.center,int(self.r2))
            self.r1 += 1
            self.r2 += 1.3
            self.life -= 1
