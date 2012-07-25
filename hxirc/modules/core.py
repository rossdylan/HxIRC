from ..model import User
import itertools

numerics = {}
errors = {
        'err_nosuchnick': 401,
        'err_nosuchserver': 402,
        'err_nosuchchannel': 403,
        'err_cannotsendtochan': 404,
        'err_toomanychannels': 405,
        'err_wasnosuchnick': 406,
        'err_toomanytargets': 407,
        'err_noorigin': 409,
        'err_norecipient': 411,
        'err_notexttosend': 412,
        'err_notoplevel': 413,
        'err_wildtoplevel': 414,
        'err_unknowncommand': 421,
        'err_nomotd': 422,
        'err_fileerror': 424,
        'err_nonicknamegiven': 431,
        'err_erroneusnickname': 432,
        'err_nicknameinuse': 433,
        'err_nickcollision': 436,
        'err_usernotinchannel': 441,
        'err_notonchannel': 442,
        'err_useronchannel': 443,
        'err_nologin': 444,
        'err_summondisabled': 445,
        'err_usersdisabled': 446,
        'err_notregistered': 451,
        'err_needmoreparams': 461,
        'err_alreadyregistred': 462,
        'err_nopermforhost': 463,
        'err_passwdmismatch': 464,
        'err_yourebannedcreep': 465,
        'err_keyset': 467,
        'err_channelisfull': 471,
        'err_unknownmode': 472,
        'err_inviteonlychan': 473,
        'err_bannedfromchan': 474,
        'err_badchannelkey': 475,
        'err_noprivileges': 481,
        'err_chanoprivsneeded': 482,
        'err_cantkillserver': 483,
        'err_nooperhost': 491,
        'err_umodeunknownflag': 501,
        'err_usersdontmatch': 502}
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
