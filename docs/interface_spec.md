# Interface specification

Status: **DRAFT / not implemented**. These conventions translate the build-guide proposal into decisions to confirm. A proposed value is not a validated board setting or a frozen software interface. Resolve the `TBD` items before wiring or coding dependent modules.

## Engine and angle conventions

| Item | Proposed convention | Status |
| --- | --- | --- |
| Engine cycle | Four-stroke, four cylinders; one cycle spans 720 crank degrees | Proposed |
| Angle zero | Cylinder 1 compression top dead center, TDC | Proposed |
| Firing order | 1-3-4-2, with a firing event every 180 degrees | Proposed |
| Spark advance | Degrees before the relevant cylinder's compression TDC; positive means earlier spark | Proposed |
| Spark error | Measured advance minus expected advance; +3 degrees means 3 degrees earlier than expected | Proposed |
| Crank wheel | 60 nominal positions per revolution, 2 consecutive missing teeth | Proposed |
| Tooth edge | Rising edge marks the start of a present tooth; 50% duty on present teeth | Proposed |
| Gap-to-TDC offset | Angle of the first rising edge after the missing-tooth gap relative to TDC 1 | **TBD** |
| Cam reference | One pulse per 720 degrees; phase, width, and counting edge must be specified | **TBD** |
| Spark edge | High is dwell; falling edge is the spark | Proposed |
| Injection edges | Rising edge is injection start; pulse width measured in microseconds | Proposed |

The same angle definitions must be used by the generator, ECU decoder, FPGA capture, Python reference, and logic-analyzer decoder. Wraparound handling must be defined before comparing events near the cycle boundary.

## Physical connections

The proposed interface uses eight 3.3 V logic signals on one KR260 PMOD, with series resistors and a common ground. Exact pins and MCU timer-channel assignments have not been selected.

| Signal | Direction | KR260 package/PMOD pin | STM32 pin/timer |
| --- | --- | --- | --- |
| Crank | KR260 to STM32 | TBD | TBD |
| Cam | KR260 to STM32 | TBD | TBD |
| Spark 1 | STM32 to KR260 | TBD | TBD |
| Spark 2 | STM32 to KR260 | TBD | TBD |
| Spark 3 | STM32 to KR260 | TBD | TBD |
| Spark 4 | STM32 to KR260 | TBD | TBD |
| Injector 1 | STM32 to KR260 | TBD | TBD |
| Throttle PWM | STM32 to KR260 | TBD | TBD |
| Ground | Common reference | TBD | TBD |

Confirm the exact board variant, official pin constraints, and electrical compatibility before wiring. This is a logic-signal rig: do not connect ignition coils, physical injectors, or 12 V actuator lines.

CAN uses a USB-to-CAN adapter on KR260 Linux and a suitable CAN transceiver on the STM32 side. The guide proposes classic CAN at 500 kbit/s, terminated at the two bus ends. Hardware selection remains to be confirmed.

## Plant quantities and model inputs

| Quantity | Proposed meaning and unit | Open decision |
| --- | --- | --- |
| `rpm` | Crank revolutions per minute | Supported model envelope |
| `m_cyc_mg` | Total air mass across all cylinders per 720-degree engine cycle, in mg | Limits and normalization |
| `spark_offset_deg` | Captured spark advance minus reference spark advance at the same speed and air charge | Reference interpolation and event association |
| `torque_nm` | Engine brake torque, in N m | Output range and representation |
| `load_torque_nm` | Positive external resisting torque, in N m | Supported range |
| `throttle_duty` | Fraction from 0 to 1; scales maximum air charge at the current speed | Proposed PWM frequency: 1 kHz |
| `J` | Equivalent rotational inertia, in kg m² | Assumed value to document |
| Air-path time constant | First-order response from requested to actual simulated air charge | Assumed value to document |

For airflow in kg/s, the proposed conversion is `m_cyc_kg = airflow_kg_s / (rpm / 120)`. Per-cylinder air charge is one quarter of this quantity for the proposed four-cylinder engine; the two quantities must never share an ambiguous field name.

