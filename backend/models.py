from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class WhatIfParameters(BaseModel):
    competitor_discount: float = Field(50.0, description="Competitor discount percentage (0 to 100)")
    shipment_delay_days: int = Field(3, description="Shipment delay in days (0 to 10)")
    sentiment_score: float = Field(65.0, description="Customer sentiment score (0 to 100)")
    inventory_overstock_pct: float = Field(40.0, description="Warehouse overstock percentage (0 to 100)")
    demand_spike_pct: float = Field(25.0, description="Customer demand spike percentage (0 to 100)")
    competitor_price: float = Field(499.0, description="Competitor price in USD")

class DigitalTwinState(BaseModel):
    business_health: float = Field(82.0, description="Overall business health score (0-100)")
    revenue_protected: float = Field(0.0, description="Estimated revenue protected in USD")
    profit_impact: float = Field(0.0, description="Net profit impact percentage")
    market_threat: float = Field(15.0, description="Current market threat level (0-100)")
    customer_sentiment: float = Field(78.0, description="Customer sentiment (0-100)")
    operational_risk: float = Field(12.0, description="Operational risk level (0-100)")
    inventory_health: float = Field(85.0, description="Inventory health score (0-100)")
    market_share: float = Field(28.5, description="Current market share percentage")

class AgentModel(BaseModel):
    id: str
    name: str
    role: str
    goal: str
    constraints: List[str]
    success_metrics: List[str]
    authority_level: str
    voting_weight: int
    trust_score: float
    current_recommendation: str = ""
    current_vote: Optional[str] = None
    status: str = "idle" # idle, investigating, debating, voting, done

class Message(BaseModel):
    sender: str
    recipient: str
    content: str
    round: int
    timestamp: str

class StrategyDecisionMatrix(BaseModel):
    revenue: float
    profit: float
    inventory: float
    customer_retention: float
    operational_risk: float
    brand_value: float
    market_share: float
    overall_score: float

class StrategyProposal(BaseModel):
    strategy_name: str
    proposed_by: str
    description: str
    decision_matrix: StrategyDecisionMatrix
    reason_for_proposal: str

class StrategyVote(BaseModel):
    agent_id: str
    agent_name: str
    strategy_name: str
    approve: bool
    rationale: str

class RejectedStrategyDetail(BaseModel):
    strategy_name: str
    proposed_by: str
    primary_showstopper: str
    pros: List[str]
    cons: List[str]
    impact_summary: str

class FinalRecommendation(BaseModel):
    winning_strategy: str
    overall_score: float
    justification: str
    action_items: List[str]
    projected_kpis: DigitalTwinState
    decision_matrix: StrategyDecisionMatrix

class MemoryEntry(BaseModel):
    event_date: str
    crises: List[str]
    strategy_chosen: str
    outcome_profit_impact: float
    outcome_revenue_impact: float
    lesson_learned: str

class SimulationPayload(BaseModel):
    events: List[str]
    what_if: Optional[WhatIfParameters] = None
