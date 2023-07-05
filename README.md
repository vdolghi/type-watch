# type-watch

"type-watch" is a Python package that provides tools for enforcing strict type checking on functions and class methods. Strict type checking can be applied to individual functions/methods or used in the form of a metaclass that applies the checks to all the methods of a class.

## Installation

Developed and tested on CPython 3.11.2. Futher testing is required for older CPython versions and for other Python implementations.

No requirements other than the standard library.

```bash

    pip install type-watch

```

## Description

The module consists of several components:

1. **`StrictDecoratorParams`**: A `TypedDict` representing the parameters that can be used with the strict decorator. These parameters include:
   - `prevent_inheritance`: When `True`, only the base class is allowed as an argument, and child classes will raise an error.
   - `skip_return`: When `True`, the return value will not be checked for type compatibility.
   - `skip_arguments`: A list of arguments that will be skipped during type checking.

2. **`StrictTypeError`**: An error class that is raised when a type mismatch occurs during type checking. This class provides detailed error messages based on the type discrepancy, including handling special cases for return type checking and inheritance prevention.

3. **`strict`**: The main decorator function that enforces strict type checking on functions and methods. It accepts various parameters from `StrictDecoratorParams` to control the behavior of the type checking. The decorator checks the type of each argument and the return value (if enabled) against their respective annotations, raising `StrictTypeError` if a type mismatch is found.

4. **`StrictTypeChecking`**: A metaclass that applies the `strict` decorator to all methods of a class. When this metaclass is used for a class, all methods of that class will undergo strict type checking based on their annotations.

5. **`apply_strict`**: A utility function that applies the `strict` decorator to functions/methods in the specified module or package. If no package name is provided, it applies the decorator to all functions/methods in the main module.

## Usage

### Using the `strict` Decorator

To use the `strict` decorator on a function or method, simply apply it above the function/method definition and provide the desired type checking options as keyword arguments. For example:

```python
@strict(prevent_inheritance=True, skip_return=False, skip_arguments=['arg_to_skip'])
def example_function(arg1: int, arg2: str) -> str:
    return str(arg1) + arg2
```

In this example, `example_function` will undergo strict type checking, checking that `arg1` is an integer and `arg2` is a string. If `prevent_inheritance` is set to `True`, it will also prevent passing child classes of the expected types.

### Using the `StrictTypeChecking` Metaclass

To apply strict type checking to all methods of a class, use the `StrictTypeChecking` metaclass as follows:

```python
class MyClass(metaclass=StrictTypeChecking):
    def method1(self, arg: int) -> str:
        return str(arg)

    def method2(self, arg: str) -> int:
        return int(arg)
```

In this example, both `method1` and `method2` will have strict type checking applied based on their annotations. 

Instance methods, classmethods and static methods are supported.

### Using the `apply_strict` Function

The `apply_strict` function applies strict type checking to all to all the functions and methods in modules or packages. If no package name is specified, it will apply the decorator to all the functions and methods in the main module. To apply it to a specific package or module, provide the package name as the argument:

```python
# Apply to all functions in the main module
apply_strict()

# Apply to all functions in a specific package
apply_strict("my_package")
```

Please note that the `apply_strict` function should be called after all functions/methods have been defined in the target module or package. It will replace the original functions/methods with their decorated versions.