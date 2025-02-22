""" tests/test_calculator.py 
    This model tests the basic arithmatic operations of
    the calculator using monkeypatchimg to simulate user
    input.
"""
import sys
from io import StringIO
from app.calculator import calculator

def run_calculator_with_input(monkeypatch, inputs):
    """ creating inputs for testing with help of monkeypatch """
    input_iterator = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))

    #capture output of calculator
    captured_output = StringIO()
    sys.stdout = captured_output
    calculator()
    sys.stdout = sys.__stdout__
    return captured_output.getvalue()

#positive tests
def test_addition(monkeypatch):
    """ Test addition operation in REPL """
    inputs = ["add 2 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 5.0" in output

def test_subtraction(monkeypatch):
    """ Test subtraction operation in REPL """
    inputs = ["subtract 3 2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 1.0" in output

def test_multiplication(monkeypatch):
    """ Test multiplication operation in REPL """
    inputs = ["multiply 2 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 6.0" in output


def test_division(monkeypatch):
    """ Test division operation in REPL """
    inputs = ["divide 9 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 3.0" in output

#negative tests
def test_invalid_operation(monkeypatch):
    """ Test invalid operation in REPL """
    inputs = ["modulus 5 3", "exit"]
    output =  run_calculator_with_input(monkeypatch, inputs)
    assert "Unknown Operation" in output

def test_invalid_input_format(monkeypatch):
    """ Test invalid input format in REPL """
    inputs = ["add two three", "exit"]
    output =  run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid Input. Please follow the format: <operation> <num1> <num2>" in output

def test_division_by_zero(monkeypatch):
    """ Test division by zero in REPL """
    inputs = ["divide 5 0", "exit"]
    output =  run_calculator_with_input(monkeypatch, inputs)
    assert "Division By zero is not allowed." in output
