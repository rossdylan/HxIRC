def on_load():

    @hook('NICK')
    def irc_NICK(proto, prefix, params):
        print proto
        print prefix
        print params
