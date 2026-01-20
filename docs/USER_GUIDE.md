# SmartPark - User Guide

Complete guide for using SmartPark's parking management features. This guide covers all operations, workflows, and best practices.

## Table of Contents

- [Getting Started](#getting-started)
- [Basic Concepts](#basic-concepts)
- [Setup Workflow](#setup-workflow)
- [Parking Operations](#parking-operations)
- [Querying Information](#querying-information)
- [Analytics & Reporting](#analytics--reporting)
- [Advanced Features](#advanced-features)
- [Common Workflows](#common-workflows)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## Getting Started

### Prerequisites
- Python 3.7+ installed
- Tkinter (for GUI)

### Choose Your Interface

**GUI (Recommended for beginners):**
```bash
cd src
python gui_main.py
```

**CLI (For advanced users):**
```bash
cd src
python main.py
```

---

## Basic Concepts

### System Hierarchy

```
Parking System
├── Zones (e.g., ZONE-A, ZONE-B)
│   ├── Parking Areas (e.g., A1, A2)
│   │   └── Parking Slots (e.g., ZONE-A-A1-1, ZONE-A-A1-2)
│   └── Adjacent Zones (graph connections)
├── Vehicles (e.g., CAR-001, TRUCK-XYZ)
└── Parking Requests (e.g., REQ0001, REQ0002)
```

### Key Terms

| Term | Definition | Example |
|------|------------|---------|
| **Zone** | Large parking area (graph node) | ZONE-A, PARKING-NORTH |
| **Parking Area** | Subdivision of a zone | A1, SECTOR-1 |
| **Parking Slot** | Individual parking space | ZONE-A-A1-1 |
| **Vehicle** | Registered car/vehicle | CAR-001, BIKE-123 |
| **Parking Request** | Vehicle's request to park | REQ0001 |
| **Adjacent Zones** | Zones connected in graph | ZONE-A ↔ ZONE-B |
| **Penalty** | Distance cost (0, 50, or 100) | 0 = same zone, 50 = adjacent |

### Request Lifecycle

```
1. REQUESTED    → Request created, awaiting allocation
2. ALLOCATED    → Slot assigned, vehicle not yet parked
3. OCCUPIED     → Vehicle parked in slot
4. RELEASED     → Vehicle left, slot freed
5. CANCELLED    → Request cancelled before completion
```

**Valid Transitions:**
- REQUESTED → ALLOCATED or CANCELLED
- ALLOCATED → OCCUPIED or CANCELLED
- OCCUPIED → RELEASED

---

## Setup Workflow

### Step 1: Add Zones

**Purpose:** Create parking zones (graph nodes)

**GUI:** Setup Tab → Add Zone section
**CLI:** Menu option 1

**Instructions:**
1. Enter a unique Zone ID (e.g., `ZONE-A`)
2. Use uppercase for consistency
3. Zone IDs must be unique

**Example:**
```
Add zones: ZONE-A, ZONE-B, ZONE-C
```

**Tips:**
- Use descriptive names: `PARKING-NORTH`, `GARAGE-EAST`
- Plan zones based on physical layout
- Typical system: 3-10 zones

---

### Step 2: Add Parking Areas to Zones

**Purpose:** Create parking areas with slots

**GUI:** Setup Tab → Add Parking Area section
**CLI:** Menu option 2

**Instructions:**
1. Select a zone (GUI dropdown or CLI input)
2. Enter an Area ID (e.g., `A1`)
3. Enter capacity (number of slots, e.g., `10`)
4. System auto-generates slot IDs

**Example:**
```
Zone: ZONE-A
Area ID: A1
Capacity: 10

Generated slots: ZONE-A-A1-1, ZONE-A-A1-2, ..., ZONE-A-A1-10
```

**Tips:**
- Multiple areas per zone allowed
- Typical capacity: 5-50 slots per area
- Area IDs must be unique within a zone

---

### Step 3: Link Adjacent Zones (Optional)

**Purpose:** Create zone graph for cross-zone allocation

**GUI:** Setup Tab → Link Adjacent Zones section
**CLI:** Menu option 3

**Instructions:**
1. Select first zone
2. Select second zone
3. System creates bidirectional link (edge)

**Example:**
```
Link ZONE-A ↔ ZONE-B (penalty = 50 for cross-zone)
Link ZONE-B ↔ ZONE-C
Result: ZONE-A can allocate in ZONE-B with penalty 50
```

**Tips:**
- Link physically adjacent zones
- Reduces penalty for cross-zone allocation
- Creates undirected graph edges

**When to Skip:**
- Small system with 1-2 zones
- No cross-zone allocation needed

---

### Step 4: Register Vehicles

**Purpose:** Add vehicles that can request parking

**GUI:** Setup Tab → Register Vehicle section
**CLI:** Menu option 4

**Instructions:**
1. Enter a unique Vehicle ID (e.g., `CAR-001`)
2. Optionally select a preferred zone
3. Vehicle can now create parking requests

**Example:**
```
Vehicle ID: CAR-001
Preferred Zone: ZONE-A (optional)
```

**Tips:**
- Use meaningful IDs: `CAR-001`, `TRUCK-XYZ`, `BIKE-123`
- Preferred zone is informational only (not enforced)
- Vehicle IDs must be unique

---

## Parking Operations

### Creating a Parking Request

**Purpose:** Request parking for a vehicle in a specific zone

**GUI:** New Request Tab
**CLI:** Menu option 5

**Instructions:**
1. Select a registered vehicle
2. Select a requested zone
3. Click "Create Request" (GUI) or confirm (CLI)
4. System generates a request ID (e.g., `REQ0001`)

**Example:**
```
Vehicle: CAR-001
Requested Zone: ZONE-A
→ Request REQ0001 created (State: REQUESTED)
```

**Tips:**
- Request ID is auto-generated
- Initial state: REQUESTED
- Vehicle can have multiple active requests

---

### Allocating Parking

**Purpose:** Assign a parking slot to a request

**GUI:** Allocation Status Tab → Click "Allocate" button
**CLI:** Menu option 6

**Instructions:**
1. Enter request ID (or select in GUI)
2. System uses 3-tier priority:
   - **Same Zone** (penalty = 0)
   - **Adjacent Zone** (penalty = 50)
   - **Distant Zone** (penalty = 100)
3. Slot assigned if available

**Example Scenarios:**

**Scenario 1: Same Zone Available**
```
Request: REQ0001 (Vehicle CAR-001, Requested ZONE-A)
Result: Allocated ZONE-A-A1-1, Penalty = 0
```

**Scenario 2: Same Zone Full, Adjacent Available**
```
Request: REQ0002 (Vehicle CAR-002, Requested ZONE-A)
ZONE-A is full
ZONE-B is adjacent and has slots
Result: Allocated ZONE-B-B1-1, Penalty = 50
```

**Scenario 3: No Adjacent Zones, Distant Zone**
```
Request: REQ0003 (Vehicle CAR-003, Requested ZONE-A)
ZONE-A is full
No adjacent zones
ZONE-C has slots
Result: Allocated ZONE-C-C1-1, Penalty = 100
```

**Scenario 4: No Slots Available**
```
Request: REQ0004
All zones full
Result: Allocation failed (remains REQUESTED)
```

**Tips:**
- Lower penalty is better (closer to requested zone)
- Link adjacent zones to reduce penalties
- Can retry allocation later if slots free up

**State Transition:** REQUESTED → ALLOCATED

---

### Marking Parking as Occupied

**Purpose:** Indicate vehicle has arrived and parked

**GUI:** Allocation Status Tab → Click "Mark Occupied" button
**CLI:** Menu option 7

**Instructions:**
1. Select an ALLOCATED request
2. Click "Mark Occupied" (GUI) or enter request ID (CLI)
3. State changes to OCCUPIED

**Example:**
```
Request: REQ0001 (State: ALLOCATED)
Action: Mark as Occupied
Result: State = OCCUPIED, slot is now in use
```

**Tips:**
- Can only mark ALLOCATED requests
- Timestamps are recorded
- Slot remains unavailable until released

**State Transition:** ALLOCATED → OCCUPIED

---

### Releasing Parking

**Purpose:** Vehicle leaves, slot becomes available

**GUI:** Allocation Status Tab → Click "Release" button
**CLI:** Menu option 8

**Instructions:**
1. Select an OCCUPIED request
2. Click "Release" (GUI) or enter request ID (CLI)
3. Slot freed, state changes to RELEASED

**Example:**
```
Request: REQ0001 (State: OCCUPIED, Slot: ZONE-A-A1-1)
Action: Release Parking
Result: State = RELEASED, slot ZONE-A-A1-1 available again
```

**Tips:**
- Can only release OCCUPIED requests
- Duration calculated (allocation time → release time)
- Terminal state (cannot transition further)

**State Transition:** OCCUPIED → RELEASED

---

### Cancelling a Request

**Purpose:** Cancel before completion (release slot if allocated)

**GUI:** Allocation Status Tab → Click "Cancel" button
**CLI:** Menu option 9

**Instructions:**
1. Select a REQUESTED or ALLOCATED request
2. Click "Cancel" (GUI) or enter request ID (CLI)
3. Slot released if allocated, state changes to CANCELLED

**Example 1: Cancel Requested**
```
Request: REQ0005 (State: REQUESTED)
Action: Cancel
Result: State = CANCELLED (no slot to free)
```

**Example 2: Cancel Allocated**
```
Request: REQ0006 (State: ALLOCATED, Slot: ZONE-B-B1-3)
Action: Cancel
Result: State = CANCELLED, slot ZONE-B-B1-3 freed
```

**Tips:**
- Cannot cancel OCCUPIED or RELEASED requests
- Use Release for occupied requests
- Terminal state (cannot undo without rollback)

**State Transitions:**
- REQUESTED → CANCELLED
- ALLOCATED → CANCELLED

---

## Querying Information

### View System Status

**Purpose:** Overview of entire system

**GUI:** Dashboard Tab (auto-displayed)
**CLI:** Menu option 10

**Information Shown:**
- Total slots (all zones)
- Available slots
- Occupied slots
- Total zones
- Total requests
- Active requests
- Operations in rollback history

**Example Output:**
```
Total slots:      50
Available slots:  38
Occupied slots:   12
Total zones:      3
Total requests:   15
Active requests:  5
Operations in history: 12
```

**Use Cases:**
- Quick system health check
- Monitor capacity
- Track activity

---

### View Zone Status

**Purpose:** Details about a specific zone

**GUI:** Dashboard Tab → Zone details section
**CLI:** Menu option 11

**Information Shown:**
- Zone ID
- Total capacity
- Available slots
- Occupied slots
- Number of parking areas
- Adjacent zones (graph edges)

**Example Output:**
```
Zone ID:          ZONE-A
Total Capacity:   20
Available:        15
Occupied:         5
Areas:            2
Adjacent Zones:   ['ZONE-B', 'ZONE-C']
```

**Use Cases:**
- Check zone availability
- Verify zone setup
- See zone connections

---

### View Request Details

**Purpose:** Complete information about a parking request

**GUI:** Allocation Status Tab → Click request → Details panel
**CLI:** Menu option 12

**Information Shown:**
- Request ID
- Vehicle ID
- Requested zone
- Allocated zone (if allocated)
- Allocated slot (if allocated)
- Current state
- Timestamps (creation, allocation, release)
- Penalty score
- Parking duration (if released)

**Example Output:**
```
Request ID:       REQ0001
Vehicle ID:       CAR-001
Requested Zone:   ZONE-A
Allocated Zone:   ZONE-A
Allocated Slot:   ZONE-A-A1-1
Current State:    OCCUPIED
Created:          2026-01-20 14:30:15
Allocated:        2026-01-20 14:30:20
Penalty:          0
```

**Use Cases:**
- Track request lifecycle
- Verify allocation
- Audit parking sessions

---

### View All Zones

**Purpose:** List all zones with availability

**GUI:** Dashboard Tab (integrated)
**CLI:** Menu option 13

**Example Output:**
```
Zone ZONE-A: 15/20 available (75% utilized)
Zone ZONE-B: 20/25 available (60% utilized)
Zone ZONE-C: 8/10 available (20% utilized)
```

---

### View All Vehicles

**Purpose:** List registered vehicles

**GUI:** Setup Tab → Vehicle list (if implemented)
**CLI:** Menu option 14

**Example Output:**
```
Vehicle CAR-001 (Prefers Zone ZONE-A)
Vehicle CAR-002 (Prefers Zone ZONE-B)
Vehicle TRUCK-001 (No preference)
```

---

## Analytics & Reporting

### Average Parking Duration

**Purpose:** Calculate average time vehicles park

**GUI:** Analytics Tab
**CLI:** Menu option 18

**Calculation:**
- Sum of all parking durations (allocation → release)
- Divided by completed sessions

**Example Output:**
```
Average Duration: 45.5 minutes
Completed Sessions: 8
```

**Use Cases:**
- Understand parking patterns
- Predict turnover
- Plan capacity

---

### Zone Utilization

**Purpose:** See how full each zone is

**GUI:** Analytics Tab → Progress bars
**CLI:** Menu option 19

**Calculation:**
- Utilization = (Occupied / Total Capacity) × 100%
- Sorted by utilization (highest first)

**Example Output:**
```
ZONE-A: 75.0% (15/20 occupied)
ZONE-B: 60.0% (15/25 occupied)
ZONE-C: 20.0% (2/10 occupied)
```

**Use Cases:**
- Identify busy zones
- Balance load
- Plan expansions

---

### Request Statistics

**Purpose:** Breakdown of requests by state

**GUI:** Analytics Tab
**CLI:** Menu option 20

**Information Shown:**
- Total requests
- Count by state (REQUESTED, ALLOCATED, OCCUPIED, RELEASED, CANCELLED)
- Completion rate (% of requests released)
- Cancellation rate (% of requests cancelled)

**Example Output:**
```
Total Requests: 15
Completed: 8 (53.33%)
Cancelled: 2 (13.33%)
Active (Requested): 1
Active (Allocated): 2
Active (Occupied): 2
```

**Use Cases:**
- Track success rate
- Identify cancellation patterns
- Monitor active requests

---

### Peak Usage Zone

**Purpose:** Find busiest zone

**GUI:** Analytics Tab
**CLI:** Menu option 21

**Calculation:**
- Find zone with highest utilization rate
- Linear search (max-finding)

**Example Output:**
```
Peak Usage Zone: ZONE-A
Utilization: 75.0%
Occupied: 15/20
Available: 5
```

**Use Cases:**
- Identify bottlenecks
- Focus maintenance on busy zones

---

### Cross-Zone Allocation Statistics

**Purpose:** See how often vehicles park outside requested zone

**GUI:** Analytics Tab
**CLI:** Menu option 22

**Calculation:**
- Same zone: requested_zone == allocated_zone
- Cross zone: requested_zone != allocated_zone
- Percentage of cross-zone allocations

**Example Output:**
```
Total Allocations: 10
Same Zone: 7 (70%)
Cross Zone: 3 (30%)
```

**Use Cases:**
- Evaluate zone layout
- Optimize zone adjacencies
- Assess user experience (lower cross-zone = better)

---

### Comprehensive Analytics

**Purpose:** All analytics in one report

**GUI:** Analytics Tab (default view)
**CLI:** Menu option 17

**Includes:**
- Average parking duration
- Zone utilization
- Request statistics
- Peak usage zone
- Cross-zone statistics

**Export (GUI only):**
- Click "Export Analytics Summary"
- Saves to `exports/summary/analytics_summary_YYYYMMDD_HHMMSS.txt`

---

## Advanced Features

### Rollback Operations

**Purpose:** Undo last k operations (stack-based)

**GUI:** Rollback Tab
**CLI:** Menu option 15

**How It Works:**
1. Every state-changing operation recorded in stack (LIFO)
2. Rollback pops k operations from stack
3. Each operation reverts to previous state

**Supported Operations:**
- ALLOCATE → Reverts to REQUESTED, frees slot
- CANCEL → Restores previous state
- OCCUPY → Reverts to ALLOCATED
- RELEASE → Reverts to OCCUPIED, re-occupies slot

**Instructions:**
1. Enter number of operations to rollback (k)
2. Confirm action
3. System reverts last k operations

**Example:**
```
Operations:
1. Allocate REQ0005
2. Occupy REQ0004
3. Allocate REQ0004

Rollback 2 operations:
→ Undo operation 3 (Allocate REQ0004)
→ Undo operation 2 (Occupy REQ0004)

Result: REQ0004 back to ALLOCATED, REQ0005 still allocated
```

**Tips:**
- Cannot rollback more than available operations
- Rollback is destructive (cannot redo without re-doing operations)
- Use carefully in production

**DSA Concept:** Stack (LIFO) data structure

---

### View Operation History

**Purpose:** See all recorded operations

**GUI:** Rollback Tab → History list
**CLI:** Menu option 16

**Information Shown:**
- Operation type (ALLOCATE, CANCEL, OCCUPY, RELEASE)
- Request ID
- Slot ID (if applicable)
- Ordered by recency (most recent first)

**Example Output:**
```
Total Operations: 12

#12: ALLOCATE - REQ0005 (Slot: ZONE-B-B1-3)
#11: OCCUPY - REQ0004
#10: ALLOCATE - REQ0004 (Slot: ZONE-A-A1-2)
#9: CANCEL - REQ0003
#8: RELEASE - REQ0002
...
```

**Use Cases:**
- Audit trail
- Verify rollback count
- Debug issues

---

## Common Workflows

### Workflow 1: Basic Parking Session

**Goal:** Park a vehicle and release

**Steps:**
1. **Setup:**
   - Add zone (e.g., ZONE-A)
   - Add parking area (e.g., A1, capacity 10)
   - Register vehicle (e.g., CAR-001)

2. **Parking:**
   - Create request (CAR-001 → ZONE-A)
   - Allocate parking → Get slot ZONE-A-A1-1
   - Mark as occupied → Vehicle parks

3. **Leaving:**
   - Release parking → Slot freed

**Result:** Completed session, slot available again

---

### Workflow 2: Cross-Zone Allocation

**Goal:** Allocate in adjacent zone when requested zone is full

**Steps:**
1. **Setup:**
   - Add ZONE-A (10 slots, all occupied)
   - Add ZONE-B (10 slots, 5 available)
   - Link ZONE-A ↔ ZONE-B
   - Register CAR-002

2. **Parking:**
   - Create request (CAR-002 → ZONE-A)
   - Allocate parking
   - ZONE-A full → Check adjacent ZONE-B
   - Allocated ZONE-B-B1-6 (penalty = 50)

**Result:** Vehicle parks in adjacent zone with penalty

---

### Workflow 3: Cancelling and Retrying

**Goal:** Cancel request and create new one

**Steps:**
1. Create request (CAR-003 → ZONE-C)
2. Allocate parking → ZONE-C-C1-1
3. Change of plans: Cancel request
4. Slot ZONE-C-C1-1 freed
5. Create new request (CAR-003 → ZONE-A)
6. Allocate in ZONE-A

**Result:** Slot reused for different zone

---

### Workflow 4: Using Rollback

**Goal:** Undo recent allocations

**Steps:**
1. Allocate REQ0010
2. Allocate REQ0011
3. Realize mistake
4. Rollback 2 operations
5. REQ0010 and REQ0011 back to REQUESTED
6. Slots freed

**Result:** System state as if allocations never happened

---

### Workflow 5: Analytics Review

**Goal:** Generate parking report

**Steps:**
1. Navigate to Analytics Tab (GUI) or Menu 17 (CLI)
2. Review all metrics
3. Export summary (GUI: click Export button)
4. File saved to `exports/summary/`

**Result:** Comprehensive analytics report

---

## Troubleshooting

### Problem: "Zone not found"

**Cause:** Zone ID doesn't exist or typo

**Solution:**
1. View all zones (Menu 13 or Dashboard)
2. Verify correct Zone ID
3. Add zone if missing

---

### Problem: "No available slots"

**Cause:** All slots in all zones are occupied

**Solution:**
1. View system status to check capacity
2. Release occupied slots
3. Add more parking areas
4. Wait for vehicles to leave

---

### Problem: "Cannot allocate - request is in CANCELLED state"

**Cause:** Trying to allocate a cancelled request

**Solution:**
1. Create a new request
2. Or rollback the cancellation operation

---

### Problem: "Invalid state transition"

**Cause:** Attempting invalid state change (e.g., REQUESTED → OCCUPIED)

**Solution:**
1. Follow correct sequence:
   - REQUESTED → ALLOCATED → OCCUPIED → RELEASED
2. Check current state (View Request Details)

---

### Problem: "Rollback failed - not enough operations"

**Cause:** Trying to rollback more operations than available

**Solution:**
1. View operation history (count operations)
2. Rollback fewer operations

---

### Problem: GUI window too small

**Cause:** Screen resolution or window resize

**Solution:**
1. Manually resize window (minimum 1000x650)
2. Maximize window
3. Check screen resolution

---

### Problem: Tkinter not found (Linux)

**Cause:** Tkinter not installed

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

---

## Best Practices

### Setup Phase

1. **Plan Zone Layout:**
   - Create zones matching physical layout
   - 3-10 zones for most systems
   - Use descriptive IDs

2. **Allocate Sufficient Capacity:**
   - 10-50 slots per area typical
   - Avoid too many small areas (harder to manage)
   - Balance zones evenly

3. **Link Adjacent Zones:**
   - Connect physically adjacent zones
   - Reduces cross-zone penalties
   - Improves user experience

4. **Register Vehicles Upfront:**
   - Batch registration faster than one-by-one
   - Use consistent ID format (CAR-001, CAR-002, ...)

---

### Operational Phase

1. **State Transitions:**
   - Always follow correct sequence
   - Don't skip states (e.g., REQUESTED → OCCUPIED invalid)
   - Mark occupied when vehicle arrives
   - Release when vehicle leaves

2. **Handle Failures:**
   - If allocation fails, check capacity
   - Consider cancelling and retrying
   - Use rollback sparingly (last resort)

3. **Monitor System:**
   - Check dashboard regularly
   - Watch for full zones
   - Review analytics periodically

---

### Analytics Phase

1. **Regular Reviews:**
   - Weekly analytics review
   - Track trends (utilization, duration, cancellations)
   - Identify patterns

2. **Export Reports:**
   - Export before major changes
   - Keep historical records
   - Compare time periods

3. **Act on Insights:**
   - High cross-zone percentage → Review zone layout
   - High cancellation rate → Investigate causes
   - Uneven utilization → Balance zones

---

### Rollback Usage

1. **Use Sparingly:**
   - Only for mistakes or testing
   - Not for normal operations
   - Destructive (cannot redo)

2. **Verify First:**
   - View operation history
   - Count operations carefully
   - Confirm rollback count

3. **Document:**
   - Note why rollback was needed
   - Track if rollback frequency increases (system issue?)

---

## Summary

**SmartPark User Guide Highlights:**

- **Setup:** Zones → Areas → Vehicles → Adjacencies
- **Operations:** Request → Allocate → Occupy → Release
- **Queries:** System status, zone status, request details
- **Analytics:** Duration, utilization, statistics, reports
- **Advanced:** Rollback (stack-based undo)

**Key Principles:**
- Follow state machine (valid transitions)
- Lower penalty is better (same zone = 0)
- Monitor system regularly
- Use analytics for insights
- Rollback only when necessary

**Interface Choice:**
- **GUI:** Visual, intuitive, dashboards
- **CLI:** Fast, scriptable, text-based

---

**For quick start, see [QUICK_START.md](QUICK_START.md)**  
**For interface details, see [UI.md](UI.md)**  
**For API reference, see [API.md](API.md)**  
**For DSA concepts, see [DSA_CONCEPTS.md](DSA_CONCEPTS.md)**
