#changing this approach to use the plugins architecture
#changing app/__init to accomodate plugins
#changing app/commands/__init to accomodate plugins
import pkgutil
import importlib
from app.commands import CommandHandler
from app.commands import Command
class App:
    #linting this block
    """
    This class is the main application class
    """
    def __init__(self):
        """
        This is the constructor for the App class
        """
        self.command_handler = CommandHandler()

    #dynamically load all plugins
    def load_plugins(self):
        """
        This method loads all plugins"""
        plugins_package = 'app.plugins'
        for _, plugin_name, is_pkg in pkgutil.iterate_modules([plugins_package.replace('.', '/' )]):
            if is_pkg:
                plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                for item_name in dir(plugin_module):
                    item = getattr(plugin_module, item_name)
                    try:
                        if issubclass(item, (Command)):
                            self.command_handler.register_command(plugin_name, item())
                    except TypeError:
                        continue

            
    def start(self):
        """
        This method starts the application
        """
        self.load_plugins()
        print("Type 'Exit to quit the program")
        while True: #REPL Read-Eval-Print Loop
            self.command_handler.execute_command(input(">>> ").strip()) #strip removes leading and trailing whitespace


