def on_load(self):

    @hook('NICK')
    def irc_NICK(proto, prefix, params):
        print proto
        print prefix
        print params
