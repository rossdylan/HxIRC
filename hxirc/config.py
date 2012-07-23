from twisted.internet.endpoints import TCP4ServerEndpoint
from irc import IRCFactory


def parse_endpoints(config, reactor):
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
    return endpoints
