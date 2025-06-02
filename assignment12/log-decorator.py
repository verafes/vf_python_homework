import logging
from functools import wraps

#Task 1: Writing and Testing a Decorator
# Task 1.2. one time setup
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pos_args = list(args) if args else "none"
        kw_args = kwargs if kwargs else "none"
        result = func(*args, **kwargs)

        log_message = (
            f"function: {func.__name__}, "
            f"positional parameters: {pos_args}, "
            f"keyword parameters: {kw_args}, "
            f"return: {result}"
        )
        logger.log(logging.INFO, log_message)

        return result
    return wrapper

# Task 1.3
@logger_decorator
def greeting():
    print("Hello, World!")

# Task 1.4
@logger_decorator
def check_args(*args):
    print("Args received:", args)
    return True

# Task 1.5
@logger_decorator
def keyword_func(**kwargs):
    print("Keyword arguments received:", kwargs)
    return logger_decorator

# Task 1.6. Mainline code
if __name__ == "__main__":
    greeting()
    check_args(1, 20, 100, "python")
    keyword_func(a=10, b=20, name="test")