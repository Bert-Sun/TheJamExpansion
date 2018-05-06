from pygame import *
from enemies import *
import random
init()

class Cap():
    def __init__(self):
        #initialize the image and pos of cap:
        self.img = image.load('resources/jam/boss/cap.png')
        self.x = 0
        self.y = -150
        self.rect = Rect(self.x, self.y, 722, 149)
        
        #initialize the cap properties:
        self.max_health = 4800
        self.health = self.max_health
        self.vulnerable = True
        
        #check Boss phase, if Boss.phase != 1, kill the Cap sprite
        if Boss.phase != 1:
            self.health = 0
            
    def check(self):
        for b in bullets:
            if b.rect.colliderrect(self.rect):
                self.health -= b.dmg
                
        #check if it is supposed to die, if dead start boss phase 2:
        if self.health <= 0:
            Boss.phase = 2

class Boss():
    
    def __init__(self):
        #initialize the image and pos:
        self.orig_imgs = [image.load('resources/jam/boss/capped.png').convert_alpha(), image.load('resources/jam/boss/uncapped.png').convert_alpha()]
        self.x = 100
        self.y = 50
        self.rect = Rect(self.x, self.y, 955, 909)
        
        #initialize boss properties
        self.phase = 0
        self.max_health = 12000
        self.health = self.max_health
        self.vulnerable = True
        
    #draws itself and its health
    def draw(self, screen):
        screen.blit(self.orig_imgs[1], (self.x, self.y))
        self.rect = Rect(self.x, self.y, 955, 909)
        
        
    def check(self):
        for b in bullets:
            if b.rect.colliderect(self.rect):
                self.health -= b.dmg
            
        #check if it is supposed to die
        if self.health <= 0:
            global bossFight
            bossFight = False
            global level
            level = 6
            self.health = self.max_health
        #check for phase change
        elif self.health < 8000:
            self.phase = 2
        elif self.health < 4000:
            self.phase = 3