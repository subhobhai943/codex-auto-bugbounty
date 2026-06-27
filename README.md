# Codex Auto Bug Bounty

Automated report generation, Bugcrowd submission guidance, and program
discovery.

## Overview

This skill consumes structured vulnerability data (program + finding) and
produces:

- A Bugcrowd-style report payload.
- A submission guide with checklist and notes for clear triage.
- Optional discovery of Bugcrowd programs available to the researcher.

The contract is defined by JSON schemas under `spec/` and the Python
implementation under `src/`.

## Program Discovery

The module `src/bugcrowd_discovery.py` provides `list_programs`, which queries
Bugcrowd's API for programs visible to the current researcher. It expects an
API token exposed via the `BUGCROWD_API_TOKEN` environment variable and
normalises the JSON:API response into a simple list of program objects.

## Usage

1. Prepare an input JSON that conforms to `spec/skill-input-schema.json`.
2. Run the CLI:

   ```bash
   python -m src.cli examples/session-fixation-input.json > out.json
   ```

3. Optionally, discover programs before selecting a target:

   ```bash
   export BUGCROWD_API_TOKEN=...  # from Bugcrowd API Credentials
   python -c "from src.bugcrowd_discovery import list_programs; import json; print(json.dumps(list_programs(), indent=2))" 
   ```

4. The output JSON from the CLI will conform to `spec/skill-output-schema.json`
   and can be used by Codex or similar runtimes to assist with Bugcrowd
   submissions.

## Codex Skill Metadata

The `codex-skill.json` file describes the tool metadata:

- `tool.id`: stable identifier for the skill.
- `tool.runtime`: `python`.
- `tool.entrypoint`: CLI module path.
- `tool.input_schema` / `tool.output_schema`: locations of the JSON schemas.

## Status

Implementation now includes report generation, submission guidance, and program
lookup via the Bugcrowd API.
