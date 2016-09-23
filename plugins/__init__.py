from importlib import import_module

class Plugin(object):

    name = 'Generic Plugin'
    version = '0.0.0'

    def __init__(self, bot):
        self.commands = []
        self.bot = bot

    def add_command(self, command):
        if isinstance(command, Command):
            self.commands.append(command)

    def get_command(self, command):
        for cmd in self.commands:
            if cmd.name == command:
                return cmd


    def get_usage(self, command):
        return self.get_command(command).usage


    def get_description(self, command):
        return self.get_command(command).description

    def setup(self):
        pass

    def run(self):
        raise NotImplemented



class Command(object):

    def __init__(self, name, description='', usage=''):
        self.name = name
        self.description = description
        self.usage = usage

    def description(self, msg=None):
        if not msg:
            return self.description
        else:
            self.description = msg


    def usage(self, msg=None):
        if not msg:
            return self.usage
        else:
            self.usage = msg



def load_plugin(bot, plugin):
    m = import_module('plugins.{}'.format(plugin))
    c = getattr(m, 'Main')(bot)

    return c

