# Incremental development

This repository starts with design documents. Keep changes small enough to review and reproduce as implementation is added.

## Pick one task

Use an unchecked item in [docs/roadmap.md](docs/roadmap.md). For a larger change, use the implementation-task issue template to record the phase, scope, acceptance criterion, and evidence required. Hardware-independent STM32 planning may overlap with PL development, but a phase is complete only after its gate is demonstrated.

## Make a change

1. Create a descriptive branch such as `p0/interface-conventions` or `p2/crank-generator`.
2. Implement the bounded task in its module directory.
3. Update any affected interface, units, assumptions, or architecture documents in the same change.
4. Run the checks appropriate to the change and record their result. If hardware was unavailable, say so and leave hardware validation pending.
5. Add a dated entry to [docs/progress.md](docs/progress.md), then update only the roadmap items supported by the change.

## Describe validation accurately

- A documentation review is not a model, simulation, or hardware test.
- A passing simulation is not an on-board measurement.
- Report measured-data accuracy separately from behavior derived from synthetic spark offsets.
- Keep out-of-envelope and unsettled cases visible as INVALID.
- Promote a proposed threshold to an agreed requirement in the interface specification before using it to claim a pass.
- Do not commit invented measurements or reports populated with demonstration numbers.

## Keep results reproducible

Commit source, data-fetch/processing scripts, interface definitions, small reference vectors, and concise evidence summaries. For real runs, record the source commit, firmware build ID, model hash, bitstream hash, tool versions, input IDs, and timestamps. Large generated outputs belong outside normal source history; document how to reproduce or retrieve them.

Raw public datasets must retain their source URL, checksum, units, and usage terms. Do not include employer data, credentials, or machine-specific configuration. Review new data and result files explicitly; `.gitignore` is not a privacy boundary.

## Suggested commit messages

- `docs: define engine signal conventions`
- `data: add reproducible EPA table processing`
- `fpga: implement crank generator and timing simulation`
- `fw: add crank synchronization state machine`
- `host: report per-point timing verdicts`

The initial scaffold has no runnable test suite. Add meaningful simulation, numerical, or hardware checks alongside the corresponding implementation; do not add empty passing tests.
