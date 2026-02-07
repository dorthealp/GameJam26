import pygame
import sys
import Animal
from Scoreboard import Scoreboard

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

pixel_font = pygame.font.Font("Fonts/SedgwickAve-Regular.ttf", 40)
pixel_font_thin = pygame.font.Font("Fonts/Pangolin-Regular.ttf", 30)

GAME_X = (FRAME_WIDTH - SCREEN_WIDTH) // 2
GAME_Y = (FRAME_HEIGHT - SCREEN_HEIGHT) // 2
#Border
TOP_BORDER_Y = 80

# Farger
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        self.background = pygame.image.load("Assets/lysrosa.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.animals = pygame.sprite.Group()
        self.current_level = 1 # Startfrukt
        self.active_game = False

        #scoreboard
        self.scoreboard = Scoreboard(GAME_X + SCREEN_WIDTH + 50, GAME_Y + 100)

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
                    # Sjekk om dyrene fortsatt eksisterer (viktig ved merging!)
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

                            # Bruker det nye nivået for å bestemme poengsummen
                            self.scoreboard.add_score_by_level(new_level)
                            
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
                        if distance == 0: distance = 1 # Unngå crash
                        nx = dx / distance
                        ny = dy / distance

                        f1.rect.x += nx * (overlap / 2)
                        f1.rect.y += ny * (overlap / 2)
                        f2.rect.x -= nx * (overlap / 2)
                        f2.rect.y -= ny * (overlap / 2)

    def reset_game(self):
        self.animals.empty()
        self.current_level = 1
        self.active_game = True               

    def check_game_over(self):
        for animal in self.animals:
            if animal.rect.top > TOP_BORDER_Y:
                animal.entered_game = True

            if (
                animal.entered_game 
                and animal.prev_top > TOP_BORDER_Y
                and animal.rect.top <= TOP_BORDER_Y
                ):
                self.active_game = False
                return
    

    def game_over_screen(self):
        screen.fill((254, 172, 90))

        game_over_surface = pixel_font.render("Game Over", False, (156, 27, 32))
        game_over_rectangle = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(game_over_surface, game_over_rectangle)
        
        game_over_description_surface = pixel_font_thin.render("Press 'spacebar' to replay", False, (156, 27, 32))
        game_over_description_rectangle = game_over_description_surface.get_rect(center=(SCREEN_WIDTH // 2, 300))
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
                        self.reset_game()

            # GAMEPLAY
            if self.active_game:
                # 1. Oppdater posisjoner
                self.animals.update()
                
                # 2. Sjekk kollisjoner og merging
                self.handle_collisions()

                #3. check game over
                self.check_game_over()

                # 4. Tegn alt på nytt
                window.fill((194, 39, 45))
                screen.fill((254, 172, 90))
                #screen.blit(self.background, (0, 0))
                self.animals.draw(screen)
                window.blit(screen, (GAME_X, GAME_Y))
                self.scoreboard.draw(window)
                
                #line
                pulse = abs((pygame.time.get_ticks() % 1000) - 500) // 4
                color = (90, 58 + pulse // 10, 46 + pulse // 10)

                pygame.draw.rect(
                    screen,
                    color,
                    (0, TOP_BORDER_Y - 5, SCREEN_WIDTH, 5)
)
                window.blit(screen, (GAME_X, GAME_Y))
                pygame.display.update()
                clock.tick(60)
            
            # GAME OVER SCREEN
            else:
                self.game_over_screen()
                
                window.fill((194, 39, 45)) 
                window.blit(screen, (GAME_X, GAME_Y)) 
                
                pygame.display.update() 
                clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()