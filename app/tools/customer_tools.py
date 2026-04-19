import json

def get_customer(email):
    with open("app/data/customers.json") as f:
        customers = json.load(f)

    return next((c for c in customers if c["email"] == email), {"error": "Customer not found"})