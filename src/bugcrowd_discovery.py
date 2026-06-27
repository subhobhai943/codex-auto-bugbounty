#!/usr/bin/env python3

"""Bugcrowd program discovery module.

This module provides a thin wrapper around the Bugcrowd API for listing
programs the researcher has access to. It expects an API token to be supplied
via the BUGCROWD_API_TOKEN environment variable.

The primary function `list_programs` returns a simplified list of programs
suitable for feeding into the Codex Auto Bug Bounty skill.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

import requests

BUGCROWD_API_BASE = "https://api.bugcrowd.com"


class BugcrowdAuthError(RuntimeError):
    pass


def _get_api_token() -> str:
    token = os.getenv("BUGCROWD_API_TOKEN")
    if not token:
        raise BugcrowdAuthError(
            "BUGCROWD_API_TOKEN environment variable is not set. "
            "Create API credentials in Bugcrowd and export the token before "
            "using program discovery."
        )
    return token


def list_programs(params: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    """List Bugcrowd programs visible to the current researcher.

    `params` can include API query parameters such as filters or pagination.
    The function returns a list of dictionaries containing key details:
    - id
    - name
    - status
    - rewards
    - brief_url
    """

    token = _get_api_token()
    headers = {
        "Accept": "application/vnd.bugcrowd+json",
        "Authorization": f"Token {token}",
    }

    response = requests.get(
        f"{BUGCROWD_API_BASE}/programs",
        headers=headers,
        params=params or {},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    programs: List[Dict[str, Any]] = []

    # The Bugcrowd API uses JSON:API-style documents. We normalise a subset
    # of fields into a simpler structure for this skill.
    for item in data.get("data", []):
        attrs = item.get("attributes", {})
        programs.append(
            {
                "id": item.get("id"),
                "name": attrs.get("name"),
                "status": attrs.get("status"),
                "rewards": attrs.get("rewards"),
                "brief_url": attrs.get("brief_url"),
            }
        )

    return programs
