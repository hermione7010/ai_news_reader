import pyttsx3
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from threading import Thread
import time
import tempfile
import os
import pygame

# Method 1: Simple TTS with Basic Animation (WORKING)
class SimpleAnimatedSpeaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.is_speaking = False
        
    def speak_with_animation(self, text):
        print(f"Speaking: {text}")
        # Start speaking in a separate thread
        speak_thread = Thread(target=self._speak, args=(text,))
        speak_thread.daemon = True
        speak_thread.start()
        
        # Create simple mouth animation
        self._animate_mouth()
        
    def _speak(self, text):
        self.is_speaking = True
        self.engine.say(text)
        self.engine.runAndWait()
        self.is_speaking = False
        
    def _animate_mouth(self):
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('black')
        
        # Draw face
        face = plt.Circle((0, 0), 1.5, fill=False, linewidth=3, color='cyan')
        ax.add_patch(face)
        
        # Eyes
        left_eye = plt.Circle((-0.5, 0.3), 0.15, color='white')
        right_eye = plt.Circle((0.5, 0.3), 0.15, color='white')
        left_pupil = plt.Circle((-0.5, 0.3), 0.07, color='black')
        right_pupil = plt.Circle((0.5, 0.3), 0.07, color='black')
        
        ax.add_patch(left_eye)
        ax.add_patch(right_eye)
        ax.add_patch(left_pupil)
        ax.add_patch(right_pupil)
        
        # Mouth (will be animated)
        mouth_line, = ax.plot([], [], 'r-', linewidth=4)
        
        # Title
        ax.text(0, 1.8, 'AI Assistant Speaking', ha='center', fontsize=14, color='white', weight='bold')
        
        def animate(frame):
            if self.is_speaking:
                # Create mouth movement
                mouth_width = 0.3 + 0.3 * np.sin(frame * 0.5)
                mouth_height = 0.15 * np.sin(frame * 0.3)
                x = np.linspace(-mouth_width, mouth_width, 15)
                y = mouth_height * np.sin(np.pi * x / mouth_width) - 0.5
                mouth_line.set_data(x, y)
            else:
                # Closed mouth
                x = np.linspace(-0.2, 0.2, 15)
                y = np.zeros(15) - 0.5
                mouth_line.set_data(x, y)
            return mouth_line,
        
        ani = animation.FuncAnimation(fig, animate, frames=200, 
                                    interval=100, blit=True, repeat=True)
        plt.tight_layout()
        plt.show()

# Method 2: Fixed Google TTS with Animation
class FixedGTTSAnimatedSpeaker:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
    def speak_with_gtts(self, text, lang='en'):
        try:
            import gtts
            print(f"Generating speech: {text}")
            
            # Generate speech
            tts = gtts.gTTS(text=text, lang=lang, slow=False)
            
            # Create temporary file
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, f"tts_audio_{int(time.time())}.mp3")
            
            # Save audio
            tts.save(temp_file)
            print(f"Audio saved to: {temp_file}")
            
            # Verify file exists
            if os.path.exists(temp_file):
                print(f"File size: {os.path.getsize(temp_file)} bytes")
                # Play with animation
                self._play_with_animation(temp_file, text)
            else:
                print("Error: Audio file was not created")
                
        except ImportError:
            print("Google TTS not installed. Install with: pip install gtts")
        except Exception as e:
            print(f"Error in Google TTS: {e}")
    
    def _play_with_animation(self, audio_file, text):
        try:
            # Load and play audio
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Create animation
            self._create_animation(text)
            
        except Exception as e:
            print(f"Error playing audio: {e}")
        finally:
            # Clean up
            try:
                if os.path.exists(audio_file):
                    # Wait a bit before deleting to ensure playback is done
                    time.sleep(1)
                    os.unlink(audio_file)
                    print("Temporary file cleaned up")
            except Exception as e:
                print(f"Could not delete temp file: {e}")
    
    def _create_animation(self, text):
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('navy')
        
        # Character face
        face = plt.Circle((0, 0), 1.5, fill=False, linewidth=3, color='gold')
        ax.add_patch(face)
        
        # Eyes
        left_eye = plt.Circle((-0.5, 0.3), 0.15, color='white')
        right_eye = plt.Circle((0.5, 0.3), 0.15, color='white')
        left_pupil = plt.Circle((-0.5, 0.3), 0.08, color='blue')
        right_pupil = plt.Circle((0.5, 0.3), 0.08, color='blue')
        
        ax.add_patch(left_eye)
        ax.add_patch(right_eye)
        ax.add_patch(left_pupil)
        ax.add_patch(right_pupil)
        
        # Mouth
        mouth_line, = ax.plot([], [], 'red', linewidth=5)
        
        # Display text
        ax.text(0, 1.8, 'Google TTS Speaking', ha='center', fontsize=14, color='white', weight='bold')
        ax.text(0, -1.8, f'"{text[:50]}..."', ha='center', fontsize=10, color='lightgray', style='italic')
        
        frame_count = [0]
        
        def animate(frame):
            frame_count[0] += 1
            
            # Check if music is still playing
            if pygame.mixer.music.get_busy():
                # Animate mouth with realistic movement
                t = frame_count[0] * 0.2
                mouth_width = 0.4 + 0.3 * abs(np.sin(t * 2))
                mouth_height = 0.2 * abs(np.sin(t * 3))
                
                x = np.linspace(-mouth_width, mouth_width, 20)
                y = mouth_height * np.sin(np.pi * x / mouth_width) - 0.5
                mouth_line.set_data(x, y)
            else:
                # Neutral mouth
                x = np.linspace(-0.3, 0.3, 20)
                y = np.zeros(20) - 0.5
                mouth_line.set_data(x, y)
            
            return mouth_line,
        
        ani = animation.FuncAnimation(fig, animate, interval=50, blit=True, repeat=True)
        plt.tight_layout()
        plt.show()

