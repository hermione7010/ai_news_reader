# Method 1: Simple TTS with Basic Animation Visualization
import pyttsx3
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from threading import Thread
import time

class SimpleAnimatedSpeaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.is_speaking = False
        
    def speak_with_animation(self, text):
        # Start speaking in a separate thread
        speak_thread = Thread(target=self._speak, args=(text,))
        speak_thread.start()
        
        # Create simple mouth animation
        self._animate_mouth()
        
    def _speak(self, text):
        self.is_speaking = True
        self.engine.say(text)
        self.engine.runAndWait()
        self.is_speaking = False
        
    def _animate_mouth(self):
        fig, ax = plt.subplots()
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Draw face
        face = plt.Circle((0, 0), 1.5, fill=False, linewidth=2)
        ax.add_patch(face)
        
        # Eyes
        left_eye = plt.Circle((-0.5, 0.3), 0.1, color='black')
        right_eye = plt.Circle((0.5, 0.3), 0.1, color='black')
        ax.add_patch(left_eye)
        ax.add_patch(right_eye)
        
        # Mouth (will be animated)
        mouth_line, = ax.plot([], [], 'r-', linewidth=3)
        
        def animate(frame):
            if self.is_speaking:
                # Create mouth movement
                mouth_width = 0.3 + 0.2 * np.sin(frame * 0.5)
                mouth_height = 0.1 * np.sin(frame * 0.3)
                x = np.linspace(-mouth_width, mouth_width, 10)
                y = mouth_height * np.sin(np.pi * x / mouth_width) - 0.5
                mouth_line.set_data(x, y)
            else:
                # Closed mouth
                x = np.linspace(-0.3, 0.3, 10)
                y = np.zeros(10) - 0.5
                mouth_line.set_data(x, y)
            return mouth_line,
        
        ani = animation.FuncAnimation(fig, animate, frames=200, 
                                    interval=50, blit=True, repeat=True)
        plt.show()

# Method 2: Using gTTS with Audio Visualization
import gtts
import io
import pygame
import numpy as np
from pydub import AudioSegment
import tempfile
import os

class GTTSAnimatedSpeaker:
    def __init__(self):
        pygame.mixer.init()
        
    def speak_with_gtts(self, text, lang='en'):
        # Generate speech
        tts = gtts.gTTS(text=text, lang=lang)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            
            # Play audio with visualization
            self._play_with_animation(tmp_file.name)
            
            # Clean up
            os.unlink(tmp_file.name)
    
    def _play_with_animation(self, audio_file):
        # Load and play audio
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        # Simple visualization while playing
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        
        # Character face
        ax1.set_xlim(-2, 2)
        ax1.set_ylim(-2, 2)
        ax1.set_aspect('equal')
        ax1.axis('off')
        ax1.set_title('Animated Character')
        
        # Face elements
        face = plt.Circle((0, 0), 1.5, fill=False, linewidth=2)
        ax1.add_patch(face)
        left_eye = plt.Circle((-0.5, 0.3), 0.1, color='black')
        right_eye = plt.Circle((0.5, 0.3), 0.1, color='black')
        ax1.add_patch(left_eye)
        ax1.add_patch(right_eye)
        
        # Audio waveform visualization
        ax2.set_xlim(0, 100)
        ax2.set_ylim(-1, 1)
        ax2.set_title('Audio Waveform')
        
        mouth_line, = ax1.plot([], [], 'r-', linewidth=4)
        wave_line, = ax2.plot([], [], 'b-')
        
        def animate(frame):
            if pygame.mixer.music.get_busy():
                # Animate mouth
                mouth_width = 0.3 + 0.3 * np.random.random()
                mouth_height = 0.2 * np.random.random()
                x = np.linspace(-mouth_width, mouth_width, 10)
                y = mouth_height * np.sin(np.pi * x / mouth_width) - 0.5
                mouth_line.set_data(x, y)
                
                # Animate waveform
                x_wave = np.arange(100)
                y_wave = np.random.random(100) * 0.5 - 0.25
                wave_line.set_data(x_wave, y_wave)
            else:
                # Closed mouth
                x = np.linspace(-0.2, 0.2, 10)
                y = np.zeros(10) - 0.5
                mouth_line.set_data(x, y)
                wave_line.set_data([], [])
                
            return mouth_line, wave_line
        
        ani = animation.FuncAnimation(fig, animate, interval=100, 
                                    blit=True, repeat=True)
        plt.show()

