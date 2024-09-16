import pygame

class MusicPlayer:
    """Class that handles creation of a simple music mixer to play sounds. member functions to control the mixer"""
    def __init__(self, bg_music_path, completion_sound_path, fail_sound_path):

        pygame.mixer.init()  # Initialize mixer
        self.bg_music_path = bg_music_path
        self.completion_sound = pygame.mixer.Sound(completion_sound_path)
        self.fail_sound = pygame.mixer.Sound(fail_sound_path)
        
        #self.play_background_music()

    def play_background_music(self):
        #load and play background music in loop
        pygame.mixer.music.load(self.bg_music_path)
        pygame.mixer.music.play(-1)  # (-1) forever loop 

    def play_level_completion_sound(self): # pass level sound, plays upon level feedback
        self.completion_sound.play()
        pygame.time.delay(500)

    def play_level_fail_sound(self): # level failed sound, also plays upon receiving level feedback
        self.fail_sound.play()
        pygame.time.delay(500)

    def stop_background_music(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        #set volume of all songs/sounds (0.0 to 1.0)
        pygame.mixer.music.set_volume(volume)
        self.completion_sound.set_volume(volume)
        self.fail_sound.set_volume(volume)
