from Hook import bindFunction,requires
from Logging import LogFile
log = LogFile("PluginManager2")

@requires("IRCArgs")
@requires("PluginManager")
class PluginManager:
    @bindFunction(command="NOTICE", message="^plugin load (.*)$")
    def load(self,response,message0,nick,pm,pd,ro,core):
        log.debug("Loading plugin",message0)
        if pm.HasPlugin(message0):
            log.warning("Plugin already loaded.")
            return response.msg(nick,"Plugin is already loaded. Use cycle to force a reload.")

        plug = pm.LoadPlugin(message0)
        if plug:
            log.debug("Plugin loaded. Updating dedicated threads.")
            pd.EnsureDedicated(pm.GetDedicated(),ro,pd.GetResponseHandler())
            log.debug("Finished loading plugin.")
            return response.msg(nick,"Plugin %s loaded."%message0)
        else:
            log.warning("Plugin failed to load. Check PluginManager's logs.")
            return response.msg(nick,"Plugin %s failed to load."%message0)            

    @bindFunction(command="NOTICE", message="^plugin unload (.*)$")
    def unload(self,pm,response,message0,nick,pd,ro,core):
        log.debug("Unloading plugin",message0)
        if not pm.HasPlugin(message0):
            log.warning("Plugin was not loaded.")
            return response.msg(nick,"Plugin %s wasn't loaded"%message0)

        if pm.UnloadPlugin(message0):
            log.debug("Unloaded plugin. Updating dedicated threads.")
            pd.EnsureDedicated(pm.GetDedicated(),ro,pd.GetResponseHandler())
            log.debug("Finished unloading plugin.")
            return response.msg(nick,"Plugin %s is nolonger loaded."%message0)
        else:
            log.warning("Unload failed. Check PluginManager's logs.")
            return response.msg(nick,"Couldn't unload %s for some reason. Check the log!"%message0)

    @bindFunction(command="NOTICE", message="^plugin cycle$")
    @bindFunction(command="NOTICE", message="^plugin cycle (.*)$")
    def cycle(self,pm,response,nick,pd,ro,core,message0="ALL"):
        log.debug("Starting cycle of plugin",message0)
        self.unload(pm,response,message0,nick,pd,ro,core)
        self.load(response,message0,nick,pm,pd,ro,core)
        log.debug("Cycle finished.")

    @bindFunction(command="NOTICE", message="^plugin list$")
    def List(self,pm,response,nick):
        log.debug("List plugins")
        yield response.msg(nick,"Plugins")
        yield response.msg(nick,", ".join(pm.__plugins__.keys()))
        yield response.msg(nick,"Services")
        yield response.msg(nick,", ".join(pm.__services__.keys()))
