# Incremental development

Keep changes small enough to review and reproduce as implementation is added.

## Pick one task

Use an unchecked item in [docs/roadmap.md](docs/roadmap.md). For a larger change, open an issue with the **Implementation task** template to record the phase, scope, acceptance criterion, and evidence required before starting. Hardware-independent STM32 work may overlap with PL development, but a phase is complete only after its gate is demonstrated.

## Make a change

1. Create a descriptive branch such as `p0/interface-conventions` or `p2/crank-generator`.
2. Implement the bounded task in its module directory.
3. Update any affected contract — [interface spec](docs/interface_spec.md), [register map](docs/register_map.md), [DBC](interfaces/engineloop.dbc), units, assumptions, architecture — in the same change.
4. Run the checks appropriate to the change and record their result. Always run `python tools/check_md_links.py`. If hardware was unavailable, say so and leave hardware validation pending.
5. Add a dated entry to [docs/progress.md](docs/progress.md), then tick only the roadmap items supported by the change.

## Describe validation accurately

- A documentation review is not a model, simulation, or hardware test.
- A passing simulation is not an on-board measurement.
- Report measured-data accuracy separately from behavior derived from synthetic spark offsets.
- Keep out-of-envelope and unsettled cases visible as INVALID.
- Promote a *Proposed* threshold to *Frozen* in the interface specification before using it to claim a pass.
- Do not commit invented measurements or reports populated with demonstration numbers.

## Keep results reproducible

Commit source, data-fetch/processing scripts, interface definitions, small reference vectors, and concise evidence summaries. For real runs, record the source commit, firmware build ID, model hash, spark-table hash, bitstream hash, tool versions, input IDs, and timestamps. Large generated outputs go to GitHub Releases; document how to reproduce or retrieve them.

## Data rule

- Raw public datasets keep their source URL, download date, checksum, units, and usage terms.
- **Employer data never enters this repository**: no workbooks, channel names, threshold values, or anything fitted from them, unless the owner has written permission. Employer practice may inform *method only* (DOE flow, tolerance structure, INVALID vs FAIL, A/B build discipline), described in general terms.
- No credentials or machine-specific configuration.
- Review every new data and result file explicitly; `.gitignore` reduces accidents but is not a privacy boundary.

## Suggested commit messages

- `docs: freeze crank and cam phase conventions`
- `data: add reproducible EPA table processing`
- `fpga: implement crank generator and timing simulation`
- `fw: add crank synchronization state machine`
- `host: report per-point timing verdicts`

Add meaningful simulation, numerical, or hardware checks alongside each implementation; do not add empty passing tests.
