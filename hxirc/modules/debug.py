def on_load():

    @hook('NICK')
    def irc_NICK(proto, prefix, params):
        print proto
        print prefix
        print params

def on_unload():
    pass
