import pygame

class Scoreboard:
    def __init__(self, x, y):
        self.score = 0
        self.x = x
        self.y = y
        self.font = pygame.font.Font("Fonts/Pangolin-Regular.ttf", 60)
        self.label_font = pygame.font.Font("Fonts/SedgwickAve-Regular.ttf", 30)

    def add_score_by_level(self, points):
        points = 10 # 10 poeng hver gang det merger
        self.score += points

    def draw(self, window):
        # Tegn merkelapp
        label_surf = self.label_font.render("POENG", True, (255, 182, 193)) # Lys rosa tekst
        window.blit(label_surf, (self.x, self.y))
        
        # Tegn selve tallet rett under
        score_surf = self.font.render(str(self.score), True, (255, 255, 255))
        window.blit(score_surf, (self.x, self.y + 40))