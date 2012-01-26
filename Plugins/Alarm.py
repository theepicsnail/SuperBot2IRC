from Hook import *
parser = None
from Logging import LogFile
log = LogFile("Alarm")
import time
import datetime
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

@requires("IRCArgs")
class Alarm:
    alarms = []
    @dedicated()
    def ded(self,response):
        time.sleep(1)
        if len(self.alarms)==0:
            return
        log.debug("Alarms exist. Checking time.")
        now = datetime.datetime.now()
        curAlarm = self.alarms[0]
        log.debug("Next alarm:",curAlarm)
        log.debug(curAlarm[0] > now)
        while curAlarm[0] < now:
            yield response.msg(curAlarm[1],curAlarm[2])
            self.alarms.pop(0)
            curAlarm = self.alarms[0]


    @bindFunction(message="!alarm (?P<when>.*):(?P<what>.*)")
    def sched(self,response,target,when,what):
        log.debug("Scheduler triggered.")
        dt = parser(when)
        if not dt:
            log.warning("Invalid time.",when)
            return response.msg(target,"Sorry, I couldn't figure out when \"%s\" is."%when)
        log.debug("Scheduled alarm:",when,target,what)
        self.alarms.append((dt,target,what))
        self.alarms.sort()




