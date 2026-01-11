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

### `list_all_zones() -> list`

Gets a list of all zones with their status.

**Returns:**
- `list`: Array of zone status dictionaries

**Example:**
```python
zones = system.list_all_zones()
for zone in zones:
    print(f"{zone['zone_id']}: {zone['available']}/{zone['total_capacity']} available")
```

---

## Vehicle Management Methods

### `register_vehicle(vehicle_id: str, preferred_zone: str) -> Vehicle`

Registers a new vehicle in the system.

**Parameters:**
- `vehicle_id` (str): Unique identifier for the vehicle
- `preferred_zone` (str): Zone ID where vehicle prefers to park

**Returns:**
- `Vehicle`: The created vehicle object

**Example:**
```python
vehicle = system.register_vehicle("CAR-001", "ZONE-A")
```

---

### `get_vehicle(vehicle_id: str) -> Vehicle | None`

Retrieves vehicle information.

**Parameters:**
- `vehicle_id` (str): Vehicle identifier

**Returns:**
- `Vehicle`: Vehicle object or None if not found

**Example:**
```python
vehicle = system.get_vehicle("CAR-001")
if vehicle:
    print(f"Prefers: {vehicle.preferred_zone}")
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
  - `request_id` (str): Generated request ID
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

### `mark_occupied(request_id: str) -> dict`

Marks an allocated parking slot as occupied by the vehicle.

**Parameters:**
- `request_id` (str): Request ID to mark as occupied

**Returns:**
- `dict`: Result with keys:
  - `success` (bool): Whether operation succeeded
  - `message` (str): Status message

**Example:**
```python
result = system.mark_occupied(request_id)
```

---

### `release_parking(request_id: str) -> dict`

Releases a parking slot (vehicle leaves).

**Parameters:**
- `request_id` (str): Request ID to release

**Returns:**
- `dict`: Result with keys:
  - `success` (bool): Whether release succeeded
  - `slot_id` (str): Released slot ID
  - `duration` (float): Parking duration in seconds
  - `message` (str): Status message

**Example:**
```python
result = system.release_parking(request_id)
if result['success']:
    print(f"Parked for {result['duration']:.0f} seconds")
```

---

### `cancel_request(request_id: str) -> dict`

Cancels a parking request (any state except RELEASED).

**Parameters:**
- `request_id` (str): Request ID to cancel

**Returns:**
- `dict`: Result with keys:
  - `success` (bool): Whether cancellation succeeded
  - `previous_state` (str): State before cancellation
  - `message` (str): Status message

**Example:**
```python
result = system.cancel_request(request_id)
```

---

### `get_request_status(request_id: str) -> dict`

Gets detailed information about a parking request.

**Parameters:**
- `request_id` (str): Request ID to query

**Returns:**
- `dict`: Request information with keys:
  - `request_id` (str): Request identifier
  - `vehicle_id` (str): Vehicle identifier
  - `requested_zone` (str): Originally requested zone
  - `allocated_zone` (str): Actually allocated zone (or None)
  - `allocated_slot_id` (str): Allocated slot (or None)
  - `state` (str): Current state
  - `timestamp` (datetime): Request creation time
  - `duration` (float): Parking duration in seconds (or None)
  - `is_cross_zone` (bool): Whether cross-zone allocation

**Example:**
```python
status = system.get_request_status(request_id)
print(f"State: {status['state']}")
if status['is_cross_zone']:
    print(f"Cross-zone: {status['requested_zone']} → {status['allocated_zone']}")
```

---

## Rollback Methods

### `rollback_last_operation() -> dict`

Rolls back the most recent operation using stack-based undo.

**Returns:**
- `dict`: Rollback result with keys:
  - `success` (bool): Whether rollback succeeded
  - `operation_type` (str): Type of operation rolled back
  - `request_id` (str): Affected request ID
  - `message` (str): Description

**Example:**
```python
result = system.rollback_last_operation()
if result['success']:
    print(f"Rolled back: {result['operation_type']}")
```

---

## Analytics Methods

### `get_system_summary() -> dict`

Gets overall system statistics.

**Returns:**
- `dict`: System summary with keys:
  - `total_zones` (int): Number of zones
  - `total_slots` (int): Total parking slots
  - `available_slots` (int): Currently available
  - `occupied_slots` (int): Currently occupied
  - `overall_occupancy_rate` (float): Percentage
  - `total_requests` (int): All requests created
  - `active_requests` (int): Non-released/cancelled
  - `registered_vehicles` (int): Vehicle count

**Example:**
```python
summary = system.get_system_summary()
print(f"Occupancy: {summary['overall_occupancy_rate']:.1f}%")
print(f"Active Requests: {summary['active_requests']}")
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
   # Rollback only undoes the LAST operation
   # Cannot rollback multiple operations at once
   system.rollback_last_operation()
   ```

---

## Complete Workflow Example

```python
# 1. Setup
system = ParkingSystem()
system.add_zone("ZONE-A")
system.add_parking_area_to_zone("ZONE-A", "A1", 10)

# 2. Register vehicle
system.register_vehicle("CAR-001", "ZONE-A")

# 3. Request parking
req_result = system.create_parking_request("CAR-001", "ZONE-A")
request_id = req_result['request_id']

# 4. Allocate
alloc_result = system.allocate_parking(request_id)
if alloc_result['success']:
    print(f"Allocated: {alloc_result['slot_id']}")
    
    # 5. Mark as occupied
    system.mark_occupied(request_id)
    
    # 6. Later... release
    release_result = system.release_parking(request_id)
    print(f"Duration: {release_result['duration']} seconds")
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
