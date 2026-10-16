"""Dashboard start/stop commands (Phase 12)."""

from drico_bot.core.registry import Command
from drico_bot.dashboard import dashboard_status, start_dashboard, stop_dashboard


def _handle_dashboard(context):
    parts = context.normalized.split()
    if len(parts) >= 2 and parts[1] == "stop":
        print("Drico > {0}\n".format(stop_dashboard()))
        return
    if len(parts) >= 2 and parts[1] == "status":
        print("Drico > {0}\n".format(dashboard_status()))
        return
    print("Drico > {0}\n".format(start_dashboard()))


def register(registry):
    registry.register(
        Command(
            name="dashboard",
            handler=_handle_dashboard,
            help_text="Start local dashboard (dashboard stop | status).",
            category="interface",
        )
    )
