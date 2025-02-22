# main.py
"""
Command-line entry point for the Calculator application.
"""
import sys
from decimal import Decimal, InvalidOperation
from app.operations import Operations

def calculate_and_print(a, b, operation_name):
    """
    Parse string inputs a_value and b_value as Decimals, then perform
    the specified operation (operation_name). Print the result or an error.

    :param a_value: String representing the first number.
    :param b_value: String representing the second number.
    :param operation_name: One of 'add', 'subtract', 'multiply', or 'divide'.
    """
    operation_mappings = {
        'add': Operations.addition,
        'subtract': Operations.subtraction,
        'multiply': Operations.multiplication,
        'divide': Operations.division
    }

    try:
        a_decimal, b_decimal = map(Decimal, [a, b])
        op_func = operation_mappings.get(operation_name)
        if op_func:  # If the operation is recognized
            result = op_func(a_decimal, b_decimal)
            print(f"The result of {a} {operation_name} {b} is equal to {result}")
        else:
            print(f"Unknown operation: {operation_name}")
    except InvalidOperation:
        print(f"Invalid number input: {a} or {b} is not a valid number.")
    except ZeroDivisionError:
        print("Error: Division by zero.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """
    Main entry point. Reads arguments from sys.argv and delegates
    calculation to calculate_and_print.
    """
    if len(sys.argv) != 4:
        print("Usage: python main.py <number1> <number2> <operation>")
        sys.exit(1)

    _, a, b, operation = sys.argv
    calculate_and_print(a, b, operation)

if __name__ == "__main__":
    main()
