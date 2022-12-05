import pygame

class ScreenMessage:
    # a class to initialize the final screen
    def __init__(self, position, message, fontsize = 100):
        pygame.init()
        #final message

        self.text_color = (0, 0, 0)
        self.bg_color = (0, 255, 0)
        #creating a message
        self.font = pygame.font.SysFont('Futura', fontsize, bold = True, italic = False)

        self.img = self.font.render(message, True, self.text_color, self.bg_color)

        self.text_rect = self.img.get_rect()
        self.text_rect.center = position

    def display(self, screen):
        #displays the message of losing
        screen.fill((173,3, 46))
        screen.blit(self.img, self.text_rect)


