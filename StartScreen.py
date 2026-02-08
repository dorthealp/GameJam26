import pygame

class StartScreen:
    def __init__(self, screen, font_main, font_sub):
        self.screen = screen
        self.font_main = font_main
        self.font_sub = font_sub
        
        # Her laster du inn tegningene dine etter hvert
        try:
            self.envelope = pygame.image.load("Assets/lixi.png").convert_alpha()
            # Vi skalerer den så den passer fint i midten (f.eks. 200 piksler bred)
            # Du kan justere størrelsen her:
            self.envelope = pygame.transform.scale(self.envelope, (200, 350))
            self.has_image = True
        except:
            # Hvis bildet ikke finnes ennå, bruker vi en rød firkant som plassholder
            self.has_image = False

    def draw(self):
        # Fyll bakgrunnen (samme oransje som spillet)
        self.screen.fill((254, 172, 90))

        # Tittel-tekst
        title_surface = self.font_main.render("MERGE SPILL", True, (90, 13, 16))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_surface, title_rect)

        # Plassholder for tegning (hvis du ikke har lastet inn bilde ennå)
        if self.has_image:
            # Sentrer bildet i midten av skjermen
            rect = self.envelope.get_rect(center=(self.screen.get_width() // 2, 320))
            self.screen.blit(self.envelope, rect)
        else:
            # Midlertidig rød konvolutt-firkant til du har bildet klart
            temp_rect = pygame.Rect(0, 0, 180, 300)
            temp_rect.center = (self.screen.get_width() // 2, 320)
            pygame.draw.rect(self.screen, (156, 27, 32), temp_rect) # En rød rektangel
            pygame.draw.rect(self.screen, (212, 175, 55), temp_rect, 3) # Gull-kant?

        # Instruksjons-tekst
        inst_surface = self.font_sub.render("Press to start", True, (90, 13, 16))
        inst_rect = inst_surface.get_rect(center=(self.screen.get_width() // 2, 530))
        self.screen.blit(inst_surface, inst_rect)