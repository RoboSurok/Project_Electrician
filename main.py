import pygame
import sys


class MainMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (150, 150, 150)

        self.font_large = pygame.font.Font(None, 55)
        self.font_medium = pygame.font.Font(None, 45)
        self.font_small = pygame.font.Font(None, 35)

        self.levels_text = self.font_medium.render("Выбор уровня", True, self.BLACK)
        self.quit_text = self.font_medium.render("Выход", True, self.BLACK)
        self.reset_profile_text = self.font_small.render("Сбросить профиль", True, self.BLACK)
        self.select_skin_text = self.font_small.render("Выбрать скин", True, self.BLACK)

        self.levels_button = pygame.Rect(self.WIDTH // 2 - 150, self.HEIGHT // 2 - 50, 300, 70)
        self.quit_button = pygame.Rect(self.WIDTH // 2 - 150, self.HEIGHT // 2 + 50, 300, 70)
        self.reset_profile_button = pygame.Rect(self.WIDTH - 250, self.HEIGHT - 70, 240, 50)
        self.select_skin_button = pygame.Rect(10, self.HEIGHT - 70, 200, 50)

    def draw_menu(self):
        self.screen.fill(self.WHITE)

        title_text = self.font_large.render("Electrician", True, self.BLACK)
        self.screen.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 50))

        pygame.draw.rect(self.screen, self.GRAY, self.levels_button)
        pygame.draw.rect(self.screen, self.GRAY, self.quit_button)
        pygame.draw.rect(self.screen, self.GRAY, self.reset_profile_button)
        pygame.draw.rect(self.screen, self.GRAY, self.select_skin_button)

        self.screen.blit(self.levels_text, (self.levels_button.x + 40, self.levels_button.y + 15))
        self.screen.blit(self.quit_text, (self.quit_button.x + 100, self.quit_button.y + 15))
        self.screen.blit(self.reset_profile_text, (self.reset_profile_button.x + 10, self.reset_profile_button.y + 10))
        self.screen.blit(self.select_skin_text, (self.select_skin_button.x + 10, self.select_skin_button.y + 10))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.levels_button.collidepoint(event.pos):
                    pass
                if self.quit_button.collidepoint(event.pos):
                    return False
                if self.reset_profile_button.collidepoint(event.pos):
                    pass
                if self.select_skin_button.collidepoint(event.pos):
                    pass
        return True


if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Главное меню игры")
    menu = MainMenu(screen, WIDTH, HEIGHT)
    running = True
    while running:
        running = menu.handle_events()
        menu.draw_menu()
        pygame.display.flip()
    pygame.quit()
    sys.exit()