# Method 3: Advanced setup with Coqui TTS (requires installation)
class CoquiTTSAnimatedSpeaker:
    def __init__(self):
        try:
            from TTS.api import TTS
            # Initialize TTS with a multilingual model
            self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
            print("Coqui TTS initialized successfully!")
        except ImportError:
            print("Coqui TTS not installed. Install with: pip install TTS")
            self.tts = None
    
    def speak_advanced(self, text, output_path="output.wav"):
        if not self.tts:
            print("TTS not available")
            return
            
        # Generate speech
        self.tts.tts_to_file(text=text, file_path=output_path)
        
        # Play with advanced animation
        self._advanced_animation(output_path)
    
    def _advanced_animation(self, audio_file):
        # Load audio for analysis
        try:
            audio = AudioSegment.from_wav(audio_file)
            samples = np.array(audio.get_array_of_samples())
            
            if audio.channels == 2:
                samples = samples.reshape((-1, 2))
                samples = samples.mean(axis=1)
            
            # Create animation based on audio amplitude
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.set_xlim(-3, 3)
            ax.set_ylim(-3, 3)
            ax.set_aspect('equal')
            ax.axis('off')
            
            # Character elements
            face = plt.Circle((0, 0), 2, fill=False, linewidth=3, color='blue')
            ax.add_patch(face)
            
            # Eyes with expressions
            left_eye = plt.Circle((-0.7, 0.5), 0.2, color='black')
            right_eye = plt.Circle((0.7, 0.5), 0.2, color='black')
            ax.add_patch(left_eye)
            ax.add_patch(right_eye)
            
            # Eyebrows
            left_brow, = ax.plot([-1, -0.4], [0.8, 0.8], 'k-', linewidth=3)
            right_brow, = ax.plot([0.4, 1], [0.8, 0.8], 'k-', linewidth=3)
            
            # Mouth
            mouth_line, = ax.plot([], [], 'r-', linewidth=5)
            
            # Play audio
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            def animate(frame):
                if pygame.mixer.music.get_busy():
                    # Get audio amplitude for this frame
                    sample_idx = min(frame * 100, len(samples) - 1)
                    amplitude = abs(samples[sample_idx]) / 32768.0 if len(samples) > sample_idx else 0
                    
                    # Animate mouth based on amplitude
                    mouth_width = 0.5 + amplitude * 0.8
                    mouth_height = amplitude * 0.3
                    
                    x = np.linspace(-mouth_width, mouth_width, 20)
                    y = mouth_height * np.sin(np.pi * x / mouth_width) - 0.8
                    mouth_line.set_data(x, y)
                    
                    # Animate eyebrows based on speech
                    brow_lift = amplitude * 0.2
                    left_brow.set_ydata([0.8 + brow_lift, 0.8 + brow_lift])
                    right_brow.set_ydata([0.8 + brow_lift, 0.8 + brow_lift])
                else:
                    # Neutral expression
                    x = np.linspace(-0.4, 0.4, 20)
                    y = np.zeros(20) - 0.8
                    mouth_line.set_data(x, y)
                    left_brow.set_ydata([0.8, 0.8])
                    right_brow.set_ydata([0.8, 0.8])
                
                return mouth_line, left_brow, right_brow
            
            ani = animation.FuncAnimation(fig, animate, interval=50, 
                                        blit=True, repeat=True)
            plt.show()
            
        except Exception as e:
            print(f"Error in advanced animation: {e}")

# Usage Examples
if __name__ == "__main__":
    # Example 1: Simple TTS with basic animation
    print("1. Simple TTS Animation")
    simple_speaker = SimpleAnimatedSpeaker()
    # simple_speaker.speak_with_animation("Hello! I am your animated assistant speaking this text.")
    
    # Example 2: Google TTS with visualization
    print("2. Google TTS Animation")
    gtts_speaker = GTTSAnimatedSpeaker()
    # gtts_speaker.speak_with_gtts("Welcome to the animated text to speech demo!")
    
    # Example 3: Advanced TTS (requires Coqui TTS installation)
    print("3. Advanced TTS Animation")
    advanced_speaker = CoquiTTSAnimatedSpeaker()
    # advanced_speaker.speak_advanced("This is an advanced text to speech system with realistic animation!")
    
    # Interactive demo
    print("\nInteractive Demo:")
    choice = input("Choose method (1-3): ")
    text = input("Enter text to speak: ")
    
    if choice == "1":
        simple_speaker.speak_with_animation(text)
    elif choice == "2":
        gtts_speaker.speak_with_gtts(text)
    elif choice == "3":
        advanced_speaker.speak_advanced(text)
    else:
        print("Invalid choice")