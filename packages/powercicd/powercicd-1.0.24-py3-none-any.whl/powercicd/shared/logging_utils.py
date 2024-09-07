import logging
import functools


# decorator to log entry and exit of a class method
call_depth = 0


def log_call(log: logging.Logger) -> callable:
    def log_call_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            global call_depth
            human_name = func.__name__.replace("_", " ")
            non_self_args = args[1:]
            all_args_str = [str(arg) for arg in non_self_args] + [f"{key}={value}" for key, value in kwargs.items()]
            # if log level is DEBUG, log the call depth
            if log.isEnabledFor(logging.DEBUG):
                log.debug(f"{human_name}: Entering {func.__name__} with params {', '.join(all_args_str)}")
            else:
                log.info(human_name)
            call_depth += 1
            try:
                result = func(*args, **kwargs)
                if log.isEnabledFor(logging.DEBUG):
                    log.debug(f"Exiting  {func.__name__}: {result}")
                else:
                    pass
            except:
                if log.isEnabledFor(logging.DEBUG):
                    log.exception(f"Exiting  {func.__name__} with exception")
                else:
                    log.exception(f"Exiting  {func.__name__} with exception")
                raise
            finally:
                call_depth -= 1
            return result
        return wrapper
    return log_call_decorator
