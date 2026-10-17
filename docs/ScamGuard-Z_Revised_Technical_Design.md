# ScamGuard-Z: Revised Technical Solution & Design Document

**IBM Z Datathon 2026 Submission**  
**Selected Challenge:** Theme 1: Real-Time AI for Critical Decisions  
**Cross-Cutting Theme:** Theme 2: AI Secured — Innovation Without Exposure  
**Target Architecture:** IBM Z / LinuxONE Community Cloud (Target for Exploration & Validation)  
**Project Team Scope:** Six-Member Undergraduate Student Team (Beginner-Friendly Project Scope)  
**Document Status:** Revised Technical Design Specification & Prototype Architecture  

---

## Problem Statement

> “Victims of social engineering scams may authorise fraudulent bank transfers themselves under pressure or deception. Traditional transaction checks may not identify these coercion-related risks, allowing victims to lose their savings.”

*ScamGuard-Z analyses simulated transactions, identifies suspicious patterns, explains its risk assessment, and displays an educational safety warning encouraging users to pause and verify the recipient.*

---

## 1. Executive Summary

In digital retail banking, Authorized Push Payment (APP) fraud and psychological coercion—such as scammers impersonating law enforcement officers ("digital arrest" scams), tax inspectors, or distressed family members—trick victims into voluntarily authenticating bank transfers. Because the genuine account owner enters their legitimate credentials, PINs, and two-factor authentication codes, traditional fraud controls designed for unauthorized account takeovers often fail to detect that the user is acting under severe psychological pressure or deception.

**ScamGuard-Z** is an explainable transaction evaluation prototype designed to address this vulnerability within a realistic, achievable scope for a team of six beginner students. Rather than attempting to block transactions irreversibly or claim complete scam elimination, ScamGuard-Z analyzes simulated transactions across four observable detection factors: atypical transfer amounts, unfamiliar recipient status, rapid transfer velocity, and high account balance depletion ratios. 

The system computes an explainable composite risk score categorized into **Low, Medium, and High** risk tiers. When compounding indicators trigger a High-Risk classification, the interface deploys an empathetic, practical safety warning modal encouraging the user to pause, question the caller's instructions, and verify recipient authenticity through independent channels. The project relies strictly on synthetic transaction data to protect consumer privacy, establishes a robust rule-based scoring baseline with an optional machine-learning extension, and targets the **IBM LinuxONE Community Cloud (s390x)** as an enterprise mainframe deployment platform to explore and validate during the datathon.

---

## 2. Problem Statement & Project Objectives

### 2.1 The Vulnerability of Authorized Coercion
Traditional banking fraud architectures focus predominantly on detecting unauthorized access—such as credential stuffing, malware, or logins from unrecognized devices and foreign IP addresses. In social engineering scams, however, the cybercriminal manipulates the human user directly through fabricated urgency, fear, or false authority. Because the legitimate account owner initiates and authorizes the payment from their own trusted device, standard security rules evaluate the payment as legitimate.

### 2.2 Realistic Nuance: Suspicious Does Not Equal Scam
A central requirement of ScamGuard-Z is acknowledging that **not every unusual transaction is a scam**. Legitimate consumers regularly execute large or unfamiliar transfers (e.g., purchasing a vehicle, paying a property deposit, or hiring a new contractor). Claiming that every anomaly represents fraud would lead to unacceptable false-positive rates and user frustration. Therefore, ScamGuard-Z is designed as an **educational and advisory safety layer**, not an accusatory or automated account-blocking system.

### 2.3 Core Project Objectives
1. **Simulation Interface:** Build a lightweight, web-based transaction simulation interface allowing users and judges to test realistic payment scenarios.
2. **Explainable Risk Engine:** Implement a transparent, inspectable mathematical scoring baseline evaluating four key transaction factors.
3. **Actionable Risk Tiers:** Categorize transactions into Low, Medium, and High risk levels accompanied by plain-English explanations.
4. **Safety Intervention Modal:** Deploy a supportive safety dialog with practical verification steps when high-risk patterns converge.
5. **Optional ML Extension:** Explore training a supervised classifier using Python's Scikit-Learn on synthetic transaction logs to compare against the rule-based baseline.
6. **IBM LinuxONE Exploration:** Package the FastAPI backend as a container and explore deploying and validating it on the IBM LinuxONE Community Cloud.

