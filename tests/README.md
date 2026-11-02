# Validation cases - planned

The only executable checks today are repository checks, run locally and in CI:

| Check | Command |
| --- | --- |
| Relative Markdown links resolve | `python tools/check_md_links.py` |
| CAN DBC parses (strict) and fits classic CAN | `python tools/check_dbc.py interfaces/engineloop.dbc` |

Planned checks, added alongside each implemented component:

| Layer | Planned check |
| --- | --- |
| Data | Units, schema, provenance, split-group separation, no target leakage, spark-table hash stable |
| Model | Held-out measured accuracy; float vs HLS (≤ 0.5 % of range); quantized vs HLS |
| RTL | Trigger geometry and gap/cam phase, capture latency and FIFO overflow, numerical equivalence, mode behavior |
| Firmware | Synchronization states, output timing, signal-loss response, CAN encode/decode against the DBC, interpolation vs a Python reference on the same table |
| Integration | On-board vectors bit-exact, independent logic-analyzer timing, build-identity check, normal/faulty/fixed regression |

Define each check's stimulus, reference, tolerance, evidence, and supported claim. A fixture is an input or reference, not proof that the hardware passed. See [docs/validation.md](../docs/validation.md).
