import pygame

class StartScreen:
    def __init__(self, screen, font_main, font_sub):
        self.screen = screen
        self.font_main = font_main
        self.font_sub = font_sub
        
       # 1. Last inn det heldekkende bildet
        try:
            self.bg_image = pygame.image.load("Assets/startscreen.png").convert()
            # Skaler bildet slik at det fyller hele skjermens bredde og høyde
            self.bg_image = pygame.transform.scale(self.bg_image, (screen.get_width(), screen.get_height()))
            self.has_image = True
        except:
            print("Kunne ikke laste bakgrunnsbilde for startskjerm.")
            self.has_image = False

    def draw(self):
        # Fyll bakgrunnen (samme oransje som spillet)
        self.screen.fill((254, 172, 90))


       # 2. Tegn bildet eller fallback-farge
        if self.has_image:
            # Tegn det heldekkende bildet fra øverste venstre hjørne (0,0)
            self.screen.blit(self.bg_image, (0, 0))
        else:
            # Fallback hvis bildet mangler (samme farge som før)
            self.screen.fill((254, 172, 110))

        # --- CREDITS TEKST ---

        text_color = (253, 187, 105)
        center_x = self.screen.get_width() // 2

        made_by_title = self.font_sub.render("Spill laget av:", True, text_color)
        self.screen.blit(made_by_title, made_by_title.get_rect(center=(center_x, 350)))

     
        names = self.font_sub.render("Dorthea, Juni, Kristy, Sandra", True, text_color)
        self.screen.blit(names, names.get_rect(center=(center_x, 385)))

        art_by_title = self.font_sub.render("Tegninger av:", True, text_color)
        self.screen.blit(art_by_title, art_by_title.get_rect(center=(center_x, 450)))

        artist_name = self.font_sub.render("Dorthea", True, text_color)
        self.screen.blit(artist_name, artist_name.get_rect(center=(center_x, 485)))

        

        # Instruksjons-tekst
        inst_surface = self.font_main.render("Trykk for å starte", True, (90, 13, 16))
        inst_rect = inst_surface.get_rect(center=(self.screen.get_width() // 2, 580))
        self.screen.blit(inst_surface, inst_rect)