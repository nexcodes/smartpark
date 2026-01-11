"""
Analytics Module - Calculates metrics and statistics for the parking system
"""
from enums import RequestState


class AnalyticsEngine:
    """
    Handles analytics and metrics calculation for the parking system
    
    DSA Focus:
    - Array traversal for calculating metrics
    - Counters and accumulators
    - Handles rollback-adjusted data
    """
    
    def __init__(self, parking_system):
        """
        Initialize analytics engine
        
        Args:
            parking_system: Reference to the ParkingSystem instance
        """
        self.parking_system = parking_system
    
    def get_average_parking_duration(self):
        """
        Calculate average parking duration for completed requests
        
        DSA: Array traversal with accumulator
        
        Returns:
            dict: Result with average duration in seconds and count
        """
        total_duration = 0
        completed_count = 0
        
        # Traverse all requests (array traversal)
        for request in self.parking_system.requests.values():
            # Only consider released requests with valid duration
            if request.current_state == RequestState.RELEASED:
                duration = request.get_parking_duration()
                if duration is not None:
                    total_duration += duration
                    completed_count += 1
        
        if completed_count == 0:
            return {
                'success': True,
                'average_duration_seconds': 0,
                'average_duration_minutes': 0,
                'completed_requests': 0,
                'message': 'No completed parking sessions yet'
            }
        
        avg_duration = total_duration / completed_count
        return {
            'success': True,
            'average_duration_seconds': round(avg_duration, 2),
            'average_duration_minutes': round(avg_duration / 60, 2),
            'completed_requests': completed_count,
            'message': f'Average from {completed_count} completed sessions'
        }
    
    def get_zone_utilization(self):
        """
        Calculate utilization rate for each zone
        
        DSA: Array traversal with counters
        
        Returns:
            dict: Zone utilization statistics
        """
        if not self.parking_system.zones:
            return {
                'success': False,
                'message': 'No zones in the system',
                'zones': []
            }
        
        zone_stats = []
        
        # Traverse zones (array traversal)
        for zone_id, zone in self.parking_system.zones.items():
            total_capacity = zone.get_total_capacity()
            occupied_count = zone.get_occupied_count()
            
            if total_capacity > 0:
                utilization_rate = (occupied_count / total_capacity) * 100
            else:
                utilization_rate = 0
            
            zone_stats.append({
                'zone_id': zone_id,
                'total_capacity': total_capacity,
                'occupied': occupied_count,
                'available': zone.get_available_count(),
                'utilization_rate': round(utilization_rate, 2)
            })
        
        # Sort by utilization rate (descending)
        zone_stats.sort(key=lambda x: x['utilization_rate'], reverse=True)
        
        return {
            'success': True,
            'zones': zone_stats,
            'total_zones': len(zone_stats),
            'message': f'Utilization calculated for {len(zone_stats)} zones'
        }
    
    def get_request_statistics(self):
        """
        Calculate statistics for cancelled vs completed requests
        
        DSA: Array traversal with state-based counters
        
        Returns:
            dict: Request statistics by state
        """
        # Initialize counters
        state_counts = {
            'requested': 0,
            'allocated': 0,
            'occupied': 0,
            'released': 0,
            'cancelled': 0
        }
        
        total_requests = len(self.parking_system.requests)
        
        # Traverse requests and count by state (array traversal)
        for request in self.parking_system.requests.values():
            if request.current_state == RequestState.REQUESTED:
                state_counts['requested'] += 1
            elif request.current_state == RequestState.ALLOCATED:
                state_counts['allocated'] += 1
            elif request.current_state == RequestState.OCCUPIED:
                state_counts['occupied'] += 1
            elif request.current_state == RequestState.RELEASED:
                state_counts['released'] += 1
            elif request.current_state == RequestState.CANCELLED:
                state_counts['cancelled'] += 1
        
        # Calculate completion vs cancellation rates
        completed = state_counts['released']
        cancelled = state_counts['cancelled']
        
        if total_requests > 0:
            completion_rate = (completed / total_requests) * 100
            cancellation_rate = (cancelled / total_requests) * 100
        else:
            completion_rate = 0
            cancellation_rate = 0
        
        return {
            'success': True,
            'total_requests': total_requests,
            'state_breakdown': state_counts,
            'completed_requests': completed,
            'cancelled_requests': cancelled,
            'completion_rate': round(completion_rate, 2),
            'cancellation_rate': round(cancellation_rate, 2),
            'message': f'Statistics for {total_requests} requests'
        }
    
    def get_peak_usage_zone(self):
        """
        Find the zone with highest utilization
        
        DSA: Array traversal with max-finding algorithm
        
        Returns:
            dict: Peak usage zone information
        """
        if not self.parking_system.zones:
            return {
                'success': False,
                'message': 'No zones in the system'
            }
        
        peak_zone_id = None
        peak_utilization = -1
        peak_occupied = 0
        peak_capacity = 0
        
        # Find max utilization (linear search)
        for zone_id, zone in self.parking_system.zones.items():
            total_capacity = zone.get_total_capacity()
            occupied_count = zone.get_occupied_count()
            
            if total_capacity > 0:
                utilization_rate = (occupied_count / total_capacity) * 100
                
                # Update peak if this zone has higher utilization
                if utilization_rate > peak_utilization:
                    peak_utilization = utilization_rate
                    peak_zone_id = zone_id
                    peak_occupied = occupied_count
                    peak_capacity = total_capacity
        
        if peak_zone_id is None:
            return {
                'success': False,
                'message': 'No zones with capacity found'
            }
        
        return {
            'success': True,
            'zone_id': peak_zone_id,
            'utilization_rate': round(peak_utilization, 2),
            'occupied': peak_occupied,
            'total_capacity': peak_capacity,
            'available': peak_capacity - peak_occupied,
            'message': f'Peak usage zone: {peak_zone_id} ({round(peak_utilization, 2)}% utilized)'
        }
    
    def get_cross_zone_allocation_statistics(self):
        """
        Calculate statistics for cross-zone allocations (penalty cases)
        
        DSA: Array traversal with conditional counting
        
        Returns:
            dict: Cross-zone allocation statistics
        """
        total_allocated = 0
        cross_zone_count = 0
        same_zone_count = 0
        
        # Traverse all requests
        for request in self.parking_system.requests.values():
            # Count only allocated and beyond states
            if request.current_state in [RequestState.ALLOCATED, RequestState.OCCUPIED, RequestState.RELEASED]:
                total_allocated += 1
                
                if request.is_cross_zone_allocation():
                    cross_zone_count += 1
                else:
                    same_zone_count += 1
        
        if total_allocated > 0:
            cross_zone_percentage = (cross_zone_count / total_allocated) * 100
        else:
            cross_zone_percentage = 0
        
        return {
            'success': True,
            'total_allocated': total_allocated,
            'same_zone_allocations': same_zone_count,
            'cross_zone_allocations': cross_zone_count,
            'cross_zone_percentage': round(cross_zone_percentage, 2),
            'message': f'{cross_zone_count} out of {total_allocated} allocations were cross-zone'
        }
    
    def get_comprehensive_analytics(self):
        """
        Get all analytics in one comprehensive report
        
        Returns:
            dict: Complete analytics report
        """
        return {
            'success': True,
            'average_duration': self.get_average_parking_duration(),
            'zone_utilization': self.get_zone_utilization(),
            'request_statistics': self.get_request_statistics(),
            'peak_usage_zone': self.get_peak_usage_zone(),
            'cross_zone_statistics': self.get_cross_zone_allocation_statistics()
        }
    
    def display_analytics_summary(self):
        """
        Generate a formatted text summary of analytics
        
        Returns:
            str: Formatted analytics summary
        """
        lines = []
        lines.append("=" * 60)
        lines.append("PARKING SYSTEM ANALYTICS SUMMARY")
        lines.append("=" * 60)
        
        # Average parking duration
        duration_data = self.get_average_parking_duration()
        lines.append("\n--- Average Parking Duration ---")
        if duration_data['completed_requests'] > 0:
            lines.append(f"  Average Duration: {duration_data['average_duration_minutes']} minutes")
            lines.append(f"  Completed Sessions: {duration_data['completed_requests']}")
        else:
            lines.append(f"  {duration_data['message']}")
        
        # Request statistics
        request_data = self.get_request_statistics()
        lines.append("\n--- Request Statistics ---")
        lines.append(f"  Total Requests: {request_data['total_requests']}")
        lines.append(f"  Completed: {request_data['completed_requests']} ({request_data['completion_rate']}%)")
        lines.append(f"  Cancelled: {request_data['cancelled_requests']} ({request_data['cancellation_rate']}%)")
        lines.append(f"  Active (Requested): {request_data['state_breakdown']['requested']}")
        lines.append(f"  Active (Allocated): {request_data['state_breakdown']['allocated']}")
        lines.append(f"  Active (Occupied): {request_data['state_breakdown']['occupied']}")
        
        # Zone utilization
        zone_data = self.get_zone_utilization()
        lines.append("\n--- Zone Utilization ---")
        if zone_data['success'] and zone_data['zones']:
            for zone in zone_data['zones']:
                lines.append(f"  {zone['zone_id']}: {zone['utilization_rate']}% "
                           f"({zone['occupied']}/{zone['total_capacity']} occupied)")
        else:
            lines.append(f"  {zone_data.get('message', 'No data available')}")
        
        # Peak usage zone
        peak_data = self.get_peak_usage_zone()
        lines.append("\n--- Peak Usage Zone ---")
        if peak_data['success']:
            lines.append(f"  Zone: {peak_data['zone_id']}")
            lines.append(f"  Utilization: {peak_data['utilization_rate']}%")
            lines.append(f"  Occupied: {peak_data['occupied']}/{peak_data['total_capacity']}")
        else:
            lines.append(f"  {peak_data['message']}")
        
        # Cross-zone allocations
        cross_zone_data = self.get_cross_zone_allocation_statistics()
        lines.append("\n--- Cross-Zone Allocation Statistics ---")
        lines.append(f"  Total Allocations: {cross_zone_data['total_allocated']}")
        lines.append(f"  Same Zone: {cross_zone_data['same_zone_allocations']}")
        lines.append(f"  Cross Zone: {cross_zone_data['cross_zone_allocations']} "
                   f"({cross_zone_data['cross_zone_percentage']}%)")
        
        lines.append("\n" + "=" * 60)
        
        return "\n".join(lines)
