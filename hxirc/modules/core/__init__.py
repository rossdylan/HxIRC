from model import User
from numerics import errors, numerics


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
                    '',
                    irc,
                    [])
        irc.store('nicks', nicks_dict)

    @hook('USER')
    def user_hook(irc, prefix, params):
        nicks_dict = irc.get('nicks')
        this_nick = filter(
                lambda nick: nick.connection == irc,
                nicks_dict.values())[0]
        if this_nick != []:
            if len(params) < 3:
                # Call a function to return the proper numeric error
                return
            this_nick = this_nick._replace(
                    username= params[0],
                    hostname = params[1],
                    realname = params[2])
            nicks_dict[this_nick.nick] = this_nick
        irc.store('nicks', nicks_dict)

def on_unload():
    pass
