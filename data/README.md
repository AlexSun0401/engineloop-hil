# Data pipeline - planned

Owns reproducible retrieval and processing of public engine data.

**Planned inputs:** EPA's 2016 Honda L15B7 engine test data and related ALPHA map, subject to P0 schema and usage-term checks.

**Planned outputs:** a clean steady-state table with `rpm`, `m_cyc_mg`, `spark_stock_deg`, `torque_nm`, `group_id`, and `source_row`; provenance metadata; and a saved train/test group split.

Start by recording units and whether air charge refers to the whole engine or one cylinder. Keep augmented spark-offset rows in their measured source point's split group. Do not use power, BMEP, or efficiency columns that would leak the torque target into model inputs.

Future entry points: `fetch_epa.py` and `build_table.py`. They do not exist yet. Raw and processed datasets are ignored by default; commit processing source and small reviewed reference fixtures when available.

See [P0](../docs/roadmap.md) and the [interface draft](../docs/interface_spec.md).
