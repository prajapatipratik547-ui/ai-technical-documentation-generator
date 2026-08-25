from calculator import add, subtract, multiply, divide
from utils import format_result, validate_numbers
from config import get_app_info


def calculate(operation, a, b):
    """Perform the requested mathematical operation."""

    validate_numbers(a, b)

    if operation == "add":
        result = add(a, b)

    elif operation == "subtract":
        result = subtract(a, b)

    elif operation == "multiply":
        result = multiply(a, b)

    elif operation == "divide":
        result = divide(a, b)

    else:
        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    return format_result(
        operation,
        result,
    )


def run_demo():
    """Run example calculations."""

    app_info = get_app_info()

    print(
        f"{app_info['name']} "
        f"v{app_info['version']}"
    )

    print(
        calculate("add", 10, 5)
    )

    print(
        calculate("multiply", 6, 7)
    )


if __name__ == "__main__":
    run_demo()