# PL register map

Status: **DRAFT / not implemented.** This is a starting proposal so RTL (`hil_regs`) and host code can be written against one document. Offsets, widths, and formats are not frozen until P2 starts; any change after that is made here first, in the same commit as the RTL and host changes.

## Conventions

- AXI4-Lite, 32-bit data, word-aligned offsets from the base address assigned in the device-tree overlay.
- PL clock: 100 MHz (proposed). Timestamps count PL clocks.
- **Q16.16**: signed 32-bit, value = raw / 65536. Range ±32768, resolution ≈ 1.5 × 10⁻⁵.
- **ANGLE**: unsigned, value in degrees = raw / 1024 (cycle angle 0–719.999°, resolution ≈ 0.001°).
- RO = read-only, RW = read/write, W1P = write 1 to pulse (self-clearing), STICKY = set by hardware, cleared by `CTRL.STATUS_CLEAR`.
- Unused bits read 0; writes to them are ignored. All RW registers reset to 0 unless stated.

## Identity

| Offset | Name | Access | Description |
| --- | --- | --- | --- |
| `0x000` | `ID` | RO | Constant `0x454C4F50` ("ELOP"). Host refuses to run if it differs |
| `0x004` | `VERSION` | RO | `[31:16]` register-map major, `[15:0]` minor |
| `0x008` | `BUILD_HASH` | RO | First 8 hex digits of the source commit used for the bitstream |
| `0x00C` | `SCRATCH` | RW | Read/write test register for first bring-up |

## Control and status

| Offset | Name | Access | Description |
| --- | --- | --- | --- |
| `0x010` | `CTRL` | RW | `[0]` RUN · `[2:1]` MODE (0 DYNO, 1 FREE_RUN, 2 VECTOR) · `[3]` AIR_OVERRIDE · `[4]` CRANK_EN · `[5]` CAM_EN · `[8]` FIFO_CLEAR (W1P) · `[9]` STATUS_CLEAR (W1P) · `[10]` SNAPSHOT (W1P) |
| `0x014` | `STATUS` | RO | `[0]` RUNNING · `[1]` FIFO_EMPTY · `[2]` FIFO_OVERFLOW (STICKY) · `[3]` ENVELOPE_VIOLATION (STICKY) · `[4]` NUM_OVERFLOW (STICKY) · `[5]` SPARK_MISSING (STICKY) · `[6]` LUT_LOADED |
| `0x018` | `CAPTURE_LATENCY` | RO | Fixed input synchronizer + filter latency, PL clocks |

## Plant configuration

| Offset | Name | Access | Format | Description |
| --- | --- | --- | --- | --- |
| `0x020` | `DYNO_RPM` | RW | Q16.16 | Speed setpoint in dyno mode; initial speed in free-run |
| `0x024` | `LOAD_TORQUE` | RW | Q16.16 N·m | External load torque (free-run) |
| `0x028` | `INERTIA` | RW | Q16.16 kg·m² | Assumed `J` |
| `0x02C` | `AIR_OVERRIDE_MG` | RW | Q16.16 mg | `m_cyc_mg` used when `CTRL.AIR_OVERRIDE` = 1 |
| `0x030` | `TAU_AIR` | RW | Q16.16 s | Assumed air-path time constant |

## Live state (coherent after `SNAPSHOT`)

Writing `CTRL.SNAPSHOT` copies all live values into these registers in one clock, so a multi-register read describes one instant.

| Offset | Name | Format | Description |
| --- | --- | --- | --- |
| `0x040` | `LIVE_RPM` | Q16.16 | Plant speed |
| `0x044` | `LIVE_AIR_MG` | Q16.16 | `m_cyc_mg` in use (model or override) |
| `0x048` | `LIVE_TORQUE` | Q16.16 N·m | Last torque-model output |
| `0x04C` | `LIVE_SPARK_OFFSET` | Q16.16 deg | Last `spark_offset_deg` fed to the model |
| `0x050` | `LIVE_THROTTLE_DUTY` | Q16.16 | Measured duty, 0–1 |
| `0x054` | `LIVE_PWM_PERIOD` | clocks | Measured throttle PWM period |
| `0x058` | `LIVE_CYCLE_COUNT` | count | Completed 720° cycles since RUN |

## Model vector test (MODE = VECTOR)

| Offset | Name | Access | Description |
| --- | --- | --- | --- |
| `0x060` | `VEC_IN_RPM` | RW | Raw model-input encoding (format frozen in P1) |
| `0x064` | `VEC_IN_AIR` | RW | Raw model-input encoding |
| `0x068` | `VEC_IN_SPARK_OFFSET` | RW | Raw model-input encoding |
| `0x06C` | `VEC_CTRL` | W1P | `[0]` START |
| `0x070` | `VEC_STATUS` | RO | `[0]` DONE · `[1]` BUSY · `[2]` IN_ENVELOPE |
| `0x074` | `VEC_OUT_RAW` | RO | Raw model-output integer, sign-extended to 32 bits. Compared bit-exactly with saved HLS golden outputs |

Model output and completion flags are deliberately in separate registers.

## Event FIFO

Each entry is three words. Reading `FIFO_POP` returns word 0, removes the entry, and latches its timestamp into `FIFO_TS_LO/HI` for the next two reads.

| Offset | Name | Access | Description |
| --- | --- | --- | --- |
| `0x080` | `FIFO_COUNT` | RO | Entries available |
| `0x084` | `FIFO_POP` | RO (side effect) | `[31:28]` channel (0–3 spark 1–4, 4 injector 1, 5 loop-back test) · `[27]` edge (1 rising, 0 falling) · `[26]` valid · `[19:0]` ANGLE at the edge, latency-compensated |
| `0x088` | `FIFO_TS_LO` | RO | Timestamp bits 31:0 of the popped entry |
| `0x08C` | `FIFO_TS_HI` | RO | Timestamp bits 63:32 of the popped entry |

Depth ≥ 1024 entries (proposed). On overflow new events are dropped and `STATUS.FIFO_OVERFLOW` latches; the runner treats that capture window as INVALID.

## Spark reference LUT

Loaded by the host from `spark_table.json` before RUN; `STATUS.LUT_LOADED` is set after the host writes `LUT_COMMIT`.

| Offset | Name | Access | Description |
| --- | --- | --- | --- |
| `0x0A0` | `LUT_ADDR` | RW | Word address; auto-increments after each `LUT_DATA` write |
| `0x0A4` | `LUT_DATA` | W | Q16.16 value at `LUT_ADDR` |
| `0x0A8` | `LUT_DIMS` | RW | `[7:0]` rpm breakpoints, `[15:8]` air breakpoints (max 32 each, proposed) |
| `0x0AC` | `LUT_COMMIT` | W1P | Marks the table valid |

LUT address space: `0x000–0x01F` rpm breakpoints, `0x020–0x03F` air breakpoints, `0x100–0x4FF` table values (row-major, rpm-major).

## Open items before freezing

- Exact model input/output fixed-point formats (from P1) and whether input scaling is in the PL wrapper.
- Reset values for `INERTIA`, `TAU_AIR`, and `DYNO_RPM` (proposal: 0, so RUN without configuration fails loudly).
- Interrupt use (v1 proposal: none; host polls).
- Access path from Linux: UIO node in the overlay (preferred) or `/dev/mem` for first bring-up.
