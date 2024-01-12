import asyncio
from typing import Awaitable, Callable, Generator, TypeVar


R_co = TypeVar("R_co", covariant=True)


def __await__(fun: Callable[..., Awaitable[R_co]]) -> Callable[..., Generator[None, None, R_co]]:
    """Decorate a class's __await__ with this to be able to write it as an async def."""

    def wrapper(*args: object, **kwargs: object) -> Generator[None, None, R_co]:
        return fun(*args, **kwargs).__await__()

    return wrapper


def concurrently(fun: Callable[..., R_co], *args: object, **kwargs: object) -> Awaitable[R_co]:
    """
    Run a synchronous blocking computation in a different python thread, avoiding blocking the current async thread.
    This function starts the computation and returns a future referring to its result. Beware of (actual) thread-safety.
    """
    return asyncio.get_running_loop().run_in_executor(None, lambda: fun(*args, **kwargs))
