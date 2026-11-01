# Progress log

Record completed work here. The roadmap tracks remaining work; this log records changes and evidence.

## 2026-11-01 - EngineLoop English upload package

**Completed:** adopted the name **EngineLoop — FPGA-Based Engine HIL Testbench**, prepared an English-only repository, and added initial-upload and future-update instructions. The upload package places repository files directly at its root and excludes local Git history and temporary outputs.

**Validation:** documentation and packaging checks only. Implementation milestones P0-P4 remain not started; no model, simulation, firmware, or hardware result is claimed.

**Next:** upload the extracted files to the owner's GitHub repository and begin P0.

## 2026-11-01 - Initial architecture and repository scaffold

**Completed:** documented the system purpose, PS/PL/STM32 responsibilities, feedback loop, module boundaries, proposed interfaces, phased roadmap, and validation strategy. Added project introductions and a workflow for incremental updates.

**Validation:** documentation-only change. No model training, FPGA simulation/synthesis, firmware build, or hardware measurements have been performed. P0-P4 implementation remains not started.

**Next:** resolve P0 conventions and acceptance thresholds, verify dataset fields and units, and create reproducible public-data processing scripts.

## Entry format for future work

```text
YYYY-MM-DD - Short description
Phase/task:
Completed:
Evidence and checks actually run:
Limitations or checks still pending:
Next:
```
