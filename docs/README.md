# SmartPark Documentation

Complete documentation for the SmartPark Intelligent Parking Allocation System.

---

## 📚 Documentation Index

### Getting Started
1. **[Quick Start Guide](QUICK_START.md)** ⚡
   - Get running in 5 minutes
   - Basic examples
   - Common patterns
   - **Start here if you're new!**

2. **[User Guide](USER_GUIDE.md)** 📖
   - Comprehensive usage instructions
   - All features explained
   - Advanced workflows
   - Troubleshooting

### Technical Reference
3. **[API Reference](API_REFERENCE.md)** 🔧
   - Complete API documentation
   - All methods and parameters
   - Return value formats
   - Code examples

4. **[Architecture](ARCHITECTURE.md)** 🏗️
   - System design
   - Component interactions
   - Design patterns
   - Scalability considerations

5. **[DSA Concepts](DSA_CONCEPTS.md)** 🎓
   - Data structures used
   - Algorithm explanations
   - Complexity analysis
   - Learning outcomes

---

## Quick Links

### For First-Time Users
→ Start with [QUICK_START.md](QUICK_START.md)

### For Developers
→ Read [API_REFERENCE.md](API_REFERENCE.md)

### For Students Learning DSA
→ Study [DSA_CONCEPTS.md](DSA_CONCEPTS.md)

### For System Designers
→ Review [ARCHITECTURE.md](ARCHITECTURE.md)

### For General Usage
→ Consult [USER_GUIDE.md](USER_GUIDE.md)

---

## Documentation Overview

### Quick Start Guide
**Purpose:** Get you up and running immediately  
**Time:** 5-10 minutes  
**Content:**
- Installation steps
- First parking system
- Basic workflows
- Quick reference

---

### User Guide
**Purpose:** Comprehensive feature coverage  
**Time:** 30-45 minutes  
**Content:**
- Basic operations
- Advanced features
- Common workflows
- Best practices
- Troubleshooting
- Integration examples

---

### API Reference
**Purpose:** Complete technical reference  
**Time:** Reference as needed  
**Content:**
- All public methods
- Parameter specifications
- Return value formats
- Error handling
- Performance characteristics
- Complete workflow examples

---

### Architecture
**Purpose:** Understand system design  
**Time:** 20-30 minutes  
**Content:**
- Component architecture
- Design decisions
- Algorithm details
- Memory layout
- Scalability analysis
- Future enhancements

---

### DSA Concepts
**Purpose:** Learn data structures & algorithms  
**Time:** 45-60 minutes  
**Content:**
- Arrays implementation
- Stack for rollback
- Graph for zones
- State machines
- Hash tables
- Search algorithms
- Complexity analysis
- Future DSA enhancements

---

## System Features

### Core Functionality
- ✅ Multi-zone parking management
- ✅ Intelligent slot allocation
- ✅ Same-zone priority allocation
- ✅ Cross-zone fallback with penalties
- ✅ State machine for request lifecycle
- ✅ Stack-based rollback operations
- ✅ Real-time zone monitoring
- ✅ Comprehensive analytics

### Data Structures
- 🔢 **Arrays** - Slot and area storage
- 📚 **Stacks** - Rollback operations
- 🕸️ **Graphs** - Zone adjacency
- 🔄 **State Machines** - Request lifecycle
- #️⃣ **Hash Tables** - Fast lookups

### Algorithms
- 🔍 **Linear Search** - Find available slots
- 🎯 **First-Fit** - Allocation strategy
- 🌐 **BFS** - Cross-zone traversal
- ✅ **State Validation** - Transition checking

---

## Project Structure

```
py_project/
├── docs/                       ← You are here
│   ├── README.md              ← This file
│   ├── QUICK_START.md         ← 5-minute guide
│   ├── USER_GUIDE.md          ← Complete usage
│   ├── API_REFERENCE.md       ← Technical API docs
│   ├── ARCHITECTURE.md        ← System design
│   └── DSA_CONCEPTS.md        ← Data structures
├── src/
│   ├── main.py                ← Demo & examples
│   ├── parking_system.py      ← Main controller
│   ├── allocation_engine.py   ← Slot allocation
│   ├── rollback_manager.py    ← Undo operations
│   ├── zone.py                ← Zone management
│   ├── parking_area.py        ← Area management
│   ├── parking_slot.py        ← Individual slots
│   ├── vehicle.py             ← Vehicle data
│   ├── parking_request.py     ← Request handling
│   └── enums.py               ← Enumerations
├── planning/
│   └── roadmap.md             ← Development plan
├── .gitignore                 ← Git exclusions
└── README.md                  ← Project overview
```

---

## Learning Path

### For Beginners
1. Read [../README.md](../README.md) - Project overview
2. Follow [QUICK_START.md](QUICK_START.md) - Get hands-on
3. Explore [USER_GUIDE.md](USER_GUIDE.md) - Learn features
4. Study [DSA_CONCEPTS.md](DSA_CONCEPTS.md) - Understand theory

