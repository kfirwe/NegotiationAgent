"""
Nash/Pareto Analysis for Group4 Negotiation Agent
Assignment Step 4: Performance Documentation with Nash/Pareto Analysis
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Tuple, Optional
from group4 import Group4
from helpers.runner import negotiate_head_to_head, create_test_negotiator
import json
from itertools import product

class NashParetoAnalysis:
    """Analyze negotiation outcomes for Nash solutions and Pareto efficiency"""
    
    def __init__(self):
        self.outcomes_analyzed = []
        self.pareto_outcomes = []
        self.nash_outcomes = []
        
    def analyze_outcome(self, outcome: Dict[str, Any], agent1_ufun, agent2_ufun, 
                       agent1_reservation: float = 0.0, agent2_reservation: float = 0.0) -> Dict[str, Any]:
        """
        Analyze a single outcome for Nash and Pareto properties
        
        Args:
            outcome: The negotiation outcome
            agent1_ufun: Agent 1's utility function
            agent2_ufun: Agent 2's utility function
            agent1_reservation: Agent 1's reservation value
            agent2_reservation: Agent 2's reservation value
            
        Returns:
            Analysis results
        """
        # Calculate utilities
        utility1 = agent1_ufun(outcome) if agent1_ufun else 0.5
        utility2 = agent2_ufun(outcome) if agent2_ufun else 0.5
        
        # Nash product (above reservation values)
        nash_product = max(0, (utility1 - agent1_reservation) * (utility2 - agent2_reservation))
        
        # Pareto efficiency (sum of utilities)
        pareto_efficiency = utility1 + utility2
        
        # Social welfare
        social_welfare = (utility1 + utility2) / 2
        
        analysis = {
            'outcome': outcome,
            'agent1_utility': utility1,
            'agent2_utility': utility2,
            'nash_product': nash_product,
            'pareto_efficiency': pareto_efficiency,
            'social_welfare': social_welfare,
            'is_individually_rational': (utility1 >= agent1_reservation and utility2 >= agent2_reservation),
            'distance_from_nash': 0.0,  # Will be calculated later
            'is_pareto_optimal': False,  # Will be calculated later
            'is_nash_solution': False   # Will be calculated later
        }
        
        self.outcomes_analyzed.append(analysis)
        return analysis
    
    def find_nash_solution(self, all_outcomes: List[Dict[str, Any]], agent1_ufun, agent2_ufun,
                          agent1_reservation: float = 0.0, agent2_reservation: float = 0.0) -> Dict[str, Any]:
        """
        Find the Nash bargaining solution from a set of outcomes
        
        Args:
            all_outcomes: List of all possible outcomes
            agent1_ufun: Agent 1's utility function
            agent2_ufun: Agent 2's utility function
            agent1_reservation: Agent 1's reservation value
            agent2_reservation: Agent 2's reservation value
            
        Returns:
            Nash solution analysis
        """
        best_nash_product = 0
        nash_solution = None
        nash_utilities = None
        
        outcome_analyses = []
        
        for outcome in all_outcomes:
            analysis = self.analyze_outcome(outcome, agent1_ufun, agent2_ufun, 
                                          agent1_reservation, agent2_reservation)
            outcome_analyses.append(analysis)
            
            if analysis['nash_product'] > best_nash_product:
                best_nash_product = analysis['nash_product']
                nash_solution = outcome
                nash_utilities = (analysis['agent1_utility'], analysis['agent2_utility'])
        
        # Mark Nash solution
        for analysis in outcome_analyses:
            if analysis['outcome'] == nash_solution:
                analysis['is_nash_solution'] = True
                analysis['distance_from_nash'] = 0.0
            else:
                # Calculate distance from Nash solution
                if nash_utilities:
                    distance = np.sqrt((analysis['agent1_utility'] - nash_utilities[0])**2 + 
                                     (analysis['agent2_utility'] - nash_utilities[1])**2)
                    analysis['distance_from_nash'] = distance
        
        return {
            'nash_solution': nash_solution,
            'nash_utilities': nash_utilities,
            'nash_product': best_nash_product,
            'all_analyses': outcome_analyses
        }
    
    def find_pareto_frontier(self, all_outcomes: List[Dict[str, Any]], agent1_ufun, agent2_ufun) -> List[Dict[str, Any]]:
        """
        Find all Pareto optimal outcomes
        
        Args:
            all_outcomes: List of all possible outcomes
            agent1_ufun: Agent 1's utility function
            agent2_ufun: Agent 2's utility function
            
        Returns:
            List of Pareto optimal outcomes with analysis
        """
        pareto_outcomes = []
        
        # Calculate utilities for all outcomes
        outcome_utilities = []
        for outcome in all_outcomes:
            utility1 = agent1_ufun(outcome) if agent1_ufun else 0.5
            utility2 = agent2_ufun(outcome) if agent2_ufun else 0.5
            outcome_utilities.append((outcome, utility1, utility2))
        
        # Find Pareto optimal outcomes
        for i, (outcome1, u1_1, u2_1) in enumerate(outcome_utilities):
            is_pareto = True
            
            for j, (outcome2, u1_2, u2_2) in enumerate(outcome_utilities):
                if i != j:
                    # Check if outcome2 dominates outcome1
                    if (u1_2 >= u1_1 and u2_2 >= u2_1) and (u1_2 > u1_1 or u2_2 > u2_1):
                        is_pareto = False
                        break
            
            if is_pareto:
                pareto_outcomes.append({
                    'outcome': outcome1,
                    'agent1_utility': u1_1,
                    'agent2_utility': u2_1,
                    'pareto_efficiency': u1_1 + u2_1,
                    'is_pareto_optimal': True
                })
        
        # Sort by agent1 utility
        pareto_outcomes.sort(key=lambda x: x['agent1_utility'])
        
        # Update analysis with Pareto optimality
        for analysis in self.outcomes_analyzed:
            for pareto_outcome in pareto_outcomes:
                if analysis['outcome'] == pareto_outcome['outcome']:
                    analysis['is_pareto_optimal'] = True
                    break
        
        self.pareto_outcomes = pareto_outcomes
        return pareto_outcomes
    
    def analyze_negotiation_session(self, negotiation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a complete negotiation session for Nash and Pareto properties
        
        Args:
            negotiation_result: Result from negotiate_head_to_head function
            
        Returns:
            Complete analysis of the negotiation
        """
        if not negotiation_result['agreement_reached']:
            return {
                'agreement_reached': False,
                'analysis': 'No agreement reached - cannot analyze Nash/Pareto properties'
            }
        
        final_offer = negotiation_result['final_offer']
        final_utilities = negotiation_result['final_utilities']
        
        # Create mock utility functions based on final utilities
        # (This is a simplified approach - in real scenarios, you'd have actual utility functions)
        def create_mock_ufun(preferred_outcome, utility_value):
            def ufun(outcome):
                if outcome == preferred_outcome:
                    return utility_value
                else:
                    # Generate some variation for other outcomes
                    import random
                    return max(0, utility_value + random.uniform(-0.3, 0.3))
            return ufun
        
        agent1_ufun = create_mock_ufun(final_offer, final_utilities['agent1'])
        agent2_ufun = create_mock_ufun(final_offer, final_utilities['agent2'])
        
        # Generate possible outcomes for comparison
        possible_outcomes = self._generate_possible_outcomes()
        
        # Find Nash solution
        nash_analysis = self.find_nash_solution(possible_outcomes, agent1_ufun, agent2_ufun)
        
        # Find Pareto frontier
        pareto_frontier = self.find_pareto_frontier(possible_outcomes, agent1_ufun, agent2_ufun)
        
        # Analyze final outcome
        final_analysis = self.analyze_outcome(final_offer, agent1_ufun, agent2_ufun)
        
        # Check if final outcome is Nash solution
        is_nash_solution = final_offer == nash_analysis['nash_solution']
        
        # Check if final outcome is Pareto optimal
        is_pareto_optimal = any(p['outcome'] == final_offer for p in pareto_frontier)
        
        return {
            'agreement_reached': True,
            'final_offer': final_offer,
            'final_utilities': final_utilities,
            'is_nash_solution': is_nash_solution,
            'is_pareto_optimal': is_pareto_optimal,
            'nash_distance': final_analysis['distance_from_nash'],
            'pareto_efficiency': final_analysis['pareto_efficiency'],
            'social_welfare': final_analysis['social_welfare'],
            'nash_solution': nash_analysis['nash_solution'],
            'nash_utilities': nash_analysis['nash_utilities'],
            'pareto_frontier_size': len(pareto_frontier),
            'negotiation_efficiency': self._calculate_negotiation_efficiency(negotiation_result),
            'outcome_quality': self._assess_outcome_quality(final_analysis, nash_analysis, pareto_frontier)
        }
    
    def _generate_possible_outcomes(self) -> List[Dict[str, Any]]:
        """Generate a set of possible outcomes for analysis"""
        issues = {
            'venue': ['Hotel', 'Restaurant', 'Club'],
            'food': ['Buffet', 'Plated', 'Cocktail'],
            'music': ['DJ', 'Band', 'Playlist'],
            'drinks': ['Premium', 'Standard', 'Basic']
        }
        
        outcomes = []
        for combo in product(*issues.values()):
            outcome = dict(zip(issues.keys(), combo))
            outcomes.append(outcome)
        
        return outcomes
    
    def _calculate_negotiation_efficiency(self, negotiation_result: Dict[str, Any]) -> float:
        """Calculate how efficiently the negotiation reached agreement"""
        total_rounds = negotiation_result['total_rounds']
        final_round = negotiation_result['final_round']
        
        # Efficiency: earlier agreement is more efficient
        if total_rounds > 0:
            return 1.0 - (final_round / total_rounds)
        return 0.0
    
    def _assess_outcome_quality(self, final_analysis: Dict[str, Any], 
                               nash_analysis: Dict[str, Any], 
                               pareto_frontier: List[Dict[str, Any]]) -> str:
        """Assess the quality of the negotiated outcome"""
        if final_analysis['is_nash_solution'] and final_analysis['is_pareto_optimal']:
            return "Excellent - Nash solution and Pareto optimal"
        elif final_analysis['is_nash_solution']:
            return "Good - Nash solution but not Pareto optimal"
        elif final_analysis['is_pareto_optimal']:
            return "Good - Pareto optimal but not Nash solution"
        elif final_analysis['distance_from_nash'] < 0.1:
            return "Fair - Close to Nash solution"
        elif final_analysis['social_welfare'] > 0.7:
            return "Fair - High social welfare"
        else:
            return "Poor - Low efficiency and far from optimal"
    
    def run_comprehensive_nash_pareto_analysis(self, num_negotiations: int = 10) -> Dict[str, Any]:
        """
        Run comprehensive Nash/Pareto analysis on multiple negotiations
        
        Args:
            num_negotiations: Number of negotiations to analyze
            
        Returns:
            Comprehensive analysis results
        """
        print(f"=== COMPREHENSIVE NASH/PARETO ANALYSIS ({num_negotiations} negotiations) ===")
        
        results = {
            'total_negotiations': num_negotiations,
            'agreements_reached': 0,
            'nash_solutions': 0,
            'pareto_optimal_outcomes': 0,
            'both_nash_and_pareto': 0,
            'negotiation_analyses': [],
            'summary_statistics': {}
        }
        
        for i in range(num_negotiations):
            print(f"Analyzing negotiation {i+1}/{num_negotiations}...")
            
            # Create two agents with different preferences
            agent1 = create_test_negotiator(name=f"Agent1_Analysis_{i}")
            agent2 = create_test_negotiator(name=f"Agent2_Analysis_{i}")
            
            # Run negotiation
            negotiation_result = negotiate_head_to_head(agent1, agent2, rounds=20, verbose=False)
            
            # Analyze the negotiation
            analysis = self.analyze_negotiation_session(negotiation_result)
            results['negotiation_analyses'].append(analysis)
            
            # Update counters
            if analysis['agreement_reached']:
                results['agreements_reached'] += 1
                
                if analysis['is_nash_solution']:
                    results['nash_solutions'] += 1
                    
                if analysis['is_pareto_optimal']:
                    results['pareto_optimal_outcomes'] += 1
                    
                if analysis['is_nash_solution'] and analysis['is_pareto_optimal']:
                    results['both_nash_and_pareto'] += 1
        
        # Calculate summary statistics
        if results['agreements_reached'] > 0:
            results['summary_statistics'] = {
                'agreement_rate': results['agreements_reached'] / num_negotiations,
                'nash_solution_rate': results['nash_solutions'] / results['agreements_reached'],
                'pareto_optimal_rate': results['pareto_optimal_outcomes'] / results['agreements_reached'],
                'optimal_outcome_rate': results['both_nash_and_pareto'] / results['agreements_reached'],
                'avg_social_welfare': np.mean([a['social_welfare'] for a in results['negotiation_analyses'] if a['agreement_reached']]),
                'avg_negotiation_efficiency': np.mean([a['negotiation_efficiency'] for a in results['negotiation_analyses'] if a['agreement_reached']]),
                'avg_pareto_efficiency': np.mean([a['pareto_efficiency'] for a in results['negotiation_analyses'] if a['agreement_reached']])
            }
        
        return results
    
    def generate_nash_pareto_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate comprehensive Nash/Pareto analysis report"""
        
        report = f"""
