import pygame
import pyttsx3
import threading
import time
import math

class CartoonCharacter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_speaking = False
        self.mouth_open = False
        self.blink_timer = 0
        self.eye_closed = False
        self.bounce_offset = 0
        self.bounce_speed = 0.1
        
    def update(self):
        # Bouncing animation when speaking
        if self.is_speaking:
            self.bounce_offset = math.sin(pygame.time.get_ticks() * 0.01) * 5
            
        # Blinking animation
        self.blink_timer += 1
        if self.blink_timer > 180:  # Blink every 3 seconds at 60 FPS
            self.eye_closed = True
        if self.blink_timer > 190:
            self.eye_closed = False
            self.blink_timer = 0
    
    def draw(self, screen):
        current_y = self.y + self.bounce_offset
        
        # Draw head (circle)
        pygame.draw.circle(screen, (255, 220, 177), (self.x, int(current_y)), 80)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, int(current_y)), 80, 3)
        
        # Draw eyes
        if not self.eye_closed:
            # Left eye
            pygame.draw.circle(screen, (255, 255, 255), (self.x - 25, int(current_y) - 20), 15)
            pygame.draw.circle(screen, (0, 0, 0), (self.x - 25, int(current_y) - 20), 15, 2)
            pygame.draw.circle(screen, (0, 0, 0), (self.x - 25, int(current_y) - 20), 8)
            
            # Right eye
            pygame.draw.circle(screen, (255, 255, 255), (self.x + 25, int(current_y) - 20), 15)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + 25, int(current_y) - 20), 15, 2)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + 25, int(current_y) - 20), 8)
        else:
            # Closed eyes (lines)
            pygame.draw.line(screen, (0, 0, 0), (self.x - 35, int(current_y) - 20), (self.x - 15, int(current_y) - 20), 3)
            pygame.draw.line(screen, (0, 0, 0), (self.x + 15, int(current_y) - 20), (self.x + 35, int(current_y) - 20), 3)
        
        # Draw nose
        pygame.draw.circle(screen, (255, 200, 150), (self.x, int(current_y) - 5), 5)
        
        # Draw mouth (changes when speaking)
        if self.is_speaking and self.mouth_open:
            # Open mouth (oval)
            pygame.draw.ellipse(screen, (50, 0, 0), (self.x - 15, int(current_y) + 20, 30, 20))
            pygame.draw.ellipse(screen, (0, 0, 0), (self.x - 15, int(current_y) + 20, 30, 20), 2)
        else:
            # Closed mouth (line)
            pygame.draw.line(screen, (0, 0, 0), (self.x - 15, int(current_y) + 25), (self.x + 15, int(current_y) + 25), 3)
        
        # Draw body (simple rectangle)
        pygame.draw.rect(screen, (100, 150, 255), (self.x - 40, int(current_y) + 80, 80, 120))
        pygame.draw.rect(screen, (0, 0, 0), (self.x - 40, int(current_y) + 80, 80, 120), 3)
        
        # Draw arms
        pygame.draw.line(screen, (255, 220, 177), (self.x - 40, int(current_y) + 100), (self.x - 70, int(current_y) + 140), 8)
        pygame.draw.line(screen, (255, 220, 177), (self.x + 40, int(current_y) + 100), (self.x + 70, int(current_y) + 140), 8)

class TextToSpeechApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Animated Cartoon Character - Text to Speech")
        self.clock = pygame.time.Clock()
        
        # Initialize TTS engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speaking speed
        self.tts_engine.setProperty('volume', 0.9)  # Volume level
        
        # Create character
        self.character = CartoonCharacter(400, 200)
        
        # Text input
        self.input_text = ""
        self.font = pygame.font.Font(None, 32)
        
        self.running = True
        
    def animate_mouth(self, duration):
        """Animate mouth movement during speech"""
        start_time = time.time()
        while time.time() - start_time < duration:
            self.character.mouth_open = not self.character.mouth_open
            time.sleep(0.1)  # Mouth movement speed
        self.character.is_speaking = False
        self.character.mouth_open = False
    
    def speak_text(self, text):
        """Convert text to speech and animate character"""
        if not text.strip():
            return
            
        self.character.is_speaking = True
        
        # Estimate speaking duration (rough calculation)
        words = len(text.split())
        duration = words * 0.5  # Approximate 0.5 seconds per word
        
        # Start mouth animation in separate thread
        animation_thread = threading.Thread(target=self.animate_mouth, args=(duration,))
        animation_thread.daemon = True
        animation_thread.start()
        
        # Start TTS in separate thread
        def speak():
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        
        tts_thread = threading.Thread(target=speak)
        tts_thread.daemon = True
        tts_thread.start()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Speak the text when Enter is pressed
                    self.speak_text(self.input_text)
                    self.input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
    
    def draw(self):
        # Clear screen
        self.screen.fill((135, 206, 235))  # Sky blue background
        
        # Draw character
        self.character.draw(self.screen)
        
        # Draw text input box
        input_rect = pygame.Rect(50, 450, 700, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), input_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), input_rect, 2)
        
        # Draw input text
        text_surface = self.font.render(self.input_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        
        # Draw instructions
        instruction_text = "Type your message and press Enter to make the character speak!"
        instruction_surface = pygame.font.Font(None, 24).render(instruction_text, True, (0, 0, 0))
        self.screen.blit(instruction_surface, (50, 420))
        
        # Draw speaking indicator
        if self.character.is_speaking:
            speaking_text = "Speaking..."
            speaking_surface = pygame.font.Font(None, 28).render(speaking_text, True, (255, 0, 0))
            self.screen.blit(speaking_surface, (350, 50))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.character.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()

# Main execution
if __name__ == "__main__":
    # Required installations:
    print("Make sure you have installed the required packages:")
    print("pip install pygame pyttsx3")
    print("\nStarting the application...")
    
    app = TextToSpeechApp()
    app.run()