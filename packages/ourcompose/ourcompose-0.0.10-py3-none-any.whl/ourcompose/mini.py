import inspect
from functools import wraps, partial
from typing import Optional, List
from graphlib import TopologicalSorter
from itertools import starmap

def dynamic_function_builder(*functions):
    # 1. Collect the parameter names from all functions
    all_params = {}
    for func in functions:
        signature = inspect.signature(func)
        for name, param in signature.parameters.items():
            if name not in all_params:
                all_params[name] = param

    # 2. Build the dynamic function with the union of parameters
    def dynamic_func(**kwargs):
        results = {}
        for func in functions:
            # Extract the subset of parameters needed for this function
            func_signature = inspect.signature(func)
            func_args = {k: v for k, v in kwargs.items() if k in func_signature.parameters}
            
            # Call the original function with its specific arguments
            results[func.__name__] = func(**func_args)
        return results

    # Dynamically build the signature for the new function (for better introspection)
    new_signature = inspect.Signature(parameters=all_params.values())
    dynamic_func.__signature__ = new_signature
    return dynamic_func

def execute(slf, functions: dict, *args, **kwargs):

    # Collect leafs
    leafs = list(
        filter(
            lambda piece: len(getattr(functions[piece], 'dependencies', [])) == 0,
            functions.keys()
        )
    )

    result = {}
    for name in TopologicalSorter(
        dict(
            starmap(
                lambda name, fn: (
                    name,
                    fn.dependencies
                ),
                functions.items()
            )
        )
    ).static_order():
        fn = functions[name]
        if name in leafs:
            # Only call leaf functions with kwargs
            fn_signature = inspect.signature(fn)
            fn_kwargs = {k: v for k, v in kwargs.items() if k in fn_signature.parameters}
            result[name] = fn(slf, **fn_kwargs)
        else:
            args = [
                result[dep] 
                for dep in fn.dependencies
            ]
            result[name] = fn(slf, *args)

    return result

def compose(cls_instance):

    # Get all the functions that are not dunder methods
    candidate_function_names = list(
        filter(
            lambda name: not (name.startswith('__') or name.endswith('__')), 
            filter(
                lambda name: (
                    inspect.isfunction(getattr(cls_instance, name))
                    and not (
                        isinstance(cls_instance.__dict__[name], staticmethod)
                        or isinstance(cls_instance.__dict__[name], property)
                    )
                ),
                cls_instance.__dict__
            )
        )
    )

    # Create a dictionary of the functions
    candidate_functions = dict(
        zip(
            candidate_function_names,
            map(
                lambda name: getattr(cls_instance, name),
                candidate_function_names
            )
        )
    )

    # Check after dependencies by looking at the function signature
    # If the function has a parameter with the same name as another function,
    # we assume it is a dependency
    for name in candidate_functions:
        fn = getattr(cls_instance, name)
        dependencies = list(
            filter(
                lambda param: param in candidate_functions,
                inspect.signature(fn).parameters.keys()
            )
        )
        setattr(fn, 'dependencies', dependencies)

    functions = dict(
        zip(
            candidate_function_names,
            map(
                lambda name: getattr(cls_instance, name),
                candidate_function_names
            )
        )
    )
    
    def __call__(self, *args, **kwargs):
        result = execute(self, functions, *args, **kwargs)
        return result[next(reversed(result))]
    
    # Add the __call__ method to the class
    setattr(cls_instance, '__call__', __call__)
    
    return cls_instance