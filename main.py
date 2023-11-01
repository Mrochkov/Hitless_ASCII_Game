import curses
import random
import time

#GLOBAL SETTINGS
PLAYER_SPEED = 5
ENEMY_SPEED = 0.15
NUM_ENEMIES = 5
RAND_ENEMY = 5
LEADERBOARD = []
GAME_OVER = False

game_speeds = {"slow": 0.15, "normal": 0.1, "fast": 0.05}
difficulty_levels = {"easy": 5, "normal": 10, "hard": 20}


def show_settings(stdscr, settings):
    global ENEMY_SPEED, RAND_ENEMY

    options = [
        ("Game Speed", list(game_speeds.keys())[list(game_speeds.values()).index(ENEMY_SPEED)]),
        ("Difficulty", list(difficulty_levels.keys())[list(difficulty_levels.values()).index(RAND_ENEMY)])
    ]

    #Settings box
    max_width = max([len(f"{text}: {value}") for text, value in options])
    max_width = max(max_width, len("Use '-' or '+' to manipulate settings"))
    box_width = max_width + 10
    box_height = len(options) * 2 + 5

    height, width = stdscr.getmaxyx()

    start_y = (height - box_height) // 2
    start_x = (width - box_width) // 2

    selected_option = 0
    while True:
        stdscr.clear()

        #Border
        for y in range(box_height):
            if y == 0 or y == box_height - 1:
                stdscr.addstr(start_y + y, start_x, "+" + "-" * (box_width - 2) + "+")
            else:
                stdscr.addstr(start_y + y, start_x, "|" + " " * (box_width - 2) + "|")

        stdscr.addstr(start_y + 1, start_x + 4, "Settings: ", curses.A_BOLD)
        stdscr.addstr(start_y + 3, start_x + 4, "Use arrows '<-''->' to manipulate settings")

        for index, (text, value) in enumerate(options):
            if index == selected_option:
                stdscr.addstr(start_y + 5 + index * 2, start_x + 4, f"> {text}: {value}", curses.A_STANDOUT)
            else:
                stdscr.addstr(start_y + 5 + index * 2, start_x + 4, f"  {text}: {value}")

        stdscr.addstr(start_y + 5 + len(options) * 2, start_x + 4, "Press Enter to return")
        key = stdscr.getch()


        # Settings option selection
        if key == curses.KEY_UP and selected_option > 0:
            selected_option -= 1
        elif key == curses.KEY_DOWN and selected_option < len(options) - 1:
            selected_option += 1
        elif key == curses.KEY_RIGHT:
            if selected_option == 0:
                current_speed = options[selected_option][1]
                next_speed_index = (list(game_speeds.keys()).index(current_speed) + 1) % len(game_speeds)
                ENEMY_SPEED = game_speeds[list(game_speeds.keys())[next_speed_index]]
            else:
                current_difficulty = options[selected_option][1]
                next_difficulty_index = (list(difficulty_levels.keys()).index(current_difficulty) + 1) % len(
                    difficulty_levels)
                RAND_ENEMY = difficulty_levels[list(difficulty_levels.keys())[next_difficulty_index]]
        elif key == curses.KEY_LEFT:
            if selected_option == 0:
                current_speed = options[selected_option][1]
                prev_speed_index = (list(game_speeds.keys()).index(current_speed) - 1) % len(game_speeds)
                ENEMY_SPEED = game_speeds[list(game_speeds.keys())[prev_speed_index]]
            else:
                current_difficulty = options[selected_option][1]
                prev_difficulty_index = (list(difficulty_levels.keys()).index(current_difficulty) - 1) % len(
                    difficulty_levels)
                RAND_ENEMY = difficulty_levels[list(difficulty_levels.keys())[prev_difficulty_index]]
        elif key == 10:
            return

        options[0] = ("Game Speed", list(game_speeds.keys())[list(game_speeds.values()).index(ENEMY_SPEED)])
        options[1] = ("Difficulty", list(difficulty_levels.keys())[list(difficulty_levels.values()).index(RAND_ENEMY)])



