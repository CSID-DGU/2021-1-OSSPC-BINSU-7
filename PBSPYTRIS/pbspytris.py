# -*-coding:utf-8-*-
# PYTRIS Copyright (c) 2017 Jason Kim All Rights Reserved.

import pygame
import operator
import wave
import os
from mino import *
from random import *
from pygame.locals import *


# Unchanged values Define 변하지 않는 변수 선언

block_size = 17  # Height, width of single block
width = 10
height = 20

board_x = 10
board_y = 20
board_width = 800 # Board width
board_height = 450 # Board height
board_rate = 0.5625 #가로세로비율
block_size = int(board_height * 0.045)
mino_matrix_x = 4 #mino는 4*4 배열이어서 이를 for문에 사용
mino_matrix_y = 4 #mino는 4*4 배열이어서 이를 for문에 사용

speed_change = 2 # 레벨별 블록 하강 속도 상승 정도

gold = 0
framerate = 30  # Bigger -> Slower

min_width = 400
min_height = 225
mid_width = 1200

total_time = 60 # 타임 어택 시간
attack_time = 30 # 어택모드 제한시간

# 기본 볼륨
music_volume = 5
effect_volume = 5

initalize = True

pygame.init()

clock = pygame.time.Clock() #창, 화면을 초당 몇번 출력하는가(FPS) clock.tick 높을수록 cpu많이 사용
screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE) #GUI창 설정하는 변수
pygame.display.set_caption("PBSPYTRIS") #GUI 창의 이름

class ui_variables:
    font_path = "./assets/fonts/OpenSans-Light.ttf"
    font_path_b = "./assets/fonts/OpenSans-Bold.ttf"
    font_path_i = "./assets/fonts/Inconsolata/Inconsolata.otf"

    # Font(글씨체, 글자크기)
    h1 = pygame.font.Font(font_path_b, 80)
    h2 = pygame.font.Font(font_path_b, 30)
    h3 = pygame.font.Font(font_path_b, 25)
    h4 = pygame.font.Font(font_path_b, 20)
    h5 = pygame.font.Font(font_path_b, 13)
    h6 = pygame.font.Font(font_path_b, 10)

    h1_b = pygame.font.Font(font_path_b, 50)
    h2_b = pygame.font.Font(font_path_b, 30)

    h2_i = pygame.font.Font(font_path_i, 30)
    h5_i = pygame.font.Font(font_path_i, 13)

    # Sounds
    pygame.mixer.music.load("assets/sounds/SFX_BattleMusic.wav") #음악 불러옴
    pygame.mixer.music.set_volume(0.5) # 이 부분도 필요 없음, set_volume에 추가해야 함
    intro_sound = pygame.mixer.Sound("assets/sounds/SFX_Intro.wav")
    fall_sound = pygame.mixer.Sound("assets/sounds/SFX_Fall.wav")
    break_sound = pygame.mixer.Sound("assets/sounds/SFX_Break.wav")
    click_sound = pygame.mixer.Sound("assets/sounds/SFX_ButtonUp.wav") #여기부터
    move_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceMoveLR.wav")
    drop_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceHardDrop.wav")
    single_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearSingle.wav")
    double_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearDouble.wav")
    triple_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearTriple.wav") #여기까지는 기존코드
    tetris_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialTetris.wav")
    LevelUp_sound = pygame.mixer.Sound("assets/sounds/SFX_LevelUp.wav")
    GameOver_sound = pygame.mixer.Sound("assets/sounds/SFX_GameOver.wav")

    # Combo graphic
    combos = []
    large_combos = []
    combo_ring = pygame.image.load("assets/Combo/4combo ring.png")  # 4블록 동시제거 그래픽
    combo_4ring = pygame.transform.smoothscale(combo_ring, (200, 100)) #이미지를 특정 크기로 불러옴, 200=가로크기, 100=세로크기#
    for i in range(1, 11): #10가지의 콤보 이미지 존재. 각 숫자에 해당하는 이미지 불러옴
        combos.append(pygame.image.load("assets/Combo/" + str(i) + "combo.png"))
        large_combos.append(pygame.transform.smoothscale(combos[i - 1], (150, 200))) #콤보이미지를 특정 크기로 불러옴, 150=가로크기, 200=세로크기#

    combos_sound = []
    for i in range(1, 10): #1-9까지 콤보사운드 존재. 각 숫자에 해당하는 음악 불러옴
        combos_sound.append(pygame.mixer.Sound("assets/sounds/SFX_" + str(i + 2) + "Combo.wav"))

    #rainbow 보너스점수 graphic
    rainbow_vector = pygame.image.load('assets/vector/rainbow.png')

    # Background colors. RGB 값에 해당함
    black = (10, 10, 10)  # rgb(10, 10, 10)
    black_pause = (0, 0, 0, 127)
    white = (0, 153, 153)  # rgb(255, 255, 255) # 청록색으로 변경
    real_white = (255, 255, 255)  # rgb(255, 255, 255)
    pinkpurple = (250, 165, 255) #rgb(250, 165, 255) 핑크+보라#

    grey_1 = (70, 130, 180)  # rgb(26, 26, 26) 테두리 파랑색
    grey_2 = (221, 221, 221)  # rgb(35, 35, 35)
    grey_3 = (000, 000, 139)  # rgb(55, 55, 55) #남색
    bright_yellow = (255, 217, 102)  # 밝은 노랑

    # Tetrimino colors. RGB 값에 해당함
    cyan = (10, 255, 226)  # rgb(69, 206, 204) # I
    blue = (64, 105, 255)  # rgb(64, 111, 249) # J
    orange = (245, 144, 12)  # rgb(253, 189, 53) # L
    yellow = (225, 242, 41)  # rgb(246, 227, 90) # O
    green = (22, 181, 64)  # rgb(98, 190, 68) # S
    pink = (242, 41, 195)  # rgb(242, 64, 235) # T
    red = (204, 22, 22)  # rgb(225, 13, 27) # Z

    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3]
    cyan_image = 'assets/block_images/cyan.png'
    blue_image = 'assets/block_images/blue.png'
    orange_image = 'assets/block_images/orange.png'
    yellow_image = 'assets/block_images/yellow.png'
    green_image = 'assets/block_images/green.png'
    pink_image = 'assets/block_images/purple.png'
    red_image = 'assets/block_images/red.png'
    ghost_image = 'assets/block_images/ghost.png'
    table_image = 'assets/block_images/background.png'
    linessent_image = 'assets/block_images/linessent.png'
    t_block = [table_image, cyan_image, blue_image, orange_image, yellow_image, green_image, pink_image, red_image,
               ghost_image, linessent_image]

#각 이미지 주소
# background
background_image = 'assets/vector/Background.png' #홈 배경화면
gamebackground_image = 'assets/vector/Background_game.png' #게임 배경화면

# board
board_challenge = 'assets/vector/board_challenge.png'
board_gameover = 'assets/vector/board_gameover.png'
board_help = 'assets/vector/board_help.png'
board_leader = 'assets/vector/board_leader.png'
board_number = 'assets/vector/board_number.png'
board_pause = 'assets/vector/board_pause.png'
board_setting = 'assets/vector/board_setting.png'
board_shop = 'assets/vector/board_shop.png'
board_start = 'assets/vector/board_start.png'
board_sandbox = 'assets/vector/board_sandbox.png'
board_difficulty = 'assets/vector/board_difficulty.png'
board_volume = 'assets/vector/board_volume.png'
board_screen = 'assets/vector/board_screen.png'

#button
button_allmute = 'assets/vector/button_allmute.png'
button_allmute_clicked = 'assets/vector/button_allumute_clicked.png'
button_allmute_on = 'assets/vector/button_allmute_on.png'

button_back = 'assets/vector/button_back.png'
button_back_clicked = 'assets/vector/button_back_clicked.png'

button_default = 'assets/vector/button_default.png'
button_default_clicked = 'assets/vector/button_default_clicked.png'
button_default_on = 'assets/vector/button_default_on.png'

button_gravity = 'assets/vector/button_gravity.png'
button_gravity_clicked = 'assets/vector/button_gravity_clicked.png'
button_gravity_on = 'assets/vector/button_gravity_on.png'

button_help = 'assets/vector/button_help.png'
button_help_clicked = 'assets/vector/button_help_clicked.png'

button_menu = 'assets/vector/button_menu.png'
button_menu_clicked = 'assets/vector/button_menu_clicked.png'

button_ok = 'assets/vector/button_ok.png'
button_ok_clicked = 'assets/vector/button_ok_clicked.png'

button_pvp = 'assets/vector/button_pvp.png'
button_pvp_clicked = 'assets/vector/button_pvp_clicked.png'

button_quit = 'assets/vector/button_quit.png'
button_quit_clicked = 'assets/vector/button_quit_clicked.png'

button_restart = 'assets/vector/button_restart.png'
button_restart_clicked = 'assets/vector/button_restart_clicked.png'

button_resume = 'assets/vector/button_resume.png'
button_resume_clicked = 'assets/vector/button_resume_clicked.png'

button_sandbox = 'assets/vector/button_sandbox.png'
button_sandbox_clicked = 'assets/vector/button_sandbox_clicked.png'
button_sandbox_on = 'assets/vector/button_sandbox_on.png'

button_setting = 'assets/vector/button_setting.png'
button_setting_clicked = 'assets/vector/button_setting_clicked.png'

button_shop = 'assets/vector/button_shop.png'
button_shop_clicked = 'assets/vector/button_shop_clicked.png'

button_single = 'assets/vector/button_single.png'
button_single_clicked = 'assets/vector/button_single_clicked.png'

button_start = 'assets/vector/button_start.png'
button_start_clicked = 'assets/vector/button_start_clicked.png'

button_timeattack = 'assets/vector/button_timeattack.png'
button_timeattack_clicked = 'assets/vector/button_timeattack_clicked.png'
button_timeattack_on = 'assets/vector/button_timeattack_on.png'

button_difficulty = 'assets/vector/button_difficulty.png'
button_difficulty_clicked = 'assets/vector/button_difficulty_clicked.png'

button_easy = 'assets/vector/button_easy.png'
button_easy_clicked = 'assets/vector/button_easy_clicked.png'

button_normal = 'assets/vector/button_normal.png'
button_normal_clicked = 'assets/vector/button_normal_clicked.png'

button_hard = 'assets/vector/button_hard.png'
button_hard_clicked = 'assets/vector/button_hard_clicked.png'

button_buy = 'assets/vector/button_buy.png'
button_buy_clicked = 'assets/vector/button_buy_clicked.png'

button_default = 'assets/vector/button_default.png'

# check 이 친구는 후에 사용하지 않으면 삭제
check = 'assets/vector/check.png'
checkbox = 'assets/vector/check_box.png'
checkbox_clicked = 'assets/vector/check_clicked_box.png'

# help : keyboard
# help_image = 'assets/vector/help_imgage.png'

# icon : 버튼이 아닌 아이콘, 이벤트 없음
icon_combo = 'assets/vector/icon_combo.png'
icon_level = 'assets/vector/icon_level.png'
icon_speed = 'assets/vector/icon_speed.png'

# item
item_bomb = 'assets/vector/item_bomb.png'
item_earth = 'assets/vector/item_earth.png'
item_gold = 'assets/vector/item_gold.png'
item_tnt = 'assets/vector/item_tnt.png'

# pvp
pvp_win_image = 'assets/vector/pvp_win.png'
pvp_lose_image = 'assets/vector/pvp_lose.png'

# screensize
size_s = 'assets/vector/screensize1.png'
size_m = 'assets/vector/screensize2.png'
size_b = 'assets/vector/screensize3.png'

# vector : 이벤트 존재하는 아이콘
vector_challenge = 'assets/vector/vector_challenge.png'
vector_challenge_clicked = 'assets/vector/vector_challenge_clicked.png'

vector_leader = 'assets/vector/vector_leaderboard.png'
vector_leader_clicked = 'assets/vector/vector_leader_clicked.png'

vector_minus = 'assets/vector/vector_minus.png'
vector_minus_clicked = 'assets/vector/vector_minus_clicked.png'

vector_plus = 'assets/vector/vector_plus.png'
vector_plus_clicked = 'assets/vector/vector_plus_clicked.png'

