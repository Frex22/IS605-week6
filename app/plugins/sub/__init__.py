from app.commands import Command
def get_float (prompt):
    """
    Helper function to get valid value from float"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid Value. Please Try Again.")

class SubCommand(Command):
    def execute(self):
        """ 
        This method executes the sub command
        """
        a = get_float("Enter first number: ")
        b = get_float("Enter second number: ")
        print(f"Result: {a} - {b} = {a - b}")
