import re

from drico_bot.core.registry import Command
from drico_bot.core.text import normalize_text
from drico_bot.core.ui import show_loading
from drico_bot.builtin_data import CATEGORY_KEYWORDS, TOOLS


def find_category(text):
    words = set(re.findall(r"[a-z0-9+]+", normalize_text(text)))

    for category, keywords in CATEGORY_KEYWORDS.items():
        if words.intersection(keywords):
            return category

    return None


def show_tools(category):
    print("\nDrico > {0} tools\n".format(category.title()))

    for name, url in TOOLS[category]:
        print("{0} - {1}".format(name, url))

    print()


def show_all_tools():
    print("\nDrico > Full Tool Directory\n")

    for category, tool_list in TOOLS.items():
        print("[{0}]".format(category.title()))

        for name, url in tool_list:
            print("  {0} - {1}".format(name, url))

        print()


def _handle_list(context):
    show_all_tools()


def _handle_tool(context):
    requested = context.normalized[len("tool ") :].strip()

    matches = []

    for category, entries in TOOLS.items():
        for name, url in entries:
            if name.casefold() == requested:
                matches.append((category, name, url))

    if matches:
        for category, name, url in matches:
            print("Drico > {0} [{1}]".format(name, category))
            print("Drico > {0}\n".format(url))
    else:
        print("Drico > Tool not found.")
        print("Drico > Type 'tools' to see the full directory.\n")


def _handle_search_tools(context):
    query = context.normalized[len("search tools ") :].strip()

    matches = []

    for category, entries in TOOLS.items():
        for name, url in entries:
            if query in name.casefold():
                matches.append((category, name, url))

    if matches:
        print("\nDrico > Found {0} matching tools:\n".format(len(matches)))

        for category, name, url in matches:
            print("{0} [{1}] - {2}".format(name, category, url))
    else:
        print("Drico > No matching tools found.")

    print()


def _handle_category(context):
    category = find_category(context.normalized)
    if not category:
        return
    show_loading()
    show_tools(category)


def register(registry):
    registry.register(
        Command(
            name="list",
            aliases=("tools", "links"),
            handler=_handle_list,
            help_text="Show the full tool directory.",
            category="tools",
        )
    )
    registry.register(
        Command(
            name="tool_lookup",
            handler=_handle_tool,
            help_text="Look up a tool by name.",
            category="tools",
            match_fn=lambda ctx: ctx.normalized.startswith("tool ")
            and ctx.normalized != "tool count",
            priority=8,
        )
    )
    registry.register(
        Command(
            name="search tools",
            handler=_handle_search_tools,
            help_text="Search tools by keyword.",
            category="tools",
        )
    )
    registry.register(
        Command(
            name="category_tools",
            handler=_handle_category,
            help_text="Show tools for a category keyword.",
            category="tools",
            match_fn=lambda ctx: find_category(ctx.normalized) is not None,
            priority=70,
        )
    )
