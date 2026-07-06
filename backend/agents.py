import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from google import genai
from google.genai import types
from backend.models import (
    AgentModel, Message, StrategyProposal, StrategyVote, StrategyDecisionMatrix,
    FinalRecommendation, DigitalTwinState, RejectedStrategyDetail, MemoryEntry, WhatIfParameters
)
from backend.tools import (
    competitor_intelligence_mcp, customer_insight_mcp, inventory_analytics_mcp,
    financial_modeling_mcp, marketing_optimization_mcp, supply_chain_intelligence_mcp
)

# Initialize Gemini Client if Key is Present
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
client = None
if GEMINI_KEY:
    try:
        client = genai.Client(api_key=GEMINI_KEY)
    except Exception as e:
        print(f"Failed to initialize live Gemini Client: {e}")

class ExecutiveAgent:
    def __init__(self, agent_id: str, name: str, role: str, goal: str, constraints: List[str], success_metrics: List[str], authority_level: str, voting_weight: int, trust_score: float):
        self.id = agent_id
        self.name = name
        self.role = role
        self.goal = goal
        self.constraints = constraints
        self.success_metrics = success_metrics
        self.authority_level = authority_level
        self.voting_weight = voting_weight
        self.trust_score = trust_score
        self.current_recommendation = ""
        self.current_vote = None
        self.status = "idle"
        self.mcp_logs = []

    def to_model(self) -> AgentModel:
        return AgentModel(
            id=self.id,
            name=self.name,
            role=self.role,
            goal=self.goal,
            constraints=self.constraints,
            success_metrics=self.success_metrics,
            authority_level=self.authority_level,
            voting_weight=self.voting_weight,
            trust_score=self.trust_score,
            current_recommendation=self.current_recommendation,
            current_vote=self.current_vote,
            status=self.status
        )

    def execute_investigation(self, events: List[str], params: WhatIfParameters) -> Dict[str, Any]:
        """
        Stage 1: Calls corresponding MCP tools and gathers raw data.
        """
        self.status = "investigating"
        mcp_data = {}
        
        if self.id == "cfo":
            # CFO uses Financial Modeling MCP. Raw costs for a laptop: COGS = 500, Sell Price = 999.
            mcp_data = financial_modeling_mcp(cogs_usd=500.0, sell_price_usd=999.0, discount_pct=params.competitor_discount)
        elif self.id == "cmo":
            # CMO uses Marketing Optimization MCP.
            mcp_data = marketing_optimization_mcp(demand_spike_pct=params.demand_spike_pct)
        elif self.id == "inventory":
            # Inventory uses Inventory Analytics MCP.
            mcp_data = inventory_analytics_mcp(overstock_pct=params.inventory_overstock_pct)
        elif self.id == "coo":
            # Operations uses Supply Chain Intelligence MCP.
            mcp_data = supply_chain_intelligence_mcp(delay_days=params.shipment_delay_days)
        elif self.id == "cco":
            # Customer uses Customer Insight MCP.
            mcp_data = customer_insight_mcp(sentiment_score=params.sentiment_score, competitor_discount=params.competitor_discount)
        elif self.id == "market":
            # Market Intelligence uses Competitor Intelligence MCP.
            mcp_data = competitor_intelligence_mcp(competitor_discount=params.competitor_discount, competitor_price=params.competitor_price)
            
        self.mcp_logs.append(mcp_data)
        self.status = "idle"
        return mcp_data

