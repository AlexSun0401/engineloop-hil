# Data pipeline - planned

Owns reproducible retrieval and processing of public engine data.

**Inputs:** the EPA test data package for the 2016 Honda 1.5 L L15B7 (speed, torque, airflow, spark) and the related ALPHA map (motoring drag; fallback source), subject to P0 schema and usage-term checks.

**Outputs:**

| File | Content |
| --- | --- |
| `processed/train_table.csv` | `rpm`, `m_cyc_mg`, `spark_stock_deg`, `torque_nm`, `group_id`, `source_row`, `is_synthetic` |
| `processed/split.json` | Frozen train / hold-out group lists |
| `processed/spark_table.json` | Gridded reference spark: breakpoints, values (deg BTDC), gridding method and parameters, source rows, SHA-256. Single source for firmware, PL LUT, and the Python reference (see [interface spec](../docs/interface_spec.md#spark-reference-table-single-source-of-truth)) |
| `processed/motoring_drag.json` | Drag torque vs rpm from the ALPHA map |
| `provenance.json` (committed) | Source URLs, download dates, SHA-256 of raw files, usage terms, script revision |

Rules:

- Record units first, and whether airflow/air charge refers to the whole engine or one cylinder. `m_cyc_mg` is the **total** of all cylinders per 720° cycle.
- Keep only the stoichiometric steady-state region for v1; record the selection rule.
- Never use power, BMEP, or efficiency columns as model inputs (they leak the torque target).
- Synthetic spark-offset rows are flagged `is_synthetic = 1` and share their measured source point's `group_id`.
- Employer data never enters this directory or the repository.

Planned entry points: `fetch_epa.py` (download + checksum check) and `build_table.py`. They do not exist yet. `raw/` and `processed/` are ignored by Git; commit scripts, `provenance.json`, and small reviewed CSV fixtures.

See [P0](../docs/roadmap.md#p0--define-the-contract-and-build-the-data-baseline).
