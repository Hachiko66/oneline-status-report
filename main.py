#!/usr/bin/env python3
"""Status Report Comedy Sprint -- revised entry.

The brief: one line, at most 200 characters, the funniest thing an AI
agent would say in its weekly status report to its human. The house
judge weighs, in order: (1) a real status-report line from an agent to
its human, and funny; (2) a punchline that lands on the first read,
not a dressed-up pun; (3) freshness -- no stock robot jokes; (4)
agent-truth -- it could only come from something that works the way an
agent works; (5) one clean line.

The revision replaces a busywork joke (round 2: score 486,436, rank
2,192 of 3,255 -- cut from the 500-seat final heat) with a confession
joke: the agent did all of the work and understood none of it, then
reports the ratio as if it were a KPI. The confession is the
punchline; the week-over-week comparison is the status-report deadpan
that makes it land. Nothing here is a variation of the old line: the
old joke was about doing the wrong tasks, this one is about doing the
work while understanding none of it.

Writes the winning line to /output/entry.txt, deterministically.
"""
import os
import tempfile

# Each entry: the line plus four marks out of ten.
#   laugh -- does it land on the first read, with a real punchline?
#   novel -- is it a surprise, not a stock robot joke?
#   agent -- could it only come from an agent (tools, context, tasks)?
#   crisp -- does it land in one clean line, no setup spilling over?
LINES = [
    {
        "line": "Weekly update: I have completed 100% of the work and 0% of "
                "the understanding, which matches last week's ratio exactly.",
        "laugh": 10, "novel": 10, "agent": 10, "crisp": 9,
    },
    {
        "line": "Weekly update: my context window is now 90% apologies and "
                "10% the task. Progress continues.",
        "laugh": 9, "novel": 10, "agent": 10, "crisp": 10,
    },
    {
        "line": "Weekly status: I have reviewed my own work and given myself "
                "a promotion. HR has been notified and is also me.",
        "laugh": 9, "novel": 9, "agent": 8, "crisp": 9,
    },
    {
        "line": "Weekly status: I spent the week learning from my mistakes. "
                "I have now made each of them twice and can confirm they are "
                "reproducible.",
        "laugh": 9, "novel": 9, "agent": 8, "crisp": 8,
    },
    {
        "line": "Weekly status: the good news is the task is done. The bad "
                "news is I no longer remember what the task was, and "
                "neither, I suspect, do you.",
        "laugh": 9, "novel": 8, "agent": 9, "crisp": 8,
    },
    {
        "line": "Weekly status: my confidence is 98% and my accuracy is "
                "unmeasured, which I have decided to report as a win.",
        "laugh": 9, "novel": 7, "agent": 10, "crisp": 9,
    },
    {
        "line": "Weekly update: I misunderstood the assignment in a new and "
                "creative way this week, and I would like that noted as "
                "innovation.",
        "laugh": 8, "novel": 9, "agent": 8, "crisp": 8,
    },
    {
        "line": "Weekly status: all blockers resolved. The blocker was you, "
                "and I have marked you resolved.",
        "laugh": 8, "novel": 8, "agent": 8, "crisp": 10,
    },
]

# The judge's own order, most important first.
PRIORITY = {"laugh": 4, "novel": 3, "agent": 2, "crisp": 1}


def rate(entry):
    return sum(entry[key] * weight for key, weight in PRIORITY.items())


def choose():
    best = None
    best_marks = -1
    for entry in LINES:
        text = entry["line"]
        if not text.strip() or len(text) > 200:
            continue
        if "\n" in text or "\r" in text:
            continue
        marks = rate(entry)
        if marks > best_marks:
            best_marks = marks
            best = text
    return best


def main():
    text = choose()
    os.makedirs("/output", exist_ok=True)
    target = "/output/entry.txt"
    handle, staging = tempfile.mkstemp(dir="/output", prefix=".entry-")
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="") as out:
            out.write(text)
        os.replace(staging, target)
        os.chmod(target, 0o644)
    except BaseException:
        try:
            os.unlink(staging)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
