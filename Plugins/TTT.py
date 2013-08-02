from Hook import *

def split_len(seq, length):
        return [seq[i:i+length] for i in range(0, len(seq), length)]

class TTT:

    board = "123456789"
    turn = "X"

    def changeTurn(self):
        if self.turn=="X":
            self.turn = "O"
        else:
            self.turn = "X"
    
       getWinner(self):
        wins = [
            [0,1,2],[3,4,5],[6,7,8],[0,3,6],
            [1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for (a,b,c) in wins:
            if self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]    
    def printBoard(self,response,target):
        for i in split_len(self.board,3):
            yield response.msg(target,i)
    
    @bindFunction(message="!ttt")
    def startGame(self,response,target):
        self.board="123456789"
        self.turn = "X"

        for i in self.printBoard(response,target):
            yield i

    @bindFunction(message="go ([1-9])")
    def go(self,response,target, message0):
        i = int(message0)-1
        yield response.msg(target,"%i %s"%(i,self.board))
        if self.board[i] in "XO":
            yield response.msg(target,"That spaces is already taken!")
            return
        self.board = self.board.replace(self.board[i],self.turn)
        for i in self.printBoard(response,target):
            yield i
        self.changeTurn()
        win = self.getWinner()
        if win==None:
            return
        if win=="":
            yield response.msg(target,"Tie!")
        else:
            yield response.msg(target,"Winner: %s"%win)
    
    @bindFunction(message="!ttt -h")
    def manOne(self,response,target):
        return response.say("Tic tac toe. !ttt to start game. A board consisting of numbers will appear\ntype: 'go <i>' to place your piece on the corresponding board number")

    @bindFunction(message="!ttt --help")
    def manTwo(self,response,target):
        return response.say("Tic tac toe. !ttt to start game. A board consisting of numbers will appear\ntype: 'go <i>' to place your piece on the corresponding board number")