# Method 3: Edge TTS (Alternative to Coqui)
class EdgeTTSAnimatedSpeaker:
    def __init__(self):
        pygame.mixer.init()
        
    def speak_advanced(self, text, voice="en-US-AriaNeural"):
        try:
            import edge_tts
            import asyncio
            
            print(f"Generating advanced speech: {text}")
            
            async def generate_speech():
                communicate = edge_tts.Communicate(text, voice)
                temp_file = os.path.join(tempfile.gettempdir(), f"edge_tts_{int(time.time())}.mp3")
                await communicate.save(temp_file)
                return temp_file
            
            # Generate speech
            audio_file = asyncio.run(generate_speech())
            
            if os.path.exists(audio_file):
                print(f"Edge TTS audio generated: {audio_file}")
                # Play with advanced animation
                self._advanced_animation(audio_file, text)
            else:
                print("Error: Edge TTS file not created")
                
        except ImportError:
            print("Edge TTS not installed. Install with: pip install edge-tts")
        except Exception as e:
            print(f"Error with Edge TTS: {e}")
    
    def _advanced_animation(self, audio_file, text):
        try:
            # Load and play audio
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Create advanced animation
            fig, ax = plt.subplots(figsize=(12, 10))
            ax.set_xlim(-3, 3)
            ax.set_ylim(-3, 3)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_facecolor('black')
            
            # Advanced character
            # Face outline
            face = plt.Circle((0, 0), 2, fill=False, linewidth=4, color='lime')
            ax.add_patch(face)
            
            # Eyes with more detail
            left_eye = plt.Circle((-0.7, 0.5), 0.3, color='white', alpha=0.9)
            right_eye = plt.Circle((0.7, 0.5), 0.3, color='white', alpha=0.9)
            left_pupil = plt.Circle((-0.7, 0.5), 0.15, color='green')
            right_pupil = plt.Circle((0.7, 0.5), 0.15, color='green')
            left_highlight = plt.Circle((-0.65, 0.6), 0.05, color='white')
            right_highlight = plt.Circle((0.75, 0.6), 0.05, color='white')
            
            ax.add_patch(left_eye)
            ax.add_patch(right_eye)
            ax.add_patch(left_pupil)
            ax.add_patch(right_pupil)
            ax.add_patch(left_highlight)
            ax.add_patch(right_highlight)
            
            # Eyebrows
            left_brow, = ax.plot([-1, -0.4], [0.9, 0.9], color='lime', linewidth=4)
            right_brow, = ax.plot([0.4, 1], [0.9, 0.9], color='lime', linewidth=4)
            
            # Nose
            nose, = ax.plot([0, 0], [0.2, -0.2], color='lime', linewidth=3)
            
            # Mouth (animated)
            mouth_line, = ax.plot([], [], color='red', linewidth=6)
            
            # Title and text
            ax.text(0, 2.5, 'Advanced AI Speaker', ha='center', fontsize=16, color='white', weight='bold')
            ax.text(0, -2.7, f'Voice: {voice}', ha='center', fontsize=10, color='gray')
            
            frame_count = [0]
            
            def animate(frame):
                frame_count[0] += 1
                
                if pygame.mixer.music.get_busy():
                    # Complex mouth animation
                    t = frame_count[0] * 0.15
                    
                    # Multiple frequency components for realistic speech
                    base_width = 0.6
                    width_mod = 0.4 * (np.sin(t * 2) + 0.5 * np.sin(t * 5) + 0.3 * np.sin(t * 8))
                    mouth_width = base_width + abs(width_mod)
                    
                    base_height = 0.3
                    height_mod = 0.25 * (np.sin(t * 3) + 0.3 * np.sin(t * 7))
                    mouth_height = base_height * abs(height_mod)
                    
                    # Create mouth shape
                    x = np.linspace(-mouth_width, mouth_width, 25)
                    y = mouth_height * np.sin(np.pi * x / mouth_width) - 0.8
                    mouth_line.set_data(x, y)
                    
                    # Expressive eyebrows
                    brow_lift = 0.15 * np.sin(t * 0.7)
                    left_brow.set_ydata([0.9 + brow_lift, 0.9 + brow_lift])
                    right_brow.set_ydata([0.9 + brow_lift, 0.9 + brow_lift])
                    
                    # Eye movement
                    eye_x = 0.03 * np.sin(t * 0.4)
                    left_pupil.center = (-0.7 + eye_x, 0.5)
                    right_pupil.center = (0.7 + eye_x, 0.5)
                    left_highlight.center = (-0.65 + eye_x, 0.6)
                    right_highlight.center = (0.75 + eye_x, 0.6)
                    
                else:
                    # Neutral expression
                    x = np.linspace(-0.4, 0.4, 25)
                    y = np.zeros(25) - 0.8
                    mouth_line.set_data(x, y)
                    left_brow.set_ydata([0.9, 0.9])
                    right_brow.set_ydata([0.9, 0.9])
                    left_pupil.center = (-0.7, 0.5)
                    right_pupil.center = (0.7, 0.5)
                    left_highlight.center = (-0.65, 0.6)
                    right_highlight.center = (0.75, 0.6)
                
                return mouth_line, left_brow, right_brow
            
            ani = animation.FuncAnimation(fig, animate, interval=30, blit=False, repeat=True)
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"Animation error: {e}")
        finally:
            # Cleanup
            try:
                time.sleep(1)
                if os.path.exists(audio_file):
                    os.unlink(audio_file)
                    print("Advanced TTS file cleaned up")
            except:
                pass

