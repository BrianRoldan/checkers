import sys,pygame,os
from pygame.locals import * 
pygame.init()
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
tcolor= (253,77,145)
width = 400
height = 400
FPS = 30
LEFT = 1
currentTurn = None
screen = pygame.display.set_mode((width,height))
screen.set_colorkey((253,77,145))
fpsClock = pygame.time.Clock()



class gameBoard(pygame.sprite.Sprite):
        def __init__(self):
                
                pygame.sprite.Sprite.__init__(self)
                self.whiteTile = pygame.image.load("white.png")
                self.redTile = pygame.image.load("red.png")
                self.tileSize = 50
                self.boardheight = 400
                self.boardwidth = 400
                
                
                
                self.boardimage = pygame.Surface([self.boardwidth,self.boardheight])

                
                self.boardDict = {0:self.redTile,1:self.whiteTile}
                self.board =[[1,0,1,0,1,0,1,0],
                             [0,1,0,1,0,1,0,1],
                             [1,0,1,0,1,0,1,0],
                             [0,1,0,1,0,1,0,1],
                             [1,0,1,0,1,0,1,0],
                             [0,1,0,1,0,1,0,1],
                             [1,0,1,0,1,0,1,0],
                             [0,1,0,1,0,1,0,1]]
        
                self.rect = self.boardimage.get_rect()
                
                
        def drawBackground(self):
                
                for self.x in range(len(self.board)):
                        for self.y in range(len(self.board[self.x])):
                                self.tileType = self.board[self.x][self.y]
                                self.tile = self.boardDict[self.tileType]
                                screen.blit(self.tile,(self.x * self.tileSize,self.y * self.tileSize))


class checkpcs(gameBoard,pygame.sprite.Sprite):
        
        def __init__(self,player):
                pygame.sprite.Sprite.__init__(self)
                gameBoard.__init__(self)
                self.player = player
                
                self.redpieces =    [[0,'r',0,'r',0,'r',0,'r'],
                                     ['r',0,'r',0,'r',0,'r',0],
                                     [0,'r',0,'r',0,'r',0,'r'],
                                     [0, 0, 0, 0, 0, 0, 0, 0,],
                                     [0, 0, 0, 0, 0, 0, 0, 0,],
                                     [0, 0, 0, 0, 0, 0, 0, 0,],
                                     [0, 0, 0, 0, 0, 0, 0, 0,],
                                     [0, 0, 0, 0, 0, 0, 0, 0,],]
                
                self.whitepieces =  [[0, 0, 0, 0, 0, 0, 0, 0,],
                                     [0, 0, 0, 0, 0, 0, 0, 0,],
                                     [0, 0, 0, 0, 0, 0, 0, 0,],
                                     [0, 0, 0, 0, 0, 0, 0, 0,],
                                     [0, 0, 0, 0, 0, 0, 0, 0,],
                                     ['w',0,'w',0,'w',0,'w',0],
                                     [0,'w',0,'w',0,'w',0,'w'],
                                     ['w',0,'w',0,'w',0,'w',0]]
                
                
                                
        def startpos(self):
                
                
                if self.player == "red":
                        self.red = pygame.image.load('redpce.png')
                        for y in range(len(self.redpieces)):
                                for x in range(len(self.redpieces[y])):
                                        if self.redpieces[y][x] == 'r':  
                                                self.red.set_colorkey(tcolor)
                                                screen.blit(self.red,(x*self.tileSize,y*self.tileSize))
                                              
                      
                else:
                        
                        self.white = pygame.image.load('whitepce.png')
                        for y in range(len(self.whitepieces)):
                                for x in range(len(self.whitepieces[y])):
                                        if self.whitepieces[y][x] == 'w': 
                                                self.white.set_colorkey(tcolor)
                                                screen.blit(self.white,(x*self.tileSize,y*self.tileSize))
                            
        def selectPiece(self):
        #loop until player selects a piece
                
                self.tileSize = 50
                self.pos = pygame.mouse.get_pos()
                self.column = self.pos[0]//(self.tileSize)
                self.row = self.pos[1]//(self.tileSize)
                self.currentpiece = []
                self.piece = False
                if self.player == "red":
                        if self.redpieces[self.row][self.column] == 'r':
                                self.currentpiece.append((self.row,self.column))
                                return True
                        else:
                                return False
                else:
                        if self.whitepieces[self.row][self.column] == 'w':
                                self.currentpiece.append((self.row,self.column))
                                
                                return True
                        else:
                                return False
                        
                               
                        
                
        def selectSpace(self):
        #check if distance between 1st click and 2nd click is valid(x+1,y+1)or(x-1,y+1)
        #if there is an r in that position or is not a point in the grid invalid move
                
                self.tileSize = 50
                self.pos = pygame.mouse.get_pos()
                self.column = self.pos[0]//(self.tileSize)
                self.row = self.pos[1]//(self.tileSize)
                if self.player == "red":
                        if self.redpieces[self.row][self.column] == 0: 
                                self.redpieces[self.row][self.column] = 'r'
                                self.redpieces[self.currentpiece[0][0]][self.currentpiece[0][1]] = 0
                               
                else:
                        
                        if self.whitepieces[self.row][self.column] == 0: 
                                self.whitepieces[self.row][self.column] = 'w'
                                self.whitepieces[self.currentpiece[0][0]][self.currentpiece[0][1]] = 0
               

        def isCapture(self):
        #is one piece's xy equal to another, the current player captures other player piece in the same x,y
                captureDict = {}
                if self.player == "red":
                        
                        if self.redpieces[self.row][self.column] ==  self.whitepieces\
                           and self.whitepieces[self.currentpiece[0][0]][self.currentpiece[0][1]] == 'w':
                                self.whitepieces[self.row][self.column] = 0
                else:
                        if self.whitepieces[self.row][self.column] == self.redpieces[self.row][self.column]:
                                self.redpieces[self.row][self.column] = 0 
                     

        def update(self):
                if self.player == "red":
                        self.red = pygame.image.load('redpce.png')
                        for y in range(len(self.redpieces)):
                                for x in range(len(self.redpieces[y])):
                                        if self.redpieces[y][x] == 'r':  
                                                self.red.set_colorkey(tcolor)
                                                screen.blit(self.red,(x*self.tileSize,y*self.tileSize))
                else:
                        
                        self.white = pygame.image.load('whitepce.png')
                        for y in range(len(self.whitepieces)):
                                for x in range(len(self.whitepieces[y])):
                                        if self.whitepieces[y][x] == 'w':  
                                                self.white.set_colorkey(tcolor)
                                                screen.blit(self.white,(x*self.tileSize,y*self.tileSize))


player1 = checkpcs("red")
player2 = checkpcs("white")
                       
                                     
def main():
        
        currentTurn = player1
        background = gameBoard()
        background.drawBackground()
        player1.startpos()
        player2.startpos()
        
        while True:
        
                for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                            
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                currentTurn.selectPiece()
                        if event.type == pygame.MOUSEBUTTONUP:
                                currentTurn.selectSpace()
                                player1.isCapture()
                                background.drawBackground()
                                player1.update()
                                player2.update()
                                if currentTurn == player1:
                                        currentTurn = player2
                                elif currentTurn == player2:
                                        currentTurn = player1

                                                                
                pygame.display.update()
                fpsClock.tick(FPS)

        

main()
