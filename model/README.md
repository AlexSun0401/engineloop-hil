# Torque surrogate - planned

Owns the float baseline, quantization, model export, and shared numerical test vectors.

**Inputs:** `rpm`, `m_cyc_mg` (air per cycle), `spark_offset_deg`. No torque-derived inputs.
**Output:** brake torque only (single output), plus an envelope decision at the plant boundary.

**Model:** a `3 → 32 → 32 → 1` MLP (about 1,200 parameters), quantization-aware training with HGQ2 (Keras 3) or QKeras (Keras 2) — pick one in P1 and pin it — then hls4ml conversion. A lookup table is a fallback only, behind the same interface.

**Assumptions to label in every report:** spark-offset response = textbook torque-ratio curve centered on stock spark (stock treated as MBT); the coefficient and source curve are recorded in `data/provenance.json`.

Planned files:

| Path | Purpose |
| --- | --- |
| `train.py` | Float baseline and QAT training from the frozen split |
| `export_hls.py` | hls4ml conversion; writes the project to the ignored `hls4ml_prj/` |
| `vectors/` | Shared input vectors in the exact integer encoding the hardware receives, plus float, quantized, and HLS golden outputs |
| `release/` | Released weights with SHA-256 (small enough to commit) |

Evidence produced here (numbering from [validation.md](../docs/validation.md)):

- **1:** float and quantized model vs held-out **measured, zero-offset** EPA points, plus a simple interpolation baseline on the same points for comparison.
- **2:** HLS C simulation vs the **float** model, ≤ 0.5 % of the declared output range, no layer overflow.
- **2b:** HLS C simulation vs the quantized Keras model (diagnostic; expected bit-exact).

Decide in P1 whether input scaling lives in a PL wrapper or is folded into the first layer, and record it in the [interface spec](../docs/interface_spec.md#model-encoding). No model, weights, results, or vectors exist yet.
