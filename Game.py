import pygame
import shelve
from random import randint

# region Свойства экрана и системы
pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Knight-scroller")
icon = pygame.image.load("picture/icon.png")
pygame.display.set_icon(icon)

default_size = [300, 240]
default_size_troll = [600, 480]


# endregion

class Player:
    def __init__(self, pl_stay):
        self.player_stay = pl_stay
        self.player_speed = 20
        self.player_count = 0
        self.player_collider = pl_stay.get_rect(topleft=(player_x, player_y))
        self.player_health = 100
        self.player_armor = 10
        self.player_damage = 40
        self.player_point = 0
        self.player_lvl = 0
        self.player_act = False
        self.player_walk_right = [
            pygame.transform.scale(
                pygame.image.load("picture/player/player-walk_right/player-walk_right1.png").convert_alpha(),
                default_size),
            pygame.transform.scale(
                pygame.image.load("picture/player/player-walk_right/player-walk_right4.png").convert_alpha(),
                default_size),
            pygame.transform.scale(
                pygame.image.load("picture/player/player-walk_right/player-walk_right8.png").convert_alpha(),
                default_size),
            pygame.transform.scale(
                pygame.image.load("picture/player/player-walk_right/player-walk_right11.png").convert_alpha(),
                default_size)
        ]
        self.player_hit = [
            pygame.transform.scale(pygame.image.load("picture/player/player_hit/player_hit1.png").convert_alpha(),
                                   default_size),
            pygame.transform.scale(pygame.image.load("picture/player/player_hit/player_hit2.png").convert_alpha(),
                                   default_size),
            pygame.transform.scale(pygame.image.load("picture/player/player_hit/player_hit3.png").convert_alpha(),
                                   default_size),
            pygame.transform.scale(pygame.image.load("picture/player/player_hit/player_hit4.png").convert_alpha(),
                                   default_size)
        ]

    def walk(self):
        keys = pygame.key.get_pressed()
        if pygame.mouse.get_pressed()[0] is True or self.player_act:
            self.player_act = True
            screen.blit(self.player_hit[self.player_count], self.player_collider)
            self.count_walk()
            if self.player_count == 3:
                self.hit(enemy_list)
                self.player_act = False
        elif keys[pygame.K_a] and self.player_collider.x > 50:
            self.player_collider.x -= self.player_speed
            screen.blit(self.player_walk_right[self.player_count], self.player_collider)
            self.count_walk()
        elif keys[pygame.K_d] and self.player_collider.x < 950:
            self.player_collider.x += self.player_speed
            screen.blit(self.player_walk_right[self.player_count], self.player_collider)
            self.count_walk()
        else:
            self.player_count = 0
            screen.blit(player_stay, self.player_collider)

    def count_walk(self):
        if self.player_count == 3:
            self.player_count = 0
        else:
            self.player_count += 1
        return self.player_count

    def hit(self, enemy_hit):
        for (index, el) in enumerate(enemy_hit):
            if self.player_collider.colliderect(el.enemy_collider):
                el.enemy_health -= self.player_damage - el.enemy_armor
                if el.enemy_health <= 0:
                    self.player_point += el.enemy_point
                    enemy_list.pop(index)

    def restart_but(self):
        self.player_health = 100
        enemy_list.clear()
        self.player_collider = player_stay.get_rect(topleft=(player_x, player_y))
        self.player_point = 0
        self.player_lvl = 0

    def info(self):
        print_text(f"ХП: {self.player_health}", 30, 30)
        print_text(f"Уровень: {self.player_lvl + 1}", 400, 30)
        print_text(f"Очки: {self.player_point}", 900, 30)


# region Инициализация игрока
player_stay = pygame.transform.scale(pygame.image.load("picture/player/Player.png").convert_alpha(),
                                     default_size)
player_x = 490
player_y = 450
player_object = Player(player_stay)


# endregion


