# Implementation roadmap

**Status:** documentation baseline only. No engine model, FPGA design, ECU firmware, automated test runner, or hardware result is implemented or verified in this initial repository.

Work proceeds through P0–P4. Complete a phase's gate and record its evidence before claiming that phase is complete. The checkboxes below track implementation, not intentions. Architecture and draft interfaces live in [architecture.md](architecture.md) and [interface_spec.md](interface_spec.md); evidence rules live in [validation.md](validation.md).

| Phase | Deliverable | Current status |
| --- | --- | --- |
| P0 | Agreed interfaces, reproducible training table, float baseline | Not started |
| P1 | Quantized torque surrogate and HLS reference | Not started |
| P2 | KR260 FPGA signal generation, capture, plant, and register access | Not started |
| P3 | STM32 trigger decoding, output scheduling, idle control, and CAN | Not started |
| P4 | Automated sweeps, fault regression, reports, and idle demonstration | Not started |

## P0 — Define the contract and build the data baseline

- [ ] Finalize angle zero/sign, trigger-wheel phase, signal edges, firing order, physical pin assignments, units, and model normalization.
- [ ] Define the supported operating envelope, steady-state rule, timing limits, and torque-error limits before final evaluation.
- [ ] Record chosen hardware and exact tool versions after checking the available bench and toolchain.
- [ ] Add scripts to obtain the public EPA Honda L15B7 test and ALPHA map packages; record source URLs and checksums without committing raw packages.
- [ ] Build a traceable table of stoichiometric steady-state speed, air charge, stock spark, and measured torque; retain source-row identifiers.
- [ ] Add explicitly labeled synthetic spark-offset rows using a documented efficiency assumption; keep each row in its source point's group.
- [ ] Freeze a grouped train/hold-out split and reusable float/fixed-point test vectors.
- [ ] Train and evaluate a float torque baseline on held-out **measured, zero-offset** rows.

**Gate A:** a versioned dataset, split, interface contract, and measured-point score satisfy the agreed torque criterion. The guide proposes at least 95% of points within tolerance and none beyond twice the tolerance; these are targets, not results. If the envelope changes, version it and repeat evaluation explicitly.

## P1 — Make the torque surrogate hardware-ready

- [ ] Train a quantized model and rerun the measured-point accuracy check.
- [ ] Convert the model to HLS, document input/output fixed-point formats, and check layer ranges for clipping or overflow.
- [ ] Compare HLS C simulation with the software quantized-model reference on the shared vectors; preserve raw integer golden outputs.
- [ ] Record synthesis latency and DSP/LUT/BRAM utilization.
- [ ] If the neural-network conversion path stalls, document a switch to the planned speed/air-charge lookup table plus spark-efficiency table, retaining the same validation interfaces.

**Gate B:** measured-point accuracy remains acceptable; maximum software-to-HLS discrepancy meets the proposed 0.5% of declared output-range target; no unaccounted overflow occurs; latency and resource use are recorded. The guide's proposed DSP budget is below 20% of the device total.

## P2 — Bring up the KR260 FPGA in small steps

- [ ] Implement and simulate the crank/cam generator, edge capture, PWM measurement, air-path approximation, torque core, dynamics, and AXI-Lite registers.
- [ ] Verify signal conventions, capture/FIFO behavior, reset behavior, and shared-vector numerical equivalence in simulation.
- [ ] Confirm board pin constraints against the chosen connector before wiring.
- [ ] Build the FPGA image and device-tree overlay; document a repeatable load procedure.
- [ ] Read a build identifier through the register interface before enabling signal generation.
- [ ] Verify crank/cam timing independently at the proposed 1,000, 3,000, and 7,000 rpm checkpoints.
- [ ] Run the shared vectors on the board and compare raw outputs with HLS golden outputs.
- [ ] Loop a generated signal into a capture input to verify angle/time capture.

**Gate C:** independent captures confirm trigger timing at the selected checkpoints; on-board inference is bit-exact to HLS C simulation for the shared vectors; capture behavior is demonstrated. No physical timing or latency claim is made from synthesis alone.

## P3 — Implement the STM32 ECU

- [ ] Decode crank/cam signals into a documented synchronization state machine; enable outputs only in full synchronization.
- [ ] Schedule four spark outputs and one injector output with hardware timers.
- [ ] Generate a spark table from the selected EPA data; implement ECU interpolation in C.
- [ ] Receive simulated air charge and pedal commands over CAN and transmit build/status information.
- [ ] Implement pedal-to-throttle behavior and a PI idle controller with anti-windup.
- [ ] Build normal, deliberate `+3°` spark-offset, and repaired firmware variants with identifiable provenance.
- [ ] Verify synchronization through the proposed 600–7,000 rpm ramp.
- [ ] Disconnect the crank signal, check output shutdown, reconnect, and measure resynchronization.

**Gate D:** zero unexpected sync losses over the agreed ramp; the expected firing sequence and timing are observed; outputs stop on sync loss. The guide proposes resynchronization within two revolutions after reconnection. Injection remains a timing test and does not drive a fuel model.

## P4 — Prove the regression workflow

- [ ] Define a versioned DOE point table: an initial 30–60-point in-envelope sweep plus explicit out-of-envelope cases is the guide's suggested scope.
- [ ] Implement point setup, settling, capture, independent expected-value calculation, verdicts, and machine-readable logging.
- [ ] Cross-check about five selected points per run with a logic analyzer using a separate decoder.
- [ ] Automate flashing and running the same point table against normal, faulty, and repaired firmware.
- [ ] Generate comparable reports containing point-level evidence and build/data provenance.
- [ ] In free-run mode, demonstrate idle control under a load step; report dip and recovery using declared assumed inertia and air-path lag.
- [ ] Publish one reproducible tagged evidence set and a short bench demonstration once measurements exist.

**Gate E:** normal and repaired builds pass every eligible timing point; the faulty build fails every eligible point with approximately the injected signed offset; invalid cases are reported separately. One command performs flashing, sweep, and reporting. The proposed idle target is ±50 rpm under the defined load-step test; this is a demonstration criterion, not validated real-engine transient accuracy.

## How to update this repository

For each completed task, add its implementation and a short explanation of how it was checked, update only the relevant checkboxes, and link the supporting report or capture. Keep unimplemented work visibly unchecked. Record changes to interfaces, assumptions, test points, or thresholds alongside the code that depends on them. Add runnable setup and reproduction commands only after they have been exercised.
