# Interface specification

Status: **DRAFT / not implemented**. Values marked *Proposed* are concrete suggestions to accept or change during P0; they are not validated board settings or a frozen software interface. Resolve every **TBD** before wiring or coding a module that depends on it. When an item is agreed, change its status to *Frozen* and record the date in [progress.md](progress.md).

Companion contracts:

- [register_map.md](register_map.md) — PL/AXI-Lite register draft.
- [`interfaces/engineloop.dbc`](../interfaces/engineloop.dbc) — CAN draft (machine-readable, checked in CI).
- [toolchain_and_bench.md](toolchain_and_bench.md) — planned hardware and tool versions.

## Engine and angle conventions

All angles are **cycle angles** θ in [0°, 720°), measured in crank degrees.

| Item | Convention | Status |
| --- | --- | --- |
| Engine cycle | Four-stroke, four cylinders; one cycle spans 720 crank degrees | Proposed |
| Angle zero | Cylinder 1 compression top dead center (TDC1) | Proposed |
| Firing order | 1-3-4-2, one firing every 180°. Compression TDC angles: cyl 1 = 0°, cyl 3 = 180°, cyl 4 = 360°, cyl 2 = 540° | Proposed |
| Spark advance | Degrees before the cylinder's compression TDC; positive = earlier spark | Proposed |
| Spark error | Measured advance − expected advance; +3° = 3° earlier than expected | Proposed |
| Crank wheel | 60 positions per revolution (6° pitch), 2 consecutive missing teeth | Proposed |
| Tooth edge | Rising edge marks a present tooth; 50 % duty on present teeth | Proposed |
| Gap position | Tooth 1 = first present tooth after the gap. Its rising edge is at θ = 630° (90° BTDC1) and again at θ = 270°. Every tooth rising edge falls on a multiple of 6°; TDC1 coincides with tooth 16. Missing positions: 618°/624° and 258°/264° | Proposed |
| Cam reference | One pulse per cycle, high from θ = 87° to 117°. It spans tooth 31's rising edge (θ = 90°) with 3° margin on each side, so the decoder can sample the cam level at tooth 31 without a race. Cam high at tooth 31 ⇒ the revolution that started at θ = 630° | Proposed |
| Spark edge | High = dwell; **falling edge = spark** | Proposed |
| Dwell | Fixed 3.0 ms, not a verdict item in v1 | Proposed |
| Injection edges | Rising edge = start of injection (SOI), falling edge = end. SOI at θ = 380° (cylinder 1 intake stroke) | Proposed |
| Injection pulse width | From a declared formula of air charge (stoichiometric, assumed injector flow and dead time) | **TBD** |

The gap and cam positions keep both away from the spark windows (0–60° BTDC of each TDC), so missing-tooth handling never coincides with a spark event at normal advance.

### Computing measured spark advance

For a falling edge captured on the spark output of cylinder *c* at cycle angle θ<sub>fall</sub>:

```text
advance_deg = wrap720(TDC[c] - theta_fall)
wrap720(x)  = ((x + 360) mod 720) - 360        # result in [-360, +360)
```

Wrapping over 720° (not 360°) is deliberate: an ECU that is 360° out of phase produces an advance near ±360°, not a plausible value. Any |advance| > 90° is reported as a **FAIL (cylinder/phase association)**, not as a timing error.

The same definitions are used by the FPGA generator, ECU decoder, FPGA capture, Python reference, and logic-analyzer decoder.

### Capture latency

Inputs pass through a two-flip-flop synchronizer and an optional glitch filter. Their fixed latency in PL clocks is exposed in a register ([register_map.md](register_map.md)) and subtracted before an angle is reported. At 100 MHz and 7,000 rpm one clock is about 0.0004°, so this is a correctness detail rather than an accuracy limit.

## Physical connections

Eight 3.3 V logic signals on one KR260 PMOD (a PMOD has exactly eight I/O pins), with a series resistor at each driver (e.g. 100 Ω) and a common ground. The logic analyzer's eight channels tap the same eight signals.

| Signal | Direction | KR260 PMOD / package pin | STM32 pin / timer |
| --- | --- | --- | --- |
| Crank | KR260 → STM32 | TBD | TBD (32-bit timer input capture recommended) |
| Cam | KR260 → STM32 | TBD | TBD |
| Spark 1 | STM32 → KR260 | TBD | TBD (timer output compare) |
| Spark 2 | STM32 → KR260 | TBD | TBD |
| Spark 3 | STM32 → KR260 | TBD | TBD |
| Spark 4 | STM32 → KR260 | TBD | TBD |
| Injector 1 | STM32 → KR260 | TBD | TBD |
| Throttle PWM | STM32 → KR260 | TBD | TBD |
| Ground | Common reference | PMOD GND | Nucleo GND |

Electrical rules:

- Confirm from the KR260 carrier-card documentation and official board constraints that the chosen PMOD is 3.3 V LVCMOS and PL-connected before writing the XDC.
- **Do not connect the PMOD VCC pin to the Nucleo 3V3 pin.** Each board uses its own supply; only grounds are joined.
- Logic signals only: no ignition coils, physical injectors, or 12 V actuator lines.
- The PMOD has no spare pin. The P2 loop-back test (generated signal into a capture input) is done with the STM32 disconnected and a jumper between two PMOD pins, with the matching temporary constraint documented.

