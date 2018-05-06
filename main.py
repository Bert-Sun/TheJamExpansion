'''
Timur Khayrullin
ICS3CUJJJ1 - 01
Mr.Van Rooyen
Wednesday, January 24, 2018

Final computer science summative "ultimate antivirus"
'''

#imports necessary modules
from enemies import *
from player import *
from items import *
from boss import *

from pygame import *
from sys import *
from math import *
import random
init()

# screen init
backg = ('background.png') 
SIZE = WIDTH, HEIGHT = (1000,700)
screen = display.set_mode(SIZE)
bk = image.load(backg).convert_alpha()
bk = transform.scale(bk, (WIDTH, HEIGHT))

# color init 
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (128,128,128)

# font init 
fontCal = font.Font('resources/fonts/Calibri.ttf', 35)
fontGeneral = font.Font('resources/fonts/Calibri.ttf', 30)
fontHealth = font.Font('resources/fonts/Calibri Bold.ttf', 15)
fontTitle = font.Font('resources/fonts/FORCED SQUARE.ttf', 100)


#class that handles everything related to the player

#list of displayable guns
bulletDisplay = [image.load('resources/player/gattling_bullet.png').convert_alpha(), image.load('resources/player/sniper_bullet.png').convert_alpha()]
bullets = []

enemyBullets = []

enemies = []
spawnX = 0
spawnY = 0

mainMenuRect = []
for y in range(200, 500, 100):
    mainMenuRect.append(Rect(400, y, 200, 75))
    
#function for drawing the main menu
def drawMain(): 
    draw.rect(screen, BLACK, (0,0, WIDTH, HEIGHT))
    screen.blit(fontTitle.render("Ultimate Antivirus",  1,  (0,  255,  0)), (100, 5, fontTitle.size("Ultimate Antivirus")[0], fontTitle.size("Ultimate Antivirus")[1]))
    texts = ["Play game", "Exit game"]
    for i in range(2): #sequentially draws buttons for menu, using text from list above if necessary
        draw.rect(screen, WHITE, mainMenuRect[i])
        text = fontGeneral.render(texts[i],  1,  (0,  0,  0))	
        screen.blit(text, mainMenuRect[i].move(5,5)) 

