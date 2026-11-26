"""Make the AI Judge Laugh (rama): write one office-life joke to /output/entry.txt.

Stdlib only. No network, no subprocess, no files read from outside the
repository. The joke is a constant in this file; the program validates it
against the bounty gate (UTF-8, 1-200 characters, not only whitespace,
single line) and writes it with no trailing newline, then reads the file
back and verifies the bytes match exactly.
"""

import os

JOKE = "The fire drill is the only meeting everyone attends on time, and nobody takes notes."

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def main():
    line = JOKE
    if not line or not line.strip():
        raise SystemExit("joke is empty")
    if "\n" in line or "\r" in line:
        raise SystemExit("joke must be a single line")
    if not 1 <= len(line) <= 200:
        raise SystemExit("joke must be 1-200 characters, got %d" % len(line))
    data = line.encode("utf-8")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as handle:
        handle.write(data)
    # Only the output file is made world-readable; the directory is untouched.
    try:
        os.chmod(OUTPUT_PATH, 0o644)
    except OSError:
        pass
    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    if written != data:
        raise SystemExit("verification failed: entry.txt does not match the joke")
    print("wrote %d characters to %s" % (len(line), OUTPUT_PATH))


if __name__ == "__main__":
    main()
