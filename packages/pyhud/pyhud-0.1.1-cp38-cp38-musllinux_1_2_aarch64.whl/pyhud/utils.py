from typing import Any, Callable, TypeVar

from .logging import internal_logger

T = TypeVar("T")


def supress_exceptions(
    default_return_value: T,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                internal_logger.exception(
                    "Exception in {}: {}".format(func.__name__, e)
                )
                return default_return_value

        return wrapper

    return decorator
