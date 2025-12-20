# company_project
🧠 AI Ops Assistant – Order Intelligence System (LangGraph)
Overview

This project implements a real-world AI Operations Assistant that automatically evaluates incoming orders based on inventory availability, daily production capacity, and order priority.

The system is built using LangGraph to model deterministic, production-grade decision-making and includes:
**Features**

Key Features

✅ Automatically reads new orders from CSV

✅ Validates inventory availability

✅ Enforces daily production capacity (200 units/day)

✅ Detects and flags:

Stock shortages

Capacity overloads

✅ Generates decisions per order:

      . APPROVE

      . DELAY

      . SPLIT

      . ESCALATE

✅ Human-readable recommendation reasons

✅ Logs decisions to a file

✅ Sends Slack alerts for escalations (optional)

✅ Live Streamlit dashboard with:

       . Auto-refresh

       . Filters

       . Metrics

       . CSV export

✅ File-watcher for automatic reprocessing on new data

**Tech Stack**

* Python 3.9+
* LangGraph
* LangChain
* Pandas
* Streamlit
* Requests

Project Structure
company/

company/
├── app.py              # LangGraph core decision engine
├── watcher.py          # File watcher for auto-processing
├── dashboard.py        # Streamlit dashboard
├── notifier.py         # Logging + Slack alerts
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    ├── orders.csv
    └── inventory.csv

**Business Rules Implemented**

1. Maximum production capacity: 200 units per day
2. No negative inventory allowed
3. Urgent orders may escalate but never violate constraints
4. Orders exceeding stock → Split
5. Orders exceeding capacity → Delay / Escalate
6. One final decision per order with clear reasoning

**How the System Works**

1. Watcher monitors orders.csv for changes
2. On detecting new data, it automatically runs app.py
3. LangGraph processes all orders using current inventory & capacity
4. Decisions + reasoning are:
5.           . Printed to console
6.           . Logged to ops_output.log
7.           . Sent to Slack if escalated
8. Streamlit dashboard auto-refreshes and displays results

▶️ Working Demo & Execution Proof
1️⃣ Create & activate virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate   # Windows

2️⃣ Install dependencies
pip install -r requirements.txt

**▶️ How to Run (Correct Order)**
🔹 Terminal 1 – Start Dashboard
streamlit run dashboard.py

🔹 Terminal 2 – Start Watcher (Automation)
python watcher.py
Watches orders.csv and triggers processing automatically.

🔹 Add New Orders

Edit data/orders.csv, add a new row, and save the file.

✅ Processing starts automatically
✅ Logs update
✅ Dashboard refreshes


**Sample Console Output**

ORD003 → SPLIT
Reason: Only 250 units available, rest delayed

ORD007 → ESCALATE
Reason: Daily production capacity exceeded

**Log File Output**

All decisions are appended to:

ops_output.log

Each log entry includes:
       . Order ID
       . Decision
       . Reason
       . Execution trace

**📈 Dashboard Capabilities**

* Live auto-refresh
* Decision filtering (Approve / Delay / Split / Escalate)
* Summary metrics
* Execution trace per order
* CSV export of results

**Logic**

The system automatically reads new orders, checks inventory availability and daily production capacity, and generates one operational decision (Approve, Delay, Split, or Escalate) per order.
All decisions are deterministic, constraint-driven, and include a clear human-readable reason.

**🛠 Failure Handling & Edge Cases**
Missing data files are auto-created, CSV headers are normalized, inventory is never allowed to go negative, capacity overloads are safely delayed or escalated, Python environment mismatches are avoided, and the dashboard gracefully handles missing or delayed logs.

**Assumptions**

* Orders are processed sequentially
* Inventory is shared across days
* Production capacity resets daily
* CSV files act as data ingestion source
* Console + logs are sufficient for Level-1 evaluation

**Future Enhancements (Level-2 Ready)**

* LLM-based reasoning node
* Autonomous capacity forecasting
* Multi-agent negotiation (Sales vs Ops)
* Database-backed ingestion
* API-based order intake
* Cloud deployment

Author

Satendra
AI / ML Engineer
Automation • LangGraph • Operations Intelligence