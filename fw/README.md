# STM32 ECU firmware - planned

Owns the simplified controller under test. The board family and final peripheral assignment remain to be confirmed; the source guide suggests a Nucleo board with a CAN controller and a separate CAN transceiver.

Planned modules:

- Crank/cam decoding and synchronization state machine.
- Timer-driven spark scheduling for four cylinders.
- Injector-1 timing output, used for timing validation only in v1.
- Pedal mapping, throttle PWM, and PI idle regulation.
- CAN sensor input, commands, status, and build identity.
- A controlled build-time spark offset for normal / faulty / fixed regression.

Only full synchronization should enable spark and injection. Signal-loss behavior and re-synchronization must be tested explicitly.

No Cube project, source, binary, or firmware test currently exists. Add the first project with its tool version, reproducible build instructions, and selected pin/peripheral assignments.
