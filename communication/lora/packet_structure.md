# Trinetra07 LoRa Packet Structure (Draft v0.1)

This document defines a **starter, versioned packet format** for prototype interoperability.
It is not yet a finalized production protocol.

## Frame Layout

| Byte(s) | Field | Type | Description |
|---|---|---|---|
| 0 | `version` | `uint8` | Protocol version (`0x01` for this draft). |
| 1 | `message_type` | `uint8` | Message kind (heartbeat, telemetry, alert, ack). |
| 2-3 | `sequence_id` | `uint16` | Monotonic sender sequence number. |
| 4-7 | `sender_id` | `uint32` | Unique node/vehicle identifier. |
| 8-11 | `timestamp_s` | `uint32` | Sender-local UNIX epoch seconds. |
| 12 | `payload_length` | `uint8` | Payload bytes that follow. |
| 13..N | `payload` | `bytes` | Message-specific payload. |
| N+1..N+2 | `crc16` | `uint16` | CRC-16 over bytes `0..N`. |

## Message Type Suggestions

- `0x01`: Heartbeat
- `0x02`: Vehicle telemetry summary
- `0x03`: Roadside node status
- `0x04`: Hazard alert
- `0x05`: ACK/NACK

## Notes

- Keep payload compact for low-bandwidth conditions.
- Reserve unknown message types for forward compatibility.
- Validate `version`, `payload_length`, and CRC before parsing payload data.
