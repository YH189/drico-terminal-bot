import re

from drico_bot.core.registry import Command
from drico_bot.core.text import normalize_text
from drico_bot.core.ui import show_loading
from drico_bot.builtin_data import REFERENCES


def find_reference(text):
    text = normalize_text(text)
    words = set(text.split())

    if "c++" in text:
        return "c++"

    for topic in REFERENCES:
        if topic in words:
            return topic

    return None


def find_reference_command(text, reference):
    text = normalize_text(text)

    for command in sorted(reference.keys(), key=len, reverse=True):
        pattern = r"(?<!\w){0}(?!\w)".format(re.escape(command))
        if re.search(pattern, text):
            return command

    return None


def _handle_references_list(context):
    print("\nDrico > Programming references:\n")
    for topic in REFERENCES:
        print("  - {0}".format(topic))

    print()


def _handle_commands_topic(context):
    user = context.normalized
    if not user.startswith("commands "):
        return
    topic = user[len("commands ") :].strip()

    if topic in REFERENCES:
        print("\nDrico > {0} commands:\n".format(topic.upper()))

        for command, description in REFERENCES[topic].items():
            print("  {0}: {1}".format(command, description))
    else:
        print("Drico > Unknown reference.")
        print("Drico > Type 'references' to see available topics.")

    print()


def _handle_reference_question(context):
    topic = find_reference(context.normalized)
    if not topic:
        return

    reference = REFERENCES[topic]
    command = find_reference_command(context.normalized, reference)

    if not command:
        return

    show_loading()
    print("Drico > {0}: {1}\n".format(command, reference[command]))


def _match_reference(context):
    topic = find_reference(context.normalized)
    if not topic:
        return False
    reference = REFERENCES[topic]
    return find_reference_command(context.normalized, reference) is not None


def register(registry):
    registry.register(
        Command(
            name="references",
            aliases=("languages",),
            handler=_handle_references_list,
            help_text="List programming reference topics.",
            category="references",
        )
    )
    registry.register(
        Command(
            name="commands",
            handler=_handle_commands_topic,
            help_text="List commands for a reference topic.",
            category="references",
        )
    )
    registry.register(
        Command(
            name="reference_lookup",
            handler=_handle_reference_question,
            help_text="Explain a programming reference command.",
            category="references",
            match_fn=_match_reference,
            priority=60,
            show_in_help=False,
        )
    )
