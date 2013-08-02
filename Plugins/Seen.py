from Hook import *
parser = None
from Logging import LogFile
log = LogFile("Seen")
import datetime


storeFile = "SeenStore.pkl"
try:
    import cPickle as pickle
    log.debug("Using cPickle")
except:
    import pickle
    log.debug("Using pickle.")

def now():
    return datetime.datetime.now().strftime("%H:%M:%S")

def saveState(state):
    try:
        pickle.dump(state,file(storeFile,"w"))
    except:
        log.exception("Failed to store pickle.")

def loadState():
    try:
        return pickle.load(file(storeFile))
    except:
        log.exception("Failed to load pickle")
        return None




@requires("IRCArgs")
class Seen:
    seenTable = {}#nick=>date string
    tellTable = {}#nick=>[Message list]
    def __init__(self):
        state = loadState()
        if state == None:
            state = {}
        self.seenTable = state.get("seen",{})
        self.tellTable = state.get("tell",{})

    @bindFunction(message="^!seen (?P<who>.*)")
    def seen(self,response,target,who):
        who=who.lower().strip()
        when = self.seenTable.get(who,False)
        if when:
            return response.say(target,"%s was last seen at %s"%(who,when))
        return response.say(target,"I haven't seen %s yet."%(who))


    @bindFunction(message="^!tell (?P<who>.*?)[,:]? (?P<what>.*)")
    def tell(self,nick, who, what, response):
        who=who.lower().strip()
        log.debug("Tell",who,what)

        messages = self.tellTable.get(who,[])
        
        messages.append("<%s>%s: %s"%(now(),nick,what))
        self.tellTable[who] = messages
        self.save()
        return response.say(target,"Noted.")

    def save(self):
        saveState({"seen":self.seenTable, "tell":self.tellTable})

    @bindFunction(command="JOIN|PRIVMSG")
    def event(self,response,nick,target,command):
        log.debug("Event:",nick,target,command)
        nick=nick.lower().strip()
        self.seenTable[nick] = now()
        messages = self.tellTable.get(nick,[])
        if messages == []:
            return
        

        yield response.say(target,"%s, You have %s message%s"%(
                                    nick,
                                    len(messages),
                                    "" if len(messages)==1 else "s" ))
        for idx,msg in enumerate(messages):
            yield response.say(target,"%s) %s"%(idx+1,msg))
        self.tellTable[nick]=[]
        self.save()
    
