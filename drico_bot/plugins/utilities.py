"""Developer utilities (stdlib only)."""

import base64
import binascii
import hashlib
import json
import re
import uuid
from datetime import datetime, timezone

from drico_bot.core.registry import Command

MAX_JSON_BYTES = 1024 * 1024
MAX_REGEX_TEXT = 100 * 1024
MAX_REGEX_PATTERN = 200


def _nested_quantifier_warning(pattern):
    if re.search(r"\([^)]*[+*][^)]*\)[+*]", pattern):
        return True
    return False


def _handle_json(context):
    text = context.raw[len("json ") :].strip()
    if len(text.encode("utf-8")) > MAX_JSON_BYTES:
        print("Drico > JSON input exceeds 1 MB limit.\n")
        return
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        print("Drico > JSON error at line {0} column {1}: {2}\n".format(
            exc.lineno, exc.colno, exc.msg
        ))
        return
    print(json.dumps(data, indent=2, sort_keys=True))
    print()


def _handle_base64(context):
    parts = context.normalized.split()
    if len(parts) < 3:
        print("Drico > Usage: base64 encode <text> | base64 decode <text>\n")
        return
    action = parts[1]
    payload = context.raw.split(None, 2)[2] if len(context.raw.split(None, 2)) > 2 else ""
    if action == "encode":
        print(base64.b64encode(payload.encode("utf-8")).decode("ascii"))
        print()
    elif action == "decode":
        try:
            print(base64.b64decode(payload.encode("ascii"), validate=True).decode("utf-8"))
            print()
        except (binascii.Error, ValueError, UnicodeDecodeError):
            print("Drico > Invalid base64 input.\n")
    else:
        print("Drico > Usage: base64 encode <text> | base64 decode <text>\n")


def _handle_hash(context):
    if not context.normalized.startswith("hash sha256 "):
        print("Drico > Usage: hash sha256 <text>\n")
        return
    text = context.raw[len("hash sha256 ") :]
    print(hashlib.sha256(text.encode("utf-8")).hexdigest())
    print()


def _handle_uuid(context):
    print(str(uuid.uuid4()))
    print()


def _handle_timestamp(context):
    parts = context.normalized.split()
    if len(parts) == 2 and parts[1] == "now":
        now = datetime.now()
        utc = datetime.now(timezone.utc)
        print("Local: {0}".format(now.isoformat(sep=" ", timespec="seconds")))
        print("UTC:   {0}".format(utc.isoformat().replace("+00:00", "Z")))
        print()
        return
    if len(parts) != 2:
        print("Drico > Usage: timestamp now | timestamp <epoch>\n")
        return
    try:
        epoch = int(parts[1])
    except ValueError:
        print("Drico > Invalid epoch.\n")
        return
    if epoch < 0 or epoch > 253402300799:
        print("Drico > Epoch out of allowed range.\n")
        return
    dt = datetime.fromtimestamp(epoch, tz=timezone.utc)
    local = datetime.fromtimestamp(epoch)
    print("UTC:   {0}".format(dt.isoformat().replace("+00:00", "Z")))
    print("Local: {0}".format(local.isoformat(sep=" ", timespec="seconds")))
    print()


def _handle_hex(context):
    parts = context.normalized.split()
    if len(parts) != 2:
        print("Drico > Usage: hex <int>\n")
        return
    try:
        value = int(parts[1])
    except ValueError:
        print("Drico > Invalid integer.\n")
        return
    print(hex(value))
    print()


def _handle_bin(context):
    parts = context.normalized.split()
    if len(parts) != 2:
        print("Drico > Usage: bin <int>\n")
        return
    try:
        value = int(parts[1])
    except ValueError:
        print("Drico > Invalid integer.\n")
        return
    print(bin(value))
    print()


def _handle_dec(context):
    parts = context.normalized.split()
    if len(parts) != 2:
        print("Drico > Usage: dec <hex-or-bin-string>\n")
        return
    token = parts[1].lower()
    try:
        if token.startswith("0x"):
            print(int(token, 16))
        elif token.startswith("0b"):
            print(int(token, 2))
        else:
            print("Drico > Prefix with 0x or 0b.\n")
            return
    except ValueError:
        print("Drico > Invalid number.\n")
        return
    print()


def _handle_regex(context):
    if "|" not in context.raw:
        print("Drico > Usage: regex <pattern> | <text>\n")
        return
    pattern_part, text_part = context.raw.split("|", 1)
    pattern = pattern_part[len("regex ") :].strip()
    text = text_part.strip()
    if len(pattern) > MAX_REGEX_PATTERN:
        print("Drico > Regex pattern too long.\n")
        return
    if len(text.encode("utf-8")) > MAX_REGEX_TEXT:
        print("Drico > Regex text exceeds 100 KB.\n")
        return
    if _nested_quantifier_warning(pattern):
        print("Drico > Warning: pattern may be slow (nested quantifiers).")
    try:
        compiled = re.compile(pattern)
    except re.error as exc:
        print("Drico > Regex error: {0}\n".format(exc))
        return
    for match in compiled.finditer(text):
        print("match at {0}-{1}: {2}".format(match.start(), match.end(), match.group()))
    print()


def register(registry):
    registry.register(Command(name="json", handler=_handle_json, help_text="Pretty-print JSON.", category="utilities"))
    registry.register(Command(name="base64", handler=_handle_base64, help_text="Base64 encode/decode.", category="utilities"))
    registry.register(Command(name="hash", handler=_handle_hash, help_text="hash sha256 <text>", category="utilities"))
    registry.register(Command(name="uuid", handler=_handle_uuid, help_text="Generate a UUID.", category="utilities"))
    registry.register(Command(name="timestamp", handler=_handle_timestamp, help_text="timestamp now | timestamp <epoch>", category="utilities"))
    registry.register(Command(name="hex", handler=_handle_hex, help_text="hex <int>", category="utilities"))
    registry.register(Command(name="bin", handler=_handle_bin, help_text="bin <int>", category="utilities"))
    registry.register(Command(name="dec", handler=_handle_dec, help_text="dec <0x..|0b..>", category="utilities"))
    registry.register(Command(name="regex", handler=_handle_regex, help_text="regex <pattern> | <text>", category="utilities"))
