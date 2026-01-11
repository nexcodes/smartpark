# API Reference

Complete API documentation for the SmartPark Parking System.

---

## ParkingSystem

Main controller class that orchestrates all parking operations.

### Constructor

```python
ParkingSystem()
```

Initializes an empty parking system with no zones, vehicles, or requests.

**Example:**
```python
system = ParkingSystem()
```

---

## Zone Management Methods

### `add_zone(zone_id: str) -> Zone`

Creates a new parking zone.

**Parameters:**
- `zone_id` (str): Unique identifier for the zone

**Returns:**
- `Zone`: The created zone object

**Example:**
```python
zone = system.add_zone("ZONE-A")
```

---

### `add_parking_area_to_zone(zone_id: str, area_id: str, capacity: int) -> bool`

Adds a parking area with specified capacity to a zone.

**Parameters:**
- `zone_id` (str): ID of the target zone
- `area_id` (str): Unique identifier for the parking area
- `capacity` (int): Number of parking slots in the area

**Returns:**
- `bool`: True if successful, False if zone not found

**Example:**
```python
success = system.add_parking_area_to_zone("ZONE-A", "A1", 10)
```

---

### `link_adjacent_zones(zone1_id: str, zone2_id: str) -> bool`

Creates bidirectional adjacency between two zones for cross-zone allocation.

**Parameters:**
- `zone1_id` (str): First zone ID
- `zone2_id` (str): Second zone ID

**Returns:**
- `bool`: True if successful, False if either zone not found

**Example:**
```python
system.link_adjacent_zones("ZONE-A", "ZONE-B")
```

---

### `get_zone_status(zone_id: str) -> dict`

Retrieves comprehensive status information for a zone.

**Parameters:**
- `zone_id` (str): Zone ID to query

**Returns:**
- `dict`: Zone status with keys:
  - `zone_id` (str): Zone identifier
  - `total_capacity` (int): Total slots in zone
  - `available` (int): Available slots
  - `occupied` (int): Occupied slots
  - `occupancy_rate` (float): Percentage (0-100)
  - `adjacent_zones` (list): List of adjacent zone IDs

**Example:**
```python
status = system.get_zone_status("ZONE-A")
print(f"Occupancy: {status['occupancy_rate']}%")
```

---

## Vehicle Management Methods

### `register_vehicle(vehicle_id: str, preferred_zone: str) -> dict`

Registers a new vehicle in the system.

**Parameters:**
- `vehicle_id` (str): Unique identifier for the vehicle
- `preferred_zone` (str): Zone ID where vehicle prefers to park (can be None)

**Returns:**
- `dict`: Result with keys:
  - `success` (bool): Whether registration succeeded
  - `message` (str): Status message

**Example:**
```python
result = system.register_vehicle("CAR-001", "ZONE-A")
if result['success']:
    print(result['message'])
```

---

## Request Management Methods

### `create_parking_request(vehicle_id: str, requested_zone: str) -> dict`

Creates a new parking request.

**Parameters:**
- `vehicle_id` (str): ID of the vehicle requesting parking
- `requested_zone` (str): Desired zone for parking

