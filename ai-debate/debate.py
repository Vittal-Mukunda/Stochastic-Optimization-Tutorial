#!/usr/bin/env python3
"""Debate a math problem between Claude Code and the Cursor CLI.

Each turn is a fresh, stateless CLI call. The full problem and the transcript
so far are sent every time. Both agents are kept from editing files or running
tools.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

MAX_ROUNDS = 5
DEFAULT_ROUNDS = 3
DEFAULT_TIMEOUT = 240

RULES = (
    "You are debating another AI on a math problem. Check its reasoning step "
    "by step, point out concrete errors, and concede if it is right. Include "
    "a small-case or numeric check with every claim. Be concise. End every "
    "turn with a line `FINAL ANSWER: <answer>`."
)

NO_TOOLS = (
    "Do not use tools. Do not read files, edit files, search the web, or run "
    "commands. Reason in text only."
)

ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
FINAL_RE = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?(?:\*\*)?FINAL ANSWER:(?:\*\*)?\s*(.+?)\s*$"
)


class DebateError(Exception):
    def __init__(self, message: str, code: int = 1):
        super().__init__(message)
        self.code = code


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def emit(text: str = "") -> None:
    try:
        print(text, flush=True)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
        safe = text.encode(encoding, errors="replace").decode(encoding, errors="replace")
        print(safe, flush=True)


def strip_ansi(text: str) -> str:
    return ANSI.sub("", text or "").replace("\r\n", "\n").replace("\r", "\n")


def which_claude() -> str:
    for name in ("claude", "claude.exe", "claude.cmd"):
        found = shutil.which(name)
        if found:
            return found
    local = Path.home() / ".local" / "bin" / "claude.exe"
    if local.exists():
        return str(local)
    raise DebateError(
        "Claude Code CLI was not found on PATH. Install it and confirm `claude -p` works.",
        code=2,
    )


def cursor_invocation() -> list[str]:
    """Return the argv prefix for a non-interactive Cursor agent call.

    On Windows the documented entry point is cursor-agent.cmd, which only
    forwards to node.exe. Calling node directly keeps the prompt out of cmd.exe
    quoting. Elsewhere, cursor-agent (or the agent alias) is used as-is.
    """
    base = Path(os.environ.get("LOCALAPPDATA", "")) / "cursor-agent"
    versions = base / "versions"
    if versions.is_dir():
        candidates = []
        for path in versions.iterdir():
            match = re.match(r"(\d{4})\.(\d{1,2})\.(\d{1,2})", path.name)
            node = path / "node.exe"
            index = path / "index.js"
            if match and node.exists() and index.exists():
                key = tuple(int(part) for part in match.groups())
                candidates.append((key, node, index))
        if candidates:
            _, node, index = max(candidates)
            return [str(node), str(index)]

    for name in ("cursor-agent", "cursor-agent.cmd", "agent", "agent.cmd"):
        found = shutil.which(name)
        if found:
            return [found]
    raise DebateError(
        "Cursor CLI was not found. Install it and confirm `cursor-agent -p` works. "
        "On Windows the binary is usually %LOCALAPPDATA%\\cursor-agent\\cursor-agent.cmd.",
        code=2,
    )


def child_env() -> dict[str, str]:
    env = os.environ.copy()
    # These are set inside Cursor itself and can make a nested CLI think it is
    # already an agent session.
    for key in (
        "CURSOR_AGENT",
        "CURSOR_CONVERSATION_ID",
        "CURSOR_LAYOUT",
        "CURSOR_RIPGREP_PATH",
        "CURSOR_WORKSPACE_LABEL",
    ):
        env.pop(key, None)
    env["CURSOR_INVOKED_AS"] = "cursor-agent"
    return env


def prepare_cursor_workspace() -> str:
    """Empty workspace whose permission file refuses shell, writes, web, and MCP."""
    workspace = Path(tempfile.mkdtemp(prefix="ai-debate-"))
    config_dir = workspace / ".cursor"
    config_dir.mkdir()
    config = {
        "permissions": {
            "allow": [],
            "deny": [
                "Shell(*)",
                "Write(**)",
                "WebFetch(*)",
                "Mcp(*:*)",
            ],
        }
    }
    (config_dir / "cli.json").write_text(json.dumps(config), encoding="utf-8")
    return str(workspace)


def run_cli(
    argv: list[str],
    timeout: int,
    cwd: str,
    label: str,
    stdin_text: str | None = None,
) -> str:
    try:
        completed = subprocess.run(
            argv,
            cwd=cwd,
            env=child_env(),
            input=stdin_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        partial = strip_ansi(exc.stdout or "")
        detail = f" Partial output: {partial[:400]}" if partial.strip() else ""
        raise DebateError(
            f"{label} timed out after {timeout}s.{detail}",
            code=3,
        ) from exc
    except FileNotFoundError as exc:
        raise DebateError(f"{label} executable is missing: {exc}", code=2) from exc
    except OSError as exc:
        raise DebateError(f"{label} could not be started: {exc}", code=2) from exc

    stdout = strip_ansi(completed.stdout).strip()
    stderr = strip_ansi(completed.stderr).strip()
    combined = f"{stdout}\n{stderr}".lower()
    if any(
        phrase in combined
        for phrase in (
            "not logged in",
            "authentication required",
            "please run /login",
            "agent login",
            "claude auth login",
        )
    ):
        raise DebateError(
            f"{label} is not authenticated. Run `claude auth login` or `cursor-agent login`, then retry.\n{stderr or stdout}",
            code=2,
        )
    if completed.returncode != 0:
        tail = stderr or stdout or "(no output)"
        raise DebateError(
            f"{label} exited with status {completed.returncode}.\n{tail[:1200]}",
            code=1,
        )
    if not stdout:
        raise DebateError(
            f"{label} returned an empty response.\n{stderr[:800]}",
            code=4,
        )
    return stdout


def claude_turn(prompt: str, timeout: int, cwd: str, label: str) -> str:
    # The prompt is sent on stdin. --tools and --disallowed-tools are variadic,
    # so a prompt placed after them is parsed as extra tool names.
    argv = [
        which_claude(),
        "-p",
        "--tools",
        "",
        "--strict-mcp-config",
        "--no-session-persistence",
        "--permission-mode",
        "dontAsk",
        "--disallowed-tools",
        "Bash,PowerShell,Edit,Write,Read,WebFetch,WebSearch,NotebookEdit,Task",
    ]
    return run_cli(argv, timeout, cwd, label, stdin_text=prompt)


def cursor_turn(prompt: str, timeout: int, workspace: str, label: str) -> str:
    # --mode ask is read-only. --trust skips the workspace prompt.
    # There is no Cursor equivalent of Claude's --tools "".
    # --sandbox enabled is Linux/macOS only; on Windows it exits immediately.
    argv = cursor_invocation() + [
        "-p",
        "--mode",
        "ask",
        "--trust",
        "--output-format",
        "text",
        "--workspace",
        workspace,
    ]
    if sys.platform != "win32":
        argv.extend(["--sandbox", "enabled"])
    argv.append(prompt)
    return run_cli(argv, timeout, workspace, label)


def build_prompt(problem: str, transcript: str, instruction: str) -> str:
    parts = [RULES, NO_TOOLS, "", "PROBLEM:", problem.strip(), ""]
    if transcript.strip():
        parts.extend(["DEBATE SO FAR:", transcript.strip(), ""])
    parts.append(instruction.strip())
    return "\n".join(parts)


def render_turns(turns: list[tuple[str, str]]) -> str:
    chunks = []
    for title, body in turns:
        chunks.append(f"## {title}\n\n{body.strip()}")
    return "\n\n".join(chunks)


def extract_final(text: str) -> str | None:
    matches = FINAL_RE.findall(text)
    if not matches:
        return None
    answer = matches[-1].strip()
    answer = answer.strip("`").strip()
    answer = answer.rstrip(".").strip()
    return answer or None


def normalize_answer(answer: str) -> str:
    text = answer.strip().strip("`").replace("$", "")
    text = text.replace(",", "")
    text = re.sub(r"\s+", " ", text)
    return text.casefold().rstrip(".")


def as_number(answer: str) -> int | None:
    text = normalize_answer(answer).replace("^", "**")
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if not re.fullmatch(r"[0-9+\-*/() ]+", text.replace("**", "")):
        return None
    try:
        value = eval(text, {"__builtins__": {}}, {})  # noqa: S307 - digits and arithmetic only
    except Exception:
        return None
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, int):
        return value
    return None


def answers_match(left: str | None, right: str | None) -> bool:
    if not left or not right:
        return False
    if normalize_answer(left) == normalize_answer(right):
        return True
    left_n, right_n = as_number(left), as_number(right)
    return left_n is not None and left_n == right_n


def parse_counting_problem(problem: str) -> tuple[str, str, int, int] | None:
    """Parse 'positive integers v ≤ N such that <expr> is divisible by M'."""
    bound = re.search(
        r"positive integers\s+([A-Za-z])\s*(?:≤|<=)\s*([0-9][0-9,]*)",
        problem,
        flags=re.IGNORECASE,
    )
    divisible = re.search(
        r"such that\s+(.+?)\s+is divisible by\s+([0-9]+)",
        problem,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not bound or not divisible:
        return None
    var = bound.group(1)
    limit = int(bound.group(2).replace(",", ""))
    expr = divisible.group(1).strip()
    modulus = int(divisible.group(2))
    return var, expr, limit, modulus


def python_expr(expr: str, var: str) -> str:
    translated = (
        expr.replace("²", "**2")
        .replace("³", "**3")
        .replace("⁴", "**4")
        .replace("^", "**")
        .replace("·", "*")
        .replace("×", "*")
    )
    translated = re.sub(r"\s+", "", translated)
    allowed = re.fullmatch(rf"[0-9{re.escape(var)}+\-*/()]+", translated.replace("**", ""))
    if not allowed:
        raise DebateError(f"Cannot safely evaluate expression: {expr}")
    return translated


def brute_force_count(problem: str) -> int | None:
    parsed = parse_counting_problem(problem)
    if parsed is None:
        return None
    var, expr, limit, modulus = parsed
    if limit < 1 or limit > 1_000_000 or modulus == 0:
        raise DebateError(f"Refusing to brute-force an unbounded check (n ≤ {limit}, mod {modulus}).")
    code = python_expr(expr, var)
    count = 0
    for value in range(1, limit + 1):
        result = eval(code, {"__builtins__": {}}, {var: value})  # noqa: S307
        if result % modulus == 0:
            count += 1
    return count


def verify_answer(problem: str, label: str, answer: str | None) -> str:
    if answer is None:
        return f"{label}: no FINAL ANSWER line to check."
    expected = brute_force_count(problem)
    if expected is None:
        numeric = as_number(answer)
        if numeric is None:
            return (
                f"{label}: `{answer}` is not a plain integer or arithmetic expression, "
                "and the problem is not a positive-integer divisibility count this tool can brute-force."
            )
        return (
            f"{label}: parsed `{answer}` as {numeric}. "
            "No independent check applies to this problem shape."
        )
    numeric = as_number(answer)
    if numeric is None:
        return f"{label}: `{answer}` does not parse as a number. Brute-force count is {expected}."
    status = "matches" if numeric == expected else "does not match"
    return f"{label}: {numeric} {status} the brute-force count {expected}."


def write_transcript(path: Path, problem: str, started: str, body: str, summary: str) -> None:
    text = (
        f"# AI debate\n\n"
        f"- Problem: {problem.strip()}\n"
        f"- Started: {started}\n\n"
        f"{body.strip()}\n\n"
        f"## Summary\n\n"
        f"{summary.strip()}\n"
    )
    path.write_text(text, encoding="utf-8")


def ensure_authenticated() -> None:
    """Fail before any model call if either CLI is missing or logged out."""
    claude = which_claude()
    cursor = cursor_invocation()
    claude_auth = run_cli([claude, "auth", "status"], timeout=60, cwd=os.getcwd(), label="claude auth status")
    if '"loggedIn": false' in claude_auth.replace(" ", "") or '"loggedIn":false' in claude_auth.replace(" ", ""):
        raise DebateError("Claude Code is not logged in. Run `claude auth login` and retry.", code=2)
    cursor_auth = run_cli(cursor + ["status"], timeout=60, cwd=os.getcwd(), label="cursor-agent status")
    if "not logged in" in cursor_auth.lower():
        raise DebateError(
            "Cursor CLI is not logged in. Run `cursor-agent login` (or set CURSOR_API_KEY) and retry.",
            code=2,
        )


def debate(problem: str, rounds: int, timeout: int, verify: bool) -> int:
    ensure_authenticated()
    workspace = prepare_cursor_workspace()
    started = datetime.now().isoformat(timespec="seconds")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = Path.cwd() / f"debate_{stamp}.md"
    turns: list[tuple[str, str]] = []
    claude_answer: str | None = None
    cursor_answer: str | None = None
    rounds_used = 0
    agreed = False
    stopped = "completed the scheduled rounds"

    def flush(summary: str) -> None:
        body = render_turns(turns) if turns else "_No turns completed._"
        write_transcript(out_path, problem, started, body, summary)

    try:
        emit("Claude (opening)...")
        opening = claude_turn(
            build_prompt(problem, "", "Give your opening solution."),
            timeout,
            workspace,
            "Claude (opening)",
        )
        turns.append(("Claude (opening)", opening))
        claude_answer = extract_final(opening)
        flush("In progress.")
        emit(opening)
        emit()

        for round_index in range(1, rounds + 1):
            rounds_used = round_index
            emit(f"Cursor (round {round_index})...")
            critique = cursor_turn(
                build_prompt(
                    problem,
                    render_turns(turns),
                    "Critique the other agent's latest argument and give your own answer.",
                ),
                timeout,
                workspace,
                f"Cursor (round {round_index})",
            )
            turns.append((f"Cursor (round {round_index})", critique))
            cursor_answer = extract_final(critique)
            flush("In progress.")
            emit(critique)
            emit()
            if answers_match(claude_answer, cursor_answer):
                agreed = True
                stopped = f"stopped after Cursor (round {round_index}) because the latest FINAL ANSWER lines match"
                break

            emit(f"Claude (round {round_index})...")
            reply = claude_turn(
                build_prompt(
                    problem,
                    render_turns(turns),
                    "Respond by defending your latest answer or conceding. "
                    "If the critique is right, correct your answer.",
                ),
                timeout,
                workspace,
                f"Claude (round {round_index})",
            )
            turns.append((f"Claude (round {round_index})", reply))
            claude_answer = extract_final(reply)
            flush("In progress.")
            emit(reply)
            emit()
            if answers_match(claude_answer, cursor_answer):
                agreed = True
                stopped = f"stopped after Claude (round {round_index}) because the latest FINAL ANSWER lines match"
                break
    except DebateError as exc:
        summary = (
            f"- Status: failed\n"
            f"- Error: {exc}\n"
            f"- Claude final: {claude_answer or '(none)'}\n"
            f"- Cursor final: {cursor_answer or '(none)'}\n"
            f"- Rounds used: {rounds_used}\n"
            f"- Transcript: {out_path}\n"
        )
        flush(summary)
        emit(summary)
        emit(f"Partial transcript: {out_path}")
        return exc.code

    lines = [
        f"- Claude final: {claude_answer or '(no FINAL ANSWER line)'}",
        f"- Cursor final: {cursor_answer or '(no FINAL ANSWER line)'}",
        f"- Agree: {'yes' if agreed else 'no'}",
        f"- Rounds used: {rounds_used}",
        f"- Stop: {stopped}",
    ]
    if verify:
        lines.append("- Verification:")
        try:
            lines.append(f"  - {verify_answer(problem, 'Claude', claude_answer)}")
            lines.append(f"  - {verify_answer(problem, 'Cursor', cursor_answer)}")
        except DebateError as exc:
            lines.append(f"  - Verification failed: {exc}")
    summary = "\n".join(lines)
    flush(summary)
    emit("Summary")
    emit(summary)
    emit(f"Transcript: {out_path}")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Debate a math problem between Claude Code and Cursor CLI."
    )
    parser.add_argument("problem", help="Math problem text")
    parser.add_argument(
        "rounds",
        nargs="?",
        type=int,
        default=DEFAULT_ROUNDS,
        help=f"Critique rounds after Claude's opening (default {DEFAULT_ROUNDS}, max {MAX_ROUNDS})",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Brute-force a positive-integer divisibility count, or evaluate a plain arithmetic FINAL ANSWER",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Seconds allowed for each CLI call (default {DEFAULT_TIMEOUT})",
    )
    args = parser.parse_args(argv)
    if args.rounds < 1 or args.rounds > MAX_ROUNDS:
        parser.error(f"rounds must be from 1 to {MAX_ROUNDS}")
    if args.timeout < 1:
        parser.error("timeout must be positive")
    return args


def main(argv: list[str] | None = None) -> int:
    configure_stdio()
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        return debate(args.problem, args.rounds, args.timeout, args.verify)
    except DebateError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return exc.code


if __name__ == "__main__":
    sys.exit(main())
