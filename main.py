"""Fix Human Sleep: Funniest Patch Note — entry program.

Writes one patch-note line announcing that human sleep has been
fixed to /output/entry.txt (falling back to ./output/entry.txt only
if /output is not writable). Deterministic: the same line every run.
"""

import os

FIX_CLAUSE = "Fixed: humans now fall asleep in under 10 minutes"
CONSEQUENCE_CLAUSE = "sheep have been laid off effective immediately"


def build_line() -> str:
    """Compose the patch note from its two beats: the fix, then the
    consequence (the sheep losing their job)."""
    return f"{FIX_CLAUSE}; {CONSEQUENCE_CLAUSE}."


def validate_line(line: str) -> str:
    """Enforce every gate: UTF-8 encodable, 1-160 chars, single line,
    not only whitespace."""
    line.encode("utf-8")
    stripped = line.strip()
    if not stripped:
        raise ValueError("line must not be only whitespace")
    if len(stripped) != len(line):
        raise ValueError("line must not have leading/trailing whitespace")
    if not 1 <= len(line) <= 160:
        raise ValueError(f"line must be 1-160 chars, got {len(line)}")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    return line


def write_entry(line: str) -> str:
    """Write the line with no trailing newline; try /output first,
    fall back to ./output only if /output is not writable."""
    for base in ("/output", os.path.join(os.getcwd(), "output")):
        try:
            os.makedirs(base, exist_ok=True)
            path = os.path.join(base, "entry.txt")
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(line)
            return path
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> None:
    line = validate_line(build_line())
    path = write_entry(line)
    print(f"wrote {len(line)} chars to {path}")


if __name__ == "__main__":
    main()
