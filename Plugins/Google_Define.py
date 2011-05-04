from Hook import bindFunction, requires, prefers


@requires("Google")
@prefers("Colors")
class Google_Define:
    @bindFunction(message="!gd (?P<term>\w+) ?(?P<definition>\d*)")
    def g_define(self, term, response, target, colorize, gdefine, definition):
        print(definition)
        if colorize:
            return response.msg(target, colorize(
                "<{C3}Google Define{}: %s | {LINK}%s{} [{B}%s{} of %s]>" % gdefine(term, definition)))
        else:
            return response.msg(target,
                    "<Google Define: %s | {LINK}%s{} [{B}%s{} of %s]>" % gdefine(term, definition))
