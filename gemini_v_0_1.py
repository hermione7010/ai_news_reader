if "__main__" == __name__:
    
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    image = pygame.image.load("sddefault.jpg")
    image_rect = image.get_rect()
    image_rect.x = 100
    image_rect.y = 100

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle key presses for movement (e.g., arrow keys)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    image_rect.x += 5
                # Add more conditions for other directions

        screen.fill((255, 255, 255)) # Fill background
        screen.blit(image, image_rect) # Draw image
        pygame.display.flip() # Update display

    pygame.quit()


    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    import numpy as np

    fig, ax = plt.subplots()
    xdata, ydata = [], []
    ln, = plt.plot([], [], 'ro')

    def init():
        ax.set_xlim(0, 2*np.pi)
        ax.set_ylim(-1, 1)
        return ln,

    def update(frame):
        xdata.append(frame)
        ydata.append(np.sin(frame))
        ln.set_data(xdata, ydata)
        return ln,

    ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                        init_func=init, blit=True)
    plt.show()



    import pyttsx3
    import pygame # For displaying image (optional)

    engine = pyttsx3.init()
    engine.say("Hello, I am a talking image!")
    engine.runAndWait()

    # You could also load and display an image here using Pygame or similar