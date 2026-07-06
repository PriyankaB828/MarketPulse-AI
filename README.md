# MarketPulse AI 🧠
> **Autonomous Executive Decision Intelligence Platform & Business Digital Twin**

MarketPulse AI is an enterprise-grade **Business Digital Twin** that simulates a C-Suite executive boardroom crisis response. Built for the Kaggle + Google "AI Agents Capstone Project," it demonstrates a true multi-agent network where 7 C-suite agents with competing constraints negotiate, dispute, vote, and arrive at consolidated corporate action items in real-time.

---

## 🏗️ System Architecture

MarketPulse AI implements a structured **14-Stage Decision Intelligence Pipeline**:

```
[1. Business Crisis Activated]
             ↓
[2. Business Digital Twin State Loaded]
             ↓
[3. Round 1: Independent Investigation] (Each agent calls MCP tool)
             ↓
[4. Round 2: Evidence Sharing] (Data combined in context)
             ↓
[5. Round 3: Executive Debate] (Conflict resolution & reasoning negotiation)
             ↓
[6. Round 4: Strategy Proposals] (Each agent proposes its optimal strategy)
             ↓
[7. Round 5: Executive Voting] (Agents vote on all strategies)
             ↓
[8. CEO Question Round / What-If Interruption] (CEO adjusts parameters, triggering loop to Round 3)
             ↓
[9. Strategy Synthesizer Runs] (Weighted evaluation based on Trust Scores)
             ↓
[10. Business Decision Matrix Output] (Revenue, Profit, Inventory, Risk, NPS)
             ↓
[11. Business KPI Projection] (Simulated post-strategy metrics)
             ↓
[12. Why This Strategy Won] (Detailed justification)
             ↓
[13. Why Other Strategies Lost (Why-Not Panel)] (Explicit show-stoppers)
             ↓
[14. Business Memory Updated] (Historical outcome saved to ledger)
```

---

## 📁 Project Directory Structure

```
marketpulse-ai/
├── README.md                 # Core system documentation
├── package.json              # Workspace script manager
├── backend/
│   ├── main.py               # FastAPI server, Real-Time SSE streams, Memory State Store
│   ├── agents.py             # C-Suite Agent Models & 5-Stage Orchestrator
│   ├── tools.py              # Business Intelligence MCP Layer tools
│   ├── models.py             # Pydantic schemas for What-If variables & matrices
│   ├── test_simulation.py    # CLI validation test script
│   └── .env                  # GEMINI_API_KEY configuration
└── frontend/
    ├── package.json          # React, Framer Motion, and Recharts dependencies
    ├── vite.config.js        # Vite config with reverse proxy
    ├── index.html            # Web app entry point
    └── src/
        ├── main.jsx
        ├── index.css         # Glassmorphic utilities & CRT overlay styling
        ├── App.jsx           # Live war-room layout container
        ├── mockData.js       # Fallback local data simulation presets
        └── components/
            ├── Header.jsx             # Twin status header bar
            ├── KPICards.jsx           # Executive KPI Strip
            ├── CommunicationGraph.jsx # SVG-based C-Suite communication network
            ├── AgentGrid.jsx          # Agent cards, trust scores, and goals
            ├── DebateTimeline.jsx     # Chronological message feed
            ├── VotingPanel.jsx        # Executive Strategy Voting Matrix
            ├── StrategyDashboard.jsx  # Radar chart & final recommendation actions
            ├── WhyNotPanel.jsx        # Why-Not Rejected Strategy Explainability
            ├── MemoryTimeline.jsx     # Past corporate lessons learned
            └── CEOControlPanel.jsx    # Real-time What-If sliders
```

---

## 👥 C-Suite Agents & MCP Tools

Each agent operates with its own system prompt, constraints, and custom tools:

1.  **CFO (Finance)**: Goal is protecting gross margins (>=15%) and ROI (>=10%). Vetoes direct price matches. (Tool: `Financial Modeling MCP`)
2.  **CMO (Marketing)**: Protects market share and brand equity. Focuses on customer acquisition and reach. (Tool: `Marketing Optimization MCP`)
3.  **VP Inventory**: Optimizes storage levels. Aims to clear dead stock and prevent stockouts. (Tool: `Inventory Analytics MCP`)
4.  **COO (Operations)**: Assesses logistics bottlenecks and protects delivery fulfillment SLAs. (Tool: `Supply Chain Intelligence MCP`)
5.  **CCO (Customer)**: Monitors customer satisfaction and retention. Constraints: NPS >= 70, Churn < 8%. (Tool: `Customer Insight MCP`)
6.  **VP Market Intel**: Constantly scans competitor pricing and threat events. (Tool: `Competitor Intelligence MCP`)
7.  **CEO/Chief of Staff**: Orchestrates execution rounds, detects disputes, and maintains the boardroom communication link.

---

## 🚀 Installation & Startup Guide

### Prerequisites
*   Node.js (v18+)
*   Python (3.9+)

### 1. Backend Setup
1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  *(Optional)* Configure your Gemini key in `.env`:
    ```env
    GEMINI_API_KEY=your-api-key-here
    ```
4.  Start the FastAPI server:
    ```bash
    uvicorn main:app --reload --port 8000
    ```

### 2. Frontend Setup
1.  Navigate to the frontend directory:
    ```bash
    cd ../frontend
    ```
2.  Install packages:
    ```bash
    npm install
    ```
3.  Start the Vite dev server:
    ```bash
    npm run dev
    ```
4.  Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 📺 Cinematic 5-Minute Hackathon Demo Guide

1.  **Introduce the Dashboard**: Showcase the glowing dark theme, real-time Digital Twin status, and the C-Suite executive grid.
2.  **Launch the Black Friday Price War**: Select *Competitor Flash Sale* + *Supplier Shipment Delay*. Click **Launch Crisis**.
3.  **Watch the Multi-Agent Debate**: Point out the SVG Communication Network where glowing data packets transfer between nodes, the live chat timeline where CFO and CMO disagree on price-matching, and the populating Voting Matrix.
4.  **CEO Intervention**: Drag the *Competitor Discount* slider to 60% and click **Recalculate Strategy**. Show how C-suite agents immediately renegotiate, updating the voting matrix and selecting the Bundle campaign instead of No Action.
5.  **Explainability**: Open the **Why-Not Veto Panel** to show why direct price matches and ignoring competitor sales were rejected, proving that business constraints drive decisions.
