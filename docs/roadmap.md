# Implementation roadmap

**Status:** documentation baseline only. No engine model, FPGA design, ECU firmware, automated test runner, or hardware result is implemented or verified yet.

Work proceeds through P0–P4. Complete a phase's gate and record its evidence before claiming that phase is complete. Checkboxes track implementation, not intentions. Architecture and draft interfaces live in [architecture.md](architecture.md), [interface_spec.md](interface_spec.md), and [register_map.md](register_map.md); evidence rules live in [validation.md](validation.md).

| Phase | Deliverable | Estimate at 10–15 h/week | Gate | Status |
| --- | --- | --- | --- | --- |
| P0 | Interface spec, EPA training table, float baseline, bench smoke tests | 1–2 weeks | A | Not started |
| P1 | Single-output QAT MLP and hls4ml C simulation | 1–2 weeks | B | Not started |
| P2 | PL bring-up: one bitstream loaded as a Kria app | 3–4 weeks | C (riskiest) | Not started |
| P3 | STM32 firmware, CAN, `+3°` build flag | 2–3 weeks | D | Not started |
| P4 | Closed loop and regression report | 2–3 weeks | E | Not started |

Total: about 9–14 weeks. Hardware-independent STM32 work may overlap with P2, but a phase is complete only after its gate is demonstrated.

## P0 — Define the contract and build the data baseline

