#!/usr/bin/env python3

"""CLI wrapper for Codex Auto Bug Bounty skill.

Usage:
    python -m src.cli examples/session-fixation-input.json > out.json

This CLI reads a skill-input JSON file, runs the transformation, and writes
skill-output JSON to stdout. Intended for integration with Codex-style runtimes
that invoke tools via subprocess.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

from .skill_core import generate_bugcrowd_payload


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
    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
