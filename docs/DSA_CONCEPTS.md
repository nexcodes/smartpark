# SmartPark - Data Structures & Algorithms Concepts

This document explains the data structures and algorithms used in SmartPark, their implementations, complexity analysis, and educational rationale.

## Table of Contents

- [Overview](#overview)
- [Arrays (Python Lists)](#arrays-python-lists)
- [Stack (LIFO)](#stack-lifo)
- [Graph (Adjacency List)](#graph-adjacency-list)
- [State Machine](#state-machine)
- [Algorithm Analysis](#algorithm-analysis)
- [Design Trade-offs](#design-trade-offs)
- [Educational Insights](#educational-insights)

---

## Overview

SmartPark demonstrates **four fundamental data structures** in a practical parking management context:

1. **Arrays** — for slot storage and linear search
2. **Stack** — for undo/rollback operations
3. **Graph** — for zone relationships and cross-zone allocation
4. **State Machine** — for request lifecycle management

Each data structure is implemented **explicitly** with clear DSA patterns, prioritizing educational clarity over production optimization.

---

## Arrays (Python Lists)

### Implementation Locations

| Class | Array Usage | Purpose |
|-------|------------|---------|
| `Zone` | `parking_areas: list` | Store parking areas in a zone |
| `Zone` | `adjacent_zones: list` | Adjacency list for graph |
| `ParkingArea` | `slots: list` | Store parking slots |
| `ParkingSystem` | `request_history: list` | Chronological request log |

### Key Pattern: Linear Search

**Location:** `parking_area.py` → `find_available_slot()`

```python
def find_available_slot(self):
    for slot in self.slots:  # Linear traversal
        if slot.is_available:
            return slot      # Early return on first match
    return None              # No available slot
```

**Time Complexity:** O(n) where n = number of slots

**Space Complexity:** O(1) — no additional storage

### Why Linear Search?

**Rationale:**

1. **Dynamic Availability**: Slot availability changes constantly (allocate/release), making sorted structures impractical
2. **Small Dataset**: Typical parking areas have 10-50 slots; O(n) is acceptable
3. **Educational Focus**: Demonstrates classic array traversal pattern
4. **Simplicity**: Easy to understand for beginners

**Alternative (Not Used):**

Binary search requires:
- Sorted array (by availability → not stable)
- O(log n) search time
- O(n) sorting time on every change → worse overall performance

**Conclusion:** Linear search is optimal for this use case.

### Array Traversal Patterns

**Pattern 1: Linear Search with Early Return**

```python
# Find first match
for item in array:
    if condition(item):
        return item  # Stop immediately
return None
```

**Used in:**
- `Zone.find_available_slot()`
- `ParkingArea.find_available_slot()`

---

**Pattern 2: Full Traversal with Counter**

```python
# Count matching items
count = 0
for item in array:
    if condition(item):
        count += 1
return count
```

**Used in:**
- `ParkingArea.get_available_count()`
- `Zone.get_available_count()`

---

**Pattern 3: Nested Traversal (2D Array)**

```python
# Search across multiple arrays
for outer in outer_array:
    for inner in outer.inner_array:
        if condition(inner):
            return inner
return None
```

**Used in:**
- `Zone.find_available_slot()` → iterates areas → iterates slots
- `ParkingSystem._find_slot()` → iterates zones → areas → slots

**Complexity:** O(n × m) where n = outer items, m = inner items

---

**Pattern 4: Accumulation**

```python
# Sum values
total = 0
for item in array:
    total += item.value
return total
```

**Used in:**
- `Zone.get_total_capacity()` → sums area capacities
- `AnalyticsEngine.get_average_parking_duration()` → sums durations

---

### Array Operations Complexity

| Operation | Time | Space | Location |
|-----------|------|-------|----------|
| Append (add slot) | O(1) amortized | O(1) | `ParkingArea.__init__()` |
| Linear search | O(n) | O(1) | `find_available_slot()` |
| Count matching | O(n) | O(1) | `get_available_count()` |
| Nested search | O(n×m) | O(1) | `_find_slot()` |
| Full traversal | O(n) | O(1) | Analytics methods |

---

## Stack (LIFO)

### Implementation Location

**Class:** `RollbackManager`  
**Data Structure:** `operation_stack: list`

### Stack Operations

**1. Push (Record Operation)**

```python
def record_allocation(self, slot, request):
    operation = Operation(...)  # Create operation object
    self.operation_stack.append(operation)  # Push to stack
```

**Complexity:** O(1)

---

**2. Pop (Rollback)**

```python
def rollback(self, k, zones, requests_dict):
    for _ in range(k):
        operation = self.operation_stack.pop()  # Pop from top (LIFO)
        self._reverse_operation(operation)       # Undo the operation
```

**Complexity:** O(k) where k = number of operations to rollback

---

**3. Peek (View History)**

```python
# View last operation without removing
last_operation = self.operation_stack[-1] if self.operation_stack else None
```

**Complexity:** O(1)

---

### Why Stack for Rollback?

**LIFO (Last-In-First-Out) Semantics:**

```
Operations: [Op1, Op2, Op3, Op4]
                              ↑
                         (most recent)

Undo last 2:
1. Pop Op4 → Undo Op4
2. Pop Op3 → Undo Op3

Result: State as if Op3 and Op4 never happened
```

**Benefits:**

1. **Natural Undo Behavior**: Users expect to undo recent actions first
2. **O(1) Push/Pop**: Constant time operations
3. **Simple Implementation**: Python list as stack with `append()` and `pop()`
4. **Complete State Storage**: Each operation stores previous state for perfect reversal

### Operation Object Structure

```python
class Operation:
    operation_type: str          # ALLOCATE, CANCEL, OCCUPY, RELEASE
    slot_id: str                 # Affected slot
    slot_previous_availability: bool
    slot_previous_vehicle_id: str | None
    request_id: str              # Affected request
    request_previous_state: RequestState
    request_previous_allocated_slot: str | None
    request_previous_allocated_zone: str | None
```

**Key Insight:** Each operation stores **complete previous state**, enabling **idempotent reversal** (rollback can be applied multiple times).

### Example: Rollback Allocation

**Operation Recorded:**

```python
Operation(
    type='ALLOCATE',
    slot_id='ZONE-A-A1-1',
    slot_previous_availability=True,        # Was available
    slot_previous_vehicle_id=None,          # Was empty
    request_previous_state=REQUESTED,       # Was not allocated
    request_previous_allocated_slot=None    # Had no slot
)
```

**Rollback Execution:**

```python
# Restore slot
slot.is_available = True          # Free the slot
slot.occupied_vehicle_id = None   # Remove vehicle

# Restore request
request.current_state = REQUESTED          # Back to requested
request.allocated_slot_id = None           # Remove allocation
request.allocated_zone = None              # Remove zone
```

**Result:** System state as if allocation never happened.

### Stack Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Push (record) | O(1) | O(1) per operation | Constant time append |
| Pop (rollback 1) | O(1) | O(1) | Constant time pop |
| Rollback k | O(k) | O(k) | Linear in operations |
| View history | O(n) | O(1) | Iterate stack |
| Stack storage | — | O(n) | n = total operations |

---

## Graph (Adjacency List)

### Implementation Location

**Class:** `Zone`  
**Data Structure:** `adjacent_zones: list`

### Graph Structure

**Zones as Nodes:**

```python
class Zone:
    zone_id: str                  # Node identifier
    adjacent_zones: list          # Adjacency list (edges)
    parking_areas: list           # Node data
```

**Example Graph:**

```
Zone A: adjacent_zones = ['ZONE-B', 'ZONE-C']
Zone B: adjacent_zones = ['ZONE-A', 'ZONE-D']
Zone C: adjacent_zones = ['ZONE-A']
Zone D: adjacent_zones = ['ZONE-B']
```

**Visual Representation:**

```
    A ←→ B ←→ D
    ↕
    C
```

### Graph Operations

**1. Add Vertex (Zone)**

```python
def add_zone(self, zone_id):
    zone = Zone(zone_id)
    self.zones[zone_id] = zone
```

**Complexity:** O(1)

---

**2. Add Edge (Link Zones)**

```python
def link_adjacent_zones(self, zone1_id, zone2_id):
    # Bidirectional edge
    self.zones[zone1_id].add_adjacent_zone(zone2_id)
    self.zones[zone2_id].add_adjacent_zone(zone1_id)
```

**Complexity:** O(1) — append to adjacency lists

**Graph Type:** Undirected (edges are bidirectional)

---

**3. Graph Traversal (Allocation)**

```python
def allocate_slot(self, parking_request):
    requested_zone = parking_request.requested_zone
    
    # Step 1: Check same zone (0-hop)
    if slot_available_in(requested_zone):
        return allocate(penalty=0)
    
    # Step 2: Check adjacent zones (1-hop)
    for adjacent_zone_id in requested_zone.adjacent_zones:
        if slot_available_in(adjacent_zone_id):
            return allocate(penalty=50)
    
    # Step 3: Check all other zones (2+ hops)
    for zone_id in all_zones:
        if zone_id not in [requested, *adjacent_zones]:
            if slot_available_in(zone_id):
                return allocate(penalty=100)
```

**Complexity:**
- Same zone: O(m) — search slots in zone
- Adjacent zones: O(k × m) — k adjacent zones, m slots each
- All zones: O(n × m) — n zones, m slots each

**Total Worst Case:** O(n × m)

---

### Why Adjacency List?

**Advantages:**

1. **Space Efficiency**: Only store actual edges, not full matrix
2. **Dynamic Graph**: Easy to add/remove zones and edges
3. **Sparse Graph**: Parking lots typically have few adjacent zones
4. **Educational Value**: Demonstrates classic graph representation

**Space Complexity:**

- Adjacency List: O(V + E) where V = zones, E = edges
- Adjacency Matrix: O(V²) — wasteful for sparse graphs

**Example:**

```
5 zones, 6 edges (sparse graph):
- Adjacency List: 5 + 6 = 11 storage units
- Adjacency Matrix: 5 × 5 = 25 storage units
```

### Graph Algorithms

**Simplified BFS (Breadth-First Search):**

SmartPark uses a **simplified BFS** approach:

```
Level 0: Requested zone (same zone)
Level 1: Adjacent zones (1-hop neighbors)
Level 2+: All other zones (distant)
```

**Why Not Full BFS?**

- Full BFS would traverse zones by exact distance (2-hop, 3-hop, etc.)
- SmartPark simplifies to 3 tiers: same, adjacent, distant
- **Educational Trade-off**: Demonstrates adjacency lists without complex queue-based BFS

**Full BFS Implementation (Not Used):**

```python
from collections import deque

def bfs_allocate(start_zone):
    queue = deque([start_zone])
    visited = set()
    
    while queue:
        zone = queue.popleft()
        if zone in visited:
            continue
        visited.add(zone)
        
        if slot_available_in(zone):
            return allocate(zone)
        
        for adjacent in zone.adjacent_zones:
            queue.append(adjacent)
```

**Why Not Implemented:** Overkill for typical 3-10 zone parking systems; simplified version is sufficient and more understandable.

### Graph Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Add vertex (zone) | O(1) | O(1) | Dictionary insert |
| Add edge (link zones) | O(1) | O(1) | Append to list |
| Check adjacency | O(k) | O(1) | k = adjacent zones |
| Traverse 1-hop neighbors | O(k) | O(1) | Iterate adjacency list |
| Full graph traversal | O(V + E) | O(V) | V vertices, E edges |

---

## State Machine

### Implementation Location

**Enum:** `RequestState` in `enums.py`  
**Validation:** `is_valid_transition()`

### State Diagram

```
         ┌──────────┐
    ┌────┤ REQUESTED├────┐
    │    └──────────┘    │
    │         │          │
    │         ↓          ↓
    │    ┌─────────┐  ┌───────────┐
    │    │ALLOCATED│  │ CANCELLED │ (terminal)
    │    └─────────┘  └───────────┘
    │         │
    │         ↓
    │    ┌────────┐
    └───→│OCCUPIED│
         └────────┘
              │
              ↓
         ┌─────────┐
         │RELEASED │ (terminal)
         └─────────┘
```

### State Transition Rules

```python
valid_transitions = {
    REQUESTED: [ALLOCATED, CANCELLED],
    ALLOCATED: [OCCUPIED, CANCELLED],
    OCCUPIED:  [RELEASED],
    RELEASED:  [],  # Terminal state
    CANCELLED: []   # Terminal state
}
```

### Validation Implementation

```python
@staticmethod
def is_valid_transition(from_state, to_state):
    valid_transitions = {
        RequestState.REQUESTED: [RequestState.ALLOCATED, RequestState.CANCELLED],
        RequestState.ALLOCATED: [RequestState.OCCUPIED, RequestState.CANCELLED],
        RequestState.OCCUPIED:  [RequestState.RELEASED],
        RequestState.RELEASED:  [],
        RequestState.CANCELLED: []
    }
    return to_state in valid_transitions.get(from_state, [])
```

**Time Complexity:** O(1) — dictionary lookup + list membership check (small constant)

**Space Complexity:** O(1) — fixed-size transition table

### State Machine Enforcement

**Enforcement Point:** `ParkingRequest.change_state()`

```python
def change_state(self, new_state):
    if RequestState.is_valid_transition(self.current_state, new_state):
        self.current_state = new_state
        # Update timestamps
        return True
    else:
        print(f"Invalid transition: {self.current_state} -> {new_state}")
        return False
```

**Used By:**
- `allocate_slot()` → REQUESTED → ALLOCATED
- `mark_parking_occupied()` → ALLOCATED → OCCUPIED
- `release_parking()` → OCCUPIED → RELEASED
- `cancel_request()` → REQUESTED/ALLOCATED → CANCELLED

### Why State Machine?

**Benefits:**

1. **Prevents Invalid States**: Cannot release a REQUESTED slot, cannot occupy a CANCELLED request
2. **Clear Lifecycle**: Visual diagram shows all possible paths
3. **Easy Debugging**: Invalid transitions logged with clear messages
4. **Rollback Safety**: Rollback validates state restoration

**Example Invalid Transition:**

```python
request.current_state = REQUESTED
request.change_state(OCCUPIED)  # Invalid!
# Output: "Invalid transition: REQUESTED -> OCCUPIED"
# State unchanged
```

**Correct Path:**

```python
request.current_state = REQUESTED
request.change_state(ALLOCATED)   # Valid ✓
request.change_state(OCCUPIED)    # Valid ✓
request.change_state(RELEASED)    # Valid ✓
```

### State Machine Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Validate transition | O(1) | O(1) |
| Change state | O(1) | O(1) |
| Store transition rules | — | O(s²) worst case (s = states) |

**SmartPark:** 5 states → O(25) = O(1) constant space

---

## Algorithm Analysis

### 1. Slot Allocation Algorithm

**Location:** `AllocationEngine.allocate_slot()`

**Pseudocode:**

```
function allocate_slot(request):
    // Priority 1: Same zone
    slot = search_zone(request.requested_zone)
    if slot found:
        return {success, penalty=0}
    
    // Priority 2: Adjacent zones
    for each adjacent_zone in requested_zone.adjacent_zones:
        slot = search_zone(adjacent_zone)
        if slot found:
            return {success, penalty=50}
    
    // Priority 3: All other zones
    for each zone in all_zones:
        if zone not in [requested, adjacent_zones]:
            slot = search_zone(zone)
            if slot found:
                return {success, penalty=100}
    
    return {failure}
```

**Complexity Analysis:**

- **Best Case:** O(m) — slot found in requested zone
  - m = slots in zone
  - Single zone search

- **Average Case:** O(k × m) — slot found in adjacent zone
  - k = adjacent zones (typically 2-4)
  - Search k zones, each with m slots

- **Worst Case:** O(n × m) — full scan required
  - n = total zones
  - m = slots per zone
  - All zones searched

**Space Complexity:** O(1) — no additional storage (iterate in place)

---

### 2. Rollback Algorithm

**Location:** `RollbackManager.rollback()`

**Pseudocode:**

```
function rollback(k):
    for i = 1 to k:
        operation = operation_stack.pop()  // O(1)
        
        switch operation.type:
            case ALLOCATE:
                restore_slot_availability(operation)     // O(1)
                restore_request_state(operation)         // O(1)
            case CANCEL:
                restore_slot_and_request(operation)      // O(1)
            case OCCUPY:
                restore_request_state(operation)         // O(1)
            case RELEASE:
                restore_slot_and_request(operation)      // O(1)
    
    return success
```

**Complexity Analysis:**

- **Time Complexity:** O(k)
  - k operations to rollback
  - Each operation: O(1) restore

- **Space Complexity:** O(1)
  - No additional storage during rollback
  - Stack space: O(n) where n = total operations (pre-existing)

---

### 3. Analytics Algorithms

#### Average Parking Duration

```
function get_average_parking_duration():
    total = 0
    count = 0
    
    for each request in requests:              // O(n)
        if request.state == RELEASED:
            total += request.duration()
            count += 1
    
    return total / count if count > 0 else 0
```

**Time Complexity:** O(n) where n = total requests  
**Space Complexity:** O(1)

---

#### Zone Utilization

```
function get_zone_utilization():
    zone_stats = []
    
    for each zone in zones:                    // O(z)
        total_capacity = 0
        occupied = 0
        
        for each area in zone.areas:           // O(a)
            for each slot in area.slots:       // O(s)
                total_capacity += 1
                if not slot.available:
                    occupied += 1
        
        utilization = (occupied / total_capacity) * 100
        zone_stats.append({zone, utilization})
    
    sort(zone_stats by utilization)            // O(z log z)
    return zone_stats
```

**Time Complexity:** O(z × a × s + z log z)
- z = zones, a = areas/zone, s = slots/area
- Simplifies to O(n × m + n log n) where n = zones, m = total slots/zone

**Space Complexity:** O(z) for zone_stats array

---

#### Peak Usage Zone

```
function get_peak_usage_zone():
    peak_zone = null
    peak_utilization = -1
    
    for each zone in zones:                    // O(z)
        utilization = calculate_utilization(zone)  // O(m)
        
        if utilization > peak_utilization:
            peak_utilization = utilization
            peak_zone = zone
    
    return peak_zone
```

**Time Complexity:** O(n × m) where n = zones, m = slots/zone  
**Space Complexity:** O(1)

---

### 4. Search Algorithms

#### Linear Slot Search

```
function find_available_slot(slots):
    for i = 0 to len(slots) - 1:               // O(n)
        if slots[i].is_available:
            return slots[i]
    
    return null
```

**Time Complexity:** O(n)  
**Space Complexity:** O(1)

---

#### Nested Zone Search

```
function find_slot_by_id(slot_id, zones):
    for each zone in zones:                    // O(z)
        for each area in zone.areas:           // O(a)
            for each slot in area.slots:       // O(s)
                if slot.id == slot_id:
                    return slot
    
    return null
```

**Time Complexity:** O(z × a × s) = O(n) where n = total slots  
**Space Complexity:** O(1)

---

## Design Trade-offs

### 1. Linear Search vs Binary Search

**Decision:** Use linear search for slots

**Rationale:**

| Factor | Linear Search | Binary Search |
|--------|--------------|---------------|
| Time per search | O(n) | O(log n) |
| Sorting overhead | None | O(n log n) per change |
| Code complexity | Low | High |
| Dataset size | 10-50 slots | Beneficial > 1000 |
| Dynamic data | ✓ Handles well | ✗ Re-sort needed |

**Conclusion:** For n < 50, linear search is faster overall due to no sorting overhead.

---

### 2. Adjacency List vs Adjacency Matrix

**Decision:** Use adjacency list for zones

**Rationale:**

| Factor | Adjacency List | Adjacency Matrix |
|--------|---------------|-----------------|
| Space | O(V + E) | O(V²) |
| Check adjacency | O(k) | O(1) |
| Add vertex | O(1) | O(V²) resize |
| Typical graph | Sparse (few edges) | Dense (many edges) |

**SmartPark Context:**
- 5-10 zones (sparse graph)
- 2-4 adjacent zones per zone
- Adjacency list: 15-40 storage units
- Matrix: 25-100 storage units

**Conclusion:** Adjacency list is more space-efficient for sparse parking graphs.

---

### 3. Full BFS vs Simplified Tiers

**Decision:** Use 3-tier system (same, adjacent, distant)

**Rationale:**

| Factor | Full BFS | Simplified Tiers |
|--------|---------|------------------|
| Distance accuracy | Exact (2-hop, 3-hop, etc.) | Approximate (1-hop vs 2+) |
| Implementation | Queue, visited set | Simple iteration |
| Time complexity | O(V + E) | O(V) |
| Understandability | Complex | Intuitive |

**SmartPark Context:**
- Small graphs (5-10 zones)
- User penalty understanding: "adjacent" vs "far" is clear
- Educational focus: demonstrate adjacency lists without complex BFS

**Conclusion:** Simplified tiers provide sufficient functionality with better clarity.

---

### 4. In-Memory vs Database

**Decision:** Use in-memory data structures (dictionaries, lists)

**Rationale:**

| Factor | In-Memory | Database |
|--------|-----------|----------|
| Setup | Zero | Install DB, schema |
| DSA visibility | ✓ Clear in code | ✗ Hidden in DB |
| Performance | O(1) lookups | Network overhead |
| Persistence | ✗ Lost on restart | ✓ Persistent |
| Educational value | ✓ High | ✗ Low for DSA |

**SmartPark Context:**
- Educational project (DSA demonstration)
- No production deployment
- Acceptable to lose data on restart

**Conclusion:** In-memory structures align with educational goals.

---

## Educational Insights

### What This Project Teaches

**1. Arrays:**
- Linear search patterns (early return, full traversal)
- Nested iteration (2D arrays)
- Accumulation and counting
- Why linear search can be optimal

**2. Stacks:**
- LIFO (Last-In-First-Out) semantics
- Undo/rollback implementation
- Storing complete state for reversal
- O(1) push/pop operations

**3. Graphs:**
- Adjacency list representation
- Undirected graphs (bidirectional edges)
- Simplified BFS traversal
- Sparse vs dense graphs

**4. State Machines:**
- Finite state automaton design
- Transition validation
- Preventing invalid states
- Lifecycle management

**5. Algorithm Analysis:**
- Time complexity (O-notation)
- Best/average/worst case analysis
- Space complexity
- Trade-offs (optimization vs simplicity)

### Key Takeaways

1. **Context Matters**: Optimal data structure depends on dataset size, operation frequency, and use case
2. **Simplicity Has Value**: Simple solutions often outperform complex ones for small datasets
3. **Document Complexity**: Explicit O-notation helps understand performance
4. **Real-World Application**: DSA isn't just theory — parking systems use these concepts
5. **Trade-offs Exist**: Every design choice has pros/cons; document your reasoning

### Exercises for Learners

**1. Modify Array Search:**
- Implement priority slot search (prefer closer slots)
- Add slot reservation (maintain reserved_slots array)

**2. Extend Stack:**
- Add redo functionality (maintain redo_stack)
- Limit stack size (circular buffer)

**3. Enhance Graph:**
- Implement full BFS for exact distance calculation
- Add weighted edges (different penalties per zone pair)

**4. State Machine:**
- Add new states (e.g., RESERVED, OVERDUE)
- Implement state timeouts (auto-release after duration)

**5. Optimize Analytics:**
- Cache metrics (invalidate on state change)
- Use heaps for top-k queries (top 5 peak zones)

---

## Summary

**SmartPark DSA Implementation:**

| Data Structure | Implementation | Use Case | Complexity |
|---------------|---------------|----------|-----------|
| **Array** | Python list | Slot storage, search | O(n) search |
| **Stack** | Python list (LIFO) | Rollback operations | O(1) push/pop |
| **Graph** | Adjacency list | Zone relationships | O(V + E) storage |
| **State Machine** | Enum + transitions | Request lifecycle | O(1) validation |

**Key Algorithms:**

| Algorithm | Purpose | Complexity |
|-----------|---------|-----------|
| Linear search | Find available slot | O(n) |
| Priority allocation | Same→adjacent→distant | O(n × m) worst |
| LIFO rollback | Undo operations | O(k) |
| Array traversal | Analytics metrics | O(n) |

**Educational Value:**

- ✅ Practical DSA application (not just theory)
- ✅ Explicit complexity documentation
- ✅ Clear trade-off explanations
- ✅ Multiple patterns demonstrated (search, traversal, accumulation)
- ✅ Real-world context (parking management)

---

**For implementation details, see [ARCHITECTURE.md](ARCHITECTURE.md)**  
**For API reference, see [API.md](API.md)**  
**For usage instructions, see [USER_GUIDE.md](USER_GUIDE.md)**
