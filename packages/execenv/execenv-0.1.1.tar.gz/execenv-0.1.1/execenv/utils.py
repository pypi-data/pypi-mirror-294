from typing import Any, Callable, Union

from click import Command, Context, Option, Parameter


def add_flags_callback(
    *flags: str,
    callback: Callable[[Context, Union[Option, Parameter], Any], Any],
) -> Callable:
    def callback_decorator(
        original: Callable[[Context, Union[Option, Parameter], Any], Any],
    ) -> Callable:
        def combined_callback(
            ctx: Context, param: Union[Option, Parameter], value: Any
        ):
            callback(ctx, param, value)
            return original(ctx, param, value)

        return combined_callback

    def decorator(f: Command) -> Callable:
        for param in f.params:
            if any(flag in param.opts for flag in flags):
                if param.callback:
                    param.callback = callback_decorator(param.callback)
                else:
                    param.callback = callback
        return f

    return decorator


def add_help_callback(
    callback: Callable[[Context], Any],
) -> Callable:
    def callback_decorator(
        original: Callable[[Context], Any],
    ) -> Callable:
        def combined_callback(ctx: Context):
            callback(ctx)
            return original(ctx)

        return combined_callback

    def decorator(f: Command) -> Callable:
        setattr(f, "get_help", callback_decorator(f.get_help))
        return f

    return decorator
