import pygame
import sys
import os
import sqlite3


class Game:
    """Класс для реализации уровней игры"""
    def __init__(self, level_filename, screen, width, height):
        """Инициализация уровня игры"""
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.CELL_SIZE = self.WIDTH // 10
        pygame.display.set_caption("Электрик")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.COPPER = (184, 115, 51)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (150, 150, 150)
        self.SPIKE_COLOR = (255, 165, 0)

        self.level_data = self.load_level(level_filename)

        self.start_pos = self.find_position('S')
        self.end_pos = self.find_position('E')
        self.player_pos = list(self.start_pos)
        self.path = [tuple(self.start_pos)]
        self.obstacles = self.get_obstacles()
        self.spikes = self.get_spikes()
        self.con = sqlite3.connect('data_log.db')
        cur = self.con.cursor()
        self.skin = cur.execute("SELECT skin FROM data_log").fetchall()[0][0]
        cur.close()
        self.player_image = pygame.transform.scale(
            pygame.image.load("images/skins/" + self.skin),
            (self.CELL_SIZE, self.CELL_SIZE))
        self.player_image = pygame.transform.scale(
            self.player_image, (self.CELL_SIZE, self.CELL_SIZE))

    def load_level(self, filename):
        """Загружаем карту уровня"""
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]

    def find_position(self, symbol):
        """Находим позицию символа в уровне (начало или конец)"""
        for y, row in enumerate(self.level_data):
            for x, cell in enumerate(row):
                if cell == symbol:
                    return (x, y)
        return None

    def get_obstacles(self):
        """Находим все стены в уровне"""
        obstacles = []
        for y, row in enumerate(self.level_data):
            for x, cell in enumerate(row):
                if cell == '1':
                    obstacles.append((x, y))
        return obstacles

    def get_spikes(self):
        """Находим все ловушки в уровне"""
        spikes = []
        for y, row in enumerate(self.level_data):
            for x, cell in enumerate(row):
                if cell == 'T':
                    spikes.append((x, y))
        return spikes

    def draw_grid(self):
        """Рисуем сетку"""
        for x in range(0, self.WIDTH, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.BLACK, (x, 0), (x, self.HEIGHT))
        for y in range(0, self.HEIGHT, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.BLACK, (0, y), (self.WIDTH, y))

    def draw_elements(self):
        """Рисуем элементы уровня"""
        self.screen.fill(self.WHITE)
        self.draw_grid()

        for obs in self.obstacles:
            pygame.draw.rect(self.screen,
                             self.GRAY,
                             (obs[0] * self.CELL_SIZE,
                              obs[1] * self.CELL_SIZE,
                              self.CELL_SIZE, self.CELL_SIZE))

        for spike in self.spikes:
            pygame.draw.circle(self.screen, self.SPIKE_COLOR,
                               (spike[0] * self.CELL_SIZE + self.CELL_SIZE // 2,
                                spike[1] * self.CELL_SIZE + self.CELL_SIZE // 2), self.CELL_SIZE // 3)

        pygame.draw.circle(self.screen, self.GREEN, (self.start_pos[0] * self.CELL_SIZE + self.CELL_SIZE // 2,
                                                     self.start_pos[1] * self.CELL_SIZE + self.CELL_SIZE // 2), self.CELL_SIZE // 3)
        pygame.draw.circle(self.screen, self.RED, (self.end_pos[0] * self.CELL_SIZE + self.CELL_SIZE // 2,
                                                   self.end_pos[1] * self.CELL_SIZE + self.CELL_SIZE // 2), self.CELL_SIZE // 3)

        if len(self.path) > 1:
            pygame.draw.lines(self.screen, self.COPPER, False,
                              [(x * self.CELL_SIZE + self.CELL_SIZE // 2, y * self.CELL_SIZE + self.CELL_SIZE // 2) for x, y in self.path], 8)

        self.screen.blit(
            self.player_image,
            (self.player_pos[0] * self.CELL_SIZE,
             self.player_pos[1] * self.CELL_SIZE))

    def move_player(self, dx, dy):
        """Перемещаем игрока"""
        new_pos = (self.player_pos[0] + dx, self.player_pos[1] + dy)

        if 0 <= new_pos[0] < 10 and 0 <= new_pos[1] < 10:
            if new_pos in self.obstacles:
                return

            if new_pos in self.spikes:
                self.show_game_over_message()
                return

            if new_pos in self.path:
                self.path.remove(new_pos)
            else:
                self.path.append(new_pos)

            self.player_pos = list(new_pos)

            if self.player_pos == list(self.end_pos) and len(self.path) > 1:
                self.show_win_message()

    def show_game_over_message(self):
        """Выводим сообщение о проигрыше"""
        font = pygame.font.Font(None, 50)
        text = font.render("Вы погибли!", True, self.RED)
        self.screen.blit(text,
                         (self.WIDTH // 2 - text.get_width() // 2,
                          self.HEIGHT // 2 - text.get_height() // 2))
        cur = self.con.cursor()
        cur.execute('''UPDATE data_log SET lose = lose + 1''')
        self.con.commit()
        cur.close()
        pygame.display.flip()
        pygame.time.delay(2000)
        self.running = False

    def show_win_message(self):
        """Выводим сообщение о победе"""
        font = pygame.font.Font(None, 50)
        text = font.render("Уровень пройден!", True, self.RED)
        self.screen.blit(text,
                         (self.WIDTH // 2 - text.get_width() // 2,
                          self.HEIGHT // 2 - text.get_height() // 2))
        cur = self.con.cursor()
        cur.execute('''UPDATE data_log SET wins = wins + 1''')
        self.con.commit()
        cur.close()
        pygame.display.flip()
        pygame.time.delay(2000)
        self.running = False

    def run(self):
        """Запускаем уровень игры"""
        self.running = True
        while self.running:
            self.draw_elements()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_player(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_player(1, 0)
                    elif event.key == pygame.K_UP:
                        self.move_player(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.move_player(0, 1)


class LevelSelectionMenu:
    """Класс для реализации меню выбора уровня"""
    def __init__(self, screen, width, height):
        """Инициализация меню выбора уровня"""
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height

        self.levels = ["Уровень 1", "Уровень 2", "Уровень 3", "Уровень 4",
                       "Уровень 5", "Уровень 6", "Уровень 7", "Уровень 8",
                       "Уровень 9", "Уровень 10"]
        self.current_level_index = 0

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (180, 180, 180)

        self.background = pygame.transform.scale(
            pygame.image.load("images/level_selection_2.png"), (800, 800))

        self.font_medium = pygame.font.Font(None, 60)

        self.left_button = pygame.Rect(
            50, self.HEIGHT // 2 - 35, 50, 70)
        self.right_button = pygame.Rect(
            self.WIDTH - 100, self.HEIGHT // 2 - 35, 50, 70)
        self.play_button = pygame.Rect(
            self.WIDTH // 2 - 100, self.HEIGHT - 120, 200, 50)
        self.back_button = pygame.Rect(
            self.WIDTH // 2 - 100, self.HEIGHT - 60, 200, 50)

    def draw_menu(self):
        """Постройка меню выбора уровня"""
        self.screen.blit(self.background, (0, 0))

        level_text = self.font_medium.render(
            self.levels[self.current_level_index], True, (self.BLACK))
        self.screen.blit(level_text,
                         (self.WIDTH // 2 - level_text.get_width() // 2,
                          self.HEIGHT // 2 - 25 - 80))

        pygame.draw.rect(self.screen, self.GRAY, self.left_button)
        pygame.draw.rect(self.screen, self.GRAY, self.right_button)
        pygame.draw.rect(self.screen, self.GRAY, self.play_button)
        pygame.draw.rect(self.screen, self.GRAY, self.back_button)

        left_text = self.font_medium.render("<", True, self.BLACK)
        right_text = self.font_medium.render(">", True, self.BLACK)
        play_text = self.font_medium.render("Играть", True, self.BLACK)
        back_text = self.font_medium.render("Назад", True, self.BLACK)

        self.screen.blit(
            left_text, (self.left_button.x + 15, self.left_button.y + 15))
        self.screen.blit(
            right_text, (self.right_button.x + 15, self.right_button.y + 15))
        self.screen.blit(
            play_text, (self.play_button.x + 40, self.play_button.y + 10))
        self.screen.blit(
            back_text, (self.back_button.x + 35, self.back_button.y + 10))

    def handle_events(self):
        """Обработка событий меню выбора уровня"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.left_button.collidepoint(event.pos):
                    self.current_level_index = (
                        self.current_level_index - 1) % len(self.levels)
                if self.right_button.collidepoint(event.pos):
                    self.current_level_index = (
                        self.current_level_index + 1) % len(self.levels)
                if self.play_button.collidepoint(event.pos):
                    level = Game(
                        f"levels/level_{self.current_level_index + 1}.txt",
                        self.screen, self.WIDTH, self.HEIGHT)
                    level.run()
                if self.back_button.collidepoint(event.pos):
                    return False
        return True


class SkinSelectionMenu:
    """Класс для реализации меню выбора скина"""
    def __init__(self, screen, width, height):
        """Инициализация меню выбора скина"""
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height

        self.skins_folder = "images/skins"
        self.skins = [file
                      for file in os.listdir(self.skins_folder)
                      if file.endswith(".png")]
        self.current_skin_index = 0

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (180, 180, 180)

        self.background = pygame.transform.scale(
            pygame.image.load("images/skin_selection.png"),
            (self.WIDTH, self.HEIGHT))

        self.font_medium = pygame.font.Font(None, 45)

        self.left_button = pygame.Rect(
            50, self.HEIGHT // 2 - 35, 50, 70)
        self.right_button = pygame.Rect(
            self.WIDTH - 100, self.HEIGHT // 2 - 35, 50, 70)
        self.select_button = pygame.Rect(
            self.WIDTH // 2 - 100, self.HEIGHT - 120, 200, 50)

    def draw_menu(self):
        """Постройка меню выбора скина"""
        self.screen.blit(self.background, (0, 0))

        title_text = self.font_medium.render("Выбор скина", True, self.BLACK)
        self.screen.blit(title_text,
                         (self.WIDTH // 2 - title_text.get_width() // 2, 50))

        if self.skins:
            skin_image = pygame.image.load(
                os.path.join(self.skins_folder,
                             self.skins[self.current_skin_index]))
            skin_image = pygame.transform.scale(skin_image, (150, 150))
            self.screen.blit(skin_image,
                             (self.WIDTH // 2 - 75, self.HEIGHT // 2 - 75))

        pygame.draw.rect(self.screen, self.GRAY, self.left_button)
        pygame.draw.rect(self.screen, self.GRAY, self.right_button)
        pygame.draw.rect(self.screen, self.GRAY, self.select_button)

        left_text = self.font_medium.render("<", True, self.BLACK)
        right_text = self.font_medium.render(">", True, self.BLACK)
        select_text = self.font_medium.render("Выбрать", True, self.BLACK)

        self.screen.blit(left_text,
                         (self.left_button.x + 15,
                          self.left_button.y + 15))
        self.screen.blit(right_text,
                         (self.right_button.x + 15,
                          self.right_button.y + 15))
        self.screen.blit(select_text,
                         (self.select_button.x + 20,
                          self.select_button.y + 10))

    def handle_events(self):
        """Обработка событий меню выбора скина"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.left_button.collidepoint(event.pos):
                    self.current_skin_index = (
                        self.current_skin_index - 1) % len(self.skins)
                if self.right_button.collidepoint(event.pos):
                    self.current_skin_index = (
                        self.current_skin_index + 1) % len(self.skins)
                if self.select_button.collidepoint(event.pos):
                    con = sqlite3.connect('data_log.db')
                    cur = con.cursor()
                    cur.execute("UPDATE data_log SET skin = ?",
                                (self.skins[self.current_skin_index],))
                    con.commit()
                    cur.close()
                    return False
        return True


class MainMenu:
    """Класс для реализации главного меню игры"""
    def __init__(self, screen, width, height):
        """Инициализация главного меню"""
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

        self.background = pygame.transform.scale(
            pygame.image.load("images/background.png"),
            (self.WIDTH, self.HEIGHT))

        self.levels_text = self.font_medium.render(
            "Выбор уровня", True, self.BLACK)
        self.quit_text = self.font_medium.render(
            "Выход", True, self.BLACK)
        self.reset_profile_text = self.font_small.render(
            "Сбросить профиль", True, self.BLACK)
        self.select_skin_text = self.font_small.render(
            "Выбрать скин", True, self.BLACK)

        self.levels_button = pygame.Rect(
            self.WIDTH // 2 - 150, self.HEIGHT // 2 - 50, 300, 70)

        self.quit_button = pygame.Rect(
            self.WIDTH // 2 - 150, self.HEIGHT // 2 + 50, 300, 70)

        self.reset_profile_button = pygame.Rect(
            self.WIDTH - 250, self.HEIGHT - 70, 240, 50)

        self.select_skin_button = pygame.Rect(
            10, self.HEIGHT - 70, 200, 50)

    def draw_menu(self):
        """Постройка главного меню"""
        self.screen.fill(self.WHITE)

        title_text = self.font_large.render("Электрик", True, self.BLACK)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(title_text,
                         (self.WIDTH // 2 - title_text.get_width() // 2,
                          200))

        pygame.draw.rect(self.screen, self.GRAY, self.levels_button)
        pygame.draw.rect(self.screen, self.GRAY, self.quit_button)
        pygame.draw.rect(self.screen, self.GRAY, self.reset_profile_button)
        pygame.draw.rect(self.screen, self.GRAY, self.select_skin_button)

        self.screen.blit(self.levels_text,
                         (self.levels_button.x + 40,
                          self.levels_button.y + 15))
        self.screen.blit(self.quit_text,
                         (self.quit_button.x + 100,
                          self.quit_button.y + 15))
        self.screen.blit(self.reset_profile_text,
                         (self.reset_profile_button.x + 10,
                          self.reset_profile_button.y + 10))
        self.screen.blit(self.select_skin_text,
                         (self.select_skin_button.x + 10,
                          self.select_skin_button.y + 10))

    def handle_events(self, profile):
        """Обработка событий главного меню"""
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
                        con = sqlite3.connect('data_log.db')
                        cur = con.cursor()
                        cur.execute("DELETE FROM data_log")
                        cur.execute("""INSERT INTO data_log
                                    (skin, wins, lose) VALUES (?, ?, ?)""",
                                    ("skin_first.png", 0, 0))
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
    con = sqlite3.connect('data_log.db')
    cur = con.cursor()
    if cur.execute('SELECT * FROM data_log').fetchall():
        profile = True
    else:
        cur.execute("""INSERT INTO data_log
                    (skin, wins, lose) VALUES (?, ?, ?)""",
                    ("skin_first.png", 0, 0))
        con.commit()
        profile = False
    cur.close()
    pygame.init()
    WIDTH, HEIGHT = 800, 800
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
