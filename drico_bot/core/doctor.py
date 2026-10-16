"""Health checks for `drico doctor` (Phase 13)."""

import os
import sys

from drico_bot.core.config import load_config
from drico_bot.core.security import DATA_DIR_MODE, SECRET_FILE_MODE, warn_data_permissions
from drico_bot.knowledge.pack import get_drico_home, get_knowledge_db_path, get_packs_root
from drico_bot.storage.database import ensure_db


def run_doctor():
    lines = ["Drico doctor"]
    home = get_drico_home()
    lines.append("Python: {0}".format(sys.version.split()[0]))
    lines.append("DRICO_HOME: {0}".format(home))
    lines.append("Home exists: {0}".format(home.is_dir()))
    warn_data_permissions(str(home))
    config = load_config()
    lines.append("Config loaded: {0}".format(bool(config)))
    plugins_dir = home / "plugins"
    lines.append("User plugins dir: {0} (exists={1})".format(plugins_dir, plugins_dir.is_dir()))
    packs = get_packs_root()
    lines.append("Packs root: {0}".format(packs))
    ensure_db()
    db_path = home / "drico.db"
    lines.append("SQLite db: {0} (exists={1})".format(db_path, db_path.is_file()))
    kbase = get_knowledge_db_path()
    lines.append("Knowledge index db: {0} (exists={1})".format(kbase, kbase.is_file()))
    lines.append("Permissions target: dirs {0:o}, secret files {1:o}".format(DATA_DIR_MODE, SECRET_FILE_MODE))
    if os.environ.get("NO_COLOR"):
        lines.append("NO_COLOR: set")
    return "\n".join(lines)
