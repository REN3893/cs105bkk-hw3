"""HW3 · report.py: add up the steps and save a report as JSON. Practises Session 7 (writing
and reading JSON) and Session 9 (a context manager)."""

import json
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import TextIO

from walks import Walk, good_walks, read_rows

def steps_per_day(walks: Iterable[Walk]) -> dict[str, int]:
    total: dict[str, int] = {}
    for walk in walks:
        total[walk.date] = total.get(walk.date, 0) + walk.steps
    return {date: total[date] for date in sorted(total)}


def best_day(totals: dict[str, int]) -> str:
    if not totals:
        raise ValueError
    return min(totals, key=lambda date: (-totals[date], date))


@contextmanager
def saved_safely(path: Path) -> Iterator[TextIO]:
    tmp = path.with_name(path.name + ".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as file:
            yield file
    except:
        tmp.unlink(missing_ok=True)
        raise 
    tmp.replace(path)

def write_report(path: Path, walks: Iterable[Walk]) -> dict:
    days = steps_per_day(walks)
    report = {
        "total_steps": sum(days.values()),
        "best_day": best_day(days),
        "days": days
    }
    with saved_safely(path) as file:
        json.dump(report, file, indent=2)
    return report


def load_report(path: Path) -> dict | None:
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except:
        return None


if __name__ == "__main__":
    # Provided: runs only with `python report.py`, not on import.
    here = Path(__file__).parent
    last_time = load_report(here / "report.json")
    report = write_report(here / "report.json", good_walks(read_rows(here / "walks.csv")))
    print(f"{report['total_steps']} steps this week. Best day: {report['best_day']}.")
    if last_time is not None:
        print(f"Last time you saved {last_time['total_steps']} steps.")
