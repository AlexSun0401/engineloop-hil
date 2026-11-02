# STM32 ECU firmware - planned

Owns the simplified controller under test.

**Board (planned):** Nucleo-G474RE recommended (170 MHz, FDCAN in classic mode, many timers), Nucleo-F446RE as the alternative (bxCAN). SN65HVD230 transceiver. See [toolchain_and_bench.md](../docs/toolchain_and_bench.md).

Planned modules:

- Crank/cam decoding: 32-bit timer input capture on crank; gap detection by tooth-period ratio; cam level sampled at tooth 31. State machine `NO_SYNC → GAP_FOUND → FULL_SYNC`, `SYNC_LOST` on a missing/extra tooth.
- Spark scheduling for four cylinders and injector-1 timing with hardware output-compare (no software-timed edges).
- Spark table from the generated header (`spark_table.h`, built from `data/processed/spark_table.json`) with the bilinear interpolation specified in the [interface spec](../docs/interface_spec.md#spark-reference-table-single-source-of-truth).
- Pedal mapping, throttle PWM (1 kHz proposed), ECU modes, PI idle control with anti-windup.
- CAN per [`interfaces/engineloop.dbc`](../interfaces/engineloop.dbc), including timeouts and `ECU_Info`.
- Build variants from one source tree:

| Variant | Build flag (proposed) | `ECU_Info.BuildVariant` | `SparkTrim` |
| --- | --- | --- | --- |
| Normal | `SPARK_TRIM_DECIDEG=0` | `NORMAL` | 0.0° |
| Fault | `SPARK_TRIM_DECIDEG=30` | `FAULT_SPARK_PLUS3` | +3.0° |
| Fixed | trim removed in code | `FIXED` | 0.0° |

The build embeds the git hash and a dirty flag, reported in `ECU_Info`.

Only full synchronization enables spark and injection. Signal-loss behavior and resynchronization are tested explicitly (Gate D).

Flashing from the KR260 is planned with OpenOCD or stlink-tools (see the toolchain doc).

No CubeIDE project, source, binary, or firmware test exists yet. Add the first project with its tool versions, reproducible build instructions, and the selected pin/peripheral assignments (also recorded in the interface spec).
