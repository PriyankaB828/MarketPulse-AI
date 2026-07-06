import json
from backend.models import SimulationPayload, WhatIfParameters, MemoryEntry
from backend.agents import init_executives, Coordinator

def test_cli_simulation():
    print("==================================================")
    print("MARKETPULSE AI - CLI BUSINESS DIGITAL TWIN TEST")
    print("==================================================")

    # 1. Setup events and parameters
    events = ["Competitor Flash Sale", "Supplier shipment Delay"]
    params = WhatIfParameters(
        competitor_discount=50.0,
        shipment_delay_days=3,
        sentiment_score=65.0,
        inventory_overstock_pct=40.0,
        demand_spike_pct=25.0,
        competitor_price=499.0
    )

    # 2. Setup mock memory
    memory = [
        MemoryEntry(
            event_date="Black Friday 2025",
            crises=["Competitor Flash Sale (40% OFF)", "Factory Delay (2 Days)"],
            strategy_chosen="Direct Price Match",
            outcome_profit_impact=-18.0,
            outcome_revenue_impact=12.5,
            lesson_learned="Direct Price Match protects market share, but severely dilutes profit margins and causes delivery backlogs under shipping constraints."
        )
    ]

    # 3. Initialize executives & coordinator
    agents = init_executives()
    coordinator = Coordinator(agents)

    # 4. Execute 5-stage simulation
    print(f"\n[INIT] Activating Business Digital Twin for events: {', '.join(events)}")
    print(f"[PARAMS] Competitor Discount: {params.competitor_discount}%, Shipping Delay: {params.shipment_delay_days} days")
    
    result = coordinator.run_simulation(events, params, memory)

    # 5. Verify results
    print("\n==================================================")
    print("STAGE 4: STRATEGY PROPOSALS GENERATED")
    print("==================================================")
    for prop in result["proposals"]:
        print(f"- {prop['proposed_by']} proposed: '{prop['strategy_name']}'")
        print(f"  Score breakdown -> Rev: {prop['decision_matrix']['revenue']}, Prof: {prop['decision_matrix']['profit']}, Inv: {prop['decision_matrix']['inventory']}, Overall: {prop['decision_matrix']['overall_score']}")

    print("\n==================================================")
    print("STAGE 5: VOTING MATRIX")
    print("==================================================")
    for vote in result["voting_matrix"]:
        icon = "APPROVE" if vote["approve"] else "REJECT"
        print(f"- {vote['agent_name']} voted {icon} on '{vote['strategy_name']}'. Rationale: {vote['rationale']}")

    print("\n==================================================")
    print("FINAL RECOMMENDATION SYNTHESIZED")
    print("==================================================")
    rec = result["final_recommendation"]
    print(f"WINNING STRATEGY: '{rec['winning_strategy']}' (Score: {rec['overall_score']})")
    print(f"JUSTIFICATION: {rec['justification']}")
    print("\nACTION ITEMS:")
    for idx, item in enumerate(rec["action_items"], 1):
        print(f"{idx}. {item}")

    print("\nPROJECTED DIGITAL TWIN KPIs:")
    kpis = result["digital_twin_state"]
    print(f"- Business Health Score: {kpis['business_health']}/100")
    print(f"- Revenue Protected: ${kpis['revenue_protected']:,}")
    print(f"- Profit Impact: {kpis['profit_impact']}%")
    print(f"- Market Threat: {kpis['market_threat']}/100")
    print(f"- Customer Sentiment: {kpis['customer_sentiment']}/100")
    print(f"- Inventory Health: {kpis['inventory_health']}/100")
    print(f"- Operational Risk: {kpis['operational_risk']}/100")

    print("\n==================================================")
    print("TEST COMPLETED SUCCESSFULLY")
    print("==================================================")

if __name__ == "__main__":
    test_cli_simulation()
