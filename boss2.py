from pygame import *
from enemies import *
import random
init()

fontGeneral = font.Font('resources/fonts/Calibri.ttf', 30)
fontHealth = font.Font('resources/fonts/Calibri Bold.ttf', 15)

class Cap():
    def __init__(self):
        #initialize the image and pos of cap:
        self.img = image.load('resources/jam/boss/cap.png')
        self.x = 0
        self.y = -150
        self.rect = Rect(self.x, self.y, 722, 149)
        
    def draw(self, screen):
        screen.blit(self.image[self.phase], self.Rect())
        self.rect = Rect(self.x, self.y, self.image[1].get_width(), self.image[1].get_height())    
        
            
    def check(self):
        for b in bullets:
            if b.rect.colliderrect(self.rect):
                self.health -= b.dmg
                
        #check if it is supposed to die, if dead start boss phase 2:
        

class Boss():
    
    def __init__(self):
        #initialize the image and pos:
        self.image = image.load('resources/jam/boss/uncapped.png').convert_alpha()
        self.w = self.image.get_width() // 5
        self.h = self.image.get_width() // 5
        self.x = 300
        self.y = 25
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.image = transform.scale(self.image, (self.w, self.h))
        
        
        self.gun3 = (self.rect.bottomleft[0]+10, self.rect.bottomleft[1]-10)  
        self.gun2 = (self.rect.bottomright[0]+10, self.rect.bottomright[1]-10)
        self.gun1 = (self.rect.bottomright[0] + self.w // 2, self.rect.bottomright[1]-10)
        self.guns = [self.gun1, self.gun2]
        self.firing_speed = [25, 20, 15]
        self.firing_time = 0
        #grace time is reset if grace time is reached
        self.grace_timers = [120, 90, 65]
        self.grace_time = 180        
        
        
        #initialize boss properties
        self.phase = 0
        self.max_health = 12000
        self.health = self.max_health
        self.vulnerable = True
        self.attacks = [False, False]
        self.directions = 0
        #counter of how much boss moved
        self.frames_spent_moving = 0        
    
    #draws itself and its health
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        draw.rect(screen, (255, 0, 255), (15, 700 - 85, int(985 * self.health / self.max_health), 75))
        screen.blit(fontGeneral.render("Boss health: %i/%i" %(self.health, self.max_health), 1, (0, 255, 0)), (467 - fontHealth.size("Boss health: %i/%i" %(self.health, self.max_health))[0] // 2, 700 - 55 - fontHealth.size("Boss health: %i/%i" %(self.health, self.max_health))[1] // 2))
        
    def update(self, pl, eb):
        if self.grace_time == 0:
            #handles attack timings with some randomness
            self.attacks[random.randint(0,1)] = True
            self.directions = random.randint(0,3)         
            
            #resets movement during attacks
            self.frames_spent_moving = 0
            
            #handles in between attack grace timers
            self.grace_time = self.grace_timers[self.phase]
            
        else: 
            #handles movement between attacks
            if self.frames_spent_moving <= 30:
                self.move()
                self.frames_spent_moving += 1
            self.grace_time -= 1
        
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.gun3 = (self.rect.bottomleft[0]+10, self.rect.bottomleft[1]-10)  
        self.gun2 = (self.rect.bottomright[0]+10, self.rect.bottomright[1]-10)
        self.gun1 = (self.rect.bottomright[0] - self.w // 2, self.rect.bottomright[1]-10)
        self.guns = [self.gun1, self.gun2]          
        
        #tries to fire each attack
        self.sweeper(eb)
        self.ring(eb)
    
    def check(self, bullets, pickups, pl):
        for b in bullets:
            if b.rect.colliderect(self.rect):
                self.health -= b.dmg + pl.dmg_upG
        
        #if health permits, spawns a randomly placed heart 
        if 0 <= self.health%500 <= 10 and self.health != self.max_health:
            pickups.append(Heart(random.randint(300, 700), random.randint(200, 500), random.randint(250, 500)))        
        
        if 0 <= self.health%250 <= 10 and self.health != self.max_health:
            self.weakpoint = random.randint(0, 4)
            self.health -= 11
        
          
        # checks if it is supposed to die
        if self.health <= 0:
            self.health = self.max_health
            return False
        #check for phase change
        elif self.health < 8000:
            self.phase = 2
        elif self.health < 4000:
            self.phase = 3
            
        return True 
    
    
    def move(self):
        #very similar to pl.directions, moves if it can
        if self.directions == 0:
            if self.y < 100:
                self.y += 3
                print("move 1")
        elif self.directions == 1:
            if 0 < self.y:
                self.y -= 3
                print("move 2")
        elif self.directions == 2:
            if 0 < self.x:
                self.x -= 10
                print("move 3")
        elif self.directions == 3:
            if self.x + 800 < 1000:
                self.x += 10
                print("move 4")
                
    def sweeper(self, enemyBullets):
        #shoots stream of bullets from left to right from random guns
        if self.attacks[1]:
            for angle in range(10, 170, 5):
                #checks if timer conditions are just right
                if self.firing_time + 10 == angle:
                    self.target_angle = (self.gun2[0] + 50 * cos(radians(angle)), 
                                              self.gun2[1] + 50 * sin(radians(angle)))            
                    enemyBullets.append(JamBullet(self.gun2[0], self.gun2[1], self.target_angle[0], self.target_angle[1], 15 * (self.phase + 1)))
                    
                    self.target_angle = (self.gun3[0] + 50 * cos(radians(180 - angle)), 
                                                         self.gun3[1] + 50 * sin(radians(180 -angle)))            
                    enemyBullets.append(JamBullet(self.gun3[0], self.gun3[1], self.target_angle[0], self.target_angle[1], 15 * (self.phase + 1)))                    
                
                #ends attack
                if self.firing_time + 10 >= 170:
                    self.attacks[1] = False
                    self.firing_time = 0
                    break
            else: self.firing_time += 2
    
    def ring(self, enemyBullets):
        if self.attacks[0]:
            for angle in range(0, 360, 10):
                if self.firing_time == angle:
                    self.target_angle = (self.rect.centerx + 50 * cos(radians(angle)), 
                                                         self.rect.centery + 50 * sin(radians(angle)))            
                    enemyBullets.append(JamBullet(self.rect.centerx, self.rect.centery, self.target_angle[0], self.target_angle[1], 15 * self.phase))
                
                if self.firing_time >= 360:
                    self.attacks[0] = False
                    self.firing_time = 0
                    break
            else: self.firing_time += 2.5                
    
        
        
        
    
        