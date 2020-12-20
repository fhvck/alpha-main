import os, sys, random
import pygame
from pygame.locals import *

#FIXME spawn coordinates

COLOR_BLACK = 0
COLOR_BLUE = 1
COLOR_CYAN = 2
COLOR_GREEN = 3
COLOR_MAGENTA = 4
COLOR_RED = 5
COLOR_WHITE = 6
COLOR_YELLOW = 7
COLOR_BOLD = 8

players = []

class Player(pygame.sprite.Sprite):
    def __init__(self, _map, x, y, ancho, alto, spriteArch):
        super().__init__()
        global players
        self.map=_map
        self.spriteIndex = 0
        self.spriteActual = pygame.Surface([ancho, alto])
        self.initial = [x, y]
        self.pos=[x, y]
        self.hp=100
        self.speed=3
        self.acdist=10
        self.direction=0
        self.walkingmen = []
        players.append(self)
        sprites = pygame.image.load(os.path.join('data', 'images', 'character', 'body', spriteArch[0])).convert()
        sprites.set_colorkey(sprites.get_at((0,0)), RLEACCEL)
        spritesAncho, spritesAlto = sprites.get_size()
        for i in range(int(spritesAlto/alto)):
            self.walkingmen.append([])
            for j in range(int(spritesAncho/ancho)):
                self.walkingmen[i].append(sprites.subsurface(j*ancho, i*alto, ancho, alto))
        sprites = pygame.image.load(os.path.join('data', 'images', 'character', 'body', spriteArch[1])).convert()
        sprites.set_colorkey(sprites.get_at((0,0)), RLEACCEL)
        spritesAncho, spritesAlto = sprites.get_size()
        self.personajeGolpeando = []
        for i in range(int(spritesAlto/alto)):
            self.personajeGolpeando.append([])
            for j in range(int(spritesAncho/ancho)):
                self.personajeGolpeando[i].append(sprites.subsurface(j * ancho, i * alto, ancho, alto))
        self.personaje = self.walkingmen
        self.sprite=self.personaje[0][1]
        self.spriteActual=self.sprite
        self.rect = self.spriteActual.get_rect()
        # TODO add moving sprites, so direction too
    
    def nearChar(self):
        if self.pos[1]>0:
            if isinstance(self.map):
                return
    
    def _nextHigher(self, ln, cl):
        if self.map.map[self.pos[1]+ln][self.pos[0]+cl] in self.map.elevated:
            return True
        else:
            return False
    
    def _nextLocked(self, ln, cl):
        if self.map.map[self.pos[1]+ln][self.pos[0]+cl] in self.map.lockedTiles:
            return True
        else:
            return False
    
    def _nextOccupato(self, ln, cl):
        if self.map.map[self.pos[1]+ln][self.pos[0]+cl] in self.map.occupate:
            return True
        else:
            return False
    
    def mover(self, direction):
        incX = incY = 0
        if direction == 1:
            #TODO use self.dir (or //.direction come te pare) to update self.spriteActual
            if self.pos[1]>0:
                incY = -1
                incX = 0
        elif direction == 2:
            if self.pos[1]<len([fila[self.pos[0]] for fila in self.map.map])-1:
                incY = 1
                incX = 0
        elif direction == 3:
            if self.pos[0]>0:
                incY = 0
                incX = -1
        elif direction == 4:
            if self.pos[0] < len(self.map.map[self.pos[1]])-1:
                incY = 0
                incX = 1
        if incX != 0 or incY != 0: variabilechenoncapisco=0
        # TODO add: checka se puoi usare il prossimo tile
        if not self._nextLocked(incY, incX) and not self._nextHigher(incY, incX) and not self._nextOccupato(incY, incX):
            self.map.occupate[self.pos[1]][self.pos[0]] = None
            self.pos[1] += incY
            self.pos[0] += incX
            self.map.occupate[self.pos[1]][self.pos[0]] = self
        #self.pos[0]+=incX
        #self.pos[1]+=incY
    
    def action(self, k):
        return k

    @staticmethod
    def get_players():
        return players

