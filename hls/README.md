# HLS integration - planned

Reserved for integrating the generated torque-surrogate IP into the PL design.

Model generation and export live in [`../model/`](../model/README.md). Generated projects go under `generated/` or `torque_mlp/` (both ignored by Git). Planned tools: Vitis HLS 2024.1 and hls4ml 1.3.0 with the Vitis backend (see [toolchain_and_bench.md](../docs/toolchain_and_bench.md)).

When generation is implemented, record here: exact tool versions, input/output fixed-point types, reuse factor, I/O handshake (`ap_ctrl_hs` or streaming), latency in clocks at 100 MHz, DSP/LUT/FF/BRAM use, and the SHA-256 of the exported weights.

Budget from the plan: DSP below 20 % of the device. Latency is not critical — one inference per 180° firing event leaves more than 4 ms at 7,000 rpm.

No HLS project, C simulation, synthesis result, or exported IP exists yet.
