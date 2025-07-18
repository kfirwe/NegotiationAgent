"""
Runner and testing utilities for Group 4 negotiation agent
"""

import random
import time
from negmas.sao import ResponseType
from typing import Dict, List, Any, Optional
from group4 import Group4
from .utils import setup_logging, calculate_statistics, NegotiationTimer

def create_test_negotiator(**kwargs) -> Group4:
    """
    Factory function for creating test negotiators
    """
    # Set default parameters for testing
    default_params = {
        'name': kwargs.get('name', 'TestGroup4')
    }
    
    # Remove unsupported parameters
    unsupported_params = ['can_propose', 'can_accept', 'can_reject']
    for param in unsupported_params:
        kwargs.pop(param, None)
    
    # Merge with provided kwargs
    params = {**default_params, **kwargs}
    
    try:
        return Group4(**params)
    except Exception as e:
        print(f"Error creating negotiator: {e}")
        return Group4(name=params['name'])

def simulate_negotiation(
    negotiator: Optional[Group4] = None,
    rounds: int = 10,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Improved simulation with better negotiation modeling
    """
    if negotiator is None:
        negotiator = create_test_negotiator()
    
    if verbose:
        print(f"Starting negotiation simulation with {negotiator.name}")
    
    # Initialize timer
    timer = NegotiationTimer()
    timer.start()
    
    # Create more realistic mock utility function
    def create_mock_ufun():
        class MockUtilityFunction:
            def __init__(self):
                self.outcome_space = MockOutcomeSpace()
                self.weights = {
                    'venue': 0.3,
                    'food': 0.25,
                    'music': 0.25,
                    'drinks': 0.2
                }
                self.preferences = {
                    'venue': {'Hotel': 1.0, 'Restaurant': 0.7, 'Club': 0.4},
                    'food': {'Buffet': 0.6, 'Plated': 1.0, 'Cocktail': 0.8},
                    'music': {'DJ': 0.7, 'Band': 1.0, 'Playlist': 0.3},
                    'drinks': {'Premium': 1.0, 'Standard': 0.6, 'Basic': 0.2}
                }
            
            def __call__(self, outcome):
                if isinstance(outcome, dict):
                    utility = 0.0
                    for issue, value in outcome.items():
                        if issue in self.weights and issue in self.preferences:
                            pref_value = self.preferences[issue].get(value, 0.5)
                            utility += self.weights[issue] * pref_value
                    return utility
                return 0.5
        
        return MockUtilityFunction()
    
    class MockOutcomeSpace:
        def random_outcome(self):
            return {
                'venue': random.choice(['Hotel', 'Restaurant', 'Club']),
                'food': random.choice(['Buffet', 'Plated', 'Cocktail']),
                'music': random.choice(['DJ', 'Band', 'Playlist']),
                'drinks': random.choice(['Premium', 'Standard', 'Basic'])
            }
    
    # Initialize negotiator with mock utility function
    mock_ufun = create_mock_ufun()
    negotiator.initialize(ufun=mock_ufun)
    
    # Create mock negotiation state
    class MockState:
        def __init__(self, round_num: int, max_rounds: int):
            self.step = round_num
            self.relative_time = round_num / max_rounds
            self.agreement = None
            self.current_offer = None
    
    # Simulate negotiation rounds with offers and responses
    results = {
        'negotiator_name': negotiator.name,
        'total_rounds': rounds,
        'offers_made': [],
        'offers_received': [],
        'agreements_reached': 0,
        'final_stats': None,
        'simulation_time': 0
    }
    
    agreement_reached = False
    
    for round_num in range(rounds):
        if agreement_reached:
            break
            
        state = MockState(round_num, rounds)
        
        # Agent makes proposal
        try:
            offer = negotiator.propose(state)
            if offer:
                results['offers_made'].append(offer)
                
                # Simulate opponent response
                opponent_offer = mock_ufun.outcome_space.random_outcome()
                results['offers_received'].append(opponent_offer)
                
                # Check if agent accepts opponent offer
                state.current_offer = opponent_offer
                response = negotiator.respond(state)
                
                if response == ResponseType.ACCEPT_OFFER:
                    results['agreements_reached'] += 1
                    agreement_reached = True
                    if verbose:
                        print(f"Agreement reached in round {round_num}!")
                
        except Exception as e:
            if verbose:
                print(f"Error in round {round_num}: {e}")
            break
        
        timer.checkpoint(f"Round {round_num}")
        
        if verbose and round_num % 5 == 0:
            print(f"Completed round {round_num}")
    
    timer.stop()
    
    # Get final statistics
    results['final_stats'] = negotiator.get_performance_stats()
    results['simulation_time'] = timer.get_summary()['total_time']
    
    if verbose:
        print(f"Simulation completed in {results['simulation_time']:.2f} seconds")
        print(f"Final stats: {results['final_stats']}")
    
    return results

def run_tournament_simulation(
    num_agents: int = 5,
    num_rounds: int = 20,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Run a tournament simulation with multiple agents
    
    Args:
        num_agents: Number of agents to create
        num_rounds: Number of rounds per negotiation
        verbose: Whether to print progress
    
    Returns:
        Tournament results
    """
    if verbose:
        print(f"Starting tournament with {num_agents} agents, {num_rounds} rounds each")
    
    agents = []
    agent_results = []
    
    # Create agents
    for i in range(num_agents):
        agent = create_test_negotiator(name=f"Group4_Agent_{i}")
        agents.append(agent)
    
    # Run simulations for each agent
    for i, agent in enumerate(agents):
        if verbose:
            print(f"Running simulation for Agent {i}")
        
        result = simulate_negotiation(agent, num_rounds, verbose=False)
        agent_results.append(result)
    
    # Calculate tournament statistics
    tournament_stats = analyze_tournament_results(agent_results)
    
    if verbose:
        print(f"Tournament completed. Results: {tournament_stats['summary']}")
    
    return {
        'tournament_config': {
            'num_agents': num_agents,
            'num_rounds': num_rounds
        },
        'agent_results': agent_results,
        'tournament_stats': tournament_stats
    }

def analyze_tournament_results(agent_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze results from a tournament simulation
    
    Args:
        agent_results: List of agent simulation results
    
    Returns:
        Tournament analysis
    """
    if not agent_results:
        return {'error': 'No results to analyze'}
    
    # Extract metrics
    simulation_times = [r['simulation_time'] for r in agent_results]
    success_rates = [r['final_stats']['success_rate'] for r in agent_results]
    avg_utilities = [r['final_stats']['average_utility'] for r in agent_results]
    
    # Calculate statistics
    analysis = {
        'summary': {
            'total_agents': len(agent_results),
            'avg_simulation_time': sum(simulation_times) / len(simulation_times),
            'avg_success_rate': sum(success_rates) / len(success_rates),
            'avg_utility': sum(avg_utilities) / len(avg_utilities)
        },
        'detailed_stats': {
            'simulation_times': calculate_statistics(simulation_times),
            'success_rates': calculate_statistics(success_rates),
            'utilities': calculate_statistics(avg_utilities)
        },
        'rankings': {
            'by_success_rate': sorted(
                [(r['negotiator_name'], r['final_stats']['success_rate']) 
                 for r in agent_results],
                key=lambda x: x[1], reverse=True
            ),
            'by_utility': sorted(
                [(r['negotiator_name'], r['final_stats']['average_utility']) 
                 for r in agent_results],
                key=lambda x: x[1], reverse=True
            )
        }
    }
    
    return analysis

def benchmark_agent_performance(
    agent: Group4,
    test_scenarios: List[Dict[str, Any]],
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Benchmark agent performance across different scenarios
    
    Args:
        agent: Group4 negotiator to benchmark
        test_scenarios: List of test scenario configurations
        verbose: Whether to print progress
    
    Returns:
        Benchmark results
    """
    if verbose:
        print(f"Benchmarking {agent.name} across {len(test_scenarios)} scenarios")
    
    scenario_results = []
    
    for i, scenario in enumerate(test_scenarios):
        if verbose:
            print(f"Running scenario {i+1}: {scenario.get('name', 'Unnamed')}")
        
        # Apply scenario configuration
        rounds = scenario.get('rounds', 10)
        
        # Run simulation
        result = simulate_negotiation(agent, rounds, verbose=False)
        result['scenario_config'] = scenario
        scenario_results.append(result)
    
    # Analyze performance across scenarios
    performance_analysis = {
        'agent_name': agent.name,
        'total_scenarios': len(test_scenarios),
        'scenario_results': scenario_results,
        'performance_summary': _analyze_scenario_performance(scenario_results)
    }
    
    if verbose:
        print(f"Benchmark completed. Overall performance: {performance_analysis['performance_summary']['overall_rating']}")
    
    return performance_analysis

def _analyze_scenario_performance(scenario_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze performance across different scenarios
    
    Args:
        scenario_results: List of scenario results
    
    Returns:
        Performance analysis
    """
    if not scenario_results:
        return {'error': 'No scenario results to analyze'}
    
    # Extract metrics
    success_rates = [r['final_stats']['success_rate'] for r in scenario_results]
    utilities = [r['final_stats']['average_utility'] for r in scenario_results]
    times = [r['simulation_time'] for r in scenario_results]
    
    # Calculate overall performance
    avg_success_rate = sum(success_rates) / len(success_rates)
    avg_utility = sum(utilities) / len(utilities)
    
    # Determine rating
    if avg_success_rate > 0.8 and avg_utility > 0.7:
        rating = "Excellent"
    elif avg_success_rate > 0.6 and avg_utility > 0.6:
        rating = "Good"
    elif avg_success_rate > 0.4 and avg_utility > 0.5:
        rating = "Fair"
    else:
        rating = "Poor"
    
    return {
        'overall_rating': rating,
        'avg_success_rate': avg_success_rate,
        'avg_utility': avg_utility,
        'avg_time': sum(times) / len(times),
        'consistency': {
            'success_rate_std': calculate_statistics(success_rates)['std'],
            'utility_std': calculate_statistics(utilities)['std']
        },
        'recommendations': _generate_recommendations(avg_success_rate, avg_utility)
    }

def _generate_recommendations(success_rate: float, utility: float) -> List[str]:
    """
    Generate performance improvement recommendations
    
    Args:
        success_rate: Average success rate
        utility: Average utility achieved
    
    Returns:
        List of recommendations
    """
    recommendations = []
    
    if success_rate < 0.5:
        recommendations.append("Consider more flexible acceptance criteria")
        recommendations.append("Improve opponent modeling for better offer evaluation")
    
    if utility < 0.6:
        recommendations.append("Enhance bidding strategy to target higher utilities")
        recommendations.append("Optimize concession strategy timing")
    
    if success_rate > 0.8 and utility < 0.6:
        recommendations.append("Balance between acceptance and utility - too eager to accept")
    
    if success_rate < 0.5 and utility > 0.7:
        recommendations.append("Too rigid in acceptance - missing good opportunities")
    
    if not recommendations:
        recommendations.append("Performance is well-balanced, consider fine-tuning for specific scenarios")
    
    return recommendations

def create_test_scenarios() -> List[Dict[str, Any]]:
    """
    Create a set of standard test scenarios for benchmarking
    
    Returns:
        List of test scenario configurations
    """
    scenarios = [
        {
            'name': 'Quick Negotiation',
            'rounds': 5,
            'description': 'Short negotiation with time pressure'
        },
        {
            'name': 'Standard Negotiation',
            'rounds': 15,
            'description': 'Normal length negotiation'
        },
        {
            'name': 'Extended Negotiation',
            'rounds': 30,
            'description': 'Long negotiation allowing for complex strategies'
        },
        {
            'name': 'High Pressure',
            'rounds': 8,
            'description': 'Medium length with high time pressure'
        },
        {
            'name': 'Exploration Phase',
            'rounds': 25,
            'description': 'Longer negotiation focusing on exploration'
        }
    ]
    
    return scenarios

def run_comprehensive_test(
    agent: Optional[Group4] = None,
    include_tournament: bool = True,
    include_benchmark: bool = True,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Run a comprehensive test suite for the Group4 agent
    
    Args:
        agent: Group4 agent to test (creates new if None)
        include_tournament: Whether to include tournament simulation
        include_benchmark: Whether to include scenario benchmarking
        verbose: Whether to print progress
    
    Returns:
        Comprehensive test results
    """
    if agent is None:
        agent = create_test_negotiator(name="Group4_Comprehensive_Test")
    
    if verbose:
        print(f"Starting comprehensive test for {agent.name}")
    
    results = {
        'agent_name': agent.name,
        'test_timestamp': time.time(),
        'basic_simulation': None,
        'tournament_results': None,
        'benchmark_results': None,
        'overall_assessment': None
    }
    
    # Basic simulation
    if verbose:
        print("Running basic simulation...")
    results['basic_simulation'] = simulate_negotiation(agent, verbose=False)
    
    # Tournament simulation
    if include_tournament:
        if verbose:
            print("Running tournament simulation...")
        results['tournament_results'] = run_tournament_simulation(
            num_agents=3, num_rounds=15, verbose=False
        )
    
    # Benchmark testing
    if include_benchmark:
        if verbose:
            print("Running benchmark tests...")
        test_scenarios = create_test_scenarios()
        results['benchmark_results'] = benchmark_agent_performance(
            agent, test_scenarios, verbose=False
        )
    
    # Overall assessment
    results['overall_assessment'] = _generate_overall_assessment(results)
    
    if verbose:
        print(f"Comprehensive test completed. Overall assessment: {results['overall_assessment']['rating']}")
    
    return results

def _generate_overall_assessment(test_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate overall assessment from comprehensive test results
    
    Args:
        test_results: Complete test results
    
    Returns:
        Overall assessment
    """
    assessment = {
        'rating': 'Unknown',
        'strengths': [],
        'weaknesses': [],
        'recommendations': []
    }
    
    # Analyze basic simulation
    if test_results.get('basic_simulation'):
        basic_stats = test_results['basic_simulation']['final_stats']
        if basic_stats['success_rate'] > 0.7:
            assessment['strengths'].append("Good basic negotiation success rate")
        else:
            assessment['weaknesses'].append("Low basic negotiation success rate")
    
    # Analyze benchmark results
    if test_results.get('benchmark_results'):
        benchmark_summary = test_results['benchmark_results']['performance_summary']
        if benchmark_summary['avg_success_rate'] > 0.6:
            assessment['strengths'].append("Consistent performance across scenarios")
        else:
            assessment['weaknesses'].append("Inconsistent performance across scenarios")
    
    # Determine overall rating
    strength_count = len(assessment['strengths'])
    weakness_count = len(assessment['weaknesses'])
    
    if strength_count > weakness_count:
        assessment['rating'] = "Good"
    elif strength_count == weakness_count:
        assessment['rating'] = "Fair"
    else:
        assessment['rating'] = "Needs Improvement"
    
    # Generate recommendations
    if weakness_count > 0:
        assessment['recommendations'].append("Focus on addressing identified weaknesses")
    
    if strength_count > 0:
        assessment['recommendations'].append("Leverage identified strengths in strategy refinement")
    
    return assessment

def negotiate_head_to_head(
    agent1: Group4,
    agent2: Group4,
    rounds: int = 20,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Run a real negotiation between two Group4 agents
    
    Args:
        agent1: First Group4 agent
        agent2: Second Group4 agent
        rounds: Maximum number of rounds
        verbose: Whether to print negotiation progress
    
    Returns:
        Negotiation results
    """
    if verbose:
        print(f"Starting head-to-head negotiation: {agent1.name} vs {agent2.name}")
    
    # Create different utility functions for each agent
    def create_agent_ufun(agent_preferences):
        class AgentUtilityFunction:
            def __init__(self, prefs):
                self.outcome_space = MockOutcomeSpace()
                self.weights = prefs['weights']
                self.preferences = prefs['preferences']
            
            def __call__(self, outcome):
                if isinstance(outcome, dict):
                    utility = 0.0
                    for issue, value in outcome.items():
                        if issue in self.weights and issue in self.preferences:
                            pref_value = self.preferences[issue].get(value, 0.5)
                            utility += self.weights[issue] * pref_value
                    return utility
                return 0.5
        
        return AgentUtilityFunction(agent_preferences)
    
    class MockOutcomeSpace:
        def random_outcome(self):
            return {
                'venue': random.choice(['Hotel', 'Restaurant', 'Club']),
                'food': random.choice(['Buffet', 'Plated', 'Cocktail']),
                'music': random.choice(['DJ', 'Band', 'Playlist']),
                'drinks': random.choice(['Premium', 'Standard', 'Basic'])
            }
    
    # Create different preferences for each agent
    agent1_prefs = {
        'weights': {'venue': 0.3, 'food': 0.25, 'music': 0.25, 'drinks': 0.2},
        'preferences': {
            'venue': {'Hotel': 1.0, 'Restaurant': 0.7, 'Club': 0.4},
            'food': {'Buffet': 0.6, 'Plated': 1.0, 'Cocktail': 0.8},
            'music': {'DJ': 0.7, 'Band': 1.0, 'Playlist': 0.3},
            'drinks': {'Premium': 1.0, 'Standard': 0.6, 'Basic': 0.2}
        }
    }
    
    agent2_prefs = {
        'weights': {'venue': 0.4, 'food': 0.2, 'music': 0.3, 'drinks': 0.1},
        'preferences': {
            'venue': {'Club': 1.0, 'Restaurant': 0.8, 'Hotel': 0.5},
            'food': {'Cocktail': 1.0, 'Buffet': 0.7, 'Plated': 0.6},
            'music': {'Playlist': 1.0, 'DJ': 0.8, 'Band': 0.4},
            'drinks': {'Basic': 1.0, 'Standard': 0.7, 'Premium': 0.3}
        }
    }
    
    # Initialize agents with different utility functions
    agent1_ufun = create_agent_ufun(agent1_prefs)
    agent2_ufun = create_agent_ufun(agent2_prefs)
    
    agent1.initialize(ufun=agent1_ufun)
    agent2.initialize(ufun=agent2_ufun)
    
    # Negotiation state
    class NegotiationState:
        def __init__(self, round_num: int, max_rounds: int):
            self.step = round_num
            self.relative_time = round_num / max_rounds
            self.current_offer = None
            self.agreement = None
    
    # Track negotiation
    negotiation_log = []
    agreement_reached = False
    final_offer = None
    final_round = 0
    
    # Main negotiation loop
    for round_num in range(rounds):
        if agreement_reached:
            break
            
        state = NegotiationState(round_num, rounds)
        
        # Agent 1 makes offer
        try:
            agent1_offer = agent1.propose(state)
            if agent1_offer:
                # Agent 2 responds to agent 1's offer
                state.current_offer = agent1_offer
                agent2_response = agent2.respond(state)
                
                agent1_utility = agent1_ufun(agent1_offer)
                agent2_utility = agent2_ufun(agent1_offer)
                
                negotiation_log.append({
                    'round': round_num,
                    'proposer': agent1.name,
                    'offer': agent1_offer,
                    'agent1_utility': agent1_utility,
                    'agent2_utility': agent2_utility,
                    'response': agent2_response
                })
                
                if verbose:
                    print(f"Round {round_num}: {agent1.name} offers {agent1_offer}")
                    print(f"  Utilities: {agent1.name}={agent1_utility:.3f}, {agent2.name}={agent2_utility:.3f}")
                    print(f"  {agent2.name} response: {agent2_response}")
                
                if agent2_response == ResponseType.ACCEPT_OFFER:
                    agreement_reached = True
                    final_offer = agent1_offer
                    final_round = round_num
                    if verbose:
                        print(f"  🎉 AGREEMENT REACHED! {agent2.name} accepts {agent1.name}'s offer")
                    break
        
        except Exception as e:
            if verbose:
                print(f"Error in round {round_num}: {e}")
            break
        
        # If no agreement, agent 2 makes counter-offer
        if not agreement_reached:
            try:
                agent2_offer = agent2.propose(state)
                if agent2_offer:
                    # Agent 1 responds to agent 2's offer
                    state.current_offer = agent2_offer
                    agent1_response = agent1.respond(state)
                    
                    agent1_utility = agent1_ufun(agent2_offer)
                    agent2_utility = agent2_ufun(agent2_offer)
                    
                    negotiation_log.append({
                        'round': round_num,
                        'proposer': agent2.name,
                        'offer': agent2_offer,
                        'agent1_utility': agent1_utility,
                        'agent2_utility': agent2_utility,
                        'response': agent1_response
                    })
                    
                    if verbose:
                        print(f"  {agent2.name} counters with {agent2_offer}")
                        print(f"  Utilities: {agent1.name}={agent1_utility:.3f}, {agent2.name}={agent2_utility:.3f}")
                        print(f"  {agent1.name} response: {agent1_response}")
                    
                    if agent1_response == ResponseType.ACCEPT_OFFER:
                        agreement_reached = True
                        final_offer = agent2_offer
                        final_round = round_num
                        if verbose:
                            print(f"  🎉 AGREEMENT REACHED! {agent1.name} accepts {agent2.name}'s offer")
                        break
            
            except Exception as e:
                if verbose:
                    print(f"Error in round {round_num}: {e}")
                break
    
    # Calculate final results
    if agreement_reached and final_offer:
        final_agent1_utility = agent1_ufun(final_offer)
        final_agent2_utility = agent2_ufun(final_offer)
        pareto_efficiency = (final_agent1_utility + final_agent2_utility) / 2.0
    else:
        final_agent1_utility = 0.0
        final_agent2_utility = 0.0
        pareto_efficiency = 0.0
        if verbose:
            print(f"  ❌ NO AGREEMENT REACHED after {rounds} rounds")
    
    return {
        'negotiation_type': 'head_to_head',
        'agent1_name': agent1.name,
        'agent2_name': agent2.name,
        'agreement_reached': agreement_reached,
        'final_offer': final_offer,
        'final_round': final_round,
        'total_rounds': rounds,
        'final_utilities': {
            'agent1': final_agent1_utility,
            'agent2': final_agent2_utility
        },
        'pareto_efficiency': pareto_efficiency,
        'negotiation_log': negotiation_log,
        'winner': agent1.name if final_agent1_utility > final_agent2_utility else agent2.name if final_agent2_utility > final_agent1_utility else 'Tie'
    }

def run_real_tournament(
    num_agents: int = 4,
    rounds_per_match: int = 20,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Run a real round-robin tournament between Group4 agents
    
    Args:
        num_agents: Number of agents to create
        rounds_per_match: Number of rounds per head-to-head match
        verbose: Whether to print progress
    
    Returns:
        Tournament results with rankings
    """
    if verbose:
        print(f"Starting REAL tournament with {num_agents} Group4 agents")
    
    # Create agents with different names
    agents = []
    for i in range(num_agents):
        agent = create_test_negotiator(name=f"Group4_Agent_{i+1}")
        agents.append(agent)
    
    # Round-robin tournament: every agent vs every other agent
    matches = []
    agent_scores = {agent.name: [] for agent in agents}
    
    total_matches = num_agents * (num_agents - 1)
    match_count = 0
    
    for i, agent1 in enumerate(agents):
        for j, agent2 in enumerate(agents):
            if i != j:  # Don't match agent against itself
                match_count += 1
                if verbose:
                    print(f"\nMatch {match_count}/{total_matches}: {agent1.name} vs {agent2.name}")
                
                # Run head-to-head negotiation
                match_result = negotiate_head_to_head(
                    agent1, agent2, 
                    rounds=rounds_per_match, 
                    verbose=verbose
                )
                
                matches.append(match_result)
                
                # Record scores
                agent_scores[agent1.name].append(match_result['final_utilities']['agent1'])
                agent_scores[agent2.name].append(match_result['final_utilities']['agent2'])
                
                if verbose:
                    print(f"Result: {agent1.name}={match_result['final_utilities']['agent1']:.3f}, "
                          f"{agent2.name}={match_result['final_utilities']['agent2']:.3f}")
    
    # Calculate tournament rankings
    tournament_results = []
    for agent_name, scores in agent_scores.items():
        avg_score = sum(scores) / len(scores) if scores else 0
        wins = sum(1 for score in scores if score > 0.5)
        tournament_results.append({
            'agent_name': agent_name,
            'average_utility': avg_score,
            'total_wins': wins,
            'total_matches': len(scores),
            'win_rate': wins / len(scores) if scores else 0
        })
    
    # Sort by average utility
    tournament_results.sort(key=lambda x: x['average_utility'], reverse=True)
    
    # Add rankings
    for i, result in enumerate(tournament_results):
        result['rank'] = i + 1
    
    if verbose:
        print(f"\n🏆 TOURNAMENT RESULTS:")
        for result in tournament_results:
            print(f"  {result['rank']}. {result['agent_name']}: "
                  f"Avg Utility={result['average_utility']:.3f}, "
                  f"Wins={result['total_wins']}/{result['total_matches']}")
    
    return {
        'tournament_type': 'real_round_robin',
        'num_agents': num_agents,
        'total_matches': len(matches),
        'matches': matches,
        'rankings': tournament_results,
        'champion': tournament_results[0]['agent_name']
    }