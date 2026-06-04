"""Verify packaged file checksums."""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKSUM_FILE = ROOT / "CHECKSUMS_SHA256.txt"

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    failures = []
    for line in CHECKSUM_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, rel = line.split("  ", 1)
        path = ROOT / rel
        if not path.exists():
            failures.append((rel, "missing", expected))
            continue
        actual = digest(path)
        if actual != expected:
            failures.append((rel, actual, expected))
    if failures:
        print("FAIL checksum mismatches:")
        for rel, actual, expected in failures:
            print(f"  - {rel}: got {actual}, expected {expected}")
        return 1
    print("PASS checksums")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
