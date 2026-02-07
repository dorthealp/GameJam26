import pygame
import sys

# Initialisering
pygame.init()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Farger
WHITE = (255, 255, 255)


class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y, level, image_path):
        super().__init__()
        self.level = level
        
        # 1. Last inn bildet
        try:
            raw_image = pygame.image.load(image_path).convert_alpha()
        except:
            # En "fallback" hvis bildet mangler, så spillet ikke krasjer
            raw_image = pygame.Surface((50, 50))
            raw_image.fill((255, 0, 255)) 

        # 2. Bestem størrelse basert på nivå
        # Eksempel: Level 0 = 30px, Level 1 = 50px, Level 2 = 70px...
        self.size = 30 + (level * 25) 
        
        # 3. Skaler bildet til den nye størrelsen
        self.image = pygame.transform.scale(raw_image, (self.size, self.size))
        
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = self.size // 2
        
        # Fysikk-variabler (som før)
        self.velocity_y = 0
        self.velocity_x = 0
        self.gravity = 0.5

    def update(self):
        # Bruk tyngdekraft
        self.velocity_y += self.gravity
        
        # Oppdater posisjon
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Veggkollisjon (Venstre/Høyre)
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity_x *= -0.5 # Sprett litt tilbake
        elif self.rect.right > 400: # SCREEN_WIDTH
            self.rect.right = 400
            self.velocity_x *= -0.5

        # Gulvkollisjon
        if self.rect.bottom > 550: # Sett gulvet litt opp fra bunnen
            self.rect.bottom = 550
            self.velocity_y = 0
            self.velocity_x *= 0.9 # Friksjon mot gulvet

class Game:
    def __init__(self):
        self.background = pygame.image.load("lysrosa.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.fruits = pygame.sprite.Group()
        self.current_level = 1 # Startfrukt

        # En liste med filnavnene dine i rekkefølge (0 er minste frukt)
        self.fruit_images = [
            "9hqZid.png",   # Level 0, denne vil bli ignorert pga listelogikk
            "fotb.png",  # Level 1
            "9hqZid.png",     # Level 2
            "fotb.png",  # Level 3
            "9hqZid.png",      # Level 4 osv..
            "9hqZid.png",   
            "fotb.png",  
            "9hqZid.png",     
            "fotb.png",  
            "9hqZid.png",
            "fotb.png",  
            "volleyb.png",        
        ]
        
    def spawn_fruit(self, x):
        # Vi henter riktig bilde-sti basert på current_level
        image_path = self.fruit_images[self.current_level]
        new_fruit = Fruit(x, 50, self.current_level, image_path)
        self.fruits.add(new_fruit)

    def handle_collisions(self):
            fruits_list = self.fruits.sprites()
            
            for i in range(len(fruits_list)):
                for j in range(i + 1, len(fruits_list)):
                    # Sjekk om fruktene fortsatt eksisterer (viktig ved merging!)
                    if i >= len(fruits_list) or j >= len(fruits_list): continue
                    
                    f1 = fruits_list[i]
                    f2 = fruits_list[j]

                    dx = f1.rect.centerx - f2.rect.centerx
                    dy = f1.rect.centery - f2.rect.centery
                    distance = (dx**2 + dy**2)**0.5
                    min_dist = f1.radius + f2.radius

                    if distance < min_dist:
                        # --- HER STARTER MERGING-LOGIKKEN (Punkt 3) ---
                        if f1.level == f2.level:
                            new_level = f1.level + 1
                            
                            # Sjekk at vi faktisk har et bilde for neste nivå
                            if new_level < len(self.fruit_images):
                                new_x = (f1.rect.centerx + f2.rect.centerx) / 2
                                new_y = (f1.rect.centery + f2.rect.centery) / 2
                                
                                # Fjern de gamle ballene
                                f1.kill()
                                f2.kill()
                                
                                # Lag den nye ballen med bilde fra listen
                                new_path = self.fruit_images[new_level]
                                new_fruit = Fruit(new_x, new_y, new_level, new_path)
                                self.fruits.add(new_fruit)
                                
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

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x = pygame.mouse.get_pos()[0]
                    self.spawn_fruit(mouse_x)

            # 1. Oppdater posisjoner
            self.fruits.update()
            
            # 2. Sjekk kollisjoner og merging
            self.handle_collisions()

            # 3. Tegn alt på nytt
            screen.blit(self.background, (0, 0))
            self.fruits.draw(screen)
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()