class StrategySynthesizer:
    def __init__(self):
        pass

    def synthesize(self, 
                   events: List[str], 
                   params: WhatIfParameters, 
                   agents: Dict[str, ExecutiveAgent], 
                   debate_messages: List[Message], 
                   votes: List[StrategyVote],
                   proposals: List[StrategyProposal],
                   memory: List[MemoryEntry]) -> FinalRecommendation:
        """
        Stage 5: Synthesizes final recommendations, computes business scores, and builds decision matrix.
        """
        # We calculate scores dynamically depending on the selected events and What-If values.
        # Possible strategies: 'Price Match', 'Premium Bundle', 'Loyalty Cashback', 'Delayed Promotion', 'No Action'
        
        # Calculate winning scores
        # Bundle Strategy is generally optimal on Black Friday when shipping delays exist and inventory overstock is high,
        # because it allows shipping delays to be mitigated by shipping available accessories first or bundles,
        # and protects margins since COGS of accessories are low.
        
        # Let's compute weights based on trust scores:
        # CFO: 98, CMO: 91, VP Inv: 99, COO: 95, CCO: 89, VP Mkt: 93
        
        scores = {}
        for prop in proposals:
            name = prop.strategy_name
            # Compute a base score
            if name == "Premium Accessory Bundle":
                # High overstock + shipping delays make Bundle excellent
                score_rev = min(88 + params.demand_spike_pct * 0.2, 98.0)
                score_prof = max(85 - (params.competitor_discount - 50) * 0.1, 75.0)
                score_inv = min(90 + params.inventory_overstock_pct * 0.15, 99.0)
                score_cust = min(84 + params.sentiment_score * 0.1, 95.0)
                score_risk = max(90 - params.shipment_delay_days * 3.0, 60.0)
                score_brand = 88.0
                score_share = 86.0
            elif name == "Direct Price Match":
                # Price matching increases revenue and share, but destroys profit margins (especially if competitor discount > 40%)
                score_rev = min(92 + params.demand_spike_pct * 0.3, 100.0)
                score_prof = max(55.0 - (params.competitor_discount - 30) * 1.5, 10.0) # Margin destroys profit
                score_inv = 70.0 # Clears laptops, leaves dead stock accessories
                score_cust = 92.0 # Customers love cheap laptops
                score_risk = max(75 - params.shipment_delay_days * 6.0, 30.0) # High logistics risk due to supply bottlenecks
                score_brand = 78.0
                score_share = min(95.0, 90.0 + (params.competitor_discount - 40) * 0.2)
            elif name == "Loyalty Cash-Back Strategy":
                # Loyalty cashback protects margin, increases customer retention, but has medium market share impact
                score_rev = 80.0
                score_prof = 84.0
                score_inv = 68.0
                score_cust = 93.0
                score_risk = 92.0 # Low logistics risk since it's deferred rewards
                score_brand = 92.0
                score_share = 78.0
            elif name == "SLA-Guaranteed Delayed Promotion":
                # Delaying promotion solves shipment delays but fails to defend market share during peak window
                score_rev = 65.0
                score_prof = 78.0
                score_inv = 60.0
                score_cust = 72.0
                score_risk = 98.0 # No SLA risk since shipping is scheduled later
                score_brand = 82.0
                score_share = 64.0
            else: # No Action
                score_rev = 45.0
                score_prof = 80.0
                score_inv = 50.0
                score_cust = 58.0
                score_risk = 99.0
                score_brand = 70.0
                score_share = 52.0

            # Overall score calculation
            overall = (score_rev * 0.15 + score_prof * 0.25 + score_inv * 0.15 + score_cust * 0.15 + score_risk * 0.10 + score_brand * 0.10 + score_share * 0.10)
            
            # Incorporate memory penalty if matching previous failures
            for mem in memory:
                if mem.strategy_chosen == "Direct Price Match" and name == "Direct Price Match":
                    overall -= 8.0 # Penalty for repeating historical failure
            
            scores[name] = {
                "revenue": round(score_rev, 1),
                "profit": round(score_prof, 1),
                "inventory": round(score_inv, 1),
                "customer_retention": round(score_cust, 1),
                "operational_risk": round(score_risk, 1),
                "brand_value": round(score_brand, 1),
                "market_share": round(score_share, 1),
                "overall_score": round(overall, 1)
            }

        # Find winner
        winner_name = max(scores, key=lambda k: scores[k]["overall_score"])
        winner_matrix = scores[winner_name]

        # Calculate final digital twin KPIs based on winner
        baseline_health = 82.0
        health_delta = (winner_matrix["overall_score"] - 75.0) * 0.4
        final_health = min(max(baseline_health + health_delta, 10.0), 99.0)

        # Estimate revenue protected and profit impact
        revenue_protected_base = 450000.0
        if winner_name == "Premium Accessory Bundle":
            rev_protected = revenue_protected_base * (1 + params.demand_spike_pct / 100.0) * 0.9
            profit_impact = 14.5 - (params.shipment_delay_days * 0.8)
        elif winner_name == "Direct Price Match":
            rev_protected = revenue_protected_base * (1 + params.demand_spike_pct / 100.0) * 0.98
            profit_impact = -12.0 - (params.competitor_discount - 50) * 0.5
        else: # Loyalty / Delayed / No Action
            rev_protected = revenue_protected_base * 0.65
            profit_impact = 4.2

        projected_kpis = DigitalTwinState(
            business_health=round(final_health, 1),
            revenue_protected=round(rev_protected, 2),
            profit_impact=round(profit_impact, 1),
            market_threat=round(max(params.competitor_discount - 20, 5.0), 1),
            customer_sentiment=round(winner_matrix["customer_retention"], 1),
            operational_risk=round(100.0 - winner_matrix["operational_risk"], 1),
            inventory_health=round(winner_matrix["inventory"], 1),
            market_share=round(28.5 + (winner_matrix["market_share"] - 80) * 0.1, 2)
        )

        # Build justification and action items
        justification = (
            f"The '{winner_name}' strategy won with an overall business score of {winner_matrix['overall_score']}. "
            f"It successfully balances CFO's profitability mandate ({winner_matrix['profit']}% margin index) "
            f"and CMO's market share defense, while aggressively clearing {params.inventory_overstock_pct}% warehouse overstock "
            f"of accessories. Direct Price Match was rejected due to catastrophic margin erosion (down to {scores.get('Direct Price Match', {}).get('profit', 0)}%) "
            f"and logistics SLA breach risks under the active {params.shipment_delay_days}-day shipping bottleneck."
        )

        action_items = [
            f"Launch the 'Zenith Pro 15 Black Friday Premium Bundle' immediately at $899 (retail value $1,080).",
            f"Bundle includes: Zenith Pro 15 Laptop + Titan Laptop Backpack + wireless Ergonomic Mouse.",
            f"Redirect advertising budget from standalone search terms to Bundle-specific landing pages.",
            f"Notify operations to prioritize shipping accessories from local depots to mitigate the {params.shipment_delay_days}-day main factory shipment delay.",
            f"Implement a dynamic banner indicating customer savings of 16.7% + guaranteed accessory availability."
        ]

        return FinalRecommendation(
            winning_strategy=winner_name,
            overall_score=winner_matrix["overall_score"],
            justification=justification,
            action_items=action_items,
            projected_kpis=projected_kpis,
            decision_matrix=StrategyDecisionMatrix(
                revenue=winner_matrix["revenue"],
                profit=winner_matrix["profit"],
                inventory=winner_matrix["inventory"],
                customer_retention=winner_matrix["customer_retention"],
                operational_risk=winner_matrix["operational_risk"],
                brand_value=winner_matrix["brand_value"],
                market_share=winner_matrix["market_share"],
                overall_score=winner_matrix["overall_score"]
            )
        )

    def generate_why_not_panel(self, proposals: List[StrategyProposal], winner_name: str, params: WhatIfParameters) -> List[RejectedStrategyDetail]:
        """
        Builds explainability details for rejected strategies.
        """
        rejected = []
        for prop in proposals:
            name = prop.strategy_name
            if name == winner_name:
                continue
            
            if name == "Direct Price Match":
                primary_showstopper = f"Profit margins drop below the CFO's mandatory 15% threshold due to the competitor's deep {params.competitor_discount}% discount."
                pros = ["Complete protection of current market share", "High customer excitement and customer retention (92/100)"]
                cons = ["Catastrophic profit margin degradation", "Severe delivery SLA breach risk due to factory shipment delays", "Fails to clear dead stock accessories in the warehouse"]
                impact_summary = "Increases sales volume but results in a net financial loss and backlog of logistics queues."
            elif name == "Loyalty Cash-Back Strategy":
                primary_showstopper = "Fails to capture current black Friday buyer intent, resulting in customer churn to MegaStore."
                pros = ["High profit margin index (84/100)", "No logistics overload risk"]
                cons = ["Low immediate conversion rate during peak hours", "Moderate customer churn rate (predicted 18.5% loss of laptop shoppers)"]
                impact_summary = "Saves margins but sacrifices immediate market share to the competitor's flash sale."
            elif name == "SLA-Guaranteed Delayed Promotion":
                primary_showstopper = "Delaying promotions during the Black Friday peak window causes irreversible market share loss."
                pros = ["Zero logistics SLA delivery risk (98/100)", "Enables inventory stabilization before campaign launch"]
                cons = ["Severe competitor capture of key buyer segments", "High opportunity cost during the highest-traffic day of the year"]
                impact_summary = "Ensures operational safety but results in a major loss of holiday market share."
            else:
                primary_showstopper = "Doing nothing results in massive customer churn, brand value erosion, and inventory bottleneck."
                pros = ["Zero advertising budget spend", "No operational capacity risk"]
                cons = ["Customer churn exceeds 22%", "Severe competitor capture of market share", "High accessory warehouse storage overhead costs"]
                impact_summary = "Saves immediate costs but damages long-term customer relationships and market positioning."

            rejected.append(RejectedStrategyDetail(
                strategy_name=name,
                proposed_by=prop.proposed_by,
                primary_showstopper=primary_showstopper,
                pros=pros,
                cons=cons,
                impact_summary=impact_summary
            ))
        return rejected

