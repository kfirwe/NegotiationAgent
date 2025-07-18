# Group 4 - Advanced Negotiation Agent

## Overview

This repository contains the complete implementation of Group 4's advanced negotiation agent for the BSc Computer Science Automated Negotiation Assignment. The agent implements a sophisticated BOA (Bidding, Opponent modeling, Acceptance) framework with adaptive strategies, comprehensive opponent modeling, and extensive performance analysis.

## 🎯 Assignment Completion Status: **100% COMPLETE**

### ✅ All Required Sections Implemented:

1. **Domain Analysis** - Holiday scenario analysis with Nash Point computation
2. **Agent Implementation** - Full BOA framework with adaptive strategies
3. **ANL Agent Testing** - Testing against standard competitor agents
4. **Nash/Pareto Analysis** - Comprehensive outcome quality assessment
5. **Performance Documentation** - Detailed analysis and reporting

## 🏆 Key Performance Metrics

- **Agreement Rate**: 100% (excellent negotiation success)
- **Average Utility**: 0.73-0.83 (highly competitive)
- **Negotiation Efficiency**: 0.867 (fast agreement reaching)
- **Social Welfare**: 0.750 (balanced outcomes)
- **ANL Testing**: 100% agreement rate vs all competitor types

## Features

- **Adaptive Bidding Strategy**: Hybrid Boulware/Conceder approach that adjusts based on time pressure
- **Intelligent Opponent Modeling**: Learns opponent preferences and estimates reservation values
- **Multi-criteria Acceptance**: 5-factor acceptance strategy with dynamic thresholds
- **Tournament Optimization**: Designed for competitive tournament performance
- **Comprehensive Testing**: Full test suite with benchmarking and performance analysis
- **Domain Analysis**: Complete holiday scenario analysis with Nash/Pareto computations
- **ANL Compatibility**: Tested against standard ANL competitor agents

## Directory Structure

```
group4/
├── group4.py                        # Main agent implementation
├── __init__.py                      # Package initialization
├── domain_analysis.py               # Holiday scenario analysis (Section 1)
├── anl_agent_tests.py              # ANL competitor testing (Section 4a/4b)
├── nash_pareto_analysis.py         # Nash/Pareto analysis (Section 4c)
├── run_tests.py                     # Main testing script
├── ASSIGNMENT_COMPLETION_SUMMARY.md # Complete assignment status
├── helpers/                         # Utility functions and testing
│   ├── __init__.py
│   ├── runner.py                    # Testing and simulation utilities
│   ├── utils.py                     # Utility functions (logging, statistics)
├── report/
│   └── Group4 final report.pdf
├── README.md                        # This file
└── Generated Files/
    ├── holiday_analysis_report.txt
    ├── anl_test_report.txt
    ├── nash_pareto_analysis_report.txt
    └── Various .png visualization files
```

## Installation

1. Clone or download this repository
2. Ensure you have Python 3.7+ installed
3. Install required dependencies:

```bash
pip install negmas numpy
```

## Usage

### Quick Start - Run All Tests

```python
# Run the complete test suite
python run_tests.py
```

### Domain Analysis (Assignment Section 1)

```python
# Run holiday scenario analysis
python domain_analysis.py
```

### ANL Agent Testing (Assignment Section 4a/4b)

```python
# Test against standard ANL competitor agents
python anl_agent_tests.py
```

### Nash/Pareto Analysis (Assignment Section 4c)

```python
# Run comprehensive Nash/Pareto analysis
python nash_pareto_analysis.py
```

### Basic Agent Usage

```python
from group4 import Group4

# Create a negotiator instance
negotiator = Group4(name="MyGroup4Agent")

# The agent will be used within the NegMAS framework
# for automated negotiations
```

### Advanced Testing

```python
from group4.helpers import create_test_negotiator, simulate_negotiation

# Create a test negotiator
agent = create_test_negotiator(name="TestAgent")

# Run a simple simulation
results = simulate_negotiation(agent, rounds=20, verbose=True)
print(f"Simulation results: {results}")
```

### Comprehensive Testing

```python
from group4.helpers import run_comprehensive_test

# Run full test suite
results = run_comprehensive_test(verbose=True)
print(f"Overall assessment: {results['overall_assessment']}")
```

### Tournament Simulation

```python
from group4.helpers import run_tournament_simulation

# Run tournament with multiple agents
tournament_results = run_tournament_simulation(
    num_agents=5,
    num_rounds=20,
    verbose=True
)
```

## Assignment Analysis Results

### Domain Analysis (Section 1)

- **Nash Point**: (Barcelona, 2 weeks, Hostel) with Nash Product = 0.1000
- **Pareto Frontier**: 4 Pareto optimal outcomes identified
- **Conflict Level**: Medium (correlation = -0.2318)
- **Frequency Analysis**: Successfully estimated opponent weights

### ANL Agent Testing (Section 4a/4b)

- **Overall Performance**: 100% agreement rate across all competitor types
- **Best vs**: Random agents (1.000 average utility)
- **Worst vs**: Boulware agents (0.595 average utility)
- **Average Pareto Efficiency**: 0.743

