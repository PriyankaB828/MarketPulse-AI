<img width="1920" height="1080" alt="Screenshot 2026-07-06 225850" src="https://github.com/user-attachments/assets/a9376691-b408-4104-b42d-825c724b8a4c" /><img width="1920" height="1020" alt="Screenshot 2026-07-06 225451" src="https://github.com/user-attachments/assets/9ec74bcc-430d-412f-a237-9c4052da90f8" /># 🧠 MarketPulse AI

> **Autonomous Executive Decision Intelligence Platform & Business Digital Twin**

MarketPulse AI is an AI-powered **Business Digital Twin** that simulates executive decision-making during real-world business crises.

Instead of relying on a single AI assistant, the platform models an entire **C-suite boardroom** where seven autonomous executive agents independently analyze a business situation, debate alternative strategies, vote on solutions, and collectively recommend the optimal business decision.

Built as part of the **Kaggle + Google AI Agents Intensive Vibe Coding Capstone Project**, MarketPulse AI demonstrates how multi-agent AI systems can improve enterprise decision-making through collaborative reasoning and explainable recommendations.

---

# 🎯 Problem Statement

Organizations regularly face high-impact business events such as:

- Competitor price wars
- Supply chain disruptions
- Negative customer reviews
- Seasonal demand spikes

These situations require multiple departments to work together before executives make strategic decisions.

Traditional dashboards only visualize data—they don't help executives reason through complex business situations.

MarketPulse AI addresses this gap by simulating a complete executive boardroom where AI agents collaborate exactly like real business leaders.

---

# 💡 Solution

MarketPulse AI creates a **Business Digital Twin** capable of simulating executive discussions before real business decisions are taken.

Instead of receiving one AI response, executives observe:

- Multiple AI agents investigating independently
- Evidence sharing
- Executive debates
- Strategy proposals
- Voting process
- Final recommendation
- Explainable reasoning
- KPI projections
- Historical business memory

This allows organizations to evaluate multiple strategic options safely before implementing them.

---

# ✨ Features

- Multi-Agent Executive Decision System
- Business Digital Twin Dashboard
- Real-time Crisis Simulation
- Seven Autonomous Executive Agents
- Executive Debate Timeline
- Live Communication Graph
- Strategy Voting Matrix
- Explainable AI (Why-Not Panel)
- CEO What-If Scenario Analysis
- Historical Business Memory Ledger
- Business KPI Dashboard
- FastAPI Backend
- React Frontend
- Gemini AI Integration (Optional)
- Deterministic Fallback Simulation (No API Key Required)

---

# 🛠 Tech Stack

## Frontend

- React
- Vite
- Tailwind CSS
- Framer Motion
- Recharts
- Lucide Icons

## Backend

- FastAPI
- Python
- Pydantic
- Uvicorn

## AI

- Multi-Agent Architecture
- Business Intelligence Tools
- Google Gemini API (Optional)
- Server-Sent Events (SSE)

---

# 👥 Executive AI Agents

MarketPulse AI simulates a complete executive boardroom.

| Agent | Responsibility |
|--------|---------------|
| CEO / Chief of Staff | Coordinates all executive discussions |
| CFO | Protects profitability and ROI |
| CMO | Protects market share and branding |
| COO | Optimizes logistics and operations |
| VP Inventory | Prevents stock shortages and overstock |
| Chief Customer Officer | Protects customer satisfaction |
| VP Market Intelligence | Monitors competitors and market threats |

Each executive has different priorities and constraints, resulting in realistic business negotiations.

---

# 🔄 System Workflow

```
Business Crisis
      │
      ▼
Business Digital Twin Loaded
      │
      ▼
Independent Investigation
      │
      ▼
Evidence Sharing
      │
      ▼
Executive Debate
      │
      ▼
Strategy Proposal
      │
      ▼
Executive Voting
      │
      ▼
CEO What-If Intervention
      │
      ▼
Strategy Synthesis
      │
      ▼
Business KPI Projection
      │
      ▼
Why This Strategy Won
      │
      ▼
Why Other Strategies Lost
      │
      ▼
Business Memory Updated
```

