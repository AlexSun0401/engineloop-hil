# Validation and evidence plan

**Status:** planned checks only. This repository contains no measured accuracy, successful simulation, hardware timing result, or completed regression run. Numbers below are proposed acceptance targets; they are finalized in the [interface specification](interface_spec.md#verification-rules) before the check is run.

## Separate the claims

Each check supports one specific claim and is reported separately. Numerical agreement does not establish physical engine accuracy, and successful FPGA simulation does not establish correct bench wiring or timing.

| # | Evidence | Reference and comparison | Proposed acceptance rule | What it supports |
| --- | --- | --- | --- | --- |
| 1 | Measured-point torque accuracy | Float model (and later the quantized model) vs held-out EPA measured points at zero spark offset | ±5 N·m below 100 N·m, ±5 % at or above; ≥ 95 % of points within tolerance, none beyond 2× | Steady-state torque approximation inside the evaluated envelope |
| 2 | Fixed-point vs float | hls4ml C simulation vs the float model on shared in-envelope input vectors | Max \|difference\| ≤ 0.5 % of the declared output range; no overflow in any layer | Quantization and conversion keep the float model's behavior |
| 2b | Conversion sanity (diagnostic) | hls4ml C simulation vs the quantized Keras model on the same vectors | Bit-exact, or within 1 LSB with the cause explained | Isolates conversion bugs from quantization error |
| 3 | Hardware vs C simulation | Raw on-board fixed-point output vs saved HLS integer outputs | Bit-exact for every shared vector, including defined boundary handling | Correct integration of the model on the FPGA |
| 4 | ECU timing | Logic-analyzer crank/cam/spark/injector capture vs the interface spec, and vs FPGA capture | Spark within ±0.5° of reference (tolerance frozen before testing); analyzer vs FPGA within 0.1° | Actual signal timing; cross-check of the FPGA measurement path |
| K | Known-error regression | Identical sweep against normal, +3° faulty, and fixed builds | Normal and fixed PASS every eligible point; faulty FAILs every eligible point with about +3° signed error | The test detects the selected fault and confirms its repair |
| D | Closed-loop idle demonstration | Free-run speed trace during a declared load step | Record dip and recovery; guide target ±50 rpm | Closed-loop operation under stated assumptions only |

Numbering 1–4 and K follow the agreed plan. Software-to-HLS agreement alone cannot show that either model is accurate; evidence 1 is rerun with the quantized model before Gate B.

## Dataset and model evidence

- Split by operating-point group so measured rows and their synthetic spark-offset descendants never sit on opposite sides of the split. Save the group allocation, source-row traceability, normalization constants, model weights, and vector encodings.
- Report real-data accuracy only on held-out measured, zero-offset rows. Synthetic spark-offset rows exercise an assumed response and are never presented as experimental validation.
- Report the same held-out metric for a simple interpolation baseline fitted to the same training points. This is a number in the P0 report, not a second deliverable; it shows whether the MLP earns its place.
- Exclude enrichment and transient regions from the v1 accuracy claim.
- For fixed-point checks, declare the output-range denominator, rounding/saturation rules, signed widths, and overflow policy before scoring. Keep raw integer comparisons for bit-exact checks.

## Timing sweep and verdicts

Use **dyno mode** with the ECU in `PEDAL` mode for the main steady-state sweep. With `AIR_OVERRIDE` on, each point sets speed and air charge directly.

### DOE point table

A versioned CSV in `host/doe/`. Proposed columns:

| Column | Meaning |
| --- | --- |
| `point_id` | Stable identifier, never reused |
| `mode` | `dyno` or `free_run` |
| `rpm` | Speed setpoint |
| `air_mg` | Air-charge override (`m_cyc_mg`); empty = from throttle/air path |
| `pedal_pct` | Pedal command sent in `HIL_Cmd` |
| `load_nm` | External load (free-run) |
| `ecu_mode` | `PEDAL` or `IDLE_PI` |
| `settle_timeout_s` | Default 5 |
| `capture_cycles` | Default 50 |
| `class` | `in_envelope`, `out_of_envelope` (expected INVALID), or `sync_test` |
| `notes` | Free text, e.g. "on measured EPA point" |

The table's SHA-256 goes into the run manifest. Use points both on measured EPA operating points (reference = table value at a grid node) and between them (reference = specified bilinear interpolation).

### Per-point procedure

1. Check the operating envelope and reference availability; out-of-envelope rows exist on purpose to exercise INVALID handling.
2. Apply the condition and wait for the declared settling rule.
3. Confirm full synchronization, clear the FIFO and sticky flags, and collect the requested cycles.
4. Calculate expected spark in Python from `spark_table.json` with the specified interpolation, using the setpoint rpm and the **decoded CAN air charge the ECU received**. Never read back the ECU's commanded value as the reference, and never reuse the ECU's C code.
5. Compute advance from captured falling edges per [the angle convention](interface_spec.md#computing-measured-spark-advance). Check event counts, cylinder sequence, plausibility (|advance| ≤ 90°), and injector timing.
6. Record per-cylinder mean, minimum, maximum, standard deviation, missing-edge counts, the ECU's commanded spark (diagnostic), verdict, and reason. The verdict uses every event against the limit; a mean must not hide a failing event.

| Verdict | Meaning |
| --- | --- |
| `PASS` | Eligible, settled, synchronized; every required timing/event check meets the declared limits |
| `FAIL` | An eligible measurement violates a required check, including a missing expected edge or a phase/association error |
| `INVALID` | The point cannot support the comparison: outside the envelope or spark-table grid, no reference, not settled, not synchronized, FIFO overflow, CAN alive-counter gap, ECU error flag set, or wrong build. The specific reason is recorded |

An invalid point is never a pass. Report attempted, eligible, passed, failed, and invalid counts with their denominators. Unexpected invalid points prevent a claim that the intended coverage completed. Dedicated sync-loss tests have their own expected shutdown and recovery assertions.

### Build-identity check

Before a sweep the runner requests `ECU_Info` and compares `BuildHash`, `BuildVariant`, `BuildDirty`, and `SparkTableHash` with the expected build and the table the reference uses. Any mismatch marks the whole run INVALID before a single point is measured. This is the A/B discipline that keeps normal/faulty/fixed comparisons honest.

## Independent signal measurement

For about five selected points per run, capture all eight signals with the logic analyzer. A separate decoder finds the missing-tooth gap, reconstructs cylinder-1 phase from the cam reference, and derives spark angles from observed edges. Show expected angle, FPGA-measured angle, analyzer-measured angle, and both errors side by side.

This reduces dependence on a single FPGA implementation for both generation and measurement. It does not validate the engine model's assumed combustion response.

## Deliberate-fault campaign

The three builds differ only in the spark trim and its repair; each reports its variant and hash in `ECU_Info`. Use the same point table, spark table, envelope, and thresholds for all three.

| Build | Intended behavior | Expected outcome — not a recorded result |
| --- | --- | --- |
| Normal | Nominal spark schedule | All eligible timing points pass |
| Faulty | `+3°` trim using the spec's advance convention | Every eligible point fails with about `+3°` error |
| Fixed | Trim removed | All eligible points pass again |

The ±0.5° limit leaves a wide margin below the 3° fault. A faulty point that passes, becomes unexpectedly invalid, or is never captured does not demonstrate detection; investigate the runner, measurement, convention, or coverage before claiming success.

## Idle demonstration

Use **free-run mode** with the ECU in `IDLE_PI`. At zero pedal, apply a declared load step and log speed, load, and throttle at 100 Hz. Report the idle setpoint, initial condition, load amplitude and duration, inertia, air-path lag, controller gains, dip, and the recovery definition.

The ±50 rpm criterion is a planning value. Assumed inertia and air-path lag make this a closed-loop demonstration, not validation of a real engine's transient response.

## Report provenance

Each run writes a machine-readable manifest next to its report. Proposed fields:

```text
run_id, started_utc, operator_notes
repo_commit, repo_dirty
ecu: build_hash, build_variant, build_dirty, spark_trim_deg, spark_table_hash16
pl: bitstream_sha256, pl_build_hash (BUILD_HASH register), register_map_version
model_weights_sha256, spark_table_sha256, dataset_sha256, split_id
doe_table_sha256, tolerance_config_sha256
tool_versions: os_image, kernel, vivado, hls4ml, keras_stack, cubeide, python_can, cantools, sigrok
counts: attempted, eligible, pass, fail, invalid (with reasons)
```

Store genuine selected evidence when it exists (tagged evidence sets; large captures attached to a GitHub Release). Do not add invented benchmark numbers, placeholder passing reports, or claims that unexecuted gates have passed.
