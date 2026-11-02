# Design sources

The repository outline is based on the **KR260 Engine HIL: Build Guide** and the agreed plan revision 2, both supplied by the project owner and dated November 1, 2026. They are plans, not evidence of an existing implementation. Planned tool and hardware choices are collected in [toolchain_and_bench.md](toolchain_and_bench.md).

The following links were extracted from that guide. They have not been independently reviewed or revalidated for the initial scaffold; verify their current requirements and applicability when implementing the relevant phase.

## Public engine data and modeling

- [EPA engine-data source linked in the guide](https://www.epa.gov/node/164863)
- [EPA: Combining Data into Complete Engine ALPHA Maps](https://epa.gov/vehicle-and-fuel-emissions-testing/combining-data-complete-engine-alpha-maps)
- [Benchmarking a 2016 Honda Civic 1.5 L L15B7 turbo engine](https://pmc.ncbi.nlm.nih.gov/articles/PMC6604863)
- [MathWorks: SI Engine Torque Structure Model](https://www.mathworks.com/help/autoblks/ug/si-engine-torque-structure-model.html)

## Model conversion

- [hls4ml: Keras and quantized variants](https://fastmachinelearning.org/hls4ml/frontend/keras.html)
- [hls4ml: Vitis backend](https://fastmachinelearning.org/hls4ml/backend/vitis.html)

## KR260 implementation references

- [AMD Kria: generating custom firmware](https://xilinx.github.io/kria-apps-docs/kd240/build/html/docs/generating_custom_firmware.html)
- [AMD Kria: application deployment and CAN host setup](https://xilinx.github.io/kria-apps-docs/kd240/foc-motor-ctrl/0_5/build/html/docs/app_deployment.html)
- [AMD Kria: known issues](https://xilinx.github.io/kria-apps-docs/kd240/foc-motor-ctrl/0_5/build/html/docs/known_issues.html)
- [AMD: Vivado product and licensing information](https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/vivado/vivado-buy.html)
- [Xilinx: kria-vitis-platforms](https://github.com/Xilinx/kria-vitis-platforms)

Some Kria documentation above targets KD240. Confirm KR260 applicability rather than copying board-specific settings. Hardware choices, pins, exact numerical formats, licenses, software versions, and compatibility remain implementation decisions.

## Data provenance to capture in P0

Record the exact downloaded package URL, download date, SHA-256, usage terms, selected columns, units, source-row IDs, processing-script revision, and held-out group list. The source curve and chosen coefficient for spark-efficiency augmentation must also be recorded and explicitly labeled as assumptions.
