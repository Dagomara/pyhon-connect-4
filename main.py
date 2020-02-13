import time
def makeBoard(y,x):
  board = []
  for i in range(x):
    board.append([])
  for row in board:
    for i in range(y):
      row.append(0)
  return board #makes a board y columns high, x rows long
def showBoardNums(boardInQuestion): #prints out the board numerical values
  for row in boardInQuestion:
    print("row",end="")
    for column in row:
      print ("c" + str(column) + "  ",end="")
    print()
def showBoardAscii(boardInQuestion,oneChar,twoChar):
  brick = "| |"
  #print(" _                     _\n/ |___________________| \\")
  #print out top post
  print(" _ ",end="")
  for i in range(len(boardInQuestion[0])+1):
      print("   ",end="")
  print(" _ ")
  print("/ |",end="")
  for i in range(len(boardInQuestion[0])):
    if(i==len(boardInQuestion[0])-1):
      print("___",end="")
    else:
      print("____",end="")
  print("| \\")
  #print out middle section
  i=-1
  for column in boardInQuestion:
    i+=1
    print(brick,end="")
    if(i!=len(boardInQuestion)-1): #manages middle row only, not last board
      for item in column:
        if(item==1):
          print(" "+oneChar+" |",end="")
        elif(item==2):
          print(" "+twoChar+" |",end="")
        else:
          print("   |",end="")
    else: #for the last row
      for item in column:
        if(item==1):
          print("_"+oneChar+"_|",end="")
        elif(item==2):
          print("_"+twoChar+"_|",end="")
        else:
          print("___|",end="")
    print(" |")
  #print the bottom bar
  print("|_|",end="")
  for i in range(len(boardInQuestion[0])):
    if(i==len(boardInQuestion[0])-1):
      print("___",end="")
    else:
      print("____",end="")
  print("|_|")
"""
players have a number value for putting into the board array,
have a symbol of choice to be put into the ascii array,
have a score counter for amount of won games,
and can see final board layouts of both won and lost games.

That's because the game object has a board and takes player objects as input,
runs a game inside of it, and finally returns a copy of the board
to the players involved in that game.
But for now, I'm just gonna make the basic gravity function and
placing a block into a column.
"""
def placeInto(boardInQuestion,column,value): #value is the number value, will later just be the player object and inside the function will grab the number value
 try:
  for i in range(len(boardInQuestion)):
    if ((i == (len(boardInQuestion)-1)) and (boardInQuestion[i][column-1]==0)):
        boardInQuestion[i][column-1]=value
        break
    elif (boardInQuestion[i+1][column-1]!=0 and boardInQuestion[i][column-1]==0):
        boardInQuestion[i][column-1]=value
        break
 except:

     print("\n\nThis column is full! or unavailable!")
     time.sleep(1)
def digitToWord(digit):
    words = ["ZERO","ONE","TWO","THREE","FOUR","FIVE","SIX","SEVEN","EIGHT","NINE","TEN"]
    return words[digit]
def checkForWinner(boardInQuestion):

    winner = 0
    #try:
        #check each row linearly

    for row in range(len(boardInQuestion)):
        #print(row)
        for cell in range(len(boardInQuestion[row])-3):
            #print("THING: " + str(cell) + " |inside of " + str(row))
            if ((boardInQuestion[row][cell]==boardInQuestion[row][cell+1]) and (boardInQuestion[row][cell]==boardInQuestion[row][cell+2]) and (boardInQuestion[row][cell]==boardInQuestion[row][cell+3]) and (boardInQuestion[row][cell]!=0)):
                print("HORIZONTAL MATCH ON ROW=" + str(row) + " CELL=" + str(cell))
                winner = boardInQuestion[row][cell]
                break
        #check each column vertically
    for i in range(len(boardInQuestion[0])-1):
        for row in range(len(boardInQuestion)-3):
            if( (boardInQuestion[row][i]!=0)and(boardInQuestion[row][i]==boardInQuestion[row+1][i])and(boardInQuestion[row][i]==boardInQuestion[row+2][i])and(boardInQuestion[row][i]==boardInQuestion[row+3][i]) ):
                print("VERTICAL MATCH ON ROW=" + str(row) + " CELL=" + str(cell))
                winner = boardInQuestion[row][i]
                break
        #check every possible southeast diagnal, top-down left to right
        #check every possible northeast diagonal, bottom-up left to right
    #except Exception:
        #print(Exception)
    #finally:
    return winner
def SOThing(s):
    nchars = len(s)
    # string to int or long. Type depends on nchars
    x = sum(ord(s[byte])<<8*(nchars-byte-1) for byte in range(nchars))
    # int or long to string
    #''.join(chr((x>>8*(nchars-byte-1))&0xFF) for byte in range(nchars))
    return x
class Player:
    def __init__(self,name,character):
        self.id = SOThing(name) #I will need an actual ID system later lmfao
        print(name,"id= "+ str(self.id))
        self.name = name
        #PRECONDITION: character can only be a char on length 1
        self.preferredCharacter = character #if two players have the same then it goes to the default Red and Yellow aka R & Y characters
        self.wins = 0
        self.playedGames = []
    def printPlayedGames(self):
        for game,winner in self.playedGames:
            showBoardAscii(game,"R","Y")
            print(winner)
    def printStats(self): #wins, preferred character, name
        print(self.name,"\nPREFERRED CHARACTER: "+self.preferredCharacter+"\nWINS: "+str(self.wins))
    def fullTest(self):
        self.printStats()
        self.printPlayedGames()
