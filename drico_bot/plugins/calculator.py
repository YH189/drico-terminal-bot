from drico_bot.core.registry import Command
from drico_bot.core.ui import show_loading
from drico_bot.builtin_data import MATH_PATTERN


def calculate(expression):
    match = MATH_PATTERN.fullmatch(expression)

    if not match:
        return None

    first = float(match.group(1))
    operator = match.group(2)
    second = float(match.group(3))

    if operator == "+":
        result = first + second
    elif operator == "-":
        result = first - second
    elif operator == "*":
        result = first * second
    elif operator == "/":
        if second == 0:
            return "Error: cannot divide by 0"
        result = first / second
    elif operator == "%":
        if second == 0:
            return "Error: cannot divide by 0"
        result = first % second
    else:
        return None

    if result.is_integer():
        return int(result)

    return result


def is_math(text):
    return MATH_PATTERN.fullmatch(text.strip()) is not None


def _handle_math(context):
    show_loading("Calculating")
    answer = calculate(context.normalized)
    print("Drico > The result is: {0}\n".format(answer))


def register(registry):
    registry.register(
        Command(
            name="<a><op><b>",
            handler=lambda ctx: None,
            help_text="Two-number arithmetic (+, -, *, /, %), e.g. 12+13.",
            category="calculator",
            match_fn=lambda ctx: False,
        )
    )
    registry.register(
        Command(
            name="calculator",
            handler=_handle_math,
            help_text="Basic two-operand arithmetic.",
            category="calculator",
            match_fn=lambda ctx: is_math(ctx.normalized),
            priority=10,
            show_in_help=False,
        )
    )
