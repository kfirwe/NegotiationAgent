"""
Domain Analysis for Holiday Negotiation Scenario
Assignment Section 1 - Familiarizing with the Negotiation Environment
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any
from itertools import product
import pandas as pd

class HolidayNegotiationAnalysis:
    """
    Analysis of the holiday negotiation scenario between Agent A and Agent B
    """
    
    def __init__(self):
        # Domain definition
        self.issues = {
            'location': ['Antalya', 'Barcelona', 'Milan'],
            'duration': ['1 week', '2 weeks'],
            'hotel_quality': ['Hostel', '3 star hotel', '5 star hotel']
        }
        
        # Agent A's preferences
        self.agent_a = {
            'weights': {
                'location': 0.5,
                'duration': 0.2,
                'hotel_quality': 0.3
            },
            'evaluation_values': {
                'location': {'Antalya': 4, 'Barcelona': 10, 'Milan': 2},
                'duration': {'1 week': 3, '2 weeks': 10},
                'hotel_quality': {'Hostel': 10, '3 star hotel': 2, '5 star hotel': 3}
            }
        }
        
        # Agent B's preferences
        self.agent_b = {
            'weights': {
                'location': 0.5,
                'duration': 0.4,
                'hotel_quality': 0.1
            },
            'evaluation_values': {
                'location': {'Antalya': 3, 'Barcelona': 2, 'Milan': 10},
                'duration': {'1 week': 4, '2 weeks': 10},
                'hotel_quality': {'Hostel': 3, '3 star hotel': 3, '5 star hotel': 10}
            }
        }
        
        # Reservation values (added as required)
        self.reservation_values = {
            'agent_a': 0.5,
            'agent_b': 0.2
        }
        
        # Normalize utilities to [0,1] range
        self._normalize_utilities()
        
    def _normalize_utilities(self):
        """Normalize utility values to [0,1] range"""
        for agent in [self.agent_a, self.agent_b]:
            for issue in self.issues:
                values = list(agent['evaluation_values'][issue].values())
                min_val, max_val = min(values), max(values)
                if max_val > min_val:
                    for option in agent['evaluation_values'][issue]:
                        old_val = agent['evaluation_values'][issue][option]
                        agent['evaluation_values'][issue][option] = (old_val - min_val) / (max_val - min_val)
    
    def calculate_utility(self, outcome: Dict[str, str], agent: str) -> float:
        """Calculate utility for a given outcome and agent"""
        agent_prefs = self.agent_a if agent == 'A' else self.agent_b
        
        utility = 0.0
        for issue, value in outcome.items():
            weight = agent_prefs['weights'][issue]
            eval_value = agent_prefs['evaluation_values'][issue][value]
            utility += weight * eval_value
            
        return utility
    
    def generate_all_outcomes(self) -> List[Dict[str, str]]:
        """Generate all possible outcomes in the domain"""
        outcomes = []
        for combo in product(*self.issues.values()):
            outcome = dict(zip(self.issues.keys(), combo))
            outcomes.append(outcome)
        return outcomes
    
    def compute_nash_point(self) -> Dict[str, Any]:
        """Compute Nash Point outcome (maximizes product of utilities)"""
        outcomes = self.generate_all_outcomes()
        best_outcome = None
        best_nash_product = 0
        
        nash_analysis = []
        
        for outcome in outcomes:
            utility_a = self.calculate_utility(outcome, 'A')
            utility_b = self.calculate_utility(outcome, 'B')
            
            # Nash product (subtract reservation values)
            nash_product = (utility_a - self.reservation_values['agent_a']) * \
                          (utility_b - self.reservation_values['agent_b'])
            
            nash_analysis.append({
                'outcome': outcome,
                'utility_a': utility_a,
                'utility_b': utility_b,
                'nash_product': nash_product
            })
            
            if nash_product > best_nash_product:
                best_nash_product = nash_product
                best_outcome = outcome
        
        return {
            'nash_outcome': best_outcome,
            'nash_product': best_nash_product,
            'nash_utilities': {
                'agent_a': self.calculate_utility(best_outcome, 'A'),
                'agent_b': self.calculate_utility(best_outcome, 'B')
            },
            'all_outcomes': nash_analysis
        }
    
    def compute_pareto_frontier(self) -> List[Dict[str, Any]]:
        """Compute Pareto efficient outcomes"""
        outcomes = self.generate_all_outcomes()
        pareto_outcomes = []
        
        for outcome in outcomes:
            utility_a = self.calculate_utility(outcome, 'A')
            utility_b = self.calculate_utility(outcome, 'B')
            
            is_pareto = True
            for other_outcome in outcomes:
                other_utility_a = self.calculate_utility(other_outcome, 'A')
                other_utility_b = self.calculate_utility(other_outcome, 'B')
                
                # Check if other outcome dominates this one
                if (other_utility_a >= utility_a and other_utility_b >= utility_b and
                    (other_utility_a > utility_a or other_utility_b > utility_b)):
                    is_pareto = False
                    break
            
            if is_pareto:
                pareto_outcomes.append({
                    'outcome': outcome,
                    'utility_a': utility_a,
                    'utility_b': utility_b
                })
        
        return sorted(pareto_outcomes, key=lambda x: x['utility_a'])
    
    def analyze_opponent_offers(self, offers: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze Agent B's offers using frequency analysis (n = 0.1)
        """
        # Count frequencies
        issue_value_counts = {}
        for issue in self.issues:
            issue_value_counts[issue] = {}
            for value in self.issues[issue]:
                issue_value_counts[issue][value] = 0
        
        # Count occurrences
        for offer in offers:
            for issue, value in offer.items():
                issue_value_counts[issue][value] += 1
        
        # Calculate relative frequencies
        total_offers = len(offers)
        relative_frequencies = {}
        for issue in self.issues:
            relative_frequencies[issue] = {}
            for value in self.issues[issue]:
                relative_frequencies[issue][value] = issue_value_counts[issue][value] / total_offers
        
        # Estimate weights using frequency analysis with n = 0.1
        n = 0.1
        estimated_weights = {}
        
        for issue in self.issues:
            # Calculate variance of frequencies for this issue
            frequencies = list(relative_frequencies[issue].values())
            variance = np.var(frequencies)
            estimated_weights[issue] = variance + n
        
        # Normalize weights
        total_weight = sum(estimated_weights.values())
        for issue in estimated_weights:
            estimated_weights[issue] /= total_weight
        
        # Estimate evaluation values based on frequencies
        estimated_evaluations = {}
        for issue in self.issues:
            estimated_evaluations[issue] = {}
            frequencies = relative_frequencies[issue]
            max_freq = max(frequencies.values())
            
            for value in self.issues[issue]:
                # Higher frequency suggests higher preference
                estimated_evaluations[issue][value] = frequencies[value] / max_freq if max_freq > 0 else 0
        
        return {
            'estimated_weights': estimated_weights,
            'estimated_evaluations': estimated_evaluations,
            'relative_frequencies': relative_frequencies,
            'actual_weights': self.agent_b['weights'],
            'actual_evaluations': self.agent_b['evaluation_values']
        }
    
    def classify_negotiation_steps(self, offers: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Classify all negotiation steps by Agent B"""
        classifications = []
        
        for i, offer in enumerate(offers):
            utility_a = self.calculate_utility(offer, 'A')
            utility_b = self.calculate_utility(offer, 'B')
            
            # Determine step type
            if i == 0:
                step_type = "Opening Offer"
            else:
                prev_utility_b = self.calculate_utility(offers[i-1], 'B')
                if utility_b > prev_utility_b:
                    step_type = "Concession (worse for B)"
                elif utility_b < prev_utility_b:
                    step_type = "Improvement (better for B)"
                else:
                    step_type = "Lateral Move (same utility for B)"
            
            # Check if above reservation value
            above_reservation = utility_b > self.reservation_values['agent_b']
            
            classifications.append({
                'step': i + 1,
                'offer': offer,
                'utility_a': utility_a,
                'utility_b': utility_b,
                'step_type': step_type,
                'above_reservation': above_reservation
            })
        
        return classifications
    
    def compute_sensitivity_analysis(self) -> Dict[str, Any]:
        """Compute sensitivity of Agent B to Agent A's preferences"""
        outcomes = self.generate_all_outcomes()
        
        # Calculate correlation between utilities
        utilities_a = [self.calculate_utility(outcome, 'A') for outcome in outcomes]
        utilities_b = [self.calculate_utility(outcome, 'B') for outcome in outcomes]
        
        correlation = np.corrcoef(utilities_a, utilities_b)[0, 1]
        
        # Find outcomes that are good for A and analyze B's utility
        good_for_a = [outcome for outcome in outcomes if self.calculate_utility(outcome, 'A') > 0.7]
        b_utilities_when_a_good = [self.calculate_utility(outcome, 'B') for outcome in good_for_a]
        
        # Find outcomes that are good for B and analyze A's utility
        good_for_b = [outcome for outcome in outcomes if self.calculate_utility(outcome, 'B') > 0.7]
        a_utilities_when_b_good = [self.calculate_utility(outcome, 'A') for outcome in good_for_b]
        
        return {
            'correlation': correlation,
            'avg_b_utility_when_a_good': np.mean(b_utilities_when_a_good) if b_utilities_when_a_good else 0,
            'avg_a_utility_when_b_good': np.mean(a_utilities_when_b_good) if a_utilities_when_b_good else 0,
            'conflict_level': 'High' if correlation < -0.5 else 'Medium' if correlation < 0.5 else 'Low'
        }
    
    def check_pareto_optimality(self, outcome: Dict[str, str]) -> bool:
        """Check if given outcome is Pareto optimal"""
        pareto_outcomes = self.compute_pareto_frontier()
        
        for pareto_outcome in pareto_outcomes:
            if pareto_outcome['outcome'] == outcome:
                return True
        return False
    
    def plot_pareto_frontier(self, save_path: str = None):
        """Plot the Pareto frontier with reservation values"""
        outcomes = self.generate_all_outcomes()
        pareto_outcomes = self.compute_pareto_frontier()
        nash_point = self.compute_nash_point()
        
        # All outcomes
        all_utilities_a = [self.calculate_utility(outcome, 'A') for outcome in outcomes]
        all_utilities_b = [self.calculate_utility(outcome, 'B') for outcome in outcomes]
        
        # Pareto outcomes
        pareto_utilities_a = [p['utility_a'] for p in pareto_outcomes]
        pareto_utilities_b = [p['utility_b'] for p in pareto_outcomes]
        
        plt.figure(figsize=(10, 8))
        
        # Plot all outcomes
        plt.scatter(all_utilities_a, all_utilities_b, alpha=0.5, color='lightblue', label='All Outcomes')
        
        # Plot Pareto frontier
        plt.plot(pareto_utilities_a, pareto_utilities_b, 'ro-', linewidth=2, markersize=8, label='Pareto Frontier')
        
        # Plot Nash point
        nash_utilities = nash_point['nash_utilities']
        plt.scatter(nash_utilities['agent_a'], nash_utilities['agent_b'], 
                   color='green', s=200, marker='*', label='Nash Point', zorder=5)
        
        # Plot reservation values
        plt.axhline(y=self.reservation_values['agent_b'], color='red', linestyle='--', 
                   label=f"Agent B Reservation ({self.reservation_values['agent_b']})")
        plt.axvline(x=self.reservation_values['agent_a'], color='blue', linestyle='--', 
                   label=f"Agent A Reservation ({self.reservation_values['agent_a']})")
        
        plt.xlabel('Agent A Utility')
        plt.ylabel('Agent B Utility')
        plt.title('Holiday Negotiation: Pareto Frontier and Nash Point')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    
    def generate_full_analysis_report(self) -> str:
        """Generate comprehensive analysis report"""
        
        # 1. Nash Point Analysis
        nash_analysis = self.compute_nash_point()
        
        # 2. Agent B's offers from the assignment
        agent_b_offers = [
            {'location': 'Milan', 'duration': '2 weeks', 'hotel_quality': '5 star hotel'},
            {'location': 'Milan', 'duration': '2 weeks', 'hotel_quality': '3 star hotel'},
            {'location': 'Barcelona', 'duration': '2 weeks', 'hotel_quality': 'Hostel'},
            {'location': 'Antalya', 'duration': '1 week', 'hotel_quality': '3 star hotel'},
            {'location': 'Antalya', 'duration': '1 week', 'hotel_quality': 'Hostel'},
            {'location': 'Milan', 'duration': '2 weeks', 'hotel_quality': '5 star hotel'}
        ]
        
        # 3. Frequency analysis
        frequency_analysis = self.analyze_opponent_offers(agent_b_offers)
        
        # 4. Classify negotiation steps
        step_classifications = self.classify_negotiation_steps(agent_b_offers)
        
        # 5. Sensitivity analysis
        sensitivity = self.compute_sensitivity_analysis()
        
        # 6. Check Pareto optimality of specific offer
        antalya_offer = {'location': 'Antalya', 'duration': '1 week', 'hotel_quality': 'Hostel'}
        is_pareto_optimal = self.check_pareto_optimality(antalya_offer)
        
        # 7. Pareto frontier
        pareto_frontier = self.compute_pareto_frontier()
        
        report = f"""
=== HOLIDAY NEGOTIATION DOMAIN ANALYSIS ===

1. NASH POINT COMPUTATION:
Nash Optimal Outcome: {nash_analysis['nash_outcome']}
Nash Product: {nash_analysis['nash_product']:.4f}
Nash Utilities: Agent A = {nash_analysis['nash_utilities']['agent_a']:.4f}, Agent B = {nash_analysis['nash_utilities']['agent_b']:.4f}

2. AGENT B'S OFFERS ANALYSIS:
Total offers analyzed: {len(agent_b_offers)}

3. FREQUENCY ANALYSIS (n = 0.1):
Estimated Weights: {frequency_analysis['estimated_weights']}
Actual Weights: {frequency_analysis['actual_weights']}

Weight Estimation Accuracy:
- Location: Estimated={frequency_analysis['estimated_weights']['location']:.3f}, Actual={frequency_analysis['actual_weights']['location']:.3f}
- Duration: Estimated={frequency_analysis['estimated_weights']['duration']:.3f}, Actual={frequency_analysis['actual_weights']['duration']:.3f}
- Hotel Quality: Estimated={frequency_analysis['estimated_weights']['hotel_quality']:.3f}, Actual={frequency_analysis['actual_weights']['hotel_quality']:.3f}

4. NEGOTIATION STEPS CLASSIFICATION:
"""
        
        for step in step_classifications:
            report += f"Step {step['step']}: {step['step_type']} - Utility A={step['utility_a']:.3f}, B={step['utility_b']:.3f}\n"
        
        report += f"""
5. SENSITIVITY ANALYSIS:
Correlation between Agent A and B utilities: {sensitivity['correlation']:.4f}
Conflict Level: {sensitivity['conflict_level']}
Average B utility when A has good outcomes: {sensitivity['avg_b_utility_when_a_good']:.3f}
Average A utility when B has good outcomes: {sensitivity['avg_a_utility_when_b_good']:.3f}

6. PARETO OPTIMALITY CHECK:
Offer (Antalya, 1 week, Hostel) is Pareto Optimal: {is_pareto_optimal}
Agent A utility for this offer: {self.calculate_utility(antalya_offer, 'A'):.3f}
Agent B utility for this offer: {self.calculate_utility(antalya_offer, 'B'):.3f}

7. PARETO FRONTIER:
Number of Pareto efficient outcomes: {len(pareto_frontier)}
"""
        
        for i, pareto_outcome in enumerate(pareto_frontier):
            report += f"Pareto {i+1}: {pareto_outcome['outcome']} - A={pareto_outcome['utility_a']:.3f}, B={pareto_outcome['utility_b']:.3f}\n"
        
        return report


def main():
    """Run the complete holiday negotiation analysis"""
    analysis = HolidayNegotiationAnalysis()
    
    # Generate and print full analysis report
    report = analysis.generate_full_analysis_report()
    print(report)
    
    # Save report to file
    with open('holiday_analysis_report.txt', 'w') as f:
        f.write(report)
    
    # Generate Pareto frontier plot
    analysis.plot_pareto_frontier('holiday_pareto_frontier.png')
    
    print("\nAnalysis complete! Check 'holiday_analysis_report.txt' and 'holiday_pareto_frontier.png'")


if __name__ == "__main__":
    main()
