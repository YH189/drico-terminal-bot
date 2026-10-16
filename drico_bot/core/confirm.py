"""Confirmation prompts (default no)."""


def confirm(prompt, stdin=None):
    if stdin is None:
        try:
            answer = input(prompt).strip().lower()
        except EOFError:
            return False
    else:
        answer = stdin.readline().strip().lower()
    return answer in ("y", "yes")


def confirm_typed(prompt, required_word, stdin=None):
    if stdin is None:
        try:
            answer = input(prompt).strip()
        except EOFError:
            return False
    else:
        answer = stdin.readline().strip()
    return answer == required_word
