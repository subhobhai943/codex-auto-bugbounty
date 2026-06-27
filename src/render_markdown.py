#!/usr/bin/env python3

"""Markdown rendering for Codex Auto Bug Bounty skill.

This module turns the structured JSON output of `generate_bugcrowd_payload`
into Markdown documents suitable for reports and submission guides.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


def _slugify(value: str) -> str:
    return "-".join(value.lower().strip().split())[:80]


def render_report_md(output: Dict[str, Any]) -> str:
    report = output["bugcrowd_report"]

    lines = []
    lines.append(f"# {report.get('title', 'Bugcrowd Report')}")
    lines.append("")
    lines.append(f"**Weakness type:** {report.get('weakness_type', '')}")
    lines.append(f"**Severity:** {report.get('severity', '')}")
    lines.append(f"**Asset:** {report.get('asset', '')}")
    env = report.get("environment")
    if env:
        lines.append(f"**Environment:** {env}")
    lines.append("")

    impact = report.get("impact")
    if impact:
        lines.append("## Impact")
        lines.append(impact)
        lines.append("")

    steps = report.get("steps_to_reproduce") or []
    if steps:
        lines.append("## Steps to reproduce")
        for i, step in enumerate(steps, start=1):
            lines.append(f"{i}. {step}")
        lines.append("")

    expected = report.get("expected_result")
    actual = report.get("actual_result")
    if expected or actual:
        lines.append("## Expected vs actual result")
        if expected:
            lines.append(f"- **Expected:** {expected}")
        if actual:
            lines.append(f"- **Actual:** {actual}")
        lines.append("")

    attachments = report.get("attachments") or []
    if attachments:
        lines.append("## Evidence / attachments")
        for att in attachments:
            label = att.get("label", "attachment")
            path = att.get("path", "")
            type_ = att.get("type", "")
            lines.append(f"- **{label}** ({type_}): `{path}`")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_submission_md(output: Dict[str, Any]) -> str:
    guide = output["submission_guide"]

    lines = []
    lines.append("# Bugcrowd submission guide")
    lines.append("")

    checklist = guide.get("checklist") or []
    if checklist:
        lines.append("## Checklist")
        for i, item in enumerate(checklist, start=1):
            lines.append(f"{i}. {item}")
        lines.append("")

    notes = guide.get("notes") or []
    if notes:
        lines.append("## Notes")
        for note in notes:
            lines.append(f"- {note}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_markdown_files(output: Dict[str, Any], base_dir: Path) -> Dict[str, str]:
    """Write report and submission guide markdown files.

    Returns a dict with keys `report_path` and `submission_path` containing
    the string paths of the created files.
    """

    report = output["bugcrowd_report"]
    title = report.get("title", "bugcrowd-report")
    slug = _slugify(title)

    reports_dir = base_dir / "reports"
    guides_dir = base_dir / "guides"
    reports_dir.mkdir(parents=True, exist_ok=True)
    guides_dir.mkdir(parents=True, exist_ok=True)

    report_md = render_report_md(output)
    submission_md = render_submission_md(output)

    report_path = reports_dir / f"{slug}.md"
    submission_path = guides_dir / f"{slug}-submission.md"

    report_path.write_text(report_md, encoding="utf-8")
    submission_path.write_text(submission_md, encoding="utf-8")

    return {
        "report_path": str(report_path),
        "submission_path": str(submission_path),
    }