---

## 3. Proposed Solution & Core Prototype Features

ScamGuard-Z is structured into five modular components:

### 3.1 Prototype Components
1. **Transaction Simulation & Input Interface:** A straightforward web interface allowing evaluators to input mock transfer details: payment amount, historical average, account balance prior to payment, transfer frequency within the last 24 hours, and recipient verification status.
2. **Explainable Risk-Scoring Engine:** A deterministic baseline engine that calculates a composite score (0–100) using inspectable weights across the four detection factors.
3. **Risk Tier Categorization:**
   - **Low Risk (0–39):** Normal attributes; user proceeds with standard confirmation.
   - **Medium Risk (40–69):** Isolated anomaly; subtle advisory notice displayed.
   - **High Risk (70–100):** Multiple compounding indicators; prominent safety warning modal triggered.
4. **Practical Safety Warning Dialog:** Displays structured cognitive speed-bumps:
   - *"Are you currently on an active phone call with someone instructing you to transfer this money?"*
   - *"Did a caller claim to be from law enforcement, a tax department, or bank security?"*
   - Practical verification checklist: Hang up, verify via an independently sourced phone number, and speak with a trusted friend or family member.
5. **Optional Machine Learning Extension:** A supervised baseline classifier (Logistic Regression or Random Forest from Scikit-Learn) to compare predicted risk probabilities with rule-based outputs.

### 3.2 Detection Factors Evaluated

| Detection Factor | Description & Operational Rationale | Simulated Risk Indicator |
| :--- | :--- | :--- |
| **1. Atypical Transfer Amount** | Compares requested transfer against the account's historical median payment amount. | Transfer value exceeds 3× to 5× the account's historical average. |
| **2. Unfamiliar Recipient Status** | Checks whether the destination account is pre-existing or recently created. | Beneficiary added within the past 24 hours with zero previous payment history. |
| **3. Transfer Velocity (Frequency)** | Tracks repeated outbound transfers occurring within a compressed timeframe. | Multiple outbound transfers executed within minutes or hours of each other. |
| **4. Account Depletion Ratio** | Calculates the proportion of total liquid balance being liquidated in a single payment. | Single transaction attempts to drain 75% to 95% of available funds. |

---

## 4. System Architecture & Workflow

### 4.1 System Architecture Flow
```
[ Simulation Client UI (HTML/CSS/JS) ]
                  │
                  ▼ (REST / JSON Payload)
┌──────────────────────────────────────────────────────────┐
│  FastAPI Backend Service (Target: IBM LinuxONE / s390x)  │
│                                                          │
│  ┌────────────────────┐      ┌────────────────────────┐  │
│  │ Feature Extractor  │ ───► │  Risk Scoring Engine   │  │
│  │ (Velocity, Ratios, │      │  (Rule Baseline / ML)  │  │
│  │  Recipient Status) │      │  Outputs Score (0-100) │  │
│  └────────────────────┘      └───────────┬────────────┘  │
│                                          │               │
│                                          ▼               │
│                              ┌────────────────────────┐  │
│                              │ Explanation Generator  │  │
│                              │ (Human-readable logic) │  │
│                              └────────────────────────┘  │
└─────────────────────────┬────────────────────────────────┘
                          │
                          ▼ (JSON Assessment Response)
┌──────────────────────────────────────────────────────────┐
│  Simulation Interface Action:                            │
│  • Low Risk (0-39)    ➔ Normal Proceed Confirmation      │
│  • Medium Risk (40-69) ➔ Informational Advisory Note     │
│  • High Risk (70-100) ➔ Prominent Safety Warning Modal   │
└──────────────────────────────────────────────────────────┘
```

