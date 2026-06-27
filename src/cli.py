#!/usr/bin/env python3

"""CLI wrapper for Codex Auto Bug Bounty skill.

Usage:
    python -m src.cli examples/session-fixation-input.json > out.json

By default, the CLI writes JSON to stdout. When the environment variable
`SKILL_WRITE_MARKDOWN` is set to `1`, it also writes Markdown report and
submission guide files under `reports/` and `guides/` respectively and prints
their paths to stderr.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

from .skill_core import generate_bugcrowd_payload
from .render_markdown import write_markdown_files


def load_input(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def main(argv: list[str] | None = None) -> None:
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        raise SystemExit("Usage: cli <input.json>")

    input_path = Path(argv[0])
    input_json = load_input(input_path)
    output = generate_bugcrowd_payload(input_json)

    # Always emit structured JSON to stdout for Codex/tooling.
    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")

    # Optionally also write Markdown files.
    if os.getenv("SKILL_WRITE_MARKDOWN") == "1":
        paths = write_markdown_files(output, base_dir=Path("."))
        sys.stderr.write(
            f"[codex-auto-bugbounty] wrote markdown: "
            f"report={paths['report_path']} submission={paths['submission_path']}\n"
        )


if __name__ == "__main__":
    main()
