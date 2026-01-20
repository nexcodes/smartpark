"""
Test suite for RequestState enum
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from enums import RequestState


class TestRequestState(unittest.TestCase):
    """Test cases for RequestState enum"""
    
    def test_enum_values(self):
        """Test that all enum values exist"""
        self.assertEqual(RequestState.REQUESTED.value, "REQUESTED")
        self.assertEqual(RequestState.ALLOCATED.value, "ALLOCATED")
        self.assertEqual(RequestState.OCCUPIED.value, "OCCUPIED")
        self.assertEqual(RequestState.RELEASED.value, "RELEASED")
        self.assertEqual(RequestState.CANCELLED.value, "CANCELLED")
    
    def test_valid_transition_requested_to_allocated(self):
        """Test valid transition from REQUESTED to ALLOCATED"""
        result = RequestState.is_valid_transition(
            RequestState.REQUESTED, 
            RequestState.ALLOCATED
        )
        self.assertTrue(result)
    
    def test_valid_transition_requested_to_cancelled(self):
        """Test valid transition from REQUESTED to CANCELLED"""
        result = RequestState.is_valid_transition(
            RequestState.REQUESTED, 
            RequestState.CANCELLED
        )
        self.assertTrue(result)
    
    def test_valid_transition_allocated_to_occupied(self):
        """Test valid transition from ALLOCATED to OCCUPIED"""
        result = RequestState.is_valid_transition(
            RequestState.ALLOCATED, 
            RequestState.OCCUPIED
        )
        self.assertTrue(result)
    
    def test_valid_transition_allocated_to_cancelled(self):
        """Test valid transition from ALLOCATED to CANCELLED"""
        result = RequestState.is_valid_transition(
            RequestState.ALLOCATED, 
            RequestState.CANCELLED
        )
        self.assertTrue(result)
    
    def test_valid_transition_occupied_to_released(self):
        """Test valid transition from OCCUPIED to RELEASED"""
        result = RequestState.is_valid_transition(
            RequestState.OCCUPIED, 
            RequestState.RELEASED
        )
        self.assertTrue(result)
    
    def test_invalid_transition_requested_to_occupied(self):
        """Test invalid transition from REQUESTED to OCCUPIED"""
        result = RequestState.is_valid_transition(
            RequestState.REQUESTED, 
            RequestState.OCCUPIED
        )
        self.assertFalse(result)
    
    def test_invalid_transition_requested_to_released(self):
        """Test invalid transition from REQUESTED to RELEASED"""
        result = RequestState.is_valid_transition(
            RequestState.REQUESTED, 
            RequestState.RELEASED
        )
        self.assertFalse(result)
    
    def test_invalid_transition_allocated_to_released(self):
        """Test invalid transition from ALLOCATED to RELEASED"""
        result = RequestState.is_valid_transition(
            RequestState.ALLOCATED, 
            RequestState.RELEASED
        )
        self.assertFalse(result)
    
    def test_invalid_transition_occupied_to_allocated(self):
        """Test invalid transition from OCCUPIED to ALLOCATED"""
        result = RequestState.is_valid_transition(
            RequestState.OCCUPIED, 
            RequestState.ALLOCATED
        )
        self.assertFalse(result)
    
    def test_invalid_transition_occupied_to_cancelled(self):
        """Test invalid transition from OCCUPIED to CANCELLED"""
        result = RequestState.is_valid_transition(
            RequestState.OCCUPIED, 
            RequestState.CANCELLED
        )
        self.assertFalse(result)
    
    def test_invalid_transition_released_to_any(self):
        """Test that RELEASED cannot transition to any state"""
        states = [
            RequestState.REQUESTED,
            RequestState.ALLOCATED,
            RequestState.OCCUPIED,
            RequestState.CANCELLED
        ]
        
        for state in states:
            result = RequestState.is_valid_transition(RequestState.RELEASED, state)
            self.assertFalse(result, f"RELEASED should not transition to {state}")
    
    def test_invalid_transition_cancelled_to_any(self):
        """Test that CANCELLED cannot transition to any state"""
        states = [
            RequestState.REQUESTED,
            RequestState.ALLOCATED,
            RequestState.OCCUPIED,
            RequestState.RELEASED
        ]
        
        for state in states:
            result = RequestState.is_valid_transition(RequestState.CANCELLED, state)
            self.assertFalse(result, f"CANCELLED should not transition to {state}")
    
    def test_same_state_transition(self):
        """Test transitions to the same state"""
        # Same state transitions should be invalid
        for state in RequestState:
            result = RequestState.is_valid_transition(state, state)
            self.assertFalse(result, f"{state} should not transition to itself")


if __name__ == '__main__':
    unittest.main()
