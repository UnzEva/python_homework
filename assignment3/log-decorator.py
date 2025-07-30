# Task 1: Writing and Testing a Decorator
# one time setup
import logging
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        
        func_name = func.__name__
        pos_args = args if args else "none"
        kw_args = kwargs if kwargs else "none"
        
        log_message = (
            f"function: {func_name}\n"
            f"positional parameters: {pos_args}\n"
            f"keyword parameters: {kw_args}\n"
            f"return: {result}\n"
            f"{'-'*40}"
        )
        
        # Write log record 
        logger.log(logging.INFO, log_message)
        
        return result
    
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__module__ = func.__module__
    
    return wrapper

# Test function 1: No parameters, returns nothing
@logger_decorator
def hello_world():
    print("Hello, World!")

# Test function 2: Variable positional arguments, returns True
@logger_decorator
def accepts_positional_args(*args):
    return True

# Test function 3: Keyword arguments, returns the decorator itself
@logger_decorator
def accepts_keyword_args(**kwargs):
    return logger_decorator

if __name__ == "__main__":
    hello_world() 
    accepts_positional_args(1, "two", [3, 4])
    accepts_keyword_args(name="Alice", age=30, role="Developer")
    
    print("Check decorator.log for the logged function calls")