vector_screen = 'assets/vector/vector_screen.png'
vector_screen_clicked = 'assets/vector/vector_screen_clicked.png'

vector_setting = 'assets/vector/vector_setting.png'
vector_setting_clicked = 'assets/vector/vector_setting_clicked.png'

vector_sound_off = 'assets/vector/vector_sound_off.png'
vector_sound_on = 'assets/vector/vector_sound_on.png'

vector_volume = 'assets/vector/vector_volume.png'
vector_volume_clicked = 'assets/vector/vector_volume_clicked.png'


class button(): #버튼객체
    def __init__(self, board_width, board_height, x_rate, y_rate, width_rate, height_rate, img=''): #버튼생성
        self.x = board_width * x_rate #버튼 x좌표
        self.y = board_height * y_rate #버튼 y좌표
        self.width = int(board_width * width_rate) #버튼 너비
        self.height = int(board_height * height_rate) #버튼 높이
        self.x_rate = x_rate #board_width * x_rate = x좌표
        self.y_rate = y_rate #board_height * y_rate = y좌표
        self.width_rate = width_rate #board_width * width_rate = 버튼 너비
        self.height_rate = height_rate #board_height * height_rate = 버튼 높이
        self.image = img #불러올 버튼 이미지

    def change(self, board_width, board_height): #버튼 위치, 크기 바꾸기
        self.x = board_width * self.x_rate #x좌표
        self.y = board_height * self.y_rate #y좌표
        self.width = int(board_width * self.width_rate) #너비
        self.height = int(board_height * self.height_rate) #높이

    def draw(self, win, outline=None): #버튼 보이게 만들기
        if outline:
            draw_image(screen, self.image, self.x, self.y, self.width, self.height)

    def isOver(self, pos): #마우스의 위치에 따라 버튼 누르기 pos[0]은 마우스 x좌표, pos[1]은 마우스 y좌표
        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):
            if pos[1] > self.y - (self.height / 2) and pos[1] < self.y + (self.height / 2):
                return True
        return False

    def isOver_2(self, pos): #start 화면에서 single,pvp,help,setting을 위해서 y좌표 좁게 인식하도록
        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):
            if pos[1] > self.y - (self.height / 4) and pos[1] < self.y + (self.height / 4):#243줄에서의 2을 4로 바꿔주면서 좁게 인식할수 있도록함. 더 좁게 인식하고 싶으면 숫자 늘려주기#
                return True
        return False

#버튼객체 생성 class Button에서 확인
#def __init__(self, board_width, board_height, x_rate, y_rate, width_rate, height_rate, img='')
#(현재 보드너비, 현재보드높이, 버튼의 x좌표 위치비율, 버튼의 y좌표 위치비율, 버튼의 너비 길이비율, 버튼의 높이 길이비율)
#  - 전체화면 크기에 대한 비율
# (800, 450, 800*x좌표, 450*y좌표, 너비 비율, 높이 비율)

# main page 1) nothing
start_button = button(board_width, board_height, 0.375, 0.75, 0.16, 0.084, button_start)
help_button = button(board_width, board_height, 0.375, 0.84, 0.16, 0.084, button_help)
shop_button = button(board_width, board_height, 0.625, 0.75, 0.16, 0.084, button_shop)
quit_button = button(board_width, board_height, 0.625, 0.84, 0.16, 0.084, button_quit)

challenge_vector = button(board_width, board_height, 0.05, 0.9,0.0375, 0.0667, vector_challenge)
leader_vector = button(board_width, board_height, 0.15, 0.9,0.0375, 0.0667, vector_leader)
setting_vector = button(board_width, board_height, 0.95, 0.9,0.0375, 0.0667, vector_setting)

# main page 2) start board
single_button = button(board_width, board_height, 0.3, 0.62, 0.16, 0.084, button_single)
pvp_button = button(board_width, board_height, 0.3, 0.72, 0.16, 0.084, button_pvp)
sandbox_button = button(board_width, board_height, 0.7, 0.62, 0.16, 0.084, button_sandbox)
difficulty_button = button(board_width, board_height, 0.7, 0.72, 0.16, 0.084, button_difficulty)
back_button = button(board_width, board_height, 0.5, 0.66, 0.16, 0.084, button_back)
# same in start,leader, help
# setting, volume, screen board

# main page 3) sandbox board
timeattack_button = button(board_width, board_height, 0.3, 0.37, 0.16, 0.084, button_timeattack)
gravity_button = button(board_width, board_height, 0.3, 0.46, 0.16, 0.084, button_gravity)
back_right_button = button(board_width, board_height, 0.75, 0.66, 0.16, 0.084, button_back)
start_left_button = button(board_width, board_height, 0.35, 0.66, 0.16, 0.084, button_start)
# back and start is same
# sandbox, difficulty board

# number_board1 0.7875, 0.67, 0.0133, 0.075
# number_board2 0.7875, 0.77
# number_board3 0.7875, 0.87
level_minus_vector = button(board_width, board_height, 0.7675, 0.33, 0.04, 0.53, vector_minus)
combo_minus_vector = button(board_width, board_height, 0.7675, 0.42, 0.04, 0.53, vector_minus)
speed_minus_vector = button(board_width, board_height, 0.7675, 0.51, 0.04, 0.53, vector_minus)

level_plus_vector = button(board_width, board_height, 0.8075, 0.33, 0.04, 0.53, vector_plus)
combo_plus_vector = button(board_width, board_height, 0.8075, 0.42, 0.04, 0.53, vector_plus)
speed_plus_vector = button(board_width, board_height, 0.8075, 0.51, 0.04, 0.53, vector_plus)

# level_icon 0.6125, 0.67, 0.16, 0.084
# combo_icon 0.6125, 0.77, 0.16, 0.084
# speed_icon 0.6125, 0.87, 0.16, 0.084

# main page 4) difficulty board
easy_button     = button(board_width, board_height, 0.2, 0.37, 0.16, 0.084, button_easy)
normal_button   = button(board_width, board_height, 0.5, 0.37, 0.16, 0.084, button_normal)
hard_button     = button(board_width, board_height, 0.8, 0.37, 0.16, 0.084, button_hard)

# main page 5) help board
# help board
# help image

# main page 6) leader board

# main page 7) setting board
volume_vector = button(board_width, board_height, 0.425, 0.4, 0.0625, 0.1111, vector_volume)
screen_vector = button(board_width, board_height, 0.575, 0.4, 0.0625, 0.1111, vector_screen)

# main page 8) volume board
allmute_button = button(board_width, board_height, 0.5, 0.24, 0.16, 0.084, button_allmute)

# music_number_board 0.46, 0.38, 0.04, 0.53
music_plus_vector = button(board_width, board_height, 0.38, 0.38, 0.04, 0.53, vector_plus)
music_minus_vector = button(board_width, board_height, 0.54, 0.38, 0.04, 0.53, vector_minus)
music_on_button = button(board_width, board_height, 0.62, 0.38, 0.04, 0.53, vector_sound_on)
music_off_button = button(board_width, board_height, 0.62, 0.38, 0.04, 0.53, vector_sound_off)

# effect_number_board 0.46, 0.52, 0.04, 0.53
effect_plus_vector = button(board_width, board_height, 0.38, 0.52, 0.04, 0.53, vector_plus)
effect_minus_vector = button(board_width, board_height, 0.54, 0.52, 0.04, 0.53, vector_minus)
effect_on_button = button(board_width, board_height, 0.62, 0.52, 0.04, 0.53, vector_sound_on)
effect_off_button = button(board_width, board_height, 0.62, 0.52, 0.04, 0.53, vector_sound_off)

# main page 9) screen board
smallsize_button = button(board_width, board_height, 0.5, 0.24, 0.2, 0.08, size_s)
midiumsize_button = button(board_width, board_height, 0.5, 0.38, 0.2, 0.08, size_m)
bigsize_button = button(board_width, board_height, 0.5, 0.52, 0.2, 0.08, size_b)

# main page 10) shop board
bomb_buy_button = button(board_width, board_height, 0.42, 0.24, 0.0925, 0.04, button_buy)
tnt_buy_button = button(board_width, board_height, 0.42, 0.372, 0.0925, 0.04, button_buy)
earth_buy_button = button(board_width, board_height, 0.526, 0.24, 0.0925, 0.04, button_buy)
gold_buy_button = button(board_width, board_height, 0.526, 0.372, 0.0925, 0.04, button_buy)

# game page 1) pause board
resume_button = button(board_width, board_height, 0.5, 0.33, 0.16, 0.084, button_resume)
restart_button = button(board_width, board_height, 0.5, 0.51, 0.16, 0.084, button_restart)
setting_button = button(board_width, board_height, 0.5, 0.69, 0.16, 0.084, button_setting)
quit_game_button = button(board_width, board_height, 0.5, 0.87, 0.16, 0.084, button_quit)

# gmae page 2) setting board
# 위와 동일

# game page 3) volume board
# 위와 동일

# game page 4) screen board
# 위와 동일

# game page 5) game over oard
menu_button = button(board_width, board_height, 0.5, 0.33, 0.04, 0.53, button_menu)
# restart
ok_button = button(board_width, board_height, 0.5, 0.6, 0.04, 0.53, button_ok)

# about debug

level_plus_button = button(board_width, board_height, 0.63, 0.7719, 0.0625, 0.1111, vector_plus)
level_minus_button = button(board_width, board_height, 0.56, 0.7719, 0.0625, 0.1111, vector_minus)
combo_plus_button = button(board_width, board_height, 0.63, 0.9419, 0.0625, 0.1111, vector_plus)
combo_minus_button =button(board_width, board_height, 0.56, 0.9419, 0.0625, 0.1111, vector_minus)
speed_plus_button = button(board_width, board_height, 0.18, 0.12, 0.055, 0.09, vector_plus)
speed_minus_button =button(board_width, board_height, 0.035, 0.12, 0.055, 0.09, vector_minus)


#게임 중 버튼 생성하기위한 버튼객체 리스트 (버튼 전체)
button_list = [
    start_button, help_button, shop_button, quit_button, challenge_vector,
    leader_vector, setting_vector, single_button, pvp_button, sandbox_button,
    difficulty_button, back_button, timeattack_button, gravity_button,
    back_right_button, start_left_button, level_minus_vector, combo_minus_vector,
    speed_minus_vector, level_plus_vector, combo_plus_vector, speed_plus_vector,
    easy_button, normal_button, hard_button, volume_vector, screen_vector, 
    allmute_button, music_plus_vector, music_minus_vector, music_on_button, music_off_button,
    effect_plus_vector, effect_minus_vector, effect_on_button, effect_off_button,
    smallsize_button, midiumsize_button, bigsize_button, bomb_buy_button,
    tnt_buy_button, earth_buy_button, gold_buy_button, resume_button,
    restart_button, setting_button, quit_game_button, menu_button, ok_button,
    level_plus_button, level_minus_button, combo_plus_button, combo_minus_button,
    speed_plus_button, speed_minus_button
]

def set_volume():
    ui_variables.fall_sound.set_volume(effect_volume / 10) #set_volume의 argument는 0.0~1.0으로 이루어져야하기 때문에 소수로 만들어주기 위해 10으로 나눔#
    ui_variables.click_sound.set_volume(effect_volume / 10)
    ui_variables.break_sound.set_volume(effect_volume / 10)
    ui_variables.move_sound.set_volume(effect_volume / 10)
    ui_variables.drop_sound.set_volume(effect_volume / 10)
    ui_variables.single_sound.set_volume(effect_volume / 10)
    ui_variables.double_sound.set_volume(effect_volume / 10)
    ui_variables.triple_sound.set_volume(effect_volume / 10)
    ui_variables.tetris_sound.set_volume(effect_volume / 10)
    ui_variables.LevelUp_sound.set_volume(effect_volume / 10)
    ui_variables.GameOver_sound.set_volume(music_volume / 10)
    ui_variables.intro_sound.set_volume(music_volume / 10)
    pygame.mixer.music.set_volume(music_volume / 10)
    for i in range(1, 10): #10가지의 combo 사운드를 한번에 조절함
        ui_variables.combos_sound[i - 1].set_volume(effect_volume / 10)


