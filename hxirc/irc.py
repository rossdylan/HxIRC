from twisted.internet.protocol import Factory
from twisted.protocols import basic
import logging
import modules
import config


class IRCLineReceiver(basic.LineReceiver):

    def sendLine(self, line):
        return basic.LineReciever.sendLine(self,"{0}\r".format(line))

    def dataReceived(self, data):
        return basic.LineReceiver.dataReceived(self, data.replace('\r', ''))

class IRC(IRCLineReceiver):
    def connectionMade(self):
        # Send our connectionresponse and stuff
        logging.info("New Connection from {0}".format(self.transport.getPeer()))

    def lineReceived(self, line):
        prefix = ""
        if line.startswith(":"):
            line = line[1:]
            line_split = line.split(" ")
            prefix = line_split[0]
            line_split = line_split[1:]

        command = line_split[0]
        params = line_split[1:]
        parsed_params = []
        index= 0
        for param in params:
            if param.startswith(':'):
                param = param[1:]
                params[index] = param
                parsed_params.append(' '.join(params[index:]))
                break
            else:
                parsed_params.append(param)
            index += 1

            logging.debug("Recieved command {0}".format(command))
            modules.fire_hook(command, prefix, parsed_params)

class IRCFactory(Factory):
    protocol = IRC

    def __init__(self, config_dict):
        self.config_dict = config_dict

    def startFactory(self):
        for mod in config.parse_modules(self.config_dict):
            modules.load_module(mod)

    def stopFactory(self):
        for mod in config.parse_modules(self.config_dict):
            modules.unload_module(mod)

