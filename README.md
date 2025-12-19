# company_project
🧠 AI Ops Assistant – Order Intelligence System (LangGraph)
Overview

This project implements an AI-powered Operations Assistant that automatically evaluates incoming orders based on inventory availability, daily production capacity, and order priority.
The system is built using LangGraph to model real operational decision-making in a structured, state-driven workflow.

**Features**

* Automatically reads incoming orders
* Validates inventory availability
* Enforces daily production capacity constraints
* Handles urgent vs normal priorities
* Prevents negative inventory
* Generates clear operational decisions:

      .APPROVE

      .DELAY

      .SPLIT

      .ESCALATE

* Provides human-readable reasoning for every decision
* Self-healing system (auto-creates required data files if missing)
* Console output acts as an operational log

**Tech Stack**

* Python 3.9+
* LangGraph
* Pandas
Project Structure
company/

├── app.py
└── data/
    ├── orders.csv
    └── inventory.csv


 **Note:**
If the data/ folder or CSV files are missing, the system automatically creates them on first run.

**Business Rules Implemented**

* Maximum production capacity: 200 units per day
* No negative inventory allowed
* Urgent orders may escalate but cannot violate constraints
* Orders exceeding stock are split
* Orders exceeding capacity are delayed or escalated

**How the System Works**

* LangGraph initializes the workflow
* Orders and inventory are loaded into state

* Each order is evaluated against:
       . Available inventory

       .  Daily production capacity

       . Priority level

* A decision and reason are generated
* Results are logged to the console
* Graph terminates cleanly

**Installation & Run Instructions**
1️ Create virtual environment (optional)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

2️ Install dependencies
pip install pandas langgraph

3️ Run the application
python app.py

**Sample Output**
ORD001 → APPROVE
Reason: Sufficient stock and capacity

ORD003 → SPLIT
Reason: Only 250 units available, rest delayed

ORD007 → ESCALATE
Reason: Daily production capacity exceeded

**Failure Handling & Edge Cases**

* Missing CSV files → auto-generated
* Dirty CSV headers → cleaned automatically
* Capacity overload → delayed or escalated
* Zero inventory → escalated
* Safe termination (no infinite loops)

**Assumptions**

* Orders are processed sequentially
* Production capacity resets daily
* Inventory is shared across days
* Console output is sufficient for Level-1 evaluation

**Author**

Satendra
AI / ML Engineer
LangGraph • Automation • Operations Intelligence