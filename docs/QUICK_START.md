# SmartPark - Quick Start Guide

This guide will help you get SmartPark up and running in minutes.

## Prerequisites

- **Python 3.7+** (Python 3.8 or higher recommended)
- **Tkinter** (usually pre-installed with Python on Windows/macOS; on Linux, install via package manager)

### Verify Python Installation

```bash
python --version
# or
python3 --version
```

### Verify Tkinter Installation

```bash
python -m tkinter
# A small window should appear. If it does, Tkinter is installed.
```

If Tkinter is not installed on Linux:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

## Installation

### 1. Clone/Download the Project

```bash
# Option 1: Clone from Git (if applicable)
git clone <repository-url>
cd py_project

# Option 2: Extract from ZIP
# Simply extract the ZIP file and navigate to the folder
cd py_project
```

### 2. Verify Project Structure

Ensure you have the following structure:
```
py_project/
├── src/
│   ├── main.py              # CLI entry point
│   ├── gui_main.py          # GUI entry point
│   ├── parking_system.py    # Main system controller
│   ├── allocation_engine.py
│   ├── rollback_manager.py
│   └── ui/                  # GUI screens
├── docs/                    # Documentation
├── exports/                 # Analytics exports
└── readme.md
```

## Running the Application

### Option 1: Graphical User Interface (GUI) - Recommended for Beginners

Navigate to the `src` directory and run:

```bash
cd src
python gui_main.py
```

**For Python 3 specifically:**
```bash
cd src
python3 gui_main.py
```

The GUI window will open with the following tabs:
- **Setup**: Configure zones, areas, and vehicles
- **Dashboard**: View system overview
- **New Request**: Create parking requests
- **Allocation Status**: View request details
- **Rollback**: Undo operations
- **Analytics**: View statistics and metrics

### Option 2: Command-Line Interface (CLI) - For Advanced Users

Navigate to the `src` directory and run:

```bash
cd src
python main.py
```

**For Python 3 specifically:**
```bash
cd src
python3 main.py
```

The CLI presents a menu-driven interface with 23 operations organized into categories:
- Setup Operations
- Parking Operations
- Query Operations
- Analytics
- Advanced Operations

## First-Time Setup Workflow

### Using GUI (Recommended)

1. **Start the GUI:**
   ```bash
   cd src
   python gui_main.py
   ```

2. **Navigate to Setup Tab** (⚙️ Setup):

3. **Add Zones:**
   - Enter Zone ID (e.g., `ZONE-A`)
   - Click "Add Zone"
   - Repeat for additional zones (e.g., `ZONE-B`, `ZONE-C`)

4. **Add Parking Areas:**
   - Select a zone from dropdown
   - Enter Area ID (e.g., `A1`)
   - Enter capacity (e.g., `10` slots)
   - Click "Add Parking Area"

5. **Link Adjacent Zones (Optional):**
   - Select two zones to link
   - Click "Link Adjacent Zones"
   - This enables cross-zone allocation with lower penalties

6. **Register Vehicles:**
   - Enter Vehicle ID (e.g., `CAR-001`)
   - Select preferred zone (optional)
   - Click "Register Vehicle"

7. **Create Parking Requests:**
   - Navigate to "🚗 New Request" tab
   - Select vehicle from dropdown
   - Select requested zone
   - Click "Create Request"

8. **Allocate Parking:**
   - System will auto-allocate in the requested zone if available
   - Otherwise, adjacent zones (penalty: 50) or distant zones (penalty: 100)

### Using CLI

1. **Start the CLI:**
   ```bash
   cd src
   python main.py
   ```

2. **Setup System** (follow menu options):
   ```
   1. Add Zone → Enter ZONE-A
   1. Add Zone → Enter ZONE-B
   2. Add Parking Area to Zone → ZONE-A, A1, capacity 10
   2. Add Parking Area to Zone → ZONE-B, B1, capacity 15
   3. Link Adjacent Zones → ZONE-A and ZONE-B
   4. Register Vehicle → CAR-001, preferred zone ZONE-A
   ```

3. **Test Parking Operations:**
   ```
   5. Create Parking Request → Vehicle: CAR-001, Zone: ZONE-A
   6. Allocate Parking → Enter request ID (e.g., REQ0001)
   7. Mark Parking as Occupied → Enter request ID
   8. Release Parking → Enter request ID
   ```

## Sample Workflow Example

