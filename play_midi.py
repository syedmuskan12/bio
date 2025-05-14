import pygame
import time

def play_midi(filename="dna_music.mid"):
    pygame.init()
    pygame.mixer.init()
    
    try:
        print(f"Playing {filename}...")
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        # Keep the program running while music plays
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Error: {e}. Try opening 'dna_music.mid' with VLC or other media player.")
    finally:
        pygame.quit()

if __name__ == "__main__":
    play_midi()