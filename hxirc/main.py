import config
import yaml
from twisted.internet import reactor


def main(self):
    config_dict = yaml.load(file("/etc/hxircd.conf").read())
    endpoints = config.parse_endpoints(config_dict, reactor)
