import sys
from app.commands import Command
class ExitCommand(Command):
    def execute(self):
        """
        This method executes the exit command
        """
        sys.exit("Exiting the program...")
