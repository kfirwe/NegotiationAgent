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