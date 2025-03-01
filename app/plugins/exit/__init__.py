import sys
import logging
from app.commands import Command
class ExitCommand(Command):
    def execute(self):
        """
        This method executes the exit command
        """
        logging.info("Exiting the program...")
        print("Exiting the program...")
        sys.exit("Exiting the program...")
        raise SystemExit("Exiting the program...")


