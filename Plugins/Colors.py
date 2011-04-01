from Hooks import *

@requires("Colors")


class Colors:
    @bindFunction(message="!colors")
    def showColors(self, response, target):
        return response.msg(target, colorize("{C0}0 {C1}1 {C2}2 {C3}3 {C4}4 {C5}5 {C6}6 {C7}7 {C8}8 {C9}9 {C10}10 {C11}11 {C12}12 {C13}13 {C14}14 {C15}15 {B}B{} {U}U{} {LINK}LINK{}"))