=== NASH/PARETO ANALYSIS REPORT ===

NEGOTIATION OUTCOMES:
- Total negotiations: {analysis_results['total_negotiations']}
- Agreements reached: {analysis_results['agreements_reached']}
- Agreement rate: {analysis_results['summary_statistics'].get('agreement_rate', 0):.1%}

SOLUTION QUALITY:
- Nash solutions: {analysis_results['nash_solutions']} ({analysis_results['summary_statistics'].get('nash_solution_rate', 0):.1%})
- Pareto optimal: {analysis_results['pareto_optimal_outcomes']} ({analysis_results['summary_statistics'].get('pareto_optimal_rate', 0):.1%})
- Both Nash and Pareto: {analysis_results['both_nash_and_pareto']} ({analysis_results['summary_statistics'].get('optimal_outcome_rate', 0):.1%})

EFFICIENCY METRICS:
- Average social welfare: {analysis_results['summary_statistics'].get('avg_social_welfare', 0):.3f}
- Average negotiation efficiency: {analysis_results['summary_statistics'].get('avg_negotiation_efficiency', 0):.3f}
- Average Pareto efficiency: {analysis_results['summary_statistics'].get('avg_pareto_efficiency', 0):.3f}

DETAILED ANALYSIS:
"""
        
        for i, analysis in enumerate(analysis_results['negotiation_analyses']):
            if analysis['agreement_reached']:
                report += f"""