class PlayerManager(Player):
    def __init__(self, _map, x, y, ancho, alto):
        super().__init__(_map, x, y, ancho, alto, ['drackoCaminar.bmp', 'drackoGolpear.bmp'])
        self.scrollMapX=0
        self.scrollMapY=0
        self.message=[]
        global players
        players.remove(self)
    
    def mover(self, direction): # FIXME there r a lot of movement bugs, quando esce dal confine ci sono sempre problemi!!!
        if direction == 1:
            self.direction=2
            if self.pos[1]>0 and not self._nextLocked(-1, 0) and not self._nextHigher(-1, 0) and not self._nextOccupato(-1, 0):
                if (len([fila[self.pos[0]] for fila in self.map.map]) - self.pos[1])-1>16 and self.scrollMapY>0:
                    self.scrollMapY -= 1
        elif direction == 2:
            self.direction=1
            if self.pos[1] < len([fila[self.pos[0]] for fila in self.map.map])-1 and not self._nextHigher(1,0) and not self._nextLocked(1,0) and not self._nextOccupato(1,0):
                if self.pos[1] > 15 and len([fila[self.pos[0]] for fila in self.map.map]) - self.pos[1] > 4 and len([fila[self.pos[0]] for fila in self.map.map][self.scrollMapY:]) > 20:
                    self.scrollMapY += 1
        elif direction == 3:
            self.direction=3
            if self.pos[0]>0 and not self._nextLocked(0, -1) and not self._nextHigher(0, -1) and not self._nextOccupato(0, -1):
                if len(self.map.map[self.pos[1]]) - self.pos[0] > 16 and self.scrollMapX>0:
                    self.scrollMapX -= 1
        elif direction == 4:
            self.direction=0
            if self.pos[0] < len(self.map.map[self.pos[1]]) -1 and not self._nextLocked(0, -1) and not self._nextHigher(0, -1) and not self._nextOccupato(0, -1):
               if self.pos[0] > 15 and len(self.map.map[self.pos[1]]) - self.pos[0] >= 4 and len(self.map.map[self.pos[1]][self.scrollMapX:]) > 20:
                   self.scrollMapX+=1
        super(PlayerManager, self).mover(direction)
    
    def action(self, k):
        if self.acdist >= self.speed:
            self.acdist=0
        else:
            self.acdist+=1
            return
        if self != None: # TODO add life points check
            if k[K_w] or k[K_UP]:
                self.mover(3)
            elif k[K_DOWN] or k[K_s]:
                self.mover(4) 
            elif k[K_LEFT] or k[K_a]:
                self.mover(2)
            elif k[K_RIGHT] or k[K_d]:
                self.mover(1)
            # TODO add gameplay
    
    def anim(self):
        self.spriteActual = pygame.Surface.copy(self.personaje[self.direction][self.spriteIndex])
    
    def add_message(self, message, color=6):
        l = []
        elt = ""
        for word in message.split(' '):
            if len(elt) + len(word) < 30:
                elt += " " + word
            else:
                l.append(elt[1:])
                elt = " " + word
        l.append(elt[1:])
        for mess in l:
            self.message.insert(0, (mess, color))
            if len(self.message) > 100:
                print('over 100')
                self.message=[]
    
    def _action_geteventloop(self, k):
        print('helo')
        print('action manager->',k)
        if self != None: # TODO add life points check
            if k.key==pygame.K_w or k.key==pygame.K_UP:
                self.mover(3)
            elif k.key==K_DOWN or k.key==K_s:
                self.mover(4)
            elif k.key==K_LEFT or k.key==K_a:
                self.mover(2)
            elif k.key==K_RIGHT or k.key==K_d:
                self.mover(1)
            else:
                print(k.key, K_w, K_UP)
            # TODO add gameplay


class RobotBase(Player):
    def __init__(self, mapa, media, x, y, ancho, alto, archivosSprites = ['vivoraCaminar.bmp', 'vivoraGolpear.bmp']):
        super().__init__(mapa, media, x, y, ancho, alto, archivosSprites)
        self.speed=5
    
    def action(self, k):
        if self.acdist > self.speed:
            self.acdist=0
        else:
            self.acdist+=1
            return
        if self != None and not self.hp<0:
            return