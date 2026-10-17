"""
ScamGuard-Z Risk Scoring Engine
Implements the exact weighted formula for the IBM Z Datathon 2026:
    Risk Score = 30 * S_amt + 25 * S_recip + 25 * S_vel + 20 * S_dep
where S_i in [0.0, 1.0] and weights sum to 100.
"""

from typing import Dict, Any, List

def calculate_amount_factor(amount: float, avg_amount: float) -> tuple[float, str]:
    """Calculates S_amt in [0.0, 1.0] comparing amount to historical average."""
    if avg_amount <= 0:
        avg_amount = 100.0  # fallback baseline
    
    ratio = amount / avg_amount
    if ratio <= 1.0:
        score = 0.0
        explanation = f"Transfer (${amount:,.2f}) is consistent with your 30-day historical average (${avg_amount:,.2f})."
    elif ratio >= 4.0:
        score = 1.0
        explanation = f"Atypical transfer amount: ${amount:,.2f} is {ratio:.1f}x higher than your historical average (${avg_amount:,.2f})."
    else:
        score = (ratio - 1.0) / 3.0
        explanation = f"Moderately elevated transfer amount: ${amount:,.2f} is {ratio:.1f}x your historical average."
    
    return min(1.0, max(0.0, score)), explanation


def calculate_recipient_factor(recipient_age_hours: float, prior_transfers: int, recipient_name: str) -> tuple[float, str]:
    """Calculates S_recip in [0.0, 1.0] based on payee relationship and registration recency."""
    if prior_transfers > 0:
        score = 0.0
        explanation = f"Verified recipient: You have previously completed {prior_transfers} transfer(s) to '{recipient_name}'."
    elif recipient_age_hours < 24.0:
        score = 1.0
        explanation = f"Unfamiliar recipient: '{recipient_name}' was added only {recipient_age_hours:.1f} hour(s) ago with zero prior payment history."
    elif recipient_age_hours < 72.0:
        score = 0.5
        explanation = f"Recent recipient: '{recipient_name}' was added {recipient_age_hours:.1f} hours ago with no prior payment history."
    else:
        score = 0.2
        explanation = f"Established recipient '{recipient_name}' with no recorded transfers in the last 30 days."
    
    return min(1.0, max(0.0, score)), explanation


def calculate_velocity_factor(transfers_today: int) -> tuple[float, str]:
    """Calculates S_vel in [0.0, 1.0] based on transfer frequency in the last 24 hours."""
    if transfers_today <= 1:
        score = 0.0
        explanation = f"Normal transfer frequency: {transfers_today} outbound transfer(s) executed today."
    elif transfers_today == 2:
        score = 0.4
        explanation = f"Slightly elevated frequency: {transfers_today} outbound transfers executed within 24 hours."
    elif transfers_today == 3:
        score = 0.7
        explanation = f"High transfer velocity: 3 outbound transfers executed in rapid succession today."
    else:
        score = 1.0
        explanation = f"Atypical transfer velocity: {transfers_today} outbound transfers executed today, indicative of rapid liquidation patterns."
    
    return min(1.0, max(0.0, score)), explanation


def calculate_depletion_factor(amount: float, balance: float) -> tuple[float, str]:
    """Calculates S_dep in [0.0, 1.0] representing percentage of total account balance liquidated."""
    if balance <= 0:
        return 1.0, "Account balance is zero or negative."
    
    ratio = amount / balance
    percentage = ratio * 100.0
    
    if ratio < 0.25:
        score = 0.0
        explanation = f"Safe liquidity ratio: Transfer represents {percentage:.1f}% of your available balance (${balance:,.2f})."
    elif ratio >= 0.80:
        score = 1.0
        explanation = f"Severe balance depletion: Transfer liquidates {percentage:.1f}% of your entire available balance (${balance:,.2f})."
    else:
        score = (ratio - 0.25) / 0.55
        explanation = f"Moderate balance depletion: Transfer liquidates {percentage:.1f}% of your available balance."
    
    return min(1.0, max(0.0, score)), explanation