def draw_image(window, img_path, x, y, width, height):
    x = x - (width / 2) #해당 이미지의 가운데 x좌표, 가운데 좌표이기 때문에 2로 나눔
    y = y - (height / 2) #해당 이미지의 가운데 y좌표, 가운데 좌표이기 때문에 2로 나눔
    image = pygame.image.load(img_path)
    image = pygame.transform.smoothscale(image, (width, height))
    window.blit(image, (x, y))


# Draw block
def draw_block(x, y, color):
    pygame.draw.rect(
        screen,
        color,
        Rect(x, y, block_size, block_size)
    )
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(x, y, block_size, block_size),
        1
    )


def draw_block_image(x, y, image):
    draw_image(screen, image, x, y, block_size, block_size) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)


# grid[i][j] = 0 / matrix[tx + j][ty + i] = 0에서
# 0은 빈 칸 / 1-7은 테트리스 블록 종류 / 8은 ghost / 9은 장애물(벽돌) 에 해당함 = t_block 참고

# Draw game screen
def draw_board(next1, next2, hold, score, level, goal):
    sidebar_width = int(board_width * 0.5312) #크기 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.pinkpurple,
        Rect(sidebar_width, 0, int(board_width * 0.2375), board_height) #크기 비율 고정
    )

    # Draw next mino 다음 블록
    grid_n1 = tetrimino.mino_map[next1 - 1][0] #(배열이라-1) 다음 블록의 원래 모양
    grid_n2 = tetrimino.mino_map[next2 - 1][0] #(배열이라-1) 다음 블록의 원래 모양

    for i in range(mino_matrix_y): #다음 블록
        for j in range(mino_matrix_x):
            dx1 = int(board_width * 0.025) + sidebar_width + block_size * j #위치 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#
            dy1 = int(board_height * 0.3743) + block_size * i #위치 비율 고정, 전체 board 세로길이에서 원하는 비율을 곱해줌#
            if grid_n1[i][j] != 0: #해당 부분에 블록 존재하면
                draw_block_image(dx1, dy1, ui_variables.t_block[grid_n1[i][j]]) #블록 이미지 출력

    for i in range(mino_matrix_y): #다다음블록
        for j in range(mino_matrix_x):
            dx2 = int(board_width * 0.145) + sidebar_width + block_size * j #위치 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#
            dy2 = int(board_height * 0.3743) + block_size * i #위치 비율 고정, 전체 board 세로길이에서 원하는 비율을 곱해줌#
            if grid_n2[i][j] != 0: #해당 부분에 블록 존재하면
                draw_block_image(dx2, dy2, ui_variables.t_block[grid_n2[i][j]]) #블록 이미지 출력

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]  #(배열이라-1) 기본 모양

    if hold_mino != -1: #hold 존재X
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + block_size * j #위치 비율 고정
                dy = int(board_height * 0.1336) + block_size * i #위치 비율 고정
                if grid_h[i][j] != 0: #해당 부분에 블록이 존재하면
                    draw_block_image(dx, dy, ui_variables.t_block[grid_h[i][j]]) #hold 블록 출력

    # Set max score
    if score > 999999:
        score = 999999 #최대 점수가 999999를 넘기지 못하도록 설정#

    # Draw texts
    #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
    if textsize==False:
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h4.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h4.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(str(combo_count), 1, ui_variables.real_white)
        if debug:
            speed_value = ui_variables.h5.render("SPEED : "+str(framerate), 1, ui_variables.real_white) #speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        if time_attack:
            time = total_time - elapsed_time
            value = ui_variables.h5.render("TIME : "+str(int(time)), 1, ui_variables.real_white)
            screen.blit(value, (int(board_width * -0.445) + sidebar_width, int(board_height * 0.015))) #각각 전체 board 가로길이, 세로길이에 대한 원하는 비율을 곱해줌#
        if attack_mode:
            time = attack_time - elapsed_attack_time
            value = ui_variables.h5.render("TIME : "+str(int(time)), 1, ui_variables.real_white)
            screen.blit(value, (int(board_width * -0.445) + sidebar_width, int(board_height * 0.015))) #각각 전체 board 가로길이, 세로길이에 대한 원하는 비율을 곱해줌#

    if textsize==True: #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
        text_hold = ui_variables.h3.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h3.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h3.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h2.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h3.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h2.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h3.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h2.render(str(combo_count), 1, ui_variables.real_white)
        if debug:
            speed_value = ui_variables.h3.render("SPEED : "+str(framerate), 1, ui_variables.real_white) #speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        if time_attack:
            time = total_time - elapsed_time
            value = ui_variables.h2.render("TIME : "+str(int(time)), 1, ui_variables.real_white)
            screen.blit(value, (int(board_width * -0.445) + sidebar_width, int(board_height * 0.015)))
        if attack_mode:
            time = attack_time - elapsed_attack_time
            value = ui_variables.h5.render("TIME : "+str(int(time)), 1, ui_variables.real_white)
            screen.blit(value, (int(board_width * -0.445) + sidebar_width, int(board_height * 0.015))) #각각 전체 board 가로길이, 세로길이에 대한 원하는 비율을 곱해줌#

    #if time_attack:
    #    time = total_time - elapsed_time
    #    value = ui_variables.h5.render("TIME : "+str(int(time)), 1, ui_variables.real_white)
    #    screen.blit(value, (int(board_width * -0.445) + sidebar_width, int(board_height * 0.015)))
    # Place texts. 위치 비율 고정, 각각 전체 board 가로길이, 세로길이에 대한 원하는 비율을 곱해줌#
    screen.blit(text_hold, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.6791)))
    screen.blit(level_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.7219)))
    screen.blit(text_combo, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.8395)))
    screen.blit(combo_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.8823)))
    if debug:
        screen.blit(speed_value, (int(board_width * 0.065), int(board_height * 0.1)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.25) + block_size * x  #위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.055) + block_size * y #위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + 1]])


def draw_1Pboard(next, hold, score, level, goal):
    sidebar_width = int(board_width * 0.31) #위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.pinkpurple,
        Rect(sidebar_width, 0, int(board_width * 0.1875), board_height) #크기비율 고정, board 가로길이에 원하는 비율을 곱해줌#
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]  #(배열이라-1) 다음 블록의 원래 모양

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx = int(board_width * 0.045) + sidebar_width + block_size * j #위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.3743) + block_size * i #위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            if grid_n[i][j] != 0:
                draw_block_image(dx, dy, ui_variables.t_block[grid_n[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]  #(배열이라-1) 기본 모양

    if hold_mino != -1: #기본값이 -1. 즉 hold블록 존재할 떄
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + block_size * j #위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
                dy = int(board_height * 0.1336) + block_size * i #위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
                if grid_h[i][j] != 0:
                    draw_block_image(dx, dy, ui_variables.t_block[grid_h[i][j]]) #hold 블록 그림

    # Set max score
    if score > 999999:
        score = 999999 #최대 점수가 999999가 넘지 않도록 설정해줌

    # Draw texts
    #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
    if textsize==False:
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h4.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h4.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(str(combo_count), 1, ui_variables.real_white)
    if textsize==True:
        text_hold = ui_variables.h3.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h3.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h3.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h2.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h3.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h2.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h3.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h2.render(str(combo_count), 1, ui_variables.real_white)
    if debug:
        speed_value = ui_variables.h5.render("SPEED : "+str(framerate), 1, ui_variables.real_white) #speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        screen.blit(speed_value, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.015))) #각각 전체 board 가로길이, 세로길이에 원하는 비율을 곱해줌
    screen.blit(text_hold, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width*0.045) + sidebar_width, int(board_height*0.6791)))
    screen.blit(level_value, (int(board_width*0.055) + sidebar_width , int(board_height*0.7219)))
    screen.blit(text_combo, (int(board_width*0.045) + sidebar_width , int(board_height*0.8395)))
    screen.blit(combo_value, (int(board_width*0.055) + sidebar_width, int(board_height*0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.05) + block_size * x #위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
            dy = int(board_height * 0.055) + block_size * y #위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
            draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + 1]])


