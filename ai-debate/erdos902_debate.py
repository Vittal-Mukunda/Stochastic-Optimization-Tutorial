#!/usr/bin/env python3
"""Stateless debate on Erdős problem #902 between Claude Code and Cursor CLI.

Both agents reason in text only. File edits and tool use are turned off with
each CLI's own flags. Every turn receives the problem, the established-results
list, and the full transcript.
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
DEFAULT_TIMEOUT = 480

# Confirmed from `claude --help` (not guessed): --effort accepts
# low, medium, high, xhigh, max. The requested level is high.
CLAUDE_MODEL = "claude-opus-5-5"
CLAUDE_EFFORT = "high"

# Confirmed from `cursor-agent --list-models`. Fable 5.1 thinking at max is
# the strongest listed model that also exposes an explicit top reasoning tier.
CURSOR_MODEL = "grok-4.7-xhigh"

PROBLEM = """
Erdős problem #902 (Schütte's tournament problem).

A tournament has property S_k if every set of k vertices is dominated by some
other vertex: a vertex outside the set that beats all k of them. Let f(k) be
the minimum number of vertices of a tournament with property S_k.

The open question is to determine f(4), by improving the lower bound, improving
the upper bound with an explicit construction, or giving a rigorous proof that
a specific structure cannot be an S_4 tournament.

Push on genuinely new progress. Do not re-derive results listed as already
established. If something in that list conflicts with what you remember from
the literature, flag the conflict explicitly. Do not silently replace the list.
""".strip()

ESTABLISHED = """
Treat the following as given. Do not re-derive them. Status labels are the
owner's, from FILE_INDEX.md in this project, except the literature block,
which was copied from public sources so you can see where a conflict might be.

