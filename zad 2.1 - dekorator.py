import functools
import logging 
from inspect import signature

logging.basicConfig(level=logging.INFO)

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        params_names_values = {}

        sig = signature(func)

        param_names = list(sig.parameters.keys())

        for name, val in zip(param_names, args):
            params_names_values[name] = type(val).__name__

        for name, val in kwargs.items():
            params_names_values[name] = type(val).__name__

        logging.info(f'{params_names_values}')
        print(params_names_values)
        
        return func(*args, **kwargs)
    return wrapper

@timer
def example_function(a, b, c):
    return a + b + c

result = example_function(1, 2, c = 3)
print("Result:", result)
