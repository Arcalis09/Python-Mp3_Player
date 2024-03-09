import os
import pygame
import random
import json

# Global variables to store music directory, current playing index, loop status, and volume level
config_file = "config.json"
music_dir = ""
current_index = 0
loop_song = False  # Default: Do not loop the song
volume_level = 0.5  # Default volume level (0.0 to 1.0)

def clear():
    os.system("cls")

# Function to load configuration from file
def load_config():
    global music_dir
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            config = json.load(file)
            music_dir = config.get("music_dir", "")
    else:
        print("Configuration file not found. Using default values.")

# Function to save configuration to file
def save_config():
    config = {"music_dir": music_dir}
    with open(config_file, "w") as file:
        json.dump(config, file)

# Function to play a specific song from the specified directory
def play_specific_song(song):
    # Load the selected song
    pygame.mixer.music.load(os.path.join(music_dir, song))
    clear()
    print("Now playing:", song)
    
    # Set the volume level
    pygame.mixer.music.set_volume(volume_level)
    
    # Play the song
    pygame.mixer.music.play()
    
    # Set the looping status based on user input
    if loop_song:
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)  # Set a custom event for song end
    
    # Get the total duration of the song
    sound = pygame.mixer.Sound(os.path.join(music_dir, song))
    total_duration = sound.get_length()
    
    # Infinite loop to handle song playback
    while pygame.mixer.music.get_busy():
        # Check for user input to stop the music
        stop_command = input("Enter 's' to stop the music or enter 'r' to skip to a random song : ")
        if stop_command.lower() == 's':
            pygame.mixer.music.stop()
            print("\nMusic stopped.")
            return
        elif stop_command.lower() == "r":
            play_random_song()
        
        # Check if the song has finished playing
        if pygame.mixer.music.get_pos() / 1000 >= total_duration:
            print("Song finished.")
            play_random_song()  # Play a random song when the current song finishes
            return

# Function to play a random song from the music directory
def play_random_song():
    songs = os.listdir(music_dir)
    # Filter out non-MP3 files if any
    songs = [song for song in songs if song.endswith('.mp3')]
    
    # Check if there are any songs in the directory
    if not songs:
        print("No MP3 files found in the directory.")
        return
    
    # Select a random song
    random_song = random.choice(songs)
    play_specific_song(random_song)

# Function to display available songs and allow the user to select one
def select_song_to_play():
    # Get list of all files in the directory
    songs = os.listdir(music_dir)
    # Filter out non-MP3 files if any
    songs = [song for song in songs if song.endswith('.mp3')]
    
    # Check if there are any songs in the directory
    if not songs:
        print("No MP3 files found in the directory.")
        return
    clear()
    print("Available Songs:")
    for i, song in enumerate(songs, start=1):
        print(f"{i}. {song}")
    
    # Prompt the user to select a song
    while True:
        try:
            choice = int(input("Enter the number of the song you want to play (or 0 to go back): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(songs):
                global current_index
                current_index = choice - 1
                selected_song = songs[current_index]
                play_specific_song(selected_song)
                break
            else:
                print("Invalid choice. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to toggle the loop status
def toggle_loop_status():
    global loop_song
    loop_song = not loop_song
    print("Looping is", "enabled" if loop_song else "disabled")

# Function to change the volume level
def change_volume():
    global volume_level
    clear()
    while True:
        try:
            volume = float(input("Enter the volume level (0.0 to 1.0): "))
            if 0.0 <= volume <= 1.0:
                volume_level = volume
                pygame.mixer.music.set_volume(volume_level)
                print("Volume level set to", volume_level)
                break
            else:
                print("Volume level must be between 0.0 and 1.0.")
        except ValueError:
            print("Invalid input. Please enter a number between 0.0 and 1.0.")

# Function to play the next song
def play_next_song():
    play_random_song()

# Function to play the previous song
def play_previous_song():
    play_random_song()

# Function to select the music directory
def select_music_directory():
    global music_dir
    if not music_dir:  # Check if the music directory is not already set
        music_dir = input("Enter the path to your music directory: ")
        if not os.path.isdir(music_dir):
            print("Invalid directory path. Please try again.")
            select_music_directory()

# Main function
def main():
    load_config()  # Load configuration
    select_music_directory()  # Prompt the user to select the music directory
    
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Infinite loop to keep the music player running
    while True:
        clear()
        print("Toggle State : ", loop_song)
        print("\n1. Select and play specific song\n2. Toggle loop status\n3. Change volume\n4. Skip to next song\n5. Skip to previous song\n6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            select_song_to_play()
        elif choice == '2':
            toggle_loop_status()
        elif choice == '3':
            change_volume()
        elif choice == '4':
            play_next_song()
        elif choice == '5':
            play_previous_song()
        elif choice == '6':
            save_config()  # Save configuration
            pygame.mixer.quit()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
