import streamlit as st
import time
import random
import datetime

st.set_page_config(page_title="Real-Time Fraud Detection", layout="wide")
st.title("🔍 Real-Time AI Fraud Detection Dashboard")

AML_RULES = [
    {"id": 1, "rule": "Transactions above ₹5000 during night hours are high risk."},
    {"id": 2, "rule": "Multiple rapid transactions indicate account takeover."},
    {"id": 3, "rule": "Foreign high-amount transactions may be fraudulent."},
    {"id": 4, "rule": "Normal transactions with no suspicious patterns."}
]

placeholder = st.empty()
recent_tx = []

def match_aml_rule(reason):
    reason = reason.lower()
    for rule in AML_RULES:
        if "night" in reason and "night" in rule["rule"].lower():
            return rule
        if "rapid" in reason and "rapid" in rule["rule"].lower():
            return rule
        if "foreign" in reason and "foreign" in rule["rule"].lower():
            return rule
    return AML_RULES[-1]

def analyze(tx):
    amount, hour, user, country = tx["amount"], tx["hour"], tx["user_id"], tx["country"]

    if amount > 5000 and (hour < 6 or hour > 22):
        return 90, "High transaction during night hours."
    elif sum(1 for t in recent_tx if t["user_id"] == user) >= 3:
        return 75, "Rapid repeated transactions."
    elif country != "IN" and amount > 3000:
        return 85, "Foreign high-amount transaction detected."
    return 10, "Normal transaction."

tx_id = 1
while True:
    tx = {
        "transaction_id": tx_id,
        "user_id": random.choice(["U1", "U2", "U3"]),
        "amount": random.randint(100, 9000),
        "country": random.choice(["IN", "IN", "US", "UK"]),
        "hour": datetime.datetime.now().hour
    }

    score, reason = analyze(tx)
    aml = match_aml_rule(reason)

    placeholder.write({
        "transaction": tx,
        "fraud_score": score,
        "reason": reason,
        "AML_rule": aml
    })

    recent_tx.append(tx)
    if len(recent_tx) > 10:
        recent_tx.pop(0)

    tx_id += 1
    time.sleep(1)
