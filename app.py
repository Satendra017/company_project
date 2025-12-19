import pandas as pd
from pathlib import Path
from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END

# ================= CONFIG =================
MAX_DAILY_CAPACITY = 200

# ================= STATE =================
class OpsState(TypedDict):
    orders: List[Dict]
    inventory: Dict[str, int]
    daily_capacity: Dict[str, int]
    results: List[Dict]

# ================= ENSURE DATA EXISTS =================
def ensure_data_files():
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    data_dir.mkdir(exist_ok=True)

    orders_path = data_dir / "orders.csv"
    inventory_path = data_dir / "inventory.csv"

    if not orders_path.exists():
        orders_path.write_text(
            "OrderID,ProductCode,Quantity,OrderDate,Priority\n"
            "ORD001,K1001,120,2025-01-02,Normal\n"
            "ORD002,K1005,80,2025-01-02,Urgent\n"
            "ORD003,K1010,300,2025-01-03,Normal\n"
            "ORD004,K1001,60,2025-01-03,Urgent\n"
            "ORD005,K1022,150,2025-01-04,Normal\n"
            "ORD006,K1005,200,2025-01-04,Normal\n"
            "ORD007,K1010,90,2025-01-04,Urgent\n"
        )

    if not inventory_path.exists():
        inventory_path.write_text(
            "ProductCode,AvailableStock\n"
            "K1001,140\n"
            "K1005,180\n"
            "K1010,250\n"
            "K1022,100\n"
        )

    return orders_path, inventory_path

# ================= LOAD DATA NODE =================
def load_data(state: OpsState) -> OpsState:
    orders_path, inventory_path = ensure_data_files()

    orders_df = pd.read_csv(orders_path)
    inventory_df = pd.read_csv(inventory_path)

    orders_df.columns = orders_df.columns.str.strip()
    inventory_df.columns = inventory_df.columns.str.strip()

    inventory = {
        row["ProductCode"]: int(row["AvailableStock"])
        for _, row in inventory_df.iterrows()
    }

    return {
        "orders": orders_df.to_dict(orient="records"),
        "inventory": inventory,
        "daily_capacity": {},
        "results": []
    }

# ================= DECISION ENGINE =================
def decision_engine(state: OpsState) -> OpsState:
    for order in state["orders"]:
        oid = order["OrderID"]
        product = order["ProductCode"]
        qty = int(order["Quantity"])
        date = order["OrderDate"]
        priority = order["Priority"].strip().lower()

        stock = state["inventory"].get(product, 0)
        used = state["daily_capacity"].get(date, 0)
        remaining = MAX_DAILY_CAPACITY - used

        if stock <= 0:
            decision, reason = "ESCALATE", "No inventory available"

        elif qty <= stock and qty <= remaining:
            decision, reason = "APPROVE", "Sufficient stock and capacity"
            state["inventory"][product] -= qty
            state["daily_capacity"][date] = used + qty

        elif qty > stock:
            decision, reason = "SPLIT", f"Only {stock} units available, rest delayed"
            state["inventory"][product] = 0

        else:
            decision = "ESCALATE" if priority == "urgent" else "DELAY"
            reason = "Daily production capacity exceeded"

        state["results"].append({
            "OrderID": oid,
            "Decision": decision,
            "Reason": reason
        })

    return state

# ================= OUTPUT =================
def output_results(state: OpsState) -> OpsState:
    print("\n===== AI OPS ASSISTANT (LangGraph) OUTPUT =====\n")
    for r in state["results"]:
        print(f"{r['OrderID']} → {r['Decision']}")
        print(f"Reason: {r['Reason']}\n")
    return state

# ================= BUILD GRAPH =================
graph = StateGraph(OpsState)
graph.add_node("load_data", load_data)
graph.add_node("decision_engine", decision_engine)
graph.add_node("output", output_results)

graph.set_entry_point("load_data")
graph.add_edge("load_data", "decision_engine")
graph.add_edge("decision_engine", "output")
graph.add_edge("output", END)

app = graph.compile()

# ================= RUN =================
if __name__ == "__main__":
    app.invoke({})