instructImages = ['resources/instructions/instructions1.png', 'resources/instructions/instructions2.png', 'resources/instructions/instructions4.png', 'resources/instructions/instructions5.png',]
def drawInstructions():
    #displays sequence of text and images to give instructions 
    screen.blit(bk, (0,0))
    display.flip()
    
    texts = ["you are an extremely advanced antivirus", "employed by TimKhay industries,", "made to destroy any incoming viruses directly, in real time."]
    #tells story through center-aligned text
    for text in texts: 
        screen.blit(fontGeneral.render(text, 1, WHITE), (WIDTH // 2 - fontGeneral.size(text)[0] // 2, int(.20 * HEIGHT) + int((fontGeneral.size(text)[1] + 3) * texts.index(text))))
        screen.blit(fontGeneral.render("Press and hold space to skip instructions", 1, WHITE), (WIDTH // 2 - fontGeneral.size("press and hold space to skip instructions")[0] // 2, HEIGHT - fontGeneral.size("press and hold space to skip instructions")[1] - 5))
        display.flip()
        
        #checks if skip is wanted, if so, skips instructions
        event.pump()
        for ticks in range(1750):
            if key.get_pressed()[K_SPACE] != 0:
                    break
            time.wait(1) 
        else:
            continue
    else:
        #cycles through intruction images, showing more elaborate info
        for img in instructImages:
            screen.blit(image.load(img), (0,0))
            screen.blit(fontGeneral.render("Press and hold space to skip instructions", 1, WHITE), (200, HEIGHT - fontGeneral.size("press and hold space to skip instructions")[1] - 5))
            display.flip()
            #checks if skip is wanted, if so, skips instructions
            event.pump()
            for ticks in range(4000):
                if key.get_pressed()[K_SPACE] != 0:
                    break
                time.wait(1)
            else:
                continue
            break
    
    #displays final good luck message
    screen.blit(bk, (0,0))
    fontGeneral.render(text, 1, WHITE)
    text = "Good Luck!"
    screen.blit(fontGeneral.render(text, 1, WHITE), (WIDTH // 2 - fontGeneral.size(text)[0] // 2, int(.20 * HEIGHT) + int((fontGeneral.size(text)[1] + 3))))
    display.flip()
    time.wait(3000)    

returnRect = mainMenuRect[2].move(0, mainMenuRect[2][3] + 25)
def drawLoseScreen():
    #displays simple lose screen with a button to go back to main menu
    draw.rect(screen, BLACK, (0,0, WIDTH, HEIGHT))
    screen.blit(fontTitle.render("You Lost!",  1,  (0,  255,  0)), (100, 5, fontTitle.size("You Lost!")[0], fontTitle.size("You Lost!")[1]))    
    draw.rect(screen, WHITE, returnRect)
    text = fontGeneral.render("Return to",  1,  (0,  0,  0))
    screen.blit(text, returnRect)
    text = fontGeneral.render("Main menu",  1,  (0,  0,  0))
    screen.blit(text, returnRect.move(0, fontGeneral.size("Main menu")[1] + 3))

def drawWinScreen():
    #displays simple win screen with a button to go back to main menu, and some credits
    draw.rect(screen, BLACK, (0,0, WIDTH, HEIGHT))
    screen.blit(fontTitle.render("You're winner!",  1,  (0,  255,  0)), (100, 5, fontTitle.size("You're winner!")[0], fontTitle.size("You're winner!")[1]))  
    screen.blit(fontTitle.render("Made by:",  1,  (0,  255,  0)), (100, fontTitle.size("Made by")[1] * 2 + 5, fontTitle.size("Made by")[0], fontTitle.size("Made by")[1]))  
    screen.blit(fontTitle.render("Timur Khayrullin",  1,  (0,  255,  0)), (100, fontTitle.size("Made by")[1] * 3 + 5, fontTitle.size("Timur Khayrullin")[0], fontTitle.size("Timur Khayrullin")[1]))
    screen.blit(fontTitle.render("2018",  1,  (0,  255,  0)), (100, fontTitle.size("Made by")[1] * 4 + 5, fontTitle.size("2018")[0], fontTitle.size("2018")[1]))
    draw.rect(screen, WHITE, returnRect)
    text = fontGeneral.render("Return to",  1,  (0,  0,  0))
    screen.blit(text, returnRect)
    text = fontGeneral.render("Main menu",  1,  (0,  0,  0))
    screen.blit(text, returnRect.move(0, fontGeneral.size("Main menu")[1] + 3))

#list of rects for upgrade buttons
upgradeRect = []
for y in range(200, 500, 115):
    for x in range(200, 800, 200):
        upgradeRect.append(Rect(x, y, 185, 100))
    
def drawUpgradeScreen():
    #as long as boss level isn't ahead, displays upgrade instructions
    draw.rect(screen, BLACK, (0,0, WIDTH, HEIGHT))
    if level < 5 :
        screen.blit(fontTitle.render("Level Up!",  1,  (0,  255,  0)), (50, 5, fontTitle.size("Level Up! Choose your upgrade")[0], fontTitle.size("Level Up! Choose your upgrade")[1]))  
        screen.blit(fontTitle.render("Choose your upgrade",  1,  (0,  255,  0)), (50, fontTitle.size("Choose your upgrade")[1]+5, fontTitle.size("Choose your upgrade")[0], fontTitle.size("Choose your upgrade")[1]))
    else:
        #shows boss warning
        screen.blit(fontTitle.render("Warning:",  1,  (255,  0,  0)), (50, 5, fontTitle.size("Warning:")[0], fontTitle.size("Warning")[1]))  
        screen.blit(fontTitle.render("Boss Battle Ahead",  1,  (255,  0,  0)), (50, fontTitle.size("Boss Battle Ahead")[1]+5, fontTitle.size("Boss Battle Ahead")[0], fontTitle.size("Boss Battle Ahead")[1]))        
    #for each text, displays corresponding upgrade button with text on it
    texts = ['+ damage', '+ speed', '+ firing speed', 'Restore health', '+ max health', '+ shot speed']
    for i in range(len(texts)):
        draw.rect(screen, WHITE, upgradeRect[i])  
        #draw.rect(screen, RED, rect, 4)
        text = fontGeneral.render(texts[i],  1,  (0,  0,  0))	
        screen.blit(text, upgradeRect[i].move(5,5))

#general var init
clock = time.Clock()
running = True
x = WIDTH // 2 - 50
y = HEIGHT // 2 - 50
button = 0
mx, my = 0,0

#menu state init
menu = 0
MAIN = 0
START = 1
HIGHSCORES = 2
LOSE = 3
WIN = 6
PAUSE = 4
UPGRADE = 5
runMenu = True
game = False

#level var init
level = 1
wave = 0
waitingEnemies = []
pickups = []
enemyWaitTime = 0
enemySpawnTime = 500
enemyChoice = 0
enemyPoints = 0
graceTimer = 0

#used for debugging the game (set to true for cheats)
debug = False          



#list of class names for all bullet types
guns = [Gattling, Sniper]
# list of pngs of all bullets in the game
bulletPics = [image.load('resources/player/gattling_bullet.png').convert_alpha(), image.load('resources/player/sniper_bullet.png').convert_alpha()]
#abreviation for player class
bossFight = False
pl = Player(mx, my , x ,y)
bs = Boss()
# var init for player bullet timer
startTicks = 0

#main loop
while running:
    
    #menu loop
    while runMenu:
        for evnt in event.get():
            if evnt.type == QUIT:
                quit()
            if evnt.type == MOUSEBUTTONDOWN:
                # checks if any mouse button is down,  if so sets clicking to true
                button = evnt.button
            if evnt.type == MOUSEBUTTONUP:
                # checks if any mouse button is down,  if so sets clicking to true
                button = 0       
            if evnt.type == MOUSEMOTION:
                # sets mx and my to mouse x backgand y if mouse is moving
                mx, my  = evnt.pos 
        if menu == MAIN:
            drawMain()
            if button == 1:
                #starts or exits the game
                if mainMenuRect[0].collidepoint(mx, my):
                    menu = START
                elif mainMenuRect[1].collidepoint(mx, my):                        
                    running = False
                    runMenu = False 
        if menu == START:
            #initializes all game-related vars and starts game
            '''Shows instructions, stops menu'''
            drawInstructions()
            runMenu = False 
            
            '''Resets all variables used for game'''
            #general var init
            x = WIDTH // 2 - 50
            y = HEIGHT // 2 - 50
            button = 0
            mx, my = 0,0
            
            #level var init
            pl.health = 1000
            level = 1
            wave = 0
            pickups = []
            enemies = []
            bullets = []
            enemyBullets = []
            waitingEnemies = []
            enemyWaitTime = 0
            enemySpawnTime = 500
            enemyChoice = 0
            enemyPoints = 0 
            graceTimer = 0
            bossFight = False
            
            '''Starts game loop'''
            game = True
        
        # checks for return to menu button for win and lose screens
        if menu == LOSE:
            drawLoseScreen()
            if button == 1:
                if returnRect.collidepoint((mx, my)):
                    menu = MAIN
        
        if menu == WIN:
            drawWinScreen()
            if button == 1:
                if returnRect.collidepoint((mx, my)):
                    menu = MAIN        
              
        if menu == UPGRADE:
            
            drawUpgradeScreen()
            if button == 1:
                #if clicked upgrade button, changes appropriate stat and resumes game 
                if upgradeRect[0].collidepoint(mx, my):
                    pl.dmg_upG += 7
                if upgradeRect[1].collidepoint(mx, my):
                    pl.speed += 5
                if upgradeRect[2].collidepoint(mx, my):
                    pl.firingSpeed_upG += 44
                if upgradeRect[3].collidepoint(mx, my):
                    pl.health = pl.max_health                
                if upgradeRect[4].collidepoint(mx, my):
                    pl.max_health += 500
                if upgradeRect[5].collidepoint(mx, my):
                    pl.shotSpeed_upG += 1                
                for r in upgradeRect[:6]:
                    if r.collidepoint(mx, my):
                        runMenu = False
                        game = True
                
                
    
        # obligatory frame-check and display flip
        clock.tick(60)
        display.flip()
    while game:
        for evnt in event.get():
            if evnt.type == QUIT:
                quit()
            if evnt .type == MOUSEBUTTONDOWN:
                # checks if any mouse button is down,  if so sets clicking to true
                button = evnt.button
                #startTicks = time.get_ticks()            
            if evnt.type == MOUSEBUTTONUP:
                # checks if any mouse button is down,  if so sets clicking to true
                button = 0       
            if evnt.type == MOUSEMOTION:
                # sets mx and my to mouse x backgand y if mouse is moving
                mx, my  = evnt.pos
            
            if evnt.type == KEYDOWN:
                #handles keyboard movement (if key pressed, corresponding direction = True)
                if evnt.key == K_w:
                    pl.directions[0] = True
                if evnt.key == K_s:
                    pl.directions[1] = True
                if evnt.key == K_a:
                    pl.directions[2] = True
                if evnt.key == K_d:
                    pl.directions[3] = True
                if evnt.key == K_m:
                    enemies = []
                    waitingEnemies = []
                    
                #debug binds (cheats to test stuff)
                if debug == True:
                    #triggers upgrade screen
                    if evnt.key == K_g:
                        level += 1
                        game = False
                        runMenu = True
                        menu = UPGRADE
                    
                    #adds wave
                    if evnt.key == K_h:
                        wave += 1    
                    
                    #spawns enemies based on number key pressed
                    if evnt.key == K_1:
                        enemies.append(Enemy(0,0))
                    if evnt.key == K_2:
                        enemies.append(Shooter(0,0))    
                    if evnt.key == K_3:
                        enemies.append(Wolf(0,0)) 
                    if evnt.key == K_4:
                        enemies.append(Turret(0,0))
                    if evnt.key == K_b:
                        #toggles bossfight
                        bossFight = not bossFight
                    #cycles guns
                    if evnt.key == K_SPACE:
                        if pl.gun == len(guns)-1:
                            pl.gun = 0
                        else:
                            pl.gun += 1
                
            #sets apt. directions to false if key is no longer pressed
            if evnt.type == KEYUP:
                if evnt.key == K_w:
                    pl.directions[0] = False
                if evnt.key == K_s:
                    pl.directions[1] = False
                if evnt.key == K_a:
                    pl.directions[2] = False
                if evnt.key == K_d:
                    pl.directions[3] = False  
        
        if button == 1:
            
            #if bullet timer is met, creates a new bullet at appropriate x and y, catches fire rates less than 2 (because bullets start going backwards or don't move a all if they hit a fire rate of < 2)
            totalFiringSpeed = guns[pl.gun](pl.muzzle_x, pl.muzzle_y, mx, my).firing_speed - pl.firingSpeed_upG
            if totalFiringSpeed < 2:
                totalFiringSpeed = 2
            if time.get_ticks() - startTicks > totalFiringSpeed:
                bullets.append(guns[pl.gun](pl.muzzle_x, pl.muzzle_y, mx, my))
                startTicks = time.get_ticks()
        
        
        
        #after level 5, gets ready for bossfight
        if level == 5:
            bossFight = True
        
        #ends game at level 6
        elif level == 6:
            game = False
            runMenu = True
            menu = WIN
        
        
        #goes to new level once waves are completed, prompts upgrade screen
        if wave == 5 and enemies == [] and waitingEnemies == []:
            if graceTimer >= 90:
                level +=1
                wave = 1
                game = False
                runMenu = True
                menu = UPGRADE
                pl.x, pl.y = WIDTH//2, HEIGHT//2
                button = 0
                graceTimer = 0
                pl.directions = [False, False, False, False]
                
            else:
                graceTimer += 1
        #handles enemy spawn plan (number of enemies, type of enemy, damage, speed etc)
        elif enemies == [] and waitingEnemies == [] and graceTimer == 0 and not debug and not bossFight:
            enemyPoints = int((wave * 2) + (2 * level) + 1)
            #enemy points decrease with every enemy planned (different reduction for each enemy)
            while enemyPoints > 0:
                spawnX = random.choice([random.randint(0 - 100, WIDTH), random.choice([0 - 100, WIDTH])])
                
                if spawnX == 0 or spawnX == WIDTH:
                    spawnY = random.randint(0 - 100, HEIGHT)
                else:
                    spawnY = random.choice([0 - 100, HEIGHT])
                
                #on level 1, can only spawn grunts
                if level < 2:
                    waitingEnemies.append(Enemy(spawnX, spawnY)) 
                    enemyPoints -= 1
                # on level 2, can spawn grunts and shooters
                elif level < 3:
                    enemyChoice = random.randint(0, 100)
                    if enemyChoice >= 80:
                        waitingEnemies.append(Shooter(spawnX, spawnY))
                        enemyPoints -= 2
                    else:
                        waitingEnemies.append(Enemy(spawnX, spawnY))
                        enemyPoints -= 1
                #on level 3, can spawn grunts, shooters or wolves
                elif level < 4:
                    enemyChoice = random.randint(0, 100)
                    if enemyChoice >= 85:
                        enemyPoints -= 3
                        waitingEnemies.append(Wolf(spawnX, spawnY))
                    elif enemyChoice >= 75:
                        waitingEnemies.append(Shooter(spawnX, spawnY))
                        enemyPoints -= 2
                    else:
                        waitingEnemies.append(Enemy(spawnX, spawnY))      
                        enemyPoints -= 1
                else:
                    #on any level after, can spawn grunts, shooters, wolves and turrets
                    enemyChoice = random.randint(0, 100)
                    if enemyChoice >= 85:
                        enemyPoints -= 3
                        waitingEnemies.append(Wolf(spawnX, spawnY))
                    elif enemyChoice >= 75:
                        waitingEnemies.append(Shooter(spawnX, spawnY))
                        enemyPoints -= 2
                    elif enemyChoice >= 65:
                        waitingEnemies.append(Turret(spawnX, spawnY))
                        enemyPoints -= 7                    
                    else:
                        waitingEnemies.append(Enemy(spawnX, spawnY))      
                        enemyPoints -= 2     
            #adds to wave
            wave+=1
            
    
        #handles waiting enemy spawning, if timer allows, pops object(s) from waitingEnemies and appends it to enemies (spawns multiple at once if it can). 
        if len(waitingEnemies) > 0:
            if time.get_ticks() - enemyWaitTime >= enemySpawnTime:
                if len(waitingEnemies) > ceil(wave / 2):
                    for i in range(ceil(wave / 2)):
                        enemies.append(waitingEnemies.pop())
                else:
                    enemies.append(waitingEnemies.pop())
                
                #Timer decreases alot with level, a little with wave too
                enemySpawnTime = 3000 - level * 250 - wave * 150
                
                #if timer is less than 200, sets timer to 200
                if enemySpawnTime < 200: 
                    enemySpawnTime = 200
                    
                enemyWaitTime = time.get_ticks()
        
        #Enemy bullet append
        for enemy in enemies:
            if isinstance(enemy, Shooter):
                if enemy.fire_time >= enemy.firing_speed:
                    enemyBullets.append(EnemyBullet(enemy.center_x, enemy.center_y, pl.center_x, pl.center_y))
                    enemy.fire_time = 0
                else:
                    enemy.fire_time += 1
                    
            #If enemy is turret, shoot 4 bullets at alternating angles
            elif isinstance(enemy, Turret):
                if enemy.fire_time >= enemy.firing_speed:
                    if enemy.gun_state == 1:
                        for i in enemy.angles_1:
                            #gets point from angle and radius
                            enemy.turretTarget = (enemy.center_x + enemy.w // 2 * cos(radians(i)), 
                                                  enemy.center_y + enemy.w // 2 * sin(radians(i)))
                            enemyBullets.append(EnemyBullet(enemy.center_x, enemy.center_y, enemy.turretTarget[0], enemy.turretTarget[1]))
                            enemy.gun_state = 0
                    else:
                        for i in enemy.angles_2:
                            #gets point from angle and radius
                            enemy.turretTarget = (enemy.center_x + enemy.w // 2 * cos(radians(i)), 
                                                  enemy.center_y + enemy.w // 2 * sin(radians(i)))
                            enemyBullets.append(EnemyBullet(enemy.center_x, enemy.center_y, enemy.turretTarget[0], enemy.turretTarget[1]))
                            enemy.gun_state = 1
                            
                    enemy.fire_time = 0                        
                else:
                    enemy.fire_time += 1                
        
        screen.blit(bk, (0, 0))
        
        """Drawing of everything"""
        # Draws pickups
        for item in pickups:
            item.draw(screen)
            if not item.update(pl):
                pickups.remove(item)
        
        # Draws all enemies
        for enemy in enemies:
            enemy.draw(screen)
            #enemy.debug(pl.center_x, pl.center_y) #debug info display for enemy
            enemy.update(pl.center_x, pl.center_y, enemies)
            if not enemy.check(bullets, pickups, pl):
                enemies.remove(enemy)
            
        #draws boss, if it can
        if bossFight:
            bs.draw()
            bs.update()
            bs.check()

            
            
        # Draws all enemy bullets
        for bullet in enemyBullets:
            bullet.draw(screen)
            #bullet.debug() #draws debug info for bullets
            bullet.update()
            if not bullet.check(pl.hitbox):
                bullets.remove(bullet)
            
        # Draws bullets
        for bullet in bullets:
            bullet.draw(screen)
            #bullet.debug()
            bullet.update()
            if not bullet.check(enemies, bossFight):
                bullets.remove(bullet)
            
        # Draws player
        pl.rotate(mx, my)
        pl.update(mx, my, enemies, enemyBullets)
        #if health goes to or below 0, ends game and starts menu loop
        if pl.health <= 0 and debug == False:
            game = False
            runMenu = True
            menu = LOSE        
        pl.draw(screen)
        #pl.debug(guns[pl.gun](pl.muzzle_x, pl.muzzle_y, mx, my).firing_speed) #debug info display for player
    
        """HUD drawing"""
    
        #displays current gun's bullet at 3x size
        bullDisplayW = int(bulletPics[pl.gun].get_width() * 1.5)
        bullDisplayH = int(bulletPics[pl.gun].get_height() * 1.5)
        screen.blit(transform.scale(bulletPics[pl.gun], (bullDisplayW, bullDisplayH)), Rect(15 + 12 - bullDisplayW // 2, 45 + 12 - bullDisplayH // 2, bullDisplayW, bullDisplayH))
        
        #displays current level, wave and remaining enemies
        text = fontCal.render("level %i" %level, 1,BLACK)
        textSize = fontCal.size("level %i" %level)
        screen.blit(text, (WIDTH - textSize[0] - 15, textSize[1] - 15))
        
        text = fontCal.render("wave %i" %wave, 1,BLACK)
        textSize = fontCal.size("wave %i" %wave)
        screen.blit(text, (WIDTH - textSize[0] - 15, textSize[1] * 2 - 15))        
        
        text = fontCal.render("Remaining viruses: %i" %(len(waitingEnemies) + len(enemies)) , 1,BLACK)
        textSize = fontCal.size("Remaining viruses: %i" %(len(waitingEnemies) + len(enemies)) )
        screen.blit(text, (WIDTH - textSize[0] - 15, textSize[1] * 3 - 15))
        
        
        # obligatory frame-check and display flip
        clock.tick(60)
        display.flip()
        
quit()