### 4.2 Sequential Workflow
1. **Submit Transaction:** User submits simulated payment parameters via the web form.
2. **Feature Extraction:** Backend extracts relative ratios (amount-to-average, depletion ratio, velocity count, recipient status).
3. **Score Calculation:** Rule-based algorithm calculates weighted sub-scores and aggregates them into a composite score (0–100).
4. **Tier Classification:** Score is mapped to Low, Medium, or High risk tier.
5. **Explanation & Advisory Generation:** Specific triggered factor strings are returned to the client to render the safety warning dialog.

---

## 5. Technology Stack & IBM Z / LinuxONE Exploration

The technology stack is specifically chosen to be accessible, well-documented, and robust for a team of six beginner undergraduate developers:

| Technology | Layer / Role | Purpose & Beginner Rationale |
| :--- | :--- | :--- |
| **Python 3.x** | Core Language | Clear syntax, extensive standard libraries, and universal open-source documentation. |
| **FastAPI** | Backend Web API | Lightweight REST framework with automatic data validation (Pydantic) and auto-generated Swagger documentation (`/docs`). |
| **HTML5 / CSS3 / JavaScript** | Frontend Simulation UI | Zero framework overhead; straightforward to build responsive transaction forms and modal popups. |
| **Pandas & NumPy** | Data Generation & Processing | Standard tools for generating, manipulating, and filtering synthetic tabular transaction datasets. |
| **Scikit-Learn (Optional)** | Machine Learning Extension | Beginner-friendly machine learning library for training baseline tabular models (Logistic Regression, Random Forest). |
| **IBM LinuxONE Community Cloud** | Deployment Exploration Target | Target environment to learn containerization (Docker) and validate running our Python/FastAPI service on enterprise s390x architecture. |

> **Deployment Target Clarification:** Deploying on IBM LinuxONE Community Cloud is an **exploration target** for our team to validate during the datathon, not an already completed deployment. Our objective is to understand enterprise Linux on mainframe architecture and explore how containerized microservices run on `s390x`.

---

## 6. Data Strategy & Synthetic Dataset Generation

### 6.1 Synthetic Transaction Data as the Primary Source
Connecting to live bank APIs or using genuine consumer financial records is impossible due to legal, privacy, and regulatory constraints. Furthermore, genuine coercion and scam transactions are not publicly available with verified labels. Consequently, **ScamGuard-Z uses 100% synthetic transaction data as its primary foundation**.

Our synthetic data generator script creates two distinct profiles:
- **Normal Simulated Transactions:** Modest transfer amounts ($20 to $150), pre-existing and recurring recipients (utilities, saved friends), low velocity (1–2 transfers daily), and minimal account depletion (<15%).
- **Suspicious Simulated Scenarios:** High transfer amounts ($2,000+), newly created recipients (<24 hours old), rapid back-to-back transfer attempts, and high balance depletion (>80%).

### 6.2 Critical Distinction: Simulated Risk vs. Verified Fraud
Labels in our synthetic dataset denote **simulated risk profiles**, not ground-truth criminal convictions. This distinction maintains technical rigor and ensures that evaluators understand the prototype evaluates synthetic anomaly patterns rather than verified forensic crime records.

### 6.3 Exploratory Public Datasets
The team will examine the **Kaggle IEEE-CIS Fraud Detection dataset** solely as an exploratory reference for tabular financial feature distributions, strictly subject to platform availability, download constraints, and licensing terms during the hackathon.

---

## 7. AI & Risk Scoring Methodology

### 7.1 Rule-Based Baseline Engine (Primary Focus)
To ensure complete transparency and inspectability, the primary engine evaluates four detection factors with explicit mathematical weights:

$$\text{Total Risk Score} = (W_{\text{amt}} \times S_{\text{amt}}) + (W_{\text{recip}} \times S_{\text{recip}}) + (W_{\text{vel}} \times S_{\text{vel}}) + (W_{\text{dep}} \times S_{\text{dep}})$$

