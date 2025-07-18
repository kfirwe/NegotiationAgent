"""
Quick start script for Group 4 negotiation agent
"""

from helpers import (
    create_test_negotiator, 
    simulate_negotiation, 
    run_comprehensive_test,
    run_tournament_simulation,
    setup_logging,
    negotiate_head_to_head,
    run_real_tournament
)


def main():
    # Setup logging
    logger = setup_logging(log_level="INFO")
    
    print("=== Group 4 Negotiation Agent Demo ===\n")
    
    # 1. Basic simulation (1 VS 1)
    print("1. Running basic simulation...")
    agent = create_test_negotiator(name="DemoAgent")
    basic_results = simulate_negotiation(agent, rounds=15, verbose=True)
    
    print(f"\nBasic simulation completed!")
    print(f"Agent: {basic_results['negotiator_name']}")
    print(f"Final stats: {basic_results['final_stats']}")
    
    # 2. Comprehensive test (Grade)
    print("\n" + "="*50)
    print("2. Running comprehensive test...")
    comprehensive_results = run_comprehensive_test(verbose=True)
    print(f"Overall assessment: {comprehensive_results['overall_assessment']['rating']}")
    
    # 3. Tournament simulation (Tournament)
    print("\n" + "="*50)
    print("3. Running tournament simulation...")
    tournament_results = run_tournament_simulation(num_agents=3, num_rounds=10, verbose=True)
    print(f"Tournament completed with {tournament_results['tournament_config']['num_agents']} agents")

    # 4. NEW: Head-to-head negotiation
    print("\n" + "="*50)
    print("4. Running head-to-head negotiation...")
    agent1 = create_test_negotiator(name="Group4_Alpha")
    agent2 = create_test_negotiator(name="Group4_Beta")
    
    head_to_head_result = negotiate_head_to_head(agent1, agent2, rounds=20, verbose=True)
    
    print(f"\nHead-to-head completed!")
    print(f"Winner: {head_to_head_result['winner']}")
    print(f"Final utilities: {head_to_head_result['final_utilities']}")
    
    # 5. NEW: Real tournament
    print("\n" + "="*50)
    print("5. Running REAL tournament...")
    real_tournament_results = run_real_tournament(num_agents=4, rounds_per_match=15, verbose=True)
    
    print(f"\nReal tournament completed!")
    print(f"Champion: {real_tournament_results['champion']}")

if __name__ == "__main__":
    main()