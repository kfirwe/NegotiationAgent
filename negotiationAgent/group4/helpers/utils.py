"""
Utility functions for Group 4 negotiation agent
"""

import logging
import numpy as np
from typing import Dict, List, Any, Optional
from collections import defaultdict
import json
import time

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Setup logging configuration for the negotiation agent
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file path to write logs
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("Group4Negotiator")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def calculate_statistics(utilities: List[float]) -> Dict[str, float]:
    """
    Calculate comprehensive statistics for a list of utilities
    
    Args:
        utilities: List of utility values
    
    Returns:
        Dictionary containing various statistics
    """
    if not utilities:
        return {
            'count': 0,
            'mean': 0.0,
            'std': 0.0,
            'min': 0.0,
            'max': 0.0,
            'median': 0.0,
            'percentile_25': 0.0,
            'percentile_75': 0.0
        }
    
    utilities_array = np.array(utilities)
    
    return {
        'count': len(utilities),
        'mean': float(np.mean(utilities_array)),
        'std': float(np.std(utilities_array)),
        'min': float(np.min(utilities_array)),
        'max': float(np.max(utilities_array)),
        'median': float(np.median(utilities_array)),
        'percentile_25': float(np.percentile(utilities_array, 25)),
        'percentile_75': float(np.percentile(utilities_array, 75))
    }

def normalize_outcome(outcome: Any) -> Dict[str, Any]:
    """
    Normalize outcome to a consistent dictionary format
    
    Args:
        outcome: Outcome object or dictionary
    
    Returns:
        Normalized outcome dictionary
    """
    if isinstance(outcome, dict):
        return outcome
    
    # Handle different outcome types
    if hasattr(outcome, '__dict__'):
        return outcome.__dict__
    
    if hasattr(outcome, 'items'):
        return dict(outcome.items())
    
    # Fallback: convert to string representation
    return {'outcome': str(outcome)}

def save_negotiation_data(data: Dict[str, Any], filename: str) -> bool:
    """
    Save negotiation data to JSON file
    
    Args:
        data: Dictionary containing negotiation data
        filename: Output filename
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def load_negotiation_data(filename: str) -> Optional[Dict[str, Any]]:
    """
    Load negotiation data from JSON file
    
    Args:
        filename: Input filename
    
    Returns:
        Loaded data dictionary or None if failed
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def analyze_opponent_patterns(offers: List[Any]) -> Dict[str, Any]:
    """
    Analyze patterns in opponent offers
    
    Args:
        offers: List of opponent offers
    
    Returns:
        Dictionary containing pattern analysis
    """
    if not offers:
        return {'pattern_detected': False, 'analysis': 'No offers to analyze'}
    
    # Count value frequencies
    value_counts = defaultdict(int)
    issue_patterns = defaultdict(list)
    
    for offer in offers:
        normalized_offer = normalize_outcome(offer)
        for issue, value in normalized_offer.items():
            value_counts[f"{issue}_{value}"] += 1
            issue_patterns[issue].append(value)
    
    # Analyze trends
    analysis = {
        'total_offers': len(offers),
        'value_frequencies': dict(value_counts),
        'issue_patterns': dict(issue_patterns),
        'pattern_detected': len(value_counts) > 0
    }
    
    # Detect most common patterns
    if value_counts:
        most_common = max(value_counts.items(), key=lambda x: x[1])
        analysis['most_common_pattern'] = most_common[0]
        analysis['most_common_frequency'] = most_common[1]
    
    return analysis

def benchmark_performance(agent_stats: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Benchmark agent performance against multiple metrics
    
    Args:
        agent_stats: List of performance statistics from multiple negotiations
    
    Returns:
        Comprehensive benchmark results
    """
    if not agent_stats:
        return {'error': 'No statistics provided'}
    
    # Extract metrics
    success_rates = [stats.get('success_rate', 0) for stats in agent_stats]
    average_utilities = [stats.get('average_utility', 0) for stats in agent_stats]
    total_negotiations = [stats.get('total_negotiations', 0) for stats in agent_stats]
    
    benchmark = {
        'performance_summary': {
            'success_rate': calculate_statistics(success_rates),
            'average_utility': calculate_statistics(average_utilities),
            'total_negotiations': calculate_statistics(total_negotiations)
        },
        'overall_assessment': 'Good' if np.mean(success_rates) > 0.7 else 'Needs Improvement',
        'recommendations': []
    }
    
    # Generate recommendations
    mean_success_rate = np.mean(success_rates)
    mean_utility = np.mean(average_utilities)
    
    if mean_success_rate < 0.5:
        benchmark['recommendations'].append("Consider more aggressive acceptance criteria")
    
    if mean_utility < 0.6:
        benchmark['recommendations'].append("Improve bidding strategy to target higher utilities")
    
    if np.std(success_rates) > 0.2:
        benchmark['recommendations'].append("Strategy consistency needs improvement")
    
    return benchmark

class NegotiationTimer:
    """
    Timer utility for measuring negotiation performance
    """
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.checkpoints = []
    
    def start(self):
        """Start the timer"""
        self.start_time = time.time()
        self.checkpoints = []
    
    def checkpoint(self, label: str):
        """Add a checkpoint with label"""
        if self.start_time is None:
            return
        
        current_time = time.time()
        elapsed = current_time - self.start_time
        self.checkpoints.append({
            'label': label,
            'time': current_time,
            'elapsed': elapsed
        })
    
    def stop(self):
        """Stop the timer"""
        self.end_time = time.time()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get timer summary"""
        if self.start_time is None:
            return {'error': 'Timer not started'}
        
        end_time = self.end_time or time.time()
        total_elapsed = end_time - self.start_time
        
        return {
            'total_time': total_elapsed,
            'checkpoints': self.checkpoints,
            'average_time_per_checkpoint': total_elapsed / len(self.checkpoints) if self.checkpoints else 0
        }