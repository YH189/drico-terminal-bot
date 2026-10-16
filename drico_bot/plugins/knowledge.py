"""Knowledge foundation commands: ask, packs, reindex, import."""

import argparse
import sys

from drico_bot.knowledge.importer import PackImportError, import_path
from drico_bot.knowledge.manager import (
    default_yes_no_prompt,
    list_packs_text,
    reindex_text,
    remove_pack,
    verify_all_packs_text,
)
from drico_bot.knowledge.query import ask


def _cmd_ask(args):
    question = " ".join(args.question).strip()
    if not question:
        print("Usage: ask <question>")
        return 1
    print(ask(question))
    return 0


def _cmd_import(args):
    try:
        manifest = import_path(
            args.path,
            args.name,
            args.license,
            version=args.version,
            source_url=args.source_url or "",
        )
    except PackImportError as exc:
        print(str(exc))
        return 1
    print(
        "Imported pack '{0}' ({1} documents). Run 'reindex' to search.".format(
            manifest["name"], manifest["doc_count"]
        )
    )
    return 0


def _cmd_packs(args):
    if args.packs_action == "list" or args.packs_action is None:
        print(list_packs_text())
        return 0
    if args.packs_action == "verify":
        print(verify_all_packs_text())
        return 0
    if args.packs_action == "remove":
        print(remove_pack(args.pack_name, confirm_callback=default_yes_no_prompt))
        return 0
    print("Unknown packs subcommand.")
    return 1


def _cmd_reindex(args):
    print(reindex_text(force=args.force))
    return 0


def register(registry):
    registry.register_cli("ask", _cmd_ask, "Search loaded knowledge packs (BM25).")
    registry.register_cli("import", _cmd_import, "Import a folder or file into a new pack.")
    registry.register_cli("packs", _cmd_packs, "List, verify, or remove installed packs.")
    registry.register_cli("reindex", _cmd_reindex, "Rebuild the search index from packs.")


def build_parser(registry):
    parser = argparse.ArgumentParser(prog="drico-bot", description="Drico knowledge CLI")
    sub = parser.add_subparsers(dest="command")

    ask_parser = sub.add_parser("ask", help="Search knowledge packs")
    ask_parser.add_argument("question", nargs=argparse.REMAINDER)

    import_parser = sub.add_parser("import", help="Import documents into a pack")
    import_parser.add_argument("path")
    import_parser.add_argument("--name", required=True)
    import_parser.add_argument("--license", default=None)
    import_parser.add_argument("--version", default="1.0.0")
    import_parser.add_argument("--source-url", default="")

    packs_parser = sub.add_parser("packs", help="Manage installed packs")
    packs_sub = packs_parser.add_subparsers(dest="packs_action")
    packs_sub.add_parser("list", help="List installed packs (default)")
    remove_parser = packs_sub.add_parser("remove", help="Delete a pack")
    remove_parser.add_argument("pack_name")
    packs_sub.add_parser("verify", help="Verify file hashes")

    reindex_parser = sub.add_parser("reindex", help="Update the BM25 index")
    reindex_parser.add_argument(
        "--force", action="store_true", help="Reindex all packs even if unchanged"
    )

    return parser


def run_cli(argv, registry=None):
    if registry is None:
        from drico_bot.core.bootstrap import build_registry

        registry = build_registry()
    parser = build_parser(registry)
    if not argv:
        parser.print_help()
        return 0
    # When invoked as `drico-bot ask ...`, argv is ['ask', ...]
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    handler = registry.get_cli(args.command)
    if handler is None:
        print("Unknown command: {0}".format(args.command), file=sys.stderr)
        return 1
    return handler(args)
