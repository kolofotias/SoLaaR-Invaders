#!usr/bin/python

# (C) 2009 SoLaaR
#
# Author: Vaios Kolofotias
# Name: SoLaaR-Invaders
#
#
# This code is published under GNU General Public License; you can redistribute it
# and/or modify it under the terms of GNU General Public License, specifying author
# and source. See the GNU General Public License for more details. To recive a copy of
# GNU GPL write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston,MA 02110-1301, USA.
#
try:
    import pygame, os, random
    import sys
    from pygame.locals import *
    from lib import *
except ImportError:
    print "Some dependencies are not satisfied"
    exit()


pygame.mixer.init()
#function to load a sound file

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound

global explosion          
explosion = load_sound("explosion.wav")  
global applause
applause = load_sound("applause.wav")
global intro
intro = load_sound("intro.wav")
global hurt
hurt = load_sound("hurt.wav")
global shot
shot = load_sound("shot-1.ogg")
global back
back = load_sound("back.wav")

# A function to load images
def load_image(name):
    path = os.path.join('data',name)
    return pygame.image.load(path)

global backdrop
backdrop = load_image("backdrop.jpg")

# A function that generate the next group of enemies
def gen_enemies(level,group,images):
    if level < 5:
        x = 20
        y = 50
        for i in range(2):
            for j in range(5):
                group.add(Enemy(x,y,images[level-1],level,100))
                x += 100
            y += 50
            x = 50
    elif level >= 5:
        geometry = random.randint(1,3)
        if geometry == 1:
            rows = random.randint(3,6)
            x1 = x = 20
            y = 50
            for i in range(rows):
                for j in range(5):
                    t = random.randint(1,4)
                    group.add(Enemy(x,y,images[t-1],t,100))
                    x += 100
                y += 50
                x1 += 20
                x = x1
        if geometry == 2:
            rows = random.randint(3,6)
            x1 = x = 20
            y = 50
            rows1 = rows
            for i in range(rows):
                for j in range(rows1):
                    t = random.randint(1,4)
                    group.add(Enemy(x,y,images[t-1],t,100))
                    x += 100
                rows1 -= 1
                y += 50
                x1 += 50
                x = x1
        if geometry == 3:
            rows = random.randint(3,6)
            x = 20
            y = 50
            for i in range(rows):
                for j in range(rows):
                    t = random.randint(1,4)
                    group.add(Enemy(x,y,images[t-1],t,100))
                    x += 100
                y += 50
                x = 20

# A function to save highscores
def save_highscore(score):
    if os.path.exists(os.path.join("data","highscores.txt")):
        f = open(os.path.join("data","highscores.txt"))
        if int(f.readlines()[0]) < score:
            f.close()
            f = open(os.path.join("data","highscores.txt"),"w")
            f.write(str(score))
            f.close()
        else: f.close()
    else:
        f = open(os.path.join("data","highscores.txt"),"w")
        f.write(str(score))
        f.close()

# A function to load highscores
def load_highscore():
    if os.path.exists(os.path.join("data","highscores.txt")):
        f = open(os.path.join("data","highscores.txt"))
        return int(f.readlines()[0])
    else: return 0

# The main loop of the game
def manage_level(screen,player,enemies,score,images,clock,fullscreen,level):
    highscore = load_highscore()
    font = pygame.font.SysFont("arial",15)
    font1 = pygame.font.Font(os.path.join("data","maiden.TTF"),50)
    explosions = []
    lose = 0
    k = 30
    while 1:
        time = clock.tick(30)/1000.
        if time > 0.1: time = 0.033
        backdrop = load_image('backdrop.jpg')
        screen.blit(backdrop, (0,0))
        #screen.fill((0,0,0))
        if score <= highscore:
            screen.blit(font.render("Score "+str(score),True,(255,255,255)),(5,5))
        else: screen.blit(font.render("Score "+str(score),True,(255,0,0)),(5,5))
        screen.blit(font.render("Highscore "+str(highscore),True,(255,255,255)),(105,5))
        screen.blit(font.render("Life "+str(player.lives),True,(255,255,255)),(250,5))
        screen.blit(font.render("Bullets "+str(player.weapons),True,(255,255,255)),(350,5))
        if player.lives > 0:
            if player.hit > 0:
                if player.hit % 2 != 0:
                    player.render(screen)
                    player.hit -= 1
                else: player.hit -= 1
            else: player.render(screen)
        player.bullets.draw(screen)
        enemies.draw(screen)
        for i in explosions:
            i.render(screen)
        for i in enemies.sprites():
            i.bullets.update(time)
            i.bullets.draw(screen)
        for i in enemies.sprites():
            if i.rect.x <= 0 or i.rect.x >= 640-i.image.get_width():
                t = time*level
                for j in enemies.sprites():
                    j.change_direction(100,time)
                break
            frequence = 1000/level
            if frequence < 100: frequence = 100
            if random.randint(1,int(frequence)) == 1: i.shoot(images[5],100)
            for j in i.bullets:
                if j.rect.y > 480: i.bullets.remove(j)
        enemies.update(time)
        player.bullets.update(time)
        for i in player.bullets.sprites():
            if i.rect.y < 0:
                player.bullets.remove(i)
                player.weapons += 1
        for e in pygame.event.get():
            if e.type == QUIT: exit()
            elif e.type == MOUSEMOTION:
                if player.lives > 0:
                    if e.rel[0] > 0: player.update(1,time)
                    elif e.rel[0] < 0: player.update(-1,time)
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE: exit()
                elif e.key == K_SPACE:
                    if player.lives > 0:
                        shot.play()                        
                        player.shoot(images[6],100)
                elif e.key == K_F1:
                    if fullscreen:
                        screen = pygame.display.set_mode((640,480),0,32)
                        fullscreen = False
                    elif not fullscreen:
                        screen = pygame.display.set_mode((640,480),FULLSCREEN,32)
                        fullscreen = True
                elif e.key == K_p:
                    pause(screen)
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1: player.shoot(images[6],100)
        if player.lives > 0:
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]: player.update(-1,time)
            elif keys[K_RIGHT]: player.update(1,time)
        collisions = pygame.sprite.groupcollide(player.bullets,enemies,True,False)
        for i in collisions.values():
            for j in i:
                explosion.play() 
                score += 50*j.tot_life
                if j.life > 0: j.life -= 1
                if j.life == 0: j.kill()
                explosions.append(Explosion(j.rect.x+j.image.get_width()/2,j.rect.y))
        for i in collisions.keys(): player.weapons += 1
        for i in enemies:
            collisions = pygame.sprite.groupcollide(player.bullets,i.bullets,True,True)
              
            for j in collisions.keys():
                player.weapons += 1
                explosions.append(Explosion(j.rect.x+j.image.get_width()/2,j.rect.y))
            collisions = pygame.sprite.spritecollide(player,i.bullets,True)
            if len(collisions) > 0:
                if player.hit == 0:
                    hurt.play()                     
                    player.lives -= 1
                    player.hit = 100
                    explosions.append(Explosion(player.rect.x+player.image.get_width()/2,player.rect.y))
        collisions = pygame.sprite.spritecollide(player,enemies,True)
        if len(collisions) > 0:
            if player.hit == 0:
                    player.lives -= 1
                    player.hit = 100
                    explosions.append(Explosion(player.rect.x+player.image.get_width()/2,player.rect.y))
        if lose > 0:
            if k >= 0 and k < 10:
                if score <= highscore:
                    screen.blit(font1.render("GAME OVER",True,(255,255,255)),(200,200))
                else: screen.blit(font1.render("NEW HIGHSCORE",True,(255,255,0)),(100,200))
                k += 1
            elif k >= 10 and k < 20: k += 1
            elif k >= 20: k = 0
        if player.lives == 0:
            lose += 1
            if lose == 200: return False,score,fullscreen
        elif len(enemies.sprites()) == 0 and len(explosions) == 0:
            player.bullets = pygame.sprite.Group()
            player.weapons = 5
            return True,score,fullscreen
        for i in explosions:
            if i.life == 0: explosions.remove(i)
        pygame.display.update()

