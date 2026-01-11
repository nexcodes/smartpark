# 🅿️ SMARTPARK - Intelligent Parking Allocation System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DSA Project](https://img.shields.io/badge/Project-DSA-orange.svg)](docs/)

A sophisticated smart parking allocation and management system built with Python, demonstrating advanced Data Structures and Algorithms (DSA) concepts. The system intelligently allocates parking slots across multiple zones with penalty-based cross-zone allocation, rollback capabilities, and comprehensive state management.

---

## 📋 Table of Contents

- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Data Structures Used](#-data-structures-used)
- [Getting Started](#-getting-started)
- [Usage Examples](#-usage-examples)
- [API Documentation](#-api-documentation)
- [State Machine](#-state-machine)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)

---

## ✨ Features

### Core Functionality
- **Multi-Zone Management**: Organize parking slots into zones and areas
- **Intelligent Allocation**: Same-zone priority with cross-zone fallback
- **Penalty System**: Automatic penalty calculation for cross-zone allocations
  - Adjacent zone: 50 penalty points
  - Distant zone: 100 penalty points
- **State Machine**: Robust request lifecycle management
- **Rollback Support**: Stack-based rollback for undoing operations
- **Real-time Monitoring**: Zone occupancy tracking and analytics

### Advanced Features
- **Adjacency Graph**: Custom graph implementation for zone relationships
- **Dynamic Allocation**: First-fit algorithm for slot allocation
- **Request History**: Linked-list based history tracking
- **Cancellation Support**: Cancel requests at any stage
- **Comprehensive Logging**: Detailed operation tracking

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   ParkingSystem                          │
│              (Main Controller)                           │
└────────────┬─────────────────────┬──────────────────────┘
             │                     │
    ┌────────▼────────┐   ┌────────▼────────┐
    │ AllocationEngine │   │ RollbackManager │
    │  (Slot Finder)   │   │  (Stack-based)  │
    └─────────────────┘   └─────────────────┘
             │
    ┌────────▼────────┐
    │  Zone Graph     │
    │  (Adjacency)    │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Parking Areas  │
    │   (Arrays)      │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │ Parking Slots   │
    │  (Individual)   │
    └─────────────────┘
```

### Component Hierarchy

1. **ParkingSystem**: Orchestrates all operations
2. **AllocationEngine**: Handles slot allocation logic with priority rules
3. **RollbackManager**: Manages undo operations using stack
4. **Zone**: Represents parking zones with adjacency lists
5. **ParkingArea**: Contains arrays of parking slots
6. **ParkingSlot**: Individual parking space
7. **Vehicle**: User's vehicle information
8. **ParkingRequest**: Request lifecycle with state machine

---

## 🔧 Data Structures Used

| Data Structure | Implementation | Purpose |
|----------------|----------------|---------|
| **Array** | Python List | Store parking slots, zones, parking areas |
| **Stack** | Python List | Rollback operations (LIFO) |
| **Graph (Adjacency List)** | Custom Array-based | Zone relationships for cross-zone allocation |
| **State Machine** | Enum-based | Request lifecycle management |
| **Hash Map** | Python Dict | Fast lookup for zones, vehicles, requests |
| **Linked List** | (Planned) | Request history tracking |
| **Queue** | (Planned) | Incoming request handling |

### Key Algorithms

- **First-Fit Allocation**: O(n) slot search
- **BFS/DFS Traversal**: Zone adjacency exploration
- **State Validation**: O(1) transition checking
- **Rollback**: O(1) stack operations

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- No external dependencies required (uses standard library)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd py_project
   ```

2. **No additional setup needed** - All components use Python standard library

### Running the Demo

```bash
cd src
python main.py
```

This will run comprehensive demonstrations including:
- Basic allocation operations
- Cross-zone allocation with penalties
- Request cancellation
- Rollback operations
- Zone status monitoring

---

## 💡 Usage Examples

### Basic Setup

```python
from parking_system import ParkingSystem

# Initialize system
system = ParkingSystem()

# Create zones
system.add_zone("ZONE-A")
system.add_zone("ZONE-B")

# Add parking areas
system.add_parking_area_to_zone("ZONE-A", "A1", capacity=10)
system.add_parking_area_to_zone("ZONE-B", "B1", capacity=15)

# Link adjacent zones
system.link_adjacent_zones("ZONE-A", "ZONE-B")
```

### Vehicle Registration & Parking

```python
# Register a vehicle
system.register_vehicle("CAR-001", preferred_zone="ZONE-A")

# Create parking request
result = system.create_parking_request("CAR-001", "ZONE-A")
request_id = result['request_id']

# Allocate parking
allocation = system.allocate_parking(request_id)

if allocation['success']:
    print(f"Slot: {allocation['slot_id']}")
    print(f"Zone: {allocation['zone_id']}")
    print(f"Penalty: {allocation['penalty']}")
```

### Monitoring & Analytics

```python
# Get zone status
status = system.get_zone_status("ZONE-A")
print(f"Occupied: {status['occupied']}/{status['total_capacity']}")
print(f"Occupancy Rate: {status['occupancy_rate']}%")

# Get request details
request_info = system.get_request_status(request_id)
print(f"State: {request_info['state']}")
print(f"Duration: {request_info['duration']}")
```

### Cancellation & Rollback

```python
# Cancel a request
system.cancel_request(request_id)

# Rollback last operation
rollback_result = system.rollback_last_operation()
if rollback_result['success']:
    print(f"Rolled back: {rollback_result['operation_type']}")
```

---

## 📖 API Documentation

### ParkingSystem Class

#### Zone Management
- `add_zone(zone_id)` - Create a new parking zone
- `add_parking_area_to_zone(zone_id, area_id, capacity)` - Add parking area
- `link_adjacent_zones(zone1_id, zone2_id)` - Create zone adjacency
- `get_zone_status(zone_id)` - Get zone statistics

#### Vehicle & Request Management
- `register_vehicle(vehicle_id, preferred_zone)` - Register vehicle
- `create_parking_request(vehicle_id, zone_id)` - Create new request
- `allocate_parking(request_id)` - Allocate parking slot
- `mark_occupied(request_id)` - Mark vehicle as parked
- `release_parking(request_id)` - Release parking slot
- `cancel_request(request_id)` - Cancel request

#### Operations
- `rollback_last_operation()` - Undo last operation
- `get_request_status(request_id)` - Get request details
- `list_all_zones()` - List all zones with status
- `get_system_summary()` - Get overall statistics

---

## 🔄 State Machine

### Request Lifecycle

```
    ┌──────────┐
    │REQUESTED │ (Initial state)
    └────┬─────┘
         │ allocate_parking()
         ▼
    ┌──────────┐
    │ALLOCATED │ (Slot assigned)
    └────┬─────┘
         │ mark_occupied()
         ▼
    ┌──────────┐
    │ OCCUPIED │ (Vehicle parked)
    └────┬─────┘
         │ release_parking()
         ▼
    ┌──────────┐
    │ RELEASED │ (Final state)
    └──────────┘
```

### Cancellation Path

```
REQUESTED → CANCELLED
ALLOCATED → CANCELLED
```

### State Validation
All state transitions are validated. Invalid transitions are rejected automatically.

---

## 📁 Project Structure

```
py_project/
├── src/
│   ├── __init__.py                 # Package initializer
│   ├── main.py                     # Demo & examples
│   ├── parking_system.py           # Main controller
│   ├── allocation_engine.py        # Slot allocation logic
│   ├── rollback_manager.py         # Rollback operations
│   ├── zone.py                     # Zone class
│   ├── parking_area.py             # Parking area class
│   ├── parking_slot.py             # Individual slot class
│   ├── vehicle.py                  # Vehicle class
│   ├── parking_request.py          # Request with state machine
│   └── enums.py                    # Enumerations & constants
├── docs/
│   └── (detailed documentation)
├── planning/
│   └── roadmap.md                  # Development roadmap
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

---

## 🎯 Allocation Strategy

### Priority Levels

1. **Same Zone** (Penalty: 0)
   - First choice if slots available
   - Best user experience

2. **Adjacent Zone** (Penalty: 50)
   - Second choice if same zone full
   - Uses adjacency graph

3. **Distant Zone** (Penalty: 100)
   - Last resort if no nearby slots
   - Any available zone

### Example Scenario

```
User requests ZONE-A parking:
└─ ZONE-A full? 
   ├─ No  → Allocate in ZONE-A (penalty: 0)
   └─ Yes → Check adjacent zones (ZONE-B)
      ├─ Slot available? → Allocate in ZONE-B (penalty: 50)
      └─ No → Check all zones (ZONE-C)
         ├─ Slot available? → Allocate in ZONE-C (penalty: 100)
         └─ No → Allocation failed
```

---

## 🧪 Testing

Run the main demo to see comprehensive test cases:

```bash
python src/main.py
```

### Test Coverage

- ✅ Same-zone allocation
- ✅ Cross-zone allocation (adjacent)
- ✅ Cross-zone allocation (distant)
- ✅ Request cancellation at various states
- ✅ Rollback operations
- ✅ State transition validation
- ✅ Zone capacity management
- ✅ Edge cases (full capacity, invalid requests)

---

## 🎓 Learning Objectives

This project demonstrates:

1. **Object-Oriented Design**: Clean class hierarchy
2. **Data Structures**: Arrays, stacks, graphs, state machines
3. **Algorithms**: First-fit, graph traversal, state validation
4. **Design Patterns**: State pattern, strategy pattern
5. **Error Handling**: Validation and recovery
6. **Code Organization**: Modular, maintainable architecture

---

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- [ ] Implement GUI using Tkinter
- [ ] Add priority queue for VIP requests
- [ ] Implement true linked list for history
- [ ] Add pricing/payment system
- [ ] Database persistence
- [ ] RESTful API layer
- [ ] Unit test coverage
- [ ] Performance optimization

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Authors

**DSA Project Team**
- University of Management and Technology (UMT)
- Semester 3 - Data Structures & Algorithms

---

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check documentation in `docs/` folder
- Review the roadmap in `planning/roadmap.md`

---

## 🙏 Acknowledgments

- Course: Data Structures & Algorithms
- Institution: University of Management and Technology
- Focus: Practical DSA implementation in real-world scenarios

---

**Made with ❤️ for learning DSA concepts**