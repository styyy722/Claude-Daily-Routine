#!/usr/bin/env python3
"""Send a markdown report file to Discord as sequential messages.

Usage: python3 scripts/send_discord.py <path-to-report.md>

Reads DISCORD_BOT_TOKEN and DISCORD_CHANNEL_ID from the environment. Splits
the file at markdown section boundaries ("## ") to stay under Discord's
2000-character message limit, and sends each chunk as a separate message in
order. No file attachments are used.

Discord's Cloudflare edge returns a 403 (error code 1010) for requests using
the default urllib/requests User-Agent string, even with a valid bot token —
so a real User-Agent header is required on every request.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

DISCORD_API = "https://discord.com/api/v10"
USER_AGENT = "DiscordBot (https://github.com/styyy722/Claude-Daily-Routine, 1.0)"
MAX_MESSAGE_LEN = 2000
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2


def split_into_chunks(text, max_len=MAX_MESSAGE_LEN):
    lines = text.split("\n")
    chunks = []
    current = ""

    def flush():
        nonlocal current
        if current.strip():
            chunks.append(current.rstrip("\n"))
        current = ""

    for line in lines:
        is_section_boundary = line.startswith("## ") or line.startswith("# ")
        candidate = current + line + "\n"
        if is_section_boundary and current.strip():
            flush()
            current = line + "\n"
            continue
        if len(candidate) > max_len:
            if current.strip():
                flush()
            if len(line) > max_len:
                for i in range(0, len(line), max_len):
                    chunks.append(line[i:i + max_len])
                current = ""
            else:
                current = line + "\n"
        else:
            current = candidate

    flush()
    return chunks


def send_message(channel_id, token, content):
    url = f"{DISCORD_API}/channels/{channel_id}/messages"
    body = json.dumps({"content": content}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bot {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", USER_AGENT)

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                resp.read()
            return
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            last_error = f"HTTP {e.code}: {detail}"
            if e.code == 429 and attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)
                continue
            break
        except urllib.error.URLError as e:
            last_error = str(e)
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)
                continue
            break
    raise RuntimeError(f"Failed to send message to Discord: {last_error}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/send_discord.py <path-to-report.md>", file=sys.stderr)
        return 2

    path = sys.argv[1]
    token = os.environ.get("DISCORD_BOT_TOKEN")
    channel_id = os.environ.get("DISCORD_CHANNEL_ID")

    if not token or not channel_id:
        print("DISCORD_BOT_TOKEN and DISCORD_CHANNEL_ID must be set in the environment.", file=sys.stderr)
        return 2

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = split_into_chunks(content)
    if not chunks:
        print(f"Nothing to send: {path} is empty.", file=sys.stderr)
        return 2

    for i, chunk in enumerate(chunks, start=1):
        try:
            send_message(channel_id, token, chunk)
            print(f"Sent chunk {i}/{len(chunks)} ({len(chunk)} chars).")
        except RuntimeError as e:
            print(f"Failed sending chunk {i}/{len(chunks)}: {e}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
