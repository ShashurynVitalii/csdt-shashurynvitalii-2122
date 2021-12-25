import pygame
from automatic_player import *
from visible_board import *
from person_player import *
from stats import *
from client.serial_connection import *
from util import *
import time
import random
import queue

config, PLAYER_NAME = read_config_xml("config.xml")

FPS = config[0]
HEIGHT = config[1]
WIDTH = config[2]
BORDER_WIDTH = config[3]
BORDER_HEIGHT = config[4]
REQ_SHIP_SIZE = config[5]
MAX_SCORE = config[6]
MOUSE_POS_X = config[7]
MOUSE_POS_Y = config[8]
RESTRICT_X = config[9]
RESTRICT_Y = config[10]
MARGIN = config[11]
SIZE = config[12]
P_SHIPS = []


class Start(pygame.sprite.Sprite):
    """
    Start(controller) utilizes all the\
    object classes of the game.
    NOTE: This follows the MVC architecture design protocols
    as this class also represents the view part and controller of MVC.
    """

    def __init__(self, auto, person, stats, vboard, vb_auto, vb_player, p_ships):
        super(Start, self).__init__()
        self.auto = auto
        self.ai_hunt_queue = queue.Queue()
        self.stats = stats
        self.person = person
        self.vboard = vboard
        self.vb_auto = vb_auto
        self.vb_player = vb_player
        self.win = (False, "")
        self.player1_score = 0  # human player is player 1
        self.player2_score = 0  # computer is player 2
        self.turns = (
            0  # 0 means the human player turn to play, 1 means its the computers turn.
        )
        self.p_ships = p_ships
        self.guesses = 0
        self.server_data = ""

    def set_auto_ships(self):
        ships = self.auto.set_battleships()
        for enemy_ships in ships:
            self.vb_auto.add_ship(
                enemy_ships[0],
                enemy_ships[1],
                enemy_ships[2],
                enemy_ships[3],
                enemy_ships[4],
            )

    def set_person_ships(self):
        ships = self.p_ships
        for person_ships in ships:
            self.vb_player.add_ship(
                person_ships[0],
                person_ships[1],
                person_ships[2],
                person_ships[3],
                person_ships[4],
            )

    def play_ai(self):
        """
        Let's the computer player
        to be able to guess the human player's ship
        with use of Hunt algorithm
        """
        pos = ()
        if self.ai_hunt_queue.empty():
            pos = self.auto.guess_location()
        else:
            pos = self.ai_hunt_queue.get()
        send_serial_data(pos)
        if (0 <= pos[0] <= 9) and (0 <= pos[1] <= 9):
            no_go = self.update(self.vb_player, pos[0], pos[1])
            if no_go == None:
                no_go = []
            if no_go != []:
                self.player2_score = self.player2_score + 1
                if self.vb_player.status[pos[0] + 1][pos[1]] == 0:
                    self.ai_hunt_queue.put((pos[0] + 1, pos[1]))
                if self.vb_player.status[pos[0] - 1][pos[1]] == 0:
                    self.ai_hunt_queue.put((pos[0] - 1, pos[1]))
                if self.vb_player.status[pos[0]][pos[1] + 1] == 0:
                    self.ai_hunt_queue.put((pos[0], pos[1] + 1))
                if self.vb_player.status[pos[0]][pos[1] - 1] == 0:
                    self.ai_hunt_queue.put((pos[0], pos[1] - 1))
            self.auto.avoid_plots(no_go)

    def update(self, obj, coord_x, coord_y):
        """
        updates the screen based on
        guesses made by the human player or the computer player

        obj: represents an object that can either be an human player
        or the computer player.
        coord_x: coordinate for the row
        coor_y: coordinate for the column

        returns moves made.
        """
        no_go = obj.viewable_move(coord_x, coord_y)
        return no_go

    def display_score(self):
        font = pygame.font.SysFont("'couriernew'", 19)
        mess_1 = f"{PLAYER_NAME} score: "
        mess_2 = "Computer score: "
        mess_3 = str(self.player1_score)
        mess_4 = str(self.player2_score)
        txt1 = font.render(mess_1, False, (0, 128, 0))
        txt2 = font.render(mess_2, False, (0, 128, 0))
        txt3 = font.render(mess_3, False, (0, 128, 0))
        txt4 = font.render(mess_4, False, (0, 128, 0))
        self.vboard.blit(txt1, (520, 100))
        self.vboard.blit(txt2, (120, 100))
        pygame.draw.rect(self.vboard, (0, 0, 0), pygame.Rect(670, 100, 30, 20))
        self.vboard.blit(txt3, (670, 100))
        pygame.draw.rect(self.vboard, (0, 0, 0), pygame.Rect(300, 100, 30, 20))
        self.vboard.blit(txt4, (300, 100))

    def set_border(self):
        pygame.draw.rect(self.vboard, BLUE, pygame.Rect(35, 10, 745, 465), 3)

    def display_stats(self):
        font = pygame.font.SysFont("'couriernew'", 19)
        mess_1 = "Number of ships: "
        mess_2 = "Remaining ships: "
        mess_3 = "Numbers of guesses:"
        mess_4 = str(self.guesses)
        txt1 = font.render(mess_1, False, (0, 127, 0))
        txt2 = font.render(mess_2, False, (0, 127, 0))
        txt3 = font.render(mess_3, False, (0, 127, 0))
        txt4 = font.render(mess_4, False, (0, 127, 0))
        play_score_msg1 = font.render(
            "{} - {}".format(PLAYER_NAME, MAX_SCORE), False, (0, 127, 0)
        )
        play_score_msg2 = font.render(
            "Computer - {}".format(MAX_SCORE), False, (0, 127, 0)
        )
        play_score_msg3 = font.render(
            "{} - {}".format(PLAYER_NAME, MAX_SCORE - self.player2_score),
            False,
            (0, 127, 0),
        )
        play_score_msg4 = font.render(
            "Computer - {}".format(MAX_SCORE - self.player1_score), False, (0, 127, 0)
        )
        self.vboard.blit(txt1, (790, 100))
        self.vboard.blit(txt2, (790, 200))
        self.vboard.blit(txt3, (790, 300))
        pygame.draw.rect(self.vboard, (0, 0, 0), pygame.Rect(790, 330, 40, 20))
        self.vboard.blit(txt4, (790, 330))
        self.vboard.blit(play_score_msg1, (790, 130))
        self.vboard.blit(play_score_msg2, (790, 160))
        pygame.draw.rect(self.vboard, (0, 0, 0), pygame.Rect(790, 230, 80, 20))
        self.vboard.blit(play_score_msg3, (790, 230))
        pygame.draw.rect(self.vboard, (0, 0, 0), pygame.Rect(790, 260, 130, 20))
        self.vboard.blit(play_score_msg4, (790, 260))

    def quit(self):
        pygame.quit()
        sys.exit()