**Proposed Baseline Weights (Sum = 100):**
- **$W_{\text{amt}}$ (Atypical Amount):** 30 Points (scales based on multiplier over historical average).
- **$W_{\text{recip}}$ (Unfamiliar Recipient):** 25 Points (binary or age-decayed flag for new payee).
- **$W_{\text{vel}}$ (Transfer Velocity):** 25 Points (increments based on transfers within 24 hours).
- **$W_{\text{dep}}$ (Balance Depletion):** 20 Points (scales linearly with percentage of balance transferred).

### 7.2 Explainability Mechanism
When a factor exceeds its designated risk threshold, the engine attaches human-readable explanatory text to the response payload:
- *"Transfer amount is 4.2× higher than your 30-day average."*
- *"Recipient account was added 3 hours ago with zero prior payment history."*
- *"This transaction transfers 85% of your available account balance."*

### 7.3 Optional Machine-Learning Extension
If time permits after the baseline is operational, the team will train a binary classifier (Logistic Regression or Random Forest from Scikit-Learn) using an 80/20 train/test split on synthetic data. This extension will evaluate whether machine-learning feature importance aligns with our heuristic weights. *No pre-trained model is claimed prior to the datathon.*

---

## 8. Evaluation Plan & Proposed Targets

All metrics represent **proposed engineering targets** for the prototype within our synthetic test suite:

| Evaluation Metric | Description & Operational Purpose | Proposed Target |
| :--- | :--- | :--- |
| **Precision (Simulated)** | Proportion of high-risk flags that were intended suspicious scenarios. | Proposed Target: > 80% on synthetic test suite |
| **Recall (Simulated)** | Proportion of synthetic high-duress scenarios successfully identified. | Proposed Target: > 85% on synthetic test suite |
| **False-Positive Rate** | Frequency of routine, normal transactions incorrectly flagged as high risk. | Proposed Target: < 15% to minimize user irritation |
| **API Response Time** | End-to-end latency from transaction submission to risk score response. | Proposed Target: < 500ms on simulated API calls |
| **Explanation Clarity** | Qualitative review ensuring reasoning strings are understandable to laypersons. | 100% of high-risk outputs provide readable text |

---

## 9. Privacy, Security & Ethical Considerations

- **Synthetic Exclusivity:** No real bank accounts, real card numbers, credentials, or actual personal data are ever collected, processed, or stored.
- **Data Minimization:** Only operational metadata parameters (amount, relative timestamp delta, recipient status, balance percentage) are processed.
- **Respect for User Autonomy:** The prototype never permanently freezes accounts or assumes legal authority; it acts purely as a supportive cognitive pause.
- **Absence of Unsupported Claims:** The project does not claim formal PCI-DSS or GDPR compliance certification, but adheres to privacy-by-design principles appropriate for a hackathon prototype.

---

## 10. Implementation Roadmap (24-Hour Datathon Timeline)

| Phase & Timeline | Focus Area | Key Deliverables & Validation Milestones |
| :--- | :--- | :--- |
| **Phase 1: Setup & Data (Hours 0–4)** | Environment & Synthetic Data | Initialize GitHub repository; write Python synthetic data generator producing 500+ mock records. |
| **Phase 2: Core Engine (Hours 4–8)** | Rule-Based Scoring Logic | Implement mathematical factor weightings and plain-English explanation generators in Python. |
| **Phase 3: Backend API (Hours 8–12)** | FastAPI Web Service | Create `/evaluate-transaction` REST endpoint with Pydantic validation; verify via Swagger UI. |
| **Phase 4: Simulation UI (Hours 12–16)** | Web Form & Safety Dialog | Build responsive HTML/CSS/JS interface to input mock transactions and display risk tier modal. |
| **Phase 5: Testing & ML (Hours 16–20)** | Quality Assurance & ML Exploration | Execute test scenarios across simulated data; test optional Scikit-Learn baseline classifier if time allows. |
| **Phase 6: LinuxONE & Pitch (Hours 20–24)** | Mainframe Target & Video | Explore container deployment on LinuxONE Community Cloud; record 3-minute video pitch; submit project. |

