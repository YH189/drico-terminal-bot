from drico_bot.core.registry import Command


def _handle_exit(context):
    print("Drico > Thanks for using Drico.")
    context.session.running = False


def _handle_show(context):
    print("\nDrico > Commands")
    grouped = context.session.registry.help_by_category()
    for category in sorted(grouped.keys()):
        print("[{0}]".format(category))
        for label, help_text in sorted(grouped[category], key=lambda item: item[0]):
            if help_text:
                print("  {0} - {1}".format(label, help_text))
            else:
                print("  {0}".format(label))
    print()


def _handle_how_are_you(context):
    print("Drico > I am doing fine. How can I help you?\n")


def _handle_who_are_you(context):
    print("Drico > I am Drico, a simple Python AI tools router.\n")


def _handle_greeting(context):
    words = context.normalized.split()
    if "hi" in words or "hello" in words:
        print("Drico > Hello! How can I help you?\n")


def _match_greeting(context):
    words = context.normalized.split()
    return "hi" in words or "hello" in words


def _handle_plugins(context):
    print("\nDrico > Plugins:\n")
    for entry in context.session.registry.plugin_statuses():
        print("  {0}: {1}".format(entry.name, entry.status))
    print()


def register(registry):
    registry.register(
        Command(
            name="exit",
            aliases=("quit", "bye"),
            handler=_handle_exit,
            help_text="Close Drico.",
            category="basics",
        )
    )
    registry.register(
        Command(
            name="show",
            aliases=("help",),
            handler=_handle_show,
            help_text="Show this command list.",
            category="basics",
        )
    )
    registry.register(
        Command(
            name="help_question_mark",
            handler=_handle_show,
            help_text="Show the help menu (?).",
            category="basics",
            match_fn=lambda ctx: ctx.raw == "?",
            priority=5,
            show_in_help=False,
        )
    )
    registry.register(
        Command(
            name="plugins",
            handler=_handle_plugins,
            help_text="List loaded plugins and status.",
            category="basics",
        )
    )
    registry.register(
        Command(
            name="how_are_you",
            handler=_handle_how_are_you,
            help_text="Small talk response.",
            category="basics",
            match_fn=lambda ctx: "how are you" in ctx.normalized,
            priority=20,
            show_in_help=False,
        )
    )
    registry.register(
        Command(
            name="who_are_you",
            handler=_handle_who_are_you,
            help_text="Identity response.",
            category="basics",
            match_fn=lambda ctx: "who are you" in ctx.normalized,
            priority=30,
            show_in_help=False,
        )
    )
    registry.register(
        Command(
            name="greeting",
            handler=_handle_greeting,
            help_text="Greet the user.",
            category="basics",
            match_fn=_match_greeting,
            priority=40,
            show_in_help=False,
        )
    )
