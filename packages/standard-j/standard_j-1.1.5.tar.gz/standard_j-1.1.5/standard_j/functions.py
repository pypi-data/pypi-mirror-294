from standard_j.utils import *
import standard_j.log
from inspect import Signature, Parameter
import functools
import itertools
import types
import warnings


# <editor-fold desc="Experimental decorators">
class ExperimentalWarning(UserWarning):
    pass


def experimental(func):
    """
    Function decorator used to denote functions that are experimental and therefore unstable
    :param func: FunctionType Function to decorate
    :return: FunctionType Unaltered function
    """
    warnings.simplefilter("always", ExperimentalWarning)
    warnings.warn(f"Import of experimental function: {func.__name__}", ExperimentalWarning)

    return func


def experimental_class(cls):
    """
    Class decorator used to denote classes that are experimental and therefore unstable
    :param cls: ClassType Class to decorate
    :return: ClassType Unaltered class
    """
    warnings.simplefilter("always", ExperimentalWarning)
    warnings.warn(f"Import of experimental class: {cls.__name__}", ExperimentalWarning)

    return cls
# </editor-fold>


# <editor-fold desc="Overload decorator">
# <editor-fold desc="DEBUG">
DEBUG = False


if DEBUG:
    __OVERLOAD_DEBUG_FOLDER = "logs\\debug"
    __OVERLOAD_DEBUG_FILE = f"{__OVERLOAD_DEBUG_FOLDER}\\overload_log.txt"
    standard_j.log.create_log_file(__OVERLOAD_DEBUG_FOLDER, "overload_log.txt",
                                   overwrite=True, append_output_file=False)
# </editor-fold>


class DecipheredFunction(object):
    """
    A simple class used to get details about the signature of a function
    """
    def __init__(self, func: types.FunctionType):
        self.func = func
        self.inspect_sig = Signature.from_callable(func)

        self.name = func.__qualname__
        self.parameters = tuple(parameter for parameter in self.inspect_sig.parameters.values())

        self.p_only_args = []
        self.either_p_args = []
        self.either_kw_args = []
        self.kw_only_args = []
        self.var_p_args = None
        self.var_kw_args = None

        for parameter in self.parameters:
            if parameter.kind is Parameter.POSITIONAL_ONLY:
                self.p_only_args.append(parameter.name)
            elif parameter.kind is Parameter.POSITIONAL_OR_KEYWORD:
                if parameter.default is Parameter.empty:
                    self.either_p_args.append(parameter.name)
                else:
                    self.either_kw_args.append(parameter.name)
            elif parameter.kind is Parameter.KEYWORD_ONLY:
                self.kw_only_args.append(parameter.name)
            elif parameter.kind is Parameter.VAR_POSITIONAL:
                self.var_p_args = parameter
            elif parameter.kind is Parameter.VAR_KEYWORD:
                self.var_kw_args = parameter
            else:
                raise StandardJError(f"What did you even do? {parameter.name} : {parameter.kind}")

        self._base = (self.name, self.parameters)

    def __hash__(self):
        return self._base.__hash__()

    def __eq__(self, other):
        return self._base == other

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __str__(self):
        return f"DecipheredFunction(name: {self.name}, p_only: {self.p_only_args}, either_p: {self.either_p_args}, " \
               f"either_kw: {self.either_kw_args}, kw_only: {self.kw_only_args}, " \
               f"var_p: {self.var_p_args}, var_kw: {self.var_kw_args})"

    def __repr__(self):
        return str(self)

    def check(self, num_args, kwargs):
        if not len(self.p_only_args) <= num_args:
            if DEBUG:
                standard_j.log.buffer("Fail{1}", f"(p_only: {self.p_only_args})")
            return False
        if not (num_args - len(self.p_only_args) <= len(self.either_p_args) + len(self.either_kw_args) or
                self.var_p_args is not None):
            if DEBUG:
                standard_j.log.buffer("Fail{2}", f"(num_all_p: {len(self.p_only_args) + len(self.either_p_args)},",
                                      f"var_p: {self.var_p_args})")
            return False
        if not (set(filter(lambda key: key not in self.kw_only_args, kwargs)
                    ).issubset(itertools.chain(self.either_p_args, self.either_kw_args)) or
                self.var_kw_args is not None):
            if DEBUG:
                standard_j.log.buffer("Fail{3}", f"(kw_only: {self.kw_only_args},", f"either_p: {self.either_p_args},",
                                      f"either_kw: {self.either_kw_args},", f"var_kw: {self.var_kw_args})")
            return False
        if not set(self.either_p_args[num_args - len(self.p_only_args):]).issubset(kwargs):
            if DEBUG:
                standard_j.log.buffer("Fail{4}", f"(either_p: {self.either_p_args},", f"p_only: {self.p_only_args})")
            return False
        if DEBUG:
            standard_j.log.buffer("Succeed:", self)
        return True
        # DEBUG
        # p_only <= num_args
        # num_args - p_only <= all_either or var_p is not None
        # kwargs - kw_only issubset of all either OR var_kw is not None
        # all_p[num_args:] issubset of kwargs


__overloaded_functions: dict[str, list[DecipheredFunction]] = {}