The dynamics model uses angular speed in rad/s for the physical update `d(omega)/dt = (T_engine - T_load) / J`; conversion to/from rpm and the event-dependent time step must be explicit. The proposed update occurs per firing/TDC event.

Model behavior outside the supported envelope must be documented separately from numerical clamping. A clamped output does not make the original point valid. Missing-spark behavior is proposed as motoring drag torque for the affected event; initialization and event timeout rules remain TBD.

## CAN message proposal

| ID | Message | Sender | Proposed period | Content |
| --- | --- | --- | --- | --- |
| `0x100` | `ECU_Status` | STM32 | 10 ms | Speed, sync state, commanded spark, throttle duty, errors, build identifier |
| `0x110` | `ECU_Debug` | STM32 | 100 ms | Lost-sync count and worst interrupt latency |
| `0x200` | `HIL_Sensors` | KR260 Linux | 10 ms | Simulated air charge and constant v1 coolant temperature |
| `0x300` | `HIL_Cmd` | KR260 Linux | On change | Pedal position and ECU mode |

These are logical message proposals, not a DBC. Field widths, scaling, signedness, byte order, DLC, identifiers, and timeout behavior are TBD. Check that the status fields fit in classic CAN's payload; split messages if necessary. The ECU's reported spark command is diagnostic data, not a substitute for measured output timing.

## FPGA/host interface proposal

An AXI-Lite register block will expose:

- Design identity and run/mode control.
- Dyno speed, load torque, and inertia configuration.
- Live speed, torque, and air-charge state.
- Direct model-vector input, start/completion handshake, and output.
- Envelope, overflow, and FIFO status.
- Captured event readout.

The guide suggests a 100 MHz PL clock and Q16.16 for selected state quantities. Register addresses, field widths, signedness, rounding, saturation, reset values, and atomic readout are **not frozen**. Define a separate register map before implementation; keep model-output data separate from completion flags unless their packing is explicitly specified.

An event record is proposed to include channel, edge polarity, crank angle, and a 64-bit timestamp. Timestamp units, angle resolution, FIFO depth, overflow policy, and coherent multiword reads remain TBD.

## Proposed verification rules

| Rule | Proposed target | Status |
| --- | --- | --- |
| Spark timing tolerance | +/-0.5 crank degrees | Confirm before testing |
| Injected fault | +3 degrees of spark advance, with all other behavior unchanged | Proposed |
| FPGA versus independent timing measurement | Approximately 0.1 degrees agreement | Confirm measurement budget |
| Settling | Rolling variation of speed and commanded spark below fixed limits | Window and thresholds TBD |
| Torque accuracy | Absolute tolerance at low torque, relative tolerance above a breakpoint | All values TBD |
| Measured-data envelope | Defined from retained EPA steady-state points | Bounds TBD after data inspection |
| Loss of synchronization | Stop spark/injection outputs and restart synchronization | Timeout and recovery details TBD |

`PASS` means a valid, settled point meets the specified timing/error and missing-edge rules. `FAIL` means a valid point violates those rules. `INVALID` means the point lacks a usable reference, is outside the envelope, fails to settle, or lacks full ECU synchronization. Invalid points must not inflate the reported pass rate.

## Decisions required before implementation

1. Select the STM32 board, CAN hardware, physical pin map, and timer channels.
2. Freeze gap/cam phase, cylinder-event association, dwell, injection timing, and sync timeouts.
3. Inspect source data and set the model envelope, normalization, torque tolerances, and held-out groups.
4. Choose and document spark-efficiency coefficient, air-path lag, inertia, and initialization behavior.
5. Freeze the CAN DBC and register/number formats, including FIFO and completion semantics.
6. Confirm tool versions and board-support compatibility, then record exact tested versions with the first implementation.

See [system architecture](architecture.md) for the intended component and validation boundaries.