### Nash/Pareto Analysis (Section 4c)

- **Agreement Rate**: 100% (20/20 negotiations)
- **Average Social Welfare**: 0.750
- **Negotiation Efficiency**: 0.867
- **Outcome Quality**: Consistently "Fair - Close to Nash solution"

## Strategy Overview

### Bidding Strategy

- **Adaptive Concession**: Starts with Boulware strategy (slow concession) and switches to Conceder strategy (faster concession) under time pressure
- **Target Utility Calculation**: Dynamically calculates target utility based on time and negotiation context
- **Candidate Generation**: Generates multiple candidate offers and selects best based on utility and novelty

### Opponent Modeling

- **Preference Learning**: Tracks opponent offer patterns to learn their preferences
- **Reservation Value Estimation**: Continuously updates estimates of opponent's reservation value
- **Concession Rate Tracking**: Monitors opponent's concession patterns for strategic adaptation

### Acceptance Strategy

- **Multi-criteria Decision**: Uses 5 different criteria for acceptance decisions
- **Dynamic Thresholds**: Adjusts acceptance thresholds based on time pressure and negotiation context
- **Strategic Timing**: Balances between getting good deals and ensuring agreements are reached
- **Reservation Estimation**: Estimates opponent's reservation value from their bidding behavior
- **Concession Rate Tracking**: Monitors opponent's concession rate to predict future behavior

### Acceptance Strategy

- **Multi-criteria Decision**: Considers multiple factors including offer utility, time pressure, and opponent behavior
- **Dynamic Thresholds**: Adjusts acceptance thresholds based on negotiation progress
- **Trend Analysis**: Analyzes opponent offer trends to make informed acceptance decisions

## Configuration

The agent can be configured through various parameters:

```python
# Example configuration
negotiator = Group4(
    name="ConfiguredAgent",
    # Strategy parameters are set internally
    # but can be modified after initialization
)

# Modify strategy parameters
negotiator.concession_factor = 0.3  # Faster concession
negotiator.time_pressure_threshold = 0.85  # Earlier time pressure activation
negotiator.exploration_rate = 0.15  # More exploration
```

## Performance Monitoring

The agent includes comprehensive performance monitoring:

```python
# Get performance statistics
stats = negotiator.get_performance_stats()
print(f"Success rate: {stats['success_rate']}")
print(f"Average utility: {stats['average_utility']}")
print(f"Total negotiations: {stats['total_negotiations']}")
```

## Testing

### Unit Testing

```python
from group4.helpers import create_test_negotiator

# Create and test basic functionality
agent = create_test_negotiator()
assert agent.name == "TestGroup4"
assert agent.reservation_value >= 0
```

### Integration Testing

```python
from group4.helpers import run_comprehensive_test

# Run full integration test
results = run_comprehensive_test(
    include_tournament=True,
    include_benchmark=True,
    verbose=True
)
```

### Benchmark Testing

```python
from group4.helpers import create_test_scenarios, benchmark_agent_performance

# Create test scenarios
scenarios = create_test_scenarios()

# Benchmark performance
agent = create_test_negotiator()
benchmark_results = benchmark_agent_performance(agent, scenarios)
```

## Logging and Debugging

Enable detailed logging for debugging:

```python
from group4.helpers import setup_logging

# Setup logging
logger = setup_logging(log_level="DEBUG", log_file="negotiation.log")

# The agent will now log detailed information about its decisions
```

## Files Description

- **`group4.py`**: Main negotiator implementation with all core strategies
- **`helpers/runner.py`**: Testing, simulation, and benchmarking utilities
- **`helpers/utils.py`**: Utility functions for logging, statistics, and data processing
- **`__init__.py`**: Package initialization files

## Requirements

- Python 3.7+
- negmas (NegMAS framework)
- numpy (numerical computations)
- Standard library modules: logging, json, time, collections, typing

## Development Notes

- The agent is designed to be tournament-competitive while maintaining good performance across various scenarios
- All strategies are based on established negotiation research and best practices
- The code includes comprehensive error handling and fallback mechanisms
- Performance is optimized for real-time negotiation scenarios

## License

This code is developed for academic purposes as part of the BSc Computer Science Automated Negotiation Assignment.

## Authors

Group 4 - BSc Computer Science

## Contact

For questions or issues, please contact the development team through the course communication channels.

<!-- # Group 4 - Advanced Party Planning Negotiator

## Overview

This repository contains the implementation of Group 4's advanced party planning negotiator for the BSc Computer Science Automated Negotiation Assignment. The agent implements an enhanced BOA (Bidding, Opponent modeling, Acceptance) framework with adaptive strategies and intelligent opponent modeling.

## Features

- **Adaptive Bidding Strategy**: Hybrid Boulware/Conceder approach that adjusts based on time pressure
- **Bayesian Opponent Modeling**: Learns opponent preferences and estimates reservation values
- **Multi-criteria Acceptance**: Intelligent acceptance decisions based on multiple factors
- **Tournament Optimization**: Designed for competitive tournament performance
- **Comprehensive Testing**: Full test suite with benchmarking and performance analysis

