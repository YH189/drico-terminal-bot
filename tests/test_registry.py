from drico_bot.core.dispatcher import DispatchContext, Dispatcher, InteractiveSession
from drico_bot.core.registry import Command, Registry


def test_find_longest_prefix_match():
    registry = Registry()
    registry.register(
        Command(
            name="search tools",
            handler=lambda ctx: None,
            help_text="",
            category="tools",
        )
    )
    registry.register(
        Command(
            name="search",
            handler=lambda ctx: None,
            help_text="",
            category="tools",
        )
    )
    found = registry.find("search tools code")
    assert found.name == "search tools"


def test_pattern_command_priority():
    registry = Registry()
    calls = []

    registry.register(
        Command(
            name="first",
            handler=lambda ctx: calls.append("first"),
            match_fn=lambda ctx: True,
            priority=10,
        )
    )
    registry.register(
        Command(
            name="second",
            handler=lambda ctx: calls.append("second"),
            match_fn=lambda ctx: True,
            priority=20,
        )
    )
    session = InteractiveSession()
    dispatcher = Dispatcher(registry)
    dispatcher.dispatch("x", "x", session)
    assert calls == ["first"]
