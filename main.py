"""
ScamGuard-Z FastAPI Application
IBM Z Datathon 2026 - Real-Time AI for Critical Decisions
Runs natively on IBM LinuxONE (s390x)
"""

import platform
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from risk_engine import evaluate_transaction

app = FastAPI(
    title="ScamGuard-Z API",
    description="Real-Time In-Transaction AI Defense Against Coercion & Social Engineering Scams (IBM Z / LinuxONE)",
    version="1.0.0"
)

# Enable CORS for simulation clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class TransactionRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Transfer amount requested", example=4500.0)
    avg_amount: float = Field(..., gt=0, description="User's historical 30-day average transaction amount", example=1000.0)
    recipient_name: str = Field(..., min_length=1, description="Payee beneficiary name", example="Escrow Legal Clearance Vault")
    recipient_age_hours: float = Field(..., ge=0, description="Hours since payee was added to account", example=2.0)
    prior_transfers: int = Field(..., ge=0, description="Number of prior completed transfers to payee", example=0)
    transfers_today: int = Field(..., ge=0, description="Outbound transfer frequency today", example=1)
    account_balance: float = Field(..., gt=0, description="Available balance prior to transfer", example=5000.0)

@app.get("/")
def serve_ui():
    """Serves the interactive web simulation interface."""
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "ScamGuard-Z API is active on LinuxONE. Visit /docs for Swagger API documentation."}

@app.post("/api/evaluate")
def evaluate_tx(tx: TransactionRequest):
    """
    Evaluates a transaction payload and returns:
    - Composite risk score (0-100)
    - Risk Tier (LOW, MEDIUM, HIGH)
    - Itemized explanation factor cards
    - Educational intervention modal details (for High/Medium risk)
    """
    try:
        result = evaluate_transaction(
            amount=tx.amount,
            avg_amount=tx.avg_amount,
            recipient_name=tx.recipient_name,
            recipient_age_hours=tx.recipient_age_hours,
            prior_transfers=tx.prior_transfers,
            transfers_today=tx.transfers_today,
            account_balance=tx.account_balance
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/system-info")
def system_info():
    """Returns host platform details proving deployment on s390x."""
    return {
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "system": platform.system(),
        "release": platform.release(),
        "python_version": platform.python_version(),
        "is_ibm_z": platform.machine() == "s390x",
        "service_status": "ONLINE",
        "datacenter": "IBM LinuxONE Community Cloud (Marist College)"
    }

@app.get("/api/scenarios")
def get_preset_scenarios():
    """Predefined scenarios for live judge and evaluator testing."""
    return [
        {
            "id": "scenario_normal",
            "name": "1. Routine Grocery / Utility Transfer",
            "description": "Standard recurring payment to established utility or grocery merchant.",
            "data": {
                "amount": 75.0,
                "avg_amount": 80.0,
                "recipient_name": "State Electric Utility",
                "recipient_age_hours": 720.0,
                "prior_transfers": 12,
                "transfers_today": 0,
                "account_balance": 3200.0
            },
            "expected_tier": "LOW",
            "expected_score_range": "0 - 15"
        },
        {
            "id": "scenario_borderline",
            "name": "2. Legitimate High-Value Purchase (Car Repair / Furniture)",
            "description": "High-value transfer to a business, but account is not wiped out and frequency is normal.",
            "data": {
                "amount": 750.0,
                "avg_amount": 200.0,
                "recipient_name": "Metro Auto Body Services",
                "recipient_age_hours": 48.0,
                "prior_transfers": 1,
                "transfers_today": 1,
                "account_balance": 6500.0
            },
            "expected_tier": "MEDIUM",
            "expected_score_range": "40 - 65"
        },
        {
            "id": "scenario_coercion",
            "name": "3. Urgent Coercion Scam ('Digital Arrest' / Authority Impersonation)",
            "description": "Victim pressured by fake police caller into wiring 90% of life savings to new 'clearance vault'.",
            "data": {
                "amount": 4500.0,
                "avg_amount": 1000.0,
                "recipient_name": "Central Police Escrow Acct 902",
                "recipient_age_hours": 2.0,
                "prior_transfers": 0,
                "transfers_today": 1,
                "account_balance": 5000.0
            },
            "expected_tier": "HIGH",
            "expected_score_range": "70 - 100"
        }
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
