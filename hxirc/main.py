from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.protocols import basic

import yaml


class IRCLineReceiver(basic.LineReceiver):

    def sendLine(self, line):
        return basic.LineReciever.sendLine(self,"{0}\r".format(line))

    def dataReceived(self, data):
        return basic.LineReceiver.dataReceived(self, data.replace('\r', ''))

class IRC(IRCLineReceiver):
    def connectionMade(self):
        # Send our connectionresponse and stuff
        pass

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

            handler_func = getattr(self, "irc_{0}".format(command))
            handler_func(prefix, *params)

class IRCFactory(Factory):
    protocol = IRC

    def __init__(self, config_file):
        self.config_file = config_file

def main(self):
    config = yaml.load(file("/etc/hxircd.conf").read())
    endpoints = []
    listeners = config['listen']
    if 'ssl' in listeners:
        from twisted.internet.endpoints import SSL4ServerEndpoint
        from twisted.internet import ssl
        ssl_endpoint = SSL4ServerEndpoint(
                reactor,
                listeners['ssl']['port'],
                ssl.DefaultOpenSSLContextFactory(
                    listeners['ssl']['key'],
                    listeners['ssl']['cert']),
                interface=config['ssl']['addr']
                )
        ssl_endpoint.listen(IRCFactory(config))
        endpoints.append(ssl_endpoint)

    if 'addr' in listeners and 'port' in listeners:
        tcp_endpoint = TCP4ServerEndpoint(
                reactor,
                listeners['port'],
                interface=listeners['addr'])
        tcp_endpoint.listen(IRCFactory(config))
        endpoints.append(tcp_endpoint)
