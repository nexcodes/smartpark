# SmartPark Testing Documentation

## Overview

SmartPark uses Python's built-in `unittest` framework for comprehensive testing of all system components. The test suite validates data structure implementations, state machine transitions, graph operations, and business logic.

## Test Structure

```
tests/
├── test.py                    # Interactive test runner
├── test_enums.py             # State machine validation tests
├── test_parking_area.py      # Array-based parking area tests
├── test_parking_slot.py      # Individual slot tests
├── test_parking_system.py    # Core system integration tests
├── test_vehicle.py           # Vehicle registration tests
└── test_zone.py              # Graph node (zone) tests
```

## Running Tests

### Interactive Test Runner

The recommended way to run tests is using the interactive runner:

```bash
cd tests
python test.py
```

This provides a menu-driven interface where you can:
- Run individual test modules
- Run all tests at once
- See detailed test results with color-coded output

### Running Specific Test Modules

To run a specific test module directly:

```bash
cd tests
python -m unittest test_enums
python -m unittest test_parking_area
python -m unittest test_parking_slot
python -m unittest test_vehicle
python -m unittest test_zone
```

### Running All Tests

To run all tests from the command line:

```bash
cd tests
python -m unittest discover -s . -p "test_*.py"
```

### Running Individual Test Cases

To run a specific test case:

```bash
cd tests
python -m unittest test_enums.TestRequestState.test_valid_transition_requested_to_allocated
```

## Available Test Modules

### 1. test_enums.py (14 tests)

Tests the state machine implementation (`RequestState` enum):

- **Valid Transitions**: Tests all allowed state transitions
  - REQUESTED → ALLOCATED
  - REQUESTED → CANCELLED
  - ALLOCATED → OCCUPIED
  - ALLOCATED → CANCELLED
  - OCCUPIED → RELEASED

- **Invalid Transitions**: Validates that forbidden transitions are blocked
  - REQUESTED → OCCUPIED (must go through ALLOCATED)
  - ALLOCATED → RELEASED (must go through OCCUPIED)
  - CANCELLED → any state (terminal state)
  - RELEASED → any state (terminal state)

- **Same State Transitions**: Ensures idempotent operations work correctly

**Key Pattern**: State validation is critical for maintaining system integrity

### 2. test_parking_area.py (13 tests)

Tests array-based parking area operations:

- **Initialization**: Verifies area creation with proper slot arrays
- **Availability Tracking**: Tests linear search for available slots
- **Capacity Metrics**: Validates available/occupied counts
- **Edge Cases**: 
  - All slots available
  - All slots occupied
  - Partial occupancy
  - Large capacity areas (100+ slots)

**DSA Focus**: Demonstrates linear search patterns on dynamic arrays

### 3. test_parking_slot.py (6 tests)

Tests individual slot state management:

- **Initialization**: Default available state
- **Allocation**: Marking slots as occupied
- **Release**: Freeing occupied slots
- **State Validation**: Prevents invalid operations (allocating occupied slots)
- **Lifecycle**: Multiple allocation-release cycles

**Pattern**: Basic building block with simple state management

### 4. test_vehicle.py (4 tests)

Tests vehicle registration and management:

- **Initialization**: With and without preferred zones
- **ID Formats**: Various vehicle ID patterns
- **Multiple Vehicles**: Concurrent vehicle tracking

**Scope**: Simple entity validation

### 5. test_zone.py (18 tests)

Tests graph node operations (zones):

- **Initialization**: Zone creation with adjacency lists
- **Parking Areas**: Adding multiple areas to zones
- **Adjacent Zones**: Graph edge management (adjacency lists)
- **Availability Search**: Delegating to areas
- **Capacity Aggregation**: Sum across all areas in zone
- **Edge Cases**: Empty zones, full zones

**DSA Focus**: Graph node with adjacency list implementation

### 6. test_parking_system.py (Partial - 4 passing tests)

Integration tests for the complete system:

- **Vehicle Registration**: Adding vehicles to the system
- **Zone Management**: Creating and linking zones

**Note**: Many tests in this module are currently disabled due to API changes. The passing tests validate core vehicle registration logic.

## Test Results Interpretation

### Success Indicators

```
✅ test_valid_transition_requested_to_allocated ... ok
```

- Test executed successfully
- All assertions passed
- Expected behavior confirmed

### Common Status Messages

- `ok`: Test passed successfully
- `FAIL`: Assertion failed (logic error)
- `ERROR`: Exception raised (implementation error)
- `SKIP`: Test intentionally skipped

### Test Summary

After running tests, you'll see a summary:

```
======================================================================
TEST SUMMARY
======================================================================
Tests Run: 109
Successes: 56
Failures: 0
Errors: 0
Skipped: 0
======================================================================
```

## Writing New Tests

### Test Class Structure

```python
import unittest
from src.module_name import ClassName

class TestClassName(unittest.TestCase):
    """Test suite for ClassName"""
    
    def setUp(self):
        """Run before each test method"""
        self.instance = ClassName()
    
    def tearDown(self):
        """Run after each test method (optional)"""
        pass
    
    def test_feature_name(self):
        """Test description"""
        # Arrange
        expected = "expected_value"
        
        # Act
        result = self.instance.method()
        
        # Assert
        self.assertEqual(result, expected)
```

### Naming Conventions

- Test files: `test_<module_name>.py`
- Test classes: `Test<ClassName>`
- Test methods: `test_<feature>_<scenario>`
  - Example: `test_allocation_when_zone_is_full`

### Common Assertions

