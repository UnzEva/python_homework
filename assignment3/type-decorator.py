def type_converter(type_of_output):
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            
            result = func(*args, **kwargs)

            try:
                return type_of_output(result)
            except ValueError as e:
                print(f"Conversion error: {e}")
                raise  # Re-raise the exception

        return wrapper
    return decorator

# Test function 1: Returns int but will be converted to str
@type_converter(str)
def return_int():
    return 5

# Test function 2: Returns string that can't be converted to int
@type_converter(int)
def return_string():
    return "not a number"

if __name__ == "__main__":
    y = return_int()
    print(type(y).__name__)  

    try:
        y = return_string()
        print("shouldn't get here!")
    except ValueError:
        print("can't convert that string to an integer!")  