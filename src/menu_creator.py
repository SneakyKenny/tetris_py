import pygame
import read_config
import my_networking
from threading import Thread

margin_all = 30

T_pos = 5
T_scale = 7

T_matrix = [
    [False, True, False],
    [False, True,  True],
    [False, True, False]
]

background_colour = (150, 150, 150)

purple = (149, 45, 152)

#has_wrote = write_config(file_path = 'settings.ini', section = 'SectionKeyBinds', option = 'restart_key', value = 'f4')
#keybinds = read_config(file_path = 'settings.ini', section = 'SectionKeyBinds')
#print(f'keybinds: {keybinds}')

def name_from_key(key):
    if key == 0:
        return 'unbound'
    if chr(key) > ' ' and chr(key) <= '~':
        return chr(key)
    dic = {
        32: 'Space'
    }
    if chr(key) == ' ':
        return 'Space'
    elif key >= 282 and key <= 296:
        return 'F' + str(key - 281)
    elif key == 276:
        return '<'
    elif key == 275:
        return '>'
    elif key == 273:
        return '/\\'
    elif key == 274:
        return '\\/'
    return chr(key) # TODO: change that

def play_solo_option():
    return MenuOptions.IS_PLAYING_SOLO

def play_multi_option():
    MenuOptions.options = MenuOptions.multi_options
    MenuOptions.option_texts = MenuOptions.multi_option_texts
    return True

def change_nickname_option():
    username = input('Username:')
    if username and len(username) > 0 and len(username) < 32:
        return MenuOptions.IS_USERNAME_CHANGE + ';' + username
    print('Please input a username with length between 1 and 31.')
    return MenuOptions.NOT_IS_USERNAME_CHANGE

def change_control_option():
    MenuOptions.options = MenuOptions.control_options
    MenuOptions.option_texts = MenuOptions.control_option_texts
    return True

def visual_settings_option():
    print('visual_settings_option')

def quit_app_option():
    pygame.quit()
    quit()

def back_to_main_option():
    MenuOptions.options = MenuOptions.base_options
    MenuOptions.option_texts = MenuOptions.base_option_texts

    return True

def host_game_option():
    server_thread = Thread(target = my_networking.GameServer, args = ('25.9.28.33', 1234, True, True))
    server_thread.start()
    return server_thread

def join_game_option():
    return MenuOptions.IS_JOINING_TEXT

def move_left_option(opt):
    opt.set(True, 'move_left')
    return True

def move_right_option(opt):
    opt.set(True, 'move_right')
    return True

def rotate_left_option(opt):
    opt.set(True, 'rotate_left')
    return True

def rotate_right_option(opt):
    opt.set(True, 'rotate_right')
    return True

def rotate_180_option(opt):
    opt.set(True, 'rotate_180')
    return True

def hold_piece_option(opt):
    opt.set(True, 'hold_piece')
    return True

def hard_drop_piece_option(opt):
    opt.set(True, 'hard_drop')
    return True

def soft_drop_piece_option(opt):
    opt.set(True, 'soft_drop')
    return True

def sonic_drop_piece_option(opt):
    opt.set(True, 'sonic_drop')
    return True

def das_option(opt):
    pass

def arr_option(opt):
    pass

