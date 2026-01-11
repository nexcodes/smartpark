# Quick Start Guide

Get up and running with SmartPark in 5 minutes!

---

## Installation

**Requirements:**
- Python 3.8 or higher
- No external dependencies needed!

**Setup:**
```bash
# Clone the repository
git clone <repository-url>
cd py_project

# Verify Python installation
python --version
```

---

## Run the Demo

```bash
cd src
python main.py
```

You'll see comprehensive demonstrations of all features with detailed output.

---

## Your First Parking System (5 Minutes)

### Step 1: Create a Simple System (1 minute)

Create a new file `my_parking.py`:

```python
from parking_system import ParkingSystem

# Initialize system
system = ParkingSystem()

# Create a zone with 10 parking slots
system.add_zone("MAIN-ZONE")
system.add_parking_area_to_zone("MAIN-ZONE", "AREA-1", capacity=10)

print("✓ Parking system created with 10 slots")
```

Run it:
```bash
python my_parking.py
```

---

### Step 2: Register a Vehicle and Park (2 minutes)

Add to `my_parking.py`:

```python
# Register your vehicle
system.register_vehicle("MY-CAR", preferred_zone="MAIN-ZONE")
print("✓ Vehicle registered")

# Request parking
result = system.create_parking_request("MY-CAR", "MAIN-ZONE")
request_id = result['request_id']
print(f"✓ Request created: {request_id}")

# Allocate a slot
allocation = system.allocate_parking(request_id)
if allocation['success']:
    print(f"✓ Allocated slot: {allocation['slot_id']}")
    print(f"  Penalty: {allocation['penalty']}")
```

---

### Step 3: Complete the Parking Cycle (2 minutes)

Add to `my_parking.py`:

```python
# Mark as occupied (vehicle has parked)
system.mark_occupied(request_id)
print("✓ Vehicle parked")

# Check zone status
status = system.get_zone_status("MAIN-ZONE")
print(f"✓ Zone status: {status['occupied']}/{status['total_capacity']} occupied")

# Release parking (vehicle leaves)
release = system.release_parking(request_id)
print(f"✓ Vehicle left after {release['duration']:.0f} seconds")

# Check zone status again
status = system.get_zone_status("MAIN-ZONE")
print(f"✓ Zone status: {status['occupied']}/{status['total_capacity']} occupied")
```

**Complete Code:**

```python
from parking_system import ParkingSystem

# Initialize
system = ParkingSystem()
system.add_zone("MAIN-ZONE")
system.add_parking_area_to_zone("MAIN-ZONE", "AREA-1", capacity=10)

# Register and park
system.register_vehicle("MY-CAR", "MAIN-ZONE")
result = system.create_parking_request("MY-CAR", "MAIN-ZONE")
request_id = result['request_id']

allocation = system.allocate_parking(request_id)
print(f"Allocated: {allocation['slot_id']}, Penalty: {allocation['penalty']}")

system.mark_occupied(request_id)
print("Vehicle parked!")

# Later... release
release = system.release_parking(request_id)
print(f"Vehicle left after {release['duration']:.0f} seconds")
```

---

## Understanding Cross-Zone Allocation

### Setup Multiple Zones

```python
from parking_system import ParkingSystem

system = ParkingSystem()

# Create three zones
system.add_zone("ZONE-A")
system.add_zone("ZONE-B")
system.add_zone("ZONE-C")

# Add parking areas (ZONE-A has only 2 slots)
system.add_parking_area_to_zone("ZONE-A", "A1", capacity=2)
system.add_parking_area_to_zone("ZONE-B", "B1", capacity=10)
system.add_parking_area_to_zone("ZONE-C", "C1", capacity=10)

# Link zones (A adjacent to B, B adjacent to C)
system.link_adjacent_zones("ZONE-A", "ZONE-B")
system.link_adjacent_zones("ZONE-B", "ZONE-C")
```

### Test Cross-Zone Allocation

```python
# Fill up ZONE-A completely
for i in range(2):
    system.register_vehicle(f"FILLER-{i}", "ZONE-A")
    req = system.create_parking_request(f"FILLER-{i}", "ZONE-A")
    system.allocate_parking(req['request_id'])

print("ZONE-A is now full (2/2 occupied)")

# Try to park in ZONE-A (will get ZONE-B with penalty)
system.register_vehicle("LATE-CAR", "ZONE-A")
req = system.create_parking_request("LATE-CAR", "ZONE-A")
allocation = system.allocate_parking(req['request_id'])

print(f"Requested: ZONE-A")
print(f"Allocated: {allocation['zone_id']}")
print(f"Penalty: {allocation['penalty']}")
# Output: Allocated: ZONE-B, Penalty: 50 (adjacent zone)
```

