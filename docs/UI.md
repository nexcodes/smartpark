# SmartPark - User Interface Documentation

Complete documentation of SmartPark's dual interface system: Command-Line Interface (CLI) and Graphical User Interface (GUI).

## Table of Contents

- [Interface Overview](#interface-overview)
- [Command-Line Interface (CLI)](#command-line-interface-cli)
- [Graphical User Interface (GUI)](#graphical-user-interface-gui)
- [Interface Comparison](#interface-comparison)
- [Design Principles](#design-principles)

---

## Interface Overview

SmartPark provides **two complete interfaces** sharing the same backend:

| Interface | File | Purpose | Target User |
|-----------|------|---------|-------------|
| **CLI** | `main.py` | Terminal-based menu system | Developers, CLI enthusiasts |
| **GUI** | `gui_main.py` + `ui/` | Tkinter windowed application | General users, visual learners |

**Key Feature:** Both interfaces use the **same ParkingSystem backend**, ensuring consistent behavior.

---

## Command-Line Interface (CLI)

### Starting the CLI

```bash
cd src
python main.py
```

### Main Menu Structure

The CLI presents a **menu-driven interface** with 23 operations organized into 6 categories:

```
========================================================================
        SMART PARKING ALLOCATION & MANAGEMENT SYSTEM
========================================================================

--- SETUP OPERATIONS ---
1.  Add Zone
2.  Add Parking Area to Zone
3.  Link Adjacent Zones
4.  Register Vehicle

--- PARKING OPERATIONS ---
5.  Create Parking Request
6.  Allocate Parking
7.  Mark Parking as Occupied
8.  Release Parking
9.  Cancel Parking Request

--- QUERY OPERATIONS ---
10. View System Status
11. View Zone Status
12. View Request Details
13. View All Zones
14. View All Vehicles

--- ANALYTICS ---
17. View Comprehensive Analytics
18. View Average Parking Duration
19. View Zone Utilization
20. View Request Statistics
21. View Peak Usage Zone
22. View Cross-Zone Statistics

--- ADVANCED OPERATIONS ---
15. Rollback Operations
16. View Operation History

--- SYSTEM ---
0.  Exit
========================================================================
```

### CLI Operation Details

#### Setup Operations

**1. Add Zone**
```
Enter Zone ID (e.g., ZONE-A): ZONE-A
✓ Zone ZONE-A created successfully
```

- Input: Zone ID (uppercase recommended)
- Validation: Checks for duplicate zone IDs
- Output: Success/error message with emoji

**2. Add Parking Area to Zone**
```
Enter Zone ID: ZONE-A
Enter Area ID (e.g., A1): A1
Enter capacity (number of slots): 10
✓ Parking area A1 added to ZONE-A with 10 slots
```

- Input: Zone ID, Area ID, capacity (integer)
- Validation: Zone existence, positive capacity
- Output: Confirmation with slot count

**3. Link Adjacent Zones**
```
Enter first Zone ID: ZONE-A
Enter second Zone ID: ZONE-B
✓ Linked ZONE-A ↔ ZONE-B
```

- Input: Two zone IDs
- Validation: Both zones must exist
- Effect: Creates bidirectional graph edge
- Output: Arrow symbol (↔) shows bidirectional link

**4. Register Vehicle**
```
Enter Vehicle ID (e.g., CAR-001): CAR-001
Enter preferred zone (optional, press Enter to skip): ZONE-A
✓ Vehicle CAR-001 registered with preferred zone ZONE-A
```

- Input: Vehicle ID, optional preferred zone
- Validation: Checks for duplicate vehicle IDs
- Output: Confirmation with preferences

---

#### Parking Operations

**5. Create Parking Request**
```
Enter Vehicle ID: CAR-001
Enter requested zone: ZONE-A
✓ Parking request REQ0001 created
  Request ID: REQ0001
  State: REQUESTED
```

- Input: Vehicle ID, requested zone ID
- Output: Generated request ID and initial state
- Note: Request IDs are auto-incremented (REQ0001, REQ0002, ...)

**6. Allocate Parking**
```
Enter Request ID: REQ0001
✓ Allocated in requested zone
  Slot: ZONE-A-A1-1
  Zone: ZONE-A
  Penalty: 0
```

- Input: Request ID
- Output: Allocated slot ID, zone, penalty score
- Penalty: 0 (same), 50 (adjacent), 100 (distant)

**7. Mark Parking as Occupied**
```
Enter Request ID: REQ0001
✓ Parking marked as occupied
```

- Input: Request ID
- State transition: ALLOCATED → OCCUPIED
- Output: Simple confirmation

**8. Release Parking**
```
Enter Request ID: REQ0001
✓ Parking released successfully
```

- Input: Request ID
- State transition: OCCUPIED → RELEASED
- Effect: Frees the parking slot

**9. Cancel Parking Request**
```
Enter Request ID: REQ0002
✓ Request cancelled from ALLOCATED state
```

- Input: Request ID
- Valid states: REQUESTED or ALLOCATED
- Effect: Releases slot if allocated

---

#### Query Operations

**10. View System Status**
```
========================================================================

SYSTEM STATUS
----------------------------------------
Total slots:      50
Available slots:  38
Occupied slots:   12
Total zones:      3
Total requests:   15
Active requests:  5

========================================================================
```

- No input required
- Output: System-wide statistics
- Refresh: Run again to see updated values

**11. View Zone Status**
```
Enter Zone ID: ZONE-A
========================================================================

ZONE STATUS
----------------------------------------
Zone ID:          ZONE-A
Total Capacity:   20
Available:        15
Occupied:         5
Areas:            2
Adjacent Zones:   ['ZONE-B', 'ZONE-C']

========================================================================
```

- Input: Zone ID
- Output: Zone-specific statistics and adjacency info

**12. View Request Details**
```
Enter Request ID: REQ0001
========================================================================

REQUEST DETAILS
----------------------------------------
Request ID:       REQ0001
Vehicle ID:       CAR-001
Requested Zone:   ZONE-A
Allocated Zone:   ZONE-A
Allocated Slot:   ZONE-A-A1-1
Current State:    OCCUPIED
Timestamp:        2026-01-20 14:30:15
Allocation Time:  2026-01-20 14:30:20

========================================================================
```

- Input: Request ID
- Output: Complete request lifecycle information

**13. View All Zones**
```
========================================================================

ALL ZONES
----------------------------------------
Zone ZONE-A: 15/20 available
Zone ZONE-B: 20/25 available
Zone ZONE-C: 8/10 available

========================================================================
```

- No input required
- Output: List of all zones with availability

**14. View All Vehicles**
```
========================================================================

REGISTERED VEHICLES
----------------------------------------
Vehicle CAR-001 (Prefers Zone ZONE-A)
Vehicle CAR-002 (Prefers Zone ZONE-B)
Vehicle TRUCK-001 (No preference)

========================================================================
```

- No input required
- Output: List of all registered vehicles

---

#### Analytics Operations

**17. View Comprehensive Analytics**
```
============================================================
PARKING SYSTEM ANALYTICS SUMMARY
============================================================

--- Average Parking Duration ---
  Average Duration: 45.5 minutes
  Completed Sessions: 8

--- Request Statistics ---
  Total Requests: 15
  Completed: 8 (53.33%)
  Cancelled: 2 (13.33%)
  Active (Requested): 1
  Active (Allocated): 2
  Active (Occupied): 2

--- Zone Utilization ---
  ZONE-A: 75.0% (15/20 occupied)
  ZONE-B: 60.0% (15/25 occupied)
  ZONE-C: 20.0% (2/10 occupied)

--- Peak Usage Zone ---
  Zone: ZONE-A
  Utilization: 75.0%
  Occupied: 15/20

--- Cross-Zone Allocation Statistics ---
  Total Allocations: 10
  Same Zone: 7
  Cross Zone: 3 (30.0%)

============================================================
```

- No input required
- Output: Complete analytics report with all metrics

**18-22. Individual Analytics Views**

Each analytics operation shows a focused subset:
- **18**: Average parking duration only
- **19**: Zone utilization breakdown
- **20**: Request statistics by state
- **21**: Peak usage zone identification
- **22**: Cross-zone allocation percentage

---

#### Advanced Operations

**15. Rollback Operations**
```
Enter number of operations to rollback: 2
✓ Successfully rolled back 2 operations
  Operation 1: ALLOCATE for REQ0005 (Slot: ZONE-B-B1-3)
  Operation 2: OCCUPY for REQ0004
```

- Input: Number of operations (k)
- Validation: k ≤ operations in history
- Effect: Reverts last k operations using stack
- Output: List of rolled-back operations

**16. View Operation History**
```
========================================================================

OPERATION HISTORY
----------------------------------------
Total Operations: 12

Recent Operations (Last 10):
1. ALLOCATE - Request REQ0005, Slot ZONE-B-B1-3
2. OCCUPY - Request REQ0004
3. ALLOCATE - Request REQ0004, Slot ZONE-A-A1-2
4. CANCEL - Request REQ0003
5. RELEASE - Request REQ0002
... (older operations)

========================================================================
```

- No input required
- Output: Stack of operations (most recent first)

---

### CLI User Experience Features

**1. Emoji Indicators**
- ✓ (✅) — Success
- ❌ — Error/failure
- ℹ️ — Information

**2. Input Validation**
- Automatic `.strip()` removes whitespace
- `.upper()` converts to uppercase for IDs
- Integer parsing with error handling

**3. Error Messages**
```
❌ Zone ZONE-Z not found
❌ Vehicle CAR-999 already registered
❌ Cannot allocate - request is in CANCELLED state
```

Clear, specific error descriptions.

**4. Visual Separators**
```
========================================================================
----------------------------------------
```

Improve readability of output sections.

**5. Persistent Menu**

After each operation, menu redisplays. No need to restart application.

---

## Graphical User Interface (GUI)

### Starting the GUI

```bash
cd src
python gui_main.py
```

### GUI Window Structure

**Main Window Components:**

1. **Header Bar** (Dark blue background)
   - Title: "🅿️ SmartPark Management System"
   - Subtitle: "Intelligent Parking Allocation with DSA"
   - Fixed height: 100px

2. **Tabbed Navigation** (Notebook widget)
   - 6 tabs with emoji icons
   - Selected tab highlighted in blue
   - Auto-refresh on tab change

3. **Content Area** (White background)
   - Tab-specific content
   - Scrollable if needed
   - Consistent card-based layout

### Color Scheme

```python
{
    'primary':   '#2563eb',  # Blue (buttons, tabs)
    'secondary': '#10b981',  # Green (success)
    'danger':    '#ef4444',  # Red (delete, errors)
    'warning':   '#f59e0b',  # Orange (warnings)
    'info':      '#3b82f6',  # Light Blue (info)
    'success':   '#22c55e',  # Light Green (completion)
    'dark':      '#1e293b',  # Dark Blue Gray (header)
    'light':     '#f8fafc',  # Light Gray (background)
    'gray':      '#64748b',  # Medium Gray (text)
    'card_bg':   '#ffffff'   # White (cards)
}
```

---

### Tab 1: Setup (⚙️ Setup)

**Purpose:** Configure zones, areas, vehicles, and zone adjacencies

**Layout:**

```
┌─────────────────────────────────────────────┐
│          ADD ZONE                           │
│  ┌───────────────────┐  ┌──────────────┐   │
│  │ Zone ID: [______] │  │  Add Zone    │   │
│  └───────────────────┘  └──────────────┘   │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│       ADD PARKING AREA                      │
│  Zone: [Dropdown v]                         │
│  Area ID: [______]                          │
│  Capacity: [______]                         │
│  ┌──────────────────┐                       │
│  │ Add Parking Area │                       │
│  └──────────────────┘                       │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│       LINK ADJACENT ZONES                   │
│  Zone 1: [Dropdown v]                       │
│  Zone 2: [Dropdown v]                       │
│  ┌─────────────────────┐                    │
│  │ Link Adjacent Zones │                    │
│  └─────────────────────┘                    │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│       REGISTER VEHICLE                      │
│  Vehicle ID: [______]                       │
│  Preferred Zone: [Dropdown v]               │
│  ┌─────────────────┐                        │
│  │ Register Vehicle│                        │
│  └─────────────────┘                        │
└─────────────────────────────────────────────┘
```

**Features:**
- Dropdowns auto-populate from existing zones
- Real-time validation (e.g., capacity must be positive)
- Success/error messages via popup dialogs
- Input fields clear after successful operation

**Interactions:**
1. **Add Zone:** Enter ID → Click button → Popup confirms
2. **Add Area:** Select zone → Enter area ID and capacity → Click button
3. **Link Zones:** Select two zones → Click button → Creates bidirectional edge
4. **Register Vehicle:** Enter ID → Select preferred zone (optional) → Click button

---

### Tab 2: Dashboard (📊 Dashboard)

**Purpose:** System overview with real-time statistics

**Layout:**

```
┌───────────────────────────────────────────────────────┐
│  System Overview                                      │
│                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │  Total Slots │  │   Available  │  │  Occupied  ││
│  │      50      │  │      38      │  │     12     ││
│  └──────────────┘  └──────────────┘  └────────────┘│
│                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │ Total Zones  │  │Total Requests│  │   Active   ││
│  │      3       │  │      15      │  │  Requests  ││
│  │              │  │              │  │      5     ││
│  └──────────────┘  └──────────────┘  └────────────┘│
└───────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────┐
│  Zone Details                                         │
│                                                       │
│  ZONE-A      [████████░░] 80%  (16/20 occupied)     │
│  ZONE-B      [██████░░░░] 60%  (15/25 occupied)     │
│  ZONE-C      [██░░░░░░░░] 20%  (2/10 occupied)      │
└───────────────────────────────────────────────────────┘

                    [🔄 Refresh Dashboard]
```

**Features:**
- **Cards:** Large numbers in colored cards
- **Progress Bars:** Visual zone utilization
- **Auto-Refresh:** Updates when tab is opened
- **Manual Refresh:** Button to force update

**Card Colors:**
- Total Slots: Blue
- Available: Green
- Occupied: Orange
- Active Requests: Red (if > 0)

---

### Tab 3: New Request (🚗 New Request)

**Purpose:** Create new parking requests

**Layout:**

```
┌─────────────────────────────────────────────┐
│       CREATE PARKING REQUEST                │
│                                             │
│  Select Vehicle: [Dropdown v]              │
│                                             │
│  Select Requested Zone: [Dropdown v]       │
│                                             │
│  ┌─────────────────┐                       │
│  │ Create Request  │                       │
│  └─────────────────┘                       │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│       RECENT REQUESTS                       │
│                                             │
│  REQ0005 - CAR-001 → ZONE-A [REQUESTED]    │
│  REQ0004 - CAR-002 → ZONE-B [ALLOCATED]    │
│  REQ0003 - CAR-003 → ZONE-A [CANCELLED]    │
└─────────────────────────────────────────────┘
```

**Features:**
- Dropdowns show only registered vehicles and zones
- Request created immediately on button click
- Recent requests list updates automatically
- Color-coded states:
  - REQUESTED: Blue
  - ALLOCATED: Green
  - CANCELLED: Red

**Workflow:**
1. Select vehicle from dropdown
2. Select zone from dropdown
3. Click "Create Request"
4. Popup shows generated request ID
5. Request appears in recent list

---

### Tab 4: Allocation Status (📍 Allocation Status)

**Purpose:** View all requests and perform state transitions

**Layout:**

```
┌───────────────────────────────────────────────────────────────┐
│  Filters: [All States v]  [All Zones v]  [🔍 Search]         │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│ Request ID │ Vehicle  │ Req Zone │ Alloc Zone │ State         │
├────────────┼──────────┼──────────┼────────────┼───────────────┤
│ REQ0005    │ CAR-001  │ ZONE-A   │ ZONE-A     │ [Allocate]    │
│ REQ0004    │ CAR-002  │ ZONE-B   │ ZONE-A     │ [Mark Occup.] │
│ REQ0003    │ CAR-003  │ ZONE-A   │ ZONE-A     │ [Release]     │
│ REQ0002    │ CAR-001  │ ZONE-B   │ —          │ [Cancel]      │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│  Request Details: REQ0005                                     │
│                                                               │
│  Vehicle: CAR-001                                             │
│  Requested Zone: ZONE-A                                       │
│  Allocated Zone: ZONE-A                                       │
│  Allocated Slot: ZONE-A-A1-1                                  │
│  State: OCCUPIED                                              │
│  Created: 2026-01-20 14:30:15                                 │
│  Allocated: 2026-01-20 14:30:20                               │
│  Penalty: 0                                                   │
└───────────────────────────────────────────────────────────────┘
```

**Features:**
- **Table View:** All requests with action buttons
- **State-Aware Buttons:** Only valid actions shown
  - REQUESTED → "Allocate" or "Cancel"
  - ALLOCATED → "Mark Occupied" or "Cancel"
  - OCCUPIED → "Release"
  - RELEASED/CANCELLED → (no actions)
- **Filters:** Dropdown filters by state or zone
- **Search:** Filter by request ID or vehicle ID
- **Details Panel:** Click row to see full details

**Interactions:**
1. Click row to select request
2. Details appear in bottom panel
3. Click action button (e.g., "Allocate")
4. Popup confirms action
5. Table and details refresh

---

### Tab 5: Rollback (↩️ Rollback)

**Purpose:** View operation history and rollback

**Layout:**

```
┌─────────────────────────────────────────────┐
│       OPERATION HISTORY                     │
│                                             │
│  Total Operations: 12                      │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │ #12: ALLOCATE - REQ0005 (ZONE-B)    │   │
│  │ #11: OCCUPY - REQ0004               │   │
│  │ #10: ALLOCATE - REQ0004 (ZONE-A)    │   │
│  │ #9: CANCEL - REQ0003                │   │
│  │ #8: RELEASE - REQ0002               │   │
│  │ ... (scroll for more)               │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│       ROLLBACK OPERATIONS                   │
│                                             │
│  Number of operations: [____]              │
│                                             │
│  ┌──────────────────┐                      │
│  │ Rollback         │                      │
│  └──────────────────┘                      │
└─────────────────────────────────────────────┘
```

**Features:**
- **Scrollable History:** Most recent operations at top (LIFO visualization)
- **Operation Count Display:** Shows stack size
- **Numeric Input:** Spinner or text field for k
- **Validation:** Cannot rollback more than available operations
- **Confirmation Dialog:** "Are you sure?" before rollback

**Workflow:**
1. View operation history (auto-refreshed)
2. Enter number of operations to rollback
3. Click "Rollback" button
4. Confirm in popup dialog
5. Success message shows rolled-back operations
6. History updates (operations removed from stack)

---

### Tab 6: Analytics (📈 Analytics)

**Purpose:** View metrics and export reports

**Layout:**

```
┌───────────────────────────────────────────────────────┐
│  PARKING DURATION                                     │
│  Average: 45.5 minutes (8 sessions)                   │
└───────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────┐
│  ZONE UTILIZATION                                     │
│  ZONE-A: 75% [███████████████░░░░░]                   │
│  ZONE-B: 60% [████████████░░░░░░░░]                   │
│  ZONE-C: 20% [████░░░░░░░░░░░░░░░░]                   │
└───────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────┐
│  REQUEST STATISTICS                                   │
│  Total: 15  Completed: 8 (53%)  Cancelled: 2 (13%)    │
│                                                        │
│  [Pie Chart or Bar Chart visualization]               │
└───────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────┐
│  CROSS-ZONE ALLOCATIONS                               │
│  Same Zone: 7 (70%)                                    │
│  Cross Zone: 3 (30%)                                   │
└───────────────────────────────────────────────────────┘

                [🔄 Refresh]  [💾 Export Summary]
```

**Features:**
- **Visual Metrics:** Progress bars, charts, large numbers
- **Real-Time Updates:** Refresh button recalculates
- **Export Functionality:** Saves summary to `exports/summary/`
- **Timestamp:** Export files include timestamp

**Export Format:**
```
File: exports/summary/analytics_summary_20260120_191929.txt
```

**Interactions:**
1. View analytics (auto-calculated on tab open)
2. Click "Refresh" to recalculate
3. Click "Export Summary" to save
4. Popup confirms file path

---

### GUI User Experience Features

**1. Message Boxes**
- **Success:** Green checkmark, "Success" title
- **Error:** Red X, "Error" title
- **Info:** Blue i, "Information" title

**2. Tooltips (Hover Text)**
- Buttons show descriptions on hover
- Input fields show format hints

**3. Validation Feedback**
- Red border for invalid input
- Green border for valid input

**4. Loading Indicators**
- Cursor changes to hourglass during operations
- "Processing..." label for long operations

**5. Keyboard Shortcuts**
- Enter key submits forms
- Tab key navigates fields

**6. Responsive Layout**
- Minimum window size: 1000x650
- Resizable (content adapts)
- Scrollbars appear if needed

---

## Interface Comparison

### Feature Parity

| Feature | CLI | GUI | Notes |
|---------|-----|-----|-------|
| Add Zone | ✓ | ✓ | Same functionality |
| Add Parking Area | ✓ | ✓ | GUI has dropdown |
| Link Zones | ✓ | ✓ | GUI has dual dropdown |
| Register Vehicle | ✓ | ✓ | Same |
| Create Request | ✓ | ✓ | GUI shows recent requests |
| Allocate Parking | ✓ | ✓ | GUI has table view |
| Mark Occupied | ✓ | ✓ | Same |
| Release Parking | ✓ | ✓ | Same |
| Cancel Request | ✓ | ✓ | Same |
| View System Status | ✓ | ✓ | GUI has cards |
| View Zone Status | ✓ | ✓ | GUI has progress bars |
| View Request Details | ✓ | ✓ | GUI has table + details panel |
| Rollback Operations | ✓ | ✓ | GUI has visual history |
| View History | ✓ | ✓ | GUI has scrollable list |
| Analytics | ✓ | ✓ | GUI has visualizations |
| Export Analytics | CLI prints | ✓ | GUI exports to file |

### Strengths & Weaknesses

#### CLI Strengths
- ✅ Fast for experienced users
- ✅ Easy to script/automate
- ✅ No GUI dependencies
- ✅ Works over SSH
- ✅ Lightweight

#### CLI Weaknesses
- ❌ Steeper learning curve
- ❌ No visual feedback (text only)
- ❌ Menu navigation required
- ❌ Hard to see overview

#### GUI Strengths
- ✅ Visual feedback (colors, charts)
- ✅ Easy to learn (intuitive)
- ✅ Dashboard overview
- ✅ Point-and-click operations
- ✅ Export functionality

#### GUI Weaknesses
- ❌ Requires Tkinter installation
- ❌ Slower for bulk operations
- ❌ Cannot be scripted
- ❌ Larger memory footprint

### Use Case Recommendations

| Scenario | Recommended Interface |
|----------|----------------------|
| First-time user | **GUI** — Easier to learn |
| Bulk setup (many zones/vehicles) | **CLI** — Faster input |
| Monitoring system status | **GUI** — Visual dashboard |
| Scripted/automated testing | **CLI** — Can be automated |
| Analytics review | **GUI** — Better visualizations |
| Quick single operation | **CLI** — Fewer clicks |
| Demonstration/presentation | **GUI** — More visual appeal |

---

## Design Principles

### Shared Backend Architecture

```
┌─────────┐       ┌─────────┐
│   CLI   │       │   GUI   │
└────┬────┘       └────┬────┘
     │                 │
     └────────┬────────┘
              │
       ┌──────▼──────┐
       │ ParkingSystem│
       │   (Backend)  │
       └──────────────┘
```

**Benefit:** Consistent logic, single source of truth

### Input Validation Patterns

**CLI:**
```python
zone_id = input("Enter Zone ID: ").strip().upper()
if not zone_id:
    print("❌ Zone ID cannot be empty!")
    return
```

**GUI:**
```python
zone_id = self.zone_entry.get().strip().upper()
if not zone_id:
    messagebox.showerror("Error", "Zone ID cannot be empty!")
    return
```

### Error Handling

**Both interfaces:**
1. Validate input before calling backend
2. Check result dictionary for `success` key
3. Display appropriate message
4. Prevent state corruption

**Example:**
```python
result = system.add_zone(zone_id)
if result['success']:
    display_success(result['message'])
else:
    display_error(result['message'])
```

### Consistency Rules

1. **ID Formats:** Always uppercase (enforced in both interfaces)
2. **Messages:** Same wording from backend
3. **State Transitions:** Both follow state machine rules
4. **Penalties:** Same calculation (0, 50, 100)

---

## Summary

**SmartPark Dual Interface:**

- **CLI:** Menu-driven, 23 operations, emoji feedback, text-based
- **GUI:** Tabbed navigation, 6 screens, visual dashboards, point-and-click

**Shared Features:**
- Same backend (ParkingSystem)
- All 23 operations available
- Consistent validation and error handling
- State machine enforcement

**Key Differences:**
- CLI: Fast for experts, good for automation
- GUI: Visual feedback, easier learning curve

**Design Philosophy:**
- User choice: pick interface based on preference
- Consistent behavior: same logic, different presentation
- Educational value: demonstrates interface separation

---

**For usage instructions, see [USER_GUIDE.md](USER_GUIDE.md)**  
**For backend details, see [ARCHITECTURE.md](ARCHITECTURE.md)**  
**For getting started, see [QUICK_START.md](QUICK_START.md)**
