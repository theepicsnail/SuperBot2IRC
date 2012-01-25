from Hook import bindFunction,requires

#pd.EnsureDedicated(pm.GetDedicated(),self._ResponseObject,handler)

@requires("IRCArgs")
@requires("PluginManager")
class PluginManager:
    @bindFunction(command="NOTICE", message="^plugin load (.*)$")
    def load(self,response,message0,nick,pm,pd,ro,core):
        print "load",nick,message0,pm
        if pm.HasPlugin(message0):
            return response.msg(nick,"Plugin is already loaded. Use cycle to force a reload.")
        print "load2"
        plug = pm.LoadPlugin(message0)
        print "load3"
        if plug:
            print "load 4a"
            pd.EnsureDedicated(pm.getDedicated(),ro,core.handler)
            return response.msg(nick,"Plugin %s loaded."%message0)
        else:
            print "load 4b"
            return response.msg(nick,"Plugin %s failed to load."%message0)            

    @bindFunction(command="NOTICE", message="^plugin unload (.*)$")
    def unload(self,pm,response,message0,nick,pm,pd,ro,core):
        print "unload",nick,message0,pm
        if not pm.HasPlugin(message0):
            return response.msg(nick,"Plugin %s wasn't loaded"%message0)

        if pm.UnloadPlugin(message0):
            pd.EnsureDedicated(pm.getDedicated(),ro,core.handler)
            return response.msg(nick,"Plugin %s is nolonger loaded."%message0)
        else:
            return response.msg(nick,"Couldn't unload %s for some reason. Check the log!"%message0)

    @bindFunction(command="NOTICE", message="^plugin cycle$")
    @bindFunction(command="NOTICE", message="^plugin cycle (.*)$")
    def cycle(self,response,message0="ALL"):
        print "cycle",message0
