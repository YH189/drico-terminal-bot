"""AST-based safe arithmetic evaluation (no eval/exec)."""

import ast
import math
import operator

MAX_CALC_LENGTH = 200
MAX_MAGNITUDE = 1e100
MAX_DEPTH = 50

ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

ALLOWED_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}

ALLOWED_FUNCS = {
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
}

ALLOWED_NAMES = {"pi": math.pi, "e": math.e}


class SafeCalcError(Exception):
    pass


def _check_magnitude(value):
    if isinstance(value, (int, float)):
        if abs(value) > MAX_MAGNITUDE or math.isnan(value) or math.isinf(value):
            raise SafeCalcError("Result is out of range.")
    return value


def _eval_node(node, depth):
    if depth > MAX_DEPTH:
        raise SafeCalcError("Expression is too deeply nested.")
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, depth + 1)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return _check_magnitude(node.value)
        raise SafeCalcError("Only numbers are allowed.")
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_BINOPS:
            raise SafeCalcError("Operator not allowed.")
        left = _eval_node(node.left, depth + 1)
        right = _eval_node(node.right, depth + 1)
        if op_type in (ast.Div, ast.Mod) and right == 0:
            return "Error: cannot divide by 0"
        result = ALLOWED_BINOPS[op_type](left, right)
        return _check_magnitude(result)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_UNARY:
            raise SafeCalcError("Unary operator not allowed.")
        return _check_magnitude(ALLOWED_UNARY[op_type](_eval_node(node.operand, depth + 1)))
    if isinstance(node, ast.Name):
        if node.id not in ALLOWED_NAMES:
            raise SafeCalcError("Name not allowed: {0}".format(node.id))
        return ALLOWED_NAMES[node.id]
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise SafeCalcError("Only simple function calls are allowed.")
        func_name = node.func.id
        if func_name not in ALLOWED_FUNCS:
            raise SafeCalcError("Function not allowed: {0}".format(func_name))
        if node.keywords:
            raise SafeCalcError("Keyword arguments are not allowed.")
        args = [_eval_node(arg, depth + 1) for arg in node.args]
        return _check_magnitude(ALLOWED_FUNCS[func_name](*args))
    raise SafeCalcError("Unsupported expression.")


def safe_calculate(expression):
    expression = expression.strip()
    if not expression:
        raise SafeCalcError("Empty expression.")
    if len(expression) > MAX_CALC_LENGTH:
        raise SafeCalcError("Expression is too long.")
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise SafeCalcError("Invalid syntax: {0}".format(exc.msg))
    result = _eval_node(tree, 0)
    if isinstance(result, str):
        return result
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result
