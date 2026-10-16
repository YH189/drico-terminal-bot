"""BM25 index stored in SQLite; streaming pack indexing."""

import json
import math
import os
import sqlite3
from pathlib import Path

from drico_bot.knowledge.chunking import chunk_text_lines
from drico_bot.knowledge.pack import (
    MANIFEST_FILENAME,
    get_drico_home,
    get_knowledge_db_path,
    list_installed_packs,
    load_manifest,
    manifest_files_hash,
    pack_dir,
    write_manifest,
)
from drico_bot.knowledge.tokenize import term_frequencies, tokenize

BM25_K1 = 1.5
BM25_B = 0.75

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS pack_index_meta (
    pack_name TEXT PRIMARY KEY,
    manifest_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pack_name TEXT NOT NULL,
    doc_id TEXT NOT NULL,
    title TEXT NOT NULL,
    line_start INTEGER NOT NULL,
    line_end INTEGER NOT NULL,
    source_url TEXT NOT NULL,
    text TEXT NOT NULL,
    dl INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_chunks_pack ON chunks(pack_name);

CREATE TABLE IF NOT EXISTS postings (
    term TEXT NOT NULL,
    chunk_id INTEGER NOT NULL,
    tf INTEGER NOT NULL,
    PRIMARY KEY (term, chunk_id)
);

CREATE INDEX IF NOT EXISTS idx_postings_term ON postings(term);

CREATE TABLE IF NOT EXISTS term_df (
    term TEXT PRIMARY KEY,
    df INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS corpus_stats (
    key TEXT PRIMARY KEY,
    value REAL NOT NULL
);
"""


def _connect(db_path=None):
    if db_path is None:
        db_path = get_knowledge_db_path()
    home = get_drico_home()
    home.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn):
    conn.executescript(SCHEMA_SQL)
    conn.commit()


def _delete_pack_chunks(conn, pack_name):
    rows = conn.execute(
        "SELECT id FROM chunks WHERE pack_name = ?", (pack_name,)
    ).fetchall()
    chunk_ids = [row[0] for row in rows]
    if chunk_ids:
        placeholders = ",".join("?" for _ in chunk_ids)
        conn.execute(
            "DELETE FROM postings WHERE chunk_id IN ({0})".format(placeholders),
            chunk_ids,
        )
    conn.execute("DELETE FROM chunks WHERE pack_name = ?", (pack_name,))
    conn.execute("DELETE FROM pack_index_meta WHERE pack_name = ?", (pack_name,))


def _rebuild_global_stats(conn):
    conn.execute("DELETE FROM term_df")
    conn.executescript(
        """
        INSERT INTO term_df (term, df)
        SELECT term, COUNT(DISTINCT chunk_id) FROM postings GROUP BY term;
        """
    )
    row = conn.execute("SELECT COUNT(*), AVG(dl) FROM chunks").fetchone()
    total = row[0] or 0
    avg_dl = row[1] or 0.0
    conn.execute("DELETE FROM corpus_stats")
    conn.execute(
        "INSERT INTO corpus_stats (key, value) VALUES (?, ?), (?, ?)",
        ("total_chunks", float(total), "avg_dl", float(avg_dl)),
    )


def _iter_pack_documents(pack_path, default_source_url, default_license):
    for dirpath, _dirnames, filenames in os.walk(pack_path):
        for name in sorted(filenames):
            if name == MANIFEST_FILENAME:
                continue
            path = Path(dirpath) / name
            suffix = path.suffix.lower()
            rel = str(path.relative_to(pack_path)).replace("\\", "/")
            if suffix in (".txt", ".md"):
                with open(path, "r", encoding="utf-8") as handle:
                    text = handle.read()
                yield {
                    "id": rel,
                    "title": path.name,
                    "text": text,
                    "source_url": default_source_url,
                    "license": default_license,
                }
            elif suffix == ".jsonl":
                with open(path, "r", encoding="utf-8") as handle:
                    for line_no, line in enumerate(handle, start=1):
                        line = line.strip()
                        if not line:
                            continue
                        record = json.loads(line)
                        doc_id = record.get("id") or "{0}:{1}".format(rel, line_no)
                        yield {
                            "id": str(doc_id),
                            "title": record.get("title") or doc_id,
                            "text": record.get("text") or "",
                            "source_url": record.get("source_url") or default_source_url,
                            "license": record.get("license") or default_license,
                        }


def _index_document_streaming(conn, pack_name, document, chunk_counter):
    doc_id = document["id"]
    title = document["title"]
    source_url = document.get("source_url") or ""
    text = document.get("text") or ""
    for line_start, line_end, chunk_text in chunk_text_lines(text):
        tokens = tokenize(chunk_text)
        dl = len(tokens)
        if dl == 0:
            continue
        cursor = conn.execute(
            """
            INSERT INTO chunks (
                pack_name, doc_id, title, line_start, line_end, source_url, text, dl
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (pack_name, doc_id, title, line_start, line_end, source_url, chunk_text, dl),
        )
        chunk_id = cursor.lastrowid
        tfs = term_frequencies(tokens)
        for term, tf in tfs.items():
            conn.execute(
                "INSERT INTO postings (term, chunk_id, tf) VALUES (?, ?, ?)",
                (term, chunk_id, tf),
            )
        chunk_counter[0] += 1


def index_pack(conn, pack_name, force=False):
    path = pack_dir(pack_name)
    if not path.is_dir():
        return False, 0
    manifest = load_manifest(path)
    manifest_hash = manifest_files_hash(manifest)
    row = conn.execute(
        "SELECT manifest_hash FROM pack_index_meta WHERE pack_name = ?", (pack_name,)
    ).fetchone()
    if row and row[0] == manifest_hash and not force:
        return False, 0

    _delete_pack_chunks(conn, pack_name)
    chunk_counter = [0]
    default_source = manifest.get("source_url") or ""
    default_license = manifest.get("license") or ""
    for document in _iter_pack_documents(path, default_source, default_license):
        _index_document_streaming(conn, pack_name, document, chunk_counter)

    conn.execute(
        "INSERT OR REPLACE INTO pack_index_meta (pack_name, manifest_hash) VALUES (?, ?)",
        (pack_name, manifest_hash),
    )

    manifest["chunk_count"] = chunk_counter[0]
    write_manifest(path, manifest)
    return True, chunk_counter[0]


def reindex_all(conn=None, force=False):
    close = False
    if conn is None:
        conn = _connect()
        init_db(conn)
        close = True

    changed = []
    total_chunks = 0
    for name in list_installed_packs():
        did_index, count = index_pack(conn, name, force=force)
        if did_index:
            changed.append(name)
            total_chunks += count

    _rebuild_global_stats(conn)
    conn.commit()

    if close:
        conn.close()
    return changed


def remove_pack_from_index(conn, pack_name):
    _delete_pack_chunks(conn, pack_name)
    _rebuild_global_stats(conn)
    conn.commit()


def get_corpus_stats(conn):
    rows = conn.execute("SELECT key, value FROM corpus_stats").fetchall()
    data = {key: value for key, value in rows}
    return data.get("total_chunks", 0), data.get("avg_dl", 0.0)


def bm25_score(tf, dl, df, num_docs, avg_dl):
    if num_docs <= 0 or avg_dl <= 0:
        return 0.0
    idf = math.log((num_docs - df + 0.5) / (df + 0.5) + 1.0)
    denom = tf + BM25_K1 * (1.0 - BM25_B + BM25_B * (dl / avg_dl))
    if denom <= 0:
        return 0.0
    return idf * (tf * (BM25_K1 + 1.0)) / denom


def get_stored_manifest_hash(conn, pack_name):
    row = conn.execute(
        "SELECT manifest_hash FROM pack_index_meta WHERE pack_name = ?", (pack_name,)
    ).fetchone()
    if not row:
        return None
    return row[0]
