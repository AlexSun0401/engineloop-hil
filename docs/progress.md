# Progress log

Record completed work here, newest first. The roadmap tracks remaining work; this log records changes and evidence.

## 2026-11-01 - Repository review against plan revision 2

**Phase/task:** pre-P0 documentation review.

**Completed:**

- Restored repository files that the first web upload dropped: `.gitignore`, `.gitattributes`, `.github/` issue and PR templates.
- Added CI (`.github/workflows/checks.yml`) with two real checks: relative Markdown links (`tools/check_md_links.py`) and the CAN DBC (`tools/check_dbc.py`).
- Added a draft DBC (`interfaces/engineloop.dbc`). The previously proposed single status frame needed about 96 bits and did not fit classic CAN; build provenance moved to a new `ECU_Info` frame (build hash, variant, dirty flag, trim, spark-table hash).
- Added [register_map.md](register_map.md) (draft) and [toolchain_and_bench.md](toolchain_and_bench.md) (planned versions from the plan, bench list, three smoke tests).
- Interface spec: proposed gap/cam phase, dwell, SOI angle, a 720°-wrapped advance formula with a phase-association check, capture-latency compensation, dyno air-charge override, a single shared `spark_table.json` with specified bilinear interpolation, the rule that the Python reference uses the CAN-quantized air charge, ECU modes and timeouts, settling and torque-tolerance proposals.
- Architecture: added `spark_ref_lut`, shared-artifact flow, P2 bring-up order (trigger/capture first), and the labelled assumptions (stock spark treated as MBT, implicit boost/cam schedules, no turbo dynamics).
- Validation: aligned evidence numbering with the plan; evidence 2 is now HLS vs **float** (as in the plan) with HLS vs quantized Keras as a diagnostic; added DOE table schema, build-identity check, capture-integrity INVALID reasons, and manifest fields.
- Roadmap: phase estimates, bench smoke tests in P0, stretch goals.
- Removed stale "initial upload" instructions; `repository_setup.md` now describes the ongoing workflow.

**Evidence and checks actually run:** `python tools/check_md_links.py` (all relative links resolve) and `python tools/check_dbc.py interfaces/engineloop.dbc` with cantools 45.1.2 (5 frames parse in strict mode, all ≤ 64 bits); sample frames encoded and decoded round-trip. The GitHub Actions workflow itself runs after upload.

**Limitations:** documentation only. All *Proposed* values still need owner review; no model, simulation, firmware, or hardware result exists. P0–P4 remain not started.

**Next:** accept/change the proposed conventions, run the three bench smoke tests, start the EPA data scripts.

## 2026-11-01 - EngineLoop English upload package

**Completed:** adopted the name **EngineLoop — FPGA-Based Engine HIL Testbench**, prepared an English-only repository, and added upload and update instructions.

**Validation:** documentation and packaging checks only. No model, simulation, firmware, or hardware result is claimed.

**Next:** upload to GitHub and begin P0. (Done 2026-11-01; hidden configuration files were not included in that upload and were restored in the review entry above.)

## 2026-11-01 - Initial architecture and repository scaffold

**Completed:** documented the system purpose, PS/PL/STM32 responsibilities, feedback loop, module boundaries, proposed interfaces, phased roadmap, and validation strategy.

**Validation:** documentation-only change.

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
