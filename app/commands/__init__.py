from abc import ABC, abstractmethod
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {} #empty dictionary for commands to be stored

    def register_command(self, command_name:str, command:Command):
        self.commands[command_name] = command

    """def execute_command(self, command_name:str):
         Look Before you Leap (LBYL) use when you expect the key to be missing
        if command_name in self.commands:
            self.commands[command_name].execute()
        else:
            print(f"Command '{command_name}' not found") """

    """ Easier to ask for forgiveness than permission (EAFP) use when you expect the key to be present"""
    def execute_command(self, command_name:str):
        try:
            self.commands[command_name].execute()
        except KeyError:
            print(f"Command '{command_name}' not found")

