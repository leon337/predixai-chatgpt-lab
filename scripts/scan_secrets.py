#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".git", ".venv", "venv", "node_modules", "__pycache__"}
BINARY_SUFFIXES = {
    ".7z", ".avi", ".bin", ".bmp", ".class", ".db", ".dll", ".docx",
    ".exe", ".gif", ".gz", ".ico", ".jar", ".jpeg", ".jpg", ".mov",
    ".mp3", ".mp4", ".pdf", ".png", ".pptx", ".pyc", ".sqlite",
    ".sqlite3", ".tar", ".webp", ".xlsx", ".zip",
}

PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("OpenAI-style API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("GitHub classic token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{20,}\b")),
    ("Private key material", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)


def scan_text(text: str) -> list[tuple[str, int]]:
    findings: list[tuple[str, int]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern_name, pattern_regex in PATTERNS:
            if pattern_regex.search(line):
                findings.append((pattern_name, line_number))
    return findings


def _git_tracked_files(root: Path) -> list[Path] | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return [root / item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


def iter_scannable_files(root: Path):
    candidates = _git_tracked_files(root)
    if candidates is None:
        candidates = [path for path in root.rglob("*") if path.is_file()]
    for path in candidates:
        if not path.is_file() or any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in BINARY_SUFFIXES:
            continue
        yield path


def scan_file(path: Path) -> list[tuple[str, int]]:
    findings: list[tuple[str, int]] = []
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            for line_number, line in enumerate(handle, start=1):
                for pattern_name, pattern_regex in PATTERNS:
                    if pattern_regex.search(line):
                        findings.append((pattern_name, line_number))
    except OSError:
        return []
    return findings


def scan_repository(root: Path) -> list[str]:
    findings: list[str] = []
    for path in iter_scannable_files(root):
        for pattern_name, line_number in scan_file(path):
            relative = path.relative_to(root)
            findings.append(f"{relative}:{line_number}: {pattern_name}")
    return findings


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    findings = scan_repository(root)
    if findings:
        print("FAIL: potential secrets detected")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("PASS: no supported secret signatures detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