def show_information(stdscr):
    while True:
        stdscr.clear()


        sh, sw = stdscr.getmaxyx()

        information_text = "Game is all about dodging incoming bullets, the longer you survive the more points you get." \
                           "\n You have only one life." \
                           " \n\n\n How to play: \n\n Press '<-' to move left \n Press '->' to move right " \
                           "\n\n\n Press enter to return to the main menu"


        #Info box
        info_height = len(information_text.split('\n'))
        info_width = max(len(line) for line in information_text.split('\n'))

        start_y = (sh - info_height) // 2
        start_x = (sw - info_width) // 2

        border_width = info_width + 4
        border_height = info_height

        border = '+' + '-' * (border_width - 2) + '+'
        stdscr.addstr(start_y - 2, start_x - 2, '+' + '-' * (border_width) + '+')
        stdscr.addstr(start_y + border_height + 1, start_x - 2, '+' + '-' * (border_width) + '+')
        for i in range(start_y - 1, start_y + border_height + 1):
            stdscr.addch(i, start_x - 2, '|')
            stdscr.addch(i, start_x + border_width - 2, '|')

        for i, line in enumerate(information_text.split('\n')):
            stdscr.addstr(start_y + i, start_x, line.center(info_width + 2))

        stdscr.refresh()
        key = stdscr.getch()

        if key == 10:
            return



def show_welcome_screen(stdscr):
    stdscr.clear()
    stdscr.refresh()
    sh, sw = stdscr.getmaxyx()

    logo = [
        "  _    _  _  ______  _       ______   _____   _____  ",
        " | |  | || ||__  __|| |     |  ____| / ____| / ____| ",
        " | |__| || |  | |   | |     | |__   | (___  | (____  ",
        " |  __  || |  | |   | |     |  __|   \___ \  \____ \ ",
        " | |  | || |  | |   | |____ | |____  ____) |  ____) |",
        " |_|  |_||_|  |_|   |______||______||_____/  |_____/ "
    ]

    #Menu
    menu_items = ["1. Start the game", "2. Information", "3. Settings", "4. Leaderboard", "5. Quit"]
    menu_height = len(menu_items)
    menu_width = max(len(item) for item in menu_items)

    logo_height = len(logo)
    logo_width = len(logo[0])
    padding = 3

    start_y = (sh - (logo_height + menu_height + padding)) // 2
    start_x = (sw - max(logo_width, menu_width)) // 2

    selected_option = 0

    while True:
        stdscr.clear()

        #Show logo
        for i, line in enumerate(logo):
            stdscr.addstr(start_y + i, start_x, line)

        #Menu box
        border_width = max(logo_width, menu_width) + 8
        border_height = logo_height + menu_height + 3

        border = '+' + '-' * (border_width - 2) + '+'
        stdscr.addstr(start_y - 2, start_x - 3, '+' + '-' * (border_width) + '+')
        stdscr.addstr(start_y + border_height, start_x - 3, '+' + '-' * (border_width) + '+')
        for i in range(start_y - 1, start_y + border_height):
            stdscr.addch(i, start_x - 3, '|')
            stdscr.addch(i, start_x + border_width - 2, '|')

        for i, item in enumerate(menu_items):
            if i == selected_option:
                stdscr.addstr(start_y + logo_height + i + padding, start_x, '|  ' + item + '  |', curses.A_STANDOUT)
            else:
                stdscr.addstr(start_y + logo_height + i + padding, start_x, '|  ' + item + '  |')

        stdscr.refresh()


        key = stdscr.getch()

        if key == curses.KEY_UP and selected_option > 0:
            selected_option -= 1
        elif key == curses.KEY_DOWN and selected_option < len(menu_items) - 1:
            selected_option += 1
        elif key == 10:
            return selected_option

