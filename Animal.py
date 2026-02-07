import pygame


class Animal(pygame.sprite.Sprite):
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
