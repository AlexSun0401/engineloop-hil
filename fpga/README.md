# FPGA plant and timing I/O - planned

Owns the KR260 programmable-logic design.

| Planned module | Responsibility | Bring-up step |
| --- | --- | --- |
| `crank_gen` | 60-2 crank and one cam pulse per 720°, from a phase accumulator, per the [interface spec](../docs/interface_spec.md) | 1 — trigger/capture |
| `edge_capture` | Synchronize, deglitch, latency-compensate, and timestamp spark/injector edges into a FIFO | 1 |
| `pwm_meas` | Throttle PWM duty and period | 1 |
| `hil_regs` | AXI-Lite registers per [register_map.md](../docs/register_map.md) | 1 |
| `airpath` | Duty × max-air(rpm) through an assumed lag; register override in dyno mode | 2 — plant |
| `spark_ref_lut` | Reference spark from the host-loaded shared table | 2 |
| `torque_core` | hls4ml IP evaluating torque from speed, air charge, spark offset | 2 |
| `dynamics` | Speed update per firing event in free-run; setpoint in dyno | 2 |

Step 1 is all the STM32 work needs, so finish it first.

Planned directories (created with their first file): `rtl/`, `tb/`, `constraints/`, `app/` (Kria app packaging: `.bit.bin`, `.dtbo`, `shell.json`), `scripts/` (Vivado Tcl to rebuild the project from source — commit Tcl, not the project folder).

Rules:

- Module-level simulation before board integration.
- Pins and I/O standards come from the official KR260 board constraints for the chosen PMOD; do not wire from a guessed pin.
- 3.3 V logic only; no PMOD VCC to the Nucleo; real coils, injectors, and 12 V lines are outside this interface.
- Bitstreams and overlays are release artifacts with a recorded SHA-256, not committed files.

Load on the board (planned): copy the app files to `/lib/firmware/xilinx/engineloop/`, then `sudo xmutil unloadapp` and `sudo xmutil loadapp engineloop`. Access registers through a UIO node (preferred) or `/dev/mem` for first bring-up.

See [architecture](../docs/architecture.md#fpga-blocks) and [validation](../docs/validation.md).