---

## Common Patterns

### Pattern 1: Check Before Allocate

```python
# Good practice: Check zone availability first
status = system.get_zone_status("ZONE-A")
if status['available'] > 0:
    # Allocate in preferred zone
    req = system.create_parking_request(vehicle_id, "ZONE-A")
else:
    # Suggest alternative zone
    all_zones = system.list_all_zones()
    available_zones = [z for z in all_zones if z['available'] > 0]
    if available_zones:
        best_zone = max(available_zones, key=lambda z: z['available'])
        print(f"ZONE-A full. Try {best_zone['zone_id']} instead")
```

---

### Pattern 2: Batch Registration

```python
# Register multiple vehicles at once
vehicles = [
    ("CAR-001", "ZONE-A"),
    ("CAR-002", "ZONE-A"),
    ("CAR-003", "ZONE-B"),
]

for vehicle_id, preferred_zone in vehicles:
    system.register_vehicle(vehicle_id, preferred_zone)
    print(f"✓ Registered {vehicle_id}")
```

---

### Pattern 3: Monitor Occupancy

```python
def print_system_status(system):
    summary = system.get_system_summary()
    print("\n=== System Status ===")
    print(f"Total Slots: {summary['total_slots']}")
    print(f"Available: {summary['available_slots']}")
    print(f"Occupied: {summary['occupied_slots']}")
    print(f"Occupancy: {summary['overall_occupancy_rate']:.1f}%")
    print(f"Active Requests: {summary['active_requests']}")
    print()

# Use it
print_system_status(system)
```

---

### Pattern 4: Error Handling

```python
def safe_parking_request(system, vehicle_id, zone_id):
    """Safely create and allocate parking request"""
    
    # Check vehicle registered
    if not system.get_vehicle(vehicle_id):
        return {'success': False, 'message': 'Vehicle not registered'}
    
    # Create request
    req_result = system.create_parking_request(vehicle_id, zone_id)
    if not req_result['success']:
        return req_result
    
    # Allocate
    alloc_result = system.allocate_parking(req_result['request_id'])
    return alloc_result

# Use it
result = safe_parking_request(system, "CAR-001", "ZONE-A")
if result['success']:
    print(f"Success: {result['slot_id']}")
else:
    print(f"Failed: {result['message']}")
```

---

## Next Steps

1. **Read Full Documentation:**
   - [USER_GUIDE.md](USER_GUIDE.md) - Comprehensive usage guide
   - [API_REFERENCE.md](API_REFERENCE.md) - Complete API documentation
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design details
   - [DSA_CONCEPTS.md](DSA_CONCEPTS.md) - Data structures explained

2. **Explore Examples:**
   - Check [../src/main.py](../src/main.py) for advanced examples
   - See demo outputs for expected behavior

3. **Extend the System:**
   - Add GUI using Tkinter
   - Implement payment system
   - Add priority queues for VIP
   - Create RESTful API

4. **Learn DSA:**
   - Study the data structures used
   - Analyze algorithm complexities
   - Understand design decisions

---

## Quick Reference

### Essential Commands

```python
# Setup
system = ParkingSystem()
system.add_zone("ZONE-A")
system.add_parking_area_to_zone("ZONE-A", "A1", 10)

# Vehicle Operations
system.register_vehicle("CAR-001", "ZONE-A")

# Parking Flow
req = system.create_parking_request("CAR-001", "ZONE-A")
alloc = system.allocate_parking(req['request_id'])
system.mark_occupied(req['request_id'])
system.release_parking(req['request_id'])

# Monitoring
system.get_zone_status("ZONE-A")
system.get_system_summary()

# Advanced
system.cancel_request(request_id)
system.rollback_last_operation()
```

---

## Troubleshooting

**Problem:** Import errors
```bash
# Solution: Run from src/ directory
cd src
python my_parking.py
```

**Problem:** "Vehicle not registered"
```python
# Solution: Register before creating request
system.register_vehicle("CAR-001", "ZONE-A")
```

**Problem:** "No available slots"
```python
# Solution: Add more capacity or release slots
system.add_parking_area_to_zone("ZONE-A", "A2", 10)
```

---

## Tips

✓ Always check `success` field in results  
✓ Store request IDs for later operations  
✓ Monitor zone capacity proactively  
✓ Link zones strategically for better allocation  
✓ Use meaningful IDs for zones and vehicles  

---

**You're ready to use SmartPark! Start building your parking management system now.** 🚗🅿️