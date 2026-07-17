#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_BYTES = 2 * 1024 * 1024
EXCLUDED_PARTS = {".git", ".venv", "venv", "node_modules", "__pycache__"}
BINARY_SUFFIXES = {
    ".7z", ".avi", ".bin", ".bmp", ".class", ".db", ".dll", ".docx",
    ".exe", ".gif", ".gz", ".ico", ".jar", ".jpeg", ".jpg", ".mov",
    ".mp3", ".mp4", ".pdf", ".png", ".pptx", ".pyc", ".sqlite",
    ".sqlite3", ".tar", ".webp", ".xlsx", ".zip",
}


@dataclass(frozen=True)
class SecretPattern:
    name: str
    regex: re.Pattern[str]


PATTERNS = (
    SecretPattern("OpenAI-style API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    SecretPattern("GitHub classic token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    SecretPattern("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b")),
    SecretPattern("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    SecretPattern("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    SecretPattern("Slack token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{20,}\b")),
    SecretPattern("Private key material", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)


def scan_text(text: str) -> list[tuple[str, int]]:
    findings: list[tuple[str, int]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if "secret-scan: allow" in line:
            continue
        for pattern in PATTERNS:
            if pattern.regex.search(line):
                findings.append((pattern.name, line_number))
    return findings


def iter_scannable_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in BINARY_SUFFIXES:
            continue
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
        except OSError:
            continue
        yield path


def scan_repository(root: Path) -> list[str]:
    findings: list[str] = []
    for path in iter_scannable_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for pattern_name, line_number in scan_text(text):
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
