# Linux test orchestration - planned

Owns the Python side running on the KR260 ARM/Linux system.

Responsibilities:

1. Load the PL app and check `ID`, `VERSION`, and `BUILD_HASH` ([register_map.md](../docs/register_map.md)); load the spark LUT.
2. Exchange CAN frames with the ECU through SocketCAN (`python-can`) and decode them with `cantools` from [`interfaces/engineloop.dbc`](../interfaces/engineloop.dbc).
3. Flash a selected firmware build and verify `ECU_Info` (hash, variant, dirty flag, spark-table hash) before any sweep.
4. Run a DOE point table: envelope check, settle, capture, flag.
5. Compute expected timing independently of the ECU code, from `spark_table.json` and the CAN-quantized air charge.
6. Assign PASS / FAIL / INVALID with reasons and write a report plus a machine-readable run manifest.
7. Decode selected logic-analyzer captures independently of the PL angle capture.

Planned entry points: `orchestrator.py`, `report.py`, `la_check.py`. None exists yet.

`doe/` holds reviewed, versioned point tables; the column schema is in [validation.md](../docs/validation.md#doe-point-table). Reports go to `out/` (ignored); selected evidence is attached to tagged releases.

CAN bring-up (planned, to be confirmed on the board):

```bash
sudo ip link set can0 up type can bitrate 500000
candump can0
```

See the [validation plan](../docs/validation.md) before implementing verdict logic.
