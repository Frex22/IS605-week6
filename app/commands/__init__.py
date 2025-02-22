from app.commands import CommandHandler
from app.commands import DiscordCommand
from app.commands import ExitCommand
from app.commands import GoodbyeCommand
from app.commands import GreetCommand
from app.commands import MenuCommand

class App:
    def __init__(self):
        self.command_handler = CommandHandler()

    def start(self):
        self.command_handler.register_command("greet", GreetCommand())
        self.command_handler.register_command("goodbye", GoodbyeCommand())
        self.command_handler.register_command("menu", MenuCommand())
        self.command_handler.register_command("exit", ExitCommand())
        self.command_handler.register_command("discord", DiscordCommand())

        print("Type 'Exit to quit the program")
        while True:
            self.command_handler.execute_command(input(">>> ").strip())

