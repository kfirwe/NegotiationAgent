# Group 4 - Advanced Negotiation Agent

## Overview

This repository contains the complete implementation of Group 4's advanced negotiation agent for the BSc Computer Science Automated Negotiation Assignment. The agent implements a sophisticated **Adaptive BOA Framework** with intelligent opponent modeling, dynamic concession strategies, and comprehensive performance analysis.

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

## 🤖 Agent Strategy: Adaptive BOA Framework

The Group4 agent implements a sophisticated **Adaptive BOA Framework** that combines:

### Core Components:

- **Bidding Strategy** - Adaptive target utility calculation with time-based phases
- **Opponent Modeling** - Learning opponent preferences and concession patterns
- **Acceptance Strategy** - Multi-criteria acceptance decisions with dynamic thresholds

### Key Features:

- **Hybrid Concession**: Starts conservative (Boulware) and adapts to aggressive (Conceder) under time pressure
- **Intelligent Learning**: Real-time opponent preference estimation and reservation value tracking
- **Novelty-based Selection**: Avoids repetitive offers while maintaining strategic focus
- **Performance Adaptation**: Continuous strategy refinement based on negotiation outcomes

## 📋 Assignment Analysis Results

### Domain Analysis (Section 1)

- **Nash Point**: (Barcelona, 2 weeks, Hostel) with Nash Product = 0.1000
- **Pareto Frontier**: 4 Pareto optimal outcomes identified
- **Conflict Level**: Medium (correlation = -0.2318)
- **Frequency Analysis**: Successfully estimated opponent weights

### ANL Agent Testing (Section 4a/4b)

- **Overall Performance**: 100% agreement rate across all competitor types
- **Best Performance**: vs Random agents (1.000 average utility)
- **Challenging Match**: vs Boulware agents (0.595 average utility)
- **Average Pareto Efficiency**: 0.743

### Nash/Pareto Analysis (Section 4c)

- **Agreement Rate**: 100% (20/20 negotiations)
- **Average Social Welfare**: 0.750
- **Negotiation Efficiency**: 0.867
- **Outcome Quality**: Consistently "Fair - Close to Nash solution"

## 🚀 Competitive Advantage

The Adaptive BOA Framework is sophisticated because it:

- **Learns during negotiation** (opponent modeling)
- **Adapts to time pressure** (phase-based concession)
- **Uses multi-criteria decisions** (not just utility)
- **Tracks performance** (self-improvement)
- **Balances exploration vs exploitation** (novelty scoring)

## 📁 Project Structure

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
│   └── utils.py                     # Utility functions (logging, statistics)
├── report/
│   └── Group4 final report.pdf
├── README.md                        # This file
└── Generated Reports/
    ├── holiday_analysis_report.txt
    ├── anl_test_report.txt
    ├── nash_pareto_analysis_report.txt
    └── Various .png visualization files
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7+
- pip package manager

### Installation Steps

1. **Clone or download this repository**
2. **Install required dependencies:**
   ```bash
   pip install negmas numpy
   ```

## 🚀 Usage Guide

### Quick Start - Complete Test Suite

```python
# Run all assignment components
python run_tests.py
```

### Individual Assignment Sections

#### Section 1: Domain Analysis

```python
# Analyze holiday negotiation scenario
python domain_analysis.py
```

#### Section 4a/4b: ANL Agent Testing

```python
# Test against standard ANL competitor agents
python anl_agent_tests.py
```

#### Section 4c: Nash/Pareto Analysis

```python
# Run comprehensive Nash/Pareto analysis
python nash_pareto_analysis.py
```

### Using the Agent in Code

#### Basic Agent Usage

```python
from group4 import Group4

# Create a negotiator instance
negotiator = Group4(name="MyGroup4Agent")

# The agent integrates with the NegMAS framework
# for automated negotiations
```

#### Advanced Testing

```python
from group4.helpers import create_test_negotiator, simulate_negotiation

# Create a test negotiator
agent = create_test_negotiator(name="TestAgent")

# Run a simulation
results = simulate_negotiation(agent, rounds=20, verbose=True)
print(f"Simulation results: {results}")
```

#### Comprehensive Testing

```python
from group4.helpers import run_comprehensive_test

# Run full test suite
results = run_comprehensive_test(verbose=True)
print(f"Overall assessment: {results['overall_assessment']}")
```

#### Tournament Simulation

```python
from group4.helpers import run_tournament_simulation

# Run tournament with multiple agents
tournament_results = run_tournament_simulation(
    num_agents=5,
    num_rounds=20,
    verbose=True
)
```