## Directory Structure

```
group4/
├── group4.py              # Main agent implementation
├── __init__.py            # Package initialization
├── helpers/               # Utility functions and testing
│   ├── __init__.py
│   ├── runner.py          # Testing and simulation utilities
│   ├── utils.py           # Utility functions (logging, statistics)
├── report/
│   └── Group4 final report.pdf
├── README.md              # This file
```

## Installation

1. Clone or download this repository
2. Ensure you have Python 3.7+ installed
3. Install required dependencies:

```bash
pip install negmas numpy
```

## Usage

### Basic Usage

```python
from group4 import Group4

# Create a negotiator instance
negotiator = Group4(name="MyGroup4Agent")

# The agent will be used within the NegMAS framework
# for automated negotiations
```

### Testing and Development

```python
from group4.helpers import create_test_negotiator, simulate_negotiation

# Create a test negotiator
agent = create_test_negotiator(name="TestAgent")

# Run a simple simulation
results = simulate_negotiation(agent, rounds=20, verbose=True)
print(f"Simulation results: {results}")
```

### Comprehensive Testing

```python
from group4.helpers import run_comprehensive_test

# Run full test suite
results = run_comprehensive_test(verbose=True)
print(f"Overall assessment: {results['overall_assessment']}")
```

### Tournament Simulation

```python
from group4.helpers import run_tournament_simulation

# Run tournament with multiple agents
tournament_results = run_tournament_simulation(
    num_agents=5,
    num_rounds=20,
    verbose=True
)
```

## Strategy Overview

### Bidding Strategy

- **Hybrid Concession**: Starts with Boulware strategy (slow concession) and switches to Conceder strategy (faster concession) under time pressure
- **Adaptive Target Utility**: Dynamically calculates target utility based on time and negotiation context
- **Pareto-Optimal Generation**: Generates candidate offers that balance own utility with estimated opponent utility

### Opponent Modeling

- **Preference Learning**: Tracks opponent offer patterns to learn their preferences
- **Reservation Estimation**: Estimates opponent's reservation value from their bidding behavior
- **Concession Rate Tracking**: Monitors opponent's concession rate to predict future behavior

### Acceptance Strategy

- **Multi-criteria Decision**: Considers multiple factors including offer utility, time pressure, and opponent behavior
- **Dynamic Thresholds**: Adjusts acceptance thresholds based on negotiation progress
- **Trend Analysis**: Analyzes opponent offer trends to make informed acceptance decisions

## Configuration

The agent can be configured through various parameters:

```python
# Example configuration
negotiator = Group4(
    name="ConfiguredAgent",
    # Strategy parameters are set internally
    # but can be modified after initialization
)

# Modify strategy parameters
negotiator.concession_factor = 0.3  # Faster concession
negotiator.time_pressure_threshold = 0.85  # Earlier time pressure activation
negotiator.exploration_rate = 0.15  # More exploration
```

## Performance Monitoring

The agent includes comprehensive performance monitoring:

```python
# Get performance statistics
stats = negotiator.get_performance_stats()
print(f"Success rate: {stats['success_rate']}")
print(f"Average utility: {stats['average_utility']}")
print(f"Total negotiations: {stats['total_negotiations']}")
```

## Testing

### Unit Testing

```python
from group4.helpers import create_test_negotiator

# Create and test basic functionality
agent = create_test_negotiator()
assert agent.name == "TestGroup4"
assert agent.reservation_value >= 0
```

### Integration Testing

```python
from group4.helpers import run_comprehensive_test

# Run full integration test
results = run_comprehensive_test(
    include_tournament=True,
    include_benchmark=True,
    verbose=True
)
```

### Benchmark Testing

```python
from group4.helpers import create_test_scenarios, benchmark_agent_performance

# Create test scenarios
scenarios = create_test_scenarios()

# Benchmark performance
agent = create_test_negotiator()
benchmark_results = benchmark_agent_performance(agent, scenarios)
```

## Logging and Debugging

Enable detailed logging for debugging:

```python
from group4.helpers import setup_logging

# Setup logging
logger = setup_logging(log_level="DEBUG", log_file="negotiation.log")

# The agent will now log detailed information about its decisions
```

## Files Description

- **`group4.py`**: Main negotiator implementation with all core strategies
- **`helpers/runner.py`**: Testing, simulation, and benchmarking utilities
- **`helpers/utils.py`**: Utility functions for logging, statistics, and data processing
- **`__init__.py`**: Package initialization files

## Requirements

- Python 3.7+
- negmas (NegMAS framework)
- numpy (numerical computations)
- Standard library modules: logging, json, time, collections, typing

## Development Notes

- The agent is designed to be tournament-competitive while maintaining good performance across various scenarios
- All strategies are based on established negotiation research and best practices
- The code includes comprehensive error handling and fallback mechanisms
- Performance is optimized for real-time negotiation scenarios

## License

This code is developed for academic purposes as part of the BSc Computer Science Automated Negotiation Assignment.

## Authors

Group 4 - BSc Computer Science

## Contact

For questions or issues, please contact the development team through the course communication channels. -->
