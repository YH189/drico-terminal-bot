from drico_bot.builtin_data import MATH_PATTERN
from drico_bot.calc.safe_eval import SafeCalcError, safe_calculate
from drico_bot.core.registry import Command
from drico_bot.core.ui import show_loading


def calculate(expression):
    try:
        return safe_calculate(expression)
    except SafeCalcError:
        match = MATH_PATTERN.fullmatch(expression.strip())
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
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result


def is_math(text):
    text = text.strip()
    if not text:
        return False
    try:
        safe_calculate(text)
        return True
    except SafeCalcError:
        return MATH_PATTERN.fullmatch(text) is not None


def _handle_math(context):
    show_loading("Calculating")
    result = calculate(context.normalized)
    if result is None:
        print("Drico > Could not calculate that expression.\n")
        return
    print("Drico > The result is: {0}\n".format(result))


def register(registry):
    registry.register(
        Command(
            name="<expression>",
            handler=lambda ctx: None,
            help_text="Safe math (AST): + - * / % **, sqrt, abs, round, pi, e.",
            category="calculator",
            match_fn=lambda ctx: False,
        )
    )
    registry.register(
        Command(
            name="calculator",
            handler=_handle_math,
            help_text="Evaluate a math expression.",
            category="calculator",
            match_fn=lambda ctx: is_math(ctx.normalized),
            priority=10,
            show_in_help=False,
        )
    )
