import os
from Hook import *
from Logging import LogFile

try: import cPickle as pickle
except ImportError: import pickle

def save(obj, filename):
    pickle.dump(obj, open(filename, "w"))
    return obj

def load(filename):
    if not os.path.exists(filename):
        save(dict(), filename)
    return pickle.load(open(filename, "r"))

log = LogFile("Gifts")

gifts_file = "GiftsStore.pkl"
gifts = load(gifts_file)

pluralized_file = "PluralizedStore.pkl"
pluralized = load(pluralized_file)

def map_plural(singular, plural):
    global pluralized
    global gifts

    if plural in pluralized.keys():
        if plural in pluralized.values():
            if singular != plural:
                pluralized[singular] = plural
                del pluralized[plural]

    pluralized[singular] = plural
    save(pluralized, pluralized_file)

    # retroactively pluralize each owner's item dict
    for owner in gifts:
        if plural in gifts[owner]:
            if singular in gifts[owner]:
                gifts[owner][singular] += gifts[owner][plural]
            else:
                gifts[owner][singular] = gifts[owner][plural]
            del gifts[owner][plural]
    save(gifts, gifts_file)

def pluralize(string, n=0):
    n = int(n)

    if n == 1:
        return string

    if string in pluralized:
        return pluralized[string]

    if string.endswith("s"):
        if not string.endswith("es"):
            return string+"es"

    if string.endswith("y"):
        return string[:-1]+"ies"

    return string+"s"

def singularize(string):
    for singular, plural in pluralized.iteritems():
        if string == plural:
            string = singular
    return string

def give(recipient, amount, item):
    global gifts
    amount = int(amount)
    item = item.strip().lower()

    if item not in pluralized.keys() and item not in pluralized.values():
        if amount == 1: # guess the plural (may be explicitly remapped later)
            map_plural(item, pluralize(item))
        else: # store plural, plural (may be explicitly remapped later)
            map_plural(item, item)

    item = singularize(item)

    if recipient not in gifts:
        gifts[recipient] = {}

    if item not in gifts[recipient]:
        gifts[recipient][item] = amount

    elif amount >= 1:
        gifts[recipient][item] += amount

    save(gifts, gifts_file)
    return amount

def take(owner, amount, item):
    global gifts
    amount = int(amount)
    item = singularize(item.strip().lower())
    if owner in gifts:
        if item in gifts[owner]:
            amount = min(gifts[owner][item], amount)
            gifts[owner][item] -= amount
            if gifts[owner][item] <= 0:
                del gifts[owner][item]
        else:
            return 0
        if len(gifts[owner]) == 0:
            del gifts[owner]
        save(gifts, gifts_file)
        return amount
    return 0

def owner_items(owner):
    if owner in gifts:
        for item in gifts[owner]:
            yield pluralize(item, gifts[owner][item]), gifts[owner][item]

log.dict(gifts,"Loaded Gifts")

@requires("IRCArgs")
class Gifts:
    @bindFunction(message=r"^!items? give (?P<to>[^ ]*) (?P<amount>\d+) (?P<item>.*)")
    def giveGift(self, nick, response, target, to, amount, item):
        log.debug("Giving", to, amount, item)
        if give(to, amount, item):
            return response.say(target, "giving %s %s %s" % (to, amount, item))
        return response.say(target, "error giving %s %s to %s" % (amount, item, to))

    @bindFunction(message=r"^!items? list (?P<owner>[^ ]*)")
    def showGifts(self, nick, response, target, owner):
        log.debug("Showing items belonging to", owner)
        items = ", ".join("%s %s" % (n, g) for g, n in owner_items(owner))
        if items:
            return response.say(target, items)
        return response.say(target, "%s has no items :(" % owner)

    @bindFunction(message=r"^!items? discard (?P<amount>\d+) (?P<item>.*)")
    def discardGift(self, nick, response, target, amount, item):
        log.debug("Discarding", item, "belonging to", nick)
        amount_discarded = take(nick, amount, item)
        if amount_discarded > 0:
            return response.say(target, "discarded %s of %s's %s" % (amount_discarded, nick, item))
        return response.say(target, "%s doesn't have any %s" % (nick, item))

    @bindFunction(message=r"^!items? steal (?P<owner>[^ ]*) (?P<amount>\d+) (?P<item>.*)$")
    def stealGift(self, nick, response, target, owner, amount, item):
        log.debug("%s stole %s from %s" % (nick, item, owner))
        amount_stolen = take(owner, amount, item)
        if amount_stolen > 0:
            give(nick, amount_stolen, item)
            return response.say(target, "%s stole %s %s from %s" % (nick, amount_stolen, item, owner))
        return response.say(target, "%s didn't have any %s to steal. :(" % (owner, item))

    @bindFunction(message=r"^!items? define (?P<singular>.*):\s*(?P<plural>.*)")
    def definePlural(self, nick, response, target, singular, plural):
        log.debug("Mapping plural of %s to %s" % (singular, plural))
        map_plural(singular, plural)
        return response.say(target, "the plural of %s is now set to %s" % (singular, plural))

    @bindFunction(message=r"^!items? merge (?P<item1>.*)\s*,\s*(?P<item2>.*)")
    def mergeGifts(self, nick, response, target, item1, item2):
        if item2 in gifts[nick]:
            gifts[nick][item2] += gifts[nick][item1]
        else:
            gifts[nick][item2] = gifts[nick][item1]
        del gifts[nick][item1]
        return response.say(target, "merged %s with %s" % (item1, item2))

    @bindFunction(message=r"^!items? -h")
    def manOne(self,nick,response,target):
        return response.msg(target, "!item give <i> <item> <nick> to give i item(s)\n!item steal <nick> <i> <item>\n!item define <item>:<items> to define plural of item\n!item merge <item1> <item2>\n!item discard <i> <item>")

    @bindFunction(message=r"^!items? --help")
    def manTwo(self,nick,response,target):
        return response.msg(target, "!item give <i> <item> <nick> to give i item(s)\n!item steal <nick> <i> <item>\n!item define <item>:<items> to define plural of item\n!item merge <item1> <item2>\n!item discard <i> <item>")