- [ ] Accept or change the proposed angle zero/sign, gap and cam phase, signal edges, dwell, SOI, and firing order; mark them *Frozen* in the spec.
- [ ] Select the STM32 board, CAN adapter, and physical pin map; record the hardware in [toolchain_and_bench.md](toolchain_and_bench.md).
- [ ] Review and freeze the draft DBC (`interfaces/engineloop.dbc`) and the register map draft (formats may stay open until P1/P2).
- [ ] **Bench smoke tests** (in parallel with the data work; see [toolchain_and_bench.md](toolchain_and_bench.md#first-bench-smoke-tests-recommended-during-p0)): PL register read/write via a Kria app, Nucleo ↔ KR260 CAN frame, flashing from the KR260.
- [ ] Add scripts to obtain the EPA L15B7 test package and ALPHA map; record source URLs, download dates, and SHA-256 without committing raw packages.
- [ ] Build a traceable table of stoichiometric steady-state speed, air charge, stock spark, and measured torque, retaining source-row identifiers.
- [ ] Generate `spark_table.json` (grid, gridding method, source rows, SHA-256) from the measured spark data.
- [ ] Add labelled synthetic spark-offset rows from the documented torque-ratio assumption; keep each row in its source point's group.
- [ ] Freeze a grouped train/hold-out split and the shared input vectors.
- [ ] Set the envelope and torque tolerance before scoring; train and evaluate the float baseline on held-out **measured, zero-offset** rows; report a simple interpolation baseline on the same rows.

**Gate A:** a versioned dataset, split, spark table, and interface contract exist, and the float baseline meets the agreed torque criterion (proposed: ≥ 95 % of held-out points within tolerance, none beyond 2×). The three smoke tests have passed or their blockers are recorded. If the envelope changes, version it and repeat the evaluation explicitly.

## P1 — Make the torque surrogate hardware-ready

- [ ] Pin the training stack (HGQ2/Keras 3 or QKeras/Keras 2) and hls4ml version.
- [ ] Train a single-output quantization-aware MLP and rerun the measured-point accuracy check (evidence 1).
- [ ] Convert with hls4ml; document input/output fixed-point formats and where input scaling happens; check every layer for clipping or overflow.
- [ ] Compare HLS C simulation with the **float** model on the shared vectors (evidence 2) and with the quantized Keras model (evidence 2b); preserve raw integer golden outputs.
- [ ] Record synthesis latency and DSP/LUT/BRAM utilization.
- [ ] If the NN path stalls, switch to the fallback lookup table behind the same interface and record why.

**Gate B:** quantized measured-point accuracy is still acceptable; HLS vs float ≤ 0.5 % of the declared output range; no unaccounted overflow; latency and resources recorded (guide budget: DSP below 20 % of the device).

## P2 — Bring up the KR260 FPGA in small steps

Trigger and capture path first (this is what P3 needs):

- [ ] Implement and simulate `crank_gen` (60-2 + cam per the spec), checking tooth geometry, gap position, and cam phase in the testbench.
- [ ] Implement and simulate `edge_capture` with synchronizer latency compensation, the event FIFO, overflow behavior, and coherent timestamp reads.
- [ ] Implement `pwm_meas` and `hil_regs` per [register_map.md](register_map.md).
- [ ] Confirm board pin constraints against the chosen PMOD before wiring.
- [ ] Package the bitstream as a Kria app (`.bit.bin`, `.dtbo`, `shell.json`) and document the load procedure.
- [ ] Read `ID`/`BUILD_HASH` through the registers before enabling signal generation.
- [ ] Verify crank/cam timing with the logic analyzer at 1,000, 3,000, and 7,000 rpm.
- [ ] Loop a generated signal into a capture input (STM32 disconnected) to verify angle and time capture.

Plant path:

- [ ] Integrate `airpath` (with dyno override), `spark_ref_lut` (host-loaded), the hls4ml `torque_core`, and `dynamics`.
- [ ] Run the shared vectors on the board and compare raw outputs with HLS golden outputs (evidence 3).

**Gate C:** independent captures confirm trigger timing at the checkpoints; on-board inference is bit-exact to HLS C simulation for the shared vectors; capture behavior is demonstrated. No physical timing or latency claim is made from synthesis alone.

## P3 — Implement the STM32 ECU

- [ ] Decode crank/cam into a documented synchronization state machine (`NO_SYNC → GAP_FOUND → FULL_SYNC`, `SYNC_LOST`); enable outputs only in full synchronization.
- [ ] Schedule four spark outputs and one injector output with hardware timer output-compare.
- [ ] Compile the spark table from the generated header; implement the specified bilinear interpolation in C.
- [ ] Implement the DBC frames, timeouts, and `ECU_Info` (build hash, variant, dirty flag, trim, table hash).
- [ ] Implement pedal-to-throttle, the ECU modes, and a PI idle controller with anti-windup.
- [ ] Build normal, `+3°` fault, and fixed variants from one source tree with a build flag; each reports its own variant and hash.
- [ ] Verify synchronization through the 600–7,000 rpm ramp.
- [ ] Disconnect the crank signal, check output shutdown, reconnect, and measure resynchronization.

**Gate D:** zero unexpected sync losses over the agreed ramp; the expected firing sequence and timing are observed; outputs stop on sync loss; resynchronization within two revolutions after reconnection (proposed). Injection remains a timing test and does not drive a fuel model.

## P4 — Prove the regression workflow

- [ ] Define a versioned DOE point table (proposed: 30–60 in-envelope points, on and between measured EPA points, plus explicit out-of-envelope cases).
- [ ] Implement build-identity check, point setup, settling, capture, independent expected-value calculation, verdicts, and machine-readable logs.
- [ ] Cross-check about five points per run with the logic analyzer and a separate decoder.
- [ ] Automate flashing and running the same table against normal, faulty, and fixed firmware.
- [ ] Generate comparable reports with point-level evidence and the run manifest.
- [ ] In free-run mode, demonstrate idle control under a load step with the declared assumptions.
- [ ] Publish one tagged evidence set and a short bench demonstration once real measurements exist.

**Gate E:** normal and fixed builds pass every eligible timing point; the faulty build fails every eligible point with about the injected signed offset; invalid cases are reported separately. One command performs flashing, sweep, and reporting. Idle target ±50 rpm under the defined load step is a demonstration criterion only.

## Stretch (after Gate E)

- Exhaust-temperature and boost model outputs.
- Tooth-loss and misfire fault injection in `crank_gen`.
- XCP measurement/calibration via pyXCP.
- rusEFI as a second device under test.
- R5F real-time supervisor on the KR260.

## How to update this roadmap

For each completed task, add its implementation and a short explanation of how it was checked, tick only the relevant boxes, and link the supporting report or capture. Keep unimplemented work visibly unchecked. Record changes to interfaces, assumptions, test points, or thresholds alongside the code that depends on them. Add runnable setup and reproduction commands only after they have been exercised.
