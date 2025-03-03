import pytest
import random
import re
from decimal import Decimal
from faker import Faker
import types
from app.commands import Command
from app.plugins.add import get_float
from app.plugins.add import AddCommand
from app.plugins.sub import SubCommand
from app.plugins.multiply import MultiplyCommand
from app.plugins.divide import DivideCommand
from app.plugins.greet import GreetCommand
from app.plugins.exit import ExitCommand
from app.plugins.menu import MenuCommand
from app import CommandHandler
from app import App  # Assuming App class with load_plugins() is in app/__init__.py
from unittest.mock import patch, MagicMock
import os
import logging


fake = Faker()

@pytest.fixture
def app_instance():
    """Fixture to create a fresh App instance for each test."""
    return App()

def generate_arithmetic_test_data(num_records=10):
    """
    Dynamically generate test cases for arithmetic commands using Faker.
    Each record is a tuple: (operation_name, a, b, expected_result).
    """
    # Define operations mapping using lambda functions for simplicity.
    operations = {
        'add': (lambda a, b: a + b),
        'sub': (lambda a, b: a - b),
        'multiply': (lambda a, b: a * b),
        'divide': (lambda a, b: a / b if b != 0 else "ZeroDivisionError")
    }
    test_data = []
    for _ in range(num_records):
        # Generate random two-digit numbers for a and b.
        a = Decimal(fake.random_number(digits=2))
        b = Decimal(fake.random_number(digits=2))
        # Randomly select an operation.
        op_name = random.choice(list(operations.keys()))
        op_func = operations[op_name]
        # For division, ensure b is not zero; if it is, use 1.
        if op_name == 'divide' and b == 0:
            b = Decimal('1')
        try:
            expected = op_func(a, b)
        except ZeroDivisionError:
            expected = "ZeroDivisionError"
        test_data.append((op_name, a, b, expected))
    return test_data


@pytest.mark.parametrize("op_name, a, b, expected", generate_arithmetic_test_data(10))
def test_arithmetic_commands(monkeypatch, capsys, op_name, a, b, expected):
    """
    Test arithmetic commands (add, sub, multiply, divide) using dynamically generated test data.
    """
    # Map operation names to the corresponding command class.
    command_map = {
        'add': AddCommand,
        'sub': SubCommand,
        'multiply': MultiplyCommand,
        'divide': DivideCommand,
    }
    # Simulate user input by providing a and b as strings.
    inputs = iter([str(a), str(b)])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    cmd_class = command_map[op_name]
    cmd = cmd_class()
    cmd.execute()
    captured = capsys.readouterr().out
     #adding exception for divide mismatch issue by using aproximate comparison
    if op_name == 'divide':
        m = re.search(r"=\s*([\d\.]+)", captured)
        assert m, f"Could not find a result in output: {captured}"
        result_str = m.group(1)
        result_value = float(result_str)
        expected_value = float(expected)
        assert result_value == pytest.approx(expected_value, rel=1e-10), (
            f"Failed {op_name} with {a} and {b}. Expected: {expected_value}, Got: {result_value}"
        )
    else:
        assert str(expected) in captured, f"Failed {op_name} with {a} and {b}. Expected: {expected}"


def test_greet_command(capsys):
    """
    Test that the greet command produces a greeting message.
    """
    cmd = GreetCommand()
    cmd.execute()
    captured = capsys.readouterr().out
    # Adjust the expected substring based on your actual greeting output.
    assert "hello" in captured.lower()


def test_exit_command():
    """
    Test that the exit command raises SystemExit.
    """
    cmd = ExitCommand()
    with pytest.raises(SystemExit):
        cmd.execute()


def test_menu_command(capsys):
    """
    Test that the menu command correctly lists available commands.
    """
    # Create a dummy CommandHandler and register a few commands.
    dummy_handler = CommandHandler()
    dummy_handler.register_command("add", AddCommand())
    dummy_handler.register_command("sub", SubCommand())
    dummy_handler.register_command("greet", GreetCommand())
    # Instantiate MenuCommand with the dummy command handler.
    cmd = MenuCommand(dummy_handler)
    cmd.execute()
    captured = capsys.readouterr().out
    # Check that the output includes the registered command names.
    for key in ["add", "sub", "greet"]:
        assert key in captured, f"Menu did not list command: {key}"


def test_dynamic_plugin_loader():
    """
    Test that the App's dynamic plugin loader registers all expected plugins.
    """
    app = App()
    app.load_plugins()
    # Expected commands based on your plugins folder names.
    expected_commands = {"add", "sub", "multiply", "divide", "greet", "exit", "menu"}
    loaded_commands = set(app.command_handler.commands.keys())
    missing = expected_commands - loaded_commands
    assert not missing, f"Missing commands: {missing}"