class MainMenu:
    def __init__(self, player_board):
        self.player_board = player_board

    def display_menu(self):
        title = pygame.font.SysFont("'couriernew'", 40)
        font = pygame.font.SysFont("'couriernew'", 19)
        font.set_bold(True)
        main_title = title.render("Sea Battle Game", True, (0, 128, 0))
        self.player_board.blit(main_title, (315, 40))
        txt1 = font.render("1 - Start new game", True, (0, 128, 0))
        txt2 = font.render("ESC - Exit", True, (0, 128, 0))
        self.player_board.blit(txt1, (390, 150))
        self.player_board.blit(txt2, (440, 250))


class Begin:
    def __init__(self, player_board, user_board, person):
        self.player_board = player_board
        self.user_board = user_board
        self.person = person
        self.required_ships = [
            5,
            4,
            3,
            2,
            1,
        ]  # numbers of ships(5 ships) needed to play the game.
        self.num_set_ships = 0

    def show_required(self, color, index):
        x = 5
        for row in range(5):
            for column in range(x):
                if index == x:
                    pygame.draw.rect(
                        self.player_board,
                        color,
                        pygame.Rect(
                            800 + (REQ_SHIP_SIZE * column),
                            200 + (REQ_SHIP_SIZE * row),
                            30,
                            30,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.player_board,
                        WHITE,
                        pygame.Rect(
                            800 + (REQ_SHIP_SIZE * column),
                            200 + (REQ_SHIP_SIZE * row),
                            30,
                            30,
                        ),
                    )
            x -= 1

    def set_player_ships(self, x_head, y_head, battleship_length):
        person = self.person.set_battleship(x_head, y_head, battleship_length)
        if len(person) > 0:
            person_ships = person[-1]
            self.user_board.add_ship(
                person_ships[0],
                person_ships[1],
                person_ships[2],
                person_ships[3],
                person_ships[4],
            )
            P_SHIPS.append(
                (
                    person_ships[0],
                    person_ships[1],
                    person_ships[2],
                    person_ships[3],
                    person_ships[4],
                )
            )

    def display_info(self):
        title = pygame.font.SysFont("'couriernew'", 40)
        font = pygame.font.SysFont("'couriernew'", 19)
        font.set_bold(True)
        main_title = title.render("Preparation for the game", True, (0, 128, 0))
        self.player_board.blit(main_title, (110, 40))
        txt1 = font.render("- Set battleship locations", True, (0, 128, 0))
        txt2 = font.render("- Press any key to start game", True, (0, 128, 0))
        self.player_board.blit(txt1, (50, 150))
        self.player_board.blit(txt2, (50, 250))
        font = pygame.font.SysFont("couriernew", 17)
        mess_1 = "Required ships: "
        font.set_bold(True)
        txt1 = font.render(mess_1, True, (0, 127, 0))
        self.player_board.blit(txt1, (800, 150))

    def update(self, human_player, coord_x, coord_y):
        human_player.viewable_move(coord_x, coord_y)

    def set_border(self):
        pygame.draw.rect(
            self.player_board,
            BLUE,
            pygame.Rect(10, 10, HEIGHT - BORDER_WIDTH, WIDTH - BORDER_HEIGHT),
            3,
        )


def run_menu():
    pygame.init()
    DISPLAY = pygame.display.set_mode((1000, 500), 0, 32)
    DISPLAY.fill(BLACK)
    pygame.display.set_caption("SeaBattleGame")

    menu = MainMenu(DISPLAY)
    menu.display_menu()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    run = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    pass
        pygame.display.update()


def run_preparation():
    pygame.init()
    DISPLAY = pygame.display.set_mode((1000, 500), 0, 32)
    DISPLAY.fill(BLACK)
    pygame.display.set_caption("SeaBattleGame")
    user_board = VisibleUserBoard(DISPLAY)
    person = PersonPlayer()

    begin = Begin(DISPLAY, user_board, person)
    begin.display_info()
    begin.set_border()
    begin.show_required(WHITE, 0)

    begin.num_set_ships = 0  # numbers of battleship bricks can not be more than 15

    def mouse_event(event, start, size):
        """
        handle mouse events and ensures mouse clicks
        only works on the grid coordinates.
        start: The object or present screen.
        size: Size of a single brick coordinate.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if (
                MOUSE_POS_X <= mouse_pos[0] <= RESTRICT_X
                and MOUSE_POS_Y <= mouse_pos[1] <= RESTRICT_Y
            ):
                col = mouse_pos[0] - MOUSE_POS_X
                rw = mouse_pos[1] - MOUSE_POS_Y
                column = col // (size + MARGIN)
                row = rw // (size + MARGIN)
                if len(begin.required_ships) > 0:
                    begin.set_player_ships(column, row, begin.required_ships[0])
                    popped_val = begin.required_ships.pop(0)
                    begin.show_required(RED, popped_val)
                    begin.num_set_ships += 1
            else:
                pass

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and begin.num_set_ships >= 5:
                run = False
            elif event.type == pygame.constants.USEREVENT:
                pass
            n_event = mouse_event(event, begin, 30)  # called the mouse event function
        pygame.display.update()


if __name__ == "__main__":

    def mouse_event(mouse_pos, start):
        """
        handle mouse events and ensures mouse clicks
        only works on the grid coordinates.
        start: The object or present screen.
        """
        if (
            REQ_SHIP_SIZE <= mouse_pos[0] <= (RESTRICT_X - 390)
            and MOUSE_POS_Y <= mouse_pos[1] <= RESTRICT_Y
        ):
            col = mouse_pos[0] - REQ_SHIP_SIZE
            rw = mouse_pos[1] - MOUSE_POS_Y
            column = col // (SIZE + MARGIN)
            row = rw // (SIZE + MARGIN)
            no_go = start.update(start.vb_auto, column, row)
            if no_go != None and no_go != []:
                start.player1_score = start.player1_score + 1
            start.guesses += 1
            start.turns = 1

    stats = Stats()
    auto = AutomaticPlayer()
    person = PersonPlayer()
    run_menu()
    run_preparation()

    start_time = time.process_time()

    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    DISPLAY = pygame.display
    main_board = DISPLAY.set_mode((HEIGHT, WIDTH), 0, 32)
    main_board.fill(BLACK)
    DISPLAY.set_caption("SeaBattleGame")
    user_board = VisibleUserBoard(main_board)
    enemy_board = VisibleEnemyBoard(main_board)

    start = Start(auto, person, stats, main_board, enemy_board, user_board, P_SHIPS)
    start.set_auto_ships()
    start.set_border()
    start.set_person_ships()
    win = 0  # end game if equal to 1

    running = True
    while running:
        while True:
            try:
                start.server_data = get_serial_data(
                    SERVER_ROOT["start"], SERVER_ROOT["end"], start.server_data
                )
                break
            except Exception as e:
                if str(e)[:14] == "ClearCommError":
                    pygame.quit()
                    print("Can't find port")
                    sys.exit()
                continue
        for event in pygame.event.get():
            start.display_score()
            start.display_stats()
            if event.type == QUIT:
                start.quit()
            elif event.type == pygame.constants.USEREVENT:
                pass
            if win == 0 and start.server_data == "GAME_UPDATE":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    send_serial_data(mouse_pos)
                    if start.turns == 0:
                        m_event = mouse_event(mouse_pos, start)
                        if start.vb_auto.all_ships_sunk():
                            pygame.draw.rect(
                                start.vboard, BLACK, pygame.Rect(315, 80, 40, 40)
                            )

                            pygame.draw.rect(
                                start.vboard, BLACK, pygame.Rect(680, 80, 40, 40)
                            )

                            pygame.draw.rect(
                                start.vboard, BLACK, pygame.Rect(800, 230, 300, 30)
                            )

                            start.display_score()
                            start.display_stats()
                            title = pygame.font.SysFont("'couriernew'", 40)
                            title.set_bold(True)
                            main_title = title.render(
                                f"{PLAYER_NAME} wins!", True, (0, 128, 0)
                            )
                            main_board.blit(main_title, (250, 40))
                            start.display_score()
                            start.display_stats()
                            win = 1
                            end_time = time.process_time()
                            write_results_xml(
                                f"{PLAYER_NAME}",
                                f"{end_time - start_time:.2f}",
                                f"{start.guesses}",
                                f"{start.player1_score}",
                                f"{start.player2_score}",
                            )
                        pygame.draw.rect(
                            start.vboard, BLACK, pygame.Rect(960, 300, 40, 40)
                        )

                    else:
                        start.play_ai()
                        if start.vb_player.all_ships_sunk():
                            pygame.draw.rect(
                                start.vboard, BLACK, pygame.Rect(315, 80, 40, 40)
                            )

                            pygame.draw.rect(
                                start.vboard, BLACK, pygame.Rect(680, 80, 40, 40)
                            )

                            pygame.draw.rect(
                                start.vboard, BLACK, pygame.Rect(800, 230, 300, 30)
                            )

                            start.display_score()
                            start.display_stats()
                            title = pygame.font.SysFont("'couriernew'", 40)
                            title.set_bold(True)
                            main_title = title.render(
                                "Computer wins!", True, (0, 128, 0)
                            )
                            main_board.blit(main_title, (195, 40))
                            start.display_score()
                            start.display_stats()
                            win = 1
                            end_time = time.process_time()
                            write_results_xml(
                                "Computer",
                                f"{end_time - start_time:.2f}",
                                f"{start.guesses}",
                                f"{start.player1_score}",
                                f"{start.player2_score}",
                            )
                        pygame.draw.rect(
                            start.vboard, BLACK, pygame.Rect(960, 300, 40, 40)
                        )
                        start.turns = 0

                    if win == 0:
                        pygame.draw.rect(
                            start.vboard, BLACK, pygame.Rect(315, 80, 40, 40)
                        )

                        pygame.draw.rect(
                            start.vboard, BLACK, pygame.Rect(680, 80, 40, 40)
                        )

                        pygame.draw.rect(
                            start.vboard, BLACK, pygame.Rect(800, 230, 300, 30)
                        )

        pygame.display.flip()
        clock.tick(FPS)
