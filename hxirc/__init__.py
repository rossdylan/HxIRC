import config
import yaml
from twisted.internet import reactor
import logging


def main():
    config_dict = yaml.load(file("/etc/hxircd.conf").read())

    log_levels = dict(
            debug=logging.DEBUG,
            info=logging.INFO,
            warning=logging.WARNING,
            error=logging.ERROR,
            critical=logging.CRITICAL)

    logging.basicConfig(
            filename=config_dict['logging']['file'],
            format='%(asctime)s %(message)s',
            level=log_levels[config_dict['logging']['level']])

    endpoints = config.parse_endpoints(config_dict, reactor)
    for endpoint in endpoints:
        logging.info("Listening; {0}".format(endpoint))

    logging.info("HxIRCD Starting up")
    reactor.run()
    logging.info("HxIRCD Shutting down")
