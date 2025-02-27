from app.commands import Command
class GreetCommand(Command):
    def execute(self):
        """
        This method executes the greet command
        """
        print("Hello World!")