```python
# Equality
self.assertEqual(actual, expected)
self.assertNotEqual(actual, unexpected)

# Boolean
self.assertTrue(condition)
self.assertFalse(condition)

# None checks
self.assertIsNone(value)
self.assertIsNotNone(value)

# Collections
self.assertIn(item, collection)
self.assertNotIn(item, collection)

# Exceptions
with self.assertRaises(ExceptionType):
    function_that_should_raise()
```

## Testing Patterns

### 1. State Machine Testing

```python
def test_valid_transition(self):
    """Ensure valid state transition is allowed"""
    result = RequestState.is_valid_transition(
        RequestState.REQUESTED, 
        RequestState.ALLOCATED
    )
    self.assertTrue(result)
```

### 2. Array Operations Testing

```python
def test_linear_search_pattern(self):
    """Test finding first available slot"""
    # Fill first 3 slots
    for i in range(3):
        self.area.slots[i].is_available = False
    
    # Fourth slot should be found
    slot = self.area.find_available_slot()
    self.assertEqual(slot.slot_id, "ZONE-A-A1-4")
```

### 3. Graph Operations Testing

```python
def test_adjacency_list(self):
    """Test zone adjacency tracking"""
    zone_a = Zone("ZONE-A")
    zone_b = Zone("ZONE-B")
    
    zone_a.add_adjacent_zone("ZONE-B")
    
    self.assertIn("ZONE-B", zone_a.adjacent_zones)
```

## Best Practices

### 1. Test Independence

Each test should be completely independent:

```python
def setUp(self):
    """Create fresh instances for each test"""
    self.system = ParkingSystem()
    self.zone = Zone("TEST-ZONE")
```

### 2. Descriptive Names

Use clear, descriptive test names:

```python
# ✅ Good
def test_allocation_fails_when_no_slots_available(self):

# ❌ Bad
def test_allocation(self):
```

### 3. Single Responsibility

Each test should verify one specific behavior:

```python
# ✅ Good - Tests one thing
def test_slot_becomes_available_after_release(self):
    slot.allocate("CAR-001")
    slot.release()
    self.assertTrue(slot.is_available)

# ❌ Bad - Tests multiple things
def test_slot_lifecycle(self):
    # Tests allocation, release, re-allocation...
```

### 4. Arrange-Act-Assert Pattern

Structure tests clearly:

```python
def test_feature(self):
    # Arrange - Set up test data
    zone = Zone("ZONE-A")
    area = ParkingArea("A1", 5)
    zone.add_parking_area(area)
    
    # Act - Execute the operation
    result = zone.get_total_capacity()
    
    # Assert - Verify the result
    self.assertEqual(result, 5)
```

### 5. Edge Cases

Always test boundary conditions:

```python
def test_empty_zone_has_zero_capacity(self):
    """Test zone with no areas"""
    self.assertEqual(self.zone.get_total_capacity(), 0)

def test_zone_with_100_areas(self):
    """Test zone with many areas"""
    for i in range(100):
        self.zone.add_parking_area(ParkingArea(f"A{i}", 10))
    self.assertEqual(self.zone.get_total_capacity(), 1000)
```

## Continuous Testing

### During Development

Run tests frequently while developing:

1. Write a failing test
2. Implement the feature
3. Run the test to verify it passes
4. Refactor if needed
5. Run all related tests to ensure no regressions

### Before Commits

Always run the full test suite before committing:

```bash
cd tests
python test.py
# Select option 10: Run ALL tests
```

## Test Coverage

Current test coverage by module:

| Module | Tests | Status |
|--------|-------|--------|
| enums.py | 14 | ✅ Complete |
| parking_area.py | 13 | ✅ Complete |
| parking_slot.py | 6 | ✅ Complete |
| vehicle.py | 4 | ✅ Complete |
| zone.py | 18 | ✅ Complete |
| parking_system.py | 4 | ⚠️ Partial |

**Total Passing Tests**: 56 tests passing

## Troubleshooting

### Import Errors

If you see import errors, ensure you're running tests from the `tests/` directory:

```bash
cd tests
python test.py
```

### Module Not Found

The test runner automatically adds the `src/` directory to the Python path. If you run tests manually, you may need to:

```bash
export PYTHONPATH="${PYTHONPATH}:../src"  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;..\src        # Windows
```

### Assertion Failures

When an assertion fails:

1. Read the error message carefully
2. Check the expected vs actual values
3. Verify your test assumptions
4. Use `print()` statements for debugging (remove before committing)

### Test Hangs

If a test hangs:

1. Check for infinite loops
2. Verify timeout conditions
3. Look for blocking I/O operations
4. Use `Ctrl+C` to interrupt

## Future Test Additions

Planned test modules (not yet implemented):

- `test_allocation_engine.py` - Allocation algorithm tests
- `test_rollback_manager.py` - Stack-based undo tests
- `test_analytics.py` - Metrics and reporting tests

These will be added as the corresponding features are finalized.

## Quick Reference

### Run All Tests
```bash
cd tests && python test.py
# Select: 10
```

### Run Specific Module
```bash
cd tests
python -m unittest test_enums
```

### Check Test Count
```bash
cd tests
python -m unittest discover -v | grep -c "ok"
```

### Test Verbosity Levels
```bash
# Minimal output
python -m unittest test_enums

# Verbose output (-v)
python -m unittest test_enums -v

# Very verbose (-vv) - not standard but some frameworks support it
python -m unittest test_enums -v
```

## Additional Resources

- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- Project Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
- DSA Concepts: [DSA_CONCEPTS.md](DSA_CONCEPTS.md)
- Quick Start Guide: [QUICK_START.md](QUICK_START.md)

---

**Last Updated**: January 20, 2026
**Test Framework**: Python unittest
**Total Tests**: 56 passing tests
