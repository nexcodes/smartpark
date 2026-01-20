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
- **State Machine**: Robust request lifecycle management with validated transitions
- **Rollback Support**: Stack-based rollback for undoing operations
- **Real-time Monitoring**: Zone occupancy tracking and analytics
- **Dual Interface**: Complete CLI and GUI implementations sharing the same backend

### Advanced Features
- **Adjacency Graph**: Custom graph implementation for zone relationships
- **Dynamic Allocation**: First-fit algorithm for slot allocation
- **Request History**: Operation history tracking with rollback support
- **Cancellation Support**: Cancel requests at any stage
- **Comprehensive Analytics**: 6 analytics methods for system insights
  - Average parking duration
  - Zone utilization rates
  - Request statistics by state
  - Peak usage zone identification
  - Cross-zone allocation tracking
  - Export analytics to text files

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

### Running the System

#### CLI Interface (Menu-Driven)
```bash
cd src
python main.py
```

This launches an **interactive menu-driven interface** with 23 operations:
- **Setup Operations** (4): Add zones, parking areas, link adjacent zones, and register vehicles
- **Parking Operations** (5): Create requests, allocate, occupy, release, and cancel
- **Query Operations** (5): View system status, zone status, request details, zones, and vehicles
- **Analytics** (6): Comprehensive metrics including duration, utilization, statistics, and trends
- **Advanced Operations** (2): Rollback operations and view operation history
- **System Operations** (1): Exit the system

The CLI provides real-time feedback with emoji indicators (✅, ❌, ℹ️) and comprehensive input validation.

#### GUI Interface (Tkinter Application)
```bash
cd src
python gui_main.py
```

This launches a **windowed application** with 6 tabs:
- **Setup**: Configure zones, areas, adjacency, and vehicles
- **Dashboard**: View system overview with real-time statistics
- **Request**: Create and manage parking requests
- **Status**: Monitor zones, vehicles, and request details
- **Rollback**: Undo operations and view operation history
- **Analytics**: View metrics and export analytics reports

The GUI provides visual feedback, color-coded status indicators, and intuitive forms for all operations.

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
result = system.register_vehicle("CAR-001", preferred_zone="ZONE-A")
print(result['message'])

# Create parking request
result = system.create_parking_request("CAR-001", "ZONE-A")
request_id = result['request_id']
print(f"Request ID: {request_id}, State: {result['state']}")

# Allocate parking
allocation = system.allocate_parking(request_id)

if allocation['success']:
    print(f"Slot: {allocation['slot_id']}")
    print(f"Zone: {allocation['zone_id']}")
    print(f"Penalty: {allocation['penalty']}")
```

### Monitoring & Analytics

```python
# Get system status
system_status = system.get_system_status()
print(f"Total slots: {system_status['total_slots']}")
print(f"Available: {system_status['available_slots']}")
print(f"Active requests: {system_status['active_requests']}")

# Get zone status
zone_status = system.get_zone_status("ZONE-A")
print(f"Occupied: {zone_status['occupied']}/{zone_status['total_capacity']}")
print(f"Number of areas: {zone_status['areas']}")

# Get request details
request = system.get_request_by_id(request_id)
print(f"State: {request.current_state.value}")
print(f"Allocated slot: {request.allocated_slot_id}")
```

### Cancellation & Rollback

```python
# Cancel a request
cancel_result = system.cancel_parking_request(request_id)
if cancel_result['success']:
    print(cancel_result['message'])

# Rollback last 2 operations
rollback_result = system.rollback_operations(2)
if rollback_result['success']:
    print(rollback_result['message'])
    for op in rollback_result['rolled_back']:
        print(f"  - {op['operation']} on {op['request_id']}")
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
- `mark_parking_occupied(request_id)` - Mark vehicle as parked
- `release_parking(request_id)` - Release parking slot
- `cancel_parking_request(request_id)` - Cancel request

#### Query Operations
- `get_system_status()` - Get overall system statistics
- `get_zone_status(zone_id)` - Get zone details
- `get_request_by_id(request_id)` - Get request details
- `get_all_requests()` - List all parking requests

#### Analytics Operations
- `analytics.get_average_parking_duration()` - Calculate average parking duration
- `analytics.get_zone_utilization()` - Get utilization rates for all zones
- `analytics.get_request_statistics()` - Get request breakdown by state
- `analytics.get_peak_usage_zone()` - Identify most utilized zone
- `analytics.get_cross_zone_allocation_statistics()` - Track cross-zone allocations
- `analytics.get_comprehensive_analytics()` - Get all analytics data