def draw_2Pboard(next, hold, score, level, goal):
    sidebar_width = int(board_width * 0.82) #위치 비율 고정, , board의 가로길이에 원하는 비율을 곱해줌

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.pinkpurple,
        Rect(sidebar_width, 0, int(board_width * 0.1875), board_height) #크기 비율 고정, , board의 가로길이에 원하는 비율을 곱해줌, Rect(x축, y축, 가로길이, 세로길이)#
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(mino_matrix_y):  # 16개의 그리드 칸에서 true인 값만 뽑아서 draw.rect
        for j in range(mino_matrix_x):
            dx = int(board_width * 0.05) + sidebar_width + block_size * j  #위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
            dy = int(board_height * 0.3743) + block_size * i  #위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
            if grid_n[i][j] != 0:
                draw_block_image(dx, dy, ui_variables.t_block[grid_n[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino_2P != -1:  #기본값이 -1. 즉 hold블록 존재할 떄
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + block_size * j  #위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
                dy = int(board_height * 0.1336) + block_size * i  #위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
                if grid_h[i][j] != 0:
                    draw_block_image(dx, dy, ui_variables.t_block[grid_h[i][j]])

    # Set max score
    if score > 999999:
        score = 999999 #최대 점수가 999999가 넘지 못하도록 설정#

    #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래 코드의 숫자 1=안티에일리어싱 적용에 대한 코드
    if textsize==False:
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h4.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h4.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(str(combo_count), 1, ui_variables.real_white)
    if textsize==True:
        text_hold = ui_variables.h4.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h4.render("NEXT", 1, ui_variables.real_white)
        text_score = ui_variables.h4.render("SCORE", 1, ui_variables.real_white)
        score_value = ui_variables.h3.render(str(score), 1, ui_variables.real_white)
        text_level = ui_variables.h4.render("LEVEL", 1, ui_variables.real_white)
        level_value = ui_variables.h3.render(str(level), 1, ui_variables.real_white)
        text_combo = ui_variables.h4.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h3.render(str(combo_count), 1, ui_variables.real_white)
    if debug:
        speed_value = ui_variables.h5.render("SPEED : "+str(framerate_2P), 1, ui_variables.real_white) #speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        screen.blit(speed_value, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.015))) #각각 전체 board의 가로길이, 세로길이에 대해 원하는 비율을 곱해줌
    screen.blit(text_hold, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) + sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) + sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width*0.045) + sidebar_width, int(board_height*0.6791)))
    screen.blit(level_value, (int(board_width*0.055) + sidebar_width , int(board_height*0.7219)))
    screen.blit(text_combo, (int(board_width*0.045) + sidebar_width , int(board_height*0.8395)))
    screen.blit(combo_value, (int(board_width*0.055) + sidebar_width, int(board_height*0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.54) + block_size * x #위치비율 고정
            dy = int(board_height * 0.055) + block_size * y #위치비율 고정
            draw_block_image(dx, dy, ui_variables.t_block[matrix_2P[x][y + 1]])


# Draw a tetrimino
def draw_mino(x, y, mino, r, matrix): #mino는 모양, r은 회전된 모양 중 하나
    grid = tetrimino.mino_map[mino - 1][r] #grid : 출력할 테트리스

    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r, matrix): #테트리스가 바닥에 존재하면 true -> not이니까 바닥에 없는 상태
        ty += 1 #한칸 밑으로 하강

    # Draw ghost
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[tx + j][ty + i] = 8 #테트리스가 쌓일 위치에 8 이라는 ghost 만듦

    # Draw mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[x + j][y + i] = grid[i][j] #해당 위치에 블록 만듦

# Erase a tetrimino
def erase_mino(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r]

    # Erase ghost
    for j in range(board_y+1):
        for i in range(board_x):
            if matrix[i][j] == 8: #테트리스 블록에서 해당 행렬위치에 ghost블록 존재하면
                matrix[i][j] = 0  #없애서 빈 곳으로 만들기

    # Erase mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[x + j][y + i] = 0 #해당 위치에 블록 없애서 빈 곳으로 만들기

# Returns true if mino is at bottom
def is_bottom(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (y + i + 1) > board_y :   #바닥의 y좌표에 있음(바닥에 닿음)
                    return True
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8: #그 블록위치에 0, 8 아님(즉 블록 존재 함)
                    return True

    return False

def gravity(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r] #grid : 출력할 테트리스

    for j in range(mino_matrix_x-1, -1, -1): #mino_matrix 4*4 배열이므로 -1 해서 3, 2, 1, 0 index로 for문을 돎
        for i in range(mino_matrix_y-1, -1, -1):  #mino_matrix 4*4 배열이므로 -1 해서 3, 2, 1, 0 index로 for문을 돎
            if grid[i][j] != 0: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                dy = y
                if ((dy + i) == board_y or (matrix[x + j][dy + i+1] != 0)) : #바닥에 닿았거나, 해당 위치 아랫칸에 블록이 이미 존재하는 경우
                    matrix[x+j][dy+i] = grid[i][j] #그 위치에 그대로 테트리스 블록을 둠
                else :
                    while((dy + 1 + i) <= board_y and (matrix[x + j][dy + i + 1] == 0)): #바닥에 닿지 않았으며, 해당 위치 아랫칸에 블록이 없는 경우 (= 공중에 떠있는 경우)
                        dy+=1 #이 조건에서 벗어날 때까지 계속해서 한 칸씩 밑으로 떨어뜨림
                        matrix[x+j][dy+i] = 9  #떨어지는 블록은 장애물 블록으로 표현
                        matrix[x+j][dy+i-1] = 0  #블록이 한칸 떨어졌으니, 그 위의 기존블록 또는 만들어두었던 장애물 블록은 빈칸으로 처리함(없앰)

def attack(y,matrix):
    for i in range(board_x): # 가로줄 전체에 대해서
        matrix[i][y] = 9 # 맨 밑줄부터 장애물 블록으로 채워짐

# Returns true if mino is at the left edge
def is_leftedge(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j - 1) < 0:  #맨 왼쪽에 위치함
                    return True
                elif matrix[x + j - 1][y + i] != 0:  #그 위치의 왼쪽에 이미 무엇인가 존재함
                    return True

    return False

# Returns true if mino is at the right edge
def is_rightedge(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0: #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j + 1) >= board_x :  #맨 오른쪽에 위치
                    return True
                elif matrix[x + j + 1][y + i] != 0:   #그 위치의 오른쪽에 이미 무엇인가 존재함
                    return True

    return False

def is_turnable_r(x, y, mino, r, matrix):
    if r != 3:  #회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino - 1][r + 1] #3이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino - 1][0] #3이면 0번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y :  #테트리스 matrix크기 벗어나면 못돌림
                    return False
                elif matrix[x + j][y + i] != 0:  #해당 자리에 이미 블록이 있으면 못돌림
                    return False
    return True

# Returns true if turning left is possible
def is_turnable_l(x, y, mino, r, matrix):
    if r != 0:  #회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino - 1][r - 1]  #0이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino - 1][3] #0이면 3번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  #테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y:  #테트리스 matrix크기 벗어나면 못돌림
                    return False
                elif matrix[x + j][y + i] != 0: #해당 자리에 이미 블록이 있으면 못돌림
                    return False

    return True

# Returns true if new block is drawable
def is_stackable(mino, matrix):
    grid = tetrimino.mino_map[mino - 1][0] #grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0 and matrix[3 + j][i] != 0: ###
                return False

    return True


def draw_multiboard(next_1P, hold_1P, next_2P, hold_2P, score1P, score2P, level1P, level2P, goal1P, goal2P):
    screen.fill(ui_variables.real_white)
    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
    draw_1Pboard(next_1P, hold_1P, score1P, level1P, goal1P)
    draw_2Pboard(next_2P, hold_2P, score2P, level2P, goal2P)


def set_vol(val):
    volume = int(val) / 100 #set_volume argenment로 넣기 위해서(소수점을 만들어주기 위해서) 100으로 나눠줌
    print(volume)
    ui_variables.click_sound.set_volume(volume)

def set_music_playing_speed(CHANNELS, swidth, Change_RATE):
    spf = wave.open('assets/sounds/SFX_BattleMusic.wav', 'rb')
    RATE = spf.getframerate()
    signal = spf.readframes(-1)
    if os.path.isfile('assets/sounds/SFX_BattleMusic_Changed.wav'):
        pygame.mixer.quit()
        os.remove('assets/sounds/SFX_BattleMusic_Changed.wav')
        pygame.mixer.init()
    wf = wave.open('assets/sounds/SFX_BattleMusic_Changed.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(swidth)
    wf.setframerate(RATE * Change_RATE)
    wf.writeframes(signal)
    wf.close()

    pygame.mixer.music.load('assets/sounds/SFX_BattleMusic_Changed.wav')
    pygame.mixer.music.play(-1) #위 노래를 반복재생하기 위해 play(-1)로 설정


def set_music_playing_speed(CHANNELS, swidth, Change_RATE):
    spf = wave.open('assets/sounds/SFX_BattleMusic.wav', 'rb')
    RATE = spf.getframerate()
    signal = spf.readframes(-1)
    if os.path.isfile('assets/sounds/SFX_BattleMusic_Changed.wav'):
        pygame.mixer.quit()
        os.remove('assets/sounds/SFX_BattleMusic_Changed.wav')
        pygame.mixer.init()
    wf = wave.open('assets/sounds/SFX_BattleMusic_Changed.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(swidth)
    wf.setframerate(RATE * Change_RATE)
    wf.writeframes(signal)
    wf.close()

    pygame.mixer.music.load('assets/sounds/SFX_BattleMusic_Changed.wav')
    pygame.mixer.music.play(-1) #위 노래를 반복재생하기 위해 play(-1)로 설정

def set_initial_values():
    global combo_count, combo_count_2P, gravity_mode, score, level, goal, score_2P, level_2P, goal_2P, bottom_count, bottom_count_2P, hard_drop, hard_drop_2P, attack_point, attack_point_2P, dx, dy, dx_2P, dy_2P, rotation, rotation_2P, mino, mino_2P, next_mino1, next_mino2, next_mino1_2P, hold, hold_2P, hold_mino, hold_mino_2P, framerate, framerate_2P, matrix, matrix_2P, Change_RATE, blink, start, pause, done, game_over, leader_board, setting, volume_setting, screen_setting, pvp, help, debug, d, e, b, u, g, time_attack, start_ticks, textsize, CHANNELS, swidth, name_location, name, previous_time, current_time, pause_time, lines, leaders, volume, game_status, framerate_blockmove, framerate_2P_blockmove, game_speed, game_speed_2P, sandbox, difficulty, shop, challenge, single, game
    framerate = 30 # Bigger -> Slower  기본 블록 하강 속도, 2도 할만 함, 0 또는 음수 이상이어야 함
    framerate_blockmove = framerate * 3 # 블록 이동 시 속도
    game_speed = framerate * 20 # 게임 기본 속도
    framerate_2P = 30 # 2P
    framerate_2P_blockmove = framerate_2P * 3 # 블록 이동 시 속도
    game_speed_2P = framerate_2P * 20 # 2P 게임 기본 속도


    # Initial values
    blink = False
    start = False
    sandbox = False
    difficulty = False
    shop = False
    challenge = False
    pause = False
    done = False
    game_over = False
    leader_board = False
    setting = False
    volume_setting = False
    screen_setting = False
    single = False
    game = False
    pvp = False
    help = False
    gravity_mode = False #이 코드가 없으면 중력모드 게임을 했다가 Restart해서 일반모드로 갈때 중력모드로 게임이 진행됨#
    debug = False
    d = False
    e = False
    b = False
    u = False
    g = False
    time_attack = False
    start_ticks = pygame.time.get_ticks()
    textsize = False

    attack_mode = False # 어택모드
    attack_mode_time = False # 어택모드 30초마다 시간 초기화하도록
    attack_board_y = 20  #장애물 블록 밑에서부터 생성하도록 board_y와 똑같이 설정
    

    # 게임 음악 속도 조절 관련 변수
    CHANNELS = 1
    swidth = 2
    Change_RATE = 2

    combo_status = False
    combo_count = 0
    combo_count_2P = 0
    score = 0
    level = 1
    goal = level * 5
    score_2P = 0
    level_2P = 1
    goal_2P = level_2P * 5
    bottom_count = 0
    bottom_count_2P = 0
    hard_drop = False
    hard_drop_2P = False
    attack_point = 0
    attack_point_2P = 0

    dx, dy = 3, 0  # Minos location status
    dx_2P, dy_2P = 3, 0
    rotation = 0  # Minos rotation status
    rotation_2P = 0
    mino = randint(1, 7)  # Current mino #테트리스 블록 7가지 중 하나
    mino_2P = randint(1, 7)
    next_mino1 = randint(1, 7)  # Next mino1 # 다음 테트리스 블록 7가지 중 하나
    next_mino2 = randint(1, 7)  # Next mino2 # 다음 테트리스 블록 7가지 중 하나
    next_mino1_2P = randint(1, 7)
    hold = False  # Hold status
    hold_2P = False
    hold_mino = -1  # Holded mino #현재 hold하는 것 없는 상태
    hold_mino_2P = -1
    textsize = False

    name_location = 0
    name = [65, 65, 65]

    previous_time = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()
    pause_time = pygame.time.get_ticks()

    with open('leaderboard.txt') as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in open('leaderboard.txt')]  #leaderboard.txt 한줄씩 읽어옴

    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
    for i in lines:
        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

    matrix = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix
    matrix_2P = [[0 for y in range(height + 1)] for x in range(width)]  # Board matrix

    volume = 1.0 # 필요 없는 코드, effect_volume으로 대체 가능
    ui_variables.click_sound.set_volume(volume) # 필요 없는 코드, 전체 코드에서 click_sound를 effect_volume로 설정하는 코드 하나만 있으면 됨
    pygame.mixer.init()
    ui_variables.intro_sound.set_volume(music_volume / 10)
    ui_variables.break_sound.set_volume(effect_volume / 10) # 소리 설정 부분도 set_volume 함수에 넣으면 됨
    ui_variables.intro_sound.play()
    game_status = ''
    pygame.mixer.music.load("assets/sounds/SFX_BattleMusic.wav")

set_initial_values()
pygame.time.set_timer(pygame.USEREVENT, 10)

###########################################################
# Loop Start
###########################################################

while not done:

    # Pause screen
    # ui_variables.click_sound.set_volume(volume)

    if volume_setting: #volume board complete
        pause_surface = screen.convert_alpha() #투명 가능하도록
        pause_surface.fill((0, 0, 0, 0)) #투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)]) #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0)) #위치 비율 고정
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5,
        int(board_width*0.8), int(board_height*0.8)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        if single:
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
        if pvp:
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

        #draw_image(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        draw_image(screen, board_volume, board_width * 0.5, board_height * 0.7,
                     int(board_width*0.8), int(board_height*0.8))
        draw_image(screen, board_number, board_width * 0.46, board_height * 0.38,
                    int(board_width * 0.04), int(board_height * 0.53))
        draw_image(screen, board_number, board_width * 0.46, board_height * 0.52,
                    int(board_width * 0.04), int(board_height * 0.53))
        allmute_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색#
        effect_plus_vector.draw(screen, (0, 0, 0))
        effect_minus_vector.draw(screen, (0, 0, 0))
        music_plus_vector.draw(screen, (0, 0, 0))
        music_minus_vector.draw(screen, (0, 0, 0))
        effect_on_button.draw(screen,(0,0,0))
        music_on_button.draw(screen,(0,0,0))
        back_button.draw(screen, (0, 0, 0))
        allmute_button.draw(screen, (0, 0, 0))

        #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
        music_volume_text = ui_variables.h5.render('Music Volume', 1, ui_variables.grey_1)
        effect_volume_text = ui_variables.h5.render('Effect Volume', 1, ui_variables.grey_1)
        screen.blit(music_volume_text, (board_width * 0.4, board_height * 0.4)) #위치 비율 고정
        screen.blit(effect_volume_text, (board_width * 0.4, board_height * 0.6)) #위치 비율 고정

        music_volume_text = ui_variables.h5.render('Music On/Off', 1, ui_variables.grey_1)
        effect_volume_text = ui_variables.h5.render('Effect On/Off', 1, ui_variables.grey_1)
        screen.blit(music_volume_text, (board_width * 0.6, board_height * 0.4)) #위치 비율 고정
        screen.blit(effect_volume_text, (board_width * 0.6, board_height * 0.6)) #위치 비율 고정

        music_volume_size_text = ui_variables.h4.render(str(music_volume), 1, ui_variables.grey_1)
        effect_volume_size_text = ui_variables.h4.render(str(effect_volume), 1, ui_variables.grey_1)
        screen.blit(music_volume_size_text, (board_width * 0.46, board_height * 0.38)) #위치 비율 고정
        screen.blit(effect_volume_size_text, (board_width * 0.46, board_height * 0.52)) #위치 비율 고정

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초로 설정

                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = button_back_clicked
                else:
                    back_button.image = back_button

                if effect_plus_vector.isOver(pos):
                    effect_plus_vector.image = vector_plus_clicked
                else:
                    effect_plus_vector.image = vector_plus

                if effect_minus_vector.isOver(pos):
                    effect_minus_vector.image = vector_minus_clicked
                else:
                    effect_minus_vector.image = vector_minus

                if music_plus_vector.isOver(pos):
                    music_plus_vector.image = vector_plus_clicked
                else:
                    music_plus_vector.image = vector_plus

                if music_minus_vector.isOver(pos):
                    music_minus_vector.image = vector_minus_clicked
                else:
                    music_minus_vector.image = vector_minus

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    volume_setting = False
                if music_plus_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume >= 10: #음량 최대크기
                        music_volume = 10
                    else:
                        music_on_button.image = vector_sound_on
                        music_volume += 1
                if music_minus_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume <= 0: #음량 최소크기
                        music_volume = 0
                        music_on_button.image=vector_sound_off
                    else:
                        if music_volume == 1:
                            music_on_button.image=vector_sound_off
                            music_volume -= 1
                        else:
                            music_on_button.image=vector_sound_on
                            music_volume -= 1
                if effect_plus_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume >= 10: #음량 최대크기
                        effect_volume = 10
                    else:
                        effect_on_button.image=vector_sound_on
                        effect_volume += 1
                if effect_minus_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume <= 0: #음량 최소크기
                        effect_volume = 0
                        effect_on_button.image=vector_sound_off
                    else:
                        if effect_volume == 1:
                            effect_on_button.image=vector_sound_off
                            effect_volume -= 1
                        else:
                            effect_on_button.image=vector_sound_on
                            effect_volume -= 1
                #음소거 추가#
                if music_on_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume == 0 :
                        music_volume = 5 #중간 음량으로
                        music_on_button.image=vector_sound_on
                    else:
                        music_volume = 0
                        music_off_button.draw(screen,(0,0,0)) #rgb(0,0,0) = 검정색
                        music_on_button.image=vector_sound_off
                if effect_on_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume == 0 :
                        effect_volume = 5  #중간 음량으로
                        effect_on_button.image=vector_sound_on
                    else:
                        effect_volume = 0
                        effect_off_button.draw(screen,(0,0,0))
                        effect_on_button.image=vector_sound_off
                if allmute_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if (effect_volume == 0) and (music_volume == 0):
                        music_volume = 5  #중간 음량으로
                        effect_volume = 5  #중간 음량으로
                        allmute_button.image=button_allmute
                    else:
                        music_volume = 0 #최소 음량으로
                        effect_volume = 0 #최소 음량으로
                        allmute_button.image=button_allmute_on

                set_volume()

    elif screen_setting: # screen board complete 
        pause_surface = screen.convert_alpha() #투명 가능하도록
        pause_surface.fill((0, 0, 0, 0)) #투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)]) #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5,
        int(board_width*0.8), int(board_height*0.8)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        
        if single:
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
        if pvp:
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

        draw_image(screen, board_screen, board_width * 0.5, board_height * 0.7,
                     int(board_width*0.8), int(board_height*0.8))
        smallsize_button.draw(screen, (0, 0, 0))
        bigsize_button.draw(screen, (0, 0, 0))
        midiumsize_button.draw(screen, (0, 0, 0))
        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초로 설정
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = button_back_clicked
                else:
                    back_button.image = button_back

                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    screen_setting = False
                if smallsize_button.isOver(pos):
                    ui_variables.click_sound.play()
                    board_width = 800
                    board_height = 450
                    block_size = int(board_height * 0.045) #블록 크기 비율 고정
                    screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                    textsize=False

                    for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)
                    pygame.display.update()

                if midiumsize_button.isOver(pos):
                    ui_variables.click_sound.play()
                    board_width = 1200
                    board_height = 675
                    block_size = int(board_height * 0.045) #블록 크기 비율 고정
                    screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                    textsize=True

                    for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

                    pygame.display.update()

                if bigsize_button.isOver(pos):
                    ui_variables.click_sound.play()
                    board_width = 1600
                    board_height = 900
                    block_size = int(board_height * 0.045) #블록 크기 비율 고정
                    screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                    textsize=True

                    for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)
                    pygame.display.update()

    elif setting: # setting board little complete
        pause_surface = screen.convert_alpha() #투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  #투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)]) #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5,
        int(board_width*0.8), int(board_height*0.8)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        
        if single:
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
        if pvp:
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
        
        draw_image(screen, board_setting, board_width * 0.5, board_height * 0.5,
          int(board_width*0.8), int(board_height*0.8)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)

        screen_vector.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        volume_vector.draw(screen, (0, 0, 0))

        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초로 설정
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = button_back_clicked
                else:
                    back_button.image = button_back

                if volume_vector.isOver(pos):
                    volume_vector.image = vector_volume_clicked
                else:
                    volume_vector.image = volume_vector

                if screen_vector.isOver(pos):
                    screen_vector.image = vector_screen_clicked
                else:
                    screen_vector.image = screen_vector

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = False

                if volume_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    volume_setting = True

                if screen_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    screen_setting = True

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045) #블록 크기 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif pause: # pause board in game little complete
        pygame.mixer.music.pause()

        if single:
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
        if pvp:
            draw_image(screen, gamebackground_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
            draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

        draw_image(screen, board_pause, board_width * 0.5, board_height * 0.5, int(board_height * 0.7428), board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        resume_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        restart_button.draw(screen, (0, 0, 0))
        setting_button.draw(screen, (0, 0, 0))
        quit_game_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초
                pygame.display.update()
            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                if event.key == K_ESCAPE:
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.mixer.music.unpause()
                    pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초

            elif event.type == pygame.MOUSEMOTION:
                if resume_button.isOver(pos):
                    resume_button.image = button_resume_clicked
                else:
                    resume_button.image = button_resume

                if restart_button.isOver(pos):
                    restart_button.image = button_restart_clicked
                else:
                    restart_button.image = button_restart

                if setting_button.isOver(pos):
                    setting_button.image = button_setting_clicked
                else:
                    setting_button.image = button_setting_clicked
                if quit_game_button.isOver(pos):
                    quit_game_button.image = button_quit_clicked
                else:
                    quit_game_button.image = button_quit
                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if quit_game_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    done = True
                if setting_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    setting = True
                if restart_button.isOver_2(pos):
                    ui_variables.click_sound.play()

                    pause = False
                    start = False

                    if pvp:
                        pvp = False

                if resume_button.isOver(pos):
                    pygame.mixer.music.unpause()
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif help: # help board little complete
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5,
        int(board_width*0.8), int(board_height*0.8)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        
        pause_surface = screen.convert_alpha()  #투명 가능하도록
        pause_surface.fill((0, 0, 0, 0)) #투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)])  #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))

        draw_image(screen, board_help, board_width * 0.5, board_height * 0.7, 
        int(board_width * 0.8), int(board_height * 0.8)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        draw_image(screen, 'assets/vector/help_image.png',
        board_width * 0.5, board_height * 0.444,
        int(board_width * 0.5), int(board_height * 0.5)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)

        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = button_back_clicked
                else:
                    back_button.image = button_back
                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    help = False

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045) #board 세로길이에 원하는 비율을 곱해줌
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif start: # start board little complete
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        draw_image(screen, board_start, board_width * 0.5, board_height * 0.4,  int(board_width*0.8), int(board_height*0.8)) 
        single_button.draw(screen, (0, 0, 0))
        pvp_button.draw(screen, (0, 0, 0))
        sandbox_button.draw(screen, (0, 0, 0))
        difficulty_button.draw(screen, (0, 0, 0))
        back_button.draw(screen, (0, 0, 0))
        pause_surface = screen.convert_alpha()
        pause_surface.fill((0,0,0,0))
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)]) #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0)) 
 

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초로 설정
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = button_back_clicked
                else:
                    back_button.image = button_back

                if single_button.isOver(pos):
                    single_button.image = button_single_clicked
                else:
                    single_button.image = button_single

                if pvp_button.isOver(pos):
                    pvp_button.image = button_pvp_clicked
                else:
                    pvp_button.image = button_pvp

                if sandbox_button.isOver(pos):
                    sandbox_button.image = button_sandbox_clicked
                else:
                    sandbox_button.image = button_sandbox

                if difficulty_button.isOver(pos):
                    difficulty_button.image = button_difficulty_clicked
                else:
                    difficulty_button.image = button_difficulty

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    start = False
                if single_button.isOver(pos):
                    ui_variables.click_sound.play()
                    single = True
                    game = True
                    previous_time = pygame.time.get_ticks()
                    initalize = True
                    pygame.mixer.music.play(-1) #play(-1) = 노래 반복재생
                    ui_variables.intro_sound.stop()
                if pvp_button.isOver(pos):
                    ui_variables.click_sound.play()
                    pvp = True
                    game = True
                    previous_time = pygame.time.get_ticks()
                    initalize = True
                    pygame.mixer.music.play(-1) #play(-1) = 노래 반복재생
                    ui_variables.intro_sound.stop()
                if difficulty_button.isOver(pos):
                    ui_variables.click_sound.play()
                    difficulty = True
                if sandbox_button.isOver(pos):
                    ui_variables.click_sound.play()
                    sandbox = True
 

                pygame.display.update()

        # Game screen
    
    elif sandbox: # sandbox board little complete
        timeattack_button.draw(screen, (0, 0, 0))
        gravity_button.draw(screen, (0, 0, 0))
        back_right_button.draw(screen, (0, 0, 0))
        start_left_button.draw(screen, (0, 0, 0))
        draw_image(screen, icon_level, board_width * 0.6125, board_height * 0.67,
        int(board_width*0.16), int(board_height*0.084))
        draw_image(screen, icon_combo, board_width * 0.6125, board_height * 0.77,
        int(board_width*0.16), int(board_height*0.084))
        draw_image(screen, icon_speed, board_width * 0.6125, board_height * 0.87,
        int(board_width*0.16), int(board_height*0.084))
        draw_image(screen, board_number, board_width * 0.7875, board_height * 0.67,
        int(board_width*0.04), int(board_height*0.53))
        draw_image(screen, board_number, board_width * 0.7875, board_height * 0.77,
        int(board_width*0.04), int(board_height*0.53))
        draw_image(screen, board_number, board_width * 0.7875, board_height * 0.87,
        int(board_width*0.04), int(board_height*0.53))
        level_minus_vector.draw(screen,(0,0,0))
        combo_minus_vector.draw(screen,(0,0,0))
        speed_minus_vector.draw(screen,(0,0,0))
        level_plus_vector.draw(screen,(0,0,0))
        combo_plus_vector.draw(screen,(0,0,0))
        speed_plus_vector.draw(screen,(0,0,0))

        pause_surface = screen.convert_alpha()
        pause_surface.fill((0,0,0,0))
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)]) #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))
        draw_image(screen, board_sandbox, board_width * 0.5, board_height * 0.7,
             int(board_width*0.8), int(board_height*0.8))  


        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초로 설정
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_right_button.isOver(pos):
                    back_right_button.image = button_back_clicked
                else:
                    back_right_button.image = button_back 

                if start_left_button.isOver(pos):
                    start_left_button.image = button_start_clicked
                else:
                    start_left_button.image = button_start

                if timeattack_button.isOver(pos):
                    timeattack_button.image = button_timeattack_clicked
                else:
                    timeattack_button.image = button_timeattack

                if gravity_button.isOver(pos):
                    gravity_button.image = button_gravity_clicked
                else:
                    gravity_button.image = button_gravity

                if level_minus_button.isOver(pos):
                    level_minus_button.image = vector_minus_clicked
                else:
                    level_minus_button.image = vector_minus

                if level_plus_button.isOver(pos):
                    level_plus_button.image = vector_plus_clicked
                else:
                    level_plus_button.image = vector_plus

                if combo_minus_button.isOver(pos):
                    combo_minus_button.image = vector_minus_clicked
                else:
                    combo_minus_button.image = vector_minus

                if combo_plus_button.isOver(pos):
                    combo_plus_button.image = vector_plus_clicked
                else:
                    combo_plus_button.image = vector_plus

                if speed_minus_button.isOver(pos):
                    speed_minus_button.image = vector_minus_clicked
                else:
                    speed_minus_button.image = vector_minus

                if speed_plus_button.isOver(pos):
                    speed_plus_button.image = vector_plus_clicked
                else:
                    speed_plus_button.image = vector_plus

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_right_button.isOver(pos):
                    ui_variables.click_sound.play()
                    sandbox = False
                                
                if start_left_button.isOver(pos):
                    ui_variables.click_sound.play()
                    game = True

                if timeattack_button.isOver(pos):
                    if timeattack:
                        ui_variables.click_sound.play()
                        timeattack = False
                        timeattack_button.image = button_timeattack
                    else:
                        ui_variables.click_sound.play()
                        timeattack = True
                        timeattack_button.image = button_timeattack_on
                                    
                if gravity_button.isOver(pos):
                    if gravity_mode:
                        ui_variables.click_sound.play()
                        gravity_mode = False
                        gravity_button.image = button_gravity
                    else :
                        ui_variables.click_sound.play()
                        gravity_mode = True
                        gravity_button.image = button_gravity_on
                                  
                if level_minus_button.isOver(pos):
                    ui_variables.click_sound.play()
                                  
                if level_plus_button.isOver(pos):
                    ui_variables.click_sound.play()
                                    
                if combo_minus_button.isOver(pos):
                    ui_variables.click_sound.play()
                                   
                if combo_plus_button.isOver(pos):
                    ui_variables.click_sound.play()
                                   
                if speed_minus_button.isOver(pos):
                    ui_variables.click_sound.play()
                                    
                if speed_plus_button.isOver(pos):
                    ui_variables.click_sound.play()

    elif difficulty: # diff board little complete
        draw_image(screen, board_difficulty, board_width * 0.5, board_height * 0.7, int(board_width * 0.8), int(board_height * 0.8))
        back_right_button.draw(screen, (0, 0, 0))
        start_left_button.draw(screen, (0, 0, 0))
        easy_button.draw(screen, (0, 0, 0))
        normal_button.draw(screen, (0, 0, 0))
        hard_button.draw(screen, (0,0,0))

        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_right_button.isOver(pos):
                    back_right_button.image = button_back_clicked
                else:
                    back_right_button.image = button_back

                if start_left_button.isOver(pos):
                    start_left_button.image = button_start_clicked
                else:
                    start_left_button.image = button_start

                if easy_button.isOver(pos):
                    easy_button.image = button_easy_clicked
                else:
                    easy_button.image = button_easy

                if normal_button.isOver(pos):
                    normal_button.image = button_normal_clicked
                else:
                    normal_button.image = button_normal

                if hard_button.isOver(pos):
                    hard_button.image = button_hard_clicked
                else:
                    hard_button.image = button_hard

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_right_button.isOver(pos):
                    ui_variables.click_sound.play()
                    difficulty = False
                if start_left_button.isOver(pos):
                    ui_variables.click_sound.play()
                    start = True
                if easy_button.isOver(pos):
                    ui_variables.click_sound.play()
                if normal_button.isOver(pos):
                    ui_variables.click_sound.play()
                if hard_button.isOver(pos):
                    ui_variables.click_sound.play()
                                   
    elif leader_board: # leader little complete        
        pause_surface = screen.convert_alpha() #투명 가능하도록
        pause_surface.fill((0, 0, 0, 0)) #투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)])  #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))

        draw_image(screen, board_leader, board_width * 0.5, board_height * 0.7,
            int(board_height * 0.8),int(board_height*0.8))

        back_button.draw(screen, (0, 0, 0))

        #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
        leader_1 = ui_variables.h1_b.render('1st ' + leaders[0][0] + ' ' + str(leaders[0][1]), 1, ui_variables.grey_1)
        leader_2 = ui_variables.h1_b.render('2nd ' + leaders[1][0] + ' ' + str(leaders[1][1]), 1, ui_variables.grey_1)
        leader_3 = ui_variables.h1_b.render('3rd ' + leaders[2][0] + ' ' + str(leaders[2][1]), 1, ui_variables.grey_1)
        screen.blit(leader_1, (board_width * 0.3, board_height * 0.15)) #위치 비율 고정
        screen.blit(leader_2, (board_width * 0.3, board_height * 0.35)) #위치 비율 고정
        screen.blit(leader_3, (board_width * 0.3, board_height * 0.55)) #위치 비율 고정

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초
                pygame.display.update()
            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                if event.key == K_ESCAPE:
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = button_back_clicked
                else:
                    back_button.image = button_back
                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    leader_board = False

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    elif shop: # shop little complete
        bomb_buy_button.draw(screen, (0, 0, 0))
        tnt_buy_button.draw(screen, (0, 0, 0))
        earth_buy_button.draw(screen, (0, 0, 0))
        gold_buy_button.draw(screen, (0, 0, 0))

        #배경 약간 어둡게
        pause_surface = screen.convert_alpha()  #투명 가능하도록
        pause_surface.fill((0, 0, 0, 0)) #투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(board_width), int(board_height)])  #(screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))

        draw_image(screen, board_shop, board_width * 0.5, board_height * 0.7, 
            int(board_width * 0.8), int(board_height * 0.8)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)

        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image=button_back_clicked
                else:
                    back_button.image=button_back

                if bomb_buy_button.isOver(pos):
                    bomb_buy_button.image=button_buy_clicked
                else:
                    bomb_buy_button.image=button_buy

                if tnt_buy_button.isOver(pos):
                    tnt_buy_button.image=button_buy_clicked
                else:
                    tnt_buy_button.image=button_buy

                if earth_buy_button.isOver(pos):
                    earth_buy_button.image=button_buy_clicked
                else:
                    earth_buy_button.image=button_buy

                if gold_buy_button.isOver(pos):
                    gold_buy_button.image=button_buy_clicked
                else:
                    gold_buy_button.image=button_buy

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    shop = False

                if bomb_buy_button.isOver(pos):
                    ui_variables.click_sound.play()

                if tnt_buy_button.isOver(pos):
                    ui_variables.click_sound.play()

                if earth_buy_button.isOver(pos):
                    ui_variables.click_sound.play()

                if gold_buy_button.isOver(pos):
                    ui_variables.click_sound.play()

    elif challenge: # challenge little complete
        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5,
            int(board_width*0.8), int(board_height*0.8)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        start_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        shop_button.draw(screen, (0, 0, 0))
        help_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        setting_vector.draw(screen, (0, 0, 0))
        challenge_vector.draw(screen, (0, 0, 0))
        leader_vector.draw(screen, (0, 0, 0))
        draw_image(screen, board_challenge, board_width * 0.5, board_height * 0.7, 
            int(board_width * 0.8), int(board_height * 0.8)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        back_button.draw(screen,(0, 0, 0))

    elif game:
        if time_attack:
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 경과 시간 계산
        if attack_mode:
            if attack_mode_time == False:
                current_attack_ticks = pygame.time.get_ticks() # 어택모드 진입했을 때의 시간
                attack_mode_time = True
            elapsed_attack_time = (pygame.time.get_ticks() - current_attack_ticks) / 1000
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, framerate) #프레임 시간만큼 빠르게 소프트드롭
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, game_speed)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation, matrix)
                screen.fill(ui_variables.real_white)
                draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                pygame.display.update()

                current_time = pygame.time.get_ticks()
                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation, matrix)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation, matrix):
                    dy += 1

                # Create new mino: 중력 모드
                elif gravity_mode:
                    if hard_drop or bottom_count == 6:
                        if gravity(dx, dy, mino, rotation, matrix):
                            erase_mino(dx, dy, mino, rotation, matrix)
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        screen.fill(ui_variables.real_white)
                        draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        pygame.display.update()
                        if is_stackable(next_mino1, matrix):
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            ui_variables.GameOver_sound.play()
                            start = False
                            game_status = 'start'
                            game_over = True
                            gravity_mode = False
                            pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초
                    else:
                        bottom_count += 1

                # Create new mino: 일반 모드
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation, matrix)
                        screen.fill(ui_variables.real_white)
                        draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        pygame.display.update()
                        if is_stackable(next_mino1, matrix):
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            ui_variables.GameOver_sound.play()
                            start = False
                            game_status = 'start'
                            game_over = True
                            pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초
                    else:
                        bottom_count += 1

                # Erase line
                erase_count = 0
                rainbow_count = 0
                matrix_contents = []
                combo_value = 0

                for j in range(board_y+1):
                    is_full = True
                    for i in range(board_x):
                        if matrix[i][j] == 0 or matrix[i][j] == 9 : #빈 공간이거나, 장애물블록
                            is_full = False
                    if is_full: # 한 줄 꽉 찼을 때
                        erase_count += 1
                        k = j
                        combo_value += 1
                        combo_status = True

                        #rainbow보너스 점수
                        rainbow = [1,2,3,4,5,6,7] #각 mino에 해당하는 숫자
                        for i in range(board_x):
                            matrix_contents.append(matrix[i][j]) #현재 클리어된 줄에 있는 mino 종류들 저장
                        rainbow_check = list(set(matrix_contents).intersection(rainbow)) #현재 클리어된 줄에 있는 mino와 mino의 종류중 겹치는 것 저장
                        if rainbow == rainbow_check: #현재 클리어된 줄에 모든 종류 mino 있다면
                            rainbow_count += 1

                        while k > 0:
                            for i in range(board_x):
                                matrix[i][k] = matrix[i][k - 1]  # 남아있는 블록 한 줄씩 내리기(덮어쓰기)
                            k -= 1
                if erase_count >= 1:
                    if rainbow_count >= 1:
                        score += 500 * rainbow_count #임의로 rainbow는 한 줄당 500점으로 잡음
                        rainbow_count = 0 #다시 초기화
                        screen.blit(ui_variables.rainbow_vector, (board_width * 0.28, board_height * 0.1)) #blit(이미지, 위치)
                        pygame.display.update()
                        pygame.time.delay(400) #0.4초

                    previous_time = current_time
                    
                    #점수 계산
                    if erase_count == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        score += 50 * level * erase_count + combo_count
                        combo_count += 1
                    elif erase_count == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        score += 150 * level * erase_count + 2 * combo_count
                        combo_count += 2
                    elif erase_count == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        score += 350 * level * erase_count + 3 * combo_count
                        combo_count += 3
                    elif erase_count == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        score += 1000 * level * erase_count + 4 * combo_count
                        combo_count += 4
                        screen.blit(ui_variables.combo_4ring, (250, 160)) #blit(이미지, 위치)
                    total_time += 5 # 콤보 시 시간 5초 연장

                    for i in range(1, 11):
                        if combo_count == i:  # 1 ~ 10 콤보 이미지
                            screen.blit(ui_variables.large_combos[i - 1], (board_width * 0.27, board_height * 0.35)) #각 콤보 이미지에 대해 blit(이미지, 위치)
                            pygame.display.update()
                            pygame.time.delay(500)
                        elif combo_count > 10:  # 11 이상 콤보 이미지
                            pygame.display.update()
                            pygame.time.delay(300)

                    for i in range(1, 9): # 1~8의 콤보 사운드
                        if combo_count == i + 2:  # 3 ~ 11 콤보 사운드
                            ui_variables.combos_sound[i - 1].play()
                        if combo_count > 11:
                            ui_variables.combos_sound[8].play()
                if current_time - previous_time > 10000: #10초가 지나면
                    previous_time = current_time #현재 시간을 과거시간으로 하고
                    combo_count = 0 #콤보 수 초기화
                if current_time - previous_time > 1000: #콤보만들고 1초 뒤에
                    combo_status = False #combo_Status가 true가 된 걸 false로 바꿔줌


                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    ui_variables.LevelUp_sound.play()
                    goal += level * 5
                    framerate = int(framerate-speed_change)
                    Change_RATE += 1
                    set_music_playing_speed(CHANNELS, swidth, Change_RATE)

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation, matrix):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                    pygame.display.update()
                elif event.key == K_j :
                    framerate = int(framerate-speed_change)
                    print(framerate)

                # Hold
                elif event.key == K_RSHIFT : #keyboard 변경하기
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

                #dx, dy는 각각 좌표위치 이동에 해당하며, rotation은 mino.py의 테트리스 블록 회전에 해당함
                # Turn right
                elif event.key == K_UP:
                    if is_turnable_r(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Turn left
                elif event.key == K_m:
                    if is_turnable_l(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)

                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    screen.fill(ui_variables.real_white)
                    draw_image(screen, gamebackground_image , board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                # rainbow test
                elif event.key == K_F1:
                    ui_variables.click_sound.play()
                    matrix[0][20] = 7 #빨
                    matrix[1][20] = 7 #빨
                    matrix[2][20] = 3#주
                    matrix[3][20] = 3#주
                    matrix[4][20] = 4#노
                    matrix[5][20] = 5#초
                    matrix[6][20] = 5#초
                    matrix[7][20] = 1#하
                    matrix[8][20] = 2#파
                    mino = 6
                # debug mode block change
                elif debug:
                    if event.key == K_1:
                        ui_variables.click_sound.play()
                        mino = 1 #빨
                    if event.key == K_2:
                        ui_variables.click_sound.play()
                        mino = 2 #빨
                    if event.key == K_3:
                        ui_variables.click_sound.play()
                        mino = 3 #빨
                    if event.key == K_4:
                        ui_variables.click_sound.play()
                        mino = 4 #빨
                    if event.key == K_5:
                        ui_variables.click_sound.play()
                        mino = 5 #빨
                    if event.key == K_6:
                        ui_variables.click_sound.play()
                        mino = 6 #빨
                    if event.key == K_7:
                        ui_variables.click_sound.play()
                        mino = 7 #빨

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

            elif event.type == pygame.MOUSEMOTION:
                if debug:
                    if level_plus_button.isOver(pos):
                        level_plus_button.image = vector_plus_clicked
                    else:
                        level_plus_button.image = vector_plus
                    if level_minus_button.isOver(pos):
                        level_minus_button.image = vector_minus_clicked
                    else:
                        level_minus_button.image = vector_minus
                    if combo_plus_button.isOver(pos):
                        combo_plus_button.image = vector_plus_clicked
                    else:
                        combo_plus_button.image = vector_plus
                    if combo_minus_button.isOver(pos):
                        combo_minus_button.image = vector_minus_clicked
                    else:
                        combo_minus_button.image = vector_minus
                    if speed_plus_button.isOver(pos):
                        speed_plus_button.image = vector_plus_clicked
                    else:
                        speed_plus_button.image = vector_plus
                    if speed_minus_button.isOver(pos):
                        speed_minus_button.image = vector_minus_clicked
                    else:
                        speed_minus_button.image = vector_minus

                    pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if debug:
                    if level_plus_button.isOver(pos):
                        ui_variables.click_sound.play()
                        if level < 15:
                            level += 1
                            goal += level * 5
                            Change_RATE = level + 1
                            set_music_playing_speed(CHANNELS, swidth, Change_RATE)
                    if level_minus_button.isOver(pos):
                        ui_variables.click_sound.play()
                        if level > 1:
                            level -= 1
                            goal += level * 5
                            Change_RATE = level + 1
                            set_music_playing_speed(CHANNELS, swidth, Change_RATE)
                    if combo_plus_button.isOver(pos):
                        ui_variables.click_sound.play()
                        combo_count += 1
                    if combo_minus_button.isOver(pos):
                        ui_variables.click_sound.play()
                        if combo_count > 0:
                            combo_count -= 1
                    if speed_plus_button.isOver(pos):
                        ui_variables.click_sound.play()
                        if framerate <= 28:
                            framerate = int(framerate + speed_change)
                    if speed_minus_button.isOver(pos):
                        ui_variables.click_sound.play()
                        if framerate > 2:
                            framerate = int(framerate - speed_change)
                    pygame.display.update()

        if time_attack and total_time - elapsed_time < 0: #타임어택 모드이면서, 60초가 지났으면
            ui_variables.GameOver_sound.play()
            start = False
            game_status = 'start'
            game_over = True
            time_attack = False
            pygame.time.set_timer(pygame.USEREVENT, 1)

        if attack_mode: #어택모드일 때 
            if attack_time - elapsed_attack_time < 0: # attack_time이 다 지났을 때 
                attack(attack_board_y,matrix) 
                attack_mode_time = False #elapsed_attack_time 초기화 
                attack_board_y -= 1 #장애물 블록 만든 윗 줄에 다음 장애물블록 생성하도록
            elif combo_status == True: #콤보 만들어졌을 때
                attack_mode_time = False #elapsed_attack_time 초기화

        pygame.display.update()

    elif pvp:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_s]: #프레임만큼의 시간으로 소프트드롭 되도록 함
                        pygame.time.set_timer(pygame.USEREVENT, framerate)
                    elif keys_pressed[K_DOWN] :  #프레임만큼의 시간으로 소프트드롭 되도록 함
                        pygame.time.set_timer(pygame.USEREVENT, framerate_2P)
                    else :
                        pygame.time.set_timer(pygame.USEREVENT, game_speed)  #기본 게임속도
                        pygame.time.set_timer(pygame.USEREVENT, game_speed_2P)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation, matrix)
                draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation, matrix)
                    erase_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation, matrix):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        draw_mino(dx, dy, mino, rotation, matrix)

                        if is_stackable(next_mino1, matrix):
                            mino = next_mino1
                            # next_mino1 = next_mino2
                            next_mino1 = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                            score += 10 * level
                        else:  # 더이상 쌓을 수 없으면 게임오버
                            pvp = True
                            game_status = 'pvp'

                            if score >= score_2P :
                                draw_image(screen, board_gameover,board_width * 0.15, board_height * 0.5, int(board_width * 0.25), int(board_height * 0.45)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                            else :
                                ui_variables.GameOver_sound.play()
                                draw_image(screen,pvp_lose_image,board_width * 0.15, board_height * 0.5, int(board_width * 0.25), int(board_height * 0.6)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                                draw_image(screen,pvp_win_image,board_width * 0.6, board_height * 0.5, int(board_width * 0.25), int(board_height * 0.55)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                                pvp = False
                                pygame.mixer.music.stop()
                                if game_status == 'start':
                                    start = True
                                    pygame.mixer.music.play(-1)
                                if game_status == 'pvp':
                                    pvp = True
                                    pygame.mixer.music.play(-1)
                                ui_variables.click_sound.play()
                                game_over = False
                                pause = False
                    else:
                        bottom_count += 1

                # Move mino down
                if not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                    dy_2P += 1

                # Create new mino
                else:
                    if hard_drop_2P or bottom_count_2P == 6:
                        hard_drop_2P = False
                        bottom_count_2P = 0
                        draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)

                        if is_stackable(next_mino1_2P, matrix_2P):
                            mino_2P = next_mino1_2P
                            next_mino1_2P = randint(1, 7)
                            dx_2P, dy_2P = 3, 0
                            rotation_2P = 0
                            hold_2P = False
                            score_2P += 10 * level_2P
                        else:  # 더이상 쌓을 수 없으면 게임오버
                            pvp = True
                            gagame_status = 'pvp'
                            if score <= score_2P :
                                draw_image(screen, board_gameover,board_width * 0.6, board_height * 0.5, int(board_width * 0.25), int(board_height * 0.45)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                            else :
                                ui_variables.GameOver_sound.play()
                                draw_image(screen,pvp_win_image,board_width * 0.15, board_height * 0.5, int(board_width * 0.25), int(board_height * 0.55)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                                draw_image(screen,pvp_lose_image,board_width * 0.6, board_height * 0.5, int(board_width * 0.25), int(board_height * 0.6)) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                                pvp = False
                                pygame.mixer.music.stop()
                                if game_status == 'start':
                                    start = True
                                    pygame.mixer.music.play(-1)
                                if game_status == 'pvp':
                                    pvp = True
                                    pygame.mixer.music.play(-1)
                                ui_variables.click_sound.play()
                                game_over = False
                                pause = False
                    else:
                        bottom_count_2P += 1

                # Erase line
                # 콤보 카운트
                erase_count = 0
                erase_count_2P = 0
                combo_value = 0
                combo_value_2P = 0
                attack_line = 0
                attack_line_2P = 0

                for j in range(board_y+1):
                    is_full = True
                    for i in range(board_x):
                        if matrix[i][j] == 0 or matrix[i][j] == 9: #빈 곳이거나 장애물 블록이 있는 경우
                            is_full = False #클리어 되지 못함
                    if is_full:
                        erase_count += 1
                        attack_line += 1
                        k = j
                        combo_value += 1
                        while k > 0: #y좌표가 matrix 안에 있는 동안
                            for i in range(board_x): #해당 줄의 x좌표들 모두
                                matrix[i][k] = matrix[i][k - 1] #한줄씩 밑으로 내림
                            k -= 1

                for j in range(board_y+1):
                    is_full = True
                    for i in range(board_x):
                        if matrix_2P[i][j] == 0 or matrix_2P[i][j] == 9: #빈 곳이거나 장애물 블록이 있는 경우
                            is_full = False #클리어 되지 못함
                    if is_full:
                        erase_count_2P += 1
                        attack_line_2P += 1
                        k = j
                        combo_value_2P += 1
                        while k > 0:  #y좌표가 matrix 안에 있는 동안
                            for i in range(board_x): #해당 줄의 x좌표들 모두
                                matrix_2P[i][k] = matrix_2P[i][k - 1] #한줄씩 밑으로 내림
                            k -= 1

                while attack_line >= 1 : #2p에게 공격 보내기
                    for i in range(board_x):
                        if matrix_2P[i][board_y-attack_point] == 0 : #비어있는 공간을
                            matrix_2P[i][board_y-attack_point] = 9 #모두 장애물 블록으로 채움
                    attack_line -= 1
                    attack_point += 1


                while attack_line_2P >= 1 :  #1p에게 공격 보내기
                    for i in range(board_x):
                        if matrix[i][board_y-attack_point_2P] == 0 : #비어있는 공간을
                            matrix[i][board_y-attack_point_2P] = 9 #모두 장애물 블록으로 채움
                    attack_line_2P -= 1
                    attack_point_2P += 1

                #1P
                if erase_count >= 1:
                    combo_count += 1
                    if erase_count == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        score += 50 * level * erase_count + combo_count

                    elif erase_count == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        score += 150 * level * erase_count + 2 * combo_count

                    elif erase_count == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        score += 350 * level * erase_count + 3 * combo_count

                    elif erase_count == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        score += 1000 * level * erase_count + 4 * combo_count

                        screen.blit(ui_variables.combo_4ring, (250, 160)) #blit(이미지, 위치)


                    for i in range(1, 11):
                        if combo_count == i:  # 1 ~ 10 콤보 이미지
                            screen.blit(ui_variables.large_combos[i - 1], (124, 190))  # blits the combo number
                        elif combo_count > 10:  # 11 이상 콤보 이미지
                            screen.blit(tetris4, (100, 190))  # blits the combo number

                    for i in range(1, 10):
                        if combo_count == i + 2:  # 3 ~ 11 콤보 사운드
                            ui_variables.combos_sound[i - 1].play()

                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    ui_variables.LevelUp_sound.play()
                    goal += level * 5
                    framerate = int(framerate - speed_change)
                if level > level_2P and Change_RATE < level + 1:
                    Change_RATE += 1
                    set_music_playing_speed(CHANNELS, swidth, Change_RATE)
                #2P
                if erase_count_2P >= 1:
                    combo_count_2P += 1
                    if erase_count_2P == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        score_2P += 50 * level_2P * erase_count_2P + combo_count_2P

                    elif erase_count_2P == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        score_2P += 150 * level_2P * erase_count_2P + 2 * combo_count_2P

                    elif erase_count_2P == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        score_2P += 350 * level_2P * erase_count_2P + 3 * combo_count_2P

                    elif erase_count_2P == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        score_2P += 1000 * level_2P * erase_count_2P + 4 * combo_count_2P

                        screen.blit(ui_variables.combo_4ring, (250, 160)) #blit(이미지, 위치)

                    for i in range(1, 11):
                        if combo_count_2P == i:  # 1 ~ 10 콤보 이미지
                            screen.blit(ui_variables.large_combos[i - 1], (124, 190)) #blit(이미지, 위치)
                        elif combo_count_2P > 10:  # 11 이상 콤보 이미지
                            screen.blit(tetris4, (100, 190)) #blit(이미지, 위치)

                    for i in range(1, 10):
                        if combo_count_2P == i + 2:  # 3 ~ 11 콤보 사운드
                            ui_variables.combos_sound[i - 1].play()

                # Increase level
                goal_2P -= erase_count_2P
                if goal_2P < 1 and level_2P < 15:
                    level_2P += 1
                    ui_variables.LevelUp_sound.play()
                    goal_2P += level_2P * 5
                    framerate_2P = int(framerate_2P - speed_change)
                if level < level_2P and Change_RATE < level_2P + 1:
                    Change_RATE += 1
                    set_music_playing_speed(CHANNELS, swidth, Change_RATE)

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                erase_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)

                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True

                #dx, dy는 각각 좌표위치 이동에 해당하며, rotation은 mino.py의 테트리스 블록 회전에 해당함
                # Hard drop
                elif event.key == K_e: #왼쪽창#
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation, matrix):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                elif event.key == K_SPACE: #오른쪽창#
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        dy_2P += 1
                    hard_drop_2P = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate_2P)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                # Hold
                elif event.key == K_LSHIFT:
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino1
                            next_mino1 = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                elif event.key == K_RSHIFT:
                    if hold_2P == False:
                        ui_variables.move_sound.play()
                        if hold_mino_2P == -1:
                            hold_mino_2P = mino_2P
                            mino_2P = next_mino1_2P
                            next_mino1_2P = randint(1, 7)
                        else:
                            hold_mino_2P, mino_2P = mino_2P, hold_mino_2P
                        dx_2P, dy_2P = 3, 0
                        rotation_2P = 0
                        hold_2P = True
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                # Turn right
                elif event.key == K_w: #왼쪽창#
                    if is_turnable_r(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                elif event.key == K_UP: #오른쪽창#
                    if is_turnable_r(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        rotation_2P += 1
                    # Kick
                    elif is_turnable_r(dx_2P, dy_2P - 1, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 1
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P + 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 1
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P - 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 1
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P, dy_2P - 2, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 2
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P + 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 2
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P - 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 2
                        rotation_2P += 1
                    if rotation_2P == 4:
                        rotation_2P = 0
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                # Turn left
                elif event.key == K_q:
                    if is_turnable_l(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation -= 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation -= 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation -= 1
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                elif event.key == K_m: #오른쪽창#
                    if is_turnable_l(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        rotation_2P -= 1
                    # Kick
                    elif is_turnable_l(dx_2P, dy_2P - 1, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 1
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P + 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 1
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P - 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 1
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P, dy_2P - 2, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 2
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P + 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 2
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P - 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 2
                        rotation_2P -= 1
                    if rotation_2P == -1:
                        rotation_2P = 3
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                # Move left
                elif event.key == K_a:  # key = pygame.key.get_pressed()
                    if not is_leftedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate_blockmove)
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                # Move right
                elif event.key == K_d:
                    if not is_rightedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate_blockmove)
                        dx += 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate_2P_blockmove)
                        dx_2P -= 1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)
                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate_2P_blockmove)
                        dx_2P += 1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P, score, score_2P, level, level_2P, goal, goal_2P)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045) #블록 크기비율 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

        pygame.display.update()

    # Game over screen
    elif game_over:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.mixer.music.stop()
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초

                draw_image(screen, board_gameover, board_width * 0.5, board_height * 0.5, int(board_height * 0.7428), board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)
                menu_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
                restart_button.draw(screen, (0, 0, 0))
                ok_button.draw(screen, (0, 0, 0))

                #render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
                name_1 = ui_variables.h1_b.render(chr(name[0]), 1, ui_variables.pinkpurple)
                name_2 = ui_variables.h1_b.render(chr(name[1]), 1, ui_variables.pinkpurple)
                name_3 = ui_variables.h1_b.render(chr(name[2]), 1, ui_variables.pinkpurple)

                underbar_1 = ui_variables.h1_b.render("_", 1, ui_variables.pinkpurple)
                underbar_2 = ui_variables.h1_b.render("_", 1, ui_variables.pinkpurple)
                underbar_3 = ui_variables.h1_b.render("_", 1, ui_variables.pinkpurple)

                screen.blit(name_1, (int(board_width * 0.434), int(board_height * 0.55))) #blit(요소, 위치), 각각 전체 board의 가로길이, 세로길이에다가 원하는 비율을 곱해줌
                screen.blit(name_2, (int(board_width * 0.494), int(board_height * 0.55))) #blit(요소, 위치)
                screen.blit(name_3, (int(board_width * 0.545), int(board_height * 0.55))) #blit(요소, 위치)

                if blink:
                    blink = False
                else:
                    if name_location == 0:
                        screen.blit(underbar_1, ((int(board_width * 0.437), int(board_height * 0.56)))) #위치 비율 고정
                    elif name_location == 1:
                        screen.blit(underbar_2, ((int(board_width * 0.497), int(board_height * 0.56)))) #위치 비율 고정
                    elif name_location == 2:
                        screen.blit(underbar_3, ((int(board_width * 0.557), int(board_height * 0.56)))) #위치 비율 고정
                    blink = True

                pygame.display.update()

            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    ui_variables.click_sound.play()

                    #1p점수만 저장함
                    outfile = open('leaderboard.txt', 'a')
                    outfile.write(chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                    outfile.close()

                    game_over = False
                    pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초

                #name은 3글자로 name_locationd은 0~2, name[name_location]은 영어 아스키코드로 65~90.
                elif event.key == K_RIGHT:
                    if name_location != 2:
                        name_location += 1
                    else:
                        name_location = 0
                    pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초
                elif event.key == K_LEFT:
                    if name_location != 0:
                        name_location -= 1
                    else:
                        name_location = 2
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_UP:
                    ui_variables.click_sound.play()
                    if name[name_location] != 90:
                        name[name_location] += 1
                    else:
                        name[name_location] = 65
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_DOWN:
                    ui_variables.click_sound.play()
                    if name[name_location] != 65:
                        name[name_location] -= 1
                    else:
                        name[name_location] = 90
                    pygame.time.set_timer(pygame.USEREVENT, 1)

            elif event.type == pygame.MOUSEMOTION:
                if resume_button.isOver_2(pos):
                    menu_button.image = button_menu_clicked
                else:
                    menu_button.image = button_menu

                if restart_button.isOver_2(pos):
                    restart_button.image = button_restart_clicked
                else:
                    restart_button.image = button_restart

                if ok_button.isOver_2(pos):
                    ok_button.image = button_ok_clicked
                else:
                    ok_button.image = button_ok

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button.isOver(pos):
                    ui_variables.click_sound.play()
                    #현재 1p점수만 저장함
                    outfile = open('leaderboard.txt', 'a')
                    outfile.write(chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                    outfile.close()
                    game_over = False
                    pygame.time.set_timer(pygame.USEREVENT, 1)

                if menu_button.isOver(pos):
                    ui_variables.click_sound.play()
                    game_over = False

                if restart_button.isOver_2(pos):
                    if game_status == 'start':
                        start = True
                        pygame.mixer.music.play(-1) #play(-1) = 노래 반복재생
                    if game_status == 'pvp':
                        pvp = True
                        pygame.mixer.music.play(-1)
                    if game_status == 'gravity_mode':
                        gravity_mode = True
                        pygame.mixer.music.play(-1)
                    if game_status == 'time_attack':
                        time_attack = True
                        pygame.mixer.music.play(-1)
                    ui_variables.click_sound.play()
                    game_over = False
                    pause = False

                if resume_button.isOver_2(pos):
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1) #0.001초

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045) #블록 크기비율 고정
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

    # Start screen
    else:
        # 변수 선언 및 초기화
        if initalize:
            set_initial_values()
        initalize = False

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300) #0.3초

            elif event.type == KEYDOWN:
                # space로 start loop 진입하면 배경음악 안 들려서 주석 처리
                # if event.key == K_SPACE:
                #     ui_variables.click_sound.play()
                #     start = True

                #F1 버튼으로 중력모드 진입
                if event.key == K_F1:
                    ui_variables.click_sound.play()
                    if not gravity_mode:
                        gravity_mode = True
                    else:
                        gravity_mode = False

                #d, e, b, u, g 입력으로 디버그모드 진입
                if event.key == K_d:
                    if not d:
                        d = True
                    else:
                        d = False
                if event.key == K_e:
                    if not e:
                        e = True
                    else:
                        e = False
                if event.key == K_b:
                    if not b:
                        b = True
                    else:
                        b = False
                if event.key == K_u:
                    if not u:
                        u = True
                    else:
                        u = False
                if event.key == K_g:
                    if not g:
                        g = True
                    else:
                        g = False

                #t 입력으로 타임어택모드 진입
                if event.key == K_t:
                    if not time_attack:
                        ui_variables.click_sound.play()
                        time_attack = True # 이 상태로 start loop 들어가면 time_attack 모드 실행
                    else:
                        ui_variables.click_sound.play()
                        time_attack = False

            elif event.type == pygame.MOUSEMOTION:
                if start_button.isOver(pos):
                    start_button.image = button_start_clicked
                else:
                    start_button.image = button_start

                if shop_button.isOver(pos):
                    shop_button.image = button_shop_clicked
                else:
                    shop_button.image = button_shop

                if help_button.isOver(pos):
                    help_button.image = button_help_clicked
                else:
                    help_button.image = button_help

                if quit_button.isOver(pos):
                    quit_button.image = button_quit_clicked
                else:
                    quit_button.image = button_quit

                if setting_vector.isOver(pos):
                    setting_vector.image = vector_setting_clicked
                else:
                    setting_vector.image = vector_setting_clicked

                if leader_vector.isOver(pos):
                    leader_vector.image = vector_leader_clicked
                else:
                    leader_vector.image = vector_leader

                if challenge_vector.isOver(pos):
                    challenge_vector.image = vector_challenge_clicked
                else:
                    challenge_vector.image = vector_challenge

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isOver(pos):
                    ui_variables.click_sound.play()
                    start = True
                if shop_button.isOver(pos):
                    ui_variables.click_sound.play()
                    shop = True
                if leader_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    leader_board = True
                if setting_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = True
                if quit_button.isOver(pos):
                    ui_variables.click_sound.play()
                    done = True
                if help_button.isOver(pos):
                    ui_variables.click_sound.play()
                    help = True
                if challenge_vector.isOver(pos):
                    ui_variables.click_sound.play()
                    challenge = True


            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height: #최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)): #높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    board_width = int(board_height / board_rate) #너비를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate) #높이를 적정 비율로 바꿔줌
                if board_width>= mid_width: #화면 사이즈가 큰 경우
                    textsize=True #큰 글자크기 사용
                if board_width < mid_width: #화면 사이즈가 작은 경우
                    textsize=False #작은 글자크기 사용

                block_size = int(board_height * 0.045) #board 세로길이에 대해 원하는 비율로 곱해줌
                screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

        draw_image(screen, background_image, board_width * 0.5, board_height * 0.5, board_width, board_height) #(window, 이미지주소, x좌표, y좌표, 너비, 높이)

        start_button.draw(screen, (0, 0, 0)) #rgb(0,0,0) = 검정색
        shop_button.draw(screen, (0, 0, 0))
        help_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        leader_vector.draw(screen, (0, 0, 0))
        challenge_vector.draw(screen, (0, 0, 0))
        setting_vector.draw(screen, (0, 0, 0))


        if not game:
            pygame.display.update()

pygame.quit()
