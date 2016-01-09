import pygame,sys, math
from pygame.locals import *
squareCenters = []
ScreenWidth = 640
ScreenHeight = 640
screen = pygame.display.set_mode((ScreenWidth,ScreenHeight))
BoardWidth = BoardHeight = 640
black = (0,0,0)
white = (255,255,255)
gray = (100,100,100)
green = (34,139,34)
violet = (238,130,238)
blue = (0,0,128)
gold = (255,215,0)
colors = [blue, gold]
def drawboard(colors):
    #0 1 2 3 4 5 6 7
    #9 10 11 12 13 14 15  etc
    increment = BoardWidth/8
    index = 1 #toswitchcolors (index - 1) * -1
    for column in range(8):
        for row in range(8):
            square = Rect(row*increment,column*increment,increment+1,increment+1)
            if square not in squareCenters:
                squareCenters.append(square)
            pygame.draw.rect(screen,colors[index],square)
            index = (index - 1) * -1
        index = (index - 1) * -1

class ChessPiece(pygame.sprite.Sprite):
    #class for pieces
    def __init__(self, image, position, team):
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (BoardWidth//8-BoardWidth//21, BoardWidth//8-BoardWidth//21))
        self.square = position
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.topleft = position.topleft
        self.rect.center = position.center
    def draw(self, surface):
        surface.blit(self.image,self.rect.topleft)
    def drag(self, cursor):
        self.rect.center=cursor
    def update(self, position):
        self.square = position
        self.rect.center = position.center
    def movelist(self):
        return squareCenters

class Pawn(ChessPiece):
    def __init__(self,image,position,team):
        ChessPiece.__init__(self,image,position,team)
        self.bool = 0
    def movelist(self):
        move_list = []
        removeupto=[]
        noblocks = make_lines(self.square,squareCenters,[math.pi/2])
        takeblocks = make_lines(self.square,squareCenters,[math.pi/4,3*math.pi/4])
        if self.bool<=0:
            for x, y in noblocks:
                move_list.append(x)
                move_list = move_list[len(move_list)-2:len(move_list)]
        else:
             for x, y in make_lines(self.square,squareCenters,[math.pi/2]):
                 move_list.append(x)
             move_list = move_list[len(move_list)-1:len(move_list)]
        for piece in Pieces:
            for item in noblocks:
                if piece.square == item[0]:
                    removeupto.append(item)
                    if item[0] in move_list:
                        move_list.remove(item[0])
        for x in move_list:
            for a, b in removeupto:
                if isfarther(self.square,a,x):
                    move_list.remove(x)
        for block, angle in takeblocks:
            if block.colliderect(self.square):
                for piece in Pieces:
                    if piece.square == block:
                        move_list.append(block)
        return move_list

class BlackPawn(Pawn):
    def movelist(self):
        move_list = []
        removeupto = []
        noblocks = make_lines(self.square,squareCenters,[-math.pi/2])
        takeblocks = make_lines(self.square,squareCenters,[-math.pi/4,-3*math.pi/4])
        if self.bool <= 0:
            for x, y in noblocks:
                move_list.append(x)
            move_list = move_list[0:2]
        else:
             for x, y in make_lines(self.square,squareCenters,[-math.pi/2]):
                 move_list.append(x)
             move_list = move_list[0:1]
        for piece in Pieces:
            for item in noblocks:
                if piece.square == item[0]:
                    removeupto.append(item)
                    if item[0] in move_list:
                        move_list.remove(item[0])
        for x in move_list:
            for a, b in removeupto:
                if isfarther(self.square,a,x):
                    move_list.remove(x)
        for block, angle in takeblocks:
            if block.colliderect(self.square):
                for piece in Pieces:
                    if piece.square == block:
                        move_list.append(block)
        return move_list

class Bishop(ChessPiece):
    def movelist(self):
        removeupto = []
        noblocks = make_lines(self.square,squareCenters,[math.pi/4,3*math.pi/4,-math.pi/4,-3*math.pi/4])
        move_list = []
        for piece in Pieces:
            for item in noblocks:
                if piece.square == item[0]:
                    removeupto.append(item)
        for item in noblocks:
            move_list.append(item[0])
        for x, y in noblocks:
            for a, b in removeupto:
                if isfarther(self.square,a,x) and y ==b and x in move_list:
                    move_list.remove(x)
        return move_list

class Knight(ChessPiece):
    def movelist(self):
        move_list = []
        noblocks = make_lines(self.square,squareCenters,[math.atan2(1,2),math.atan2(2,1),math.atan2(1,-2),math.atan2(-2,1),math.atan2(-1,-2),math.atan2(-2,-1),math.atan2(-1,2),math.atan2(2,-1)])
        adjacent = []
        for square in squareCenters:
            if square.colliderect(self.square):
                adjacent.append(square)
        for square in adjacent:
            for item in noblocks:
                if square.colliderect(item[0]):
                    move_list.append(item[0])
        return move_list

class Rook(ChessPiece):
    def movelist(self):
        removeupto = []
        noblocks = make_lines(self.square,squareCenters,[math.pi,math.pi/2,0,-math.pi/2])
        move_list = []
        for piece in Pieces:
            for item in noblocks:
                if piece.square == item[0]:
                    removeupto.append(item)
        for item in noblocks:
            move_list.append(item[0])
        for x, y in noblocks:
            for a, b in removeupto:
                if isfarther(self.square,a,x) and y ==b and x in move_list:
                    move_list.remove(x)
        return move_list
class Queen(ChessPiece):
    def movelist(self):
        removeupto = []
        noblocks = make_lines(self.square,squareCenters,[math.pi,math.pi/2,0,-math.pi/2,math.pi/4,3*math.pi/4,-math.pi/4,-3*math.pi/4])
        move_list = []
        for piece in Pieces:
            for item in noblocks:
                if piece.square == item[0]:
                    removeupto.append(item)
        for item in noblocks:
            move_list.append(item[0])
        for x, y in noblocks:
            for a, b in removeupto:
                if isfarther(self.square,a,x) and y ==b and x in move_list:
                    move_list.remove(x)
        return move_list

class King(ChessPiece):
    def __init__(self, image, position, team):
        ChessPiece.__init__(self,image,position,team)
        self.bool = 0 #can castle?
    def movelist(self):
        noblocks = make_lines(self.square,squareCenters,[math.pi,math.pi/2,0,-math.pi/2,math.pi/4,3*math.pi/4,-math.pi/4,-3*math.pi/4])
        move_list = []
        for square in squareCenters:
            for piece in Pieces:
                if square.colliderect(self.square):
                    move_list.append(square)
                elif square in move_list and piece.team!=self.team and square in piece.movelist():
                    move_list.remove(square)

        for piece in Pieces:
            if piece.square in move_list and piece.team == self.team:
                move_list.remove(piece.square)
        return move_list
    def undercheck(self):
        for piece in Pieces:
            if self.square in piece.movelist() and piece.team!=self.team:
                return True
        return False
    def checkforcheckmate(self):
        if self.undercheck() and self.movelist() ==[]:
            return True
        else:
            return False

def make_lines(position, positionlist,anglelist):
    #0 top 90 right 180 down 270 left in pygame
    listofpossiblelines = []
    for square in positionlist:
        for angle in anglelist:
            dx = square.centerx - position.centerx
            dy = square.centery - position.centery
            newangle = math.atan2(-dy,dx)
            if angle == newangle:
                listofpossiblelines.append([square, angle])
    return listofpossiblelines

def square(x):
    return x*x

def distanceFormula(pos1, pos2):
    #pos1 and pos2 are tuples of 2 numbers
    return math.sqrt(square(pos2[0]-pos1[0]) + square(pos2[1]-pos1[1]))

def isfarther(start,pos1,pos2):
    #Returns T/F whether pos2 is farther away than pos1
    if type(pos2) == int: #for pawns
        return pos2 > distanceFormula(start.center,pos1)
    else:
        return distanceFormula(start.center,pos2) > distanceFormula(start.center,pos1)

drawboard(colors)

def nearest_piece(position, listof):
    nearest = None
    posCounter = 50000 #a very high number/ could use board dimension^2
    for piece in listof:
        if distanceFormula(piece.rect.center,position) < posCounter:
            nearest = piece
            posCounter = distanceFormula(piece.rect.center,position)
    if posCounter<(BoardWidth/8-30):
        return nearest #only works when close
    else:
        return None


Pieces = [
    Pawn('MEDIA\WhitePawn.png',squareCenters[48],'white'),
    Pawn('MEDIA\WhitePawn.png',squareCenters[49],'white'),
    Pawn('MEDIA\WhitePawn.png',squareCenters[50],'white'),
    Pawn('MEDIA\WhitePawn.png',squareCenters[51],'white'),
    Pawn('MEDIA\WhitePawn.png',squareCenters[52],'white'),
    Pawn('MEDIA\WhitePawn.png',squareCenters[53],'white'),
    Pawn('MEDIA\WhitePawn.png',squareCenters[54],'white'),
    Pawn('MEDIA\WhitePawn.png',squareCenters[55],'white'),

    BlackPawn('MEDIA\BlackPawn.png',squareCenters[8],'black'),
    BlackPawn('MEDIA\BlackPawn.png',squareCenters[9],'black'),
    BlackPawn('MEDIA\BlackPawn.png',squareCenters[10],'black'),
    BlackPawn('MEDIA\BlackPawn.png',squareCenters[11],'black'),
    BlackPawn('MEDIA\BlackPawn.png',squareCenters[12],'black'),
    BlackPawn('MEDIA\BlackPawn.png',squareCenters[13],'black'),
    BlackPawn('MEDIA\BlackPawn.png',squareCenters[14],'black'),
    BlackPawn('MEDIA\BlackPawn.png',squareCenters[15],'black'),


    Bishop('MEDIA\WhiteBishop.png',squareCenters[58],'white'),
    Bishop('MEDIA\WhiteBishop.png',squareCenters[61], 'white'),

    Bishop('MEDIA\BlackBishop.png',squareCenters[2],'black'),
    Bishop('MEDIA\BlackBishop.png',squareCenters[5],'black'),

    Knight('MEDIA\WhiteKnight.png',squareCenters[57],'white'),
    Knight('MEDIA\WhiteKnight.png',squareCenters[62], 'white'),

    Knight('MEDIA\BlackKnight.png',squareCenters[1],'black'),
    Knight('MEDIA\BlackKnight.png',squareCenters[6],'black'),

    Rook('MEDIA\WhiteRook.png',squareCenters[56],'white'),
    Rook('MEDIA\WhiteRook.png',squareCenters[63], 'white'),

    Rook('MEDIA\BlackRook.png',squareCenters[0],'black'),
    Rook('MEDIA\BlackRook.png',squareCenters[7],'black'),


    King('MEDIA\BlackKing.png',squareCenters[4],'black'),
    King('MEDIA\WhiteKing.png',squareCenters[60],'white'),
    Queen('MEDIA\BlackQueen.png',squareCenters[3],'black'),
    Queen('MEDIA\WhiteQueen.png',squareCenters[59],'white')]
