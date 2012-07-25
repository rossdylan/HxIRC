from collections import namedtuple

User = namedtuple(
    'User',
    [
        'channels',
        'nick',
        'username',
        'hostname',
        'realname',
        'connection',
        'modes'
    ])
Channel = namedtuple('Channel', ['Users',])