### Complete Example: Park a Vehicle

**GUI Method:**
1. Setup Tab → Add Zone `ZONE-A` → Add Parking Area `A1` with capacity `5`
2. Setup Tab → Register Vehicle `CAR-001` with preferred zone `ZONE-A`
3. New Request Tab → Select `CAR-001`, select `ZONE-A` → Create Request
4. Allocation Status Tab → Click "Allocate Parking" button next to the request
5. Click "Mark as Occupied" when vehicle arrives
6. Click "Release Parking" when vehicle leaves

**CLI Method:**
```
Menu: 1 → ZONE-A
Menu: 2 → ZONE-A, A1, 5
Menu: 4 → CAR-001, ZONE-A
Menu: 5 → CAR-001, ZONE-A (Note the request ID, e.g., REQ0001)
Menu: 6 → REQ0001
Menu: 7 → REQ0001
Menu: 8 → REQ0001
```

## Key Features to Explore

### 1. Cross-Zone Allocation
- Request parking in ZONE-A when it's full
- System allocates in ZONE-B (adjacent) with penalty
- Penalty = 50 for adjacent zones, 100 for distant zones

### 2. Rollback Operations
- Every operation is recorded
- Rollback last K operations via Rollback tab (GUI) or Menu option 15 (CLI)
- Uses stack-based LIFO data structure

### 3. Analytics
- Navigate to Analytics tab (GUI) or use Menu 17-22 (CLI)
- View:
  - Average parking duration
  - Zone utilization rates
  - Request statistics (completed vs cancelled)
  - Peak usage zones
  - Cross-zone allocation statistics

### 4. State Machine Validation
- Requests follow strict state transitions:
  - REQUESTED → ALLOCATED → OCCUPIED → RELEASED
  - REQUESTED/ALLOCATED → CANCELLED
- Invalid transitions are rejected

## Troubleshooting

### Issue: "No module named tkinter" (Linux)
**Solution:** Install Tkinter:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### Issue: "ModuleNotFoundError: No module named 'parking_system'"
**Solution:** Ensure you're running from the `src` directory:
```bash
cd src
python gui_main.py
```

### Issue: GUI window is too small or text is cut off
**Solution:** Resize the window manually. Minimum size is 1000x650 pixels.

### Issue: No zones appear in dropdown
**Solution:** First add zones in the Setup tab before creating requests.

### Issue: Cannot allocate parking - "No available slots"
**Solution:** Add more parking areas or release occupied slots.

## Export Analytics

To export analytics data:

**GUI Method:**
1. Navigate to Analytics tab
2. Click "Export Analytics Summary"
3. File saved in `exports/summary/` folder with timestamp

**CLI Method:**
```
Menu: 17 → View Comprehensive Analytics
```
Output displayed on console.

## Next Steps

- Read [USER_GUIDE.md](USER_GUIDE.md) for detailed feature explanations
- Explore [DSA_CONCEPTS.md](DSA_CONCEPTS.md) to understand data structures used
- Check [API.md](API.md) for class and method documentation
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design details

## Quick Reference

### Common Zone/Vehicle ID Formats
- Zones: `ZONE-A`, `ZONE-B`, `PARKING-NORTH`
- Vehicles: `CAR-001`, `BIKE-123`, `TRUCK-XYZ`
- Areas: `A1`, `B1`, `SECTOR-1`

### ID Generation Rules
- **Zone IDs**: User-defined (uppercase recommended)
- **Vehicle IDs**: User-defined (uppercase recommended)
- **Request IDs**: Auto-generated as `REQ0001`, `REQ0002`, etc.
- **Slot IDs**: Auto-generated as `{ZONE_ID}-{AREA_ID}-{SLOT_NUMBER}`

### State Definitions
- **REQUESTED**: Request created, awaiting allocation
- **ALLOCATED**: Slot assigned, vehicle hasn't arrived
- **OCCUPIED**: Vehicle has parked in slot
- **RELEASED**: Vehicle left, slot freed
- **CANCELLED**: Request cancelled before completion

## Support

For issues or questions:
1. Check [USER_GUIDE.md](USER_GUIDE.md) for detailed instructions
2. Review [API.md](API.md) for method signatures
3. Consult [ARCHITECTURE.md](ARCHITECTURE.md) for system behavior

---

**Ready to start?** Run `python gui_main.py` from the `src` directory!