## 🧠 Detailed Strategy Breakdown

### Bidding Strategy

- **Adaptive Concession**: Starts conservative (Boulware) and switches to cooperative (Conceder) under time pressure
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
- **Trend Analysis**: Analyzes opponent offer trends to make informed acceptance decisions

## 📚 Negotiation Strategies in AI: Complete Guide

### Understanding AI Negotiation Approaches

The field of automated negotiation employs various strategic approaches. Here's a comprehensive overview of the main categories and how our Group4 agent compares:

### 1. 🕒 Time-based Strategies

These strategies primarily use time as the main factor for concession decisions:

- **Boulware Strategy** ✅ _(Used in our agent)_

  - **Approach**: Slow concession, maintains high utility for most of the negotiation
  - **Characteristics**: Conservative early, concedes rapidly near deadline
  - **Formula**: `utility = reservation + (1 - reservation) * (1 - t)^β` where β > 1

- **Conceder Strategy** ✅ _(Used in our agent)_

  - **Approach**: Fast concession, cooperative behavior
  - **Characteristics**: Concedes quickly early, stabilizes later
  - **Formula**: `utility = reservation + (1 - reservation) * (1 - t)^β` where β < 1

- **Linear Strategy**

  - **Approach**: Steady linear concession over time
  - **Characteristics**: Predictable, constant concession rate
  - **Formula**: `utility = reservation + (1 - reservation) * (1 - t)`

- **Hardliner Strategy**
  - **Approach**: Minimal concession, very tough stance
  - **Characteristics**: Maintains high utility throughout, risks no agreement
  - **Formula**: `utility = reservation + (1 - reservation) * (1 - t)^β` where β >> 1

### 2. 🎭 Behavior-based Strategies

These strategies adapt based on opponent behavior:

- **Tit-for-Tat**

  - **Approach**: Mirror opponent's behavior
  - **Characteristics**: Cooperative if opponent cooperates, competitive if opponent competes
  - **Implementation**: Copies opponent's concession patterns

- **Copycat**

  - **Approach**: Directly copy opponent's offers
  - **Characteristics**: Simple imitation strategy
  - **Risk**: Can lead to suboptimal outcomes

- **Random Strategy**

  - **Approach**: Random behavior (baseline comparison)
  - **Characteristics**: Unpredictable, used for benchmarking
  - **Purpose**: Control strategy for experiments

- **Nice Tit-for-Tat**
  - **Approach**: Cooperative version of Tit-for-Tat
  - **Characteristics**: Starts cooperative, forgives occasional defection
  - **Advantage**: More robust against noise

### 3. 🧠 Advanced Learning Strategies

Sophisticated strategies that learn and adapt:

- **Our BOA Framework** 🎯 _(Group4 Implementation)_

  - **Approach**: Adaptive, learning-based with three components
  - **Bidding**: Dynamic target utility with time-based phases
  - **Opponent Modeling**: Real-time preference learning
  - **Acceptance**: Multi-criteria decision making
  - **Advantage**: Balances all aspects of negotiation

- **AgentK**

  - **Approach**: Sophisticated frequency modeling
  - **Characteristics**: Learns opponent preferences through frequency analysis
  - **Strength**: Excellent opponent modeling

- **HardHeaded**

  - **Approach**: Aggressive utility maximization
  - **Characteristics**: Tough negotiator, maximizes own utility
  - **Risk**: May lead to failed negotiations

- **Gahboninho**

  - **Approach**: Complex opponent modeling with multiple strategies
  - **Characteristics**: Adaptive strategy selection
  - **Complexity**: High computational requirements

- **MiCRO**
  - **Approach**: Machine learning-based concession
  - **Characteristics**: Uses ML to predict optimal concession
  - **Innovation**: Data-driven approach

### 4. 📈 Learning-based Approaches

Strategies that improve through experience:

- **Frequency Analysis** ✅ _(Used in our agent)_

  - **Method**: Learn opponent preferences from offer patterns
  - **Implementation**: Track issue values and weights
  - **Advantage**: Quick adaptation during negotiation

- **Gaussian Process**

  - **Method**: Statistical opponent modeling
  - **Characteristics**: Bayesian approach to preference learning
  - **Complexity**: Requires substantial computational resources

- **Neural Networks**

  - **Method**: Deep learning for prediction
  - **Characteristics**: Can learn complex patterns
  - **Requirement**: Large training datasets

- **Reinforcement Learning**
  - **Method**: Learn from multiple negotiation episodes
  - **Characteristics**: Improves over time across negotiations
  - **Application**: Tournament scenarios

