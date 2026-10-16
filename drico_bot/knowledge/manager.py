"""Pack listing, verification, removal, and reindex commands."""

import shutil

from drico_bot.knowledge.index import _connect, init_db, reindex_all, remove_pack_from_index
from drico_bot.knowledge.pack import (
    get_packs_root,
    list_installed_packs,
    load_manifest,
    pack_dir,
    pack_size_bytes,
    verify_pack,
)


def list_packs_text():
    packs = list_installed_packs()
    if not packs:
        return "No knowledge packs installed."

    lines = ["Installed knowledge packs:", ""]
    for name in packs:
        path = pack_dir(name)
        manifest = load_manifest(path)
        size = pack_size_bytes(path)
        lines.append(
            "- {0}  docs={1}  chunks={2}  license={3}  size={4} bytes".format(
                name,
                manifest.get("doc_count", "?"),
                manifest.get("chunk_count", "?"),
                manifest.get("license", "?"),
                size,
            )
        )
    return "\n".join(lines)


def verify_all_packs_text():
    packs = list_installed_packs()
    if not packs:
        return "No knowledge packs to verify."

    lines = []
    any_bad = False
    for name in packs:
        mismatches = verify_pack(pack_dir(name))
        if not mismatches:
            lines.append("{0}: OK".format(name))
        else:
            any_bad = True
            lines.append("{0}: CORRUPT ({1} file(s))".format(name, len(mismatches)))
            for rel, expected, actual in mismatches:
                if actual is None:
                    lines.append("  missing: {0} (expected sha256 {1})".format(rel, expected))
                else:
                    lines.append(
                        "  {0}: expected {1}, got {2}".format(rel, expected, actual)
                    )
    if not any_bad:
        lines.insert(0, "All packs verified successfully.")
    return "\n".join(lines)


def remove_pack(name, confirm_callback=None):
    path = pack_dir(name)
    if not path.is_dir():
        return "Pack not found: {0}".format(name)

    if confirm_callback is not None:
        if not confirm_callback("Remove pack '{0}'? [y/N] ".format(name)):
            return "Cancelled."

    shutil.rmtree(path)
    conn = _connect()
    init_db(conn)
    remove_pack_from_index(conn, name)
    conn.close()
    return "Removed pack: {0}".format(name)


def reindex_text(force=False):
    changed = reindex_all(force=force)
    if not changed:
        return "Index up to date (no manifest changes)."
    return "Reindexed pack(s): {0}".format(", ".join(changed))


def default_yes_no_prompt(message):
    try:
        answer = input(message).strip().lower()
    except EOFError:
        return False
    return answer in ("y", "yes")
