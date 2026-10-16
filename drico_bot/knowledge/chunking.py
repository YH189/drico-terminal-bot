"""Line-window chunking for long documents."""

DEFAULT_WINDOW_LINES = 40
DEFAULT_OVERLAP_LINES = 5


def chunk_text_lines(text, window_lines=DEFAULT_WINDOW_LINES, overlap_lines=DEFAULT_OVERLAP_LINES):
    """
    Split text into overlapping line windows.

    Returns list of (line_start, line_end, chunk_text) with 1-based inclusive line numbers.
    """
    lines = text.splitlines()
    if not lines:
        return []

    if overlap_lines >= window_lines:
        overlap_lines = max(0, window_lines - 1)

    step = window_lines - overlap_lines
    if step < 1:
        step = 1

    chunks = []
    index = 0
    while index < len(lines):
        end_index = min(index + window_lines, len(lines))
        chunk_text = "\n".join(lines[index:end_index])
        line_start = index + 1
        line_end = end_index
        chunks.append((line_start, line_end, chunk_text))
        if end_index >= len(lines):
            break
        index += step
    return chunks