class MenuOptions:
    def __init__(self):
        self.base_timer = 5 * 1000
        self.is_waiting_for_input = False
        self.control_to_change = None
        self.timer = 0
        self.set()

    def set(self, is_waiting = False, control = None):
        self.is_waiting_for_input = is_waiting
        self.control_to_change = control
        self.timer = self.base_timer

    IS_JOINING_TEXT = 'joining'
    IS_PLAYING_SOLO = 'solo' #TODO: choose game_mode instead of directly getting into the game

    IS_USERNAME_CHANGE = 'username_change'
    NOT_IS_USERNAME_CHANGE = 'no_change'

    BACK_TO_MAIN = back_to_main_option
    BACK_TO_MAIN_TEXT = 'Back to main menu'

    PLAY_SOLO = play_solo_option
    PLAY_SOLO_TEXT = 'Play Solo'

    PLAY_MULTI = play_multi_option
    PLAY_MULTI_TEXT = 'Play Multi'

    HOST_GAME = host_game_option
    HOST_GAME_TEXT = 'Host a game'

    JOIN_GAME = join_game_option
    JOIN_GAME_TEXT = 'Join a game'

    multi_options = [HOST_GAME, JOIN_GAME, BACK_TO_MAIN]
    multi_option_texts = [HOST_GAME_TEXT, JOIN_GAME_TEXT, BACK_TO_MAIN_TEXT]

    CHANGE_NICKNAME = change_nickname_option
    CHANGE_NICKNAME_TEXT = 'Change Name'

    CHANGE_CONTROLS = change_control_option
    CHANGE_CONTROLS_TEXT = 'Controls'

    #TODO: display what is the current binding for these keys

    MOVE_LEFT = move_left_option
    MOVE_LEFT_TEXT = 'Move Left'

    MOVE_RIGHT = move_right_option
    MOVE_RIGHT_TEXT = 'Move Right'

    ROTATE_LEFT = rotate_left_option
    ROTATE_LEFT_TEXT = 'Rotate Left'

    ROTATE_RIGHT = rotate_right_option
    ROTATE_RIGHT_TEXT = 'Rotate Right'

    ROTATE_180 = rotate_180_option
    ROTATE_180_TEXT = 'Rotate 180'

    HOLD_PIECE = hold_piece_option
    HOLD_PIECE_TEXT = 'Hold Piece'

    HARD_DROP_PIECE = hard_drop_piece_option
    HARD_DROP_PIECE_TEXT = 'Hard Drop'

    SOFT_DROP_PIECE = soft_drop_piece_option
    SOFT_DROP_PIECE_TEXT = 'Soft Drop'

    SONIC_DROP_PIECE = sonic_drop_piece_option
    SONIC_DROP_PIECE_TEXT = 'Sonic Drop'

    DAS = das_option
    DAS_TEXT = 'DAS'

    ARR = arr_option
    ARR_TEXT = 'ARR'

    control_options = [MOVE_LEFT, MOVE_RIGHT, ROTATE_LEFT, ROTATE_RIGHT, ROTATE_180, HOLD_PIECE, HARD_DROP_PIECE, SOFT_DROP_PIECE, SONIC_DROP_PIECE, DAS, ARR, BACK_TO_MAIN]
    control_option_texts = [MOVE_LEFT_TEXT, MOVE_RIGHT_TEXT, ROTATE_LEFT_TEXT, ROTATE_RIGHT_TEXT, ROTATE_180_TEXT, HOLD_PIECE_TEXT, HARD_DROP_PIECE_TEXT, SOFT_DROP_PIECE_TEXT, SONIC_DROP_PIECE_TEXT, DAS_TEXT, ARR_TEXT, BACK_TO_MAIN_TEXT]

    VISUAL_SETTINGS = visual_settings_option
    VISUAL_SETTINGS_TEXT = 'Visual Settings'

    QUIT_APP = quit_app_option
    QUIT_APP_TEXT = 'Quit'

    base_options = [PLAY_SOLO, PLAY_MULTI, CHANGE_NICKNAME, CHANGE_CONTROLS, VISUAL_SETTINGS, QUIT_APP]
    base_option_texts = [PLAY_SOLO_TEXT, PLAY_MULTI_TEXT, CHANGE_NICKNAME_TEXT, CHANGE_CONTROLS_TEXT, VISUAL_SETTINGS_TEXT, QUIT_APP_TEXT]

    options = base_options
    option_texts = base_option_texts

    text_to_dict_text = {
        MOVE_LEFT_TEXT : 'move_left',
        MOVE_RIGHT_TEXT : 'move_right',
        ROTATE_LEFT_TEXT : 'rotate_left',
        ROTATE_RIGHT_TEXT : 'rotate_right',
        ROTATE_180_TEXT : 'rotate_180',
        HOLD_PIECE_TEXT : 'hold_piece',
        HARD_DROP_PIECE_TEXT : 'hard_drop',
        SOFT_DROP_PIECE_TEXT : 'soft_drop',
        SONIC_DROP_PIECE_TEXT : 'sonic_drop',
    }

