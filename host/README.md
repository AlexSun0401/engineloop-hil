# Linux test orchestration - planned

Owns the Python side running on the KR260 ARM/Linux system.

Future responsibilities:

1. Access PL commands, status, and captured events through a defined register interface.
2. Send virtual sensor values and commands over CAN; receive ECU status.
3. Flash a selected firmware build and record its identity.
4. Run an operating-point table, wait for settling, and capture cycles.
5. Calculate expected timing independently of the ECU implementation.
6. Assign PASS / FAIL / INVALID verdicts and produce versioned reports.
7. Analyze selected logic-analyzer captures independently of PL angle capture.

Future entry points: `orchestrator.py`, `report.py`, and `la_check.py`. None exists yet.

`doe/` is reserved for reviewed operating-point definitions. No sample rows or synthetic measurements are included in this scaffold. Actual points must state mode, speed/pedal/load inputs, settling timeout, and capture duration, with units defined in the interface specification.

See the [validation plan](../docs/validation.md) before implementing verdict logic.
