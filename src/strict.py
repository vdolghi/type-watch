from typing import Callable, Unpack, TypedDict, Type, List, Optional, Tuple, Dict, Any, overload
import inspect
import sys
import pkgutil
from functools import wraps


class StrictDecoratorParams(TypedDict, total = False):
    """TypedDict for the parameters of the strict decorator"""
    prevent_inheritance: bool # when True, only the base class is allowed, child classes will throw an error
    skip_return: bool # when True, the return value will not be checked
    skip_arguments: List[str] # when True, these arguments will not be checked

class StrictTypeError(TypeError):
    """Error raised when a type mismatch occurs"""
    def __init__(self, name, required_type, given_type, **flags):
        self.message = f"Type mismatch: argument '{name}' expected to be '{required_type}', got '{given_type}'."
        if flags.get("check_return_type")==True:
            self.message = f"Type mismatch: return value expected to be '{required_type}', got '{given_type}'."
        if flags.get("prevent_inheritance")==True:
            self.message += f". Child classes are not allowed in place of base classes."
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
  
def is_proper_subclass(cls: Type, base: Type) -> bool:
    return issubclass(cls, base) and cls != base
def strict(**flags: Unpack[StrictDecoratorParams]) -> Callable[[Callable], Callable]:
    """Decorate a function or a class method with a strict decorator"""
    def decorate(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            bind = sig.bind(*args,**kwargs)
            bind.apply_defaults() 
            # force defaults values to be applied, if any
            current_parameters = list(sig.parameters.values())
            print("current_parameters", current_parameters)
            if bind.arguments.get("self") is not None: 
                # remove self if func is an instance method
                del bind.arguments["self"]
                del current_parameters[0]
            if bind.arguments.get("cls") is not None:
                # remove cls if func is a classmethod
                del bind.arguments["cls"]
                del current_parameters[0]
            current_values = list(bind.arguments.values())
            
            for index, parameter in enumerate(current_parameters):
                if parameter.name in flags.get("skip_arguments", []):
                    # skip the arguments that are in the list of arguments to be skipped
                    continue
                if not isinstance(current_values[index], parameter.annotation):
                    raise StrictTypeError(parameter.name, parameter.annotation, type(current_values[index]))
                else:
                    if flags.get("prevent_inheritance")==True:
                        # check if the passed class is a subclass of the expected class
                        passed_class = current_values[index].__class__
                        expected_class = parameter.annotation
                        if is_proper_subclass(passed_class, expected_class):
                            raise StrictTypeError(parameter.name, parameter.annotation, str(passed_class), prevent_inheritance = True)
            # check return type
            result = func(*args, **kwargs)
            if not flags.get("skip_return")==True:
                # check if the return type is the same as the expected type
                if (sig.return_annotation is not sig.empty):
                    expected_return_type = sig.return_annotation
                    obtained_return_type = type(result)
                    if obtained_return_type != expected_return_type:
                        raise StrictTypeError("", expected_return_type, obtained_return_type, check_return_type = True)
            
            return result
        return wrapper
    return decorate

class StrictTypeChecking(type):
    """Metaclass that applies the strict decorator to all the methods of a class"""
    def __new__(cls: Type[type], name: str, bases: Tuple[Type, ...], attrs: Dict [str, Any]) -> Type[type]:
        print("attrs", attrs)
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, staticmethod):
                attrs[attr_name] = staticmethod(strict()(attr_value.__func__))
            elif isinstance(attr_value, classmethod):
                attrs[attr_name] = classmethod(strict()(attr_value.__func__))
            else:
                if callable(attr_value):
                    attrs[attr_name] = strict()(attr_value)
        print("attrs", attrs)
        return super().__new__(cls, name, bases, attrs)

def apply_strict(pkg_name: Optional[str] = None):
    """Applies the strict decorator to all functions in the specified module."""
    if pkg_name is None:
        # if no package name is specified, apply the strict decorator to all functions in the main module
        module_globals = [obj for name,obj in inspect.getmembers(sys.modules.copy()['__main__']) if (inspect.isfunction(obj) and not name == "apply_strict" and obj.__module__ == '__main__')]
        for obj in module_globals:
            setattr(sys.modules['__main__'], obj.__name__, strict()(obj))
    else:
        # if a package name is specified, apply the strict decorator to all the functions in all the modules in the package
        package = sys.modules[pkg_name]
        for _, modname, ispkg in pkgutil.walk_packages(package.__path__):
            module_globals = [obj for name,obj in inspect.getmembers(sys.modules.copy()[modname]) if (inspect.isfunction(obj) and not name == "apply_strict" and obj.__module__ == modname)]
            for obj in module_globals:
                setattr(sys.modules[modname], obj.__name__, strict()(obj))
            if ispkg:
                apply_strict(modname)
