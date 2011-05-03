class PluginManager:
    def onEvent(self,pm,event):
        event["pm"] = pm

