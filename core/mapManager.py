import os, sys, random
import pygame
from pygame.locals import *
from xml.dom.minidom import parse

class MAP(object):
    def __init__(self, WindowManager, screen):
        self._screen = screen
        self._tiles = {}
        self.map = []
        self.elevated = []
        self.occupate = []
    
    def LoadTiles(self, arch):
        print('[*] Loading tiles...')
        tilesArch = parse(arch)
        tilesList = tilesArch.getElementsByTagName('azulejo')
        for tile in tilesList:
            self._tiles[tile.childNodes[0].nodeValue] = pygame.image.load(os.path.join('data', 'images', 'terrain', tile.childNodes[0].nodeValue+'.png'))
            self._tiles[tile.childNodes[0].nodeValue].convert()
    
    def loadLockedTiles(self, arch):
        print('[*] Setting ground height...')
        self.lockedTiles=[]
        tilesArch = parse(arch)
        totalTiles = tilesArch.getElementsByTagName('azulejo')
        for tile in totalTiles:
            self.lockedTiles.append(tile.childNodes[0].nodeValue)
    
    def loadBigTiles(self, arch):
        print('[*] Setting big tiles...')
        self.bigTiles = []
        a = parse(arch)
        tot = a.getElementsByTagName('azulejo')
        for tile in tot:
            self.bigTiles.append(tile.childNodes[0].nodeValue)
    
    def MakeMap(self, arch, pos=0):
        print('[*] Building the world...')
        mapArch = parse(arch)
        MapLines = mapArch.getElementsByTagName('fila')
        for fila in MapLines:
            MapColumns = fila.getElementsByTagName('columna')
            filamapa=[]
            filaAltura = []
            filaOcupado = []
            for column in MapColumns:
                filamapa.append(column.childNodes[0].nodeName)
                filaAltura.append(column.childNodes[0].attributes['altura'].value)
                filaOcupado.append(None)
            self.map.append(filamapa)
            self.elevated.append(filaAltura)
            self.occupate.append(filaOcupado)
    
    def showMap(self, sprite=None, players=None):
        x=20; y=10
        startX = 0
        startY = 0
        posX = posY = 0
        scrollMapX = 0
        scrollMapY = 0
        big = high = 0
        #drawedWin = pygame.Surface([self._screen.get_width(), self._screen.get_height()])
        if sprite:
            scrollMapX = sprite.scrollMapX
            scrollMapY = sprite.scrollMapY
        for line in self.map[scrollMapY:]:
            posY += 1
            posX = -1
            if 380 - (posY*x)+(posX*x) < -20:
                break
            for tile in line[scrollMapX:]:
                if int(self.elevated[posY+scrollMapY][posX+scrollMapX])>1:
                    for elevPos in range(0, int(self.elevated[posY+scrollMapY][posX+scrollMapX])-1):
                        self._screen.blit(self._tiles["baseTierra"], (380 - (posY * x) + (posX * x), 180 + (posY * y) + (posX * y) - (20 * (int(elevPos)))))
                    high -= 20*int(int(self.elevated[posY+scrollMapY][posX+scrollMapX])-1)
                if self.map[posY+scrollMapY][posX+scrollMapX] in self.bigTiles:
                    big -= 80
                posX += 1
                if not 380 - (posY * x) + (posX * x) > 760 - (posY * 19):
                    self._screen.blit(self._tiles[tile], (380 - (posY * x) + (posX * x), 180 + (posY * y) + (posX * y)))
                    if sprite:
                        if posX + scrollMapX == sprite.pos[0] and posY + scrollMapY == sprite.pos[1]:
                            self._screen.blit(sprite.spriteActual, (380 - (posY * x) + ((posX) * x), 180 + (posY * y) + ((posX) * y) - 20))
                big = 0
                high = 0
