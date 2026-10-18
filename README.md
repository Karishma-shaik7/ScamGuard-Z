# ScamGuard-Z: Real-Time AI In-Transaction Coercion Shield

[![Platform](https://img.shields.io/badge/Platform-IBM%20LinuxONE%20%28s390x%29-0f62fe.svg)](https://community.ibm.com/zsystems/l1cc/)
[![Datathon](https://img.shields.io/badge/IBM%20Z%20Datathon-2026-001141.svg)](https://hack2skill.com/event/datathon-2026)
[![Theme](https://img.shields.io/badge/Theme-Real--Time%20AI%20for%20Critical%20Decisions-198038.svg)]()
[![Python](https://img.shields.io/badge/Python-3.12-3776ab.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)

> **IBM Z Datathon 2026 Submission**  
> **Challenge Track:** Real-Time AI for Critical Decisions  
> **Cross-Cutting Focus:** AI Secured: Innovation Without Exposure  
> **Target Architecture:** IBM Z / LinuxONE Community Cloud (`s390x`)  

---

## 🚨 Problem Statement

> *"Victims of social engineering scams may authorise fraudulent bank transfers themselves under pressure or deception. Traditional transaction checks may not identify these coercion-related risks, allowing victims to lose their savings."*

Over **$36 Billion** is lost annually worldwide to coercive telephone scams, authority impersonation ("digital arrest" scams), and synthetic family emergencies. Because victims enter their own valid credentials, passwords, and 2FA tokens while under duress on their personal devices, legacy banking fraud systems treat the payment as legitimate.

**ScamGuard-Z** introduces an explainable, in-transaction intelligence layer that evaluates observable payment anomalies in real time, computes an audit-ready risk score, and displays an educational safety warning encouraging users to pause and verify the recipient before irreversible fund movement occurs.

---

## 🛡️ Solution Architecture & How It Works

ScamGuard-Z deploys directly within the core payment pipeline on an **IBM LinuxONE (`s390x`)** mainframe instance:

```
[ Simulation Client UI (HTML5/CSS3/JS) ]
                  │
                  ▼  (JSON REST Request)
┌──────────────────────────────────────────────────────────┐
│     FastAPI Backend Service on IBM LinuxONE (s390x)      │
│                                                          │
│  ┌────────────────────┐      ┌────────────────────────┐  │
│  │ Feature Extractor  │ ───► │  Risk Scoring Engine   │  │
│  │ (Velocity, Ratios, │      │  (Weighted Formula)    │  │
│  │  Recipient Status) │      │  Outputs Score (0-100) │  │
│  └────────────────────┘      └───────────┬────────────┘  │
│                                          │               │
│                                          ▼               │
│                              ┌────────────────────────┐  │
│                              │  Reasoning Generator   │  │
│                              │ (Human-readable text)  │  │
│                              └────────────────────────┘  │
└─────────────────────────┬────────────────────────────────┘
                          │
                          ▼  (JSON Assessment Response)
┌──────────────────────────────────────────────────────────┐
│  Simulation Interface Action:                            │
│  • Low Risk (0-39)    ➔ Normal Proceed Confirmation      │
│  • Medium Risk (40-69) ➔ Informative Advisory Note       │
│  • High Risk (70-100) ➔ Emergency Safety Warning Modal   │
└──────────────────────────────────────────────────────────┘
```

---

## 🧮 Grounded Risk Scoring Formula

ScamGuard-Z calculates a composite score bounded between **0 and 100** using four normalized factor scores ($S_i \in [0.0, 1.0]$) and transparent integer weights totaling 100:

$$\text{Risk Score} = 30 \times S_{\text{amt}} + 25 \times S_{\text{recip}} + 25 \times S_{\text{vel}} + 20 \times S_{\text{dep}}$$

| Factor | Notation | Max Weight | Operational Risk Trigger |
| :--- | :---: | :---: | :--- |
| **Atypical Transfer Amount** | $S_{\text{amt}}$ | **30 pts** | Transfer value exceeds 3× to 5× user's 30-day historical average. |
| **Unfamiliar Recipient** | $S_{\text{recip}}$ | **25 pts** | Payee beneficiary registered within past 24 hours with zero history. |
| **Transfer Velocity** | $S_{\text{vel}}$ | **25 pts** | Multiple outbound payments executed in rapid succession within 24 hours. |
| **Account Depletion Ratio** | $S_{\text{dep}}$ | **20 pts** | Single transaction attempts to liquidate 75% to 95% of available balance. |

### Risk Tier Boundaries:
* **Low Risk (0–39):** Routine transaction characteristics; standard execution allowed.
* **Medium Risk (40–69):** Isolated deviation; advisory notice to double-check recipient details.
* **High Risk (70–100):** Multiple compounding indicators; triggers safety intervention modal with cognitive pause questions.

---

## 🖥️ Live IBM LinuxONE Mainframe Verification

The ScamGuard-Z prototype is actively deployed and verified on the **IBM LinuxONE Community Cloud**:

```bash
# Terminal output from live instance (148.100.78.36):
$ uname -a
Linux scamguardz2026 6.8.0-147-generic #147-Ubuntu SMP Thu Sep 24 10:59:43 UTC 2026 s390x s390x s390x GNU/Linux

$ uname -m
s390x
```

### Why IBM Z / LinuxONE is Essential:
1. **Mission-Critical Availability:** Banking transactions cannot tolerate downtime. IBM Z provides enterprise 99.999% uptime.
2. **Sub-Second In-Transaction Latency:** LinuxONE processes high-throughput transaction streams with near-zero latency, avoiding payment gateway bottlenecks.
3. **Pervasive Security & Privacy:** Evaluates transactions inside secure enterprise containers with strict data minimization on synthetic parameters.

---

## 📂 Project Structure

```text
scamguard-z/
├── risk_engine.ipynb           # Core deterministic scoring formula & factor explainers
├── generate_data.ipynb       # Synthetic dataset generator (600 test cases)
├── main.ipynb                  # FastAPI REST API running on LinuxONE (s390x)

├── static/
│   └── index.html           # Interactive web simulation console (IBM Carbon styling)
└── README.md                # Project documentation
```

---

## 🚀 Quickstart & Local Demonstration

### Option A: Running with Live Mainframe Backend
```bash
# Connect SSH tunnel to LinuxONE VM (port 8000)
ssh -i "ScamGuardTeamKey2026.pem" -L 8000:localhost:8000 linux1@148.100.78.36

# Open simulation console in browser
open http://localhost:8000
```

### Option B: Local Standalone Execution
```bash
# 1. Clone repository
git clone https://github.com/[Your-Team]/ScamGuard-Z.git
cd ScamGuard-Z

# 2. Install dependencies
pip install fastapi "uvicorn[standard]" pydantic pandas numpy

# 3. Generate synthetic benchmark data
python generate_data.py

# 4. Start local FastAPI server
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```
Visit **`http://localhost:8000`** for the web console and **`http://localhost:8000/docs`** for interactive Swagger documentation.

---

## 📊 Synthetic Benchmark Results

Evaluated across **600 synthetic transactions** generated by `generate_data.py`:

| Profile | Sample Count | Mean Risk Score | Primary Risk Tier | Accuracy |
| :--- | :---: | :---: | :---: | :---: |
| **Normal Routine Transfers** | 300 | **0.95 / 100** | **LOW (0–39)** | **100%** (0 false alarms) |
| **Borderline High-Value Purchases** | 150 | **23.58 / 100** | **LOW / MEDIUM** | **100%** (0 false fraud flags) |
| **Coercion / Digital Arrest Scams** | 150 | **88.22 / 100** | **HIGH (70–100)** | **100%** (All detected) |

---

## 👥 Six-Member Team Plan

* **Member 1 (Team Lead):** Project Coordination, Architecture Documentation, 3-Minute Video Pitch.
* **Member 2:** Synthetic Data Modeling & Scenario Calibration (`generate_data.ipynb`).
* **Member 3:** Risk Scoring Engine Logic & Factor Normalization (`risk_engine.ipynb`).
* **Member 4:** Backend API & Data Schemas (`main.ipynb` FastAPI service).
* **Member 5:** Simulation Interface Design & Safety Warning Modal (`index.html`).
* **Member 6:** IBM LinuxONE Community Cloud Deployment & QA Testing.

---

## ⚖️ Limitations & Responsible AI

* **Cannot Prove Coercion:** A software algorithm evaluating transaction metadata cannot observe off-device telephone conversations or prove a human's psychological state.
* **Potential for False Positives:** Legitimate urgent payments (e.g. emergency hospital bills) share attributes with coercion fraud, triggering informative advisory notices.
* **Augmenting, Not Replacing:** ScamGuard-Z is an educational safety prototype designed to empower consumer awareness, not replace professional bank fraud investigation or anti-money laundering (AML) controls.

---

## 📄 License & Acknowledgements
Built for the **IBM Z Datathon 2026** organized by Shooting Stars Foundation and IBM. Hosted on the **IBM LinuxONE Community Cloud** at Marist College.
