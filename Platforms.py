import pygame

#Creates a platform based on the platform type, and size.
class Platforms(pygame.sprite.Sprite):
    def __init__(self,
                 plat_type,
                 x_size,
                 y_size,
                 x_coord,
                 y_coord,
                 player):
        pygame.sprite.Sprite.__init__(self) #initialize sprite class
        #setting coordinates of the current platform
        self.x = x_coord
        self.y = y_coord
        self.x_size = x_size
        self.y_size = y_size
        
        self.surf = pygame.Surface((x_size, y_size))
        self.rect = self.surf.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.top = self.rect.top
        self.player = player
        self.plat = plat_type
        
        #setting file path for platforms
        self.file_path = "./images/Platforms/"
        
        #creating the sprite for the platform
        #probably should change how this is done
        self.platforms = ["start.png",
                          "floating.png",
                          "goal.png",
                          "spiked.png",
                          "kill.png"]
        self.plat_type = self.platforms[plat_type]
        self.image = pygame.image.load(self.file_path + self.plat_type).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.x_size, self.y_size))
        
        #getting current background and player
        
        if plat_type == 0:
            self.player.start(self.rect.left + self.player.px, self.rect.top - self.player.py)
    
    #platform where you start
    def start_platform(self):
        self.player.start(self.rect.left + self.player.px, self.rect.top - self.player.py)