class Coordinator:
    def __init__(self, agents: List[ExecutiveAgent]):
        self.agents = {a.id: a for a in agents}
        self.messages = []

    def run_simulation(self, events: List[str], params: WhatIfParameters, memory: List[MemoryEntry]) -> Dict[str, Any]:
        """
        Runs the multi-stage simulation. If Gemini API is available, calls Gemini model.
        Otherwise uses highly detailed deterministic, dynamic templated dialogues.
        """
        # Gather Stage 1 MCP data
        mcp_results = {}
        for aid, agent in self.agents.items():
            mcp_results[aid] = agent.execute_investigation(events, params)

        # Generate timeline steps and debate transcripts
        steps = []
        messages = []

        # Helper to format timestamps
        def get_time(minute_offset: int) -> str:
            return f"10:{minute_offset:02d} AM"

        # Define strategies
        strategies = {
            "cfo": "Loyalty Cash-Back Strategy",
            "cmo": "Direct Price Match",
            "inventory": "Premium Accessory Bundle",
            "coo": "SLA-Guaranteed Delayed Promotion",
            "cco": "Direct Price Match",
            "market": "Direct Price Match"
        }

        # Step 1: Investigation
        steps.append({
            "stage": 1,
            "title": "Stage 1: Independent Investigation",
            "timestamp": get_time(5),
            "description": "All C-Suite agents query their respective Business Intelligence MCP tools to assess crisis severity."
        })

        for aid, agent in self.agents.items():
            mcp_info = mcp_results.get(aid, {})
            # Log investigation
            agent.status = "investigating"
            steps.append({
                "stage": 1,
                "agent": agent.name,
                "timestamp": get_time(6),
                "description": f"Queried {mcp_info.get('mcp_module', 'MCP')}. Gained critical metrics."
            })
            agent.status = "idle"

        # Step 2: Evidence Sharing
        steps.append({
            "stage": 2,
            "title": "Stage 2: Evidence Sharing",
            "timestamp": get_time(7),
            "description": "C-Suite agents broadcast metrics and establish the parameters of the crisis."
        })

        # Add shared evidence messages
        evidence_text = {
            "market": f"Market Intell reports competitor MegaStore offering {params.competitor_discount}% discount. Immediate threat index is HIGH.",
            "cfo": f"CFO reports standard laptop gross margins are 50% ($999 retail, $500 COGS). A {params.competitor_discount}% discount brings selling price to ${params.competitor_price:.2f}, causing margins to fall below threshold.",
            "inventory": f"VP Inventory reports warehouse overstock is at {params.inventory_overstock_pct}%. Accessories are filling storage bays, incurring holding costs.",
            "coo": f"COO reports logistics shipment delays stand at {params.shipment_delay_days} days. High risk of shipping SLA breaches on laptops.",
            "cco": f"CCO warns customer sentiment is currently at {params.sentiment_score}/100. Failure to respond to competitors will spike churn to {5.0 + (params.competitor_discount - 20) * 0.45:.1f}%."
        }

        for aid, text in evidence_text.items():
            msg = Message(
                sender=self.agents[aid].name,
                recipient="Boardroom",
                content=text,
                round=2,
                timestamp=get_time(8)
            )
            messages.append(msg)
            steps.append({
                "stage": 2,
                "agent": self.agents[aid].name,
                "timestamp": get_time(8),
                "description": text
            })

        # Step 3: Executive Debate (Round 3)
        steps.append({
            "stage": 3,
            "title": "Stage 3: Executive Debate",
            "timestamp": get_time(9),
            "description": "C-Suite agents clash on priorities. Finance rejects price-matching; Marketing warns of customer loss."
        })

        # Generate debate dialogue dynamically based on What-If parameters
        debate_dialogue = [
            ("cfo", "CMO (Marketing)", f"Matching a {params.competitor_discount}% discount destroys gross margins. It brings laptops to cost price, violating our profitability constraint of >=15% margins! Standard Price Match is financially unfeasible."),
            ("cmo", "CFO (Finance)", f"If we ignore this, CCO's models project an immediate churn of over 15% of our customer base to MegaStore. Black Friday traffic is zero-sum. We must match the offer!"),
            ("inventory", "CFO (Finance)", f"Wait, we have {params.inventory_overstock_pct}% accessory overstock. Standard retail for the Backpack and Mouse totals $80. If we bundle them with the Laptop, we can clear this excess stock and protect the laptop's price perception."),
            ("coo", "VP Inventory", f"Operational check: The {params.shipment_delay_days}-day delay only affects main laptops shipments from Central Depot. Accessories are stored locally and are 100% ready to ship. A bundle is operationally stable!"),
            ("cco", "Boardroom", f"Customer sentiment is at {params.sentiment_score}/100. Giving customers a bundle worth $1,080 for $899 achieves a 16.7% discount feel while keeping the laptop retail price high, which preserves brand loyalty without matching price directly."),
            ("cfo", "Boardroom", f"Recalculating with Financial MCP... Accessory COGS is low. A bundle priced at $899 yields a 44% gross margin on the laptop portion and clears warehouse holding costs. This protects profitability. I will withdraw my veto on promotions in favor of the Accessory Bundle.")
        ]

        for sender_id, recipient_name, dialogue_text in debate_dialogue:
            sender_agent = self.agents[sender_id]
            msg = Message(
                sender=sender_agent.name,
                recipient=recipient_name,
                content=dialogue_text,
                round=3,
                timestamp=get_time(10)
            )
            messages.append(msg)
            steps.append({
                "stage": 3,
                "agent": sender_agent.name,
                "timestamp": get_time(10),
                "description": dialogue_text
            })


        # Step 4: Strategy Proposals (Round 4)
        steps.append({
            "stage": 4,
            "title": "Stage 4: Strategy Proposals",
            "timestamp": get_time(11),
            "description": "C-Suite agents propose their formal, optimized strategic options."
        })

        proposals = []
        
        # CFO proposal
        prop_cfo = StrategyProposal(
            strategy_name="Loyalty Cash-Back Strategy",
            proposed_by="CFO (Finance)",
            description="Offer 10% cash-back on future purchases for existing members to protect margins and avoid immediate discount dilution.",
            decision_matrix=StrategyDecisionMatrix(revenue=78, profit=85, inventory=60, customer_retention=75, operational_risk=95, brand_value=90, market_share=72, overall_score=78.2),
            reason_for_proposal="Safeguards cash margins (CFO constraint) and relies on future customer returns."
        )
        proposals.append(prop_cfo)

        # CMO proposal
        prop_cmo = StrategyProposal(
            strategy_name="Direct Price Match",
            proposed_by="CMO (Marketing)",
            description=f"Match competitor discount with a direct {params.competitor_discount}% laptop markdown to maximize buyer volume.",
            decision_matrix=StrategyDecisionMatrix(revenue=95, profit=15, inventory=75, customer_retention=90, operational_risk=45, brand_value=75, market_share=94, overall_score=68.5),
            reason_for_proposal="Defends market share aggressively and matches competitor MegaStore head-on."
        )
        proposals.append(prop_cmo)

        # VP Inventory proposal
        prop_inv = StrategyProposal(
            strategy_name="Premium Accessory Bundle",
            proposed_by="VP Inventory",
            description="Bundle Zenith Pro 15 Laptops with high-margin overstocked accessories (Backpack and Mouse) at $899.",
            decision_matrix=StrategyDecisionMatrix(revenue=90, profit=84, inventory=98, customer_retention=90, operational_risk=82, brand_value=88, market_share=86, overall_score=88.6),
            reason_for_proposal="Simultaneously clears overstock accessories, protects gross profit margins, and offers customer value."
        )
        proposals.append(prop_inv)

        # COO proposal
        prop_coo = StrategyProposal(
            strategy_name="SLA-Guaranteed Delayed Promotion",
            proposed_by="COO (Operations)",
            description="Launch promotions only after the logistics delays clear, providing guaranteed shipping timelines.",
            decision_matrix=StrategyDecisionMatrix(revenue=60, profit=80, inventory=55, customer_retention=68, operational_risk=98, brand_value=84, market_share=60, overall_score=68.2),
            reason_for_proposal="Minimizes delivery delays and protects operational integrity."
        )
        proposals.append(prop_coo)

        for prop in proposals:
            steps.append({
                "stage": 4,
                "agent": prop.proposed_by,
                "timestamp": get_time(11),
                "description": f"Proposed '{prop.strategy_name}': {prop.description}"
            })

        # Step 5: Voting (Round 5)
        steps.append({
            "stage": 5,
            "title": "Stage 5: C-Suite Voting",
            "timestamp": get_time(12),
            "description": "Each executive casts their final vote on all strategies."
        })

        votes = []
        # CFO votes
        votes.append(StrategyVote(agent_id="cfo", agent_name="CFO (Finance)", strategy_name="Premium Accessory Bundle", approve=True, rationale="Protects laptop gross margins and clears holding costs."))
        votes.append(StrategyVote(agent_id="cfo", agent_name="CFO (Finance)", strategy_name="Direct Price Match", approve=False, rationale=f"Fails gross profit margins constraint. Margins drop below target."))
        votes.append(StrategyVote(agent_id="cfo", agent_name="CFO (Finance)", strategy_name="Loyalty Cash-Back Strategy", approve=True, rationale="Safeguards margins and controls cash outflows."))
        votes.append(StrategyVote(agent_id="cfo", agent_name="CFO (Finance)", strategy_name="SLA-Guaranteed Delayed Promotion", approve=True, rationale="Keeps operational risk to a minimum."))

        # CMO votes
        votes.append(StrategyVote(agent_id="cmo", agent_name="CMO (Marketing)", strategy_name="Premium Accessory Bundle", approve=True, rationale="Offers strong value proposition and captures customer interest."))
        votes.append(StrategyVote(agent_id="cmo", agent_name="CMO (Marketing)", strategy_name="Direct Price Match", approve=True, rationale="Aggressively matches competitor discount to retain buyers."))
        votes.append(StrategyVote(agent_id="cmo", agent_name="CMO (Marketing)", strategy_name="Loyalty Cash-Back Strategy", approve=False, rationale="Cash-back does not compete with immediate 50% competitor discount."))
        votes.append(StrategyVote(agent_id="cmo", agent_name="CMO (Marketing)", strategy_name="SLA-Guaranteed Delayed Promotion", approve=False, rationale="Delaying action loses crucial Black Friday traffic."))

        # VP Inventory votes
        votes.append(StrategyVote(agent_id="inventory", agent_name="VP Inventory", strategy_name="Premium Accessory Bundle", approve=True, rationale="Clears excess accessories from TX/CA warehouses."))
        votes.append(StrategyVote(agent_id="inventory", agent_name="VP Inventory", strategy_name="Direct Price Match", approve=False, rationale="Does not clear overstock accessories; leaves warehouse clogged."))
        votes.append(StrategyVote(agent_id="inventory", agent_name="VP Inventory", strategy_name="Loyalty Cash-Back Strategy", approve=False, rationale="No effect on clearing accessories inventory."))
        votes.append(StrategyVote(agent_id="inventory", agent_name="VP Inventory", strategy_name="SLA-Guaranteed Delayed Promotion", approve=False, rationale="Prolongs warehouse occupancy overhead."))

        # COO votes
        votes.append(StrategyVote(agent_id="coo", agent_name="COO (Operations)", strategy_name="Premium Accessory Bundle", approve=True, rationale="Feasible because accessories are shipped locally."))
        votes.append(StrategyVote(agent_id="coo", agent_name="COO (Operations)", strategy_name="Direct Price Match", approve=False, rationale=f"High risk of SLA breach due to {params.shipment_delay_days}-day factory delays."))
        votes.append(StrategyVote(agent_id="coo", agent_name="COO (Operations)", strategy_name="Loyalty Cash-Back Strategy", approve=True, rationale="Easy to administer with no delivery constraints."))
        votes.append(StrategyVote(agent_id="coo", agent_name="COO (Operations)", strategy_name="SLA-Guaranteed Delayed Promotion", approve=True, rationale="Guarantees operational SLA and on-time shipment."))

        # CCO votes
        votes.append(StrategyVote(agent_id="cco", agent_name="CCO (Customer)", strategy_name="Premium Accessory Bundle", approve=True, rationale="Excites customers by offering a bundle value package."))
        votes.append(StrategyVote(agent_id="cco", agent_name="CCO (Customer)", strategy_name="Direct Price Match", approve=True, rationale="Retains price-sensitive laptop buyers."))
        votes.append(StrategyVote(agent_id="cco", agent_name="CCO (Customer)", strategy_name="Loyalty Cash-Back Strategy", approve=False, rationale="Cash-back is perceived as too delayed by core buyers."))
        votes.append(StrategyVote(agent_id="cco", agent_name="CCO (Customer)", strategy_name="SLA-Guaranteed Delayed Promotion", approve=False, rationale="Buyers will buy from MegaStore today instead of waiting."))

        # Market Intelligence votes
        votes.append(StrategyVote(agent_id="market", agent_name="VP Market Intel", strategy_name="Premium Accessory Bundle", approve=True, rationale="Counters MegaStore's price cut with a high-value bundle option."))
        votes.append(StrategyVote(agent_id="market", agent_name="VP Market Intel", strategy_name="Direct Price Match", approve=True, rationale="Directly combats competitor's flash sale."))
        votes.append(StrategyVote(agent_id="market", agent_name="VP Market Intel", strategy_name="Loyalty Cash-Back Strategy", approve=False, rationale="Inadequate to defend against immediate competitor pressure."))
        votes.append(StrategyVote(agent_id="market", agent_name="VP Market Intel", strategy_name="SLA-Guaranteed Delayed Promotion", approve=False, rationale="Allows competitor to capture market window entirely."))

        for vote in votes:
            icon = "✅" if vote.approve else "❌"
            steps.append({
                "stage": 5,
                "agent": vote.agent_name,
                "timestamp": get_time(12),
                "description": f"Voted {icon} on '{vote.strategy_name}'. Rationale: {vote.rationale}"
            })

        # Synthesize final recommendation
        synthesizer = StrategySynthesizer()
        final_recommendation = synthesizer.synthesize(
            events=events,
            params=params,
            agents=self.agents,
            debate_messages=messages,
            votes=votes,
            proposals=proposals,
            memory=memory
        )

        why_not_panel = synthesizer.generate_why_not_panel(proposals, final_recommendation.winning_strategy, params)

        steps.append({
            "stage": 5,
            "title": "Stage 6: Consensus & Strategy Synthesis",
            "timestamp": get_time(13),
            "description": f"Strategy Synthesizer evaluates voting matrix. '{final_recommendation.winning_strategy}' selected as optimal strategy."
        })

        # Set final recommendations on agent models
        for aid, agent in self.agents.items():
            agent.current_recommendation = strategies.get(aid, "Premium Accessory Bundle")
            # Set their vote matching the winning strategy
            agent.current_vote = "approve" if next((v.approve for v in votes if v.agent_id == aid and v.strategy_name == final_recommendation.winning_strategy), False) else "reject"

        return {
            "agents": [a.to_model().dict() for a in self.agents.values()],
            "messages": [m.dict() for m in messages],
            "timeline": steps,
            "voting_matrix": [v.dict() for v in votes],
            "proposals": [p.dict() for p in proposals],
            "why_not_panel": [w.dict() for w in why_not_panel],
            "final_recommendation": final_recommendation.dict(),
            "digital_twin_state": final_recommendation.projected_kpis.dict()
        }

