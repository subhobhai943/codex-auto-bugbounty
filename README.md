# Codex Auto Bug Bounty

Automated report generation and Bugcrowd submission guidance skill.

## Overview

This skill consumes structured vulnerability data (program + finding) and
produces:

- A Bugcrowd-style report payload.
- A submission guide with checklist and notes for clear triage.

The contract is defined by JSON schemas under `spec/` and the Python
implementation under `src/`.

## Usage

1. Prepare an input JSON that conforms to `spec/skill-input-schema.json`.
2. Run the CLI:

   ```bash
   python -m src.cli examples/session-fixation-input.json > out.json
   ```

3. The output JSON will conform to `spec/skill-output-schema.json` and can be
   used by Codex or similar runtimes to assist with Bugcrowd submissions.

## Codex Skill Metadata

The `codex-skill.json` file describes the tool metadata:

- `tool.id`: stable identifier for the skill.
- `tool.runtime`: `python`.
- `tool.entrypoint`: CLI module path.
- `tool.input_schema` / `tool.output_schema`: locations of the JSON schemas.

## Status

Initial implementation complete: schemas, core transformation, CLI wrapper, and
one example finding.
