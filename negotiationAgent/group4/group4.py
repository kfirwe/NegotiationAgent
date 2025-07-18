from negmas.sao import SAONegotiator, SAOState, ResponseType
from negmas.outcomes import Outcome
from typing import Optional, Dict, Any, List
import random
import numpy as np
from collections import deque, defaultdict

class Group4(SAONegotiator):
    """
    Group 4 negotiation agent using Adaptive BOA Framework
    """
    
    def __init__(self, *args, **kwargs):
        # Remove unsupported parameters
        unsupported_params = ['can_propose', 'can_accept', 'can_reject']
        for param in unsupported_params:
            kwargs.pop(param, None)
            
        super().__init__(*args, **kwargs)
        
        # Strategy parameters
        self.reservation_value = 0.0
        self.concession_factor = 0.3
        self.time_pressure_threshold = 0.75
        self.exploration_rate = 0.1
        
        # BOA Framework components
        self.opponent_offers = deque(maxlen=50)
        self.my_offers = deque(maxlen=50)
        self.opponent_utilities = []
        self.opponent_concession_rate = 0.02
        self.opponent_preference_model = defaultdict(float)
        
        # Performance tracking
        self.total_negotiations = 0
        self.successful_negotiations = 0
        self.utilities_achieved = []
        
        # Initialize with default values
        self.mock_ufun = None
        self.is_initialized = False
        
    def initialize(self, preferences=None, ufun=None, **kwargs):
        """Initialize the agent for negotiation"""
        # Store the utility function
        if ufun:
            self.mock_ufun = ufun
        
        # Calculate reservation value
        if self.mock_ufun:
            self.reservation_value = self._calculate_reservation_value()
        else:
            self.reservation_value = 0.3  # Default fallback
            
        self.is_initialized = True
        
    @property
    def ufun(self):
        """Property to access utility function"""
        return self.mock_ufun
        
    def _calculate_reservation_value(self) -> float:
        """Calculate reservation value based on outcome space"""
        if not self.mock_ufun or not hasattr(self.mock_ufun, 'outcome_space'):
            return 0.3
            
        try:
            # Sample random outcomes to estimate reservation value
            outcomes = []
            for _ in range(100):
                outcome = self.mock_ufun.outcome_space.random_outcome()
                utility = self.mock_ufun(outcome)
                if utility is not None:
                    outcomes.append(utility)
            
            if outcomes:
                return np.percentile(outcomes, 15)  # 15th percentile
            return 0.3
        except:
            return 0.3
    
    def propose(self, state: SAOState) -> Optional[Outcome]:
        """Generate a proposal using BOA bidding strategy"""
        if not self.mock_ufun or not hasattr(self.mock_ufun, 'outcome_space'):
            return self._generate_mock_proposal()
            
        try:
            target_utility = self._calculate_target_utility(state)
            candidates = self._generate_candidates(target_utility)
            
            if candidates:
                best_offer = self._select_best_offer(candidates, state)
                self.my_offers.append(best_offer)

                # print(f"MY OFFER (Round {state.step}): {best_offer}, Target Utility: {target_utility:.3f}")

                return best_offer
            else:
                return self.mock_ufun.outcome_space.random_outcome()
        except:
            return self._generate_mock_proposal()
    
    def _generate_mock_proposal(self) -> Dict[str, Any]:
        """Generate mock proposal when no proper utility function"""
        return {
            'venue': random.choice(['Hotel', 'Restaurant', 'Club']),
            'food': random.choice(['Buffet', 'Plated', 'Cocktail']),
            'music': random.choice(['DJ', 'Band', 'Playlist']),
            'drinks': random.choice(['Premium', 'Standard', 'Basic'])
        }
    
    def _calculate_target_utility(self, state: SAOState) -> float:
        """Calculate target utility using adaptive strategy"""
        time_factor = state.relative_time
        
        # Adaptive BOA strategy
        if time_factor < self.time_pressure_threshold:
            # Conservative early phase
            target = 1.0 - self.concession_factor * (time_factor ** 2)
        else:
            # Aggressive late phase
            target = max(self.reservation_value, 
                        1.0 - self.concession_factor * time_factor)
        
        return max(target, self.reservation_value)
    
    def _generate_candidates(self, target_utility: float) -> List[Outcome]:
        """Generate candidate offers near target utility"""
        candidates = []
        attempts = 0
        max_attempts = 50
        
        while len(candidates) < 10 and attempts < max_attempts:
            outcome = self.mock_ufun.outcome_space.random_outcome()
            utility = self.mock_ufun(outcome)
            
            if utility is not None and utility >= target_utility * 0.8:
                candidates.append(outcome)
            
            attempts += 1
        
        # If no candidates found, generate compromise offers
        if not candidates:
            for _ in range(5):
                compromise_offer = self._generate_compromise_offer()
                if compromise_offer:
                    candidates.append(compromise_offer)
        
        return candidates
    
    def _generate_compromise_offer(self) -> Dict[str, Any]:
        """Generate a compromise offer mixing preferences"""
        return {
            'venue': random.choice(['Hotel', 'Restaurant']),  # Avoid extreme preferences
            'food': random.choice(['Plated', 'Cocktail']),    # Middle ground
            'music': random.choice(['Band', 'DJ']),           # Avoid extremes
            'drinks': random.choice(['Standard', 'Premium'])  # Compromise
        }
    
    def _select_best_offer(self, candidates: List[Outcome], state: SAOState) -> Outcome:
        """Select best offer from candidates"""
        if not candidates:
            return self.mock_ufun.outcome_space.random_outcome()
        
        # Score candidates by utility and novelty
        scored_candidates = []
        for candidate in candidates:
            utility = self.mock_ufun(candidate)
            novelty = self._calculate_novelty(candidate)
            score = utility + self.exploration_rate * novelty
            scored_candidates.append((score, candidate))
        
        # Return best scoring candidate
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        return scored_candidates[0][1]
    
    def _calculate_novelty(self, outcome: Outcome) -> float:
        """Calculate novelty of outcome compared to previous offers"""
        if not self.my_offers:
            return 1.0
        
        # Simple novelty: different from recent offers
        recent_offers = list(self.my_offers)[-5:]
        novelty = 1.0
        
        for recent_offer in recent_offers:
            if outcome == recent_offer:
                novelty -= 0.2
        
        return max(0.0, novelty)
    
    def respond(self, state: SAOState) -> ResponseType:
        """Respond to opponent offer using BOA acceptance strategy"""
        offer = state.current_offer
        
        if offer is None:
            return ResponseType.REJECT_OFFER
        
        # Track opponent offer
        self.opponent_offers.append(offer)
        self._update_opponent_model(offer, state)
        
        # Multi-criteria acceptance
        if self._should_accept(offer, state):
            self.successful_negotiations += 1
            if self.mock_ufun:
                utility = self.mock_ufun(offer)
                if utility is not None:
                    self.utilities_achieved.append(utility)
            return ResponseType.ACCEPT_OFFER
        
        return ResponseType.REJECT_OFFER
    
    def _should_accept(self, offer: Outcome, state: SAOState) -> bool:
        """Multi-criteria acceptance decision"""
        if not self.mock_ufun:
            return random.random() < 0.3
        
        offer_utility = self.mock_ufun(offer)
        if offer_utility is None:
            return False
        
        # CHANGE: More flexible acceptance criteria
        
        # Criterion 1: Above reservation value (but lower threshold)
        if offer_utility < self.reservation_value * 0.8:  # 80% of reservation
            return False
        
        # Criterion 2: Strong time pressure (NEW: earlier pressure)
        if state.relative_time > 0.85:  # Was 0.95, now 0.85
            return offer_utility > self.reservation_value * 0.6  # 60% of reservation
        
        # Criterion 3: Very late time pressure (NEW: emergency acceptance)
        if state.relative_time > 0.95:
            return offer_utility > self.reservation_value * 0.4  # 40% of reservation
        
        # Criterion 4: Better than expected next offer
        next_offer_utility = self._predict_next_offer_utility(state)
        if offer_utility >= next_offer_utility * 0.9:  # 90% of predicted
            return True
        
        # Criterion 5: Opponent concession pattern
        if self._is_opponent_conceding() and offer_utility > self.reservation_value * 0.9:
            return True
        
        return False
    
    def _predict_next_offer_utility(self, state: SAOState) -> float:
        """Predict utility of next offer we would make"""
        target_utility = self._calculate_target_utility(state)
        return target_utility * 0.95  # Slightly lower than target
    
    def _is_opponent_conceding(self) -> bool:
        """Check if opponent is making concessions"""
        if len(self.opponent_utilities) < 3:
            return False
        
        recent_utilities = self.opponent_utilities[-3:]
        return recent_utilities[-1] < recent_utilities[0]
    
    def _update_opponent_model(self, offer: Outcome, state: SAOState):
        """Update opponent model with new offer"""
        if self.mock_ufun:
            estimated_utility = self._estimate_opponent_utility(offer)
            self.opponent_utilities.append(estimated_utility)
        
        # Update preference model
        if hasattr(offer, 'items'):
            for issue, value in offer.items():
                self.opponent_preference_model[f"{issue}_{value}"] += 1
        elif isinstance(offer, dict):
            for issue, value in offer.items():
                self.opponent_preference_model[f"{issue}_{value}"] += 1
    
    def _estimate_opponent_utility(self, offer: Outcome) -> float:
        """Estimate opponent's utility for given offer"""
        # Simple estimation: assume opponent has inverse preferences
        our_utility = self.mock_ufun(offer)
        if our_utility is not None:
            return 1.0 - our_utility
        return 0.5
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics"""
        self.total_negotiations += 1
        
        success_rate = (self.successful_negotiations / max(1, self.total_negotiations))
        avg_utility = (sum(self.utilities_achieved) / max(1, len(self.utilities_achieved))) if self.utilities_achieved else 0.0
        
        return {
            'agent_name': self.name or 'Group4',
            'strategy': 'Adaptive BOA Framework',
            'total_negotiations': self.total_negotiations,
            'successful_negotiations': self.successful_negotiations,
            'success_rate': success_rate,
            'average_utility': avg_utility,
            'reservation_value': self.reservation_value,
            'opponent_reservation_estimate': self._estimate_opponent_reservation()
        }
    
    def _estimate_opponent_reservation(self) -> float:
        """Estimate opponent's reservation value"""
        if self.opponent_utilities:
            return min(self.opponent_utilities)
        return 0.0