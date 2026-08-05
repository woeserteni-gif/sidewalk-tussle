import pygame 
import sys 
from pygame.locals import * 

# 1. Initialize pygame and the mixer FIRST before loading sounds
pygame.init()
pygame.mixer.init()

vec = pygame.math.Vector2 

# main values
ACC = 0.8  # Lowered from 5 to prevent uncontrollable speeds with friction
FRIC = -0.15 # Adjusted friction for smoother, controllable movement
GRAV = 0.5 
FPS = 60 
SCREEN_WIDTH = 1000 
SCREEN_HEIGHT = 600 

# 2. Load Sound objects after initialization
# Note: Ensure these file paths are correct on your local machine
try:
    game_music = pygame.mixer.Sound("/Users/tenzinwoeser/Documents/Python for engineers class/GUILE'S THEME.mp3") 
    jump_music = pygame.mixer.Sound("arcade retro jump - Sound Effect HD (No Copyright Sound).mp3") 
    game_music.play(loops=-1)
except pygame.error:
    print("Sound files not found, playing without sound.")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

# Load the background image 
try:
    bg_image = pygame.image.load("/Users/tenzinwoeser/Documents/Python for engineers class/UserstenzinwoeserDocumentsPython for engineers classdownload.png.png").convert_alpha() 
except pygame.error:
    # Fallback surface if image path fails
    bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image.fill((30, 30, 30))

class Fighter(pygame.sprite.Sprite): 
    def __init__(self, x, y, color): 
        super().__init__() 
        self.rect = pygame.Rect(x, y, 100, 160) 
        self.color = color 
        self.vel = vec(0,0) 
        self.acc = vec(0,0) 
        self.pos = vec(x, y) # Set position to designated spawn arguments
        
    def draw(self, surface): 
        pygame.draw.rect(surface, self.color, self.rect) 
        
    def move(self, opponent): 
        self.acc = vec(0, GRAV) 
        pressed_keys = pygame.key.get_pressed() 
        if pressed_keys[K_a]: 
            self.acc.x = -ACC 
        if pressed_keys[K_d]: 
            self.acc.x = ACC 
            
        # Physics calculations
        self.acc.x += self.vel.x * FRIC 
        self.vel += self.acc 
        
        # --- Horizontal Movement & Collision ---
        self.pos.x += self.vel.x + 0.5 * self.acc.x
        
        # Screen boundaries horizontal
        if self.pos.x > SCREEN_WIDTH - (self.rect.width / 2): 
            self.pos.x = SCREEN_WIDTH - (self.rect.width / 2)
        if self.pos.x < (self.rect.width / 2): 
            self.pos.x = (self.rect.width / 2) 
            
        self.rect.midbottom = self.pos 
        
        # Push away from opponent if intersecting horizontally
        if self.rect.colliderect(opponent.rect):
            if self.vel.x > 0: # Moving right
                self.rect.right = opponent.rect.left
                self.pos.x = self.rect.centerx
                self.vel.x = 0
            elif self.vel.x < 0: # Moving left
                self.rect.left = opponent.rect.right
                self.pos.x = self.rect.centerx
                self.vel.x = 0

        # --- Vertical Movement ---
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.midbottom = self.pos
        
        if pressed_keys[K_w]: # Jumping 
            if self.jump(): 
                try: jump_music.play(loops = 0) 
                except: pass
            
    def move_fighter2(self, opponent): 
        self.acc = vec(0, GRAV) 
        pressed_keys = pygame.key.get_pressed() 
        if pressed_keys[K_LEFT]: 
            self.acc.x = -ACC 
        if pressed_keys[K_RIGHT]: 
            self.acc.x = ACC 
            
        # Physics calculations
        self.acc.x += self.vel.x * FRIC 
        self.vel += self.acc 
        
        # --- Horizontal Movement & Collision ---
        self.pos.x += self.vel.x + 0.5 * self.acc.x
        
        # Screen boundaries horizontal
        if self.pos.x > SCREEN_WIDTH - (self.rect.width / 2): 
            self.pos.x = SCREEN_WIDTH - (self.rect.width / 2)
        if self.pos.x < (self.rect.width / 2): 
            self.pos.x = (self.rect.width / 2) 
            
        self.rect.midbottom = self.pos 
        
        # Push away from opponent if intersecting horizontally
        if self.rect.colliderect(opponent.rect):
            if self.vel.x > 0: # Moving right
                self.rect.right = opponent.rect.left
                self.pos.x = self.rect.centerx
                self.vel.x = 0
            elif self.vel.x < 0: # Moving left
                self.rect.left = opponent.rect.right
                self.pos.x = self.rect.centerx
                self.vel.x = 0

        # --- Vertical Movement ---
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.midbottom = self.pos
        
        if pressed_keys[K_UP]: # Jumping 
            if self.jump(): 
                try: jump_music.play(loops=0) 
                except: pass
            
    def update(self): 
        hit = pygame.sprite.spritecollide(self, platforms, False) 
        if self.vel.y > 0: 
            if hit: 
                self.vel.y = 0 
                self.pos.y = hit[0].rect.top + 1 
                self.rect.midbottom = self.pos
                
    def jump(self): 
        hits = pygame.sprite.spritecollide(self, platforms, False) 
        if hits: 
            self.vel.y = -14 
            return True
        return False

class Platform(pygame.sprite.Sprite): 
    def __init__(self): 
        super().__init__() 
        self.surf = pygame.Surface((SCREEN_WIDTH, 40)) # Increased height from 2 to 40 for visual grounding
        
        self.surf.set_alpha(0) # Makes the surface transparent
        self.rect = self.surf.get_rect() 
        self.rect.topleft = (0, SCREEN_HEIGHT - 40) 

# Spawn setups
fighter_1 = Fighter(150, 500, (255, 0, 0)) # Red fighter
fighter_2 = Fighter(850, 500, (0, 0, 255)) # Blue fighter

platforms = pygame.sprite.Group() 
main_surf = Platform() 
platforms.add(main_surf)

# Game clock to control frame rate
clock = pygame.time.Clock()

run = True 
while run: 
    clock.tick(FPS)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False 

    # 1. Clear screen with background image
    screen.blit(bg_image, (0, 0)) 

    # 2. Update and resolve positions (pass opponent object into move functions)
    fighter_1.move(fighter_2)
    fighter_2.move_fighter2(fighter_1)
    
    fighter_1.update()
    fighter_2.update()
    
    # 3. Draw frames (The manually drawn floor rectangle has been removed)
    fighter_1.draw(screen)
    fighter_2.draw(screen) 

    pygame.display.update() 

pygame.quit() 
sys.exit()
