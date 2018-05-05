class Boss():
    
    def __init__(self):
        #image and position
        self.orig_imgs = [image.load('resources/boss.png').convert_alpha(), image.load('resources/boss2.png').convert_alpha(), image.load('resources/boss3.png').convert_alpha()]
        self.x = 100
        self.y = 50
        self.rect = Rect(self.x, self.y, 800, 100)

        #boss properties init
        self.phase = 0
        self.max_health = 12000
        self.health = self.max_health
        self.vulnerable = True
        ##timers for attack balancing
        self.pause_timer = 120
        #firing time is reset if firing speed is reached
        self.firing_speed = [25, 20, 15]
        self.firing_time = 0
        #grace time is reset if grace time is reached
        self.grace_timers = [120, 90, 65]
        self.grace_time = 180
        #attacks init (similar to pl.directions)
        self.attacks = [False, False, False, False]
        self.directions = 0
        #counter of how much boss moved
        self.frames_spent_moving = 0

        ##vars for gun positions and angles for attack patterns
        self.gun_pos = [(75, 100), (235, 75), (395, 100), (555, 75), (715, 100)]
        self.weakpoint = 2
        self.weakpoint_rect = (self.gun_pos[self.weakpoint][0] + self.x, self.gun_pos[self.weakpoint][1] + self.y , 53, 53)
        self.gun_queue = random.sample(self.gun_pos, len(self.gun_pos))
        #chosen angle and chosen gun 
        self.target_angle = 0
        self.target_gun = (75, 100)
        #angles to shoot at 
        self.angles_double = [85, 95]
        self.angles_triple = [45, 90, 135]
        self.angles_quad = [18, 36, 54, 72]
        self.angles_quint = [15, 30, 45, 60, 75]
        
    def move(self):
        #very similar to pl.directions, moves if it can
        if self.directions == 0:
            if self.y < 100:
                self.y += 3
        elif self.directions == 1:
            if 0 < self.y:
                self.y -= 3
        elif self.directions == 2:
            if 0 < self.x:
                self.x -= 3
        elif self.directions == 3:
            if self.x + 800 < WIDTH:
                self.x += 3   
    
    
    #attack coreography
    def attack1(self):  
        #shoots 5 pellet spread from random gun
        if self.attacks[0]:
            self.target_gun = self.gun_pos[random.randint(0,4)]
            for angle in self.angles_quad:
                #finds point on circle based on angle and radius, fires enemyBullet there
                self.target_angle = (self.target_gun[0]+self.x + 50 * cos(radians(angle + 45)), 
                                          self.target_gun[1]+self.y + 50 * sin(radians(angle + 45)))            
                enemyBullets.append(EnemyBullet(self.target_gun[0]+self.x, self.target_gun[1]+self.y, self.target_angle[0], self.target_angle[1], 15 * self.phase))
            #ends attack
            self.attacks[0] = False
    
    def attack2(self):
        # shoots triple shots in random gun pattern
        if self.attacks[1]:
            for i in range(len(self.gun_queue)):
                #checks if timer conditions are just right
                if self.firing_time == self.firing_speed[self.phase] * i:
                    #sets target gun based on random queue
                    self.target_gun = self.gun_queue[i]
                    for angle in self.angles_triple:
                        #finds point on circle based on angle and radius, fires enemyBullet there
                        self.target_angle = (self.target_gun[0]+self.x + 50 * cos(radians(angle)), 
                                                  self.target_gun[1]+self.y + 50 * sin(radians(angle)))            
                        enemyBullets.append(EnemyBullet(self.target_gun[0]+self.x, self.target_gun[1]+self.y, self.target_angle[0], self.target_angle[1], 15 * self.phase))
                #ends attack
                if self.firing_time == self.firing_speed[self.phase] * len(self.gun_queue):
                    self.attacks[1] = False
                    self.firing_time = 0 
                    break
            else:
                self.firing_time += 1
            
    def attack3(self):
        #shoots stream of bullets from left to right from random guns
        if self.attacks[2]:
            for angle in range(60, 120, -self.phase + 3):
                #checks if timer conditions are just right
                if self.firing_time + 60 == angle:
                    for i in range(2):
                        #chooses random gun (twice)
                        self.target_gun = self.gun_queue[i]
                        #finds point on circle based on angle and radius, fires enemyBullet there
                        self.target_angle = (self.target_gun[0]+self.x + 50 * cos(radians(angle)), 
                                                  self.target_gun[1]+self.y + 50 * sin(radians(angle)))            
                        enemyBullets.append(EnemyBullet(self.target_gun[0]+self.x, self.target_gun[1]+self.y, self.target_angle[0], self.target_angle[1], 15 * self.phase))
                #ends attack
                if self.firing_time + 60 >= 120:
                    self.attacks[2] = False
                    self.firing_time = 0
                    break
            else: self.firing_time += 1
            
    def attack4(self):
        #shoots stream of bullets from left to right
        if self.attacks[3]:
            for angle in range(120, 60, -(-self.phase + 3)):
                #checks if timer conditions are just right
                if self.firing_time + 60 == angle:
                    for i in range(2):
                        #chooses random gun (twice)
                        self.target_gun = self.gun_queue[i]
                        #finds point on circle based on angle and radius, fires enemyBullet there
                        self.target_angle = (self.target_gun[0]+self.x + 50 * cos(radians(180 - angle)), 
                                                  self.target_gun[1]+self.y + 50 * sin(radians(180 -angle)))            
                        enemyBullets.append(EnemyBullet(self.target_gun[0]+self.x, self.target_gun[1]+self.y, self.target_angle[0], self.target_angle[1], 15 * self.phase))
                #ends attack
                if self.firing_time + 60 >= 120:
                    self.attacks[3] = False
                    self.firing_time = 0
                    break
            else: self.firing_time += 1        
    
    #if player is out of range, shoots beam straight at player (to encourage player to stay within borderlines)
    def outOfRangeAttack(self):
        if pl.center_x < self.x - 100:
            enemyBullets.append(EnemyBullet(self.gun_pos[0][0]+self.x, self.gun_pos[0][1]+self.y, pl.center_x, pl.center_y, 15 * self.phase))
        elif pl.center_x > self.x + 800 + 100:
            enemyBullets.append(EnemyBullet(self.gun_pos[4][0]+self.x, self.gun_pos[4][1]+self.y, pl.center_x, pl.center_y, 15 * self.phase))
    
    #draws itself and it's health
    def draw(self):
        screen.blit(self.orig_imgs[self.phase], (self.x, self.y))
        self.rect = Rect(self.x, self.y, 800, 100)
        draw.circle(screen, RED, (self.gun_pos[self.weakpoint][0] +self.x, self.gun_pos[self.weakpoint][1] +self.y), 53)
        draw.rect(screen, (255, 255,0), (15, HEIGHT - 85, int(985 * self.health / self.max_health), 75))
        screen.blit(fontGeneral.render("Boss health: %i/%i" %(self.health, self.max_health), 1, (0, 0, 255)), (467 - fontHealth.size("Boss health: %i/%i" %(self.health, self.max_health))[0] // 2, HEIGHT - 55 - fontHealth.size("Boss health: %i/%i" %(self.health, self.max_health))[1] // 2))
    
    
    def update(self):
        if self.grace_time == 0:
            #handles attack timings with some randomness
            self.attacks[random.randint(0,3)] = True
            self.gun_queue = random.sample(self.gun_pos, len(self.gun_pos))
            self.directions = random.randint(0,3)
            
            #resets movement during attacks
            self.frames_spent_moving = 0
            
            #handles in between attack grace timers
            if self.attacks[0] == True: 
                self.grace_time = self.grace_timers[self.phase] // 8
            else: self.grace_time = self.grace_timers[self.phase]
        else: 
            #handles movement between attacks
            if self.frames_spent_moving <= 30:
                self.move()
                self.frames_spent_moving += 1
            self.grace_time -= 1
        
        #updates weakpoint
        self.weakpoint_rect = (self.gun_pos[self.weakpoint][0] + self.x - 53, self.gun_pos[self.weakpoint][1] + self.y - 53 , 106, 106)
        
        #tries to fire each attack
        self.attack1() # random quad shot
        self.attack2() # random sequence of triple shots
        self.attack3() #chooses 2 random guns to fire from, goes from left to right
        self.attack4() #chooses 2 random guns to fire from, goes from right to left
        self.outOfRangeAttack() #shoots player if player is out of range
    
    #checks itself for health, changes phases after certain point
    def check(self):
        for b in bullets:
            if b.rect.colliderect(self.weakpoint_rect):
                self.health -= b.dmg 
        
        #if health permits, spawns a randomly placed heart 
        if 0 <= self.health%500 <= 10 and self.health != self.max_health:
            pickups.append(Heart(random.randint(300, 700), random.randint(200, 500), random.randint(250, 500)))        
        
        if 0 <= self.health%250 <= 10 and self.health != self.max_health:
            self.weakpoint = random.randint(0, 4)
            self.health -= 11
        
        
        
        # checks if it is supposed to die
        if self.health <= 0:
            global bossFight
            bossFight = False
            global level
            level = 6
            self.health = self.max_health
        #changes phases
        elif self.health <= self.max_health // 3:
            self.phase = 2        
        elif self.health <= self.max_health // 3 * 2:
            self.phase = 1
        
        
