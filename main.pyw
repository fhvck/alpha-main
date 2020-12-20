#!/usr/bin/env python

import os
import sys

try:
    from xml.dom.minidom import parse
except ImportError:
    print( "Error: xml.dom.minidom module not found. Verify your python installation.")
    sys.exit(1)

try:
    import random
except ImportError:
    print( "Error: random module not found. Verify your python installation.")
    sys.exit(1)

try:
    import pygame
except ImportError:
    print( "Error: pygame module not installed. Install pygame module.") #TODO add autoinstaller
    sys.exit(1)

try:
    from pygame.locals import *
except ImportError:
    print ("Error: pygame.locals not found. Verify your pygame installation.")
    sys.exit(1)

from core.mapManager import MAP
from core.playerManager import PlayerManager
from core.parser import ParseCommand

# --------------------------------------------------------
# ------------------ D E F I N E S -----------------------
# --------------------------------------------------------

PYGAME_COLOR = ((0, 0, 0),
                (0, 127, 255),
                (99, 175, 255),
                (51, 155, 0),
                (255, 190, 255),
                (230, 146, 150),
                (255, 255, 255),
                (252, 235, 95),
                (0, 0, 0),
                (0, 127, 255),
                (99, 175, 255),
                (51, 155, 0),
                (255, 190, 255),
                (230, 146, 150),
                (255, 255, 255),
                (252, 235, 95))

COLOR_BLACK = 0
COLOR_BLUE = 1
COLOR_CYAN = 2
COLOR_GREEN = 3
COLOR_MAGENTA = 4
COLOR_RED = 5
COLOR_WHITE = 6
COLOR_YELLOW = 7
COLOR_BOLD = 8

FONT_SIZE = 11
SCREEN_SIZE = (1050, 600)

class WindowManager(object):
    def __init__(self, win):
        self._win = win
    
    def centrarItemX(self, item):
        screenX = 800#self._win.get_width() #logo screen is not 1044 but 800
        itemX = item.get_width()
        return (screenX/2)-(itemX/2)
    
    def centrarItemY(self, item):
        screenY = self._win.get_width() #logo height is always 600
        itemY = item.get_width()
        return (screenY/2)-(itemY/2)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
window=WindowManager(screen)

background=pygame.image.load('data/images/background/fondoNoche.png')

font=pygame.font.SysFont('Courier New', 15)
font = font.render('Press Enter to continue or Esc to Exit.', 1, (255,255,255))

logo = [
    pygame.image.load(
        'data/logo/titleLessOne.png'
    ), pygame.image.load(
        'data/logo/titleLessTwo.png'
    ), pygame.image.load(
        'data/logo/titleLessThree.png'
    ), 
]

panel = pygame.image.load(os.path.join("data", 'gui', "SidePanel.png"))
panel.fill((0,0,0)) # always is better in black :)
btfont = pygame.font.Font(os.path.join("data", 'gui', 
                                        "LiberationMono-Bold.ttf"), 
                                        FONT_SIZE)
