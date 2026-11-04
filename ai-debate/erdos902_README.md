# Erdős #902 debate

Grok 4.7 Extra High and Claude Opus 5.5 work as coauthors on Schütte's tournament problem (Erdős #902). Grok proposes a proof. Opus says whether that proof is correct, wrong, or missing a step, and writes the missing mathematics. They alternate until they agree on a proof marked PROVED or COMPUTED, or until 5 rounds. Each call is stateless. Neither agent may edit files or run tools during a turn.

The established list is the literature bounds that public sources still state (`f(1)=3`, `f(2)=7`, `f(3)=19`, `48 ≤ f(4) ≤ 67`) together with the owner's later claims from `FILE_INDEX.md` (including the pending hand proof of `f(4) ≥ 51`). Agents are told to flag a conflict instead of silently overriding that list.

## Usage

```powershell
python ai-debate\erdos902_debate.py
python ai-debate\erdos902_debate.py --rounds 5 --timeout 900
python ai-debate\erdos902_debate.py --opening-prompt "Attack only circulant tournaments of prime order between 53 and 61."
```

`--rounds` is the number of Grok turns. After each one, Opus reviews it. The maximum is 5. The default timeout is 480 seconds per call. If Grok is still thinking at the limit, Grok rewrites a short public argument and Opus sees only that. Opus is not given the raw thinking trace.

```powershell
python ai-debate\erdos902_debate.py --resume erdos902_debate_20261018_114441.md --timeout 2400
```

`--resume` keeps every completed turn in the named transcript and continues from the next one. The new transcript is still a fresh `erdos902_debate_<timestamp>.md`.

The transcript is written to `erdos902_debate_<timestamp>.md` in the project root (override with `--out-dir`).

The loop stops early only when the two latest `STATUS` lines match and both `CLAIM_TAG` values are `PROVED` or `COMPUTED`.

## Rerun with a different starting prompt

`--opening-prompt` is appended to every turn as an additional direction. The problem statement and the established-results list stay fixed. Example:

```powershell
python ai-debate\erdos902_debate.py --rounds 3 --opening-prompt "Ignore circulant tournaments. Look only at whether a regular tournament on 53 vertices can have S_4."
```

## What each turn must contain

Every claim is labelled `PROVED`, `COMPUTED`, `CONJECTURE`, or `RECALLED FROM LITERATURE`. A proposed tournament must contain a `CONSTRUCTION` block (`type: paley` or `type: circulant`) so the script can check property `S_k` directly. Each turn ends with `STATUS:`, `CONFIDENCE:`, and `CLAIM_TAG:`.

After the debate the script checks every such block by exhaustive search, and it also checks the known Paley tournaments `QR_7` and `QR_19` so a broken checker is visible.

## Flags

Claude (`claude --help`):

- `-p --model claude-opus-5-5 --effort high`
- `--effort` is the documented flag. Choices are `low`, `medium`, `high`, `xhigh`, `max`. High was requested.
- `--tools ""`, `--restricted`, `--permission-mode dontAsk`
- `--disallowed-tools Bash,PowerShell,Edit,Write,Read,WebFetch,WebSearch,NotebookEdit,Task`
- `--disable-slash-commands`, `--strict-mcp-config`, `--no-session-persistence`
- The prompt is piped on stdin, because `--tools` and `--disallowed-tools` are variadic

Cursor (`cursor-agent --help` and `--list-models`):

- `-p --mode ask --trust --output-format stream-json --stream-partial-output --model grok-4.7-xhigh`
- That slug is Grok 4.7 Extra High in `cursor-agent --list-models`. Grok leads. Opus does not.
- Prompt on stdin, because Windows limits command-line length
- `--workspace` is an empty temp directory whose `.cursor/cli.json` denies `Shell(*)`, `Write(**)`, `WebFetch(*)`, and `Mcp(*:*)`
- `--sandbox enabled` is omitted on Windows: that flag exits with "Sandbox mode is enabled but not available"
- `--force` / `--yolo` is not used

`--bare` is not used for Claude. It ignores OAuth and then fails with "Not logged in" for a claude.ai subscription.