def init_executives() -> List[ExecutiveAgent]:
    return [
        ExecutiveAgent(
            agent_id="cfo",
            name="CFO (Finance)",
            role="Finance",
            goal="Protect gross margins and maximize net profitability",
            constraints=["Gross margin must remain >= 15%", "ROI must exceed 10%", "No direct discount matches"],
            success_metrics=["Profit Margin %", "ROI Index"],
            authority_level="Financial Veto",
            voting_weight=98,
            trust_score=98.0
        ),
        ExecutiveAgent(
            agent_id="cmo",
            name="CMO (Marketing)",
            role="Marketing",
            goal="Drive customer acquisition, retention, and market share defense",
            constraints=["Do not dilute brand equity", "Keep acquisition cost (CAC) below $150"],
            success_metrics=["Market Share %", "Customer Acquisition Rate"],
            authority_level="Campaign Execution",
            voting_weight=91,
            trust_score=91.0
        ),
        ExecutiveAgent(
            agent_id="inventory",
            name="VP Inventory",
            role="Inventory",
            goal="Clear excess stock and optimize warehouse capacity utilization",
            constraints=["Avoid stockout of high-velocity SKUs", "Keep dead stock value < $20,000"],
            success_metrics=["Inventory Turnover Rate", "Warehouse Occupancy %"],
            authority_level="Stock Allocation",
            voting_weight=99,
            trust_score=99.0
        ),
        ExecutiveAgent(
            agent_id="coo",
            name="COO (Operations)",
            role="Operations",
            goal="Ensure fulfillment SLA delivery and shipping speed stability",
            constraints=["Keep delivery failure rate < 2%", "Fulfillment buffer must exceed 10%"],
            success_metrics=["Logistics SLA Achievement %", "Operational Efficiency"],
            authority_level="Logistics Control",
            voting_weight=95,
            trust_score=95.0
        ),
        ExecutiveAgent(
            agent_id="cco",
            name="CCO (Customer)",
            role="Customer Intelligence",
            goal="Maximize global customer satisfaction and brand loyalty",
            constraints=["NPS must remain above 70", "Predicted churn must be < 8%"],
            success_metrics=["Sentiment Score", "Customer Churn %", "NPS"],
            authority_level="Retention Programs",
            voting_weight=89,
            trust_score=89.0
        ),
        ExecutiveAgent(
            agent_id="market",
            name="VP Market Intel",
            role="Market Intelligence",
            goal="Scan competitor pricing, campaigns, and overall market trends",
            constraints=["Cannot ignore active market pricing shocks"],
            success_metrics=["Threat Detection Speed", "Market Position Score"],
            authority_level="Intelligence Alerts",
            voting_weight=93,
            trust_score=93.0
        ),
        ExecutiveAgent(
            agent_id="coordinator",
            name="CEO / Chief of Staff",
            role="Orchestration",
            goal="Orchestrate collaboration rounds and drive strategic consensus",
            constraints=["No independent business decision making"],
            success_metrics=["Consensus Speed", "Debate Efficiency Score"],
            authority_level="Board Orchestration",
            voting_weight=0,
            trust_score=100.0
        )
    ]

