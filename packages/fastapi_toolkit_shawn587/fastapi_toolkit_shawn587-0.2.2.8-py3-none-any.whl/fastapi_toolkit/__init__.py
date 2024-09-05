from typing import Callable, Generator, Any

from sqlalchemy.orm import Session


def computed_field(db_func: Callable[..., Generator[Session, Any, None]]):
    def decorator(func, *args, **kw):
        from pydantic import computed_field

        @computed_field(*args, **kw)
        def wrapper(*args_, **kw_) -> func.__annotations__.get('return'):
            return func(*args_, **kw_, db=next(db_func()))

        return wrapper

    return decorator
