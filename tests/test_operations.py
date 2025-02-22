"""
Parametrized tests for the Operations class.
"""
from app.operations import Operations  # Adjust this import if needed

def test_operations(a, b, operation, expected):
    """
    A single test function that receives random operation
    from conftest and calls the correct operation method to compare with
    expected
    """
    if operation is Operations.addition:
        result = Operations.addition(a,b)
    elif operation is Operations.subtraction:
        result = Operations.subtraction(a,b)
    elif operation is Operations.multiplication:
        result = Operations.multiplication(a,b)
    elif operation is Operations.division:
        result = Operations.division(a,b)
    else:
        raise ValueError(f"unknown operation {operation}")
    assert result == expected
