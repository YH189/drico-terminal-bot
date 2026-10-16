"""Local knowledge packs: import, index, and search (offline, stdlib-only)."""

from drico_bot.knowledge.pack import get_drico_home, get_knowledge_db_path, get_packs_root

__all__ = [
    "get_drico_home",
    "get_knowledge_db_path",
    "get_packs_root",
]
