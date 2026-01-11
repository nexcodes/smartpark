# Architecture & Design

Detailed system architecture and design decisions for the SmartPark system.

---

## System Overview

SmartPark is a hierarchical parking management system that organizes parking resources in a multi-level structure:

```
City/Campus
    └── Zones (e.g., ZONE-A, ZONE-B)
        └── Parking Areas (e.g., A1, A2)
            └── Parking Slots (e.g., ZONE-A-A1-1)
```

---

## Component Architecture

### 1. Main Controller: ParkingSystem

**Responsibility:** Orchestrates all system operations

**Key Attributes:**
- `zones`: Dictionary of zone_id → Zone objects
- `vehicles`: Dictionary of vehicle_id → Vehicle objects
- `requests`: Dictionary of request_id → ParkingRequest objects
- `allocation_engine`: AllocationEngine instance
- `rollback_manager`: RollbackManager instance
- `request_history`: List-based history (future: linked list)

**Design Decisions:**
- Single entry point for all operations
- Maintains global state
- Delegates allocation logic to AllocationEngine
- Delegates rollback to RollbackManager

---

### 2. Allocation Engine

**Responsibility:** Implements intelligent slot allocation algorithm

**Algorithm Flow:**

```
allocate_slot(parking_request):
    1. Validate request state (must be REQUESTED)
    2. Try same-zone allocation (penalty = 0)
       └─ If found: allocate and return
    3. Try adjacent zones (penalty = 50)
       └─ For each adjacent zone:
          └─ If slot found: allocate and return
    4. Try all other zones (penalty = 100)
       └─ For each remaining zone:
          └─ If slot found: allocate and return
    5. Return failure (no slots available)
```

**Priority Levels:**

| Priority | Target | Penalty | Strategy |
|----------|--------|---------|----------|
| 1 | Same zone | 0 | Direct lookup |
| 2 | Adjacent zones | 50 | Graph traversal |
| 3 | Distant zones | 100 | Full search |

**Time Complexity:**
- Best case: O(m) - slot found in same zone (m = slots per zone)
- Worst case: O(n×m) - all zones searched (n = zones)

---

### 3. Rollback Manager

**Responsibility:** Undo operations using stack

**Data Structure:**

```python
Stack (LIFO):
    [Operation n]  ← Top (most recent)
    [Operation n-1]
    [Operation n-2]
    ...
    [Operation 1]
```

**Operation Record:**

```python
class Operation:
    - operation_type: ALLOCATE | CANCEL | RELEASE
    - slot_id: Affected slot
    - slot_previous_availability: bool
    - slot_previous_vehicle_id: str
    - request_id: Affected request
    - request_previous_state: RequestState
    - request_previous_allocated_slot: str
    - request_previous_allocated_zone: str
```

**Rollback Process:**

```
rollback_last_operation():
    1. Pop operation from stack
    2. Restore slot state:
       - availability = previous_availability
       - vehicle_id = previous_vehicle_id
    3. Restore request state:
       - state = previous_state
       - allocated_slot = previous_slot
       - allocated_zone = previous_zone
    4. Return success
```

**Limitations:**
- Only undoes last operation
- Cannot selectively undo
- Cannot redo after rollback

---

### 4. Zone Graph

**Responsibility:** Model zone relationships for cross-zone allocation

**Implementation:**

```
Adjacency List (Custom Array-based):

ZONE-A: [ZONE-B, ZONE-C]
ZONE-B: [ZONE-A, ZONE-D]
ZONE-C: [ZONE-A]
ZONE-D: [ZONE-B]
```

**Operations:**

```python
add_adjacent_zone(zone_id):
    # Add to adjacency list (bidirectional)
    self.adjacent_zones.append(zone_id)

get_adjacent_zones():
    # Return array of adjacent zone IDs
    return self.adjacent_zones
```

**Graph Properties:**
- Undirected (bidirectional edges)
- Unweighted
- No self-loops
- Can have cycles

**Example Topology:**

