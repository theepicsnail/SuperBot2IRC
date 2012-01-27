from Hook import *
parser = None
from Logging import LogFile
log = LogFile("Alarm")
import time
import datetime


storeFile = "AlarmStore.pkl"
parseStrings = [
"%m/%d",
"%m/%d/%y",
"%m/%d/%y %H:%M:%S",
"%m/%d/%y %h:%M:%S %p"
]
def backupParse(s):
    global parseStrings
    for fmt in parseStrings:
        try:
            return datetime.datetime.strptime(s,fmt)
        except:pass
    return None

try:
    import parsedatetime.parsedatetime as pdt
    import parsedatetime.parsedatetime_consts as pdc
    c = pdc.Constants()
    p = pdt.Calendar(c)
    parser = lambda s:datetime.datetime(*p.parse(s)[0][:6])
    log.debug("Using parsedatetime")
except:
    parser = backupParse
    log.debug("Using backup parser")

try:
    import cPickle as pickle
    log.debug("Using cPickle")
except:
    import pickle
    log.debug("Using pickle.")





@requires("IRCArgs")
class Alarm:
    alarms = []
    def __init__(self):
        try:
            self.alarms = pickle.load(file(storeFile))
            log.debug("Pickle loaded.",*self.alarms)
        except:
            log.exception("Failed to load pickle.")
            self.alarms = []
            pass

    @dedicated()
    def ded(self,response):
        time.sleep(1)
        while len(self.alarms)>0:
            now = datetime.datetime.now()
            curAlarm = self.alarms[0]
            if now > curAlarm[0]:
                log.debug("Firing alarm:",*curAlarm) 
                yield response.msg(curAlarm[1],curAlarm[2])
                self.alarms.pop(0)


    @bindFunction(message="!alarm (?P<when>.*)#(?P<what>.*)")
    def sched(self,response,target,when,what):
        log.debug("Scheduler triggered.")
        dt = parser(when)
        if not dt:
            log.warning("Invalid time.",when)
            yield response.msg(target,"Sorry, I couldn't figure out when \"%s\" is."%when)
            return
        log.debug("Scheduled alarm:",when,target,what)
        yield response.msg(target,"Sceduled for: %s"%dt)
        self.alarms.append((dt,target,what))
        self.alarms.sort()
        
        try:
            pickle.dump(self.alarms,file(storeFile,"w"))
        except:
            log.exception("Failed to store pickle.")


