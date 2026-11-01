# Validation cases - planned

No executable tests or passing results exist yet. Add checks alongside each implemented component.

| Layer | Planned check |
| --- | --- |
| Data | Units, schema, provenance, split-group separation, no target leakage |
| Model | Held-out measured accuracy; float/quantized/HLS numerical agreement |
| RTL | Trigger geometry, event capture, numerical equivalence, mode behavior |
| Firmware | Synchronization, output timing, signal-loss response, CAN decoding |
| Integration | Shared on-board vectors, independent logic-analyzer timing, firmware fault regression |

Define each check's stimulus, reference, tolerance, actual evidence, and supported claim. A fixture is an input or reference, not proof that the hardware passed. See [docs/validation.md](../docs/validation.md).