def text_render(string, position, size, screen, bindings, is_timer = False): #size is font_size
    if MenuOptions.options == MenuOptions.control_options:
        if string != MenuOptions.DAS_TEXT and string != MenuOptions.ARR_TEXT and string != MenuOptions.BACK_TO_MAIN_TEXT and not is_timer:
            binding = bindings[MenuOptions.text_to_dict_text[string]]
            string += '    ' + name_from_key(int(binding))

    font = pygame.font.SysFont('berlin sans fb', size)
    text = str(string)
    text = font.render(text, True, (255, 255, 255))
    rect = text.get_rect()
    screen.blit(text, (position[0], position[1] + (rect.height // 2)))

def display_index(screen, index, option_size):
    position = (T_pos, index * option_size + margin_all - (len(MenuOptions.options) // 2 - 5))
    for i in range(len(T_matrix)):
        for j in range(len(T_matrix[i])):
            if T_matrix[i][j]:
                pygame.draw.rect(screen, purple, pygame.Rect((position[0] + j * T_scale, position[1] + i * T_scale), (T_scale, T_scale)))

def display_image(screen, img):
    screen.blit(img, (200, margin_all))

def display_menu(screen, index, bindings, img, is_in_main_menu = True):
    w, h = pygame.display.get_surface().get_size()
    w -= margin_all
    h -= margin_all

    screen.fill(background_colour)

    if is_in_main_menu:
        display_image(screen, img)

    option_size = 38

    text_size = 24
    #text_render('abc', (margin_all, margin_all), 30, screen)

    for i in range(len(MenuOptions.options)):
        text_render(MenuOptions.option_texts[i], (margin_all, i * option_size + 1 + (margin_all // 2)), text_size, screen, bindings)

    display_index(screen, index, option_size)

    pygame.display.flip()

def create_menu(screen):
    #this returns the server created, if created, else None
    #TODO: start by reading from option file to set the keys
    #      then read inputs depending on these keys
    #      rather than the hardcoded ones
    opt = MenuOptions()
    clock = pygame.time.Clock()

    path = 'pytris_logo.png'

    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, (250, 160))

    config = read_config.read_config(file_path = 'settings.ini', section = 'SectionKeyBinds')
    for k, b in config.items():
        config[k] = int(b)
    w, h = pygame.display.get_surface().get_size()

    done = False

    index = 0
    display_menu(screen, index, config, img, True)

    while not done:
        dt = clock.tick(240)
        if opt.is_waiting_for_input:
            opt.timer -= dt
            screen.fill(background_colour)
            text_render(str(round(opt.timer / 1000)), ((w - margin_all) / 2, (h - margin_all) / 2 - 38), 38, screen, config, True)
            pygame.display.flip()
            if opt.timer < 0:
                opt.is_waiting_for_input = False
                display_menu(screen, index, config, img)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == ord('q') or event.key == pygame.K_ESCAPE:
                    done = True
                    pygame.quit()
                    quit()
                if opt.is_waiting_for_input:
                    if not event.key in config.values():
                        has_wrote = read_config.write_config(file_path = 'settings.ini', section = 'SectionKeyBinds', option = opt.control_to_change, value = str(event.key))
                        opt.is_waiting_for_input = False
                        if has_wrote:
                            config[opt.control_to_change] = event.key
                else:
                    if event.key == pygame.K_UP:
                        index = (index - 1) % len(MenuOptions.options)
                    elif event.key == pygame.K_DOWN:
                        index = (index + 1) % len(MenuOptions.options)
                    if event.key == pygame.K_RETURN:
                        if MenuOptions.options[index]:
                            if MenuOptions.options == MenuOptions.control_options and index < len(MenuOptions.options) - 1:
                                #TODO: DAS/ARR from file
                                done = not MenuOptions.options[index](opt)
                            else:
                                if MenuOptions.options == MenuOptions.multi_options:
                                    if index == 0:
                                        server_thread = MenuOptions.options[index]()
                                        if server_thread:
                                            return server_thread
                                    elif index == 1:
                                        joining = MenuOptions.options[index]()
                                        if joining == MenuOptions.IS_JOINING_TEXT:
                                            return joining
                                else:
                                    if MenuOptions.options == MenuOptions.base_options:
                                        if index == 0:
                                            solo = MenuOptions.options[index]()
                                            if solo == MenuOptions.IS_PLAYING_SOLO:
                                                return solo
                                        elif index == 2:
                                            ret_username = MenuOptions.options[index]().split(';')
                                            if ret_username[0] == MenuOptions.IS_USERNAME_CHANGE:
                                                has_wrote = read_config.write_config(file_path = 'settings.ini', section = 'SectionUserInfos', option = 'username', value = ret_username[1])
                                            index = 0
                                        else:
                                            done = not MenuOptions.options[index]()
                                            index = 0
                                    else:
                                        done = not MenuOptions.options[index]()
                                        index = 0

                if not done and not opt.is_waiting_for_input:
                    display_menu(screen, index, config, img, MenuOptions.options == MenuOptions.base_options)

    return None
