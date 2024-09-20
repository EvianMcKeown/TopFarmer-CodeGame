import pygame


class MusicPlayer:
    """Handles the playback of background music and sound effects within the application.
    This class initializes the Pygame mixer, provides methods to play and stop music, and control sound effects for level completion and failure, enhancing the audio experience of the game.
    """

    def __init__(self, bg_music_path, completion_sound_path, fail_sound_path):
        """
        Initializes the MusicPlayer object, setting up the audio mixer and loading sound files.
        This constructor prepares the background music and sound effects for playback by initializing the Pygame mixer and storing the paths to the audio files.

        Args:
            bg_music_path: The file path to the background music.
            completion_sound_path: The file path to the sound played upon level completion.
            fail_sound_path: The file path to the sound played upon level failure.
        """

        pygame.mixer.init()  # Initialize mixer
        self.bg_music_path = bg_music_path
        self.completion_sound = pygame.mixer.Sound(completion_sound_path)
        self.fail_sound = pygame.mixer.Sound(fail_sound_path)

        # self.play_background_music()

    def play_background_music(self):
        """
        Loads and plays the background music in a continuous loop.
        This function initializes the music playback using the specified background music path, ensuring that the music plays indefinitely until stopped.
        """

        # load and play background music in loop
        pygame.mixer.music.load(self.bg_music_path)
        pygame.mixer.music.play(-1)  # (-1) forever loop

    def play_level_completion_sound(
        self,
    ):
        """Plays the sound effect associated with level completion.
        This function triggers the completion sound and introduces a brief delay to ensure the sound plays fully before any subsequent actions occur.
        """
        self.completion_sound.play()
        pygame.time.delay(500)

    def play_level_fail_sound(
        self,
    ):
        """
        Plays the sound effect associated with a level failure.
        This function triggers the failure sound and introduces a brief delay to ensure the sound plays fully before any subsequent actions occur.
        """
        self.fail_sound.play()
        pygame.time.delay(500)

    def stop_background_music(self):
        """Stops the playback of the background music.
        This function halts any currently playing background music, allowing for a quiet environment or the transition to other audio tracks.
        """
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        """
        Sets the volume for all audio playback in the music player.
        This function adjusts the volume level for the background music and sound effects, allowing for a range between 0.0 (mute) and 1.0 (maximum volume).

        Args:
            volume: A float value between 0.0 and 1.0 representing the desired volume level.
        """
        pygame.mixer.music.set_volume(volume)
        self.completion_sound.set_volume(volume)
        self.fail_sound.set_volume(volume)
