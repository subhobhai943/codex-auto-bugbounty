# Skill: Codex Auto Bug Bounty

## Identifier

- id: `codex-auto-bugbounty`
- runtime: `python`
- entrypoint: `src/cli.py`

## Purpose

Automate Bugcrowd-ready vulnerability report generation, submission guidance,
and program discovery for security researchers.

## Inputs

The skill consumes a JSON object that conforms to `spec/skill-input-schema.json`:

- `program`: metadata about the Bugcrowd program and target asset.
  - `name`: human-readable program name.
  - `platform`: must be `Bugcrowd`.
  - `policy_url`: optional URL to the program brief / policy.
  - `asset_type`: e.g., `Web Application`, `API`, `Mobile App`.
  - `asset_identifier`: host, URL, or other asset identifier.
  - `program_id`: optional Bugcrowd program id (from discovery).
- `finding`: structured vulnerability description.
  - `title`: short, precise summary of the issue.
  - `weakness_class`: free-text class or taxonomy reference.
  - `cwe_id`: optional CWE identifier.
  - `severity`: severity label (e.g., `Low`, `Medium`, `High`, `Critical`).
  - `description`: detailed narrative of the vulnerability.
  - `impact`: narrative description of impact.
  - `environment`: environment label (e.g., `Production`).
  - `steps_to_reproduce`: ordered list of deterministic steps.
  - `expected_result`: what should have happened.
  - `actual_result`: what actually happened.
  - `evidence`: optional list of evidence objects.
    - `type`: evidence type (e.g., `http_capture`, `screenshot`).
    - `path`: file path or URI.
    - `description`: optional human-readable note.

## Outputs

The skill produces a JSON object that conforms to `spec/skill-output-schema.json`:

- `bugcrowd_report`:
  - `title`: derived from `finding.title`.
  - `weakness_type`: derived from `finding.weakness_class`.
  - `severity`: copied from `finding.severity`.
  - `asset`: formatted from `program.asset_type` and `program.asset_identifier`.
  - `environment`: copied from `finding.environment`.
  - `steps_to_reproduce`: copied from `finding.steps_to_reproduce`.
  - `expected_result`: copied from `finding.expected_result`.
  - `actual_result`: copied from `finding.actual_result`.
  - `impact`: copied from `finding.impact`.
  - `attachments`: normalised from `finding.evidence`.
- `submission_guide`:
  - `checklist`: ordered steps to submit on Bugcrowd.
  - `notes`: best-practice guidance for clear triage.

## Program Discovery

The auxiliary module `src/bugcrowd_discovery.py` exposes:

- `list_programs(params: dict | None) -> list[dict]`

This function calls the Bugcrowd API using the `BUGCROWD_API_TOKEN`
environment variable and returns a simplified list of programs visible to the
researcher:

- `id`: Bugcrowd program id.
- `name`: program name.
- `status`: program status (e.g., `live`).
- `rewards`: reward / payout information.
- `brief_url`: URL to the program brief.

Codex runtimes can use this to:

1. Discover available programs.
2. Select a program by id.
3. Populate the `program` section of the skill input automatically.

## Invocation Semantics

- Input MUST be fully validated against the input schema before calling the
  skill.
- The skill is stateless; each invocation is independent.
- Program discovery is best-effort; errors (auth, network) should be handled
  by the caller.

## Versioning

- `version`: `0.1.0`
- Changes to the input or output schema MUST bump the version and be recorded
  in the repository changelog.
