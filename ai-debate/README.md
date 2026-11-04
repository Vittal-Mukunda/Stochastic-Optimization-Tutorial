# AI debate

Claude Code and the Cursor CLI take turns on a math problem. Each call is stateless: the script sends the problem and the full transcript every time. Neither agent is allowed to edit files or run tools.

Python is the entry point. On this machine `bash` is WSL, and a `.sh` wrapper would not see the Windows `claude` and `cursor-agent` binaries reliably.

## Usage

```powershell
python debate.py "problem text" [rounds]
python debate.py --verify "problem text" 3
```

`rounds` is the number of critique rounds after Claude's opening solution. The default is 3. The maximum is 5.

```powershell
python debate.py "Find the number of positive integers n ≤ 1000 such that n^2 + n + 1 is divisible by 7."
python debate.py --verify "Find the number of positive integers n ≤ 1000 such that n^2 + n + 1 is divisible by 7." 3
```

The transcript is written to `debate_<timestamp>.md` in the current directory. After the loop the script prints each agent's latest `FINAL ANSWER`, whether those answers agree, and how many rounds ran.

The loop stops early when both agents' latest `FINAL ANSWER` lines match (numerically, if both are plain integers or arithmetic).

## What the agents are told

Both CLIs get this instruction, plus the problem and the transcript:

> You are debating another AI on a math problem. Check its reasoning step by step, point out concrete errors, and concede if it is right. Include a small-case or numeric check with every claim. Be concise. End every turn with a line `FINAL ANSWER: <answer>`.

Turn order:

1. Claude gives an opening solution.
2. Each round, Cursor critiques Claude's latest argument and gives its own answer.
3. Claude defends or concedes.

## Flags that keep them from touching the repo

Checked against `claude --help` and `cursor-agent --help`.

Claude:

- `-p` prints the answer and exits
- `--tools ""` disables every built-in tool
- `--disallowed-tools Bash,PowerShell,Edit,Write,Read,WebFetch,WebSearch,NotebookEdit,Task` is a second lock
- The prompt is piped on stdin. Both `--tools` and `--disallowed-tools` are variadic, so a prompt placed after them is treated as a list of tool names
- `--strict-mcp-config` with no MCP config loads no MCP servers
- `--no-session-persistence` so the call cannot be resumed
- `--permission-mode dontAsk` so a stray tool call is not approved
- `--bare` is intentionally not used. It ignores OAuth and then fails with "Not logged in" for a `claude.ai` subscription

Cursor has no `--tools` flag. The closest official settings are:

- `-p` and `--output-format text`
- `--mode ask` (read-only Q&A, no edits)
- `--sandbox enabled` on macOS and Linux. On Windows that flag exits with "Sandbox mode is enabled but not available", so it is omitted here
- `--trust` so headless mode does not wait on the workspace prompt
- `--workspace` pointed at an empty temp directory, with `.cursor/cli.json` denying `Shell(*)`, `Write(**)`, `WebFetch(*)`, and `Mcp(*:*)`

Do not pass `--force` / `--yolo`. That flag allows commands.

## `--verify`

When the problem asks for the number of positive integers `n ≤ N` such that an expression in `n` is divisible by `M`, the script brute-forces `n = 1..N` and reports whether each final answer matches. `N` above 1,000,000 is rejected.

If the problem is not that shape, `--verify` only evaluates a `FINAL ANSWER` that is a plain integer or an arithmetic expression such as `17*19`.

## Errors

| Situation | What you see |
| --- | --- |
| `claude` or `cursor-agent` missing | Exit 2, before any turn |
| CLI not logged in | Exit 2. Run `claude auth login` or `cursor-agent login` |
| Timeout (default 240s per turn) | Exit 3. Partial transcript is still saved |
| Empty response or non-zero exit | Exit 4 or 1. Partial transcript is still saved |

Change the per-turn limit with `--timeout 300`.

## Requirements

- Python 3.9+
- `claude -p` authenticated
- `cursor-agent -p` authenticated (`agent` is the same CLI; this script prefers `cursor-agent`)