Literature (public sources; not the owner's new claims):
- f(1) = 3 and f(2) = 7. RECALLED FROM LITERATURE: Erdős, Math. Gaz. 47 (1963), 220–223. High confidence.
- f(3) = 19. RECALLED FROM LITERATURE: Szekeres–Szekeres, Math. Gaz. 49 (1965), 290–293, attested by Graham–Spencer (1971) and proved again by Reid–McRae–Hedetniemi–Hedetniemi, Australas. J. Combin. 29 (2004), Theorem 5. High confidence.
- f(k) ≥ 2^{k+1} − 1. RECALLED FROM LITERATURE: Erdős 1963. Attained at k = 1, 2. High confidence.
- f(k) ≥ (k+2) 2^{k−1} − 1, hence f(4) ≥ 47. RECALLED FROM LITERATURE: Szekeres–Szekeres, as quoted by Graham–Spencer (1971). The 1965 paper's exact range of k is not in hand; the formula is consistent with f(1) and f(2). High confidence in the inequality for k = 3 and k = 4.
- f(4) ≥ 48. RECALLED FROM LITERATURE: Reid et al. 2004, Corollary 7, using nonexistence of a nontrivial triply regular tournament. High confidence.
- f(4) ≤ 67, via the Paley (quadratic-residue) tournament on 67 vertices. RECALLED FROM LITERATURE: Graham–Spencer 1971. High confidence. This is the best published upper bound recorded on erdosproblems.com as of the 2026 survey used here.
- Erdős's probabilistic upper bound f(k) ≤ 2^k k^2 log(2+ε) for large k. RECALLED FROM LITERATURE: Erdős 1963. High confidence.
- Graham–Spencer: the Paley tournament of a prime p ≡ 3 (mod 4) has S_k when p > k^2 2^{2k−2}. RECALLED FROM LITERATURE. High confidence.
- Smallest Paley tournaments with S_4, S_5, S_6 are on 67, 331, 1163 vertices (OEIS A362137). These are upper bounds on f, not values of f. RECALLED FROM LITERATURE. Medium-high confidence.
- A public survey (erdosproblems.ai, updated Oct 2026) still states 48 ≤ f(4) ≤ 67 and does not record the owner's later lower bounds. That is a conflict with the owner list below. Flag it if you rely on the survey; do not silently drop the owner's claims.

Owner's results (FILE_INDEX.md). These are given, not an invitation to re-prove them:
- f(4) ≥ 51 by a hand argument. Status: new record claimed by the owner; the owner checked it; an independent check is still pending. Do not re-derive this proof. You may try to push the lower bound to 52 or higher, or you may flag a specific gap if you find one.
- f(4) ≥ 49 is attributed by the owner to Wilder (2026), and f(4) ≥ 48 to Reid et al. (2004). Status: known, not the owner's.
- f(n) ≥ (0.7695… − o(1)) · n · 2^n. Status: owner's; adversarially verified inside the project.
- f(5) ≥ 121, f(6) ≥ 281, f(7) ≥ 665, and f(n) ≥ (n + 2.5) · 2^{n−1} − 1 for n ≥ 5. Status: owner's; verified twice inside the project.
- No S_4 tournament on N ≤ 64 vertices has a vertex of in-degree 23. Status: computer-assisted; re-checked.
- The case N = 51 reduces to a doubly regular tournament on 51 vertices plus one local claim. Status: exact certificates for the reduction; the local claim is still pending.
- There are 37 doubly regular tournaments on 23 vertices, and exactly 2 of them have S_3. Status: SAT classification in the project.
- (M1) is tight for every n. Barrier theorems rule out the counting method in the forms labelled B1–B5, and they rule out random symmetric constructions of the kind already analysed. Status: owner's; verified inside the project.
- A 70-vertex example exists in which some triple has only 5 dominators. Status: checked. This is not an S_4 tournament.

Already tried and ruled out. Do not repeat these as if they were new:
- Exhaustive search of group-invariant tournaments, and of 138 symmetric families, on 48–66 vertices: no S_4 example (round-1 upper-bound search, all negative).
- Scripts that used the wrong covering direction (the superseded local48.c family) are not valid arguments.
- The attempted classification of 24-vertex in-neighbourhoods stalled and is incomplete. It is not a theorem.
- Paley tournaments QR_7, QR_19, and QR_67 were checked directly. Cyclotomic searches for an S_5 tournament below 331 vertices were already run.
- Local search and tabu search from those seeds did not produce an S_4 tournament below 67.

A useful new result is a lower bound f(4) ≥ 52 or better, an explicit S_4 tournament on fewer than 67 vertices that is not one of the ruled-out families, or a proof that a named construction family still in play cannot work. Sanity-check every general claim on f(1), f(2), and f(3).
""".strip()

RULES = """
Two coauthors are trying to prove a result on f(4). They do equal work and they are allowed to disagree. One proposes a proof. The other says whether it is correct, wrong, or missing a step, and supplies the missing mathematics. Concede only when the argument is actually correct. No flattery. Write the mathematics in the reply. Do not mention a workspace, files, or tools.

Label every claim as exactly one of:
- PROVED (full argument given in this turn)
- COMPUTED (give the exact object and the exact check; you cannot run code in this turn, so a COMPUTED label is only allowed for a finite check you have fully expanded by hand, and you must still emit a CONSTRUCTION block so an external checker can rerun it)
- CONJECTURE
- RECALLED FROM LITERATURE (name the source, and say how confident you are)

Never present a recalled literature value as proved. If you are unsure of a bound or a citation, say so.

If you propose a tournament, end the construction with a block in exactly this form, and no other keys:

CONSTRUCTION:
type: paley
order: <prime>
k: 4

or

CONSTRUCTION:
type: circulant
order: <n>
k: 4
steps: <comma-separated out-neighbours of 0, all in 1..n-1, closed under neither x nor n-x>

Paley means the quadratic-residue tournament: i → j iff i − j is a nonzero square mod order, and order must be a prime ≡ 3 (mod 4).
Circulant means vertex set Z/nZ and 0 beats exactly the listed steps. The converse orientation of each step must not also be listed.

Small-case sanity checks against f(1), f(2), and f(3) are mandatory for every general claim.

Be concise. Do not re-derive the established section.

End every turn with these three lines, exactly:
STATUS: <one-line statement of your current best claim>
CONFIDENCE: <integer>%
CLAIM_TAG: <PROVED or COMPUTED or CONJECTURE or RECALLED>
""".strip()

NO_TOOLS = (
    "Do not use tools. Do not read files, edit files, search the web, or run "
    "commands. Reason in text only. Do not call any function or skill."
)

ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
STATUS_RE = re.compile(r"(?im)^\s*STATUS:\s*(.+?)\s*$")
CONF_RE = re.compile(r"(?im)^\s*CONFIDENCE:\s*(\d{1,3})\s*%?")
TAG_RE = re.compile(
    r"(?im)^\s*CLAIM_TAG:\s*(PROVED|COMPUTED|CONJECTURE|RECALLED)\b"
)
CONSTRUCTION_RE = re.compile(
    r"(?im)^CONSTRUCTION:\s*\n((?:[ \t]*[a-z]+:[^\n]*\n?){1,8})"
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
    raise DebateError("Claude Code CLI was not found on PATH.", code=2)


def cursor_invocation() -> list[str]:
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
    raise DebateError("Cursor CLI was not found.", code=2)


def child_env() -> dict[str, str]:
    env = os.environ.copy()
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
    workspace = Path(tempfile.mkdtemp(prefix="erdos902-debate-"))
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


def claude_argv() -> list[str]:
    # Prompt is sent on stdin. --tools and --disallowed-tools are variadic,
    # so a prompt placed after them is parsed as extra tool names.
    return [
        which_claude(),
        "-p",
        "--model",
        CLAUDE_MODEL,
        "--effort",
        CLAUDE_EFFORT,
        "--tools",
        "",
        "--disable-slash-commands",
        "--strict-mcp-config",
        "--no-session-persistence",
        "--permission-mode",
        "dontAsk",
        "--restricted",
        "--disallowed-tools",
        "Bash,PowerShell,Edit,Write,Read,WebFetch,WebSearch,NotebookEdit,Task",
    ]


def cursor_argv(workspace: str) -> list[str]:
    # --mode ask is read-only. --trust skips the workspace prompt.
    # There is no --tools flag. --sandbox enabled is unavailable on Windows.
    # stream-json is required because Fable at max effort can think for longer
    # than the text formatter's silence, and Windows caps argv, so the prompt
    # is passed on stdin.
    argv = cursor_invocation() + [
        "-p",
        "--mode",
        "ask",
        "--trust",
        "--output-format",
        "stream-json",
        "--stream-partial-output",
        "--model",
        CURSOR_MODEL,
        "--workspace",
        workspace,
    ]
    if sys.platform != "win32":
        argv.extend(["--sandbox", "enabled"])
    return argv


def _auth_failure(text: str) -> bool:
    lowered = text.lower()
    return any(
        phrase in lowered
        for phrase in (
            "not logged in",
            "authentication required",
            "please run /login",
            "agent login",
            "claude auth login",
        )
    )


def run_cli(
    argv: list[str],
    timeout: int,
    cwd: str,
    label: str,
    stdin_text: str,
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
        raise DebateError(f"{label} timed out after {timeout}s.{detail}", code=3) from exc
    except FileNotFoundError as exc:
        raise DebateError(f"{label} executable is missing: {exc}", code=2) from exc
    except OSError as exc:
        raise DebateError(f"{label} could not be started: {exc}", code=2) from exc

    stdout = strip_ansi(completed.stdout).strip()
    stderr = strip_ansi(completed.stderr).strip()
    if _auth_failure(f"{stdout}\n{stderr}"):
        raise DebateError(f"{label} is not authenticated.\n{stderr or stdout}", code=2)
    if completed.returncode != 0:
        tail = stderr or stdout or "(no output)"
        raise DebateError(
            f"{label} exited with status {completed.returncode}.\n{tail[:1500]}",
            code=1,
        )
    if not stdout:
        raise DebateError(f"{label} returned an empty response.\n{stderr[:800]}", code=4)
    return stdout


def run_cursor(argv: list[str], timeout: int, cwd: str, label: str, stdin_text: str) -> str:
    """Read Cursor's stream-json events and return the final result text."""
    try:
        proc = subprocess.Popen(
            argv,
            cwd=cwd,
            env=child_env(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as exc:
        raise DebateError(f"{label} executable is missing: {exc}", code=2) from exc
    except OSError as exc:
        raise DebateError(f"{label} could not be started: {exc}", code=2) from exc

    assert proc.stdin is not None and proc.stdout is not None and proc.stderr is not None
    proc.stdin.write(stdin_text)
    proc.stdin.close()
    result = ""
    failed = False
    assistant: list[str] = []
    thinking_parts: list[str] = []
    stderr_parts: list[str] = []
    started = datetime.now()
    last_note = started
    timed_out = False

    def read_stderr() -> None:
        for line in proc.stderr:
            stderr_parts.append(line)

    import threading

    def kill_if_late() -> None:
        nonlocal timed_out
        if proc.poll() is None:
            timed_out = True
            proc.kill()

    timer = threading.Timer(timeout, kill_if_late)
    timer.daemon = True
    timer.start()
    stderr_thread = threading.Thread(target=read_stderr, daemon=True)
    stderr_thread.start()

    try:
        for raw in proc.stdout:
            if timed_out:
                break
            line = strip_ansi(raw).strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            kind = event.get("type")
            if kind == "thinking" and event.get("subtype") == "delta":
                piece = str(event.get("text") or "")
                if piece:
                    thinking_parts.append(piece)
                now = datetime.now()
                if (now - last_note).total_seconds() >= 30:
                    emit(
                        f"{label} still thinking ({int((now - started).total_seconds())}s, "
                        f"{sum(len(p) for p in thinking_parts)} chars)..."
                    )
                    last_note = now
            elif kind == "assistant":
                content = event.get("message", {}).get("content", [])
                if isinstance(content, list):
                    piece = "".join(
                        part.get("text", "")
                        for part in content
                        if isinstance(part, dict) and part.get("type") == "text"
                    )
                    if piece:
                        assistant.append(piece)
            elif kind == "result":
                failed = bool(event.get("is_error"))
                result = str(event.get("result") or "")
            elif kind == "system" and event.get("subtype") == "init":
                emit(f"{label} model: {event.get('model', '(unreported)')}")
        if proc.poll() is None:
            proc.wait(timeout=30)
    except DebateError:
        raise
    except Exception as exc:  # noqa: BLE001
        if not timed_out:
            proc.kill()
            raise DebateError(f"{label} failed while reading output: {exc}", code=1) from exc
    finally:
        timer.cancel()
        if proc.poll() is None:
            proc.kill()

    stderr_thread.join(timeout=2)
    stderr = strip_ansi("".join(stderr_parts)).strip()
    code = proc.returncode if proc.returncode is not None else 1
    text = result.strip() or (max(assistant, key=len) if assistant else "")
    text = text.strip()
    if timed_out and not text:
        reasoning = "".join(thinking_parts).strip()
        if len(reasoning) > 24000:
            reasoning = reasoning[-24000:]
        if reasoning:
            emit(f"{label} hit the time limit. Keeping {len(reasoning)} characters of reasoning.")
            text = (
                "[Time limit hit before Grok closed the turn. This is the reasoning captured so far.]\n\n"
                + reasoning
            )
    if _auth_failure(f"{text}\n{stderr}"):
        raise DebateError(f"{label} is not authenticated.\n{stderr or text}", code=2)
    if failed:
        raise DebateError(f"{label} reported an error.\n{text[:1500] or stderr[:1500]}", code=1)
    if code != 0 and not text:
        raise DebateError(f"{label} exited with status {code}.\n{(stderr or '(no output)')[:1500]}", code=1)
    if not text:
        raise DebateError(f"{label} returned an empty response.\n{stderr[:800]}", code=4)
    return text


def _bad_public(text: str) -> bool:
    low = text.lower()
    if text.startswith("[Time limit hit"):
        return True
    if "status:" not in low:
        return True
    if "workspace" in low or "i will check" in low or "i will " in low:
        return True
    return len(text) < 500


def _strip_narration(notes: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", notes.replace("\n", " "))
    kept: list[str] = []
    for sentence in sentences:
        low = sentence.lower()
        if any(
            phrase in low
            for phrase in (
                "i am",
                "i will",
                "i'll",
                "i now",
                "i have",
                "the author",
                "workspace",
                "i realized",
                "i noted",
                "i found",
                "i derived",
                "i corrected",
                "i concluded",
            )
        ):
            continue
        if len(sentence.strip()) < 40:
            continue
        kept.append(sentence.strip())
    return " ".join(kept[-6:])


def condense_draft(notes: str, timeout: int, workspace: str, label: str) -> str:
    """Turn an unfinished Grok draft into a reply Opus is allowed to read.

    The draft goes back to Grok only. Opus never sees the raw narration.
    """
    clipped = notes.strip()
    if len(clipped) > 2500:
        clipped = clipped[-2500:]
    instruction = (
        "Write one finished argument, under 450 words. The first sentence is the claim. "
        "Do not mention a workspace, files, or tools. Do not say that you will check anything. "
        "Label the claim PROVED, COMPUTED, CONJECTURE, or RECALLED FROM LITERATURE. "
        "Include a sanity check on the Paley tournament of order 7 or 19. "
        "End with STATUS, CONFIDENCE, and CLAIM_TAG.\n\n"
        f"NOTES:\n{clipped}"
    )
    text = run_cursor(
        cursor_argv(workspace),
        min(timeout, 180),
        workspace,
        f"{label} rewrite",
        instruction,
    )
    if not _bad_public(text):
        return text
    emit(f"{label} rewrite was not a finished argument. Asking once more.")
    text = run_cursor(
        cursor_argv(workspace),
        min(timeout, 150),
        workspace,
        f"{label} rewrite retry",
        "The previous reply was not a proof. First sentence: the theorem. "
        "Then the argument, under 400 words. Forbidden words: workspace, files, tools, I will. "
        "End with STATUS, CONFIDENCE, and CLAIM_TAG.\n\n"
        f"NOTES:\n{_strip_narration(clipped) or clipped[-1200:]}",
    )
    if not _bad_public(text):
        return text
    cleaned = _strip_narration(notes)
    if not cleaned:
        raise DebateError(f"{label} produced no public argument.", code=4)
    return (
        "Grok did not close a public proof. The sentences below are what remained after narration was removed. "
        "They are not a finished argument.\n\n"
        f"{cleaned}\n\n"
        "STATUS: unfinished; no closed claim\n"
        "CONFIDENCE: 20%\n"
        "CLAIM_TAG: CONJECTURE"
    )


def build_prompt(transcript: str, instruction: str, extra: str) -> str:
    parts = [
        "Write the finished mathematics in this reply. One claim. Under 500 words. "
        "Do not mention a workspace, files, or tools.",
        "",
        RULES,
        NO_TOOLS,
        "",
        "PROBLEM:",
        PROBLEM,
        "",
        "ALREADY ESTABLISHED:",
        ESTABLISHED,
        "",
    ]
    if extra.strip():
        parts.extend(["ADDITIONAL STARTING DIRECTION:", extra.strip(), ""])
    if transcript.strip():
        parts.extend(["DEBATE SO FAR:", transcript.strip(), ""])
    parts.append(instruction.strip())
    return "\n".join(parts)


def render_turns(turns: list[tuple[str, str]]) -> str:
    return "\n\n".join(f"## {title}\n\n{body.strip()}" for title, body in turns)


def last_match(pattern: re.Pattern[str], text: str) -> str | None:
    found = pattern.findall(text)
    if not found:
        return None
    return found[-1].strip()


def normalize_status(text: str | None) -> str:
    if not text:
        return ""
    collapsed = re.sub(r"\s+", " ", text.strip().strip("`"))
    return collapsed.casefold().rstrip(".")


def agrees(left: str, right: str) -> bool:
    left_status, left_tag = last_match(STATUS_RE, left), last_match(TAG_RE, left)
    right_status, right_tag = last_match(STATUS_RE, right), last_match(TAG_RE, right)
    if left_tag not in {"PROVED", "COMPUTED"} or right_tag not in {"PROVED", "COMPUTED"}:
        return False
    return bool(left_status) and normalize_status(left_status) == normalize_status(right_status)


def parse_construction(block: str) -> dict[str, str] | None:
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip().lower()] = value.strip()
    if fields.get("type") not in {"paley", "circulant"}:
        return None
    if "order" not in fields or "k" not in fields:
        return None
    return fields


def legendre_is_residue(a: int, p: int) -> bool:
    return pow(a % p, (p - 1) // 2, p) == 1


def build_tournament(spec: dict[str, str]) -> tuple[int, int, list[int]]:
    order = int(spec["order"])
    k = int(spec["k"])
    if order < 1 or order > 80:
        raise DebateError(f"Refusing to check a tournament of order {order}.")
    if k < 1 or k >= order:
        raise DebateError(f"Refusing to check S_{k} on {order} vertices.")
    outs = [0] * order
    kind = spec["type"]
    if kind == "paley":
        if order % 4 != 3 or not all(order % d for d in range(2, int(order**0.5) + 1)):
            raise DebateError(f"Paley order {order} is not a prime congruent to 3 mod 4.")
        for i in range(order):
            mask = 0
            for j in range(order):
                if i != j and legendre_is_residue(i - j, order):
                    mask |= 1 << j
            outs[i] = mask
    else:
        steps = [int(part) for part in spec.get("steps", "").split(",") if part.strip()]
        step_set = set(steps)
        for step in steps:
            if step <= 0 or step >= order or (order - step) in step_set:
                raise DebateError(f"Circulant steps are not a valid orientation: {steps}")
        for i in range(order):
            mask = 0
            for step in steps:
                mask |= 1 << ((i + step) % order)
            outs[i] = mask
    return order, k, outs


def has_property_s(outs: list[int], k: int) -> tuple[bool, str]:
    import itertools

    n = len(outs)
    full = (1 << n) - 1
    for combo in itertools.combinations(range(n), k):
        mask = 0
        for vertex in combo:
            mask |= 1 << vertex
        dominated = False
        for vertex in range(n):
            if (mask >> vertex) & 1:
                continue
            if (outs[vertex] & mask) == mask:
                dominated = True
                break
        if not dominated:
            return False, f"FAIL S_{k} on {n} vertices; undominated set {list(combo)}"
    del full
    return True, f"PASS S_{k} on {n} vertices"


def verify_text(text: str) -> list[str]:
    reports = []
    seen: set[tuple[str, str, str, str]] = set()
    for match in CONSTRUCTION_RE.finditer(text):
        spec = parse_construction(match.group(1))
        if spec is None:
            reports.append(f"Skipped an unparseable CONSTRUCTION block:\n{match.group(0)[:400]}")
            continue
        key = (spec.get("type", ""), spec.get("order", ""), spec.get("k", ""), spec.get("steps", ""))
        if key in seen:
            continue
        seen.add(key)
        try:
            order, k, outs = build_tournament(spec)
            ok, detail = has_property_s(outs, k)
        except DebateError as exc:
            reports.append(f"CHECK {spec.get('type')} order {spec.get('order')}: error: {exc}")
            continue
        except Exception as exc:  # noqa: BLE001 - report checker failures in the transcript
            reports.append(f"CHECK {spec}: error: {exc}")
            continue
        reports.append(f"CHECK {spec['type']} order {order} k {k}: {detail} ({'pass' if ok else 'fail'})")
    if not reports:
        reports.append("No parseable CONSTRUCTION block was proposed, so no tournament was checked.")
    return reports


def write_transcript(path: Path, started: str, body: str, summary: str, flags: str) -> None:
    text = (
        f"# Erdős #902 debate\n\n"
        f"- Started: {started}\n"
        f"- Flags:\n\n{flags}\n\n"
        f"{body.strip()}\n\n"
        f"## Summary\n\n"
        f"{summary.strip()}\n"
    )
    path.write_text(text, encoding="utf-8")


def flag_record() -> str:
    return "\n".join(
        [
            f"- Claude: `claude -p --model {CLAUDE_MODEL} --effort {CLAUDE_EFFORT}` "
            "with `--tools \"\"`, `--restricted`, `--permission-mode dontAsk`, "
            "`--disallowed-tools Bash,PowerShell,Edit,Write,Read,WebFetch,WebSearch,NotebookEdit,Task`, "
            "`--disable-slash-commands`, `--strict-mcp-config`, `--no-session-persistence`. "
            "Prompt on stdin.",
            f"- Cursor: `cursor-agent -p --mode ask --trust --output-format stream-json --stream-partial-output --model {CURSOR_MODEL}` "
            "with `--workspace` set to an empty directory whose `.cursor/cli.json` denies "
            "`Shell(*)`, `Write(**)`, `WebFetch(*)`, and `Mcp(*:*)`. "
            "Prompt on stdin. `--sandbox enabled` is omitted on Windows because that flag exits there. "
            "`--force` is not used.",
            "- Effort source: `claude --help` lists `--effort <level>` with choices low, medium, high, xhigh, max. "
            "No separate docs page in the installed package contradicted this. High was requested, so `--effort high` is set.",
            "- Cursor model source: `cursor-agent --list-models`. "
            f"`{CURSOR_MODEL}` is Grok 4.7 Extra High, the model requested for the lead side.",
        ]
    )


def load_turns(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    # Turn headers are "## Claude (round N)" or "## Cursor (round N)".
    # The bodies themselves contain markdown headings, so a bare "^## " split is wrong.
    chunks = re.split(r"(?m)^## (?=(?:Claude|Cursor|Grok) \(round \d+\)|Summary\b)", text)
    turns: list[tuple[str, str]] = []
    for chunk in chunks[1:]:
        title, _, body = chunk.partition("\n")
        title = title.strip()
        if title.lower().startswith("summary"):
            break
        body = body.strip()
        if title and body:
            turns.append((title, body))
    if not turns:
        raise DebateError(f"No turns found in {path}")
    return turns


def planned_turns(rounds: int) -> list[tuple[str, str, int]]:
    """Grok leads every round. Opus only corrects or adds what Grok missed."""
    plan: list[tuple[str, str, int]] = []
    for round_index in range(1, rounds + 1):
        plan.append((f"Grok (round {round_index})", "cursor", round_index))
        plan.append((f"Claude (round {round_index})", "claude", round_index))
    return plan


def debate(rounds: int, timeout: int, extra: str, out_dir: Path, resume: Path | None) -> int:
    workspace = prepare_cursor_workspace()
    started = datetime.now().isoformat(timespec="seconds")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"erdos902_debate_{stamp}.md"
    turns: list[tuple[str, str]] = load_turns(resume) if resume else []
    plan = planned_turns(rounds)
    if len(turns) > len(plan):
        raise DebateError(f"Resume file has more turns than {rounds} rounds allow.")
    for index, (title, _body) in enumerate(turns):
        if title != plan[index][0]:
            raise DebateError(f"Resume mismatch at turn {index + 1}: {title!r} != {plan[index][0]!r}")
    rounds_used = 0
    agreed = False
    stopped = "completed the scheduled rounds"
    flags = flag_record()

    def flush(summary: str) -> None:
        body = render_turns(turns) if turns else "_No turns completed._"
        write_transcript(out_path, started, body, summary, flags)

    grok_open = (
        "You are Grok, coauthor A. Propose the answer. "
        "Write one precise claim about f(4) and its proof, or an explicit construction, in this reply. "
        "Under 500 words. The first sentence is the claim. "
        "Your coauthor will try to break the proof. Do not write a plan."
    )
    grok_continue = (
        "You are Grok, coauthor A. Answer the critique as an equal coauthor. "
        "If Claude showed a step is wrong, repair the proof or replace the claim. "
        "If Claude found something missing, supply that step. "
        "Under 500 words. The first sentence is the claim you now stand behind."
    )
    claude_review = (
        "You are Opus, coauthor B. You do equal work. "
        "Judge Grok's latest proof: correct, wrong, or missing a step. "
        "Name the exact step. If it is wrong, give the counterexample or the corrected argument. "
        "If a step is missing, write that step. "
        "Under 500 words. Do not write a plan, and do not start from scratch if the proof can be repaired."
    )
    for title, _body in turns:
        match = re.fullmatch(r"Grok \(round (\d+)\)", title)
        if match:
            rounds_used = int(match.group(1))
    try:
        for title, kind, number in plan[len(turns) :]:
            if kind == "cursor":
                rounds_used = number
                instruction = grok_open if number == 1 else grok_continue
                runner = run_cursor
                argv = cursor_argv(workspace)
            else:
                instruction = claude_review
                runner = run_cli
                argv = claude_argv()
            emit(f"{title}...")
            call_timeout = 150 if kind == "cursor" else timeout
            text = runner(
                argv,
                call_timeout,
                workspace,
                title,
                build_prompt("" if not turns else render_turns(turns), instruction, extra),
            )
            if kind == "cursor" and text.startswith("[Time limit hit"):
                emit(f"{title} is rewriting the draft into a finished argument...")
                notes = text.split("\n\n", 1)[-1]
                text = condense_draft(notes, timeout, workspace, title)
            turns.append((title, text))
            flush("In progress.")
            emit(text)
            emit()
            if len(turns) >= 2 and agrees(turns[-2][1], turns[-1][1]):
                agreed = True
                stopped = (
                    f"stopped after {title} because both STATUS lines match "
                    "and both CLAIM_TAG values are PROVED or COMPUTED"
                )
                break
    except DebateError as exc:
        summary = (
            f"- Status: failed\n"
            f"- Error: {exc}\n"
            f"- Rounds used: {rounds_used}\n"
            f"- Transcript: {out_path}\n"
        )
        flush(summary)
        emit(summary)
        return exc.code

    full = render_turns(turns)
    checks = verify_text(full)
    # The known quadratic-residue examples are a check that the checker itself works.
    baseline_notes = []
    for order, k, expect in ((7, 2, True), (7, 3, False), (19, 3, True), (19, 4, False)):
        spec = {"type": "paley", "order": str(order), "k": str(k)}
        try:
            _, _, outs = build_tournament(spec)
            ok, detail = has_property_s(outs, k)
        except DebateError as exc:
            baseline_notes.append(f"baseline QR_{order} S_{k}: error: {exc}")
            continue
        verdict = "pass" if ok == expect else "FAIL expected " + ("pass" if expect else "fail")
        baseline_notes.append(f"baseline QR_{order} S_{k}: {detail} ({verdict})")

    lines = [
        f"- Agree on a PROVED or COMPUTED claim: {'yes' if agreed else 'no'}",
        f"- Rounds used: {rounds_used}",
        f"- Stop: {stopped}",
        "- Latest status lines:",
    ]
    for title, body in turns:
        lines.append(
            f"  - {title}: STATUS={last_match(STATUS_RE, body) or '(none)'}; "
            f"CONFIDENCE={last_match(CONF_RE, body) or '(none)'}; "
            f"CLAIM_TAG={last_match(TAG_RE, body) or '(none)'}"
        )
    lines.append("- Construction checks:")
    lines.extend(f"  - {item}" for item in checks)
    lines.append("- Checker baselines (known Paley tournaments):")
    lines.extend(f"  - {item}" for item in baseline_notes)
    lines.append(f"- Transcript: {out_path}")
    summary = "\n".join(lines)
    flush(summary)
    emit("Summary")
    emit(summary)
    emit(f"Transcript: {out_path}")
    return 0


def smoke(timeout: int) -> int:
    workspace = prepare_cursor_workspace()
    prompt = NO_TOOLS + "\nReply with exactly the word PONG and nothing else."
    emit("Smoke: Claude...")
    claude_out = run_cli(claude_argv(), timeout, workspace, "Claude smoke", prompt)
    emit(claude_out)
    emit("Smoke: Cursor...")
    cursor_out = run_cursor(cursor_argv(workspace), timeout, workspace, "Cursor smoke", prompt)
    emit(cursor_out)
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Debate Erdős #902 between Claude Code and Cursor CLI.")
    parser.add_argument("--rounds", type=int, default=MAX_ROUNDS, help=f"Cursor critique rounds (1..{MAX_ROUNDS})")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Seconds per CLI call")
    parser.add_argument(
        "--opening-prompt",
        default="",
        help="Extra starting direction appended to every turn, for a rerun with a different attack",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Directory for erdos902_debate_<timestamp>.md",
    )
    parser.add_argument("--smoke", action="store_true", help="Send a one-word ping to both CLIs and exit")
    parser.add_argument(
        "--resume",
        type=Path,
        default=None,
        help="Transcript to continue. Completed turns are kept and not regenerated.",
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
        if args.smoke:
            return smoke(args.timeout)
        return debate(args.rounds, args.timeout, args.opening_prompt, args.out_dir, args.resume)
    except DebateError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return exc.code


if __name__ == "__main__":
    sys.exit(main())