class Game:
    def __init__(self, player1,player2,dims):
        self.boardHeight = dims[1]
        self.boardLength = dims[0]
        self.board = makeBoard(self.boardHeight,self.boardLength) # later on there should just be a board class whose constructor uses dims directly and just makes those values into Game.board.height, Game.board.length, and Game.board.space.
        self.turn = 0 #total number of turns, aka current turn number
        self.cPlayer = 1 #alternates betwixt 1 and 2.
            #if cPlayer==1: cPlayer+=1 else cPlayer-=1
        self.playerSpace = ["null",player1,player2] #you can just call whatever player number is up next when giving winner.wins and Game.board array copy.
        self.tempWinner = "none"#temporary winners slot
    def bugfix(self): #shows bugfixing information such as numerical board.
        showBoardNums(self.board)
    def playerMakesMove(self):#The player makes a selection and that selection is dropped onto board. Then, the winner's number is returned if someone won.
        winner = "none"
        placeInto(self.board,int(input("PLAYER " + digitToWord(self.cPlayer) + ": Which column? ")),self.cPlayer)
        showBoardAscii(self.board,self.playerSpace[1].preferredCharacter,self.playerSpace[2].preferredCharacter)
        if (checkForWinner(self.board)!=0):
            winner = checkForWinner(self.board)
        return winner
    def play(self):

        #do the while loop where playerMakesMove(cPlayer).
        showBoardAscii(self.board,self.playerSpace[1].preferredCharacter,self.playerSpace[2].preferredCharacter)
        while (self.tempWinner=="none"):
            self.tempWinner = self.playerMakesMove()
            #print("PLAYER " + digitToWord(self.cPlayer) + " MAKING DECISION")
            #then update cPlayer to alternate between players.
            if(self.tempWinner!="none"):
                break
            elif (self.cPlayer==1):
                self.cPlayer +=1
            else:
                self.cPlayer-=1
            #and incrememnt turns.
            self.turn+=1
        #someone won, so give them their win counter update and print out results
        self.playerSpace[self.tempWinner].wins+=1
        print("Congratulations player " + digitToWord(self.cPlayer) + ", you WIN!! ")
        #give both players a copy of the game
        self.playerSpace[1].playedGames.append(tuple((self.board,self.playerSpace[self.tempWinner].name)))
        self.playerSpace[2].playedGames.append(tuple((self.board,self.playerSpace[self.tempWinner].name)))
        #will add one to winner.wins as well as return board copy array to both players' histories.


#testing making players
#players will be a dictionary with id being the key.
p1 = Player("mike","P")
p2 = Player("greg","Q")
#p1.fullTest()
#input()
#p2.fullTest()
#input()

#def load
#f = open(input("File path? Please note that you only have one chance to type\nthis properly. Otherwise, you will have to restart.\n>>> "), "r")
"""
$PLAYER_ID
@PLAYER_NAME
@PLAYER_PREFERREDCHARACTER
@PLAYER_WINS
@PLAYER_PLAYEDGAMES
$PLAYER_ID...
"""
#f.close()




#test game goings on
game1 = Game(p1,p2,[6,7])
#game1.bugfix()
#print(game1.playerSpace)
game1.play()
game2 = Game(p1,p2,[6,7])
game2.play()
p1.fullTest()
p2.fullTest()

#old setups
#square = makeBoard(4,5)
#square[0][1]=2
#square[1][3]=1
#placeInto(square,1,2)
#showBoardNums(square)
#print("\n")
#showBoardAscii(square)
input("enter to continue")

#winner="none"
"""
while(winner=="none"):
    placeInto(square,int(input("PLAYER ONE: Which column? ")),1) #gotta fix invalid inputs later
    showBoardAscii(square)
    if (checkForWinner(square)!=0):
        winner = checkForWinner(square)
        break
    #these preceeding 3 lines would be one Game.round() and would just be used like Game.round(cPlayer) and then would update cPlayer at the end and update Game.turn.
    placeInto(square,int(input("PLAYER TWO: Which column? ")),2)
    showBoardAscii(square)
    if (checkForWinner(square)!=0):
        winner = checkForWinner(square)
        break

print("Congratulations player " + str(winner) + ", you WIN!! ")
"""

"""
 _                     _
/ |___________________| \
| |   |   |   |   |   | |
| |   |   |   |   |   | |
| |   |   |   |   |   | |
| |   |   |   |   |   | |
| |   |   | Y |   |   | |
| |___|_Y_|_R_|_Y_|___| |
|_|___________________|_|
"""


input("END OF PROGRAM")

"""
def initconsole:
    OPTIONS:
        load
        save
        devconsole
        addnewplayer
        playcustomgame(p1,p2,dims)
        play(p1,p2) #initializes a normal-sized connect 4 board
        findPlayer(name) #searches for player ids with that name
TO-DO:
    store players in a dictionary
    make basic initconsole with:
        save
        load
        play(p1id,p2id)
    finish four-in-a-row detection aka diagonals
    add more initconsole features:
        playcustomgame
        addnewplayer
        findPlayer
        devconsole?!
BACKBURNER:
    tkinter ;;;)))


"""
