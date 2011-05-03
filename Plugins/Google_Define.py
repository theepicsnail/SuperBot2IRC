from Hook import bindFunction, requires, prefers


@requires("Google")
@prefers("Colors")
class Google_Define:
    @bindFunction(message="!define")
    def g_define(self, response, target, colorize, gdefine):
        if colorize:
            print("<Google Define: %s | {LINK}%s{} [{B}%s{} of %s]>" % gdefine("test")) # debug
            return response.msg(target, colorize(
                "<{C3}Google Define{}: %s | {LINK}%s{} [{B}%s{} of %s]>" % gdefine("test")))
        else:
            print("<Google Define: %s | {LINK}%s{} [{B}%s{} of %s]>" % gdefine("test")) # debug
            return response.msg(target,
                    "<Google Define: %s | {LINK}%s{} [{B}%s{} of %s]>" % gdefine("test"))
