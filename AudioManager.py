import pygame

class AudioManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    
        try:
            pygame.mixer.music.load("Assets/Sounds/Wire Wire Docks.wav")
            pygame.mixer.music.set_volume(0.3)
        except pygame.error as e:
            print(f"Kunne ikke laste musikk: {e}")

        try:
            self.merge_sound = pygame.mixer.Sound("Assets/Sounds/pop2.mp3")
            self.merge_sound.set_volume(0.3) # eget volum
        except pygame.error as e:
            print("Kunne ikke laste lydeffekt: {e}")

    def play_music(self):
        pygame.mixer.music.play(-1)

    def play_merge_sound(self):
        self.merge_sound.play()
    
    def stop_music(self):
        pygame.mixer.music.stop()
    
    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)