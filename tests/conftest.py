#conftest.py
import pytest
from decimal import Decimal
from faker import Faker
from app.operations import Operations


fake = Faker()

def generate_test_data(num_records):
    #define operations mappings for both calculator and operation tests
    operation_mappings={
        'addition': Operations.addition,
        'subtraction': Operations.subtraction,
        'multiplication': Operations.multiplication,
        'division' : Operations.division

    }
    #generate test data
    for _ in range(num_records):
        a = Decimal(fake.random_number(digits=2))
        b = Decimal(fake.random_number(digits=2)) if _% 4 !=3 else Decimal(fake.random_number(digits=1))
        '''means: Most of the time” (_ % 4 != 3), generate a 2-digit random number (range 0–99). But every 4th iteration” (_ % 4 == 3), generate a 1-digit random number (range 0–9). '''
        operation_name = fake.random_element(elements=list(operation_mappings.keys()))
        operation_func = operation_mappings[operation_name]

        if operation_func == Operations.division:
            b = Decimal('1') if b == Decimal('0') else b #If b is zero, replace it with one. Otherwise, keep it as is.

        try:
            if operation_func == Operations.division and b == Decimal('0'):
                expected = "ZeroDivisionError"
            
            else:
                expected = operation_func(a,b)
        except ZeroDivisionError:
            expected = "ZeroDivisionError"
        
        yield a, b, operation_name, operation_func, expected
    
def pytest_addoption(parser):
    parser.addoption("--num_records", action="store", default=5, type=int, help="Number of test records to generate")

def pytest_generate_tests(metafunc):
    #check if the test is expecting any of the dynamically generated fixtures
    if {"a", "b", "expected"}.intersection(set(metafunc.fixturenames)):
        num_records = metafunc.config.getoption("num_records")
        parameters = list(generate_test_data(num_records))
        modified_parameters = [(a, b, op_name if 'operation_name' in metafunc.fixturenames else op_func, expected) for a, b, op_name, op_func, expected in parameters]
        metafunc.parametrize("a,b,operation,expected", modified_parameters)






