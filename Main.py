import pygame
import sys
import Animal
from Scoreboard import Scoreboard
from StartScreen import StartScreen

# Initialisering
pygame.init()

# INNER PLAYABLE area
SCREEN_WIDTH = 550
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
        self.on_start_screen = True # starter spillet på startscreen

        # Start screen
        self.start_menu = StartScreen(screen, pixel_font, pixel_font_thin)

        #scoreboard
        self.scoreboard = Scoreboard(GAME_X + SCREEN_WIDTH + 50, GAME_Y + 100)

        # En liste med filnavnene dine i rekkefølge (0 er minste frukt)
        self.animal_images = [
            "Asserts/rat.png",   # Level 0, denne vil bli ignorert pga listelogikk
            "Assets/snake.png",  # Level 1
            "Assets/cat.png",     # Level 2
            "Assets/rooster.png",  # Level 3
            "Assets/monkey.png",      # Level 4 osv..
            "Assets/dog.png",   
            "Assets/goat.png",  
            "Assets/pig.png",     
            "Assets/horse.png",  
            "Assets/tiger.png",
            "Assets/buffalo.png",  
            "Assets/dragon.png",        
        ]
        
    def spawn_animals(self, x):
        # Vi henter riktig bilde-sti basert på current_level
        image_path = self.animal_images[self.current_level]
        new_animal= Animal.Animal(x, 50, self.current_level, image_path, 1 + self.current_level * 0.5 )
        
         # Clamp the center so the sprite stays fully inside the inner screen
        half_width = new_animal.rect.width // 2
        clamped_x = max(half_width, min(SCREEN_WIDTH - half_width, x))
        new_animal.rect.centerx = clamped_x
        self.animals.add(new_animal)

    def handle_collisions(self):
        animals_list = self.animals.sprites()

        for i in range(len(animals_list)):
            for j in range(i + 1, len(animals_list)):
                if i >= len(animals_list) or j >= len(animals_list):
                    continue

                f1 = animals_list[i]
                f2 = animals_list[j]

                dx = f1.rect.centerx - f2.rect.centerx
                dy = f1.rect.centery - f2.rect.centery
                distance = (dx ** 2 + dy ** 2) ** 0.5
                min_dist = f1.radius + f2.radius

                if distance < min_dist:
                    # --- MERGING ---
                    if f1.level == f2.level:
                        new_level = f1.level + 1
                        if new_level < len(self.animal_images):
                            new_x = (f1.rect.centerx + f2.rect.centerx) / 2
                            new_y = (f1.rect.centery + f2.rect.centery) / 2
                            new_mass = f1.mass + f2.mass
                            f1.kill()
                            f2.kill()
                            new_path = self.animal_images[new_level]
                            new_animal = Animal.Animal(new_x, new_y, new_level, new_path, mass=new_mass)
                            self.animals.add(new_animal)
                            self.scoreboard.add_score_by_level(10) 
                            return

                    # --- STACKING / PUSHING ---
                    overlap = min_dist - distance
                    if distance == 0:
                        distance = 1
                    nx = dx / distance
                    ny = dy / distance
                    total_mass = f1.mass + f2.mass

                    # Apply movement proportional to mass
                    f1.rect.x += nx * (overlap * f2.mass / total_mass)
                    f1.rect.y += ny * (overlap * f2.mass / total_mass)
                    f2.rect.x -= nx * (overlap * f1.mass / total_mass)
                    f2.rect.y -= ny * (overlap * f1.mass / total_mass)

                    # --- CLAMP inside inner screen ---
                    for f in [f1, f2]:
                        # X posisjon
                        if f.rect.left <= 0:
                            f.rect.left = 0
                        if f.rect.right >= SCREEN_WIDTH:
                            f.rect.right = SCREEN_WIDTH
                        # y posisjon
                        if f.rect.top <= 0:
                            f.rect.top = 0
                        if f.rect.bottom >= SCREEN_HEIGHT:
                            f.rect.bottom = SCREEN_HEIGHT

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
        
        game_over_description_surface = pixel_font_thin.render("Press to replay", False, (156, 27, 32))
        game_over_description_rectangle = game_over_description_surface.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(game_over_description_surface, game_over_description_rectangle)

        game_over_score_surface = pixel_font_thin.render(f"Your score: {self.scoreboard.score}", False, (156, 27, 32))
        game_over_score_rectangle = game_over_score_surface.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(game_over_score_surface, game_over_score_rectangle)

    def run(self):
        while True:
            for event in pygame.event.get(): # håndterer events (tastetrykk og mus)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # alt blir styrt med museklikk
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # tilstand 1: start skjerm -> start spill
                    if self.on_start_screen:
                        self.on_start_screen = False
                        self.active_game = True
                    # tilstand 2: spill er i gang -> slipp dyr
                    elif self.active_game:
                        mx, my = pygame.mouse.get_pos()
                        # Check if click is inside game screen
                        if GAME_X <= mx <= GAME_X + SCREEN_WIDTH:
                            local_x = mx - GAME_X
                            self.spawn_animals(local_x)
                    # tilstand 3: game over -> reset og start på nytt
                    else:
                        self.reset_game()
            
            # TEGNING AV START SKJERM
            window.fill((194, 39, 45)) # ytterst bakgrunnsfarge

            if self.on_start_screen:
                # vis startskjerm
                self.start_menu.draw() 
                window.blit(screen, (GAME_X, GAME_Y))
                pygame.draw.rect(window, (77, 13, 15), (GAME_X - 5, GAME_Y - 5, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10), 10)
            elif self.active_game:
                self.animals.update()
                self.handle_collisions()
                self.check_game_over()
            
                # tegning av indre spillflate
                screen.fill((254, 172, 90))
                self.animals.draw(screen)

                # linje logikk
                pulse = abs((pygame.time.get_ticks() % 100) - 500) // 4
                color = (90, 58 + pulse // 10, 46 + pulse // 10)
                pygame.draw.rect(screen, color, (0, TOP_BORDER_Y - 5, SCREEN_WIDTH, 5))

                # tegne alt på vinduet
                self.scoreboard.draw(window)
                window.blit(screen, (GAME_X, GAME_Y))
                pygame.draw.rect(window, (77, 13, 15), (GAME_X - 5, GAME_Y - 5, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10), 10)
            else:
                # vise game over
                self.game_over_screen()
                window.blit(screen, (GAME_X, GAME_Y))
                pygame.draw.rect(window, (77, 13, 15), (GAME_X - 5, GAME_Y - 5, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10), 10)
            
            pygame.display.update() 
            clock.tick(60)
            
            """ GAMEPLAY
            if self.active_game:
                # 1. Oppdater posisjoner
                self.animals.update()
                
                # 2. Sjekk kollisjoner og merging
                self.handle_collisions()

                #3. check game over
                self.check_game_over()

                # 4. Tegn alt på nytt
                screen.blit(self.background, (0, 0))
                window.fill((194, 39, 45)) # ytre rød
                screen.fill((254, 172, 90)) # indre gul/oransj
                self.animals.draw(screen)
                
                #linje logikk
                pulse = abs((pygame.time.get_ticks() % 1000) - 500) // 4
                color = (90, 58 + pulse // 10, 46 + pulse // 10)

                pygame.draw.rect(
                    screen,
                    color,
                    (0, TOP_BORDER_Y - 5, SCREEN_WIDTH, 5))
                window.fill((30, 30, 30))
                self.scoreboard.draw(window)
                
                window.blit(screen, (GAME_X, GAME_Y))
                pygame.draw.rect(window, (77, 13, 15), (GAME_X - 5, GAME_Y - 5, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10), 10)

                pygame.display.update()
                clock.tick(60)
            
            # GAME OVER SCREEN
            else:
                self.game_over_screen()
                
                window.fill((194, 39, 45)) 
                window.blit(screen, (GAME_X, GAME_Y)) 
                
                pygame.draw.rect(window, (77, 13, 15), (GAME_X - 5, GAME_Y - 5, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10), 10)

                pygame.display.update() 
                clock.tick(60)"""

if __name__ == "__main__":
    game = Game()
    game.run()