---

## 11. Six-Member Team Plan & Responsibilities

| Member Role | Primary Focus Area | Key Responsibilities | Deliverables |
| :--- | :--- | :--- | :--- |
| **Member 1 (Team Lead)** | Project Coordination & Pitch | Manages timelines, coordinates documentation, writes presentation script, edits 3-minute video. | Project README, presentation script, demo video. |
| **Member 2** | Synthetic Data & Scenarios | Builds synthetic data generation scripts, creates normal and suspicious test cases. | `generate_data.py`, CSV synthetic datasets. |
| **Member 3** | Risk Scoring Engine | Implements mathematical factor scoring functions, weight normalization, and explanation logic. | `risk_engine.py`, rule validation tests. |
| **Member 4** | Backend API Developer | Constructs FastAPI service, defines Pydantic data schemas, connects scoring logic to endpoints. | `main.py` API service, Swagger endpoint docs. |
| **Member 5** | Frontend UI Developer | Develops payment input form, designs visual risk indicators (Low/Med/High), builds safety modal dialog. | `index.html`, `style.css`, frontend scripts. |
| **Member 6** | LinuxONE Target & QA Tester | Explores containerizing the application (Dockerfile), tests deployment on LinuxONE, logs test metrics. | `Dockerfile`, test results summary, LinuxONE notes. |

*Shared Team Responsibility: All six members participate in collaborative end-to-end testing, peer review, and video recording rehearsal during Hours 16–20.*

---

## 12. Limitations & Future Scope

### 12.1 Prototype Limitations
- **Cannot Prove True Coercion:** A software algorithm evaluating transaction metadata cannot observe off-device human telephone interactions or verify psychological duress.
- **Potential for False Positives:** Legitimate urgent transactions (e.g., emergency medical expenses) exhibit features similar to scams, occasionally prompting advisory warnings.
- **Does Not Replace Bank Fraud Controls:** ScamGuard-Z is an experimental educational concept designed to augment human awareness, not replace professional bank fraud departments, AML investigators, or transaction settlement systems.

### 12.2 Future Scope
- **Multi-Party Advisory Verification:** Exploring opt-in mechanisms allowing users to select a trusted contact who receives advisory notifications during high-risk transfers.
- **Enterprise Mainframe Integration:** Conducting deeper technical exploration on IBM Z infrastructure to benchmark real-time transactional throughput and hardware-accelerated security.
- **Ethical Behavioral Signals:** Investigating whether ethical, client-side interaction hesitation metrics (e.g., input pauses during beneficiary entry) can provide non-intrusive safety signals.

---

## 13. References & Conclusion

### References
1. **Payment Systems Regulator (PSR), UK.** (2023). *Authorised Push Payment (APP) Scams: Policy Statement and Performance Metrics*. Available at: https://www.psr.org.uk/
2. **Global Anti-Scam Alliance (GASA).** (2023). *The Global State of Scams Report: Consumer Vulnerability and Social Engineering Trends*. Available at: https://www.gasa.org/
3. **FastAPI Documentation.** (2024). *High Performance Python Web Framework*. Tiangolo. Available at: https://fastapi.tiangolo.com/
4. **Pedregosa, F., et al.** (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, pp. 2825–2830.
5. **IBM Corporation.** (2024). *LinuxONE Community Cloud Documentation and Fast Start Guides*. IBM Z Community. Available at: https://community.ibm.com/zsystems/l1cc/

### Conclusion
ScamGuard-Z addresses the severe challenge of social engineering and coercion scams through a practical, transparent, and human-centered design. By acknowledging that traditional security controls often fail to detect authorized transfers executed under duress, the project introduces an explainable scoring baseline and an empathetic safety pause. Tailored specifically for a team of six beginner undergraduate students, ScamGuard-Z provides a realistic, achievable, and technically sound solution for the IBM Z Datathon 2026.