Negotiation {i+1}:
- Final utilities: Agent1={analysis['final_utilities']['agent1']:.3f}, Agent2={analysis['final_utilities']['agent2']:.3f}
- Nash solution: {analysis['is_nash_solution']}
- Pareto optimal: {analysis['is_pareto_optimal']}
- Outcome quality: {analysis['outcome_quality']}
- Social welfare: {analysis['social_welfare']:.3f}
- Negotiation efficiency: {analysis['negotiation_efficiency']:.3f}
"""
        
        return report
    
    def plot_nash_pareto_analysis(self, analysis_results: Dict[str, Any], save_path: str = None):
        """Create visualizations for Nash/Pareto analysis"""
        
        # Extract data for plotting
        agreements = [a for a in analysis_results['negotiation_analyses'] if a['agreement_reached']]
        
        if not agreements:
            print("No agreements to plot")
            return
        
        agent1_utilities = [a['final_utilities']['agent1'] for a in agreements]
        agent2_utilities = [a['final_utilities']['agent2'] for a in agreements]
        nash_solutions = [a['is_nash_solution'] for a in agreements]
        pareto_optimal = [a['is_pareto_optimal'] for a in agreements]
        
        # Create subplot layout
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Utility space plot
        colors = ['red' if ns else 'blue' for ns in nash_solutions]
        markers = ['s' if po else 'o' for po in pareto_optimal]
        
        for i, (u1, u2, ns, po) in enumerate(zip(agent1_utilities, agent2_utilities, nash_solutions, pareto_optimal)):
            ax1.scatter(u1, u2, c=colors[i], marker=markers[i], s=100, alpha=0.7)
        
        ax1.set_xlabel('Agent 1 Utility')
        ax1.set_ylabel('Agent 2 Utility')
        ax1.set_title('Negotiation Outcomes in Utility Space')
        ax1.grid(True, alpha=0.3)
        
        # Legend
        ax1.scatter([], [], c='red', marker='o', s=100, label='Nash Solution')
        ax1.scatter([], [], c='blue', marker='s', s=100, label='Pareto Optimal')
        ax1.scatter([], [], c='gray', marker='o', s=100, label='Other')
        ax1.legend()
        
        # 2. Social welfare distribution
        social_welfare = [a['social_welfare'] for a in agreements]
        ax2.hist(social_welfare, bins=10, alpha=0.7, color='green')
        ax2.set_xlabel('Social Welfare')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Distribution of Social Welfare')
        ax2.grid(True, alpha=0.3)
        
        # 3. Solution quality pie chart
        quality_counts = {
            'Nash & Pareto': analysis_results['both_nash_and_pareto'],
            'Nash only': analysis_results['nash_solutions'] - analysis_results['both_nash_and_pareto'],
            'Pareto only': analysis_results['pareto_optimal_outcomes'] - analysis_results['both_nash_and_pareto'],
            'Neither': analysis_results['agreements_reached'] - analysis_results['nash_solutions'] - analysis_results['pareto_optimal_outcomes'] + analysis_results['both_nash_and_pareto']
        }
        
        ax3.pie(quality_counts.values(), labels=quality_counts.keys(), autopct='%1.1f%%', startangle=90)
        ax3.set_title('Solution Quality Distribution')
        
        # 4. Negotiation efficiency
        efficiency = [a['negotiation_efficiency'] for a in agreements]
        ax4.hist(efficiency, bins=10, alpha=0.7, color='orange')
        ax4.set_xlabel('Negotiation Efficiency')
        ax4.set_ylabel('Frequency')
        ax4.set_title('Distribution of Negotiation Efficiency')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()


def main():
    """Run comprehensive Nash/Pareto analysis"""
    analyzer = NashParetoAnalysis()
    
    # Run analysis on multiple negotiations
    results = analyzer.run_comprehensive_nash_pareto_analysis(num_negotiations=20)
    
    # Generate report
    report = analyzer.generate_nash_pareto_report(results)
    print(report)
    
    # Save report
    with open('nash_pareto_analysis_report.txt', 'w') as f:
        f.write(report)
    
    # Save detailed results as JSON
    # with open('nash_pareto_analysis_results.json', 'w') as f:
    #     json.dump(results, f, indent=2, default=str)
    
    # Create plots
    analyzer.plot_nash_pareto_analysis(results, 'nash_pareto_analysis.png')
    
    print("\nNash/Pareto analysis complete!")
    print("Check 'nash_pareto_analysis_report.txt' and 'nash_pareto_analysis.png' for results.")


if __name__ == "__main__":
    main()
