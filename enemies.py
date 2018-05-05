class Enemy():
    #basic grunt. Slow, only does contact damage
    def __init__(self, x, y):
        #init for images and hitboxes and such
        self.image = image.load("resources/enemies/Enemy1.png").convert_alpha()
        self.original_img = image.load("resources/enemies/Enemy1.png").convert_alpha()
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.x = x
        self.y = y
        self.center_x = self.x + self.w
        self.center_y = self.y + self.h
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.hitbox_side = int(sqrt(2) * self.w / 2)
        self.hitbox = Rect(self.center_x - self.hitbox_side, self.center_y - self.hitbox_side, self.hitbox_side, self.hitbox_side)        
        
        #init for default enemy properties (changed in each sub-class)
        self.speed = 5
        self.life_span = 120000
        self.age = 0
        self.health = 100
        self.dmg = 10
        self.health_drop_chance = random.random()
        
    def update(self, tox, toy, enemies): 
        #updates target x and y
        self.tox = tox - self.w // 2
        self.toy = toy - self.h // 2 
        
        #checks if colliding with any other enemies other than itself. if so, moves in opposite direction by the speed value
        for e in enemies:
            if self.hitbox.colliderect(e.hitbox) and e != self:
                try:
                    self.x -= int(self.speed * (e.x - self.x) / hypot(e.x - self.x, e.y - self.y) )
                    self.y -= int(self.speed * (e.y - self.y) / hypot(e.x - self.x, e.y - self.y) )
                except: pass #catches divide by 0 errors
                
        #moves towards player
        try:
            self.x += int(self.speed * (self.tox - self.x) / hypot(self.tox - self.x, self.toy - self.y) )
            self.y += int(self.speed * (self.toy - self.y) / hypot(self.tox - self.x, self.toy - self.y) )
        except: pass #catches divide by 0 errors
        
        #updates hitboxes and such
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.center_x = self.x + self.w // 2
        self.center_y = self.y + self.h // 2      
        self.hitbox = Rect(self.center_x - self.hitbox_side // 2, self.center_y - self.hitbox_side // 2, self.hitbox_side, self.hitbox_side)        
        
        #updates age
        self.age += 1
        
        
    
    def check(self, bullets, pickups):  
        #checks if any player bullets hit, if so, deletes some hp
        for b in bullets:
            self.image = self.original_img
            if self.hitbox.colliderect(b.rect):
                self.image = image.load("resources/enemies/EnemyHit.png").convert_alpha()
                self.health -= (b.dmg + pl.dmg_upG) * pl.dmg_mult * b.dmg_mult
        self.image = self.original_img
        
        #checks if enemy should die, if so, kills self and drops heart if it can (15% chance) 
        if self.age >= self.life_span:
            enemies.remove(self)
            
        if self.health <= 0:
            enemies.remove(self)
            if self.health_drop_chance <= .15:
                pickups.append(Heart(self.x, self.y, 200))
    
    #function for drawing the enemy
    def draw(self):
        screen.blit(self.image, self.rect)
        
    #debug draw for enemy hitboxes, and enemy health
    def debug(self, tox, toy):
        draw.rect(screen, (0,0,0), enemy.hitbox, 4) 
        draw.rect(screen, (0,0,255), (enemy.x, enemy.y + enemy.h, int(enemy.health), 25))       
        
        #draws a line between self and target
        draw.line(screen, (128,128,128), (self.center_x, self.center_y), (tox, toy), 2)    
             
   
class Shooter(Enemy):
    #super slow, shoots bullets at slow orig_imgs
    def __init__(self, x, y):
        Enemy.__init__(self, x, y)
        self.image = image.load("resources/enemies/Enemy2.png").convert_alpha()
        self.original_img = image.load("resources/enemies/Enemy2.png").convert_alpha()
        self.speed = 2
        self.life_span = 120000
        self.age = 0
        self.health = 125
        self.dmg = 10
        
        self.firing_speed = 50
        self.fire_time = self.firing_speed // 5 * random.randint(0, 5)   
class Wolf(Enemy):
    # very fast, does a lot of contact damage but has little health
    def __init__(self, x, y):
        Enemy.__init__(self, x, y)
        self.image = image.load("resources/enemies/Enemy3.png").convert_alpha()
        self.original_img = image.load("resources/enemies/Enemy3.png").convert_alpha()
        self.speed = 10
        self.life_span = 120000
        self.health = 50
        self.dmg = 20
        
class Turret(Enemy):
    # super slow, stops if gets too close to player, shoots in cardinal/diagonal directions
    def __init__(self, x, y):
        Enemy.__init__(self, x, y)
        self.image = image.load("resources/enemies/Enemy4.png").convert_alpha()
        self.original_img = image.load("resources/enemies/Enemy4.png").convert_alpha()
        self.speed = 2
        self.life_span = 120000
        self.health = 200
        self.dmg = 20  
        
        self.firing_speed = 35
        self.fire_time = self.firing_speed // 5 * random.randint(0, 5)     
        self.gun_state = 0
        self.angles_1 = [0, 90, 180, 270]
        self.angles_2 = [45, 135, 225, 315]
        self.TurretTarget = (0,0)
    
    #stops turret from moving if too close
    def update(self, tox, toy, enemies):
        if hypot((self.x - tox), (self.y - toy)) > 400:
            Enemy.update(self, tox, toy, enemies)