### For Developers
1. Read [API_REFERENCE.md](API_REFERENCE.md) - Learn API
2. Study [ARCHITECTURE.md](ARCHITECTURE.md) - Understand design
3. Review source code in [../src/](../src/) - See implementation
4. Run [../src/main.py](../src/main.py) - See examples

### For DSA Students
1. Read [DSA_CONCEPTS.md](DSA_CONCEPTS.md) - Theory
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) - Application
3. Study source code - Implementation details
4. Analyze complexity - Big-O practice

---

## Key Concepts

### Penalty System
- **0 points** - Same zone as requested (ideal)
- **50 points** - Adjacent zone (acceptable)
- **100 points** - Distant zone (suboptimal)

### State Machine
```
REQUESTED → ALLOCATED → OCCUPIED → RELEASED
    ↓           ↓
CANCELLED   CANCELLED
```

### Zone Graph
```
ZONE-A ←→ ZONE-B ←→ ZONE-C
  ↓
ZONE-D
```

---

## Common Tasks

### Setup a Parking System
→ See [QUICK_START.md#step-1](QUICK_START.md)

### Allocate Parking
→ See [USER_GUIDE.md#basic-operations](USER_GUIDE.md#basic-operations)

### Monitor Zones
→ See [API_REFERENCE.md#get_zone_status](API_REFERENCE.md)

### Handle Cross-Zone Allocation
→ See [QUICK_START.md#cross-zone](QUICK_START.md#understanding-cross-zone-allocation)

### Rollback Operations
→ See [USER_GUIDE.md#rollback](USER_GUIDE.md#rollback-operations)

### Understand Data Structures
→ See [DSA_CONCEPTS.md](DSA_CONCEPTS.md)

---

## API Summary

### Zone Management
```python
add_zone(zone_id)
add_parking_area_to_zone(zone_id, area_id, capacity)
link_adjacent_zones(zone1_id, zone2_id)
get_zone_status(zone_id)
```

### Vehicle & Request Operations
```python
register_vehicle(vehicle_id, preferred_zone)
create_parking_request(vehicle_id, zone_id)
allocate_parking(request_id)
mark_occupied(request_id)
release_parking(request_id)
cancel_request(request_id)
```

### Monitoring & Analytics
```python
get_request_status(request_id)
get_system_summary()
list_all_zones()
```

### Advanced Operations
```python
rollback_last_operation()
```

---

## Performance

### Time Complexity
| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Add Zone | O(1) | Constant time |
| Find Slot | O(n×m) | n zones, m slots |
| Allocate | O(n×m) | Worst case all zones |
| Rollback | O(1) | Stack pop |
| Get Status | O(n) | Count slots |

### Space Complexity
- **Per Slot:** ~50 bytes
- **10,000 Slots:** ~500 KB
- **Conclusion:** Memory not a constraint

---

## Code Examples

### Minimal Example
```python
from parking_system import ParkingSystem

system = ParkingSystem()
system.add_zone("ZONE-A")
system.add_parking_area_to_zone("ZONE-A", "A1", 10)
system.register_vehicle("CAR-001", "ZONE-A")

req = system.create_parking_request("CAR-001", "ZONE-A")
alloc = system.allocate_parking(req['request_id'])
print(f"Allocated: {alloc['slot_id']}")
```

### Complete Workflow
See [QUICK_START.md](QUICK_START.md#your-first-parking-system-5-minutes)

---

## Troubleshooting

### Common Issues
- **"Vehicle not registered"** → Register vehicle first
- **"No available slots"** → Add capacity or release slots
- **"Invalid state transition"** → Check request state
- **Import errors** → Run from `src/` directory

### Detailed Solutions
See [USER_GUIDE.md#troubleshooting](USER_GUIDE.md#troubleshooting)

---

## Contributing

Areas for enhancement:
- [ ] GUI implementation (Tkinter)
- [ ] Priority queue for VIP requests
- [ ] True linked list for history
- [ ] Database persistence
- [ ] RESTful API
- [ ] Unit tests
- [ ] Performance optimizations

---

## Support

- **Questions:** Check relevant documentation file
- **Issues:** Review [USER_GUIDE.md#troubleshooting](USER_GUIDE.md#troubleshooting)
- **Examples:** See [../src/main.py](../src/main.py)
- **Learning:** Study [DSA_CONCEPTS.md](DSA_CONCEPTS.md)

---

## License

MIT License - See LICENSE file for details

---

## Academic Information

**Course:** Data Structures & Algorithms  
**Institution:** University of Management and Technology (UMT)  
**Semester:** 3  
**Focus:** Practical DSA implementation

---

## Version History

- **v1.0** - Initial release
  - Core parking system
  - All basic features
  - Complete documentation

---

**Start your journey:** [QUICK_START.md](QUICK_START.md) →

**Happy Coding! 🚗🅿️**