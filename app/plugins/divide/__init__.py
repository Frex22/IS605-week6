from app.commands import Command
def get_float (prompt):
    """
    Helper function to get valid value from float"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid Value. Please Try Again.")

class DivideCommand(Command):
    def execute(self):
        """ 
        This method executes the Divide command
        """
        a = get_float("Enter first number(float): ")
        b = get_float("Enter second number(float): ")
        if b == 0:
            print("Cannot divide by zero")
            return
        print(f"Result: {a} / {b} = {a / b}")
