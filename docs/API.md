# SmartPark - API Reference

Complete documentation of all classes, methods, parameters, and return values in the SmartPark system.

## Table of Contents

- [Core System Classes](#core-system-classes)
  - [ParkingSystem](#parkingsystem)
  - [AllocationEngine](#allocationengine)
  - [RollbackManager](#rollbackmanager)
  - [AnalyticsEngine](#analyticsengine)
- [Entity Classes](#entity-classes)
  - [Zone](#zone)
  - [ParkingArea](#parkingarea)
  - [ParkingSlot](#parkingslot)
  - [ParkingRequest](#parkingrequest)
  - [Vehicle](#vehicle)
- [Enumerations](#enumerations)
  - [RequestState](#requeststate)
- [Rollback Support](#rollback-support)
  - [Operation](#operation)

---

## Core System Classes

### ParkingSystem

**Module:** `parking_system.py`

Main controller that orchestrates all parking operations. Holds global state including zones, vehicles, and requests.

#### Constructor

```python
ParkingSystem()
```

**Initializes:**
- `zones` (dict): Dictionary mapping zone_id → Zone objects
- `vehicles` (dict): Dictionary mapping vehicle_id → Vehicle objects
- `requests` (dict): Dictionary mapping request_id → ParkingRequest objects
- `request_counter` (int): Auto-incrementing counter for request IDs
- `allocation_engine` (AllocationEngine): Handles slot allocation logic
- `rollback_manager` (RollbackManager): Manages operation history and rollbacks
- `analytics` (AnalyticsEngine): Calculates metrics and statistics
- `request_history` (list): Ordered list of all requests

#### Methods

##### add_zone()

```python
add_zone(zone_id: str) -> dict
```

Add a new zone to the system.

**Parameters:**
- `zone_id` (str): Unique identifier for the zone (e.g., "ZONE-A")

**Returns:**
```python
{
    'success': bool,      # True if zone created, False if already exists
    'message': str        # Result message
}
```

**Example:**
```python
result = system.add_zone("ZONE-A")
# {'success': True, 'message': 'Zone ZONE-A created successfully'}
```

##### add_parking_area_to_zone()

```python
add_parking_area_to_zone(zone_id: str, area_id: str, capacity: int) -> dict
```

Add a parking area with specified capacity to a zone.

**Parameters:**
- `zone_id` (str): ID of the zone
- `area_id` (str): ID for the parking area (e.g., "A1")
- `capacity` (int): Number of parking slots to create

**Returns:**
```python
{
    'success': bool,
    'message': str
}
```

**Example:**
```python
result = system.add_parking_area_to_zone("ZONE-A", "A1", 10)
# {'success': True, 'message': 'Parking area A1 added to ZONE-A with 10 slots'}
```

##### link_adjacent_zones()

```python
link_adjacent_zones(zone1_id: str, zone2_id: str) -> dict
```

Create bidirectional adjacency between two zones for graph-based allocation.

**Parameters:**
- `zone1_id` (str): First zone ID
- `zone2_id` (str): Second zone ID

**Returns:**
```python
{
    'success': bool,
    'message': str
}
```

**Note:** Creates two-way edge in the zone graph. Used by AllocationEngine for penalty calculation.

##### register_vehicle()

```python
register_vehicle(vehicle_id: str, preferred_zone: str | None) -> dict
```

Register a new vehicle in the system.

**Parameters:**
- `vehicle_id` (str): Unique identifier for the vehicle
- `preferred_zone` (str | None): Zone where vehicle prefers to park (optional)

**Returns:**
```python
{
    'success': bool,
    'message': str
}
```

##### create_parking_request()

```python
create_parking_request(vehicle_id: str, requested_zone: str) -> dict
```

Create a new parking request.

**Parameters:**
- `vehicle_id` (str): ID of the vehicle requesting parking
- `requested_zone` (str): Zone where parking is requested

**Returns:**
```python
{
    'success': bool,
    'request_id': str,    # Generated ID like "REQ0001"
    'state': str,         # "REQUESTED"
    'message': str
}
```

##### allocate_parking()

```python
allocate_parking(request_id: str) -> dict
```

Allocate parking slot for a request using 3-tier priority system.

**Parameters:**
- `request_id` (str): ID of the parking request

**Returns:**
```python
{
    'success': bool,
    'message': str,
    'slot_id': str,       # e.g., "ZONE-A-A1-1" (if successful)
    'zone_id': str,       # Zone where allocated
    'penalty': int        # 0 (same zone), 50 (adjacent), 100 (distant)
}
```

**Priority Logic:**
1. Same zone (penalty=0)
2. Adjacent zones (penalty=50)
3. All other zones (penalty=100)

##### cancel_parking_request()

```python
cancel_parking_request(request_id: str) -> dict
```

Cancel a parking request and release any allocated slot.

**Parameters:**
- `request_id` (str): ID of the request to cancel

**Returns:**
```python
{
    'success': bool,
    'message': str
}
```

**Valid States:** Can cancel from REQUESTED or ALLOCATED states only.

##### mark_parking_occupied()

```python
mark_parking_occupied(request_id: str) -> dict
```

Mark parking as occupied when vehicle arrives.

**Parameters:**
- `request_id` (str): ID of the parking request

**Returns:**
```python
{
    'success': bool,
    'message': str
}
```

**State Transition:** ALLOCATED → OCCUPIED

##### release_parking()

```python
release_parking(request_id: str) -> dict
```

Release parking when vehicle leaves.

**Parameters:**
- `request_id` (str): ID of the parking request

**Returns:**
```python
{
    'success': bool,
    'message': str
}
```

**State Transition:** OCCUPIED → RELEASED

##### rollback_operations()

```python
rollback_operations(k: int) -> dict
```

Rollback the last k operations using stack-based LIFO.

**Parameters:**
- `k` (int): Number of operations to rollback

**Returns:**
```python
{
    'success': bool,
    'message': str,
    'rolled_back': list,        # List of operation details
    'skipped': list,            # List of skipped operations
    'operations_rolled_back': int
}
```

##### get_system_status()

```python
get_system_status() -> dict
```

Get overall system statistics.

**Returns:**
```python
{
    'total_slots': int,
    'available_slots': int,
    'occupied_slots': int,
    'total_zones': int,
    'total_requests': int,
    'active_requests': int,
    'operations_in_history': int
}
```

##### get_zone_status()

```python
get_zone_status(zone_id: str) -> dict | None
```

Get status of a specific zone.

**Parameters:**
- `zone_id` (str): ID of the zone

**Returns:**
```python
{
    'zone_id': str,
    'total_capacity': int,
    'available': int,
    'occupied': int,
    'areas': int,
    'adjacent_zones': list  # List of adjacent zone IDs
}
```

Returns `None` if zone not found.

##### get_all_requests()

```python
get_all_requests() -> list
```

Get list of all parking requests.

**Returns:** List of ParkingRequest objects

##### get_request_by_id()

```python
get_request_by_id(request_id: str) -> ParkingRequest | None
```

Get a specific request by ID.

**Parameters:**
- `request_id` (str): Request ID to retrieve

**Returns:** ParkingRequest object or None

---

### AllocationEngine

**Module:** `allocation_engine.py`

Handles parking slot allocation with priority-based logic and cross-zone fallback.

#### Constructor

```python
AllocationEngine(zones: dict)
```

**Parameters:**
- `zones` (dict): Reference to ParkingSystem.zones dictionary

#### Methods

##### allocate_slot()

```python
allocate_slot(parking_request: ParkingRequest) -> dict
```

Allocate a parking slot using 3-tier priority system.

**Parameters:**
- `parking_request` (ParkingRequest): Request object to allocate for

**Returns:**
```python
{
    'success': bool,
    'message': str,
    'slot_id': str,     # If successful
    'zone_id': str,     # If successful
    'penalty': int      # 0, 50, or 100
}
```

**Algorithm:**
1. Try same zone (O(m) where m = slots in zone)
2. Try adjacent zones via graph traversal (O(k×m) where k = adjacent zones)
3. Try all other zones (O(n×m) where n = total zones)

##### cancel_request()

```python
cancel_request(parking_request: ParkingRequest) -> dict
```

Cancel a request and release allocated slot if any.

**Parameters:**
- `parking_request` (ParkingRequest): Request to cancel

**Returns:**
```python
{
    'success': bool,
    'message': str
}
```

##### release_parking()

```python
release_parking(parking_request: ParkingRequest) -> dict
```

Release parking slot when vehicle leaves.

**Parameters:**
- `parking_request` (ParkingRequest): Request to release

**Returns:**
```python
{
    'success': bool,
    'message': str
}
```

---

### RollbackManager

**Module:** `rollback_manager.py`

Manages operation history using stack data structure for rollback functionality.

#### Constructor

```python
RollbackManager()
```

**Initializes:**
- `operation_stack` (list): Stack of Operation objects (LIFO)

#### Methods

##### record_allocation()

```python
record_allocation(slot: ParkingSlot, request: ParkingRequest) -> None
```

Record an allocation operation.

**Parameters:**
- `slot` (ParkingSlot): Slot that was allocated
- `request` (ParkingRequest): Request that was allocated

##### record_occupied()

```python
record_occupied(request: ParkingRequest, previous_state: RequestState) -> None
```

Record a mark-as-occupied operation.

**Parameters:**
- `request` (ParkingRequest): Request marked as occupied
- `previous_state` (RequestState): State before occupation (ALLOCATED)

##### record_cancellation()

```python
record_cancellation(slot: ParkingSlot | None, request: ParkingRequest, 
                   previous_state: RequestState) -> None
```

Record a cancellation operation.

**Parameters:**
- `slot` (ParkingSlot | None): Slot that was released (None if not allocated)
- `request` (ParkingRequest): Request that was cancelled
- `previous_state` (RequestState): State before cancellation

##### record_release()

```python
record_release(slot: ParkingSlot, request: ParkingRequest) -> None
```

Record a release operation.

**Parameters:**
- `slot` (ParkingSlot): Slot that was released
- `request` (ParkingRequest): Request that was released

##### rollback()

```python
rollback(k: int, zones: dict, requests_dict: dict) -> dict
```

Rollback the last k operations from the stack.

**Parameters:**
- `k` (int): Number of operations to rollback
- `zones` (dict): Reference to zone dictionary
- `requests_dict` (dict): Reference to requests dictionary

**Returns:**
```python
{
    'success': bool,
    'message': str,
    'rolled_back': list,
    'skipped': list,
    'operations_rolled_back': int
}
```

**Complexity:** O(k) where k is the number of operations to rollback

##### get_operation_count()

```python
get_operation_count() -> int
```

Get the number of operations in the stack.

**Returns:** Integer count of operations

---

### AnalyticsEngine

**Module:** `analytics.py`

Calculates metrics and statistics using array traversal patterns.

#### Constructor

```python
AnalyticsEngine(parking_system: ParkingSystem)
```

**Parameters:**
- `parking_system` (ParkingSystem): Reference to main system

#### Methods

##### get_average_parking_duration()

```python
get_average_parking_duration() -> dict
```

Calculate average parking duration for completed requests.

**Returns:**
```python
{
    'success': bool,
    'average_duration_seconds': float,
    'average_duration_minutes': float,
    'completed_requests': int,
    'message': str
}
```

**DSA Pattern:** Array traversal with accumulator

##### get_zone_utilization()

```python
get_zone_utilization() -> dict
```

Calculate utilization rate for each zone.

**Returns:**
```python
{
    'success': bool,
    'zones': list,          # List of zone stats
    'total_zones': int,
    'message': str
}
```

**Zone Stats Format:**
```python
{
    'zone_id': str,
    'total_capacity': int,
    'occupied': int,
    'available': int,
    'utilization_rate': float  # Percentage
}
```

**DSA Pattern:** Array traversal with counters

##### get_request_statistics()

```python
get_request_statistics() -> dict
```

Calculate statistics for requests by state.

**Returns:**
```python
{
    'success': bool,
    'total_requests': int,
    'state_breakdown': dict,      # Counts by state
    'completed_requests': int,
    'cancelled_requests': int,
    'completion_rate': float,     # Percentage
    'cancellation_rate': float,   # Percentage
    'message': str
}
```

**State Breakdown:**
```python
{
    'requested': int,
    'allocated': int,
    'occupied': int,
    'released': int,
    'cancelled': int
}
```

##### get_peak_usage_zone()

```python
get_peak_usage_zone() -> dict
```

Find zone with highest utilization.

**Returns:**
```python
{
    'success': bool,
    'zone_id': str,
    'utilization_rate': float,
    'occupied': int,
    'total_capacity': int,
    'available': int,
    'message': str
}
```

**DSA Pattern:** Linear search for maximum

##### get_cross_zone_allocation_statistics()

```python
get_cross_zone_allocation_statistics() -> dict
```

Calculate statistics for cross-zone allocations (penalty cases).

**Returns:**
```python
{
    'success': bool,
    'total_allocated': int,
    'same_zone_allocations': int,
    'cross_zone_allocations': int,
    'cross_zone_percentage': float,
    'message': str
}
```

##### get_comprehensive_analytics()

```python
get_comprehensive_analytics() -> dict
```

Get all analytics in one comprehensive report.

**Returns:**
```python
{
    'success': bool,
    'average_duration': dict,
    'zone_utilization': dict,
    'request_statistics': dict,
    'peak_usage_zone': dict,
    'cross_zone_statistics': dict
}
```

##### display_analytics_summary()

```python
display_analytics_summary() -> str
```

Generate formatted text summary of analytics.

**Returns:** Formatted string with all analytics data

---

## Entity Classes

### Zone

**Module:** `zone.py`

Represents a parking zone containing multiple parking areas. Acts as a node in the zone graph.

#### Constructor

```python
Zone(zone_id: str)
```

**Parameters:**
- `zone_id` (str): Unique identifier for the zone

**Initializes:**
- `zone_id` (str): Zone identifier
- `parking_areas` (list): Array of ParkingArea objects
- `adjacent_zones` (list): Adjacency list of zone IDs (graph implementation)

#### Methods

##### add_parking_area()

```python
add_parking_area(area_id: str, capacity: int) -> None
```

Add a parking area to this zone.

**Parameters:**
- `area_id` (str): Unique identifier for the area
- `capacity` (int): Number of slots to create

##### add_adjacent_zone()

```python
add_adjacent_zone(zone_id: str) -> None
```

Add an adjacent zone to the adjacency list.

**Parameters:**
- `zone_id` (str): ID of the adjacent zone

##### find_available_slot()

```python
find_available_slot() -> ParkingSlot | None
```

Find first available slot in this zone using linear search.

**Returns:** First available ParkingSlot or None

**Complexity:** O(m) where m = total slots in zone

##### get_total_capacity()

```python
get_total_capacity() -> int
```

Get total capacity of all parking areas.

**Returns:** Sum of all area capacities

##### get_available_count()

```python
get_available_count() -> int
```

Get count of available slots.

**Returns:** Number of available slots

##### get_occupied_count()

```python
get_occupied_count() -> int
```

Get count of occupied slots.

**Returns:** Number of occupied slots

---

### ParkingArea

**Module:** `parking_area.py`

Represents a parking area containing multiple parking slots.

#### Constructor

```python
ParkingArea(area_id: str, zone_id: str, capacity: int)
```

**Parameters:**
- `area_id` (str): Unique identifier for the area
- `zone_id` (str): Zone where this area is located
- `capacity` (int): Number of slots to create

**Initializes:**
- `area_id` (str): Area identifier
- `zone_id` (str): Parent zone ID
- `capacity` (int): Total number of slots
- `slots` (list): Array of ParkingSlot objects

**Auto-generates slots** with IDs formatted as: `{zone_id}-{area_id}-{slot_number}`

#### Methods

##### find_available_slot()

```python
find_available_slot() -> ParkingSlot | None
```

Find first available slot using linear search.

**Returns:** First available ParkingSlot or None

**Complexity:** O(n) where n = capacity

##### get_available_count()

```python
get_available_count() -> int
```

Get count of available slots.

**Returns:** Number of available slots

##### get_occupied_count()

```python
get_occupied_count() -> int
```

Get count of occupied slots.

**Returns:** Number of occupied slots

---

### ParkingSlot

**Module:** `parking_slot.py`

Represents a single parking slot.

#### Constructor

```python
ParkingSlot(slot_id: str, zone_id: str)
```

**Parameters:**
- `slot_id` (str): Unique identifier for the slot
- `zone_id` (str): Zone where this slot is located

**Initializes:**
- `slot_id` (str): Slot identifier
- `zone_id` (str): Parent zone ID
- `is_available` (bool): True if slot is free
- `occupied_vehicle_id` (str | None): ID of occupying vehicle

#### Methods

##### allocate()

```python
allocate(vehicle_id: str) -> bool
```

Allocate this slot to a vehicle.

**Parameters:**
- `vehicle_id` (str): ID of the vehicle

**Returns:** True if successful, False if already occupied

##### release()

```python
release() -> str | None
```

Release this slot (make it available).

**Returns:** Vehicle ID that was occupying the slot, or None

---

### ParkingRequest

**Module:** `parking_request.py`

Represents a parking request with state machine management.

#### Constructor

```python
ParkingRequest(request_id: str, vehicle_id: str, requested_zone: str)
```

**Parameters:**
- `request_id` (str): Unique identifier for the request
- `vehicle_id` (str): ID of the requesting vehicle
- `requested_zone` (str): Zone where parking is requested

**Initializes:**
- `request_id` (str): Request identifier
- `vehicle_id` (str): Vehicle ID
- `requested_zone` (str): Requested zone ID
- `allocated_zone` (str | None): Zone where allocated (None initially)
- `allocated_slot_id` (str | None): Allocated slot ID (None initially)
- `timestamp` (datetime): Request creation time
- `current_state` (RequestState): Current state (REQUESTED initially)
- `allocation_timestamp` (datetime | None): When allocated
- `release_timestamp` (datetime | None): When released

#### Methods

##### change_state()

```python
change_state(new_state: RequestState) -> bool
```

Change the state with validation.

**Parameters:**
- `new_state` (RequestState): Target state

**Returns:** True if transition valid, False otherwise

**Validates using state machine** defined in RequestState enum.

##### allocate_slot()

```python
allocate_slot(slot_id: str, zone_id: str) -> bool
```

Allocate a slot to this request.

**Parameters:**
- `slot_id` (str): ID of the allocated slot
- `zone_id` (str): Zone of the allocated slot

**Returns:** True if successful

**Side Effect:** Transitions to ALLOCATED state

##### get_parking_duration()

```python
get_parking_duration() -> float | None
```

Calculate parking duration in seconds.

**Returns:** Duration in seconds, or None if not yet released

##### is_cross_zone_allocation()

```python
is_cross_zone_allocation() -> bool
```

Check if this is a cross-zone allocation.

**Returns:** True if allocated_zone != requested_zone

---

### Vehicle

**Module:** `vehicle.py`

Represents a vehicle in the parking system.

#### Constructor

```python
Vehicle(vehicle_id: str, preferred_zone: str | None)
```

**Parameters:**
- `vehicle_id` (str): Unique identifier for the vehicle
- `preferred_zone` (str | None): Preferred parking zone (optional)

**Attributes:**
- `vehicle_id` (str): Vehicle identifier
- `preferred_zone` (str | None): Preferred zone ID

---

## Enumerations

### RequestState

**Module:** `enums.py`

State machine for parking requests.

#### Values

```python
REQUESTED = "REQUESTED"     # Request created
ALLOCATED = "ALLOCATED"     # Slot assigned
OCCUPIED = "OCCUPIED"       # Vehicle parked
RELEASED = "RELEASED"       # Vehicle left
CANCELLED = "CANCELLED"     # Request cancelled
```

#### Methods

##### is_valid_transition()

```python
@staticmethod
is_valid_transition(from_state: RequestState, to_state: RequestState) -> bool
```

Validate state transitions.

**Parameters:**
- `from_state` (RequestState): Current state
- `to_state` (RequestState): Target state

**Returns:** True if transition is valid

**Valid Transitions:**
- REQUESTED → ALLOCATED or CANCELLED
- ALLOCATED → OCCUPIED or CANCELLED
- OCCUPIED → RELEASED
- RELEASED → (none)
- CANCELLED → (none)

---

## Rollback Support

### Operation

**Module:** `rollback_manager.py`

Represents a reversible operation for rollback functionality.

#### Constructor

```python
Operation(operation_type: str, slot_id: str, slot_previous_availability: bool,
          slot_previous_vehicle_id: str | None, request_id: str,
          request_previous_state: RequestState,
          request_previous_allocated_slot: str | None = None,
          request_previous_allocated_zone: str | None = None)
```

**Parameters:**
- `operation_type` (str): "ALLOCATE", "CANCEL", "OCCUPY", or "RELEASE"
- `slot_id` (str): ID of affected slot
- `slot_previous_availability` (bool): Slot availability before operation
- `slot_previous_vehicle_id` (str | None): Previous vehicle in slot
- `request_id` (str): ID of the request
- `request_previous_state` (RequestState): Request state before operation
- `request_previous_allocated_slot` (str | None): Previous allocated slot
- `request_previous_allocated_zone` (str | None): Previous allocated zone

**Attributes:** Same as parameters

**Purpose:** Stores complete state needed to reverse an operation during rollback.

---

## Common Patterns

### Return Dictionary Format

All public methods that modify state return dictionaries with at least:

```python
{
    'success': bool,    # True if operation succeeded
    'message': str      # Human-readable result message
}
```

Additional keys are operation-specific (e.g., `slot_id`, `penalty`, `request_id`).

### ID Naming Conventions

- **Zone IDs**: User-defined, uppercase recommended (e.g., "ZONE-A")
- **Vehicle IDs**: User-defined, uppercase recommended (e.g., "CAR-001")
- **Request IDs**: Auto-generated as "REQ" + 4-digit number (e.g., "REQ0001")
- **Slot IDs**: Auto-generated as "{zone_id}-{area_id}-{slot_number}" (e.g., "ZONE-A-A1-1")

### Error Handling

Methods validate inputs and return early with `{'success': False, 'message': '...'}` on errors. No exceptions are raised from normal operations.

---

## Usage Examples

### Complete Workflow

```python
from parking_system import ParkingSystem

# Initialize system
system = ParkingSystem()

# Setup
system.add_zone("ZONE-A")
system.add_parking_area_to_zone("ZONE-A", "A1", 5)
system.register_vehicle("CAR-001", "ZONE-A")

# Create and allocate request
result = system.create_parking_request("CAR-001", "ZONE-A")
request_id = result['request_id']

result = system.allocate_parking(request_id)
print(f"Allocated: {result['slot_id']}, Penalty: {result['penalty']}")

# Mark occupied
system.mark_parking_occupied(request_id)

# Release
system.release_parking(request_id)

# Analytics
stats = system.analytics.get_comprehensive_analytics()
print(stats)
```

### Rollback Example

```python
# Perform operations
system.allocate_parking("REQ0001")
system.allocate_parking("REQ0002")

# Rollback last 2 operations
result = system.rollback_operations(2)
print(f"Rolled back {result['operations_rolled_back']} operations")
```

---

## Performance Characteristics

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| add_zone() | O(1) | Dictionary insert |
| add_parking_area_to_zone() | O(n) | Creates n slots |
| allocate_parking() | O(n×m) worst case | n zones, m slots/zone |
| allocate_parking() | O(m) best case | Same-zone allocation |
| rollback_operations() | O(k) | k = operations to rollback |
| find_available_slot() | O(m) | Linear search through slots |
| get_zone_utilization() | O(n×m) | Traverse all zones and slots |
| is_valid_transition() | O(1) | Dictionary lookup |

---

**For implementation details, see [ARCHITECTURE.md](ARCHITECTURE.md)**  
**For DSA explanations, see [DSA_CONCEPTS.md](DSA_CONCEPTS.md)**
