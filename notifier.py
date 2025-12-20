import logging
import requests
import os

LOG_FILE = "ops_output.log"

# ---------- LOGGER ----------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

def log_decision(order_id, decision, reason, trace):
    message = (
        f"OrderID={order_id} | "
        f"Decision={decision} | "
        f"Reason={reason} | "
        f"Trace={trace}"
    )
    logging.info(message)

# ---------- SLACK ----------
def send_slack_alert(order_id, decision, reason):
    webhook = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook:
        return  # Slack optional

    payload = {
        "text": f"🚨 *Order Alert*\n"
                f"Order: {order_id}\n"
                f"Decision: {decision}\n"
                f"Reason: {reason}"
    }
    requests.post(webhook, json=payload)
