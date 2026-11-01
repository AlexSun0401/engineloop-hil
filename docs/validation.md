# Validation and evidence plan

**Status:** planned checks only. This repository currently contains no measured accuracy, successful simulation, hardware timing result, or completed regression run. Numbers below are proposed acceptance targets from the build guide and must be finalized in the [interface specification](interface_spec.md).

## Separate the claims

Each check supports a specific claim. Numerical agreement does not establish physical engine accuracy, and successful FPGA simulation does not establish correct bench wiring or timing.

| Evidence | Reference and comparison | Proposed acceptance rule | What it supports |
| --- | --- | --- | --- |
| Measured-point torque accuracy | Predicted torque against held-out EPA measured rows at zero spark offset | A declared absolute tolerance below a torque breakpoint and relative tolerance above it; guide target: ≥95% pass, none beyond twice tolerance | Steady-state torque approximation inside the evaluated envelope |
| Quantization/conversion accuracy | HLS C output against the software quantized-model output on shared in-envelope vectors | Maximum absolute discrepancy ≤0.5% of the declared output range; no unaccounted overflow | Faithful numerical conversion; measured-point accuracy must also be rechecked |
| FPGA/HLS equivalence | Raw on-board fixed-point output against saved HLS integer outputs | Bit-exact agreement for every shared vector, including defined boundary/out-of-range handling | Correct integration of the selected numerical model on the FPGA |
| Independent physical timing | Logic-analyzer crank/cam/spark/injector capture against the specification and FPGA capture | Declared trigger tolerances; guide target for analyzer-vs-FPGA spark-angle agreement: about 0.1° | Actual signal timing and a cross-check of the FPGA measurement path |
| ECU known-error regression | Identical timing sweep against normal, `+3°` faulty, and repaired builds; independent Python expected spark | Normal/repaired pass every eligible point; faulty fails every eligible point near the injected signed offset | Detection and repair verification of the selected timing fault |
| Closed-loop idle demonstration | Free-run speed trace during a declared load step | Record speed dip and recovery; guide target: idle remains within ±50 rpm through the specified test | Closed-loop operation under stated model assumptions |

The float baseline and quantized model must both be evaluated against measured held-out rows. Software-to-HLS agreement alone cannot show that either model is accurate.

## Dataset and model evidence

Split by operating-point group so measured rows and their synthetic spark-offset descendants cannot occur on opposite sides of the split. Save the group allocation, source-row traceability, normalization constants, model weights, and vector encodings. Keep the final evaluation split and envelope fixed for a reported run; version any deliberate change.

Report real-data accuracy only on held-out measured, zero-offset rows. Synthetic spark-offset rows exercise an assumed torque response and must not be presented as independent experimental validation. Exclude unsupported enrichment/transient regions from the v1 accuracy claim.

For fixed-point checks, declare the output-range denominator, rounding/saturation rules, signed widths, and overflow policy before scoring. Keep raw integer comparisons for bit-exact checks. Out-of-envelope vector behavior can be verified without turning it into an in-envelope accuracy claim.

## Timing sweep and verdicts

Use **dyno mode**, which holds speed at a setpoint, for the main steady-state timing sweep. Each point supplies its mode, speed, pedal position, external load, settling timeout, and capture-cycle count. Freeze the point table and thresholds for a normal/faulty/repaired comparison.

For each point:

1. Check the operating envelope and reference availability; retain explicit out-of-envelope cases for invalid-status checks.
2. Apply the condition and wait for the declared speed/spark stability window.
3. Confirm full synchronization, clear old captures, and collect the requested cycles.
4. Calculate expected spark independently in Python from the reference data, rather than reading back the ECU's commanded value or reusing its C interpolation implementation.
5. Compare actual captured falling-edge spark angles with that reference; check event counts, cylinder sequence, and defined injector timing.
6. Preserve per-cylinder mean, minimum, maximum, standard deviation, missing-edge counts, verdict, and reason. Means must not conceal a failing limit or missing event.

| Verdict | Meaning |
| --- | --- |
| `PASS` | The point is eligible, settled, and synchronized; all required timing/event checks meet the declared limits. |
| `FAIL` | An eligible measurement violates a required timing/event check, including a missing expected edge within an otherwise valid capture window. |
| `INVALID` | The point cannot support the intended timing comparison: outside the envelope, missing reference, not settled, or not in full synchronization. Record the specific reason. |

An invalid point is never a pass. Report attempted, eligible, passed, failed, and invalid counts with their denominators. Unexpected invalid points, incomplete captures, FIFO overflow, communication faults, and synchronization failures must remain visible and prevent a claim that the intended regression coverage completed. Dedicated sync-loss tests have their own expected output-shutdown and recovery assertions.

## Independent signal measurement

For selected points, capture crank, cam, spark 1, and injector 1 with a logic analyzer. A separate decoder identifies the missing-tooth gap, reconstructs cylinder-1 phase from the agreed reference, and derives spark angle from observed edges. Show expected angle, FPGA-measured angle, analyzer-measured angle, and both errors side by side.

This cross-check reduces dependence on a single FPGA implementation for both generation and measurement. It does not validate the engine model's assumed combustion response.

## Deliberate-fault campaign

The three builds differ in the intended spark-offset fault and its repair; each must expose an identifiable build ID. Use the same point table, reference, envelope, and thresholds for all three.

| Build | Intended behavior | Expected test outcome — not a recorded result |
| --- | --- | --- |
| Normal | Nominal spark schedule | All eligible timing points pass |
| Faulty | Add `+3°` using the specification's advance convention | Every eligible timing point fails with approximately `+3°` error |
| Repaired | Remove the injected offset | All eligible timing points pass again |

The timing limit must be sufficiently tighter than the injected fault; ±0.5° is the guide's proposed starting target. A faulty point that passes, becomes unexpectedly invalid, or is never captured does not demonstrate fault detection. Investigate the runner, measurement, convention, or point coverage before claiming the campaign succeeded.

## Idle demonstration

Use **free-run mode** so net torque updates speed and the ECU's throttle output can affect subsequent crank timing. At zero pedal, apply a declared external-load step and log speed, load, and throttle. Report the idle setpoint, initial condition, load amplitude/duration, sampling rate, inertia, air-path lag, controller configuration, dip, and recovery definition.

The guide's suggested 100 Hz logging and ±50 rpm criterion are planning values. Assumed inertia and air-path lag make this a closed-loop demonstration, not measured validation of a real engine's transient response. Injector timing does not contribute to fuel or combustion dynamics in v1.

## Report provenance

Each future run should preserve:

- Run ID, timestamp, test-point table version, operating envelope, and tolerance/stability configuration.
- Repository commit, ECU build ID, bitstream SHA-256, model-weight SHA-256, and relevant dataset/split identifiers.
- Per-point requested and observed conditions, reference values, measured statistics, event counts, verdicts, and reasons.
- Model/simulation comparisons, hardware captures, independent decoder outputs, and normal/faulty/repaired comparison tables as applicable.
- Tool versions, numeric-format assumptions, known limitations, and reproduction commands that were actually exercised.

Store genuine selected evidence when it exists. Do not add invented benchmark numbers, placeholder passing reports, or claims that unexecuted gates have passed.
