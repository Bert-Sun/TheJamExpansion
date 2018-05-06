from pygame import *
from math import *
init()

fontHealth = font.Font('resources/fonts/Calibri Bold.ttf', 15)

#class that handles everything related to the player
class Player:
    
    
    def __init__(self, mouse_x, mouse_y, x, y):
        #player stats
        self.hasOxford = False
        self.gun = 1
        self.speed = 10
        self.max_health = 1000
        self.health = 1000
        self.dmg_upG = 0
        self.firingSpeed_upG = 0
        self.shotSpeed_upG = 0
        self.dmg_mult = 1
        self.coins = 0
        self.invulnerability = 0        
        #directions is a list containing states for moving up, down, left or right
        #speed is thepllayers speed constant (subject to change if upgrades are implemented)
        #x and y are thepllayers technical x and yplosition value, but they do not represent the hitbox. Think of them as theplosition of the top-left corner of the IMAGE for thepllayer.
        #original_image acts as a constant reference to the original image, and is used to avoid distortion
        #image is what changes during theplrogram
        #rect is the box of the IMAGE for thepllayer, it does not represent the hitbox.
        #hitbox w and h are the Height and Width of the hitbox for the player. they are constant.
        #center x and y represent the middle of the box of the IMAGE for thepllayer.
        #hitbox is what the enemy is going to want to hit in order to lower thepllayers' health. it's dimensions are constant, but it moves with thepllayer.
        self.directions = [False, False, False, False] 
        self.x = x
        self.y = y
        self.angle = 0
        self.mouse_x, self.mouse_y = mouse_x, mouse_y
        self.original_image = image.load('resources/player/cannonEnd1.png').convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.hitbox_w = self.rect[2]
        self.hitbox_h = self.rect[3]
        self.center_x, self.center_y = self.x + self.hitbox_w//2, self.y + self.hitbox_h//2
        self.hitbox = (self.center_x - 20, self.center_y - 20, 40, 40)
        self.muzzle_x = int(10 * (self.mouse_x - self.center_x) /
                      (sqrt((self.mouse_x - self.center_x) ** 2 +
                                 (self.mouse_y - self.center_y) ** 2)))
        self.muzzle_y = int(10 * (self.mouse_y - self.center_y) /
                      (sqrt((self.mouse_x - self.center_x) ** 2 +
                                 (self.mouse_y - self.center_y) ** 2)))
        
    
    #handles player orientation towards the mouse
    def rotate(self, mouseX, mouseY):
        #rel x and y finds the "vector" of the xplosition to the y position
        rel_x, rel_y = mouseX - self.x, mouseY - self.y
        #this is where the magic happens. math.atan2 is used to calculate the angle from the current position to the new mouse position (at least that's what I got from it)
        angle = (180 / pi) * -atan2(rel_y, rel_x) + 5
        self.angle = angle
        # Rotate the original image without modifying it.
        self.image = transform.rotate(self.original_image, int(angle))
        # Get a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center = self.rect.center)
     
    #handles movement and health of player
    def update(self, mouse_x, mouse_y, enemies, enemyBullets):
        if self.invulnerability != 0:
            self.original_image = image.load('resources/player/cannonEnd2.png').convert_alpha()
        else:
            self.original_image = image.load('resources/player/cannonEnd1.png').convert_alpha()        
        #if any direction states are true, movespllayer in said direction using self.speed
        if self.directions[0]:
            if 0 < self.center_y:
                self.y -= self.speed
        if self.directions[1]:
            if self.center_y < 700:
                self.y += self.speed
        if self.directions[2]:
            if 0 < self.center_x:
                self.x -= self.speed
        if self.directions[3]:
            if self.center_x < 1000:
                self.x += self.speed  
        #update hitBox and muzzle x/y
        self.center_x, self.center_y= self.x + self.hitbox_w//2, self.y + self.hitbox_h//2
        self.hitbox = Rect(self.center_x - 20, self.center_y - 20, 40, 40)
        # updates mouse x and y interpretation
        self.mouse_x, self.mouse_y = mouse_x, mouse_y
        
        # creates a line from the center of the player to the muzzle
        try:
            self.muzzle_x = self.center_x + int(35 * (self.mouse_x - self.center_x) /
                          (sqrt((self.mouse_x - self.center_x) ** 2 +
                                     (self.mouse_y - self.center_y) ** 2)))
            self.muzzle_y = self.center_y + int(35 * (self.mouse_y - self.center_y) /
                          (sqrt((self.mouse_x - self.center_x) ** 2 +
                                     (self.mouse_y - self.center_y) ** 2)))
        except: 
            pass
        
        if self.invulnerability > 0:
            self.invulnerability -= 1        
        
            #checks if any enemies hit the player
        for e in enemies:
            if self.hitbox.colliderect(e.hitbox) and self.invulnerability == 0:
                self.health -= e.dmg
        
         #check if any enemy bullets hit the player
        for b in enemyBullets:
            if self.hitbox.colliderect(b.rect) and self.invulnerability == 0:
                self.health -= b.dmg
                
        
        
    #Draws player and player health in top-left   
    def draw(self, screen):
        #draws player
        screen.blit(self.image, (self.rect[0] + self.x, self.rect[1] + self.y, self.rect[2], self.rect[3]))
        
        #draws health
        if self.health > 0:
            draw.rect(screen, (255 * (1 - self.health // self.max_health), 255 * self.health // self.max_health, 0), (15, 15, int(500 * self.health / self.max_health), 25))  
            screen.blit(fontHealth.render("%i/%i" %(self.health, self.max_health), 1, (0, 0, 255)), (250 - fontHealth.size("%i/%i" %(self.health, self.max_health))[0] // 2, 20))
            
    #Draws debug info like hitboxes and timers
    def debug(self, firingSpeed):
        #Draws hitbox of Player
        draw.rect(screen,(255,0,0),(self.hitbox),4)
        
        #Draws bullet timer for the current gun (which has marker for when next shot is allowed)
        draw.rect(screen, (255,255,0), (self.x, self.y + self.rect[3] + 27, (time.get_ticks() - startTicks) // 10, 25))
        draw.rect(screen, (255,0,0), (self.x + firingSpeed // 10, self.y + self.rect[3] + 27, 4, 25))
        
        #draws line of fire
        draw.line(screen, (128,128,128), (self.muzzle_x, self.muzzle_y), (self.mouse_x, self.mouse_y), 2)
         
