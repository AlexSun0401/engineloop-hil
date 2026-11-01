# FPGA plant and timing I/O - planned

Owns the KR260 programmable-logic implementation.

| Planned module | Responsibility |
| --- | --- |
| `crank_gen` | Generate 60-2 crank and a 720° cam reference |
| `edge_capture` | Synchronize and timestamp ECU spark/injector edges |
| `pwm_meas` | Measure throttle PWM duty and period |
| `airpath` | Convert throttle duty to air charge using an assumed lag |
| `torque_core` | Evaluate the torque surrogate using measured spark timing |
| `dynamics` | Update speed from net torque in free-run; hold setpoint in dyno |
| `hil_regs` | Expose commands, state, test-vector access, and captured events |

Directory boundaries: `rtl/`, `tb/`, `constraints/`, and `overlay/`. They contain placeholders only. Add source and module-level simulation before board integration.

Pins, clock constraints, register formats, synchronization behavior, and the custom overlay must be confirmed during implementation. Do not wire from an unreviewed pin guess. The proposed bench uses 3.3 V logic; real coils, injectors, and 12 V lines are outside its interface.

See [architecture](../docs/architecture.md), [interfaces](../docs/interface_spec.md), and [validation](../docs/validation.md).