def evaluate_transaction(
    amount: float,
    avg_amount: float,
    recipient_name: str,
    recipient_age_hours: float,
    prior_transfers: int,
    transfers_today: int,
    account_balance: float
) -> Dict[str, Any]:
    """
    Main evaluation pipeline.
    Calculates composite score, maps to risk tiers (Low, Medium, High),
    and returns itemized factor cards and safety advice.
    """
    # 1. Compute normalized factor scores (0.0 to 1.0)
    s_amt, exp_amt = calculate_amount_factor(amount, avg_amount)
    s_recip, exp_recip = calculate_recipient_factor(recipient_age_hours, prior_transfers, recipient_name)
    s_vel, exp_vel = calculate_velocity_factor(transfers_today)
    s_dep, exp_dep = calculate_depletion_factor(amount, account_balance)
    
    # 2. Compute weighted points (Weights: 30, 25, 25, 20 = 100)
    pts_amt = round(30.0 * s_amt, 1)
    pts_recip = round(25.0 * s_recip, 1)
    pts_vel = round(25.0 * s_vel, 1)
    pts_dep = round(20.0 * s_dep, 1)
    
    total_score = round(pts_amt + pts_recip + pts_vel + pts_dep, 1)
    total_score = min(100.0, max(0.0, total_score))
    
    # 3. Classify Risk Tier
    if total_score < 40.0:
        risk_tier = "LOW"
        tier_color = "success"
        action_summary = "Transaction appears consistent with routine account activity. Standard proceed allowed."
    elif total_score < 70.0:
        risk_tier = "MEDIUM"
        tier_color = "warning"
        action_summary = "Advisory: Some transaction parameters deviate from historical patterns. Please verify recipient details before sending."
    else:
        risk_tier = "HIGH"
        tier_color = "danger"
        action_summary = "CRITICAL SAFETY HOLD: Multiple high-risk coercion and social-engineering markers detected. Please pause and verify."
    
    # 4. Itemized Factor Breakdown Cards
    factors = [
        {
            "factor_name": "Atypical Transfer Amount",
            "weight_max": 30,
            "score_norm": round(s_amt, 2),
            "points_contributed": pts_amt,
            "explanation": exp_amt,
            "is_risk": s_amt > 0.3
        },
        {
            "factor_name": "Unfamiliar Recipient",
            "weight_max": 25,
            "score_norm": round(s_recip, 2),
            "points_contributed": pts_recip,
            "explanation": exp_recip,
            "is_risk": s_recip > 0.3
        },
        {
            "factor_name": "Transfer Velocity (Frequency)",
            "weight_max": 25,
            "score_norm": round(s_vel, 2),
            "points_contributed": pts_vel,
            "explanation": exp_vel,
            "is_risk": s_vel > 0.3
        },
        {
            "factor_name": "Account Balance Depletion",
            "weight_max": 20,
            "score_norm": round(s_dep, 2),
            "points_contributed": pts_dep,
            "explanation": exp_dep,
            "is_risk": s_dep > 0.3
        }
    ]
    
    # 5. Safety Warning / Intervention Content (for High & Medium risk)
    intervention = None
    if risk_tier == "HIGH":
        intervention = {
            "title": "🚨 Potential Coercion / Impersonation Scam Detected",
            "message": "This transfer matches known behavioral patterns of telephone fraud, 'digital arrest', and authority impersonation scams.",
            "verification_questions": [
                "Are you currently on an active telephone or video call with someone directing you to send these funds?",
                "Did a caller claim to be from law enforcement (Police/CBI/Interpol), tax authorities, or bank fraud security?",
                "Were you told that this transfer is an 'urgent verification', 'safe locker deposit', or 'confidential legal clearance'?"
            ],
            "practical_steps": [
                "1. HANG UP IMMEDIATELY. Legitimate police, tax, and bank officers will never demand urgent wire transfers over the phone.",
                "2. Call your bank using the official phone number printed on the back of your debit card.",
                "3. Speak to a trusted family member, colleague, or friend before transferring any money."
            ],
            "recommended_action": "PAUSE_AND_VERIFY"
        }
    elif risk_tier == "MEDIUM":
        intervention = {
            "title": "⚠️ Caution: Unusual Transfer Characteristics",
            "message": "This payment involves an elevated amount or recent payee. Double-check recipient account numbers before confirming.",
            "verification_questions": [
                "Have you confirmed the recipient's identity through a separate, trusted channel?"
            ],
            "practical_steps": [
                "Double-check payee account number and routing information."
            ],
            "recommended_action": "REVIEW_DETAILS"
        }
    
    return {
        "risk_score": total_score,
        "risk_tier": risk_tier,
        "tier_color": tier_color,
        "action_summary": action_summary,
        "formula_used": "Risk Score = 30 * S_amt + 25 * S_recip + 25 * S_vel + 20 * S_dep",
        "factor_breakdown": factors,
        "intervention": intervention,
        "evaluated_parameters": {
            "amount": amount,
            "avg_amount": avg_amount,
            "recipient_name": recipient_name,
            "recipient_age_hours": recipient_age_hours,
            "prior_transfers": prior_transfers,
            "transfers_today": transfers_today,
            "account_balance": account_balance
        }
    }