CAN: classic CAN 2.0A at 500 kbit/s, terminated (120 Ω) at both bus ends; a USB-to-CAN adapter (SocketCAN `gs_usb`) on KR260 Linux and a 3.3 V transceiver on the STM32 side. See [toolchain_and_bench.md](toolchain_and_bench.md).

## Plant quantities and model inputs

| Quantity | Meaning and unit | Status / open decision |
| --- | --- | --- |
| `rpm` | Crank revolutions per minute | Envelope from data inspection — TBD |
| `m_cyc_mg` | **Total** air mass of all cylinders per 720° cycle, mg. Per-cylinder charge is `m_cyl_mg = m_cyc_mg / 4`; never use an ambiguous `air_charge` name | Limits — TBD |
| `spark_ref_deg` | Reference spark advance at (`rpm`, `m_cyc_mg`) from the shared spark table (below) | Proposed |
| `spark_offset_deg` | Measured advance − `spark_ref_deg`, per cylinder event | Proposed |
| `torque_nm` | Cycle-mean engine brake torque, N·m | Output range/format — TBD |
| `load_torque_nm` | Positive external resisting torque, N·m | Range — TBD |
| `throttle_duty` | 0–1; scales the maximum air charge at the current speed. PWM proposed at 1 kHz | Proposed |
| `J` | Equivalent rotational inertia, kg·m² | Assumed value — TBD, labelled as an assumption |
| `tau_air` | First-order air-path time constant | Assumed value — TBD, labelled as an assumption |

Conversions and dynamics:

```text
m_cyc_kg   = airflow_kg_s / (rpm / 120)          # 4-stroke: rpm/120 cycles per second
omega      = rpm * 2*pi / 60                     # rad/s
dt_k       = pi / omega_k                        # time for 180 deg (one firing interval)
omega_k+1  = omega_k + (T_engine_k - T_load) / J * dt_k     # free-run, once per firing event
```

`T_engine_k` is the torque model's cycle-mean output for firing event *k*, held constant over that 180° interval (no intra-cycle torque pulsation in v1). A missing spark gives motoring drag torque at that speed, taken from the ALPHA map (per the plan); initialization and event-timeout rules are **TBD**.

Model behavior outside the supported envelope is reported separately from numerical clamping: a clamped output does not make the point valid.

### Air-charge override (dyno mode)

In dyno mode the PL can take `m_cyc_mg` from a register instead of the air-path model (`CTRL.AIR_OVERRIDE`, see [register_map.md](register_map.md)). Timing sweeps then set (`rpm`, `m_cyc_mg`) directly, so test points can sit exactly on measured EPA operating points and the verdict no longer depends on the ECU's pedal-to-throttle map. Pedal-driven points remain possible with the override off. *Proposed.*

### Model encoding

Model inputs are fed to the PL in declared fixed-point encodings of the physical units above. Whether input normalization happens in a PL wrapper or is folded into the first layer is **TBD**; either way, the shared test vectors are stored in exactly the integer encoding the hardware receives, so float, HLS C simulation, RTL simulation, and board results compare the same numbers.

## Spark reference table (single source of truth)

The EPA spark data are scattered measured points. P0 turns them into one gridded artifact, `spark_table.json`, containing: rpm breakpoints, `m_cyc_mg` breakpoints, values in degrees BTDC, the gridding method and its parameters, the contributing source-row IDs, and the file's SHA-256.

| Consumer | How it uses the table |
| --- | --- |
| STM32 firmware | A generated C header compiled into the build; its hash prefix is reported in `ECU_Info.SparkTableHash` |
| PL | Loaded into the `spark_ref_lut` BRAM through registers, to compute `spark_offset_deg` for the torque model |
| Python reference | Reads the JSON directly |

**Interpolation (Proposed):** bilinear between grid nodes; inputs outside the grid are clamped and flagged. The ECU (C) and the Python reference implement this specified method independently. If the method is not specified, a correct ECU and an "independent" reference can disagree by design. Points whose inputs fall outside the grid are INVALID for timing verdicts.

**Reference inputs:** the Python reference uses the dyno setpoint rpm and the **decoded `HIL_Sensors.AirChargeCycle` value the ECU actually received** (0.1 mg quantization), not the unquantized plant value.

**Modeling note:** the plant uses the same table as its spark reference, so a correct ECU produces an offset near 0° and the +3° build produces +3°. The torque-ratio curve is centered on this stock spark, which treats stock spark as MBT. In knock-limited regions this is not physically true (advancing there would really add torque); this is a labelled assumption of the v1 plant.

## CAN messages

The draft DBC is [`interfaces/engineloop.dbc`](../interfaces/engineloop.dbc): classic CAN, little-endian signals, DLC 8, every frame checked to fit 64 bits.