class Enemy:
    def __init__(self, enemy_stay, enemy_speed, enemy_count, enemy_collider,
                 enemy_health, enemy_armor, enemy_damage, enemy_point, enemy_act, enemy_walk_left, enemy_hit):
        self.enemy_stay = enemy_stay
        self.enemy_speed = enemy_speed
        self.enemy_count = enemy_count
        self.enemy_collider = enemy_collider
        self.enemy_health = enemy_health
        self.enemy_armor = enemy_armor
        self.enemy_damage = enemy_damage
        self.enemy_point = enemy_point
        self.enemy_act = enemy_act
        self.enemy_walk_left = enemy_walk_left
        self.enemy_hit = enemy_hit

    def walk(self, pl_object):
        if self.enemy_act:
            screen.blit(self.enemy_hit[self.enemy_count], self.enemy_collider)
            self.count_walk()
            if self.enemy_count == 0:
                self.hit(pl_object)
                self.enemy_act = False
        elif self.enemy_collider.colliderect(pl_object.player_collider.topleft, (130, 240)):
            self.enemy_collider.x += self.enemy_speed
            screen.blit(self.enemy_walk_left[self.enemy_count], self.enemy_collider)
        elif self.enemy_collider.colliderect(pl_object.player_collider.topleft, (150, 240)):
            self.enemy_count = 0
            self.enemy_act = True
            screen.blit(self.enemy_stay, self.enemy_collider)
        else:
            self.enemy_collider.x -= self.enemy_speed
            screen.blit(self.enemy_walk_left[self.enemy_count], self.enemy_collider)
        if not self.enemy_act:
            self.count_walk()

    def count_walk(self):
        if self.enemy_count == 3:
            self.enemy_count = 0
        else:
            self.enemy_count += 1
        return self.enemy_count

    def hit(self, pl_object):
        if self.enemy_collider.colliderect(pl_object.player_collider.topleft,
                                           (150, 240)):
            pl_object.player_health -= self.enemy_damage - pl_object.player_armor


# region Инициализация противников
orc1_stay = pygame.transform.scale(pygame.image.load("picture/enemy/orc1/orc.png").convert_alpha(),
                                   default_size)
troll_stay = pygame.transform.scale(pygame.image.load("picture/enemy/troll/troll_stay.png").convert_alpha(),
                                    default_size_troll)
pirate_stay = pygame.transform.scale(pygame.image.load("picture/enemy/pirate/pirate_stay.png").convert_alpha(),
                                     default_size)
orc1_x = 1300
orc1_y = 450
troll_y = 200
# endregion

lvl_bg = [
    pygame.image.load("picture/background/1.png").convert_alpha(),
    pygame.image.load("picture/background/2.png").convert_alpha(),
    pygame.image.load("picture/background/3.png").convert_alpha()
]
enemy_list = []


class Button:
    def __init__(self, width, height, inactive_color=(0, 53, 176), active_color=(28, 54, 217), border_radius=10):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.border_radius = border_radius

    def draw_but(self, x, y, words_input, actions=None):
        if x < pygame.mouse.get_pos()[0] < x + self.width and y < pygame.mouse.get_pos()[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height),
                             border_radius=self.border_radius)
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.time.delay(300)
                if actions is not None:
                    actions()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height),
                             border_radius=self.border_radius)

        print_text(words_input, x + 10, y + 10)


# region Функции
def print_text(words_input, x, y, font_type="fonts/PressStart2P-Regular.ttf", font_color=(255, 255, 255), font_size=40):
    font = pygame.font.Font(font_type, font_size)
    text = font.render(words_input, False, font_color)
    screen.blit(text, (x, y))


def pause():
    time_pause = True
    while time_pause:
        print_text("Нажмите Enter чтобы продолжить игру", 300, 250, font_size=20)
        print_text("Нажмите Q чтобы выйти в меню", 300, 300, font_size=20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            time_pause = False
        if pygame.key.get_pressed()[pygame.K_q]:
            main_menu()
        pygame.display.update()
        clock.tick(40)


def main_menu():
    pygame.mixer.stop()
    player_object.restart_but()
    menu_bg = pygame.image.load("picture/background/main_menu.png").convert_alpha()
    background_sound = pygame.mixer.Sound("sound/Lost Kingdom (Piano Menu).wav")
    background_sound.play(-1)
    active_color = (27, 153, 207)
    inactiv_color = (26, 184, 43)
    start_game_but = Button(255, 60, inactive_color=inactiv_color, active_color=active_color)
    table_records_but = Button(660, 60, inactive_color=inactiv_color, active_color=active_color)
    exit_but = Button(215, 60, inactive_color=inactiv_color, active_color=active_color)

    show_menu = True
    while show_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(menu_bg, (0, 0))
        start_game_but.draw_but(500, 420, "Начать", start_game)
        table_records_but.draw_but(300, 520, "Таблица рекордов", table_record)
        exit_but.draw_but(510, 620, "Выйти", exit_game)
        pygame.display.update()


def start_game():
    pygame.mixer.stop()
    background_sound = pygame.mixer.Sound("sound/Final Struggle (Boss Theme).wav")
    background_sound.play(-1)
    game = True
    lvl_size = 3
    lvl_size_spawn = 0
    while game:
        pygame.display.update()
        screen.blit(lvl_bg[player_object.player_lvl % 3], (0, 0))

        if player_object.player_health > 0:
            player_object.info()
            player_object.walk()
            if enemy_list:
                for el in enemy_list:
                    el.walk(player_object)
        else:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == enemy_spawn:
                if lvl_size_spawn < lvl_size:
                    lvl_size_spawn += 1
                    spawn()
                elif lvl_size_spawn >= lvl_size and len(enemy_list) == 0:
                    player_object.player_lvl += 1
                    lvl_size_spawn = 0
                    lvl_size += 3
                break
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] and player_object.player_health > 0:
                pause()

        clock.tick(10)
    game_over()


