# MPP-Solar Project Context

## Quick Start for AI Assistants

This file serves as the **re-entry point** for Claude Code when starting a new session or after a context reset.

## Project Overview

**MPP-Solar** is a Python package (v0.16.57) for communicating with solar inverters, Battery Management Systems (BMS), and power monitoring devices. It provides CLI tools, a daemon service, web interface, and multiple output formats (MQTT, Prometheus, Home Assistant, etc.).

**Current State:** Production-ready codebase with active development. Web interface and daemon service operational.

**Python Requirements:** 3.11+ (minimum 3.10 for >=0.16.0)

## Required Reading Order

When starting a new session, read these files in sequence:

1. **CLAUDE.md** - Development guide, commands, architecture overview, troubleshooting
   - Path: `/home/constantine/repo/mpp-solar/CLAUDE.md`
   - Purpose: Quick reference for common development tasks

2. **IMPLEMENTATION_PLAN.md** - Detailed technical architecture and design decisions
   - Path: `/home/constantine/repo/mpp-solar/IMPLEMENTATION_PLAN.md`
   - Purpose: Deep technical understanding of system design

3. **PROGRESS.md** - Development history, completed work, and known issues
   - Path: `/home/constantine/repo/mpp-solar/PROGRESS.md`
   - Purpose: Understand what's been done and what needs attention

## Critical Information

### Breaking Changes (v0.16.0)
- Command separator changed from `,` to `#`
- Example: `mpp-solar -c "QPIGS#QPIRI#QMOD"` (not `QPIGS,QPIRI,QMOD`)

### Architecture Layers
```
Hardware → I/O Port → Protocol Parser → Device (retry logic) → Output Processor → Destination
```

### Key Directories
- `mppsolar/protocols/` - 28+ protocol implementations
- `mppsolar/devices/` - Device orchestration with retry logic
- `mppsolar/inout/` - Physical communication handlers
- `mppsolar/outputs/` - Data routing (MQTT, Prometheus, etc.)
- `mppsolar/daemon/` - Background service
- `web_interface.py` - Flask web app

### Common Commands
```bash
# Run tests
make test

# Start web interface
python web_interface.py

# Basic device communication
mpp-solar -p /dev/hidraw0 -P pi30 --porttype hidraw -c QPIGS -D

# Run daemon
mpp-solar -C mpp-solar.conf --daemon
```

## Current Development Focus

Refer to `PROGRESS.md` for the latest status. The project is stable with ongoing enhancements to:
- Protocol support for new devices
- Web interface features
- Output format integrations

## Git Information

- **Current Branch:** changes
- **Main Branch:** master (use for PRs)
- **Status:** Clean working tree
- **Recent Work:** Web application improvements, Claude context documentation

## Next Steps

After reading the referenced files above, you should have full context to:
1. Answer questions about the codebase
2. Implement new features
3. Debug issues
4. Add protocol support
5. Enhance web interface or outputs

## File Structure Summary

```
mppsolar/
├── __init__.py (680+ lines, CLI entry point)
├── devices/ (AbstractDevice with retry logic)
├── protocols/ (28+ implementations)
├── inout/ (Serial, USB HID, Bluetooth, MQTT)
├── outputs/ (Screen, JSON, Prometheus, MQTT variants)
├── daemon/ (Systemd/OpenRC service)
└── libs/ (MQTT manager, utilities)

web_interface.py (Flask app, 265 lines)
templates/ (Web UI: standard + LCARS theme)
tests/ (Unit + integration tests)
```

## Workflow for Context Recovery

If you need to recover context after `/clear`:

1. Read this file (CONTEXT.md)
2. Read all referenced files in order
3. Summarize the current state and next steps
4. Confirm understanding before proceeding with work

---

**Last Updated:** 2025-10-30