def main():
    print("🎤 AI Text-to-Speech with Animation")
    print("=" * 40)
    
    while True:
        print("\nChoose TTS method:")
        print("1. Simple Offline TTS (Always works)")
        print("2. Google TTS (Requires internet)")
        print("3. Edge TTS Advanced (Requires: pip install edge-tts)")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            text = input("Enter text to speak: ")
            if text.strip():
                speaker = SimpleAnimatedSpeaker()
                speaker.speak_with_animation(text)
        
        elif choice == "2":
            text = input("Enter text to speak: ")
            if text.strip():
                speaker = FixedGTTSAnimatedSpeaker()
                speaker.speak_with_gtts(text)
        
        elif choice == "3":
            text = input("Enter text to speak: ")
            # voice = input("Voice (Enter for default): ").strip()
            voice = None  # Default voice
            if not voice:
                voice = "en-US-AriaNeural"
            if text.strip():
                speaker = EdgeTTSAnimatedSpeaker()
                speaker.speak_advanced(text, voice)
        
        elif choice == "4":
            print("Goodbye! 👋")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    # Quick test of working methods
    print("Testing Simple TTS (Method 1)...")
    simple = SimpleAnimatedSpeaker()
    # simple.speak_with_animation("Hello, this is method 1 working perfectly!")
    
    # Uncomment to test Google TTS
    print("\nTesting Google TTS (Method 2)...")
    gtts = FixedGTTSAnimatedSpeaker()
    gtts.speak_with_gtts("This is the fixed Google TTS version!")
    
    # Interactive mode
    main()