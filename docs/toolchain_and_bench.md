# Toolchain and bench

Status: **planned choices** from the agreed project plan (revision 2, 2026-11-01). Nothing here has been installed or tested in this repository yet. When a tool is first used, replace "Planned" with the exact installed version and the date, in the same commit as the work that used it.

## Software

| Purpose | Planned choice | Status | Notes |
| --- | --- | --- | --- |
| FPGA design and HLS | Vivado / Vitis HLS 2024.1 | Planned | Chosen over 2026.1 because the free tier of the newer release limits ILA and simulation (per plan) |
| Model training | Python 3, Keras + HGQ2 (Keras 3) **or** QKeras (Keras 2) | Planned | Pick one in P1 and pin it; the two stacks do not mix |
| Model → HLS | hls4ml 1.3.0 | Planned | Pin the exact installed version; record the backend (Vitis) |
| Board OS | Kria Ubuntu 24.04 on the KR260 | Planned | Confirm boot firmware and kernel version on first boot |
| PL loading | Kria app: `.bit.bin` + `.dtbo` + `shell.json`, loaded with `xmutil loadapp` | Planned | One bitstream for v1 |
| CAN on Linux | SocketCAN + python-can + cantools | Planned | `gs_usb` driver for the adapter; check `modinfo gs_usb` on the Kria kernel |
| STM32 firmware | STM32CubeIDE / CubeMX (HAL/LL) | Planned | Record CubeIDE and firmware-package versions in `fw/` |
| Flashing from the KR260 | OpenOCD or stlink-tools (packaged for arm64 Ubuntu) | Planned | Check before relying on STM32CubeProgrammer, which may not ship an Arm64 Linux build |
| Logic analyzer | sigrok (`sigrok-cli`, PulseView) with the `fx2lafw` driver | Planned | Separate Python decoder for the independent timing check |
| Repository checks | `tools/check_md_links.py`, `tools/check_dbc.py` (cantools) | **Working** | Run locally and in GitHub Actions |

## Hardware

| Item | Planned choice | Notes |
| --- | --- | --- |
| Plant and test host | AMD Kria KR260 | PMOD at 3.3 V; confirm the exact connector and pins from official constraints |
| ECU under test | STM32 Nucleo-G474RE (recommended) or Nucleo-F446RE | G474: 170 MHz, FDCAN usable in classic mode, more timers. F446: bxCAN |
| CAN transceiver (ECU side) | SN65HVD230 module | 3.3 V transceiver; check that the module's termination matches the bus plan |
| CAN adapter (KR260 side) | USB-to-CAN adapter supported by `gs_usb` (candleLight-type) | Pmod CAN is a later option |
| Bus | Twisted pair, 120 Ω at each end | Classic CAN, 500 kbit/s |
| Logic analyzer | 8-channel, 24 MHz (fx2lafw class) | If samples drop at 24 MHz with 8 channels, 12 MHz still gives about 0.004° at 7,000 rpm |
| Wiring | PMOD breakout, series resistors (e.g. 100 Ω), common ground | No PMOD VCC to the Nucleo 3V3 |

## First bench smoke tests (recommended during P0)

These de-risk P2, the riskiest phase, before any engine logic exists. Each takes an evening or two and produces a short progress entry.

1. **PL path:** a Vivado 2024.1 design with one AXI-Lite register (`ID`, `SCRATCH`) and one PMOD output toggling at a known rate, packaged as a Kria app, loaded with `xmutil`, register read and written from Linux, toggle frequency confirmed on the logic analyzer.
2. **CAN path:** the Nucleo sends one frame per second; `candump can0` on the KR260 shows it; the KR260 sends a frame back and the Nucleo echoes it.
3. **Flash path:** flash the Nucleo from the KR260 with OpenOCD or stlink-tools and read its build hash over CAN.

If any of these fails, the fix is a toolchain or board-support problem, which is much cheaper to find now than in week 6.

## Recording versions

For each run, the run manifest records: OS image and kernel, Vivado/HLS version, hls4ml and Keras/HGQ2/QKeras versions, CubeIDE and firmware-package versions, python-can/cantools versions, and the logic-analyzer firmware/driver. See [validation.md](validation.md#report-provenance).
