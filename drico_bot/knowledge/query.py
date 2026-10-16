"""Search the local BM25 index."""

from drico_bot.knowledge.index import _connect, bm25_score, get_corpus_stats, init_db
from drico_bot.knowledge.tokenize import tokenize

NOT_FOUND_MESSAGE = "Not found in your loaded packs."
# Scores below this are treated as no match (tuned for small corpora).
SCORE_THRESHOLD = 0.05


def search(question, top_k=5, db_path=None):
    """
    Return top_k hits as dicts with pack, title, line range, score, source_url, text.
    Empty list means no match above threshold.
    """
    terms = tokenize(question)
    if not terms:
        return []

    conn = _connect(db_path)
    init_db(conn)
    num_docs, avg_dl = get_corpus_stats(conn)
    if num_docs <= 0:
        conn.close()
        return []

    candidate_ids = set()
    for term in terms:
        rows = conn.execute(
            "SELECT chunk_id FROM postings WHERE term = ?", (term,)
        ).fetchall()
        for row in rows:
            candidate_ids.add(row[0])

    if not candidate_ids:
        conn.close()
        return []

    df_map = {}
    for term in terms:
        row = conn.execute("SELECT df FROM term_df WHERE term = ?", (term,)).fetchone()
        if row:
            df_map[term] = row[0]

    scored = []
    for chunk_id in candidate_ids:
        chunk = conn.execute(
            """
            SELECT pack_name, doc_id, title, line_start, line_end, source_url, text, dl
            FROM chunks WHERE id = ?
            """,
            (chunk_id,),
        ).fetchone()
        if not chunk:
            continue
        pack_name, doc_id, title, line_start, line_end, source_url, text, dl = chunk
        score = 0.0
        for term in terms:
            posting = conn.execute(
                "SELECT tf FROM postings WHERE term = ? AND chunk_id = ?",
                (term, chunk_id),
            ).fetchone()
            if not posting:
                continue
            tf = posting[0]
            df = df_map.get(term, 0)
            score += bm25_score(tf, dl, df, num_docs, avg_dl)
        if score > 0:
            scored.append(
                {
                    "pack": pack_name,
                    "doc_id": doc_id,
                    "title": title,
                    "line_start": line_start,
                    "line_end": line_end,
                    "source_url": source_url or "",
                    "score": score,
                    "text": text,
                }
            )

    conn.close()
    scored.sort(key=lambda item: item["score"], reverse=True)
    top = scored[:top_k]
    if not top or top[0]["score"] < SCORE_THRESHOLD:
        return []
    return top


def format_hits(hits):
    lines = []
    for index, hit in enumerate(hits, start=1):
        lines.append(
            "{0}. [{1}] {2} (lines {3}-{4}) score={5:.4f}".format(
                index,
                hit["pack"],
                hit["title"],
                hit["line_start"],
                hit["line_end"],
                hit["score"],
            )
        )
        if hit["source_url"]:
            lines.append("   source: {0}".format(hit["source_url"]))
        snippet = hit["text"].replace("\n", " ")
        if len(snippet) > 200:
            snippet = snippet[:197] + "..."
        lines.append("   {0}".format(snippet))
    return "\n".join(lines)


def ask(question, top_k=5, db_path=None):
    hits = search(question, top_k=top_k, db_path=db_path)
    if not hits:
        return NOT_FOUND_MESSAGE
    return format_hits(hits)
