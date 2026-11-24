def v1_create_order(body):
    return {
        "order_id": "ord_v1_001",
        "account_id": body.get("account_id"),
        "version": "v1",
        "status": "created_legacy"
    }

def v2_create_order(body):
    return {
        "order_id": "ord_v2_001",
        "account_id": body.get("account_id"),
        "version": "v2",
        "status": "created_v2",
        "metadata": {"engine": "new_pipeline"}
    }