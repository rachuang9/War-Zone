import pygame

class GameOver:
    # a class to initialize the final screen
    def __init__(self, wz_game):
        pygame.init()
        #final message
        self.screen = wz_game.screen
        self.screen_rect = self.screen.get_rect()
        lose_message = 'YOU DIED'
        win_message = 'YOU WIN'
        self.text_color = (0, 0, 0)
        self.bg_color = (0, 255, 0)
        #components of the final message
        self.font = pygame.font.SysFont('Futura', 100, bold = True, italic = False)
        self.lose_img = self.font.render( lose_message, True, self.text_color, self.bg_color)
        self.win_img = self.font.render(win_message, True, self.text_color, self.bg_color)
        self.text_rect = self.lose_img.get_rect()
        self.text_rect.center = self.screen_rect.center

    def display_lose_message(self):
        #displays the message of losing
        self.screen.fill(173,3, 46)
        self.screen.blit(self.lose_img, self.text_rect)

    def display_win_message(self):
        #display message of winning
        self.screen.fill(28, 189, 44)
        self.screen.blit(self.win_img, self.text_color)


