import random
import matplotlib.pyplot as plt
from midiutil import MIDIFile
import pygame
import time

class DNAtoMusicConverter:
    def __init__(self):
        self.base_to_note = {
            'A': 25,  # C4
            'T': 15,  # D4
            'C': 29,  # E4
            'G': 41,  # G4
            'N': 33   # F4
        }

        self.base_to_color = {
            'A': 'red',
            'T': 'blue',
            'C': 'green',
            'G': 'yellow',
            'N': 'gray'
        }

        self.original_sequence = ""
        self.cleaned_sequence = ""
        self.notes = []
        self.durations = []

    def load_dna_sequence(self, filename=None):
        if filename:
            try:
                with open(filename, 'r') as file:
                    self.original_sequence = ''.join(
                        line.strip() for line in file if not line.startswith('>')
                    )
            except FileNotFoundError:
                print(f"File {filename} not found. Generating random sequence.")
                self._generate_random_sequence(100)
        else:
            self._generate_random_sequence(100)

        self.original_sequence = self.original_sequence.upper()
        valid_bases = {'A', 'T', 'C', 'G'}
        self.cleaned_sequence = ''.join(
            base if base in valid_bases else 'N'
            for base in self.original_sequence
        )

    def _generate_random_sequence(self, length):
        bases = ['A', 'T', 'C', 'G']
        self.original_sequence = ''.join(random.choice(bases) for _ in range(length))
        self.cleaned_sequence = self.original_sequence

    def convert_to_music(self):
        self.notes = []
        self.durations = []

        for base in self.cleaned_sequence:
            note = self.base_to_note.get(base, self.base_to_note['N'])
            self.notes.append(note)
            duration = random.choice([0.5, 1.0, 1.5])
            self.durations.append(duration)

    def create_midi_file(self, filename="dna_music.mid"):
        midi = MIDIFile(1)
        track, channel, volume = 0, 0, 100
        tempo = 120

        midi.addTrackName(track, 0, "DNA Music")
        midi.addTempo(track, 0, tempo)

        time_pos = 0
        for note, duration in zip(self.notes, self.durations):
            midi.addNote(track, channel, note, time_pos, duration, volume)
            time_pos += duration

        with open(filename, "wb") as output_file:
            midi.writeFile(output_file)
        print(f"MIDI file saved as {filename}")

    def visualize_sequence(self):
        if not self.cleaned_sequence or not self.notes:
            print("No sequence or notes to visualize.")
            return

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

        for i, base in enumerate(self.cleaned_sequence):
            ax1.bar(i, 1, color=self.base_to_color[base], edgecolor='black')
            ax1.text(i, 0.5, base, ha='center', va='center', fontweight='bold')

        ax1.set_title("DNA Sequence")
        ax1.set_yticks([])
        ax1.set_xticks(range(len(self.cleaned_sequence)))

        time_pos = 0
        for i, (note, duration) in enumerate(zip(self.notes, self.durations)):
            base = self.cleaned_sequence[i]
            ax2.bar(time_pos, note, width=duration*0.9,
                    color=self.base_to_color[base], edgecolor='black', alpha=0.7)
            ax2.text(time_pos + duration/2, note,
                     f"{self._midi_to_note_name(note)}\n({duration} beat{'s' if duration != 1 else ''})",
                     ha='center', va='center')
            time_pos += duration

        ax2.set_title("Musical Notes")
        ax2.set_xlabel("Time (beats)")
        ax2.set_ylabel("Note Pitch")
        ax2.set_yticks(sorted(set(self.notes)))
        ax2.set_yticklabels([self._midi_to_note_name(n) for n in sorted(set(self.notes))])
        ax2.grid(True, axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()
        plt.savefig("dna_music_visualization.png")
        plt.show()

    def _midi_to_note_name(self, midi_number):
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return f"{notes[midi_number % 12]}{midi_number // 12 - 1}"

    def play_midi_file(self, filename="dna_music.mid"):
        pygame.init()
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            print("Playing MIDI file...")
            while pygame.mixer.music.get_busy():
                time.sleep(0.5)
        except Exception as e:
            print("Error playing MIDI file:", e)
        finally:
            pygame.mixer.quit()
            pygame.quit()

    def run_full_conversion(self, dna_file=None):
        print("Loading DNA sequence...")
        self.load_dna_sequence(dna_file)
        print(f"Sequence length: {len(self.cleaned_sequence)} bases")

        print("Converting to music...")
        self.convert_to_music()

        print("Creating MIDI file...")
        self.create_midi_file()

        print("Creating visualization...")
        self.visualize_sequence()

        print("Playing music...")
        self.play_midi_file()

        print("\nConversion complete!")

if __name__ == "__main__":
    converter = DNAtoMusicConverter()

    print("DNA to Music Converter")
    print("1. Use sample DNA sequence")
    print("2. Load DNA sequence from file")
    print("3. Generate random DNA sequence")

    choice = input("Enter your choice (1-3): ")

    if choice == "1":
        converter.original_sequence = "ATCG" * 8  # 32 bases
        converter.run_full_conversion()
    elif choice == "2":
        filename = input("Enter filename containing DNA sequence: ")
        converter.run_full_conversion(filename)
    elif choice == "3":
        length = int(input("Enter length of random sequence (10–500): "))
        converter._generate_random_sequence(min(max(length, 10), 500))
        converter.run_full_conversion()
    else:
        print("Invalid choice. Using sample sequence.")
        converter.original_sequence = "ATCG" * 8
        converter.run_full_conversion()
