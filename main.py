import pygame
import sys
import os
import sqlite3


class LevelSelectionMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height

        self.levels = ["Уровень 1", "Уровень 2", "Уровень 3", "Уровень 4", "Уровень 5", 
                       "Уровень 6", "Уровень 7", "Уровень 8", "Уровень 9", "Уровень 10"]
        self.current_level_index = 0

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (180, 180, 180)

        self.font_medium = pygame.font.Font(None, 45)

        self.left_button = pygame.Rect(50, self.HEIGHT // 2 - 35, 50, 70)
        self.right_button = pygame.Rect(self.WIDTH - 100, self.HEIGHT // 2 - 35, 50, 70)
        self.play_button = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT - 120, 200, 50)
        self.back_button = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT - 60, 200, 50)

    def draw_menu(self):
        self.screen.fill(self.WHITE)

        title_text = self.font_medium.render("Выбор уровня", True, self.BLACK)
        self.screen.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 50))

        level_text = self.font_medium.render(self.levels[self.current_level_index], True, self.BLACK)
        self.screen.blit(level_text, (self.WIDTH // 2 - level_text.get_width() // 2, self.HEIGHT // 2 - 25))

        pygame.draw.rect(self.screen, self.GRAY, self.left_button)
        pygame.draw.rect(self.screen, self.GRAY, self.right_button)
        pygame.draw.rect(self.screen, self.GRAY, self.play_button)
        pygame.draw.rect(self.screen, self.GRAY, self.back_button)

        left_text = self.font_medium.render("<", True, self.BLACK)
        right_text = self.font_medium.render(">", True, self.BLACK)
        play_text = self.font_medium.render("Играть", True, self.BLACK)
        back_text = self.font_medium.render("Назад", True, self.BLACK)

        self.screen.blit(left_text, (self.left_button.x + 15, self.left_button.y + 15))
        self.screen.blit(right_text, (self.right_button.x + 15, self.right_button.y + 15))
        self.screen.blit(play_text, (self.play_button.x + 40, self.play_button.y + 10))
        self.screen.blit(back_text, (self.back_button.x + 35, self.back_button.y + 10))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.left_button.collidepoint(event.pos):
                    self.current_level_index = (self.current_level_index - 1) % len(self.levels)
                if self.right_button.collidepoint(event.pos):
                    self.current_level_index = (self.current_level_index + 1) % len(self.levels)
                if self.play_button.collidepoint(event.pos):
                    pass #Вставить вход на уровень
                if self.back_button.collidepoint(event.pos):
                    return False
        return True


class SkinSelectionMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height

        self.skins_folder = "./images/skins"
        self.skins = [file for file in os.listdir(self.skins_folder) if file.endswith(".png")]
        self.current_skin_index = 0

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (180, 180, 180)

        self.font_medium = pygame.font.Font(None, 45)

        self.left_button = pygame.Rect(50, self.HEIGHT // 2 - 35, 50, 70)
        self.right_button = pygame.Rect(self.WIDTH - 100, self.HEIGHT // 2 - 35, 50, 70)
        self.select_button = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT - 120, 200, 50)

    def draw_menu(self):
        self.screen.fill(self.BLACK)

        title_text = self.font_medium.render("Выбор скина", True, self.BLACK)
        self.screen.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 50))

        if self.skins:
            skin_image = pygame.image.load(os.path.join(self.skins_folder, self.skins[self.current_skin_index]))
            skin_image = pygame.transform.scale(skin_image, (150, 150))
            self.screen.blit(skin_image, (self.WIDTH // 2 - 75, self.HEIGHT // 2 - 75))

        pygame.draw.rect(self.screen, self.GRAY, self.left_button)
        pygame.draw.rect(self.screen, self.GRAY, self.right_button)
        pygame.draw.rect(self.screen, self.GRAY, self.select_button)

        left_text = self.font_medium.render("<", True, self.BLACK)
        right_text = self.font_medium.render(">", True, self.BLACK)
        select_text = self.font_medium.render("Выбрать", True, self.BLACK)

        self.screen.blit(left_text, (self.left_button.x + 15, self.left_button.y + 15))
        self.screen.blit(right_text, (self.right_button.x + 15, self.right_button.y + 15))
        self.screen.blit(select_text, (self.select_button.x + 20, self.select_button.y + 10))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.left_button.collidepoint(event.pos):
                    self.current_skin_index = (self.current_skin_index - 1) % len(self.skins)
                if self.right_button.collidepoint(event.pos):
                    self.current_skin_index = (self.current_skin_index + 1) % len(self.skins)
                if self.select_button.collidepoint(event.pos):
                    con = sqlite3.connect('./data_log.db')
                    cur = con.cursor()
                    cur.execute("UPDATE data_log SET skin = ?", (self.skins[self.current_skin_index],))
                    con.commit()
                    cur.close()
                    return False
        return True


class MainMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height

        self.adv_menu_1 = SkinSelectionMenu(screen, width, height)
        self.adv_menu_2 = LevelSelectionMenu(screen, width, height)

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (150, 150, 150)

        self.font_large = pygame.font.Font(None, 55)
        self.font_medium = pygame.font.Font(None, 45)
        self.font_small = pygame.font.Font(None, 35)

        self.background = pygame.transform.scale(pygame.image.load("./images/background.png"), (self.WIDTH, self.HEIGHT))
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
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 50))

        pygame.draw.rect(self.screen, self.GRAY, self.levels_button)
        pygame.draw.rect(self.screen, self.GRAY, self.quit_button)
        pygame.draw.rect(self.screen, self.GRAY, self.reset_profile_button)
        pygame.draw.rect(self.screen, self.GRAY, self.select_skin_button)

        self.screen.blit(self.levels_text, (self.levels_button.x + 40, self.levels_button.y + 15))
        self.screen.blit(self.quit_text, (self.quit_button.x + 100, self.quit_button.y + 15))
        self.screen.blit(self.reset_profile_text, (self.reset_profile_button.x + 10, self.reset_profile_button.y + 10))
        self.screen.blit(self.select_skin_text, (self.select_skin_button.x + 10, self.select_skin_button.y + 10))

    def handle_events(self, profile):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.levels_button.collidepoint(event.pos):
                    choose_level = True
                    while choose_level:
                        choose_level = self.adv_menu_2.handle_events()
                        self.adv_menu_2.draw_menu()
                        pygame.display.flip()

                if self.quit_button.collidepoint(event.pos):
                    return False

                if self.reset_profile_button.collidepoint(event.pos):
                    if profile:
                        con = sqlite3.connect('./data_log.db')
                        cur = con.cursor()
                        cur.execute("DELETE FROM data_log")
                        cur.execute("""INSERT INTO data_log 
                                    (skin, wins) VALUES (?, ?)""", 
                                    ("skin_first", 0))
                        con.commit()
                        cur.close()
                        profile = False

                if self.select_skin_button.collidepoint(event.pos):
                    choose_skin = True
                    while choose_skin:
                        choose_skin = self.adv_menu_1.handle_events()
                        self.adv_menu_1.draw_menu()
                        pygame.display.flip()
        return True


if __name__ == "__main__":
    con = sqlite3.connect('./data_log.db')
    cur = con.cursor()
    if cur.execute('SELECT * FROM data_log').fetchall():
        profile = True
    else:
        cur.execute("""INSERT INTO data_log
                    (skin, wins) VALUES (?, ?)""",
                    ("skin_first", 0))
        con.commit()
        profile = False
    cur.close()
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Главное меню игры")
    menu = MainMenu(screen, WIDTH, HEIGHT)
    running = True
    while running:
        running = menu.handle_events(profile)
        menu.draw_menu()
        pygame.display.flip()
    pygame.quit()
    sys.exit()
