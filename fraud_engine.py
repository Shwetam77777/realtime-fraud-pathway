import time
import random
import datetime

AML_RULES = [
    {"id": 1, "rule": "Transactions above ₹5000 during night hours are high risk."},
    {"id": 2, "rule": "Multiple rapid transactions indicate potential account takeover."},
    {"id": 3, "rule": "Foreign country transactions with high amount may be fraudulent."},
    {"id": 4, "rule": "Normal transactions have no risk indicators."}
]

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

def analyze_transaction(tx, recent_tx):
    amount = tx["amount"]
    hour = tx["hour"]
    user = tx["user_id"]
    country = tx["country"]

    if amount > 5000 and (hour < 6 or hour > 22):
        reason = "High transaction amount during unusual night hours."
        score = 90
    elif sum(1 for t in recent_tx if t["user_id"] == user) >= 3:
        reason = "Rapid repeated transactions from the same user."
        score = 75
    elif country != "IN" and amount > 3000:
        reason = "Foreign country high transaction amount detected."
        score = 85
    else:
        reason = "Normal transaction with no risk indicators."
        score = 10

    aml_rule = match_aml_rule(reason)
    return {"score": score, "reason": reason, "aml_rule": aml_rule}

def stream_transactions():
    users = ["U1", "U2", "U3", "U4"]
    countries = ["IN", "IN", "IN", "US", "UK"]
    tx_id = 1
    recent_tx = []

    while True:
        tx = {
            "transaction_id": tx_id,
            "user_id": random.choice(users),
            "amount": random.randint(100, 9000),
            "country": random.choice(countries),
            "hour": datetime.datetime.now().hour
        }

        analysis = analyze_transaction(tx, recent_tx)
        recent_tx.append(tx)
        if len(recent_tx) > 10:
            recent_tx.pop(0)

        print("\n🔹 Transaction:", tx)
        print("🚨 Fraud Score:", analysis["score"])
        print("📌 Reason:", analysis["reason"])
        print(f"📘 AML Rule #{analysis['aml_rule']['id']}: {analysis['aml_rule']['rule']}")

        tx_id += 1
        time.sleep(1)

if __name__ == "__main__":
    stream_transactions()
