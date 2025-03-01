from app.commands import Command
import logging
def get_float (prompt):
    """
    Helper function to get valid value from float"""
    while True:
        try:
            value = float(input(prompt))
            logging.info(f"Value entered: {value}")
            return value
        except ValueError:
            logging.warning("Invalid Value. Please Try Again.")
            print("Invalid Value. Please Try Again.")

class DivideCommand(Command):
    def execute(self):
        """ 
        This method executes the Divide command
        """
        logging.info("Executing Divide Command")
        a = get_float("Enter first number(float): ")
        b = get_float("Enter second number(float): ")
        if b == 0:
            print("Cannot divide by zero")
            return
        result = a / b
        logging.info(f"Division Performed: {a} / {b} = {result}")        
        print(f"Result: {a} / {b} = {a / b}")
