import functools
import inspect


def exactly_one_kw_only_arg(func):
    """
    Decorator that verifies that one and only one optional argument is given

    Raises:
        ValueError: If 0 or > 1 optionla arguments are given, raise en error
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        signature = inspect.signature(func)
        keyword_only_args = [
            param.name
            for param in signature.parameters.values()
            if param.default is None
        ]
        if sum(value in keyword_only_args for value in kwargs.keys()) == 0:
            raise ValueError(f"No required arguments were given to {func.__name__} ")
        if sum(value in keyword_only_args for value in kwargs.keys()) > 1:
            raise ValueError(
                f"To many optional arguments were given to {func.__name__}. Give only one of {keyword_only_args} "
            )
        func(*args, **kwargs)

    return wrapper
