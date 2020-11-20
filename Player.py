import pygame
from Platforms import Platforms
from pygame.locals import (K_LEFT,
                           K_RIGHT,
                           K_SPACE,
                           K_UP)

#creats and handles player interaction
class Player(pygame.sprite.Sprite):
    def __init__(self,
                 width,
                 height,
                 jump_height,
                 image,
                 background,
                 level):
        pygame.sprite.Sprite.__init__(self)
        
        #sprite handling
        self.width = width
        self.height = height
        self.px = 50
        self.py = 50
        self.image = pygame.image.load(image).convert_alpha() #loading in image 
        self.image = pygame.transform.scale(self.image, (self.px, self.py)) #scalling picture to fit
        self.surf = pygame.Surface((self.px, self.py)) #surface to put sprite onto
        self.rect = self.surf.get_rect() #rectangle used to draw sprite
        self.platforms = background
        self.startx = 50
        self.starty = 300
        self.rect.center = (self.startx, self.starty)
        self.level = level
        self.goal = False
        
        #movement variable handling
        self.jumping = False
        self.jump_offset = int(jump_height/2)
        self.jump_height = jump_height
        self.jump_half = int(jump_height/2)
        self.velocity = 0
        self.pvelocity = 0
        self.max_vel = 10
        self.grav = True
        self.floor = height
        self.worldx = self.startx
        self.checklx = -1
        self.checkrx = -1
        
    #updates for left and right movement****************************************
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        #left key handling
        if pressed_keys[K_LEFT] and self.worldx > 0 and not pressed_keys[K_RIGHT]:
            self.left(pressed_keys)
        elif not pressed_keys[K_RIGHT]:
            self.velocity = 0
            self.pvelocity = 0

        #right key handling
        if pressed_keys[K_RIGHT] and not pressed_keys[K_LEFT]:
            self.right(pressed_keys)
        elif not pressed_keys[K_LEFT]:
            self.velocity = 0
            self.pvelocity = 0 
    
    #when left key pressed
    def left(self, pressed_keys):
        if self.velocity > 0:
            self.velocity = 0
            self.pvelocity = 0
        if self.velocity > -self.max_vel:
            self.velocity -= 1  
            self.pvelocity -= 1
        if self.worldx > 0:
            if self.rect.left > 0 and self.worldx < self.width/2:
                self.rect.x += self.velocity
            elif self.pvelocity > -self.max_vel*2:
                self.pvelocity -= 1

            collisions = pygame.sprite.spritecollide(self, self.platforms, False)
            if not collisions:
                for plat in self.platforms:
                    plat.rect.x += -self.pvelocity
                if self.worldx > 0:
                    self.worldx += self.velocity
                    self.checklx += -self.pvelocity
                    self.checkrx += -self.pvelocity
            else:
                for plat in collisions:
                    self.plat_checks(plat, collisions)
                    if not self.jumping and self.rect.left < plat.rect.right and self.rect.left > plat.rect.left:
                        self.rect.x = plat.rect.right
                        for plat in self.platforms:
                            plat.rect.x -= 1
                            self.worldx -= 1
                    elif self.rect.left < plat.rect.right and self.rect.left > plat.rect.left:
                        self.rect.x = plat.rect.right - self.px
                    else:
                        self.rect.bottom = plat.rect.top
                        self.col_drop(plat, collisions)
                    self.velocity = 0
                    self.pvelocity = 0
    
    #when right key pressed
    def right(self, pressed_keys):
        if self.velocity < 0:
            self.velocity = 0
            self.pvelocity = 0
        if self.velocity < self.max_vel:
            self.velocity += 1
            self.pvelocity += 1
        #makes the character stop from going further right than middle
        if self.rect.right < self.width/2:
            self.rect.x += self.velocity
        elif self.pvelocity < self.max_vel*2:
            self.pvelocity += 1

        collisions = pygame.sprite.spritecollide(self, self.platforms, False)
        if not collisions:
            for plat in self.platforms:
                plat.rect.x += -self.pvelocity
            self.worldx += self.velocity
            self.checklx += -self.pvelocity
            self.checkrx += -self.pvelocity
        else:
            for plat in collisions:
                self.plat_checks(plat, collisions)
                if not self.jumping and self.rect.right > plat.rect.left and self.rect.right < plat.rect.right:
                    self.rect.x = plat.rect.left - self.px
                elif self.rect.right > plat.rect.left and self.rect.right < plat.rect.right:
                    self.rect.x = plat.rect.left - self.px
                else:
                    self.rect.bottom = plat.rect.top
                    self.col_drop(plat, collisions)
                self.velocity = 0
                self.pvelocity = 0
    
    #detects if the space bar was pressed under the right circumstances ****************************************
    def spaced(self):
        pressed_keys = pygame.key.get_pressed()
        if ((pressed_keys[K_SPACE] or pressed_keys[K_UP]) and
            self.jumping == False):
            self.jumping = True
            self.grav = False
    
    #handles the jumping for the character
    def jump(self):
        collisions = pygame.sprite.spritecollide(self, self.platforms, False)
        #handles the journey up on jump when no collosions
        if not collisions:
            #handles jumping
            if self.jumping and not self.grav:
                self.jumper()
            #handles the journey down on jump when no collisions
            elif self.grav:
                    self.gravity()
            #handles falling off of platforms
            if not self.grav and not self.jumping and self.rect.bottom < self.floor:
                if self.rect.left > self.checkrx or self.rect.right < self.checklx:
                    self.grav = True
                    self.jump_offset = 1
                    self.checkrx = -1
                    self.checklx = -1
        
        #hanldes collisions for the y-coordinates
        collisions = pygame.sprite.spritecollide(self, self.platforms, False)
        if collisions:
            collision = {}
            
            for plat in collisions:
                if self.jumping:
                    y = plat.rect.bottom
                    collision[y] = plat
                elif self.grav:
                    y = plat.rect.top
                    collision[y] = plat
            
            collision = list(collision.items())
            if len(collision) >= 1:
                if self.jumping:
                    collision = min(collision)[1]
                elif self.grav:
                    collision = max(collision)[1]
                    
                for plat in collisions:
                    if plat != collision:
                        collisions.remove(plat)
            
            for plat in collisions:
                #jumping collisions
                self.plat_checks(plat, collisions)
                if len(collisions) == 1:
                    if self.rect.top < plat.rect.bottom and self.jumping and not self.grav:
                        self.col_jump(plat, collisions)
                    #when player if falling down onto a platform
                    elif self.rect.bottom > plat.rect.top and self.grav:
                        self.col_drop(plat, collisions)
    
    def col_jump(self, plat, collisions):
        if self.rect.y + self.jump_offset > plat.rect.bottom:
            self.rect.y = plat.rect.bottom
            self.jumping = False
            self.grav = True
            self.jump_offset = 1
            collisions.remove(plat)
        elif self.rect.bottom + self.jump_offset > plat.rect.top and self.rect.left - self.velocity > plat.rect.right:
            self.rect.left = plat.rect.right
            self.jumping = False
            self.grav = True
            self.jump_offset = 1
            collisions.remove(plat)
        elif self.rect.bottom + self.jump_offset > plat.rect.top and self.rect.right - self.velocity < plat.rect.left:
            self.rect.right = plat.rect.left
            self.jumping = False
            self.grav = True
            self.jump_offset = 1
            collisions.remove(plat)
        else:
            self.rect.y = plat.rect.bottom
            self.jumping = False
            self.grav = True
            self.jump_offset = 1
            collisions.remove(plat)
    
    def col_drop(self, plat, collisions):
        if self.rect.bottom - self.jump_offset < plat.rect.top:
            self.rect.y = plat.rect.top - self.py
            self.jumping = False
            self.grav = False
            self.checklx = plat.rect.left
            self.checkrx = plat.rect.right
            self.jump_offset = self.jump_half
            collisions.remove(plat)
        elif self.rect.bottom - self.jump_offset < plat.rect.top and self.rect.left + self.velocity > plat.rect.right:
            if plat.rect.right - self.rect.left >= self.rect.bottom - plat.rect.top:
                self.rect.bottom = plat.rect.top
            else:
                self.rect.left = plat.rect.right
            self.jumping = False
            self.grav = False
            self.checklx = plat.rect.left
            self.checkrx = plat.rect.right
            self.jump_offset = self.jump_half
            collisions.remove(plat)
        elif self.rect.bottom - self.jump_offset < plat.rect.top and self.rect.right - self.velocity < plat.rect.left:
            if self.rect.right - plat.rect.left >= self.rect.bottom - plat.rect.top:
                self.rect.bottom = plat.rect.top
            else:
                self.rect.right = plat.rect.left
            self.rect.bottom = plat.rect.top
            self.jumping = False
            self.grav = False
            self.checklx = plat.rect.left
            self.checkrx = plat.rect.right
            self.jump_offset = self.jump_half
            collisions.remove(plat)
        else:
            self.rect.y = plat.rect.top - self.py
            self.jumping = False
            self.grav = False
            self.checklx = plat.rect.left
            self.checkrx = plat.rect.right
            self.jump_offset = self.jump_half
            collisions.remove(plat)
    
    #upwards part of jumping ****************************************
    def jumper(self):
        self.jump_offset -= (self.jump_offset - int(self.jump_offset/2))
        if self.jump_offset <= 1:
            self.grav = True
            self.jump_offset = 1
        else:
            self.rect.y += -self.jump_offset
    
    #downward part of jumping ****************************************
    def gravity(self):
        self.jump_offset += int(self.jump_offset*2)
        if self.jump_offset > self.jump_half:
            self.jump_offset = self.jump_half
        if self.rect.bottom+self.jump_offset < self.floor+self.py:
            self.rect.y += self.jump_offset
        else:
            self.grav = False
            self.jumping = False
            self.jump_offset = self.jump_half
            for plat in self.platforms: #checking if reset level by falling off world
                if plat.plat_type == "start.png":
                    self.start(plat.rect.left + self.px, plat.rect.top)
                    for plat in self.platforms:
                        self.platforms.remove(plat)
                    self.platforms = self.get_level(self.platforms, self.level, self)
                    self.jumping = False
                    self.jump_offset = self.jump_half
                    self.velocity = 0
                    self.pvelocity = 0
                    self.max_vel = 10
                    self.grav = True
                    self.worldx = self.startx
                    self.checklx = -1
                    self.checkrx = -1
    
    #*****************************************
    def plat_checks(self, plat, collisions):
        if plat.plat_type == "kill.png" and len(collisions) == 1:
            for plat2 in self.platforms:
                if plat2.plat_type == "start.png":
                    self.start(plat.rect.left + self.px, plat.rect.top)
                    for plat in self.platforms:
                        self.platforms.remove(plat)
                    self.platforms = self.get_level(self.platforms, self.level, self)
                    self.jumping = False
                    self.jump_offset = self.jump_half
                    self.velocity = 0
                    self.pvelocity = 0
                    self.max_vel = 10
                    self.grav = True
                    self.worldx = self.startx
                    self.checklx = -1
                    self.checkrx = -1
                    return
            return
        elif plat.plat_type == "goal.png" and len(collisions) == 1:
            self.goal = True
            return
            
    #cicular imports ****************************************
    def get_level(self, background, level, P1):
        with open(level) as test:
            lines = test.readlines()
            for line in lines:
                plat_type, x_size, y_size, x_coord, y_coord = line.split(" ")
                background.add(Platforms(int(plat_type),
                                        int(x_size),
                                        int(y_size),
                                        int(y_coord),
                                        int(x_coord),
                                        P1))
        return background

    #used to set the starting point for the character ****************************************
    def start(self, x, y):
        self.rect.centerx = x
        self.rect.bottom = y
    
    #draws sprite to screen ****************************************
    def draw(self, surface):
        surface.blit(self.image, self.rect)