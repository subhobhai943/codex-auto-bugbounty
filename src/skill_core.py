#!/usr/bin/env python3

"""Core entrypoint for Codex Auto Bug Bounty skill.

This module exposes a single function `generate_bugcrowd_payload` that takes
validated skill input JSON and returns the structured Bugcrowd report payload
plus a submission checklist.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Program:
    name: str
    platform: str
    policy_url: str | None
    asset_type: str
    asset_identifier: str


@dataclass
class Evidence:
    type: str
    path: str
    description: str | None = None


@dataclass
class Finding:
    title: str
    weakness_class: str
    cwe_id: str | None
    severity: str
    description: str
    impact: str
    environment: str | None
    steps_to_reproduce: List[str]
    expected_result: str | None
    actual_result: str | None
    evidence: List[Evidence]


def generate_bugcrowd_payload(input_json: Dict[str, Any]) -> Dict[str, Any]:
    """Transform validated skill input into Bugcrowd-style payload.

    This function assumes the input_json already conforms to spec/skill-input-schema.json.
    """

    program_raw = input_json["program"]
    finding_raw = input_json["finding"]

    program = Program(
        name=program_raw["name"],
        platform=program_raw.get("platform", "Bugcrowd"),
        policy_url=program_raw.get("policy_url"),
        asset_type=program_raw["asset_type"],
        asset_identifier=program_raw["asset_identifier"],
    )

    evidence_list = [
        Evidence(
            type=e["type"],
            path=e["path"],
            description=e.get("description"),
        )
        for e in finding_raw.get("evidence", [])
    ]

    finding = Finding(
        title=finding_raw["title"],
        weakness_class=finding_raw["weakness_class"],
        cwe_id=finding_raw.get("cwe_id"),
        severity=finding_raw["severity"],
        description=finding_raw["description"],
        impact=finding_raw["impact"],
        environment=finding_raw.get("environment"),
        steps_to_reproduce=finding_raw["steps_to_reproduce"],
        expected_result=finding_raw.get("expected_result"),
        actual_result=finding_raw.get("actual_result"),
        evidence=evidence_list,
    )

    bugcrowd_report = {
        "title": finding.title,
        "weakness_type": finding.weakness_class,
        "severity": finding.severity,
        "asset": f"{program.asset_type}: {program.asset_identifier}",
        "environment": finding.environment,
        "steps_to_reproduce": finding.steps_to_reproduce,
        "expected_result": finding.expected_result,
        "actual_result": finding.actual_result,
        "impact": finding.impact,
        "attachments": [
            {
                "label": ev.description or ev.type,
                "path": ev.path,
                "type": ev.type,
            }
            for ev in finding.evidence
        ],
    }

    checklist: List[str] = [
        "Login to Bugcrowd and navigate to the target program.",
        "Click 'Submit Vulnerability' and choose the appropriate asset.",
        "Paste the generated title and weakness type.",
        "Copy the steps to reproduce into the 'Steps to Reproduce' section.",
        "Copy expected vs actual result into their respective fields.",
        "Describe impact using the generated impact text.",
        "Upload the referenced evidence files as attachments.",
        "Review all fields for clarity and remove any internal notes before submission.",
    ]

    notes: List[str] = [
        "Ensure the steps are deterministic and can be followed by a triager.",
        "Avoid speculative impact; focus on concrete, demonstrable risk.",
        "Redact any sensitive data not strictly required as evidence.",
    ]

    submission_guide = {
        "checklist": checklist,
        "notes": notes,
    }

    return {
        "bugcrowd_report": bugcrowd_report,
        "submission_guide": submission_guide,
    }
