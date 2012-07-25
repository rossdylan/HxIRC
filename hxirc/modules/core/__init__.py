from model import User
from numerics import errors, numerics
import itertools


def on_load():

    @hook('NICK')
    def nick_hook(irc, prefix, params):
        nicks_dict = irc.get('nicks')
        if nicks_dict == None:
            irc.store('nicks', {})
            nicks_dict = irc.get('nicks')
        if prefix != '':
            user = nicks_dict[prefix]
            user.nick = params[0]
            nicks_dict[params[0]] = user
        else:
            nicks_dict[params[0]] = User(
                    [],
                    params[0],
                    '',
                    '',
                    irc)

    @hook('USER')
    def user_hook(irc, prefix, params):
        nicks_dict = irc.get('nicks')
        this_nick = itertools.filter(lambda nick: nick.connection == irc,
                nicks_dict.itervalues())
        if this_nick != []:
            this_nick.username = params[0]
            this_nick.hostname = params[1]
            this_nick.realname = params[2]
            

def on_unload():
    pass
