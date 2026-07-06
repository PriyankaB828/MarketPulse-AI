import json
from typing import Dict, Any, List

def competitor_intelligence_mcp(competitor_discount: float, competitor_price: float) -> Dict[str, Any]:
    """
    Scrapes competitor pricing logs, active discount levels, and calculates market share threat.
    """
    threat_level = "HIGH" if competitor_discount >= 40 else "MEDIUM" if competitor_discount >= 20 else "LOW"
    return {
        "mcp_module": "Competitor Intelligence MCP",
        "competitor_name": "MegaStore",
        "active_campaign": "Black Friday Laptop Flash Sale",
        "competitor_price_usd": competitor_price,
        "competitor_discount_pct": competitor_discount,
        "market_threat_level": threat_level,
        "competitor_estimated_inventory": 1500,
        "estimated_traffic_loss_pct": round(competitor_discount * 0.8, 1)
    }

def customer_insight_mcp(sentiment_score: float, competitor_discount: float) -> Dict[str, Any]:
    """
    Crawls social media and customer support tickets to evaluate brand loyalty and churn threat.
    """
    estimated_churn = 5.0
    if competitor_discount > 30:
        # Increase churn if discount is high and company does not respond
        estimated_churn = round(5.0 + (competitor_discount - 20) * 0.45 * (100 - sentiment_score) / 50.0, 1)
    
    return {
        "mcp_module": "Customer Insight MCP",
        "global_sentiment_score": sentiment_score,
        "social_media_mention_volume": 4200,
        "sentiment_breakdown": {
            "positive_pct": round(sentiment_score * 0.6, 1),
            "neutral_pct": round(25 + sentiment_score * 0.1, 1),
            "negative_pct": round(100 - (sentiment_score * 0.6 + 25 + sentiment_score * 0.1), 1)
        },
        "customer_acquisition_cost_usd": 120.0,
        "brand_loyalty_index": round(sentiment_score / 10.0, 1),
        "predicted_churn_no_response_pct": estimated_churn
    }

def inventory_analytics_mcp(overstock_pct: float) -> Dict[str, Any]:
    """
    Queries the central warehouse inventory database for stock levels, shelf occupancy, and holding costs.
    """
    accessories_held = int(3000 + overstock_pct * 80)
    laptop_stock = 600
    return {
        "mcp_module": "Inventory Analytics MCP",
        "warehouse_locations": ["TX-East-1", "CA-West-2"],
        "critical_skus": {
            "LAPTOP-SKU-A": {
                "name": "Zenith Pro 15",
                "in_stock": laptop_stock,
                "monthly_velocity": 450,
                "holding_cost_per_unit_monthly": 15.0
            },
            "ACC-BAG-01": {
                "name": "Titan Laptop Backpack",
                "in_stock": accessories_held,
                "monthly_velocity": 120,
                "holding_cost_per_unit_monthly": 2.5
            },
            "ACC-MOUSE-02": {
                "name": "Aero wireless Ergonomic Mouse",
                "in_stock": accessories_held + 500,
                "monthly_velocity": 180,
                "holding_cost_per_unit_monthly": 1.2
            }
        },
        "overall_warehouse_capacity_occupancy_pct": round(50.0 + overstock_pct * 0.4, 1),
        "estimated_dead_stock_value_usd": round(accessories_held * 12.0 + (accessories_held + 500) * 8.0, 2)
    }

def financial_modeling_mcp(cogs_usd: float, sell_price_usd: float, discount_pct: float) -> Dict[str, Any]:
    """
    Computes profit margins, cost-of-goods-sold, ROI, and break-even points for promotions.
    """
    selling_price = sell_price_usd * (1 - discount_pct / 100.0)
    margin = (selling_price - cogs_usd) / sell_price_usd * 100.0 if sell_price_usd > 0 else 0.0
    return {
        "mcp_module": "Financial Modeling MCP",
        "baseline_cogs_usd": cogs_usd,
        "standard_retail_price_usd": sell_price_usd,
        "offered_discount_pct": discount_pct,
        "calculated_selling_price_usd": round(selling_price, 2),
        "gross_margin_usd": round(selling_price - cogs_usd, 2),
        "gross_margin_percentage": round(margin, 1),
        "roi_index": round((selling_price - cogs_usd) / cogs_usd, 2),
        "below_margin_threshold": margin < 15.0
    }

def marketing_optimization_mcp(demand_spike_pct: float) -> Dict[str, Any]:
    """
    Configures promotional bundles and evaluates historical performance data.
    """
    conversion_base = 2.4
    estimated_reach = int(120000 + demand_spike_pct * 3000)
    return {
        "mcp_module": "Marketing Optimization MCP",
        "proposed_bundles": [
            {
                "bundle_id": "BUNDLE-BF-01",
                "name": "Zenith Complete Premium Package",
                "items": ["LAPTOP-SKU-A", "ACC-BAG-01", "ACC-MOUSE-02"],
                "retail_price_sum_usd": 1080.0,
                "bundle_price_usd": 899.0,
                "implied_discount_pct": 16.7,
                "projected_conversion_rate_pct": round(conversion_base + demand_spike_pct * 0.08, 2)
            }
        ],
        "projected_campaign_reach": estimated_reach,
        "estimated_ad_cost_usd": 15000.0
    }

def supply_chain_intelligence_mcp(delay_days: int) -> Dict[str, Any]:
    """
    Accesses logistics trackers and monitors shipment timelines and delays.
    """
    sla_impact = "CRITICAL" if delay_days >= 5 else "WARNING" if delay_days >= 2 else "NORMAL"
    return {
        "mcp_module": "Supply Chain Intelligence MCP",
        "active_shipments_in_transit": 8,
        "shipment_delays_days": delay_days,
        "logistics_bottlenecks": ["Chicago Freight Hub (Delayed)", "LA Port (Normal)"],
        "sla_breach_risk_level": sla_impact,
        "re_routing_cost_per_unit_usd": round(delay_days * 18.5, 2),
        "carrier_on_time_performance_pct": max(98.5 - delay_days * 8.0, 40.0)
    }
