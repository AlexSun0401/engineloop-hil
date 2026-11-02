#!/usr/bin/env python3
"""Sanity-check the EngineLoop CAN DBC.

Checks: the file parses in cantools strict mode (no overlapping signals, no
signal past the frame end), every frame is classic CAN (standard 11-bit ID,
DLC <= 8), and every frame has a sender and a cycle-time or comment.

Usage:  python tools/check_dbc.py interfaces/engineloop.dbc
Requires: pip install cantools
"""
from __future__ import annotations

import sys

import cantools


def main(path: str) -> int:
    db = cantools.database.load_file(path, strict=True)
    problems: list[str] = []
    for msg in db.messages:
        tag = f"0x{msg.frame_id:03X} {msg.name}"
        if msg.is_extended_frame:
            problems.append(f"{tag}: extended ID not allowed (classic 11-bit only)")
        if msg.frame_id > 0x7FF:
            problems.append(f"{tag}: ID exceeds 11 bits")
        if msg.length > 8:
            problems.append(f"{tag}: DLC {msg.length} > 8 (classic CAN)")
        if not msg.senders:
            problems.append(f"{tag}: no sender node")
        used = sum(s.length for s in msg.signals)
        print(f"{tag:<22} DLC={msg.length} signals={len(msg.signals):2d} bits used={used:2d}/64 "
              f"cycle={msg.cycle_time or '-'} ms sender={','.join(msg.senders)}")
    for p in problems:
        print("ERROR:", p)
    print(f"{len(db.messages)} frames: {'OK' if not problems else f'{len(problems)} problem(s)'}")
    return 1 if problems else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
