import pandas as pd
from pathlib import Path
from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from notifier import log_decision, send_slack_alert

MAX_DAILY_CAPACITY = 200

class OpsState(TypedDict):
    orders: List[Dict]
    inventory: Dict[str, int]
    daily_capacity: Dict[str, int]
    results: List[Dict]

def load_data(state: OpsState) -> OpsState:
    base = Path(__file__).parent
    data = base / "data"

    orders_df = pd.read_csv(data / "orders.csv")
    inventory_df = pd.read_csv(data / "inventory.csv")

    orders_df.columns = orders_df.columns.str.strip()
    inventory_df.columns = inventory_df.columns.str.strip()

    inventory = dict(zip(
        inventory_df["ProductCode"],
        inventory_df["AvailableStock"]
    ))

    return {
        "orders": orders_df.to_dict("records"),
        "inventory": inventory,
        "daily_capacity": {},
        "results": []
    }

def decision_engine(state: OpsState) -> OpsState:
    for order in state["orders"]:
        oid = order["OrderID"]
        product = order["ProductCode"]
        qty = int(order["Quantity"])
        date = order["OrderDate"]
        priority = order["Priority"].lower()

        stock = state["inventory"].get(product, 0)
        used = state["daily_capacity"].get(date, 0)
        remaining = MAX_DAILY_CAPACITY - used

        trace = []
        trace.append(f"Stock={stock}")
        trace.append(f"UsedCapacity={used}")

        if stock <= 0:
            decision, reason = "ESCALATE", "No inventory available"

        elif qty <= stock and qty <= remaining:
            decision, reason = "APPROVE", "Sufficient stock and capacity"
            state["inventory"][product] -= qty
            state["daily_capacity"][date] = used + qty

        elif qty > stock:
            decision, reason = "SPLIT", f"Only {stock} units available"
            state["inventory"][product] = 0

        else:
            decision = "ESCALATE" if priority == "urgent" else "DELAY"
            reason = "Daily production capacity exceeded"

        trace.append(f"Decision={decision}")

        log_decision(oid, decision, reason, " | ".join(trace))

        if decision in ["ESCALATE"]:
            send_slack_alert(oid, decision, reason)

        state["results"].append({
            "OrderID": oid,
            "Decision": decision,
            "Reason": reason,
            "Trace": trace
        })

    return state

def output_results(state: OpsState) -> OpsState:
    print("\n===== AI OPS ASSISTANT OUTPUT =====\n")
    for r in state["results"]:
        print(f"{r['OrderID']} → {r['Decision']}")
        print(f"Reason: {r['Reason']}")
        print(f"Trace: {r['Trace']}\n")
    return state

graph = StateGraph(OpsState)
graph.add_node("load", load_data)
graph.add_node("decide", decision_engine)
graph.add_node("output", output_results)

graph.set_entry_point("load")
graph.add_edge("load", "decide")
graph.add_edge("decide", "output")
graph.add_edge("output", END)

app = graph.compile()

if __name__ == "__main__":
    app.invoke({})