def spawn():
    rand_end = 2
    if player_object.player_lvl < 3:
        rand_end = player_object.player_lvl % 3
    enemy_number = randint(0, rand_end)
    if enemy_number == 0:
        enemy_list.append(Enemy(orc1_stay, 20, 0, orc1_stay.get_rect(topleft=(orc1_x, player_y)), 100, 0, 20, 20, False,
                                [pygame.transform.scale(pygame.image.load(
                                    "picture/enemy/orc1/orc1_walk_left/orc1_walk_left1.png").convert_alpha(),
                                                        default_size),
                                 pygame.transform.scale(pygame.image.load(
                                     "picture/enemy/orc1/orc1_walk_left/orc1_walk_left2.png").convert_alpha(),
                                                        default_size),
                                 pygame.transform.scale(pygame.image.load(
                                     "picture/enemy/orc1/orc1_walk_left/orc1_walk_left3.png").convert_alpha(),
                                                        default_size),
                                 pygame.transform.scale(pygame.image.load(
                                     "picture/enemy/orc1/orc1_walk_left/orc1_walk_left4.png").convert_alpha(),
                                                        default_size)],

                                [pygame.transform.scale(
                                    pygame.image.load("picture/enemy/orc1/orc1_hit/orc1_hit1.png").convert_alpha(),
                                    default_size),
                                    pygame.transform.scale(pygame.image.load(
                                        "picture/enemy/orc1/orc1_hit/orc1_hit2.png").convert_alpha(),
                                                           default_size),
                                    pygame.transform.scale(pygame.image.load(
                                        "picture/enemy/orc1/orc1_hit/orc1_hit3.png").convert_alpha(),
                                                           default_size),
                                    pygame.transform.scale(pygame.image.load(
                                        "picture/enemy/orc1/orc1_hit/orc1_hit4.png").convert_alpha(),
                                                           default_size)]))
    elif enemy_number == 1:
        enemy_list.append(
            Enemy(pirate_stay, 20, 0, pirate_stay.get_rect(topleft=(orc1_x, player_y)), 100, 10, 30, 30, False,
                  [pygame.transform.scale(pygame.image.load(
                      "picture/enemy/pirate/pirate_walk_left/pirate_walk_left1.png").convert_alpha(),
                                          default_size),
                   pygame.transform.scale(pygame.image.load(
                       "picture/enemy/pirate/pirate_walk_left/pirate_walk_left2.png").convert_alpha(),
                                          default_size),
                   pygame.transform.scale(pygame.image.load(
                       "picture/enemy/pirate/pirate_walk_left/pirate_walk_left3.png").convert_alpha(),
                                          default_size),
                   pygame.transform.scale(pygame.image.load(
                       "picture/enemy/pirate/pirate_walk_left/pirate_walk_left4.png").convert_alpha(),
                                          default_size)],

                  [pygame.transform.scale(
                      pygame.image.load("picture/enemy/pirate/pirate_hit/pirate_hit1.png").convert_alpha(),
                      default_size),
                      pygame.transform.scale(
                          pygame.image.load("picture/enemy/pirate/pirate_hit/pirate_hit2.png").convert_alpha(),
                          default_size),
                      pygame.transform.scale(
                          pygame.image.load("picture/enemy/pirate/pirate_hit/pirate_hit3.png").convert_alpha(),
                          default_size),
                      pygame.transform.scale(
                          pygame.image.load("picture/enemy/pirate/pirate_hit/pirate_hit4.png").convert_alpha(),
                          default_size)]))

    elif enemy_number == 2:
        enemy_list.append(
            Enemy(troll_stay, 20, 0, troll_stay.get_rect(topleft=(orc1_x, troll_y)), 200, 0, 40, 40, False,
                  [pygame.transform.scale(pygame.image.load(
                      "picture/enemy/troll/troll_walk_left/troll_walk_left1.png").convert_alpha(),
                                          default_size_troll),
                   pygame.transform.scale(pygame.image.load(
                       "picture/enemy/troll/troll_walk_left/troll_walk_left2.png").convert_alpha(),
                                          default_size_troll),
                   pygame.transform.scale(pygame.image.load(
                       "picture/enemy/troll/troll_walk_left/troll_walk_left3.png").convert_alpha(),
                                          default_size_troll),
                   pygame.transform.scale(pygame.image.load(
                       "picture/enemy/troll/troll_walk_left/troll_walk_left4.png").convert_alpha(),
                                          default_size_troll)],

                  [pygame.transform.scale(
                      pygame.image.load("picture/enemy/troll/troll_hit/troll_hit1.png").convert_alpha(),
                      default_size_troll),
                      pygame.transform.scale(
                          pygame.image.load("picture/enemy/troll/troll_hit/troll_hit2.png").convert_alpha(),
                          default_size_troll),
                      pygame.transform.scale(
                          pygame.image.load("picture/enemy/troll/troll_hit/troll_hit3.png").convert_alpha(),
                          default_size_troll),
                      pygame.transform.scale(
                          pygame.image.load("picture/enemy/troll/troll_hit/troll_hit4.png").convert_alpha(),
                          default_size_troll)]))