screen.blit(panel, (1024-224, 0))
input_box = pygame.Rect(100, 100, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
input_box.w=200
#input_box.y = 10
#input_box.x = 824

inpbx_text = ''

count=0
contsprite=0

# define map and player (im calling map as "mappa" cuz map is a python built-in func :) )
tiles=open(os.path.join('data', 'maps', 'azulejos.xml'))
mapfile = open(os.path.join('data', 'maps', 'demo.xml'))
mappa = MAP(window, screen)
mappa.LoadTiles(tiles)
mappa.loadBigTiles(open(os.path.join('data', 'maps', 'bigTiles.xml')))
mappa.loadLockedTiles(open(os.path.join('data', 'maps', 'lockedTiles.xml')))
mappa.MakeMap(mapfile)
print('[*] Game successfully created!')
# make the player object
player=PlayerManager(mappa, 0, 0, 40, 40)

def BorderText(font, text, coul, shift=1):
    """
    Return a surface of white text with black border
    """
    coul_text = (0, 0, 0)
    surf_name = font.render(text, True, coul_text)
    surf = pygame.Surface((surf_name.get_width() + 2 * shift + 1, 
                           surf_name.get_height() + 2 * shift + 1), 
                           pygame.SRCALPHA, 32)
    if shift >= 0:
        for i in range(0, 2 * shift + 1):
            for j in range(0, 2 * shift + 1):
                surf.blit(surf_name, (i, j))

    surf.blit(font.render(text, True, coul), (shift, shift))
    return surf

def _blit_messages(player):
        """
        Blits player messages to the screen
        """
        nb = min((SCREEN_SIZE[1] - 320)/FONT_SIZE, len(player.message))
        nb=int(nb)
        for i in range(nb):
            col_mess = player.message[nb-i-1][1]
            if col_mess > 7:
                shift = 2
            else:
                shift = 1
            screen.blit(BorderText(btfont, player.message[nb-i-1][0],
                              PYGAME_COLOR[col_mess], shift), 
                              (SCREEN_SIZE[0]-250+5, 25 + i * FONT_SIZE*1.5))

def blit_messages():
    smx=int((SCREEN_SIZE[1]-320)/FONT_SIZE)
    nb = len(player.message)-smx
    if nb<0: nb=0
    lim=min(smx,len(player.message))
    for i in range(nb, lim):
        col_mess = player.message[i-1][1]
        if col_mess > 7:
            shift = 2
        else:
            shift = 1
        screen.blit(BorderText(btfont, player.message[i-1][0],
                            PYGAME_COLOR[col_mess], shift), 
                            (SCREEN_SIZE[0]-250+5, 25 + i * FONT_SIZE*1.5))

# --------------------------------------------------------
# ------------------ M A I N  M E N U --------------------
# --------------------------------------------------------

while True:
    # start menu screen
    pygame.event.pump()
    kin = pygame.key.get_pressed()
    screen.blit(background, (0,0))

    count+=1
    flag=False

    if count>=1 and count<300 and not contsprite==0:
        contsprite=0
        flag=True
    elif count>=300 and count<600 and not contsprite==1:
        contsprite=1
        flag=True
    elif count>=600 and count<900 and not contsprite==2:
        contsprite=2
        flag=True
    elif count>=900 and count<1200 and not contsprite==1:
        contsprite=1
        flag=True
    elif count==1200:
        count=0
    
    if flag:
        screen.blit(font, (window.centrarItemX(font), window.centrarItemY(font)))
        screen.blit(logo[contsprite], (window.centrarItemX(logo[contsprite]), window.centrarItemY(logo[contsprite])/2))
        pygame.display.update()
    
    # handle events
    if kin[K_RETURN]:
        break # break this loop and launch the game loop
    elif kin[K_ESCAPE] or pygame.event.peek(QUIT):
        sys.exit() # stop the code

# --------------------------------------------------------
# ---------------------- G A M E -------------------------
# --------------------------------------------------------
clock = pygame.time.Clock()
while True:
    # game loop
    # TODO aggiungi la grafica del player, cambia sprite con il cambio di direzione
    pygame.event.pump()
    if not active:
        kin=pygame.key.get_pressed()
        player.action(kin)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if active:
                print(event, event.key, event.unicode)
                if event.key == K_RETURN or event.key==13:
                    player.add_message(inpbx_text)
                    ParseCommand(inpbx_text)
                    inpbx_text=''
                elif event.key == K_BACKSPACE:
                    inpbx_text = inpbx_text[:-1]
                else:
                    inpbx_text += event.unicode
        elif event.type == MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
        color = color_active if active else color_inactive
    screen.blit(background,(0,0))
    _blit_messages(player)
    text_surface = pygame.font.SysFont('Courier new', 15).render(inpbx_text, True, color)
    screen.blit(text_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, color, input_box, 2)
    mappa.showMap(sprite=player)
    pygame.display.flip()
    #breakpoint()
    clock.tick(40)
    if player.hp<=0:
        break # if player life is under zero stop the loop #TODO add: enter the menuscreen loop

pygame.time.delay(500)