# DSA Concepts Implementation

Detailed explanation of Data Structures and Algorithms concepts used in SmartPark.

---

## Overview

This project demonstrates practical applications of fundamental DSA concepts in a real-world parking management system. Each data structure and algorithm is chosen for specific reasons aligned with system requirements.

---

## Table of Contents

1. [Arrays](#1-arrays)
2. [Stacks](#2-stacks)
3. [Graphs](#3-graphs)
4. [State Machines](#4-state-machines)

---

## 1. Arrays

### Implementation

**Used In:**
- Parking slots within `ParkingArea`
- Parking areas within `Zone`
- Adjacency lists for zones

**Code Example:**

```python
class ParkingArea:
    def __init__(self, area_id, zone_id, capacity):
        self.slots = []  # Array of ParkingSlot objects
        
        # Create parking slots
        for i in range(capacity):
            slot_id = f"{zone_id}-{area_id}-{i+1}"
            self.slots.append(ParkingSlot(slot_id, zone_id))
```

### Why Arrays?

**Advantages:**
- **O(1) Index Access**: Direct access to any slot
- **Sequential Storage**: Good cache locality
- **Simple Iteration**: Easy to loop through all slots
- **Fixed Size**: Each area has fixed capacity

**Operations:**

| Operation | Time Complexity | Use Case |
|-----------|----------------|----------|
| Access by index | O(1) | Get specific slot |
| Search | O(n) | Find available slot |
| Append | O(1) amortized | Add new slot |
| Iterate | O(n) | Check all slots |

### Practical Example

**Finding Available Slot:**

```python
def find_available_slot(self):
    """Linear search through array"""
    for slot in self.slots:  # O(n)
        if slot.is_available:
            return slot
    return None
```

**Why Not Binary Search?**
- Slots are not sorted by availability
- Availability changes dynamically
- Linear search is sufficient for small arrays (typical area: 10-50 slots)

### DSA Principles Demonstrated

1. **Sequential Access Pattern**: Iterate until condition met
2. **Early Return**: Stop when found (optimization)
3. **Dynamic Arrays**: Python lists grow automatically

---

## 2. Stacks

### Implementation

**Used In:**
- Rollback manager for undo operations

**Code Example:**

```python
class RollbackManager:
    def __init__(self):
        self.operation_stack = []  # Stack (LIFO)
    
    def record_allocation(self, slot, request):
        """Push operation onto stack"""
        operation = Operation(...)
        self.operation_stack.append(operation)  # Push: O(1)
    
    def rollback_last_operation(self):
        """Pop and undo last operation"""
        if not self.operation_stack:
            return {'success': False, 'message': 'No operations to rollback'}
        
        operation = self.operation_stack.pop()  # Pop: O(1)
        self._undo_operation(operation)
        return {'success': True, 'operation_type': operation.operation_type}
```

### Why Stack?

**LIFO (Last-In-First-Out) is Perfect For:**
- **Undo Operations**: Most recent action should be undone first
- **Temporal Ordering**: Natural chronological reverse
- **Simple API**: Push and pop only

**Alternative Considered:**
- **Queue (FIFO)**: Wrong - need to undo last, not first
- **Array with index**: Possible but stack abstraction clearer

### Stack Operations

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Push | O(1) | O(1) |
| Pop | O(1) | O(1) |
| Peek | O(1) | O(1) |
| IsEmpty | O(1) | O(1) |

### Practical Example

**Rollback Workflow:**

```python
# Step 1: Allocate (automatically recorded)
system.allocate_parking(req_id)  
# Stack: [ALLOCATE_OP]

# Step 2: Mark occupied (recorded)
system.mark_occupied(req_id)
# Stack: [ALLOCATE_OP, OCCUPY_OP]

# Step 3: Rollback (undo last)
system.rollback_last_operation()  # Pops OCCUPY_OP
# Stack: [ALLOCATE_OP]

# Step 4: Rollback again
system.rollback_last_operation()  # Pops ALLOCATE_OP
# Stack: []
```

### DSA Principles Demonstrated

1. **LIFO Ordering**: Last operation undone first
2. **Constant Time Operations**: O(1) push/pop
3. **State Restoration**: Each operation records previous state
4. **Encapsulation**: Stack hides implementation details

---

## 3. Graphs

### Implementation

**Used In:**
- Zone adjacency for cross-zone allocation

**Representation:**

```
Adjacency List (Array-based):

Zone A: [Zone B, Zone C]
Zone B: [Zone A, Zone D]
Zone C: [Zone A]
Zone D: [Zone B]

Visualized:
    A ─── B ─── D
    │     
    │     
    C     
```

**Code Example:**

```python
class Zone:
    def __init__(self, zone_id):
        self.zone_id = zone_id
        self.adjacent_zones = []  # Adjacency list
    
    def add_adjacent_zone(self, zone_id):
        """Add edge to graph"""
        if zone_id not in self.adjacent_zones:
            self.adjacent_zones.append(zone_id)

# Creating graph
system.link_adjacent_zones("ZONE-A", "ZONE-B")  # Bidirectional edge
```

### Why Graph?

**Zone Relationships Are:**
- **Non-hierarchical**: No parent-child structure
- **Many-to-many**: One zone can be adjacent to multiple zones
- **Symmetric**: If A is adjacent to B, then B is adjacent to A

**Why Adjacency List Over Matrix?**

| Factor | Adjacency List | Adjacency Matrix |
|--------|---------------|------------------|
| Space | O(V + E) | O(V²) |
| Add Edge | O(1) | O(1) |
| Check Edge | O(degree) | O(1) |
| Iterate Neighbors | O(degree) | O(V) |

For sparse graphs (few edges), adjacency list is better.

### Graph Algorithms

#### Cross-Zone Allocation (Implicit BFS)

```python
def allocate_slot(self, parking_request):
    requested_zone_id = parking_request.requested_zone
    
    # Step 1: Try same zone (distance 0)
    if requested_zone_id in self.zones:
        zone = self.zones[requested_zone_id]
        slot = zone.find_available_slot()
        if slot:
            return {'success': True, 'penalty': 0}
    
    # Step 2: Try adjacent zones (distance 1)
    zone = self.zones[requested_zone_id]
    for adjacent_zone_id in zone.adjacent_zones:  # BFS-like
        adj_zone = self.zones[adjacent_zone_id]
        slot = adj_zone.find_available_slot()
        if slot:
            return {'success': True, 'penalty': 50}
    
    # Step 3: Try all zones (distance 2+)
    for zone_id, zone in self.zones.items():
        if zone_id != requested_zone_id:
            slot = zone.find_available_slot()
            if slot:
                return {'success': True, 'penalty': 100}
    
    return {'success': False}
```

**Complexity:**
- **Time**: O(V + E + S) where V=zones, E=edges, S=slots
- **Space**: O(1) - no queue needed (small graph)

### DSA Principles Demonstrated

1. **Graph Representation**: Adjacency list for sparse graph
2. **BFS-like Traversal**: Level-by-level search (distance-based priority)
3. **Bidirectional Edges**: Symmetric relationships
4. **Unweighted Graph**: All edges have equal cost (one hop)

---

## 4. State Machines

### Implementation

**Used In:**
- `ParkingRequest` lifecycle management

**States:**

```python
class RequestState(Enum):
    REQUESTED = "REQUESTED"
    ALLOCATED = "ALLOCATED"
    OCCUPIED = "OCCUPIED"
    RELEASED = "RELEASED"
    CANCELLED = "CANCELLED"
```

**State Transition Graph:**

```
REQUESTED ──→ ALLOCATED ──→ OCCUPIED ──→ RELEASED
    │             │
    ↓             ↓
CANCELLED     CANCELLED
```

**Code Example:**

```python
@staticmethod
def is_valid_transition(from_state, to_state):
    """Validate state transition"""
    valid_transitions = {
        RequestState.REQUESTED: [RequestState.ALLOCATED, RequestState.CANCELLED],
        RequestState.ALLOCATED: [RequestState.OCCUPIED, RequestState.CANCELLED],
        RequestState.OCCUPIED: [RequestState.RELEASED],
        RequestState.RELEASED: [],
        RequestState.CANCELLED: []
    }
    return to_state in valid_transitions.get(from_state, [])
```

### DSA Principles Demonstrated

1. **Finite State Machine**: Fixed set of states
2. **Transition Validation**: O(1) lookup in hash map
3. **Enumeration**: Type-safe state representation
4. **Deterministic Behavior**: Same input always produces same result

---

## Summary Table

| DSA Concept | Implementation | Purpose | Complexity |
|-------------|---------------|---------|------------|
| **Array** | Python List | Store slots, areas | O(1) access, O(n) search |
| **Stack** | Python List | Rollback operations | O(1) push/pop |
| **Graph** | Adjacency List | Zone relationships | O(V+E) traversal |
| **State Machine** | Enum + validation | Request lifecycle | O(1) transition check |
| **Hash Table** | Python Dict | Fast ID lookup | O(1) average |
| **Linear Search** | Loop with early return | Find available slot | O(n) |
| **First-Fit** | Greedy algorithm | Slot allocation | O(n) |
| **BFS** | Implicit level-order | Cross-zone search | O(V+E) |

---

For more details on implementation, see [ARCHITECTURE.md](ARCHITECTURE.md) and [API_REFERENCE.md](API_REFERENCE.md).