```
    A ─── B ─── C
    │           │
    │           │
    D ─────────┘
```

---

### 5. State Machine

**Responsibility:** Enforce valid request lifecycle transitions

**States:**

```
┌─────────────┐
│  REQUESTED  │ ← Initial
└──────┬──────┘
       │
       ├─────────┐
       │         │
       ▼         ▼
┌─────────┐  ┌──────────┐
│ALLOCATED│  │CANCELLED │ ← Terminal
└────┬────┘  └──────────┘
     │
     ├─────────┐
     │         │
     ▼         ▼
┌────────┐  ┌──────────┐
│OCCUPIED│  │CANCELLED │
└────┬───┘  └──────────┘
     │
     ▼
┌────────┐
│RELEASED│ ← Terminal
└────────┘
```

**Validation:**

```python
is_valid_transition(from_state, to_state):
    valid_transitions = {
        REQUESTED: [ALLOCATED, CANCELLED],
        ALLOCATED: [OCCUPIED, CANCELLED],
        OCCUPIED: [RELEASED],
        RELEASED: [],
        CANCELLED: []
    }
    return to_state in valid_transitions[from_state]
```

**State Meanings:**

| State | Meaning | Slot Status |
|-------|---------|-------------|
| REQUESTED | Created, not yet allocated | None |
| ALLOCATED | Slot assigned, not yet parked | Reserved |
| OCCUPIED | Vehicle parked | Occupied |
| RELEASED | Vehicle left, slot freed | Available |
| CANCELLED | Request cancelled | Available (if was allocated) |

---

## Data Structure Choices

### Arrays (Python Lists)

**Used For:**
- Parking slots within areas
- Parking areas within zones
- Adjacency lists

**Advantages:**
- O(1) index access
- Simple iteration
- Low memory overhead

**Disadvantages:**
- O(n) search for available slots
- Fixed capacity (though Python lists are dynamic)

**Alternative Considered:**
- Binary heap for slot availability (rejected: overkill)
- Bitmap for availability (rejected: harder to debug)

---

### Stack (Python List)

**Used For:**
- Rollback operation history

**Advantages:**
- O(1) push/pop operations
- Natural LIFO behavior
- Simple implementation

**Why Not Queue?**
- Need to undo LAST operation, not FIRST

---

### Graph (Adjacency List)

**Used For:**
- Zone relationships

**Advantages:**
- Efficient adjacent zone lookup
- Flexible topology
- Easy to add/remove edges

**Why Not Adjacency Matrix?**
- Sparse connections (few adjacent zones)
- O(n²) space wasteful
- List more flexible

---

### Hash Map (Python Dict)

**Used For:**
- Zone lookup by ID
- Vehicle lookup by ID
- Request lookup by ID

**Advantages:**
- O(1) average-case lookup
- Natural key-value pairing
- Built-in Python support

**Why Not Array?**
- Need fast lookup by ID
- Don't need ordering

---

## Design Patterns

### 1. Strategy Pattern

**Where:** AllocationEngine

**Purpose:** Encapsulate allocation algorithm

**Benefits:**
- Can swap allocation strategies
- Testable independently
- Single Responsibility Principle

---

### 2. State Pattern

**Where:** ParkingRequest with RequestState

**Purpose:** Manage request lifecycle

**Benefits:**
- Invalid transitions impossible
- Clear state semantics
- Easy to add states

---

### 3. Facade Pattern

**Where:** ParkingSystem

**Purpose:** Simplify complex subsystem

**Benefits:**
- Single API for users
- Hide internal complexity
- Easier to use

---

### 4. Command Pattern (Implicit)

**Where:** Rollback operations

**Purpose:** Encapsulate operations as objects

**Benefits:**
- Can undo operations
- Operation history
- Audit trail

---

## Scalability Considerations

### Current Limitations

1. **Memory:** All data in RAM
   - Solution: Database persistence

2. **Search:** Linear slot search
   - Solution: Indexing available slots

3. **Concurrency:** No thread safety
   - Solution: Locking mechanisms

