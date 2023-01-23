''' Sorry no comments :).

Usage:
python3 nameGame.py myPlayer1.py myPlayer2.py
'''

import Goban 
import importlib
#import time
from io import StringIO
import sys

class GameAbstract:
    
    def __init__(self, board, player1Name = 'randomPlayer', player2Name = 'randomPlayer', nextplayer = 0, nextplayercolor = Goban.Board._BLACK):
        self.player1Name = player1Name
        self.player2Name = player2Name
        self.b = board
        self.players = []
        player1class = importlib.import_module(player1Name)
        player1 = player1class.myPlayer()
        player1.newGame(Goban.Board._BLACK)
        self.players.append(player1)

        player2class = importlib.import_module(player2Name)
        player2 = player2class.myPlayer()
        player2.newGame(Goban.Board._WHITE)
        self.players.append(player2)

        #self.totalTime = [0,0] # total real time for each player
        self.nextplayer = nextplayer
        self.nextplayercolor = nextplayercolor
        self.nbmoves = 1

        self.outputs = ["",""]
        self.sysstdout= sys.stdout
        self.stringio = StringIO()
        self.wrongmovefrom = 0

    def _move(self):
        
         

        nextplayer = self.nextplayer
        nextplayercolor = self.nextplayercolor

        #print("Referee Board:")
        #self.b.prettyPrint() 
        #print("Before move", self.nbmoves)
        legals = self.b.legal_moves() # legal moves are given as internal (flat) coordinates, not A1, A2, ...
        #print("Legal Moves: ", [self.b.move_to_str(m) for m in legals]) # I have to use this wrapper if I want to print them
        self.nbmoves += 1

        otherplayer = (nextplayer + 1) % 2
        othercolor = Goban.Board.flip(nextplayercolor)
  
        #currentTime = time.time()
        sys.stdout = self.stringio

        move = self.players[nextplayer].getPlayerMove() # The move must be given by "A1", ... "J8" string coordinates (not as an internal move)

        sys.stdout = self.sysstdout

        playeroutput = self.stringio.getvalue()
        self.stringio.truncate(0)
        self.stringio.seek(0)
        #print(("[Player "+str(nextplayer) + "] ").join(playeroutput.splitlines(True)))
        self.outputs[nextplayer] += playeroutput
        #self.totalTime[nextplayer] += time.time() - currentTime
        #print("Player", nextplayercolor, self.players[nextplayer].getPlayerName(), "plays: " + move) #changed 

        if not Goban.Board.name_to_flat(move) in legals:
            print(otherplayer, nextplayer, nextplayercolor)
            print("Problem: illegal move")
            self.wrongmovefrom = nextplayercolor
            
        self.b.push(Goban.Board.name_to_flat(move)) # Here I have to internally flatten the move to be able to check it.
        self.players[otherplayer].playOpponentMove(move)
    
        self.nextplayer = otherplayer
        self.nextplayercolor = othercolor

        if self.b.is_game_over():
            print("The game is over")
           
            self.b.prettyPrint()
            result = self.b.result()
            #print("Time:", self.totalTime)
            print("GO Score:", self.b.final_go_score())
            print("Winner: ", end="")
            w = -1
            if self.wrongmovefrom > 0:
                if self.wrongmovefrom == self.b._WHITE:
                    print("BLACK")
                    w=1
                elif self.wrongmovefrom == self.b._BLACK:
                    print("WHITE")
                    w=0
                else:
                    print("ERROR")
            elif result == "1-0":
                w = 0
                print("WHITE")
            elif result == "0-1":
                print("BLACK")
                w=1
            else:
                print("DEUCE")
            return w
        
        return move
        
        