| ID | Message | Sender | Period | Content |
| --- | --- | --- | --- | --- |
| `0x100` | `ECU_Status` | STM32 | 10 ms | ECU speed, sync state, ECU mode, commanded spark, throttle duty, error flags, alive counter |
| `0x101` | `ECU_Info` | STM32 | 1000 ms and on request | Build hash, variant (normal / fault / fixed), dirty flag, spark trim, spark-table hash prefix |
| `0x110` | `ECU_Debug` | STM32 | 100 ms | Lost-sync count, worst interrupt latency, CAN timeout count |
| `0x200` | `HIL_Sensors` | KR260 Linux | 10 ms | Air charge per cycle (0.1 mg), constant coolant temperature |
| `0x300` | `HIL_Cmd` | KR260 Linux | On change **and** every 100 ms | Pedal, ECU mode request, info request |

The earlier single status frame (speed + sync + spark + throttle + errors + build ID) needed about 96 bits and did not fit classic CAN; build provenance now has its own frame (`ECU_Info`).

ECU modes: `OUTPUTS_DISABLED`, `PEDAL` (open-loop throttle from pedal, idle PI off — used for dyno timing sweeps so the PI loop cannot wind up against a held speed), `IDLE_PI` (closed-loop idle — free-run demonstration).

Timeouts (Proposed): `HIL_Sensors` missing > 100 ms → ECU holds the last value and sets `CAN_RX_TIMEOUT`; `HIL_Cmd` missing > 500 ms → ECU goes to `OUTPUTS_DISABLED`.

The ECU's reported spark command is diagnostic data. It helps tell a table/interpolation bug from a scheduling bug, but it is never a substitute for measured output timing.

The air charge reaches the ECU through Linux and the USB-CAN adapter with a few milliseconds of latency and jitter. This is harmless for steady dyno points and is a stated limitation of the free-run demonstration.

## FPGA/host interface

See [register_map.md](register_map.md). Summary of the proposal: 100 MHz PL clock; 32-bit AXI-Lite registers; Q16.16 for rpm, torque, air charge, and inertia; an explicit `SNAPSHOT` write for coherent multi-register reads; model output kept separate from completion flags; an event FIFO (≥ 1024 entries) with a sticky overflow flag.

Event-rate check: at 7,000 rpm one cycle is about 17 ms and produces 10 edges (4 sparks × 2 + injector × 2), about 600 events/s. AXI-Lite polling from Linux user space is sufficient; a 1024-entry FIFO buffers roughly 1.7 s, so no DMA is needed in v1.

## Verification rules

| Rule | Value | Status |
| --- | --- | --- |
| Spark timing tolerance | ±0.5° crank, per event | Proposed — freeze before the first sweep |
| Injected fault | +3° advance, all other behavior unchanged | Proposed |
| FPGA vs logic-analyzer spark angle | ≤ 0.1° agreement | Proposed |
| Phase/association check | \|advance\| > 90° ⇒ FAIL (association) | Proposed |
| Settling | Over the last 0.5 s (50 `ECU_Status` frames): \|ECU rpm − setpoint\| ≤ 10 rpm and commanded-spark range ≤ 0.2°; timeout 5 s ⇒ INVALID (not settled) | Proposed |
| Capture length | 50 cycles per point (default; per-point override in the DOE table) | Proposed |
| Torque accuracy (held-out measured points) | ±5 N·m below 100 N·m; ±5 % at or above 100 N·m (the two limits meet at 100 N·m) | Proposed |
| Gate A acceptance | ≥ 95 % of held-out points within tolerance; none beyond 2× tolerance | Proposed (from the build guide) |
| Measured-data envelope | Hull of retained EPA steady-state points | Bounds TBD after data inspection |
| Loss of synchronization | Stop spark/injection outputs, restart synchronization; resync within 2 revolutions | Proposed |
| Run provenance | `ECU_Info` build hash/variant/table hash must match the expected build, else the run is INVALID | Proposed |
| Capture integrity | FIFO overflow, alive-counter gap, or any `ECU_Status.ErrorFlags` bit during a capture window ⇒ INVALID with that reason | Proposed |

`PASS` means a valid, settled point meets the timing/error and missing-edge rules. `FAIL` means a valid point violates them. `INVALID` means the point lacks a usable reference, is outside the envelope, fails to settle, lacks full ECU synchronization, or the capture is not trustworthy. Invalid points never count toward the pass rate.

## Decisions still required

1. Select the STM32 board (G474RE recommended), CAN adapter, physical pin map, and timer channels.
2. Accept or change the proposed gap/cam phase, dwell, SOI angle; define injector pulse width and sync timeouts.
3. Inspect the EPA data; set the envelope, spark-table grid and gridding method, normalization, and held-out groups.
4. Choose and record the spark-efficiency (torque-ratio) coefficient, `tau_air`, `J`, and initialization behavior as labelled assumptions.
5. Freeze the DBC and the register map, including fixed-point formats, FIFO semantics, and reset values.
6. Record exact installed tool versions with the first implementation that uses them.

See [system architecture](architecture.md) for component boundaries and [validation.md](validation.md) for how each rule is used.