def ask_for_name(stdscr, score):
    stdscr.clear()

    game_over_text = [
        " _____                         ____                 ",
        "|  __ \                       / __ \                ",
        "| |  \/ __ _ _ __ ___   ___  | |  | |_   _____ _ __ ",
        "| | __ / _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|",
        "| |_\ \ (_| | | | | | |  __/ | |__| |\ V /  __/ |   ",
        " \____/\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   ",
    ]
    sh, sw = stdscr.getmaxyx()
    w = len(game_over_text[0]) + 4
    h = len(game_over_text) + 4
    y = (sh - h) // 2
    x = (sw - w) // 2

    stdscr.addstr(y - 1, x, '+' + '-' * w + '+')
    for i in range(y, y + h):
        stdscr.addstr(i, x, '|')
        stdscr.addstr(i, x + w + 2, '|')
    stdscr.addstr(y + h, x, '+' + '-' * w + '+')

    for idx, line in enumerate(game_over_text, start=1):
        stdscr.addstr(y + idx, x + 2, line)

    stdscr.addstr(19, 35, "Enter your name: ")
    curses.echo()
    name = stdscr.getstr(19, 53, 20).decode("utf-8")
    curses.noecho()
    return name

def game_over_screen(stdscr, score):
    global GAME_OVER, ENEMY_SPEED
    GAME_OVER = True
    player_name = ask_for_name(stdscr, score)

    #current game settings
    game_speed = list(game_speeds.keys())[list(game_speeds.values()).index(ENEMY_SPEED)]
    difficulty_level = list(difficulty_levels.keys())[list(difficulty_levels.values()).index(RAND_ENEMY)]

    LEADERBOARD.append((player_name, score, game_speed, difficulty_level))
    LEADERBOARD.sort(key=lambda x: x[1], reverse=True)
    stdscr.getch()


def show_leaderboard(stdscr, settings):
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()


        max_width = 40

        #Content border calculation
        for _, (name, score, game_speed, difficulty_level) in enumerate(LEADERBOARD):
            line_content_length = len(f"{name} - {score} (Speed: {game_speed}, Difficulty: {difficulty_level})")
            max_width = max(line_content_length + 20, max_width)  # Adjust as needed

        border_top_bottom = "+" + "=" * (max_width - 2) + "+"
        start_x = (w - max_width) // 2
        start_y = (h - len(LEADERBOARD) - 5) // 2

        #Border Top
        stdscr.addstr(start_y, start_x, border_top_bottom)

        stdscr.addstr(start_y + 1, start_x, "|")
        stdscr.addstr(start_y + 1, start_x + 1, "Leaderboard".center(max_width - 2), curses.A_BOLD)
        stdscr.addstr(start_y + 1, start_x + max_width - 1, "|")
        stdscr.addstr(start_y + 2, start_x, "|")
        stdscr.addstr(start_y + 2, start_x + 1, "===========".center(max_width - 2), curses.A_BOLD)
        stdscr.addstr(start_y + 2, start_x + max_width - 1, "|")

        #Entries with borders
        for index, (name, score, game_speed, difficulty_level) in enumerate(LEADERBOARD, start=1):
            line_content = f"{index}. {name} - Score: {score} (Speed: {game_speed}, Difficulty: {difficulty_level})"
            y_position = start_y + 2 + index
            stdscr.addstr(y_position, start_x, "|")
            stdscr.addstr(y_position, start_x + 1, line_content.ljust(max_width - 2))
            stdscr.addstr(y_position, start_x + max_width - 1, "|")

        #Instructions inside the border
        instruction_index = start_y + 4 + len(LEADERBOARD)
        stdscr.addstr(instruction_index, start_x, "|")
        stdscr.addstr(instruction_index, start_x + 1, "Press enter key to return to the menu.".ljust(max_width - 2))
        stdscr.addstr(instruction_index, start_x + max_width - 1, "|")

        #side borders for leaderboard
        for i in range(start_y + 3 + len(LEADERBOARD), instruction_index):
            stdscr.addstr(i, start_x, "|")
            stdscr.addstr(i, start_x + max_width - 1, "|")

        # Border Bottom
        stdscr.addstr(instruction_index + 1, start_x, border_top_bottom)

        stdscr.refresh()
        key = stdscr.getch()

        if key == 10:
            return




