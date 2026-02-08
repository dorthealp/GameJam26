import pygame

class AudioManager:
    def __init__(self):
        # initiere music mixer
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    
        # laste inn bakgrunnsmusikk
        # bruker music-modul for lange filer da den streamer fra disk (sparer RAM)
        try:
            pygame.mixer.music.load("Assets/Sounds/Wire Wire Docks.wav")
            pygame.mixer.music.set_volume(0.3)
        except pygame.error as e:
            print(f"Kunne ikke laste musikk: {e}")

        # lydeffekt
        try:
            self.merge_sound = pygame.mixer.Sound("Assets/Sounds/p2.mp3")
            self.merge_sound.set_volume(0.3) # eget volum
        except pygame.error as e:
            print("Kunne ikke laste lydeffekt: {e}")

    def play_music(self):
        pygame.mixer.music.play(-1) # looper evig

    def play_merge_sound(self):
        self.merge_sound.play()
    
    def stop_music(self):
        pygame.mixer.music.stop()
    
    def set_volume(self, volume):
        # volum mellom 0.0 og 1.0
        pygame.mixer.music.set_volume(volume)