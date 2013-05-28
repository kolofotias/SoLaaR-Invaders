# Modified and released by: Vaios "SoLaaR" Kolofotias 
# Author: Vaios Kolofotias,Dario "Riovandaino" Navoni
# Name: SoLaaR-Invaders
# Tested: Linux
#
# The script is published under GNU General Public License; you can redistribute it
# and/or modify it under the terms of GNU General Public License, specifying author
# and source. See the GNU General Public License for more details. To recive a copy of
# GNU GPL write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston,MA 02110-1301, USA.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

try:
    from lib import *
    from helpers import *
except ImportError: 
    print "Some dependencies are not satisfied"
    exit()

bullet = pygame.Surface((5,15))
bullet1 = pygame.Surface((5,15))
bullet.fill((255,0,0))
bullet1.fill((255,255,0))
images = [load_image("enemy1.jpg"),load_image("enemy2.jpg"),load_image("enemy3.jpg"),load_image("enemy4.jpg"),load_image("ship.bmp"),bullet,bullet1]

pygame.init()

# The main function
def main():
    print "### SoLaaRInvaders v. 0.1 ###"
    screen = pygame.display.set_mode((640,480),0,32)
    pygame.display.set_caption("SoLaaR Invaders")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    while 1:
        if menu(screen,images,clock) == 1:
            fullscreen = False
            ship = Ship(320,480-images[4].get_height(),images[4],1,200)
            level = 1
            score = 0
            m = True
            while m:
                enemies = pygame.sprite.Group()
                present_level(screen,level,clock)
                gen_enemies(level,enemies,images)
                m,score,fullscreen = manage_level(screen,ship,enemies,score,images,clock,fullscreen,level)
                if m == True: level += 1
                else: 
                    save_highscore(score)
        else: 
            print "Goodbye"
            exit()

if __name__ == "__main__": 
    main()

