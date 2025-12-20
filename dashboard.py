import pandas as pd
import streamlit as st
from pathlib import Path
from datetime import datetime
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Ops Dashboard",
    layout="wide"
)

st.title("📊 AI Ops Assistant – Order Intelligence Dashboard")

# ---------------- PATH HANDLING ----------------
BASE_DIR = Path(__file__).parent
LOG_FILE = BASE_DIR / "ops_output.log"

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")
auto_refresh = st.sidebar.checkbox("Auto refresh (every 5 sec)", value=True)

# ---------------- FILE CHECK ----------------
if not LOG_FILE.exists():
    st.warning("⚠️ No execution log found.")
    st.info("Run `python app.py` first to generate decisions.")
    st.stop()

# ---------------- LOAD LOG ----------------
log_df = pd.read_csv(
    LOG_FILE,
    sep="\\|",
    engine="python",
    names=["Timestamp", "Message"]
)

log_df["Timestamp"] = log_df["Timestamp"].str.strip()
log_df["Message"] = log_df["Message"].str.strip()

# ---------------- PARSE MESSAGE ----------------
def extract_value(text, key):
    for part in text.split("|"):
        if key in part:
            return part.split("=")[1].strip()
    return ""

log_df["OrderID"] = log_df["Message"].apply(lambda x: extract_value(x, "OrderID"))
log_df["Decision"] = log_df["Message"].apply(lambda x: extract_value(x, "Decision"))
log_df["Reason"] = log_df["Message"].apply(lambda x: extract_value(x, "Reason"))
log_df["Trace"] = log_df["Message"].apply(lambda x: extract_value(x, "Trace"))

# ---------------- FILTER ----------------
decision_filter = st.sidebar.multiselect(
    "Filter by Decision",
    options=["APPROVE", "DELAY", "SPLIT", "ESCALATE"],
    default=["APPROVE", "DELAY", "SPLIT", "ESCALATE"]
)

filtered_df = log_df[log_df["Decision"].isin(decision_filter)]

# ---------------- METRICS ----------------
st.subheader("📈 Summary")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Approved", (filtered_df["Decision"] == "APPROVE").sum())
col2.metric("Delayed", (filtered_df["Decision"] == "DELAY").sum())
col3.metric("Split", (filtered_df["Decision"] == "SPLIT").sum())
col4.metric("Escalated", (filtered_df["Decision"] == "ESCALATE").sum())

# ---------------- TABLE ----------------
st.subheader("📋 Order Execution Log")
st.dataframe(
    filtered_df[["Timestamp", "OrderID", "Decision", "Reason", "Trace"]],
    use_container_width=True
)

# ---------------- EXPORT ----------------
st.subheader("⬇️ Export")
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name=f"ops_decisions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)

# ---------------- AUTO REFRESH (SAFE) ----------------
if auto_refresh:
    time.sleep(5)
    st.rerun()
