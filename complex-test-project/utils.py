def format_result(operation, result):
    """Format a calculation result for display."""
    return f"{operation}: {result}"


def validate_numbers(a, b):
    """Validate that both values are numeric."""

    if not isinstance(a, (int, float)):
        raise TypeError("First value must be a number.")

    if not isinstance(b, (int, float)):
        raise TypeError("Second value must be a number.")

    return True