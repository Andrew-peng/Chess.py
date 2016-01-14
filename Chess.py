#Created by Andrew Peng
#www.andrew-peng.com
import pygame,sys, math
from pygame.locals import *
from Classes import *

pygame.display.set_caption("ChessBot1.0")
pygame.mixer.init()
FPS = pygame.time.Clock()
pygame.mixer.music.load('MEDIA\Opening.mp3')
pygame.mixer.music.play()
def main():
#Game loop
    Mousedown2 = False
    Mousedown = False
    Mousereleased = False
    TargetPiece = None
    pieceholder = None
    checkmate = False
    check = False
    teams = ['white','black']

    while True:
        turn = teams[0]
        FPS.tick(30)
        checkquitgame()
        pieceholder = None
        if checkmate:
            #game over
            drawboard([gray,violet])
        else:
            drawboard(colors)
        # CursorRect = pygame.rect(pygame.mouse.get_pos(),(1,1))
        Cursor = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                Mousedown = True
                Mousedown2 = True
            if event.type == MOUSEBUTTONUP:
                Mousedown = False
                Mousereleased = True
        if Mousedown and TargetPiece == None:
            TargetPiece = nearest_piece(Cursor,Pieces)
            if TargetPiece != None:
                OriginalPlace = TargetPiece.square
        if Mousedown2 and TargetPiece != None:
            TargetPiece.drag(Cursor)
        if Mousereleased:
            Mousereleased = False
            Mousedown2 = False
            if TargetPiece!=None and TargetPiece.team != turn: #check your turn
                TargetPiece.update(OriginalPlace)
                TargetPiece = None
            elif TargetPiece!=None:
                pos1 = TargetPiece.rect.center
                for square in squareCenters:
                    if distanceFormula(pos1, square.center) < BoardWidth/16: #half width of square
                        newspot = square
                        otherpiece = nearest_piece(square.center, Pieces)
                if True: #always check every turn at beginning
                    for piece in Pieces:
                        if type(piece)==King and piece.team == turn:
                            check = piece.undercheck()
                if otherpiece!=None and otherpiece!=TargetPiece and otherpiece.team ==TargetPiece.team:
                    #check if space is occupied by team
                    TargetPiece.update(OriginalPlace)
                    if check:
                        teams = teams[::-1]#tempfix
                elif newspot not in TargetPiece.movelist():
                    #check if you can move there
                    TargetPiece.update(OriginalPlace)
                    if check:
                        teams = teams[::-1]#tempfix
                elif otherpiece!=None and otherpiece!=TargetPiece and type(otherpiece)!=King:
                    #take enemy piece
                    for piece in Pieces:
                        if piece == otherpiece:
                            pieceholder = piece #temp
                            Pieces.remove(piece)
                            TargetPiece.update(newspot)
                    teams = teams[::-1] #switch teams

                else:
                    #move
                    TargetPiece.update(newspot)
                    if type(TargetPiece) == Pawn or type(TargetPiece) == BlackPawn or type(TargetPiece)==King:
                        TargetPiece.bool += 1
                    teams = teams[::-1] #switch teams

                if True: #always check every turn at end
                    for piece in Pieces:
                        if type(piece)==King and piece.team == turn:
                            check = piece.undercheck()

                if check:
                    #if still under check revert back
                    TargetPiece.update(OriginalPlace)
                    if pieceholder and pieceholder.team!=TargetPiece.team:
                        Pieces.append(pieceholder)
                        pieceholder=None
                    if type(TargetPiece) == Pawn or type(TargetPiece) == BlackPawn or type(TargetPiece)==King:
                        TargetPiece.bool -= 1
                    teams = teams[::-1] #switch back
            TargetPiece = None
        for piece in Pieces:
            piece.draw(screen)
        pygame.display.flip()


def checkquitgame():
    for event in pygame.event.get(QUIT):
        print(len(squareCenters))
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.key == K_r:
            pygame.quit()
            sys.exit()
            main()
        pygame.event.post(event)

if __name__ == '__main__':
    main()