**Returns:**
- `dict`: Result with keys:
  - `success` (bool): Whether request was created
  - `request_id` (str): Generated request ID (format: REQ####)
  - `state` (str): Initial state ("REQUESTED")
  - `message` (str): Status message

**Example:**
```python
result = system.create_parking_request("CAR-001", "ZONE-A")
if result['success']:
    request_id = result['request_id']
```

---

### `allocate_parking(request_id: str) -> dict`

Allocates a parking slot for a request.

**Parameters:**
- `request_id` (str): ID of the parking request

**Returns:**
- `dict`: Allocation result with keys:
  - `success` (bool): Whether allocation succeeded
  - `slot_id` (str): Allocated slot ID (if successful)
  - `zone_id` (str): Allocated zone ID (if successful)
  - `penalty` (int): Penalty points (0, 50, or 100)
  - `message` (str): Description of result

**Example:**
```python
result = system.allocate_parking(request_id)
if result['success']:
    print(f"Slot: {result['slot_id']}, Penalty: {result['penalty']}")
```

**Penalty Levels:**
- 0: Same zone as requested
- 50: Adjacent zone
- 100: Distant zone

---

### `mark_parking_occupied(request_id: str) -> dict`

Marks an allocated parking slot as occupied by the vehicle.

**Parameters:**
- `request_id` (str): Request ID to mark as occupied

**Returns:**
- `dict`: Result with keys:
  - `success` (bool): Whether operation succeeded
  - `message` (str): Status message

**Example:**
```python
result = system.mark_parking_occupied(request_id)
if result['success']:
    print(result['message'])
```

---

### `release_parking(request_id: str) -> dict`

Releases a parking slot (vehicle leaves).

**Parameters:**
- `request_id` (str): Request ID to release

**Returns:**
- `dict`: Result with keys:
  - `success` (bool): Whether release succeeded
  - `message` (str): Status message

**Example:**
```python
result = system.release_parking(request_id)
if result['success']:
    print(result['message'])
```

---

### `cancel_parking_request(request_id: str) -> dict`

Cancels a parking request (any state except RELEASED).

**Parameters:**
- `request_id` (str): Request ID to cancel

**Returns:**
- `dict`: Result with keys:
  - `success` (bool): Whether cancellation succeeded
  - `message` (str): Status message

**Example:**
```python
result = system.cancel_parking_request(request_id)
if result['success']:
    print(result['message'])
```

---

### `get_request_by_id(request_id: str) -> ParkingRequest | None`

Gets a parking request object by its ID.

**Parameters:**
- `request_id` (str): Request ID to query

**Returns:**
- `ParkingRequest`: Request object or None if not found

**Example:**
```python
request = system.get_request_by_id(request_id)
if request:
    print(f"State: {request.current_state.value}")
    print(f"Vehicle: {request.vehicle_id}")
    print(f"Requested Zone: {request.requested_zone}")
    if request.allocated_slot_id:
        print(f"Allocated Slot: {request.allocated_slot_id}")
        print(f"Allocated Zone: {request.allocated_zone}")
```

---

### `get_all_requests() -> list`

Gets all parking requests in the system.

**Returns:**
- `list`: List of ParkingRequest objects

**Example:**
```python
requests = system.get_all_requests()
for request in requests:
    print(f"{request.request_id}: {request.current_state.value}")
```

---

## Rollback Methods

### `rollback_operations(k: int) -> dict`

Rolls back the last k operations using stack-based undo.

**Parameters:**
- `k` (int): Number of operations to rollback

**Returns:**
- `dict`: Rollback result with keys:
  - `success` (bool): Whether rollback succeeded
  - `message` (str): Description
  - `rolled_back` (list): List of rolled back operations, each with:
    - `operation` (str): Operation type (ALLOCATE, CANCEL, RELEASE)
    - `request_id` (str): Affected request ID

**Example:**
```python
result = system.rollback_operations(2)
if result['success']:
    print(result['message'])
    for op in result['rolled_back']:
        print(f"  - {op['operation']} on {op['request_id']}")
```

---

## Analytics Methods

### `get_system_status() -> dict`

Gets overall system statistics.

**Returns:**
- `dict`: System status with keys:
  - `total_zones` (int): Number of zones
  - `total_slots` (int): Total parking slots
  - `available_slots` (int): Currently available
  - `occupied_slots` (int): Currently occupied
  - `total_requests` (int): All requests created
  - `active_requests` (int): Non-released/cancelled requests
  - `operations_in_history` (int): Operations in rollback stack

**Example:**
```python
status = system.get_system_status()
print(f"Total slots: {status['total_slots']}")
print(f"Available: {status['available_slots']}")
print(f"Active Requests: {status['active_requests']}")
print(f"Operations in History: {status['operations_in_history']}")
```

---

### `get_zone_status(zone_id: str) -> dict | None`

Gets status of a specific zone.

**Parameters:**
- `zone_id` (str): Zone ID to query

**Returns:**
- `dict`: Zone status with keys:
  - `zone_id` (str): Zone identifier
  - `total_capacity` (int): Total slots in zone
  - `available` (int): Available slots
  - `occupied` (int): Occupied slots
  - `areas` (int): Number of parking areas
  - `adjacent_zones` (list): List of adjacent zone IDs
- `None`: If zone not found

**Example:**
```python
status = system.get_zone_status("ZONE-A")
if status:
    print(f"Capacity: {status['available']}/{status['total_capacity']}")
    print(f"Adjacent: {', '.join(status['adjacent_zones'])}")
```

---

## Enumerations

### RequestState

States in the parking request lifecycle.

```python
class RequestState(Enum):
    REQUESTED = "REQUESTED"   # Initial state
    ALLOCATED = "ALLOCATED"   # Slot assigned
    OCCUPIED = "OCCUPIED"     # Vehicle parked
    RELEASED = "RELEASED"     # Vehicle left
    CANCELLED = "CANCELLED"   # Request cancelled
```

**Valid Transitions:**
- REQUESTED → ALLOCATED
- REQUESTED → CANCELLED
- ALLOCATED → OCCUPIED
- ALLOCATED → CANCELLED
- OCCUPIED → RELEASED

---

## Error Handling

All methods return dictionaries with `success` boolean and `message` string. Check `success` before accessing other fields.

**Common Error Scenarios:**

1. **Zone not found:**
   ```python
   {'success': False, 'message': 'Zone ZONE-X not found'}
   ```

2. **Vehicle not registered:**
   ```python
   {'success': False, 'message': 'Vehicle CAR-999 not registered'}
   ```

3. **Invalid state transition:**
   ```python
   {'success': False, 'message': 'Cannot transition from RELEASED to ALLOCATED'}
   ```

4. **No available slots:**
   ```python
   {'success': False, 'message': 'No available slots in any zone', 'penalty': 0}
   ```

---

## Response Format Examples

### Successful Allocation

```python
{
    'success': True,
    'slot_id': 'ZONE-A-A1-3',
    'zone_id': 'ZONE-A',
    'penalty': 0,
    'message': 'Allocated in requested zone'
}
```

### Cross-Zone Allocation

```python
{
    'success': True,
    'slot_id': 'ZONE-B-B1-5',
    'zone_id': 'ZONE-B',
    'penalty': 50,
    'message': 'Allocated in adjacent zone ZONE-B'
}
```

### Failed Allocation

```python
{
    'success': False,
    'message': 'No available slots in any zone',
    'penalty': 0
}
```

---

## Best Practices

1. **Always check `success` flag:**
   ```python
   result = system.allocate_parking(request_id)
   if result['success']:
       # Process successful allocation
   else:
       # Handle failure
       print(result['message'])
   ```

2. **Store request IDs:**
   ```python
   result = system.create_parking_request("CAR-001", "ZONE-A")
   request_id = result['request_id']  # Keep this for later operations
   ```

3. **Monitor zone capacity:**
   ```python
   status = system.get_zone_status("ZONE-A")
   if status['available'] < 5:
       print("Zone nearly full!")
   ```

4. **Use rollback carefully:**
   ```python
   # Rollback k operations from the stack
   result = system.rollback_operations(2)  # Rollback last 2 operations
   if result['success']:
       for op in result['rolled_back']:
           print(f"Rolled back: {op['operation']}")
   ```

---

## Complete Workflow Example

```python
# 1. Setup
system = ParkingSystem()
result = system.add_zone("ZONE-A")
result = system.add_parking_area_to_zone("ZONE-A", "A1", 10)

# 2. Register vehicle
result = system.register_vehicle("CAR-001", "ZONE-A")
if result['success']:
    print(result['message'])

# 3. Request parking
req_result = system.create_parking_request("CAR-001", "ZONE-A")
request_id = req_result['request_id']
print(f"Request ID: {request_id}, State: {req_result['state']}")

# 4. Allocate
alloc_result = system.allocate_parking(request_id)
if alloc_result['success']:
    print(f"Allocated: {alloc_result['slot_id']}")
    print(f"Zone: {alloc_result['zone_id']}")
    print(f"Penalty: {alloc_result['penalty']}")
    
    # 5. Mark as occupied
    result = system.mark_parking_occupied(request_id)
    print(result['message'])
    
    # 6. Check status
    request = system.get_request_by_id(request_id)
    print(f"Current state: {request.current_state.value}")
    
    # 7. Later... release
    release_result = system.release_parking(request_id)
    print(release_result['message'])
```

---

## Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Add Zone | O(1) | O(1) |
| Add Parking Area | O(n) - create slots | O(n) |
| Link Zones | O(1) | O(1) |
| Find Available Slot | O(n×m) - zones×slots | O(1) |
| Allocate Parking | O(n×m) | O(1) |
| Rollback | O(1) | O(k) - k operations |
| Get Status | O(n) - count slots | O(1) |

Where:
- n = number of zones
- m = average slots per zone
- k = operations in rollback stack

---

For more examples, see [main.py](../src/main.py).
