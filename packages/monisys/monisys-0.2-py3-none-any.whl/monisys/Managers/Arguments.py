import sys
class Arguments:
    def __init__(self, args=None):
        self.commands = []
        self.options = []
        self.optionValues = {}
        if args is None:
            self.original = sys.argv.copy()
        else:
            self.original = args
        
        for arg in self.original:
            if arg.startswith("-"):
                if "=" in arg:
                    pair = arg.split("=")
                    self.optionValues[pair[0]] = pair[1]
                    self.options.append(pair[0])
                else:
                    self.options.append(arg)
            else:
                self.commands.append(arg)

    def hasArgument(self, haystake, needle):
        return len(set(needle) & set(haystake)) >= 1

    def hasOptions(self, option):
        return self.hasArgument(self.options, option)

    def hasCommands(self, command):
        return self.hasArgument(self.commands, command)

    def getOptionValue(self, option, default=False):
        if option in self.optionValues:
            return self.optionValues[option]
        else:
            return default
