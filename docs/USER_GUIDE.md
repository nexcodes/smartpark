# User Guide

Complete guide for using the SmartPark Parking System.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Basic Operations](#basic-operations)
3. [Advanced Features](#advanced-features)
4. [Common Workflows](#common-workflows)
5. [Troubleshooting](#troubleshooting)
6. [Best Practices](#best-practices)

---

## Quick Start

### Installation

1. Ensure Python 3.8+ is installed:
   ```bash
   python --version
   ```

2. Clone or download the project:
   ```bash
   cd py_project
   ```

3. No dependencies needed - uses Python standard library only!

### Running the Interactive System

```bash
cd src
python main.py
```

This launches an **interactive menu-driven interface** with the following sections:

**Setup Operations:**
- Add Zone
- Add Parking Area to Zone
- Link Adjacent Zones
- Register Vehicle

**Parking Operations:**
- Create Parking Request
- Allocate Parking
- Mark Parking as Occupied
- Release Parking
- Cancel Parking Request

**Query Operations:**
- View System Status
- View Zone Status
- View Request Details
- View All Zones
- View All Vehicles

**Advanced Operations:**
- Rollback Operations
- View Operation History

The system provides immediate feedback and validation for each operation.

---

## Basic Operations

### 1. Initialize the System

```python
from parking_system import ParkingSystem

# Create system instance
system = ParkingSystem()
```

---

### 2. Setup Zones and Parking Areas

#### Create Zones

```python
# Add zones
system.add_zone("ZONE-A")
system.add_zone("ZONE-B")
system.add_zone("ZONE-C")
```

#### Add Parking Areas

```python
# Add areas to ZONE-A
system.add_parking_area_to_zone("ZONE-A", "A1", capacity=10)
system.add_parking_area_to_zone("ZONE-A", "A2", capacity=10)

# Add areas to ZONE-B
system.add_parking_area_to_zone("ZONE-B", "B1", capacity=15)

# Add areas to ZONE-C
system.add_parking_area_to_zone("ZONE-C", "C1", capacity=8)
```

**Result:** You now have 43 total parking slots across 3 zones.

#### Link Adjacent Zones

```python
# Make ZONE-A and ZONE-B adjacent
system.link_adjacent_zones("ZONE-A", "ZONE-B")

# Make ZONE-B and ZONE-C adjacent
system.link_adjacent_zones("ZONE-B", "ZONE-C")
```

**Topology:**
```
ZONE-A ←→ ZONE-B ←→ ZONE-C
```

---

### 3. Register Vehicles

```python
# Register vehicles with their preferred zones
result = system.register_vehicle("CAR-001", preferred_zone="ZONE-A")
if result['success']:
    print(result['message'])

result = system.register_vehicle("CAR-002", preferred_zone="ZONE-B")
if result['success']:
    print(result['message'])

result = system.register_vehicle("CAR-003", preferred_zone="ZONE-A")
if result['success']:
    print(result['message'])
```

---

### 4. Create Parking Requests

```python
# Vehicle CAR-001 requests parking in ZONE-A
result = system.create_parking_request("CAR-001", "ZONE-A")

if result['success']:
    request_id = result['request_id']
    print(f"Request created: {request_id}")
    print(f"State: {result['state']}")  # Will show "REQUESTED"
else:
    print(f"Failed: {result['message']}")
```

**Important:** Save the `request_id` - you'll need it for all subsequent operations!

---

### 5. Allocate Parking Slot

```python
# Allocate a slot for the request
allocation = system.allocate_parking(request_id)

if allocation['success']:
    print(f"✓ Allocated slot: {allocation['slot_id']}")
    print(f"  Zone: {allocation['zone_id']}")
    print(f"  Penalty: {allocation['penalty']}")
else:
    print(f"✗ Allocation failed: {allocation['message']}")
```

**Penalty Guide:**
- `0` = Same zone as requested (ideal)
- `50` = Adjacent zone (acceptable)
- `100` = Distant zone (not ideal)

---

### 6. Mark as Occupied

```python
# Vehicle has parked, mark slot as occupied
result = system.mark_parking_occupied(request_id)

if result['success']:
    print(f"✓ {result['message']}")
```

---

### 7. Release Parking Slot

```python
# Vehicle is leaving
result = system.release_parking(request_id)

if result['success']:
    print(f"✓ {result['message']}")
```

---

## Advanced Features

### Monitor Zone Status

```python
# Get detailed zone information
status = system.get_zone_status("ZONE-A")

if status:
    print(f"Zone: {status['zone_id']}")
    print(f"Total Capacity: {status['total_capacity']}")
    print(f"Available: {status['available']}")
    print(f"Occupied: {status['occupied']}")
    print(f"Number of Areas: {status['areas']}")
    print(f"Adjacent Zones: {', '.join(status['adjacent_zones'])}")
```

**Example Output:**
```
Zone: ZONE-A
Total Capacity: 20
Available: 12
Occupied: 8
Number of Areas: 2
Adjacent Zones: ZONE-B
```

---

### Check Request Details

```python
request = system.get_request_by_id(request_id)

if request:
    print(f"Request: {request.request_id}")
    print(f"Vehicle: {request.vehicle_id}")
    print(f"State: {request.current_state.value}")
    print(f"Requested Zone: {request.requested_zone}")
    print(f"Timestamp: {request.timestamp}")
    
    if request.allocated_zone:
        print(f"Allocated Zone: {request.allocated_zone}")
        print(f"Slot: {request.allocated_slot_id}")
        
        if request.allocated_zone != request.requested_zone:
            print("⚠ Cross-zone allocation")
```

---

### System Status

```python
status = system.get_system_status()

print(f"Total Zones: {status['total_zones']}")
print(f"Total Slots: {status['total_slots']}")
print(f"Available: {status['available_slots']}")
print(f"Occupied: {status['occupied_slots']}")
print(f"Total Requests: {status['total_requests']}")
print(f"Active Requests: {status['active_requests']}")
print(f"Operations in History: {status['operations_in_history']}")
```

---

### Cancel Request

You can cancel a request at any stage (except RELEASED).

```python
# Cancel a request
result = system.cancel_parking_request(request_id)

if result['success']:
    print(f"✓ {result['message']}")
else:
    print(f"✗ {result['message']}")
```

**When to Cancel:**
- User changed their mind
- Vehicle not coming
- Error in request

---

### Rollback Operations

Undo the last k operations:

```python
# Rollback last 2 operations
rollback = system.rollback_operations(2)

if rollback['success']:
    print(f"✓ {rollback['message']}")
    for op in rollback['rolled_back']:
        print(f"  - {op['operation']} on {op['request_id']}")
else:
    print(f"✗ Rollback failed: {rollback['message']}")
```

**What Can Be Rolled Back:**
- Allocations
- Cancellations
- Releases

**Limitations:**
- Undoes k most recent operations from stack
- Cannot redo after rollback
- Order matters - LIFO (Last In, First Out)

---

## Common Workflows

### Workflow 1: Happy Path (Same Zone)

```python
# Setup
system.add_zone("ZONE-A")
system.add_parking_area_to_zone("ZONE-A", "A1", 10)
system.register_vehicle("CAR-001", "ZONE-A")

# Request → Allocate → Park → Leave
req = system.create_parking_request("CAR-001", "ZONE-A")
request_id = req['request_id']

alloc = system.allocate_parking(request_id)
# Penalty: 0 (same zone)

system.mark_parking_occupied(request_id)
# ... vehicle parked ...
system.release_parking(request_id)
```

---

### Workflow 2: Cross-Zone Allocation

```python
# Setup with linked zones
system.add_zone("ZONE-A")
system.add_zone("ZONE-B")
system.add_parking_area_to_zone("ZONE-A", "A1", 2)  # Small capacity
system.add_parking_area_to_zone("ZONE-B", "B1", 10)
system.link_adjacent_zones("ZONE-A", "ZONE-B")

# Fill ZONE-A
for i in range(2):
    system.create_parking_request(f"FILLER-{i}", "ZONE-A")
    system.allocate_parking(f"REQ-{i}")

# Now allocate to ZONE-B with penalty
system.register_vehicle("CAR-LATE", "ZONE-A")
req = system.create_parking_request("CAR-LATE", "ZONE-A")
alloc = system.allocate_parking(req['request_id'])
# Penalty: 50 (adjacent zone)
# Zone: ZONE-B
```

---

### Workflow 3: Request Cancellation

```python
# Create and allocate
req = system.create_parking_request("CAR-001", "ZONE-A")
request_id = req['request_id']
system.allocate_parking(request_id)

# User changes mind before parking
cancel = system.cancel_parking_request(request_id)
# Slot is released and available again
```

---

### Workflow 4: Error Recovery with Rollback

```python
# Allocate slot
req = system.create_parking_request("CAR-001", "ZONE-A")
alloc = system.allocate_parking(req['request_id'])

# Oops, wrong request!
rollback = system.rollback_operations(1)
# Allocation is undone, slot available again

# Correct allocation
req2 = system.create_parking_request("CAR-002", "ZONE-A")
system.allocate_parking(req2['request_id'])
```

---

## Troubleshooting

### Problem: "Vehicle not registered"

**Cause:** Trying to create request for unregistered vehicle

**Solution:**
```python
system.register_vehicle("CAR-001", "ZONE-A")
```

---

### Problem: "No available slots in any zone"

**Cause:** All zones are full

**Solutions:**
1. Check zone status:
   ```python
   status = system.get_system_status()
   # Check status['zones'] - all show 0 available
   ```

2. Release some slots:
   ```python
   system.release_parking(old_request_id)
   ```

3. Add more capacity:
   ```python
   system.add_parking_area_to_zone("ZONE-A", "A3", 10)
   ```

---

### Problem: "Invalid state transition"

**Cause:** Trying invalid operation for current state

**Example:**
```python
# Request is already RELEASED
system.mark_occupied(request_id)  # ✗ Invalid
```

**Solution:** Check request state first:
```python
request = system.get_request_by_id(request_id)
if request and request.state == 'ALLOCATED':
    system.mark_parking_occupied(request_id)  # ✓ Valid
```

---

### Problem: High penalties

**Cause:** Zone full, allocating to distant zones

**Solutions:**

1. **Add more capacity to popular zones:**
   ```python
   system.add_parking_area_to_zone("ZONE-A", "A4", 20)
   ```

2. **Link more adjacent zones:**
   ```python
   # Connect ZONE-A to ZONE-C directly
   system.link_adjacent_zones("ZONE-A", "ZONE-C")
   ```

3. **Balance load:**
   ```python
   # Encourage users to use less popular zones
   summary = system.get_system_status()
   # Guide users to zones with high availability
   ```

---

### Problem: Rollback not working

**Cause:** No operations to rollback or operation not recorded

**Check:**
```python
rollback = system.rollback_last_operation()
if not rollback['success']:
    print(rollback['message'])
    # "No operations to rollback"
```

**Note:** Rollback only works on allocation, cancellation, and release operations.

---

## Best Practices

### 1. Always Check Return Values

```python
# ✓ Good
result = system.allocate_parking(request_id)
if result['success']:
    slot_id = result['slot_id']
else:
    handle_error(result['message'])

# ✗ Bad
result = system.allocate_parking(request_id)
slot_id = result['slot_id']  # May not exist!
```

---

### 2. Store Request IDs

```python
# ✓ Good
request_map = {}
req = system.create_parking_request("CAR-001", "ZONE-A")
request_map["CAR-001"] = req['request_id']

# Later...
system.release_parking(request_map["CAR-001"])

# ✗ Bad
system.create_parking_request("CAR-001", "ZONE-A")
# Lost the request_id!
```

---

### 3. Monitor Capacity Proactively

```python
# ✓ Good
status = system.get_zone_status("ZONE-A")
if status['available'] < 5:
    send_alert("ZONE-A nearly full!")
    
# ✗ Bad
# Wait until allocation fails
```

---

### 4. Link Zones Strategically

```python
# ✓ Good - Create logical adjacency
system.link_adjacent_zones("NORTH-ENTRANCE", "NORTH-PARKING")
system.link_adjacent_zones("SOUTH-ENTRANCE", "SOUTH-PARKING")

# ✗ Bad - Everything connected to everything
for zone1 in all_zones:
    for zone2 in all_zones:
        system.link_adjacent_zones(zone1, zone2)
# Defeats purpose of priority allocation
```

---

### 5. Use Meaningful IDs

```python
# ✓ Good
system.add_zone("FACULTY-PARKING")
system.add_parking_area_to_zone("FACULTY-PARKING", "F-BUILDING-A", 20)
system.register_vehicle("PROF-SMITH-001", "FACULTY-PARKING")

# ✗ Bad
system.add_zone("Z1")
system.add_parking_area_to_zone("Z1", "A1", 20)
system.register_vehicle("V1", "Z1")
```

---

### 6. Handle Edge Cases

```python
# ✓ Good
def safe_allocate(vehicle_id, zone_id):
    # Check if vehicle registered
    if not system.get_vehicle(vehicle_id):
        system.register_vehicle(vehicle_id, zone_id)
    
    # Check if zone exists
    zones = system.list_all_zones()
    zone_ids = [z['zone_id'] for z in zones]
    if zone_id not in zone_ids:
        return {'success': False, 'message': 'Zone not found'}
    
    # Create and allocate
    req = system.create_parking_request(vehicle_id, zone_id)
    return system.allocate_parking(req['request_id'])
```

---

### 7. Clean Up Released Requests

```python
# Periodically clean old requests
released_requests = [
    req_id for req_id, req in system.requests.items()
    if req.current_state == RequestState.RELEASED
]

# Archive or remove old requests
# (Implementation depends on your needs)
```

---

## Performance Tips

### 1. Avoid Repeated Zone Queries

```python
# ✗ Bad - Multiple queries
for i in range(100):
    status = system.get_zone_status("ZONE-A")
    print(status['available'])

# ✓ Good - Cache result
status = system.get_zone_status("ZONE-A")
for i in range(100):
    print(status['available'])
```

---

### 2. Batch Operations When Possible

```python
# ✓ Better
vehicles = ["CAR-001", "CAR-002", "CAR-003"]
for vehicle_id in vehicles:
    system.register_vehicle(vehicle_id, "ZONE-A")
```

---

### 3. Pre-allocate Capacity

```python
# ✓ Good - Setup once
system.add_parking_area_to_zone("ZONE-A", "A1", 100)  # Large capacity

# ✗ Bad - Add incrementally
for i in range(100):
    system.add_parking_area_to_zone("ZONE-A", f"A{i}", 1)  # Wasteful
```

---

## Integration Examples

### With GUI (Tkinter)

```python
import tkinter as tk
from parking_system import ParkingSystem

class ParkingGUI:
    def __init__(self):
        self.system = ParkingSystem()
        self.root = tk.Tk()
        
        # Setup zones
        self.setup_system()
        
        # Create GUI elements
        self.create_widgets()
    
    def setup_system(self):
        self.system.add_zone("ZONE-A")
        self.system.add_parking_area_to_zone("ZONE-A", "A1", 20)
    
    def allocate_button_click(self):
        vehicle_id = self.vehicle_entry.get()
        zone_id = self.zone_entry.get()
        
        req = self.system.create_parking_request(vehicle_id, zone_id)
        alloc = self.system.allocate_parking(req['request_id'])
        
        if alloc['success']:
            self.result_label.config(text=f"Slot: {alloc['slot_id']}")
        else:
            self.result_label.config(text=f"Failed: {alloc['message']}")
```

---

### With Web API (Flask)

```python
from flask import Flask, jsonify, request
from parking_system import ParkingSystem

app = Flask(__name__)
system = ParkingSystem()

@app.route('/zones', methods=['POST'])
def create_zone():
    data = request.json
    system.add_zone(data['zone_id'])
    return jsonify({'success': True})

@app.route('/requests', methods=['POST'])
def create_request():
    data = request.json
    result = system.create_parking_request(
        data['vehicle_id'],
        data['zone_id']
    )
    return jsonify(result)

@app.route('/allocate/<request_id>', methods=['POST'])
def allocate(request_id):
    result = system.allocate_parking(request_id)
    return jsonify(result)
```

---

## Next Steps

- Read [API_REFERENCE.md](API_REFERENCE.md) for complete API details
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Check [../src/main.py](../src/main.py) for more examples
- Extend the system with GUI using Tkinter

---

For support, consult the documentation or review example code in the demo.
