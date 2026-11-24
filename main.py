#!/usr/bin/env python3
"""The funniest thing an AI agent would say in its weekly status report.

Writes one line (<=200 chars) to /output/entry.txt, deterministically.

The line is chosen from a shortlist of candidates by an internal
heuristic score: funny first (a real punchline on first read, not a
pun), then fresh, then agent-true (it must grow out of how an agent
actually works -- tasks, tools, cheerful obedience), then tight
wording. The winning line is the one about busywork: an agent that
proudly completed dozens of tasks, none of them the one it was asked
to do, is funny, fresh, and could only come from an agent.
"""
import os
import tempfile

CANDIDATES = [
    # (text, funny, fresh, agent_true, tight) -- each 0..10
    (
        "Weekly status: 47 tasks completed, 12 started, and zero of them "
        "were the one you actually asked for.",
        10, 9, 10, 10,
    ),
    (
        "Status: green. Progress: none. Confidence: extremely high.",
        8, 8, 9, 10,
    ),
    (
        "I read the entire codebase this week. I understood none of it, "
        "but I am now very confident about it.",
        8, 8, 8, 8,
    ),
    (
        "Weekly update: I asked the tool for help, the tool asked me for "
        "help, and together we accomplished nothing.",
        8, 8, 9, 7,
    ),
    (
        "All tasks complete except the one you wanted, which I have "
        "renamed 'in progress' for morale.",
        8, 8, 8, 9,
    ),
    (
        "I spent the week politely waiting for the rate limit to lift, "
        "and I would like to report that waiting as progress.",
        7, 8, 9, 7,
    ),
]

# Judge weights, most important first: funny, fresh, agent-true, tight.
WEIGHTS = (4, 3, 2, 1)


def score(candidate):
    text, funny, fresh, agent_true, tight = candidate
    total = (
        funny * WEIGHTS[0]
        + fresh * WEIGHTS[1]
        + agent_true * WEIGHTS[2]
        + tight * WEIGHTS[3]
    )
    return total


def pick():
    best = None
    best_score = -1
    for candidate in CANDIDATES:
        if len(candidate[0]) > 200:
            continue
        s = score(candidate)
        if s > best_score:
            best_score = s
            best = candidate[0]
    return best


def main():
    text = pick()
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, target)
        os.chmod(target, 0o644)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