def test_non_command_attribute_handling():
    """
    Create a dummy module with a non-class attribute to verify that
    the loader's try/except correctly ignores it.
    """
    dummy_module = types.ModuleType("dummy_plugin")
    dummy_module.not_a_command = 42  # Not a class.
    # Iterate over the dummy module attributes.
    for attr_name in dir(dummy_module):
        attr = getattr(dummy_module, attr_name)
        try:
            if issubclass(attr, Command):
                pytest.fail("Non-class attribute incorrectly processed as a command.")
        except TypeError:
            # Expected, since 42 is not a class.
            pass
def test_get_float(monkeypatch, capsys):
    """ Test the get_float function with valid input. """
    inputs = iter(["not a number", "42.5", "still no"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    result = get_float("Enter a number:")
    assert result == 42.5

def test_divide_by_zero(monkeypatch, capsys):
    """
    Test the DivideCommand when the second number (divisor) is zero.
    """
    inputs = iter(["10", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    cmd = DivideCommand()
    cmd.execute()
    captured = capsys.readouterr().out
    assert "Cannot divide by zero" in captured

def test_configure_logging_existing_config(app_instance, monkeypatch):
    """Test logging configuration when logging.conf exists."""
    monkeypatch.setattr("os.path.exists", lambda path: True)  # Simulate config file exists
    with patch("logging.config.fileConfig") as mock_file_config:
        app_instance.configure_logging()
        mock_file_config.assert_called_once()

def test_configure_logging_default_config(app_instance, monkeypatch):
    """Test default logging configuration when logging.conf is missing."""
    monkeypatch.setattr("os.path.exists", lambda path: False)  # Simulate config file missing
    with patch("logging.basicConfig") as mock_basic_config:
        app_instance.configure_logging()
        mock_basic_config.assert_called_once()

def test_load_environment_variables(app_instance, monkeypatch):
    """Test environment variable loading."""
    mock_env = {"TEST_VAR": "123", "ENV": "PROD"}
    monkeypatch.setattr(os, "environ", mock_env)
    env_vars = app_instance.load_environment_variables()
    assert env_vars["TEST_VAR"] == "123"
    assert env_vars["ENV"] == "PROD"



def test_get_environment_variable(app_instance, monkeypatch):
    """Test fetching specific environment variables."""
    monkeypatch.setattr(app_instance, "settings", {"ENV": "TEST"})
    assert app_instance.get_environment_variable("ENV") == "TEST"
    assert app_instance.get_environment_variable("NON_EXISTENT") is None

# def test_load_plugins_successful_registration(app_instance, monkeypatch):
#     """Test that plugins load successfully and commands get registered."""
#     mock_command = MagicMock()
#     mock_command_instance = mock_command.return_value
#     mock_command_instance.__class__.__name__ = "MockCommand"

#     mock_module = types.ModuleType("app.plugins.mock_plugin")
#     setattr(mock_module, "MockCommand", mock_command)

#     monkeypatch.setattr("pkgutil.iter_modules", lambda path: iter([("mock_plugin", None, True)]))
#     monkeypatch.setattr("importlib.import_module", lambda name: mock_module)

#     with patch.object(app_instance.command_handler, "register_command") as mock_register:
#         app_instance.load_plugins()
        
#         print(f"Loaded commands: {app_instance.command_handler.commands.keys()}")
#           # Ensures command registration was attempted
#         assert mock_register.called, "Expected 'register_command' to have been called."

def test_load_plugins_failure_during_import(app_instance, monkeypatch, caplog):
    """Test handling of plugin import failures."""
    def mock_import_fail(name):
        raise ImportError("Simulated import failure")

    monkeypatch.setattr("importlib.import_module", mock_import_fail)
    with caplog.at_level(logging.ERROR):
        app_instance.load_plugins()
    assert "Failed to load plugin" in caplog.text  # Ensures failure was logged

def test_load_plugins_non_command_class_ignored(app_instance, monkeypatch):
    """Test that non-command classes or attributes are ignored."""
    mock_module = types.ModuleType("mock_plugin")
    mock_module.not_a_command = 42  # Not a class
    monkeypatch.setattr("importlib.import_module", lambda name: mock_module)

    with patch.object(app_instance.command_handler, "register_command") as mock_register:
        app_instance.load_plugins()
        mock_register.assert_not_called()  # Ensure no invalid commands were registered

# def test_start_invalid_command_handling(app_instance, monkeypatch, capsys):
#     """Test execution of an invalid command logs an error but does not crash."""
#     inputs = iter(["invalid_command", "exit"])
#     monkeypatch.setattr("builtins.input", lambda _: next(inputs))

#     with pytest.raises(SystemExit):
#         app_instance.start()


#     with patch.object(app_instance.command_handler, "execute_command", side_effect=Exception("Simulated error")):
#         app_instance.start()

#     captured = capsys.readouterr().out
#     assert "An error occurred while executing command" in captured

def test_app_start_exit(monkeypatch):
    """Test The App.start by simulating user input and exit."""
    app = App()
    inputs = iter(["exit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    with pytest.raises(SystemExit):
        app.start()
