import re

from drico_bot.core.registry import Command
from drico_bot.core.text import normalize_text
from drico_bot.core.ui import show_loading
from drico_bot.builtin_data import CONCEPTS, CONCEPT_ALIASES


def find_concept(text):
    text = normalize_text(text)

    for alias in sorted(CONCEPT_ALIASES, key=len, reverse=True):
        if re.search(r"(?<!\w){0}(?!\w)".format(re.escape(alias)), text):
            return CONCEPT_ALIASES[alias]

    return None


def is_concept_question(text):
    text = normalize_text(text)

    starters = (
        "what is ",
        "what are ",
        "what's ",
        "whats ",
        "explain ",
        "tell me about ",
        "define ",
        "describe ",
        "meaning of ",
        "what is the use of ",
        "what are the uses of ",
        "what is use of ",
    )

    return text.startswith(starters)


def _handle_concepts_list(context):
    print("\nDrico > Available concepts:\n")

    for topic in sorted(CONCEPTS):
        print("  - {0}".format(topic))

    print()


def _handle_concept_question(context):
    concept = find_concept(context.normalized)

    show_loading()

    if concept:
        print("Drico > {0}\n".format(CONCEPTS[concept].strip()))
    else:
        print("Drico > I don't have an explanation for that yet.")
        print("Drico > Type 'show' to see what I can answer.\n")


def register(registry):
    registry.register(
        Command(
            name="concepts",
            aliases=("topics",),
            handler=_handle_concepts_list,
            help_text="List concept topics.",
            category="concepts",
        )
    )
    registry.register(
        Command(
            name="concept_question",
            handler=_handle_concept_question,
            help_text="Answer concept questions.",
            category="concepts",
            match_fn=lambda ctx: is_concept_question(ctx.normalized),
            priority=50,
            show_in_help=False,
        )
    )