@experimental
def overload(func: types.FunctionType):
    """
    A function decorator used to overload functions. NOTE: this decorator must be applied to all versions of this
    function, including the first and last instances
    :param func: The function that is to be overloaded
    :return: A wrapper function that will select the appropriate overloaded function based on the passed args and kwargs
    """
    func = DecipheredFunction(func)
    if func.name in __overloaded_functions.keys():
        __overloaded_functions[func.name].append(func)
    else:
        __overloaded_functions[func.name] = [func]

    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        matches = []
        if DEBUG:
            standard_j.log.buffer(f"{func.name}(num_args: {len(args)}, kwargs: {kwargs.keys()})")
        for sig in __overloaded_functions[func.name]:
            if sig.check(len(args), kwargs.keys()):
                matches.append(sig)
        if DEBUG:
            standard_j.log.flush(files=(__OVERLOAD_DEBUG_FILE, None))

        if len(matches) == 0:
            if DEBUG:
                standard_j.log.buffer(f"{func.name}(num_args: {len(args)},",
                                      f"kwargs: [{', '.join(k for k in kwargs.keys())}])")
                standard_j.log.buffer("No matches")
                standard_j.log.flush(status=standard_j.log.LogStatusType.ERROR, files=(__OVERLOAD_DEBUG_FILE, None))
            raise StandardJError("Error in overload: no matching functions for call: ",
                                 f"(# args: {len(args)}, kwargs: [{', '.join(k for k in kwargs.keys())}])")
        if len(matches) == 1:
            if DEBUG:
                standard_j.log.buffer(f"{func.name}(num_args: {len(args)}, kwargs: {kwargs.keys()})")
                standard_j.log.buffer(f"Match: {matches[0]}")
                standard_j.log.flush(files=(__OVERLOAD_DEBUG_FILE, None))
            return matches[0](*args, **kwargs)
        if DEBUG:
            standard_j.log.buffer(f"{func.name}(num_args: {len(args)},", f"kwargs: {kwargs.keys()})")
            standard_j.log.buffer(f"matches[{len(matches)}]:", matches)
            standard_j.log.flush(status=standard_j.log.LogStatusType.ERROR, files=(__OVERLOAD_DEBUG_FILE, None))
        raise StandardJError(f"Error in overload: too many[{len(matches)}] matching functions for call: ",
                             f"(# args: {len(args)}, kwargs: [{', '.join(k for k in kwargs.keys())}])")

    return func_wrapper
# </editor-fold>


# <editor-fold desc="Recursion Guarded decorator">
__recursion_guarded_functions = {}


@experimental
def recursion_guarded(func: typing.Callable, max_recursions: int = 0):
    """
    Function decorator that ensures the passed function will not be called recursively. Any would be recursive calls
    are ignored.  If Optional[max_limit] is provided, that is the maximum number of recursive calls allowed.

    NOTE: This function only checks for simultaneous calls to a function, if it is called multiple times successively,
    then those calls will not be ignored.
    :param func: Callable Function to decorate
    :param max_recursions: int The maximum number of recursive calls that are allowed before they are ignored
    :return: Callable Wrapper function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if func not in __recursion_guarded_functions:
            __recursion_guarded_functions[func] = 0
        elif __recursion_guarded_functions[func] < max_recursions:
            __recursion_guarded_functions[func] += 1
        else:
            return
        output = func(*args, **kwargs)
        __recursion_guarded_functions[func] -= 1
        if __recursion_guarded_functions[func] == -1:
            __recursion_guarded_functions.pop(func)
        return output
    return wrapper
# </editor-fold>


# <editor-fold desc="Switch function">
class SwitchCase(object):
    """
    Wrapper class for a lambda expression used in a switch statement. Used in case obj is a function type
    """
    def __init__(self, func: types.FunctionType | typing.Callable):
        self.func = func
        self.num_args = len(DecipheredFunction(func).parameters)

    def __call__(self, *args, **kwargs):
        if 0 < self.num_args:
            self.func(*args, **kwargs)
        else:
            self.func()


def switch(obj, cases: dict, error: Exception = None):
    """
    A functional form of the switch statement found in other languages.

    obj is checked against cases.keys() and if a match is found, the associated value is returned.
    A SwitchCase object can be used with a Function (or lambda) that returns a boolean as the parameter.

    If no match is found, an optional "DEFAULT" key is used.

    If no match is found and no "DEFAULT" key exists, a specified error will be raised or the function will return
    None if error is None
    :param obj: object to be checked
    :param cases: dict[cases_to_check, value_to_return] where each case can be an exact value, SwitchCase, or "DEFAULT"
    :param error: Exception to raise if no match is found
    :return: value_to_return from matching case or None
    :raises Exception: error is raised if no match is found and no "DEFAULT" key is specified
    """
    for case, value in cases.items():
        if case == obj:
            return value
        if isinstance(case, SwitchCase):
            if case(obj):
                return value
    if "DEFAULT" in cases.keys():
        return cases["DEFAULT"]
    if error is not None:
        raise error


def sc_switch(obj, cases: dict, error: Exception = None):
    """
    A modified version of the switch statement that allows for short-circuit evaluation.

    The values of the cases dict are placed within lambda functions to ensure they do not run
    unless that case matches obj.

    If no error is specified, the function exits without raising anything and None is returned
    :param obj: object to compare
    :param cases: dict[cases_to_match, lambda: val_to_return]
    :param error: Exception to raise if no match is found, and "DEFAULT" is not specified
    :return: val_to_return from lambda function for matching case or None if no match is found
    :raises Exception: error is raised if no match is found, and no "DEFAULT" is specified
    """
    out = switch(obj, cases, error)
    if out is not None:
        return out()
    return None
# </editor-fold>