---

# 📊 Dashboard Components

The dashboard consists of several business intelligence modules.

### KPI Cards

Displays

- Business Health
- Revenue Protected
- Profit Impact
- Market Threat
- Customer Sentiment
- Operational Risk
- Inventory Health
- Market Share

---

### Communication Graph

Visualizes communication between executive agents during debates.

---

### Executive Agent Cards

Displays

- Executive Role
- Current Status
- Trust Score
- Recommendation
- Current Activity

---

### Debate Timeline

Shows the chronological discussion between executives.

---

### CEO What-If Panel

Allows executives to modify:

- Competitor Discount
- Shipment Delay
- Customer Sentiment
- Inventory Overstock
- Demand Spike

The system immediately recalculates recommendations.

---

### Voting Matrix

Displays how every executive votes on competing business strategies.

---

### Strategy Dashboard

Shows

- Winning Strategy
- Revenue Projection
- Profit Impact
- Business Health
- Expected Outcomes

---

### Why-Not Panel

Provides explainable AI by showing why rejected strategies were not selected.

---

### Business Memory Timeline

Stores previous simulations and lessons learned to improve future decision-making.

---

# 📂 Project Structure

```
marketpulse-ai/

│
├── backend/
│   ├── main.py
│   ├── agents.py
│   ├── tools.py
│   ├── models.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── mockData.js
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── package.json
```

---

# 🚀 Installation

## Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload --port 8000
```

Backend runs on

```
http://localhost:8000
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on

```
http://localhost:5173
```

---

# 🔑 Gemini API (Optional)

MarketPulse AI supports Google Gemini for enhanced executive reasoning.

Create a `.env` file inside the backend folder.

```env
GEMINI_API_KEY=your_api_key_here
```

If no API key is provided, the application automatically switches to a deterministic fallback simulation so every feature remains functional.

---

# 🎬 Demo Walkthrough

### Step 1

Launch the application.

Observe the Business Digital Twin dashboard.

---

### Step 2

Select crisis events such as

- Competitor Flash Sale
- Shipment Delay

Click

**Launch Crisis**

---

### Step 3

Watch executives

- investigate
- debate
- communicate
- propose strategies

---

### Step 4

Observe the

- Voting Matrix
- Strategy Recommendation
- KPI Updates

---

### Step 5

Adjust CEO What-If sliders.

For example

- Increase competitor discount
- Increase shipment delay

Click

**Recalculate Strategy**

Notice how every executive updates their recommendation.

---

### Step 6

Open the

**Why-Not Panel**

to understand why rejected strategies were not selected.

---

### Step 7

View the

Business Memory Timeline

to review previous simulations and lessons learned.

---

# 📸 Screenshots

Add screenshots here after uploading them.

```
images/

dashboard.png

agents.png

debate.png

strategy.png

memory.png
```
<img width="1920" height="1020" alt="Screenshot 2026-07-06 225451" src="https://github.com/user-attachments/assets/11dedd1d-ff09-4981-9899-23643f8900a2" />
<img width="1920" height="1080" alt="Screenshot 2026-07-06 225828" src="https://github.com/user-attachments/assets/7b3772fc-0a83-4a7b-9233-a8a558c9ade6" />
<img width="1920" height="1080" alt="Screenshot 2026-07-06 225850" src="https://github.com/user-attachments/assets/61f05352-0f17-4220-b1cc-b5489072e2cc" />

---

# 🎥 Demo Video

A complete walkthrough video demonstrating the project is available on YouTube.

(Add your YouTube link here)

---

# 🌐 GitHub Repository

(Add your GitHub repository link here)

---

# 📌 Future Improvements

- Real-world competitor pricing APIs
- ERP integration
- Live inventory synchronization
- Financial forecasting models
- Predictive demand forecasting
- Real-time social media monitoring
- Autonomous agent planning
- Cloud deployment

---

# 👩‍💻 Team Members

- Aishwarya D
- Komal B
- Priyanka B
- Seema G R

---

# 📄 License

Developed for the **Kaggle + Google AI Agents Intensive Vibe Coding Capstone Project**.