def main_game(stdscr):
    global GAME_OVER
    GAME_OVER = False
    curses.curs_set(0)
    stdscr.clear()
    stdscr.timeout(0)
    stdscr.refresh()

    # Arena dimensions
    sh, sw = 20, 40

    # Calculate screen center
    screen_h, screen_w = stdscr.getmaxyx()
    start_y = (screen_h - sh) // 2
    start_x = (screen_w - sw) // 2

    #Player_create
    player = "<O>"
    player_x = sw // 2 - 1
    player_y = sh - 3

    #Enemies_create
    enemies = []
    num_enemies = NUM_ENEMIES

    for _ in range(num_enemies):
        enemy = 'v'
        enemy_x = random.randint(1, sw - 2)
        enemy_y = 2
        enemies.append((enemy_x, enemy_y, enemy))

    #Arena ascii border
    top_bottom_border = '+' + '-' * (sw - 4) + '+'
    side_border = '|' + ' ' * (sw - 4) + '|'
    ascii_art = [' ' * (sw - 2), top_bottom_border] + [side_border] * (sh - 4) + [top_bottom_border]

    score = 0

    while not GAME_OVER:
        win = stdscr.subwin(sh, sw, start_y, start_x)
        win.clear()

        for i, line in enumerate(ascii_art):
            win.addstr(i, 1, line)

        #Move player
        action = stdscr.getch()
        if action == curses.KEY_LEFT and player_x > 2:
            player_x -= 1
        elif action == curses.KEY_RIGHT and player_x < sw - 5:
            player_x += 1

        #Move enemies
        new_enemies = []
        for enemy_x, enemy_y, enemy in enemies:
            enemy_y += 1

            #Collisions
            if enemy_y == sh - 2:
                if enemy_x >= player_x and enemy_x <= player_x:
                    GAME_OVER = True
                    return game_over_screen(stdscr, score)
            else:
                new_enemies.append((enemy_x, enemy_y, enemy))

        #Spawn enemies
        if random.randint(1, RAND_ENEMY) > 4:
            new_enemy = 'v'
            new_enemy_x = random.randint(2, sw - 3)
            new_enemy_y = 0
            new_enemies.append((new_enemy_x, new_enemy_y, new_enemy))

        enemies = new_enemies

        # Is game over
        if any((enemy_x >= player_x and enemy_x <= player_x + 2 and player_y == enemy_y) for enemy_x, enemy_y, _ in enemies):
            GAME_OVER = True

        # Draw player
        win.addstr(player_y, player_x, player)

        # Draw enemies
        for enemy_x, enemy_y, enemy in enemies:
            win.addch(enemy_y, enemy_x, enemy)
            if enemy_y == player_y:
                score += 1

        win.addstr(0, 2, f'Score: {score}')

        win.refresh()
        time.sleep(ENEMY_SPEED)
    game_over_screen(stdscr, score)




def main(stdscr, settings=game_speeds):
    curses.curs_set(0)
    sh, sw = 20, 40
    stdscr.clear()
    stdscr.refresh()

    while True:
        choice = show_welcome_screen(stdscr)

        if choice == 0:
            stdscr.clear()
            stdscr.addstr(0, 0, "Starting the game...")
            stdscr.refresh()
            main_game(stdscr)

        elif choice == 1:
            stdscr.clear()
            stdscr.addstr(0, 0, "Information:")
            show_information(stdscr)
            stdscr.refresh()

        elif choice == 2:
            stdscr.clear()
            stdscr.addstr(0, 0, "Settings:")
            show_settings(stdscr, settings)
            stdscr.refresh()
            stdscr.getch()

        elif choice == 3:
            stdscr.clear()
            stdscr.addstr(0, 0, "Leaderboard")
            show_leaderboard(stdscr, settings)
            stdscr.refresh()
            stdscr.getch()

        elif choice == 4:
            stdscr.addstr(0, 0, "Goodbye!")
            stdscr.refresh()
            stdscr.getch()
            break




if __name__ == "__main__":
    curses.wrapper(main)
