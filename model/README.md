# Torque surrogate - planned

Owns the float baseline, quantization, model export, and shared numerical test vectors.

**Inputs:** speed, air charge per engine cycle, and spark offset relative to the reference timing surface. Exact normalization and fixed-point formats must be frozen in the interface specification.

**Output:** estimated brake torque plus an explicit validity/envelope decision at the plant boundary.

Proposed model: a `3 → 32 → 32 → 1` MLP, then quantization-aware training and hls4ml conversion. A speed/air-charge lookup table plus a separate spark-efficiency table is the fallback under the same contract.

Future files: `train.py`, `export_hls.py`, and `vectors/`. No model, weights, training results, or reference vectors exist yet. The shared vectors must connect float, quantized/HLS, RTL simulation, and on-board checks.

Score base torque accuracy on held-out measured zero-offset rows. Report assumed spark-offset behavior separately. See the [validation plan](../docs/validation.md).
