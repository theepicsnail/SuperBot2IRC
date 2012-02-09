import time
import random
import re
import urllib
from Hook import *
from Logging import LogFile
log = LogFile("Numbers")

def solve(game):
    url = "http://djce.org.uk/countdown?n="+"&n=".join(map(str,game[0]))+"&t="+str(game[1])
    return urllib.urlopen(url).read().split("\n</pre>")[0].split("\n")[-1]


def chooseNumbers(numLarge):
    log.debug("Choose numbers called, {}".format(numLarge))
    if 0 > numLarge or numLarge > 4:
        return None
    large = [25,50,75,100]
    small = [1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10]
    random.shuffle(large)
    random.shuffle(small)
    numbers = large[:numLarge]+small[:6-numLarge]
    return numbers,random.randint(100,900)


def factor(n):
    if n == 1: return [1]
    i = 2
    limit = n**0.5
    while i <= limit:
        if n % i == 0:
            ret = factor(n/i)
            ret.append(i)
            return ret
        i += 1
    return [n]
@requires("IRCArgs")
class Numbers:
    numbers = None#([],0)Current numbers and goal
    equations = {} #nick->last equation
    currentWinner = (None,0)#(nick, distance from target)
    startTime = 0

    def validEquation(self,player):
        log.debug("Valid equation",player)
        equ = self.equations[player]
        log.debug("Equation:",equ)
        nums = re.findall("[0-9]+",equ)
        try:
            map(list(self.numbers[0]).remove,map(int,nums))
            log.debug("valid.")
            return True
        except:
            log.debug("inalid.")
            return False
    @bindFunction(message="!solve")
    def Solve(self,target,response):
        if not self.numbers:
            yield response.msg(target,"No active game.")
            return
        ans = solve(self.numbers)
        yield response.msg(target,ans)
        for i in self.EndGame(target,response):
            yield i

    @bindFunction(message="%.*")
    def OnEquation(self,nick,message):
        log.debug("OnEquation",nick,message)
        self.equations[nick]=message

    @bindFunction(message="(?P<player>.*): (?P<score>.*)")
    def OnResult(self,nick,message,player,score, response,target):
        log.debug("OnResult",nick,message,player,score, response,target)
        if nick!="Superbot":
            return
        if not self.numbers:
            return
        try:
            score = abs(self.numbers[1]-int(float(score))) #score = how far the answer is from the goal
            log.debug("Score:",player,score)
            if not self.validEquation(player): return

            if self.currentWinner[0]==None:
                self.currentWinner = (player,score)
            elif score < self.currentWinner[1]:
                self.currentWinner = (player,score)
            log.debug("Current winner:",*self.currentWinner)
            if score==0:
                for i in self.EndGame(target,response):
                    yield i

        except:
            log.exception("Parsing number exception.")
            yield response.msg(target,"Couldn't parse Score.")

    @bindFunction(message="^!numbers( end)?$")
    def EndGame(self,target,response):
        log.debug("Ending game.",self.currentWinner,self.numbers)
        yield response.msg(target,"Numbers game ended.")
        if self.currentWinner[0]!=None:
            yield response.msg(target,"Winner: {} with a score of {}".format(*self.currentWinner))
        self.numbers = None
        self.currentWinner = (None,0)

    @bindFunction(message="!numbers (?P<big>[01234])")
    def StartGame(self,response,target,big):
        newNums = chooseNumbers(int(big))

        if self.numbers:
            for i in self.EndGame(target,response):
                yield i


        self.numbers = newNums
        self.currentWinner = (None,0)
        startTime = time.time()
        yield response.msg(target,"{}".format(self.numbers))

    @bindFunction(message="!factor (?P<num>[0-9]+)")
    def Factor(self,response,target,num):
        return response.msg(target,str(factor(int(num))))