def game_over():
    pygame.mixer.stop()
    background_sound = pygame.mixer.Sound("sound/Heartbreaking.mp3")
    background_sound.play(-1)
    over_bg = pygame.image.load("picture/background/game_over.png").convert_alpha()
    active_color = (27, 153, 207)
    inactiv_color = (26, 184, 43)
    color_text = (19, 2, 161)
    input_need = True
    input_text = "Player"
    s = ""
    score = player_object.player_point
    while True:
        screen.blit(over_bg, (0, 0))
        print_text("Введите своё имя и нажмите Enter,", 150, 50, font_size=30, font_color=color_text)
        print_text("чтобы сохранить результат", 250, 100, font_size=30, font_color=color_text)
        print_text(f"Ваши очки: {score}", 400, 410)
        print_text("Вы проиграли!", 400, 340)
        if player_object.player_health <= 0:
            player_object.restart_but()
        game_over_but = Button(530, 60, inactive_color=inactiv_color, active_color=active_color)
        game_over_but.draw_but(360, 500, "Начать заново", start_game)
        menu_but = Button(175, 60, inactive_color=inactiv_color, active_color=active_color)
        menu_but.draw_but(550, 600, "Меню", main_menu)

        for event in pygame.event.get():
            if event.type == pygame.KEYUP and input_need:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 10:
                        s += event.unicode
                        if s.isalnum():
                            input_text += s
                            s = ""
                        else:
                            s = ""
                if event.key == pygame.K_RETURN and len(input_text) > 0:
                    scores_table = shelve.open("score.db")
                    if input_text in scores_table:
                        if score > scores_table[f"{input_text}"]:
                            scores_table[f"{input_text}"] = score
                    else:
                        scores_table[f"{input_text}"] = score
                    scores_table.close()
                    input_need = False

        if not input_need:
            print_text("Ок", 900, 240, font_color=color_text)
        x = 640 - len(input_text) * 20
        pygame.draw.rect(screen, color_text, (x - 20, 220, 70 + len(input_text) * 37, 80), border_radius=10)
        pygame.draw.rect(screen, (140, 180, 200), (x - 10, 230, 50 + len(input_text) * 37, 60),
                         border_radius=10)
        print_text(input_text, x, 240)
        pygame.display.update()


def table_record():
    color_text = (19, 2, 161)
    record_bg = pygame.image.load("picture/background/table_record.png").convert_alpha()
    score_bool = True
    screen.blit(record_bg, (0, 0))
    y = 100
    i = 0
    scores_table = shelve.open("score.db")
    scores_temporary = sorted(scores_table.items(), key=lambda x: x[1], reverse=True)
    scores_table = dict(scores_temporary)
    print_text("Таблица рекордов", 350, 30, font_color=color_text)
    print_text("Имя игрока", 100, 100, font_color=color_text)
    print_text("Очки", 1000, 100, font_color=color_text)
    for item in scores_table.items():
        y += 70
        print_text(f"{item[0]}", 100, y, font_color=color_text)
        print_text(f"{item[1]}", 1000, y, font_color=color_text)
        if i == 4:
            break
        i += 1

    while score_bool:
        print_text("Нажмите Escape для возвращения в меню", 70, 600, font_size=30, font_color=color_text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                return
        pygame.display.update()
        clock.tick(40)


def exit_game():
    pygame.quit()
    quit()


# endregion

enemy_spawn = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_spawn, 3000)

main_menu()