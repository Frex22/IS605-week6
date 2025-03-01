from app.commands import Command
import logging
class GreetCommand(Command):
    def execute(self):
        """
        This method executes the greet command
        """
        logging.info("Executing Greet Command")
        print("Hello World!")
