import asyncio
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any, Optional

from backend.models import SimulationPayload, WhatIfParameters, DigitalTwinState, MemoryEntry
from backend.agents import ExecutiveAgent, Coordinator, init_executives

app = FastAPI(
    title="MarketPulse AI Backend",
    description="Autonomous Executive Decision Intelligence Platform & Business Digital Twin API"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Persistent Business Digital Twin State (Baseline)
digital_twin_state = DigitalTwinState(
    business_health=82.0,
    revenue_protected=0.0,
    profit_impact=0.0,
    market_threat=15.0,
    customer_sentiment=78.0,
    operational_risk=12.0,
    inventory_health=85.0,
    market_share=28.5
)

# Persistent Business Memory Ledger
business_memory_ledger: List[MemoryEntry] = [
    MemoryEntry(
        event_date="Black Friday 2025",
        crises=["Competitor Flash Sale (40% OFF)", "Factory Delay (2 Days)"],
        strategy_chosen="Direct Price Match",
        outcome_profit_impact=-18.0,
        outcome_revenue_impact=12.5,
        lesson_learned="Direct Price Match protects market share, but severely dilutes profit margins and causes delivery backlogs under shipping constraints."
    ),
    MemoryEntry(
        event_date="Summer Prime Week 2025",
        crises=["Competitor Discount (30% OFF)"],
        strategy_chosen="No Action (Ignore Competitor)",
        outcome_profit_impact=2.0,
        outcome_revenue_impact=-14.0,
        lesson_learned="Ignoring competitor promotions during high-demand seasonal spikes causes major customer churn and permanent market share loss."
    )
]

@app.get("/api/events")
def get_available_events():
    return {
        "events": [
            {
                "id": "competitor_flash_sale",
                "name": "Competitor Flash Sale",
                "description": "MegaStore launches a 50% discount on all competitor laptop models.",
                "default_threat": 85.0
            },
            {
                "id": "shipment_delay",
                "name": "Supplier shipment Delay",
                "description": "Logistics reports a 3-day factory shipping delay on new laptop shipments.",
                "default_threat": 60.0
            },
            {
                "id": "negative_reviews",
                "name": "Negative Reviews Surge",
                "description": "Social media complaints spike due to minor power cable heating issues.",
                "default_threat": 50.0
            },
            {
                "id": "festival_demand",
                "name": "Festival Demand Spike",
                "description": "Black Friday customer demand spikes by 25% across all tech categories.",
                "default_threat": 10.0
            }
        ]
    }

@app.get("/api/memory")
def get_business_memory():
    return {"memory": [m.dict() for m in business_memory_ledger]}

@app.get("/api/digital-twin")
def get_digital_twin_status():
    global digital_twin_state
    return digital_twin_state.dict()

@app.post("/api/simulate")
def simulate_crisis(payload: SimulationPayload):
    """
    Direct simulation endpoint (instant response) for What-If slider adjustments.
    """
    global digital_twin_state
    params = payload.what_if or WhatIfParameters()
    
    # Initialize agents
    agents = init_executives()
    coordinator = Coordinator(agents)
    
    # Run simulation logic
    result = coordinator.run_simulation(payload.events, params, business_memory_ledger)
    
    # Update persistent digital twin state baseline
    new_twin = result["digital_twin_state"]
    digital_twin_state = DigitalTwinState(**new_twin)
    
    return result

@app.post("/api/simulate/stream")
def stream_simulation(payload: SimulationPayload):
    """
    SSE stream endpoint for cinematic real-time dashboard animations.
    Streams each stage sequentially with a delay to simulate active negotiation.
    """
    global digital_twin_state
    params = payload.what_if or WhatIfParameters()
    
    agents = init_executives()
    coordinator = Coordinator(agents)
    
    # Run the full simulation locally first to get complete data
    full_result = coordinator.run_simulation(payload.events, params, business_memory_ledger)
    
    # Update persistent state
    new_twin = full_result["digital_twin_state"]
    digital_twin_state = DigitalTwinState(**new_twin)

    async def event_generator():
        # Stream Stage 1: Investigation
        yield f"data: {json.dumps({'stage': 1, 'timeline': [s for s in full_result['timeline'] if s['stage'] == 1], 'agents': full_result['agents']})}\n\n"
        await asyncio.sleep(2.0)

        # Stream Stage 2: Evidence Sharing
        yield f"data: {json.dumps({'stage': 2, 'timeline': [s for s in full_result['timeline'] if s['stage'] == 2], 'messages': [m for m in full_result['messages'] if m['round'] == 2]})}\n\n"
        await asyncio.sleep(2.5)

        # Stream Stage 3: Executive Debate
        yield f"data: {json.dumps({'stage': 3, 'timeline': [s for s in full_result['timeline'] if s['stage'] == 3], 'messages': [m for m in full_result['messages'] if m['round'] == 3]})}\n\n"
        await asyncio.sleep(3.5)

        # Stream Stage 4: Strategy Proposals
        yield f"data: {json.dumps({'stage': 4, 'timeline': [s for s in full_result['timeline'] if s['stage'] == 4], 'proposals': full_result['proposals']})}\n\n"
        await asyncio.sleep(2.5)

        # Stream Stage 5: Voting & Synthesis
        yield f"data: {json.dumps({'stage': 5, 'timeline': [s for s in full_result['timeline'] if s['stage'] == 5], 'voting_matrix': full_result['voting_matrix'], 'final_recommendation': full_result['final_recommendation'], 'why_not_panel': full_result['why_not_panel'], 'digital_twin_state': full_result['digital_twin_state']})}\n\n"

        # Update memory ledger in backend
        mem_entry = MemoryEntry(
            event_date=datetime.now().strftime("%B %d, %Y"),
            crises=payload.events,
            strategy_chosen=full_result['final_recommendation']['winning_strategy'],
            outcome_profit_impact=full_result['final_recommendation']['projected_kpis']['profit_impact'],
            outcome_revenue_impact=round(full_result['final_recommendation']['projected_kpis']['revenue_protected'] / 10000.0, 1),
            lesson_learned=f"Running '{full_result['final_recommendation']['winning_strategy']}' in response to {', '.join(payload.events)} achieved a net business health score of {full_result['final_recommendation']['winning_strategy']}."
        )
        business_memory_ledger.append(mem_entry)
        
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