#### Rollback Operations
- `rollback_operations(k)` - Rollback last k operations

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
│   ├── main.py                     # CLI interface (23 menu operations)
│   ├── gui_main.py                 # GUI entry point
│   ├── parking_system.py           # Main controller
│   ├── allocation_engine.py        # Slot allocation logic
│   ├── rollback_manager.py         # Stack-based rollback operations
│   ├── analytics.py                # Analytics engine with 6 metrics
│   ├── zone.py                     # Zone class with adjacency graph
│   ├── parking_area.py             # Parking area class (array container)
│   ├── parking_slot.py             # Individual slot class
│   ├── vehicle.py                  # Vehicle class
│   ├── parking_request.py          # Request with state machine
│   ├── enums.py                    # Enumerations & constants
│   └── ui/                         # GUI components (Tkinter)
│       ├── __init__.py             # UI package initializer
│       ├── main_window.py          # Main application window
│       ├── setup_screen.py         # Setup tab
│       ├── dashboard_screen.py     # Dashboard tab
│       ├── request_screen.py       # Request management tab
│       ├── status_screen.py        # Status monitoring tab
│       ├── rollback_screen.py      # Rollback operations tab
│       ├── analytics_screen.py     # Analytics & reports tab
│       └── theme.py                # UI theming constants
├── docs/
│   ├── API.md                      # Complete API documentation
│   ├── ARCHITECTURE.md             # System design & algorithms
│   ├── DSA_CONCEPTS.md             # Data structures explained
│   ├── QUICK_START.md              # Getting started guide
│   ├── USER_GUIDE.md               # User manual with examples
│   ├── UI.md                       # Interface documentation (CLI & GUI)
│   └── README.md                   # Documentation index
├── planning/
│   └── roadmap.md                  # Development roadmap
├── exports/
│   └── summary/                    # Analytics export directory
├── .gitignore                      # Git ignore rules
└── readme.md                       # This file
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

## 🧪 Testing & Usage

### CLI Testing
Run the interactive menu to test all features:

```bash
cd src
python main.py
```

### GUI Testing
Run the graphical interface to visually test the system:

```bash
cd src
python gui_main.py
```

### Test Coverage

**Allocation Logic:**
- ✅ Same-zone allocation (0 penalty)
- ✅ Cross-zone allocation - adjacent (50 penalty)
- ✅ Cross-zone allocation - distant (100 penalty)
- ✅ Allocation failure (no available slots)

**State Management:**
- ✅ Request lifecycle (REQUESTED → ALLOCATED → OCCUPIED → RELEASED)
- ✅ Request cancellation at various states
- ✅ State transition validation
- ✅ Invalid state transition rejection

**Advanced Features:**
- ✅ Rollback operations (stack-based undo)
- ✅ Zone capacity management
- ✅ Analytics calculations (6 different metrics)
- ✅ Edge cases (full capacity, invalid requests, duplicate IDs)

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

Contributions are welcome! Please follow these guidelines:

### Completed Features ✅
- ✅ GUI using Tkinter (6-tab interface)
- ✅ Export analytics to text files
- ✅ Dual interface support (CLI & GUI)
- ✅ Comprehensive state machine validation
- ✅ Stack-based rollback system

### Areas for Enhancement

**High Priority:**
- [ ] Add priority queue for VIP requests
- [ ] Unit test coverage with pytest
- [ ] Database persistence (SQLite)
- [ ] Export analytics to CSV/JSON formats

**Medium Priority:**
- [ ] Add pricing/payment system
- [ ] Performance optimization for large-scale scenarios
- [ ] Real-time notifications for slot availability
- [ ] Reservation system with time slots

**Future Enhancements:**
- [ ] RESTful API layer
- [ ] Multi-tenant support
- [ ] Mobile-responsive web interface
- [ ] Heat map visualization for zone usage

### Contributing Process
1. Check `planning/roadmap.md` for planned features
2. Review `docs/ARCHITECTURE.md` to understand system design
3. Follow DSA implementation patterns from `docs/DSA_CONCEPTS.md`
4. Ensure both CLI and GUI interfaces are updated for new features
5. Update relevant documentation in `docs/`

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Authors

**DSA Project Team**
- University of Management and Technology (UMT)
- Semester 3 - Data Structures & Algorithms

---

## 📞 Support & Documentation

### Quick Access
- **Getting Started**: See [docs/QUICK_START.md](docs/QUICK_START.md)
- **API Reference**: See [docs/API.md](docs/API.md)
- **Architecture Details**: See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **DSA Concepts**: See [docs/DSA_CONCEPTS.md](docs/DSA_CONCEPTS.md)
- **User Guide**: See [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
- **Interface Guide**: See [docs/UI.md](docs/UI.md)
- **Development Roadmap**: See [planning/roadmap.md](planning/roadmap.md)

### Getting Help
- Check comprehensive documentation in `docs/` folder
- Review code examples in `docs/QUICK_START.md`
- Examine the interactive demos in both CLI and GUI

---

## 🙏 Acknowledgments

- Course: Data Structures & Algorithms
- Institution: University of Management and Technology
- Focus: Practical DSA implementation in real-world scenarios

---

**Made with ❤️ for learning DSA concepts**