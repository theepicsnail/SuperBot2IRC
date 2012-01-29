from Hook import *

HookNick = "Gitbot"
class GitHubReloader:
    @bindFunction(command="NOTICE", prefix="^"+HookNick,message="(https://github.com/.*)")
    def onPush(self,message0,pm):
        print message0
    """This push is mostly to create a better test to work with. For now..."""
