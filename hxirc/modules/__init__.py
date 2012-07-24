import logging
import sys
from collections import namedtuple

log = logging.getLogger('HxIRCD.modules')

modules = {}
hooks = {}

HookInfo = namedtuple('HookInfo', ['mod', 'func'])

def hook(command):
    def hook_wrapper(func):
        the_hook = HookInfo(func.__module__, func)
        if command in hooks:
            hooks[command].append(the_hook)
        else:
            hooks[command] = [the_hook,]
        return func
    return hook_wrapper


def fire_hook(_hook, *args, **kwargs):
    if _hook in hooks:
        for hinfo in hooks[_hook]:
            func = hinfo.func
            log.debug('Firing "{0}" hook for {1}'.format(_hook, func))
            try:
                func(*args, **kwargs)
            except:
                log.ERROR('Hook "{0}" for {1} failed'.format(_hook, func))

def unload_module(mod_name):
    if mod_name in modules:
        fire_hook('module_preunload', mod_name, modules[mod_name])
        for h in hooks:
            to_delete = {}
            index = 0
            for hinfo in hooks[h]:
                if hinfo.mod == modules[mod_name]:
                    to_delete[hook] = index
                index += 1
            for h in to_delete:
                del hooks[h][to_delete[h]]
        modules[mod_name].on_unload()
        fire_hook('module_postunload', mod_name, modules[mod_name])
        del modules[mod_name]
    if "modules.{0}".format(mod_name) in sys.modules:
        del sys.modules['modules.{0}'.format(mod_name)]
    log.info("Unloaded {0}".format(mod_name))


def load_module(mod_name):
    if mod_name in modules:
        unload_module(mod_name)
    modules[mod_name] = __import__(mod_name, globals(), locals(), [], -1)
    inject_funcs(
            modules[mod_name],
            [('hook', hook),])

    fire_hook('module_preload', mod_name, modules[mod_name])
    modules[mod_name].on_load()
    fire_hook('module_postload', mod_name, modules[mod_name])
    log.info('Loaded {0}'.format(mod_name))

def inject_funcs(mod, funcs):
    for name, func in funcs:
        setattr(mod, name, func)