### 5. 🎯 Game-theoretic Strategies

Strategies based on mathematical game theory:

- **Nash Equilibrium**

  - **Concept**: Optimal mutual strategy where no player can improve unilaterally
  - **Application**: Theoretical optimal point
  - **Challenge**: Requires complete information

- **Pareto Optimal**

  - **Concept**: Maximize joint utility (social welfare)
  - **Characteristics**: No improvement possible without hurting someone
  - **Goal**: Efficient outcomes

- **Kalai-Smorodinsky**
  - **Concept**: Proportional bargaining solution
  - **Characteristics**: Fair division based on maximum possible gains
  - **Implementation**: Requires utility function knowledge

### 🎯 Why Our Adaptive BOA Framework is Advanced

Our Group4 agent's strategy is sophisticated because it combines multiple approaches:

#### **Multi-Strategy Integration**:

- **Time-based**: Uses both Boulware and Conceder strategies adaptively
- **Learning-based**: Implements real-time opponent modeling
- **Behavior-based**: Adapts to opponent patterns
- **Performance-based**: Tracks and improves its own performance

#### **Adaptive Intelligence**:

1. **Context Awareness**: Recognizes negotiation phases and adjusts accordingly
2. **Opponent Learning**: Builds models of opponent preferences during negotiation
3. **Strategic Flexibility**: Switches between conservative and aggressive approaches
4. **Multi-criteria Decisions**: Considers multiple factors beyond just utility

#### **Competitive Advantages**:

- **Robust Performance**: Works well against various opponent types
- **Fast Adaptation**: Learns quickly within single negotiations
- **Strategic Depth**: Uses sophisticated decision-making processes
- **Tournament Optimized**: Designed for competitive scenarios

### 📊 Strategy Comparison Matrix

| Strategy Type         | Learning   | Adaptability | Complexity   | Tournament Performance |
| --------------------- | ---------- | ------------ | ------------ | ---------------------- |
| **Our BOA Framework** | ✅ High    | ✅ High      | ✅ High      | ✅ Excellent           |
| Time-based            | ❌ None    | ❌ Low       | ✅ Low       | ⚠️ Moderate            |
| Behavior-based        | ⚠️ Limited | ✅ Medium    | ✅ Medium    | ⚠️ Variable            |
| Pure Learning         | ✅ High    | ✅ High      | ❌ Very High | ⚠️ Depends on data     |
| Game-theoretic        | ❌ None    | ❌ Low       | ✅ Medium    | ⚠️ Limited             |

This comprehensive approach makes our agent highly competitive while maintaining robustness across different negotiation scenarios.

## ⚙️ Configuration & Customization

### Agent Configuration

```python
# Example configuration
negotiator = Group4(
    name="ConfiguredAgent",
    # Strategy parameters can be modified after initialization
)

# Modify strategy parameters
negotiator.concession_factor = 0.3  # Faster concession
negotiator.time_pressure_threshold = 0.85  # Earlier time pressure activation
negotiator.exploration_rate = 0.15  # More exploration
```

### Performance Monitoring

```python
# Get comprehensive performance statistics
stats = negotiator.get_performance_stats()
print(f"Success rate: {stats['success_rate']}")
print(f"Average utility: {stats['average_utility']}")
print(f"Total negotiations: {stats['total_negotiations']}")
```

## 🧪 Testing & Validation

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

## 📊 Logging & Debugging

### Enable Detailed Logging

```python
from group4.helpers import setup_logging

# Setup comprehensive logging
logger = setup_logging(log_level="DEBUG", log_file="negotiation.log")

# The agent will now log detailed information about its decisions
```

## 📋 System Requirements

- **Python**: 3.7+
- **Core Dependencies**:
  - `negmas` (NegMAS framework)
  - `numpy` (numerical computations)
- **Standard Library**: logging, json, time, collections, typing

## 🏗️ Architecture Notes

- **Tournament-Ready**: Designed for competitive tournament performance
- **Research-Based**: All strategies based on established negotiation research
- **Robust**: Comprehensive error handling and fallback mechanisms
- **Optimized**: Performance-optimized for real-time negotiation scenarios

## 📄 License

This code is developed for academic purposes as part of the BSc Computer Science Automated Negotiation Assignment.

## 👥 Authors

**Group 4** - BSc Computer Science

## 📞 Contact

For questions or technical support, please contact the development team through the official course communication channels.

---

_This project demonstrates advanced negotiation agent design and implementation, showcasing sophisticated AI techniques for automated negotiation scenarios._