# A function to present the next level
def present_level(screen,level,clock):
    font = pygame.font.SysFont("arial",50)
    loading = 0
        
    while loading < 100:
        clock.tick(30)
        screen.fill((0,0,0))
        intro.stop()        
        applause.play()      
        if loading >= 0 and loading <= 50:
            screen.blit(font.render("LOADING LEVEL "+str(level),True,(255,0,0)),(120,150))
        elif loading > 50 and loading <= 75:
            screen.blit(font.render("LOADING LEVEL "+str(level),True,(255,255,0)),(120,150))
        elif loading > 75 and loading < 100:
            screen.blit(font.render("LOADING LEVEL "+str(level),True,(0,255,0)),(120,150))
        screen.fill((255,0,0),(130,250,400,20))
        screen.fill((0,255,0),(130,250,loading*4,20))
        loading += 1
        pygame.display.update()

# A function to pause the game
def pause(screen):
    back.play()     
    font = pygame.font.Font(os.path.join("data","maiden.TTF"),50)
    screen.blit(font.render("PAUSE",True,(255,255,255)),(200,200))
    c = False
    pygame.display.update()
    while not c:
        for e in pygame.event.get():
            if e.type == QUIT: exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    exit()
                if e.key == K_p:
                    return 0

# A simple and user-friendly menu
def menu(screen,images,clock):
    font1 = pygame.font.Font(os.path.join("data","maiden.TTF"),90)
    font2 = pygame.font.SysFont("arial",50)
    k = 0
    pos = 1
    intro.play()    
    while 1:
        
        clock.tick(30)
        screen.fill((0,0,0))
        if k >= 0 and k < 10:
            screen.blit(font1.render("   SoLaaR",True,(0,255,0)),(10,1))
            k += 1
        elif k >= 10 and k < 20: k += 1
        elif k >= 20: k = 0
        pygame.draw.rect(screen,(255,255,0),((110,120),(400,300)),15)
        screen.blit(images[0],(200,150))
        screen.blit(images[1],(200,200))
        screen.blit(images[2],(200,250))
        screen.blit(images[3],(200,300))
        screen.blit(font2.render("  =  50",True,(255,255,255)),(250,150))
        screen.blit(font2.render("  =  100",True,(255,255,255)),(250,200))
        screen.blit(font2.render("  =  150",True,(255,255,255)),(250,250))
        screen.blit(font2.render("  =  200",True,(255,255,255)),(250,300))
        if pos == 0:
            screen.blit(font2.render("PLAY",True,(255,255,255)),(150,430))
            screen.blit(font2.render("QUIT",True,(0,255,0)),(300,430))
        elif pos == 1:
            screen.blit(font2.render("PLAY",True,(0,255,0)),(150,430))
            screen.blit(font2.render("QUIT",True,(255,255,255)),(300,430))
        for e in pygame.event.get():
            if e.type == QUIT: exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE: exit()
                elif e.key == K_LEFT:
                    pos -= 1
                    if pos < 0: pos = 1
                elif e.key == K_RIGHT:
                    pos += 1
                    if pos > 1: pos = 0
                elif e.key == K_RETURN: return pos
        pygame.display.update()
