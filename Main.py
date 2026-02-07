import pygame
import sys
import Game
import Animal

# Initialisering
pygame.init()

# INNER PLAYABLE area
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

# OUTER FRAME
FRAME_WIDTH = 1080
FRAME_HEIGHT = 700

screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
window = pygame.display.set_mode((FRAME_WIDTH, FRAME_HEIGHT))
clock = pygame.time.Clock()

pixel_font = pygame.font.Font("Fonts/PixelifySans-Medium.ttf", 40)
pixel_font_thin = pygame.font.Font("Fonts/PixelifySans-Regular.ttf", 30)

GAME_X = (FRAME_WIDTH - SCREEN_WIDTH) // 2
GAME_Y = (FRAME_HEIGHT - SCREEN_HEIGHT) // 2

# Farger
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        self.background = pygame.image.load("Assets/lysrosa.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.animals = pygame.sprite.Group()
        self.current_level = 1 # Startfrukt
        self.active_game = False

        # En liste med filnavnene dine i rekkefølge (0 er minste frukt)
        self.animal_images = [
            "Assets\9hqZid.png",   # Level 0, denne vil bli ignorert pga listelogikk
            "Assets/fotb.png",  # Level 1
            "Assets/9hqZid.png",     # Level 2
            "Assets/fotb.png",  # Level 3
            "Assets/9hqZid.png",      # Level 4 osv..
            "Assets/9hqZid.png",   
            "Assets/fotb.png",  
            "Assets/9hqZid.png",     
            "Assets/fotb.png",  
            "Assets/9hqZid.png",
            "Assets/fotb.png",  
            "Assets/volleyb.png",        
        ]
        
    def spawn_animals(self, x):
        # Vi henter riktig bilde-sti basert på current_level
        image_path = self.animal_images[self.current_level]
        new_animal= Animal.Animal(x, 50, self.current_level, image_path)
        self.animals.add(new_animal)

    def handle_collisions(self):
            animals_list = self.animals.sprites()
            
            for i in range(len(animals_list)):
                for j in range(i + 1, len(animals_list)):
                    # Sjekk om fruktene fortsatt eksisterer (viktig ved merging!)
                    if i >= len(animals_list) or j >= len(animals_list): continue
                    
                    f1 = animals_list[i]
                    f2 = animals_list[j]

                    dx = f1.rect.centerx - f2.rect.centerx
                    dy = f1.rect.centery - f2.rect.centery
                    distance = (dx**2 + dy**2)**0.5
                    min_dist = f1.radius + f2.radius

                    if distance < min_dist:
                        # --- HER STARTER MERGING-LOGIKKEN (Punkt 3) ---
                        if f1.level == f2.level:
                            new_level = f1.level + 1
                            
                            # Sjekk at vi faktisk har et bilde for neste nivå
                            if new_level < len(self.animal_images):
                                new_x = (f1.rect.centerx + f2.rect.centerx) / 2
                                new_y = (f1.rect.centery + f2.rect.centery) / 2
                                
                                # Fjern de gamle ballene
                                f1.kill()
                                f2.kill()
                                
                                # Lag den nye ballen med bilde fra listen
                                new_path = self.animal_images[new_level]
                                new_animal = Animal.Animal(new_x, new_y, new_level, new_path)
                                self.animals.add(new_animal)
                                
                                # Vi må gå ut av funksjonen her fordi lista har endret seg
                                return 
                        # --- HER SLUTTER MERGING-LOGIKKEN ---

                        # Logikk for stabling/dytting (hvis de ikke merget)
                        overlap = min_dist - distance
                        if distance == 0: distance = 1 # Unngå krash
                        nx = dx / distance
                        ny = dy / distance

                        f1.rect.x += nx * (overlap / 2)
                        f1.rect.y += ny * (overlap / 2)
                        f2.rect.x -= nx * (overlap / 2)
                        f2.rect.y -= ny * (overlap / 2)
                    
    def game_over_screen(self):
        screen.fill("#7bceea")
        game_over_surface = pixel_font.render("Game Over", False, (12, 81, 105))
        game_over_rectangle = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(game_over_surface, game_over_rectangle)
        
        game_over_description_surface = pixel_font_thin.render("Press 'spacebar' to replay", False, (12, 81, 105))
        game_over_description_rectangle = game_over_surface.get_rect(center=(SCREEN_WIDTH // 3.25, 300))
        screen.blit(game_over_description_surface, game_over_description_rectangle)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.active_game:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()

                        # Check if click is inside game screen
                        if GAME_X <= mx <= GAME_X + SCREEN_WIDTH:
                            local_x = mx - GAME_X
                            self.spawn_animals(local_x)
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.active_game = True

            # GAMEPLAY
            if self.active_game:
                # 1. Oppdater posisjoner
                self.animals.update()
                
                # 2. Sjekk kollisjoner og merging
                self.handle_collisions()

                # 3. Tegn alt på nytt
                screen.blit(self.background, (0, 0))
                window.fill((30, 30, 30))
                screen.fill((255, 255, 255))
                screen.blit(self.background, (0, 0))
                self.animals.draw(screen)
                window.blit(screen, (GAME_X, GAME_Y))
                
                pygame.display.update()
                clock.tick(60)
            
            # GAME OVER SCREEN
            else:
                self.game_over_screen()
                
                window.fill((30, 30, 30)) 
                window.blit(screen, (GAME_X, GAME_Y)) 
                
                pygame.display.update() 
                clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()