import pygame, numpy, time, random
import functions_test as fc_t

# pygame setup
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                  pygame.display.Info().current_h),
                                  pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 64)

running = True
fc = 0
scaleTest = 0

# testing this useless function
print(fc_t.pixel_to_scale((960, 540)))

while running:
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # render and stuff every frame
    fpsTest = font.render("frame " + str(fc), True, (0, 0, 0))
    fc += 1

    # Blit
    screen.blit(fpsTest, fc_t.scale_to_pixel((scaleTest, scaleTest)))
    scaleTest += 0.001
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60