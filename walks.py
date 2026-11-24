"""HW3 · walks.py: read the step counter's CSV file and keep only the good rows. Practises
Session 7 (reading a CSV file, cleaning data) and Session 9 (a generator and a decorator)."""

import csv
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

WALKS_CSV = Path(__file__).parent / "walks.csv"

@dataclass
class Walk:
    """Provided: one walk from the log, cleaned. `steps` is a whole number, 0 or more."""
    date: str
    steps: int
    place: str


def parse_walk(row: dict[str, str]) -> Walk:
    # row = {"date": "2026-11-16", "steps": " 3100 ", "place": " campus "}
    date = row["date"].strip()
    print(date)
    if len(date) == 0:
        raise ValueError
    step = int(row["steps"])
    print(step)
    if step < 0:
        raise ValueError(f'steps is below o: {step}')
    place = row["place"].strip()
    print(place)
    if len(place) == 0:
        raise ValueError
    return Walk(date, step, place)
    

def none_on_error(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return None
    return wrapper


def read_rows(path: Path) -> Iterator[dict[str, str]]:
    with open(path, encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            yield row


def good_walks(rows: Iterable[dict[str, str]]) -> Iterator[Walk]:
    parse = none_on_error(parse_walk)
    for row in rows:
        walk = parse(row)
        if walk is not None:
            yield walk

if __name__ == "__main__":
    print(none_on_error('abc'))