4. **Rollback:** Only last operation
   - Solution: Full command history

---

### Scaling to Production

**For 1,000 slots:**
- Current design sufficient
- In-memory fine

**For 10,000 slots:**
- Consider slot indexing
- Add caching layer

**For 100,000+ slots:**
- Distributed system
- Database backend
- Message queue for requests
- Microservices architecture

---

## Algorithm Analysis

### Slot Allocation

**Best Case:** O(1)
- First slot in first area checked is available

**Average Case:** O(m)
- m = average slots per zone
- Typically find slot quickly

**Worst Case:** O(n × m)
- n = number of zones
- m = slots per zone
- All zones full except last slot

**Space Complexity:** O(1)
- No additional data structures
- In-place search

---

### Adjacent Zone Search

**Graph Traversal:** Implicit BFS

```
Current Zone → Check slots
    ├─ Not found → Visit adjacent[0] → Check slots
    ├─ Not found → Visit adjacent[1] → Check slots
    └─ Not found → Visit adjacent[2] → Check slots
```

**Complexity:**
- Time: O(d × m) where d = degree (adjacent zones)
- Space: O(1)

---

### State Validation

**Hash Lookup:** O(1)

```python
valid_transitions = {
    REQUESTED: [ALLOCATED, CANCELLED],
    ...
}
return to_state in valid_transitions[from_state]
```

---

## Memory Layout

### Per Parking Slot

```
ParkingSlot:
    slot_id: str (8 bytes + string)
    zone_id: str (8 bytes + string)
    is_available: bool (1 byte)
    occupied_vehicle_id: str | None (8 bytes + string)
Total: ~50 bytes per slot
```

### Per Zone

```
Zone:
    zone_id: str (~20 bytes)
    parking_areas: list[ParkingArea] (~100 bytes + areas)
    adjacent_zones: list[str] (~50 bytes + IDs)
Total: ~200 bytes + areas + adjacency
```

### System Memory Estimate

For 10,000 slots across 10 zones:
- Slots: 10,000 × 50 = 500 KB
- Zones: 10 × 200 = 2 KB
- Requests (assume 1,000): 1,000 × 200 = 200 KB
- Total: ~700 KB (negligible)

**Conclusion:** Memory not a constraint for typical use cases

---

## Future Enhancements

### 1. Priority Queue for Requests

**Purpose:** VIP handling

**Implementation:**
```python
import heapq

class PriorityRequest:
    def __init__(self, priority, request):
        self.priority = priority
        self.request = request
    
    def __lt__(self, other):
        return self.priority < other.priority

# Use heapq for min-heap
request_queue = []
heapq.heappush(request_queue, PriorityRequest(priority=1, request=vip_req))
```

---

### 2. Linked List for History

**Purpose:** Efficient history traversal

**Implementation:**
```python
class HistoryNode:
    def __init__(self, request, next=None):
        self.request = request
        self.next = next

class History:
    def __init__(self):
        self.head = None
    
    def add(self, request):
        self.head = HistoryNode(request, self.head)
```

---

### 3. B+ Tree for Slot Index

**Purpose:** Fast range queries

**Use Case:** "Find 5 adjacent slots"

---

### 4. Bloom Filter for Quick Checks

**Purpose:** Fast "definitely full" checks

**Use Case:** Skip zones without available slots

---

## Testing Strategy

### Unit Tests

- Each class independently
- State transitions
- Allocation logic
- Rollback operations

### Integration Tests

- End-to-end workflows
- Multiple concurrent requests
- Edge cases

### Performance Tests

- Large-scale (10,000+ slots)
- Allocation speed
- Memory usage

---

## Conclusion

The SmartPark system demonstrates practical DSA concepts:

- **Arrays** for storage
- **Stacks** for undo
- **Graphs** for relationships
- **State machines** for validation
- **Hash maps** for lookups

The architecture is modular, testable, and ready for enhancement with additional DSA structures (heaps, trees, etc.).

---

For implementation details, see individual class files in [src/](../src/).
