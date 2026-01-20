# SmartPark - AI Agent Instructions

## Project Overview
SmartPark is a **DSA-focused** parking management system demonstrating practical implementations of arrays, stacks, graphs, and state machines. This is an educational project with explicit emphasis on data structure choices and algorithmic complexity.

## Architecture

**Hierarchical Structure:** `ParkingSystem` → `Zone` (graph nodes) → `ParkingArea` (arrays) → `ParkingSlot`

**Key Components:**
- `parking_system.py` - Main orchestrator, holds all global state (zones, vehicles, requests)
- `allocation_engine.py` - Slot allocation with 3-tier priority (same-zone→adjacent→distant)
- `rollback_manager.py` - Stack-based undo using LIFO operations
- `zone.py` - Graph node with adjacency list for cross-zone navigation
- `enums.py` - State machine with validated transitions (REQUESTED→ALLOCATED→OCCUPIED→RELEASED)
- `analytics.py` - Metrics engine with array traversal patterns

**Data Flow:**
```
Request → AllocationEngine tries same-zone → adjacent zones (penalty=50) → distant zones (penalty=100)
All operations recorded in RollbackManager stack for undo
```

## DSA Implementation Patterns

### Arrays (Python Lists)
- **Used for:** Parking slots within areas, areas within zones, adjacency lists
- **Pattern:** Linear search with early return (e.g., `zone.find_available_slot()`)
- **Why not optimized?** Educational focus; typical zone size (10-50 slots) doesn't warrant binary search

### Stack (LIFO)
- **Implementation:** `rollback_manager.operation_stack` 
- **Operations:** Record allocation/cancel/release as `Operation` objects, pop for undo
- **Critical:** Each operation stores previous state for perfect rollback

### Graph (Custom Adjacency List)
- **Implementation:** Each `Zone` has `adjacent_zones` array
- **Traversal:** BFS-style in `allocation_engine.py` (adjacent zones before distant)
- **Bidirectional:** Use `link_adjacent_zones()` to create two-way edges

### State Machine
- **Enum:** `RequestState` with validated transitions via `is_valid_transition()`
- **Enforce:** All state changes must pass validation (see `parking_request.py`)

## Coding Conventions

### Return Format (CRITICAL)
All public methods return dicts with `success`, `message`, plus context-specific keys:
```python
{'success': True, 'message': 'Allocated...', 'slot_id': 'ZONE-A-A1-1', 'penalty': 50}
```

### Naming
- **IDs:** UPPERCASE with hyphens (e.g., `ZONE-A`, `CAR-001`)
- **Generated IDs:** Format `{zone_id}-{area_id}-{slot_number}` for slots
- **Request IDs:** Auto-incremented integers starting from 1

### Validation Pattern
Check preconditions first, return early with error dict:
```python
if zone_id not in self.zones:
    return {'success': False, 'message': f'Zone {zone_id} not found'}
```

## Development Workflows

### Running the System
```bash
# CLI Interface (23 menu operations)
cd src
python main.py

# GUI Interface (Tkinter, 6 tabs)
cd src
python gui_main.py
```

### Testing a Feature
Create scripts in project root:
```python
from src.parking_system import ParkingSystem
system = ParkingSystem()
# Setup zones, areas, then test
```

### Adding a New Operation
1. Add method to `ParkingSystem` (returns dict)
2. If modifies state, record in `RollbackManager`
3. Add menu option in `main.py` with input validation
4. For GUI: add to appropriate `ui/` screen with event handlers
5. Update `DOCUMENTATION_UPDATES.md` (if exists)

## Critical Implementation Details

### Allocation Engine Priority
1. **Same zone (penalty=0):** Direct lookup in requested zone
2. **Adjacent zones (penalty=50):** Iterate `zone.adjacent_zones`
3. **All other zones (penalty=100):** Full scan excluding above

**Time Complexity:** O(m) best case, O(n×m) worst case (n zones, m slots/zone)

### State Transitions
Valid paths only:
- `REQUESTED` → `ALLOCATED` or `CANCELLED`
- `ALLOCATED` → `OCCUPIED` or `CANCELLED`  
- `OCCUPIED` → `RELEASED`

### Rollback Logic
Each `Operation` stores:
- Previous state of slot (availability, vehicle_id)
- Previous state of request (state, allocated_slot, allocated_zone)
- Rollback inverts: allocate→release, cancel→restore

### Analytics Traversal
Analytics methods use array iteration patterns:
```python
# Pattern: traverse all requests, filter by state, accumulate
for request in self.parking_system.requests.values():
    if request.current_state == RequestState.RELEASED:
        total_duration += request.get_parking_duration()
```

## Common Patterns

### Finding Slots
```python
# Zone level (delegates to areas)
slot = zone.find_available_slot()  # Returns first available or None

# Area level (linear search)
for slot in self.slots:
    if slot.is_available:
        return slot
```

### Recording Operations
```python
# After successful allocation
self.rollback_manager.record_allocation(slot, request)
```

### Graph Traversal
```python
# AllocationEngine pattern
for adjacent_zone_id in requested_zone.adjacent_zones:
    adj_zone = self.zones[adjacent_zone_id]
    slot = adj_zone.find_available_slot()
    if slot: return allocate_with_penalty(50)
```

## Avoiding Common Mistakes

- **Don't** modify state in `allocation_engine.py` - it only finds slots, `parking_system.py` commits changes
- **Don't** bypass state validation - always use `is_valid_transition()`
- **Don't** forget to record operations in rollback manager for reversible actions
- **Don't** use binary search on unsorted/dynamic arrays (slots change availability)
- **Don't** import Tkinter in non-GUI modules - keep `ui/` isolated

## Dual Interface Architecture

### CLI (`main.py`)
- 23 menu operations organized in 6 categories
- Verbose print output with emojis (✅, ❌, ℹ️)
- Input validation with `.strip().upper()` for IDs

### GUI (`gui_main.py` + `ui/`)
- Tkinter notebook with 6 tabs: Setup, Dashboard, Request, Status, Rollback, Analytics
- Shared backend: both interfaces use same `ParkingSystem` instance
- Pattern: Screen classes inherit from `tk.Frame`, call `parking_system` methods
- Key files: `main_window.py` (navigation), individual screens for each tab

## Documentation Structure

- `docs/DSA_CONCEPTS.md` - Detailed DSA rationale (read before optimizing)
- `docs/ARCHITECTURE.md` - Component interactions, algorithms
- `docs/QUICK_START.md` - Working examples (copy patterns from here)
- `planning/roadmap.md` - Future features (check before proposing ideas)

## Project Constraints

- **Pure Python:** No external dependencies except Tkinter (standard library)
- **DSA Focus:** Prioritize demonstrating concepts over production optimization
- **Dual Interface:** CLI and GUI both supported, share backend logic
