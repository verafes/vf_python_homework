# Task 2.2 - the type_converter decorator
def type_converter(type_of_output):
    "Decorator that converts the return value of the function to a specified type."
    def decorator(func):
        """Wraps the target function and ensures its return value is converted to the specified type."""
        def wrapper(*args, **kwargs):
            """Executes the function and converts its return value."""
            return type_of_output(func(*args, **kwargs))
        return wrapper
    return decorator

# Task 2.3
@type_converter(str)
def return_int():
    """Returns an integer but is decorated to return a string"""
    return 5

# Task 2.4
@type_converter(int)
def return_string():
    """Returns an integer value. """
    return "not a number"

# Mainline
if __name__ == "__main__":
    y = return_int()
    print(type(y).__name__) # This should print "str"

    try:
        y = return_string()
        print("shouldn't get here!")
    except ValueError:
        print("can't convert that string to an integer!")
