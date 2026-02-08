import random
import pygame
import sys
import Animal
from Scoreboard import Scoreboard
from StartScreen import StartScreen
from AudioManager import AudioManager

# Initialisering
pygame.init()
pygame.display.set_caption("Path to Prosperity")

# INNER PLAYABLE area
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 600

# OUTER FRAME
FRAME_WIDTH = 1080
FRAME_HEIGHT = 700

screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
window = pygame.display.set_mode((FRAME_WIDTH, FRAME_HEIGHT))
icon = pygame.image.load("Assets/dragon.png").convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

pixel_font = pygame.font.Font("Fonts/SedgwickAve-Regular.ttf", 40)
pixel_font_thin = pygame.font.Font("Fonts/Pangolin-Regular.ttf", 30)
pixel_font_credits = pygame.font.Font("Fonts/Pangolin-Regular.ttf", 25)
pixel_font_over = pygame.font.Font("Fonts/SedgwickAve-Regular.ttf", 50)

GAME_X = (FRAME_WIDTH - SCREEN_WIDTH) // 2
GAME_Y = (FRAME_HEIGHT - SCREEN_HEIGHT) // 2

#Border
TOP_BORDER_Y = 80

# Farger
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        self.background = pygame.image.load("Assets/background.png").convert()
        self.background = pygame.transform.scale(self.background, (FRAME_WIDTH, FRAME_HEIGHT))
        
        self.inner_background = pygame.image.load("Assets/game_background.png").convert() 
        self.inner_background = pygame.transform.scale(self.inner_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.animals = pygame.sprite.Group()
        self.current_level = 1 # Startfrukt
        self.active_game = False
        self.on_start_screen = True # Starter spillet på startscreen
        self.start_menu = StartScreen(window, pixel_font, pixel_font_credits)

        #Opprette lydbehandleren & starter musikk med en gang
        self.audio = AudioManager()
        self.audio.play_music()

        #Scoreboard
        self.scoreboard = Scoreboard(GAME_X + SCREEN_WIDTH + 50, GAME_Y + 40)
        self.high_score = 0

        #Animals
        self.animal_images = [
            "Assets/volleyb.png", # Level 0, denne vil bli ignorert pga listelogikk
            "Assets/rat.png",   # Level 1
            "Assets/snake.png",  # Level 2
            "Assets/cat.png",     # Level 3
            "Assets/rooster.png",  # Level 4
            "Assets/monkey.png",      # Level 5
            "Assets/dog.png",           #...
            "Assets/goat.png",  
            "Assets/pig.png",     
            "Assets/horse.png",  
            "Assets/tiger.png",
            "Assets/buffalo.png",  
            "Assets/dragon.png",        
        ]

        self.next_animal_level = self.choose_next_level()
        self.next_animal_image = self.animal_images[self.next_animal_level]
        self.animal_surfaces = []
        for path in self.animal_images:
            try:
                img = pygame.image.load(path).convert_alpha()
            except:
                img = pygame.Surface((50, 50))
                img.fill((255, 0, 255))
            self.animal_surfaces.append(img)
        self.next_animal_level = self.choose_next_level()
        
        # Drop Bar
        self.bar_x = SCREEN_WIDTH // 2 
        self.bar_y = 40 
        self.bar_speed = 7 
        self.bar_width = 80 
        self.bar_height = 6

    def choose_next_level(self):
            levels = [1, 2, 3, 4]
            weights = [50, 30, 15, 5]
            return random.choices(levels, weights=weights, k=1)[0]
        
    def spawn_animals(self, x):
        level = self.next_animal_level

        new_animal = Animal.Animal(self.bar_x, 100, level, self.animal_images[level])
        half_width = new_animal.rect.width // 2
        clamped_x = max(half_width, min(SCREEN_WIDTH - half_width, x))
        new_animal.rect.centerx = clamped_x
        self.animals.add(new_animal)
        self.next_animal_level = self.choose_next_level()

    def draw_next_animal_preview(self):
        preview_x = GAME_X + SCREEN_WIDTH + 50
        preview_y = GAME_Y + 250

        # Scale preview image smaller
        surface = self.animal_surfaces[self.next_animal_level]
        preview_size = 60
        image = pygame.transform.scale(surface, (preview_size, preview_size))
        window.blit(image, (preview_x, preview_y))
        font = pygame.font.Font("Fonts/SedgwickAve-Regular.ttf", 30)
        label_surf = font.render("NESTE", True, (77, 13, 15))
        window.blit(label_surf, (preview_x, preview_y - 30))

    def handle_collisions(self):
        animals_list = self.animals.sprites()
        for i in range(len(animals_list)):
            for j in range(i + 1, len(animals_list)):
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
                            f1.kill()
                            f2.kill()
                            self.audio.play_merge_sound()
                            new_path = self.animal_images[new_level]
                            new_animal = Animal.Animal(new_x, new_y, new_level, new_path)
                            self.animals.add(new_animal)
                            self.scoreboard.add_score_by_level(10) 
                            return

                    # --- STACKING / PUSHING ---
                    overlap = min_dist - distance
                    if overlap > 0:
                        if distance == 0:
                            dx = 0.01
                            distance = 0.01
                        nx = dx / distance
                        ny = dy / distance
                        push_factor = 0.3
                        f1.rect.centerx += nx * overlap * push_factor
                        f1.rect.centery += ny * overlap * push_factor
                        f2.rect.centerx -= nx * overlap * push_factor
                        f2.rect.centery -= ny * overlap * push_factor

                        # Reset vertical velocity if stacking vertically
                        if ny > 0.7:
                            f1.velocity_y *= 0.8
                            f2.velocity_y *= 0.8
                        # --- CLAMP inside inner screen ---
                        for f in [f1, f2]:
                            if f.rect.left < 0:
                                f.rect.left = 0
                            if f.rect.right > SCREEN_WIDTH:
                                f.rect.right = SCREEN_WIDTH

    def reset_game(self):
        self.animals.empty()
        self.current_level = 1
        self.active_game = True
        self.scoreboard.score = 0               

    def check_game_over(self):
        for animal in self.animals:
            # 1. Ballen må først falle UNDER baren for å være "i spill"
            if not animal.entered_game:
                if animal.rect.top > self.bar_y:
                    animal.entered_game = True
                continue

            # 2. Hvis ballen HAR vært under baren og nå går OPP igjen → game over
            if (animal.entered_game and animal.prev_top >= TOP_BORDER_Y and animal.rect.top <= TOP_BORDER_Y):
                self.update_high_score()
                self.active_game = False
                return
    
    def update_high_score(self):
        if self.scoreboard.score > self.high_score:
            self.high_score = self.scoreboard.score
        return self.high_score
    
    def game_over_screen(self):
        screen.blit(self.inner_background, (0, 0))

        game_over_surface = pixel_font_over.render("Game Over", False, (156, 27, 32))
        game_over_rectangle = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(game_over_surface, game_over_rectangle)
        
        game_over_description_surface = pixel_font_thin.render("Trykk på mellomromstasten", False, (156, 27, 32))
        game_over_description_rectangle = game_over_description_surface.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(game_over_description_surface, game_over_description_rectangle)

        game_over_description2_surface = pixel_font_thin.render("for å prøve igjen", False, (156, 27, 32))
        game_over_description2_rectangle = game_over_description2_surface.get_rect(center=(SCREEN_WIDTH // 2, 350))
        screen.blit(game_over_description2_surface, game_over_description2_rectangle)

        game_over_score_surface = pixel_font_thin.render(f"Dine poeng: {self.scoreboard.score}", False, (156, 27, 32))
        game_over_score_rectangle = game_over_score_surface.get_rect(center=(SCREEN_WIDTH // 2, 450))
        screen.blit(game_over_score_surface, game_over_score_rectangle)
        
        game_over_highscore_surface = pixel_font_thin.render(f"Din rekord: {self.high_score}", False, (156, 27, 32))
        game_over_highscore_rectangle = game_over_highscore_surface.get_rect(center=(SCREEN_WIDTH // 2, 500))
        screen.blit(game_over_highscore_surface, game_over_highscore_rectangle)

    def run(self):
        while True:
            for event in pygame.event.get(): # håndterer events (tastetrykk og mus)
                if event.type == pygame.QUIT: 
                    pygame.quit() 
                    sys.exit() 
                
                # SPACE på GAME OVER → restart 
                if not self.active_game and not self.on_start_screen: 
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
                        self.reset_game() 
                
                # alt med mus 
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    # tilstand 1: start skjerm -> start spill (med klikk) 
                    if self.on_start_screen: 
                        self.on_start_screen = False 
                        self.active_game = True 
                    # tilstand 2: spill er i gang -> slipp dyr 
                    elif self.active_game: 
                        mx, my = pygame.mouse.get_pos() 
                        if GAME_X <= mx <= GAME_X + SCREEN_WIDTH: 
                            local_x = mx - GAME_X 
                            self.spawn_animals(self.bar_x) 
                    # tilstand 3: game over -> INGENTING med mus 
                    else:
                        pass
            
            window.blit(self.background, (0, 0))
            # --- TEGNING ---
            if self.on_start_screen:
                self.start_menu.draw()
            elif self.active_game:
                window.blit(self.background, (0, 0)) # Bakgrunn for selve spillet
                
                self.animals.update()
                self.handle_collisions()
                self.check_game_over()

                # Tegning av indre spillflate
                screen.blit(self.inner_background, (0, 0))
                self.animals.draw(screen)

                # Linje logikk
                pulse = abs((pygame.time.get_ticks() % 1000) - 500) // 4
                color = (90, 58 + pulse // 10, 46 + pulse // 10)
                pygame.draw.rect(screen, color, (0, TOP_BORDER_Y - 5, SCREEN_WIDTH, 5))
                
                # --- DRAW DROP BAR ---
                pygame.draw.rect(
                    screen,
                    (212, 68, 62),
                    (self.bar_x - self.bar_width//2, self.bar_y, self.bar_width, self.bar_height),
                    border_radius = 6
                )
                
                # --- BAR FOLLOWS MOUSE ---
                mx, my = pygame.mouse.get_pos()

                # konverter musens posisjon til lokal spillflate
                local_x = mx - GAME_X

                # clamp så baren ikke går utenfor
                self.bar_x = max(self.bar_width//2, min(SCREEN_WIDTH - self.bar_width//2, local_x))

                # Tegne alt på vinduet
                self.scoreboard.draw(window)
                self.draw_next_animal_preview()  # <-- here
                window.blit(screen, (GAME_X, GAME_Y))
                window.blit(screen, (GAME_X, GAME_Y))
                pygame.draw.rect(window, (77, 13, 15), (GAME_X - 5, GAME_Y - 5, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10), 10)
            else:
                self.game_over_screen()
                window.blit(screen, (GAME_X, GAME_Y))
                pygame.draw.rect(window, (77, 13, 15), (GAME_X - 5, GAME_Y - 5, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10), 10)
            pygame.display.update() 
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()