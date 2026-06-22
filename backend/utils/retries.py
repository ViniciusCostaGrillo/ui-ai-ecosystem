import asyncio
import functools
import time
from typing import Any, Callable, Tuple, Type, Union

from backend.utils.custom_logger import setup_logger

logger = setup_logger("utils.retries")


def retry_on_failure(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = (Exception,),
) -> Callable[..., Any]:
    """Decorator that retries a synchronous or asynchronous function on failure

    using exponential backoff.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                delay = initial_delay
                for attempt in range(1, max_retries + 1):
                    try:
                        return await func(*args, **kwargs)
                    except exceptions as e:
                        if attempt == max_retries:
                            logger.error(
                                f"Failed executing {func.__name__} after {max_retries} attempts. Error: {e}"
                            )
                            raise
                        logger.warning(
                            f"Attempt {attempt}/{max_retries} failed for {func.__name__} due to {type(e).__name__}: {e}. "
                            f"Retrying in {delay:.2f}s..."
                        )
                        await asyncio.sleep(delay)
                        delay *= backoff_factor
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                delay = initial_delay
                for attempt in range(1, max_retries + 1):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        if attempt == max_retries:
                            logger.error(
                                f"Failed executing {func.__name__} after {max_retries} attempts. Error: {e}"
                            )
                            raise
                        logger.warning(
                            f"Attempt {attempt}/{max_retries} failed for {func.__name__} due to {type(e).__name__}: {e}. "
                            f"Retrying in {delay:.2f}s..."
                        )
                        time.sleep(delay)
                        delay *= backoff_factor
            return sync_wrapper
    return decorator
