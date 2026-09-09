from flask import Flask, jsonify
app = Flask(__name__)

# Database giả lập
ORDERS = {
    "ord_1": {"id": "ord_1", "item": "Item_1", "status": "pending"},
    "ord_2": {"id": "ord_2", "item": "Item_2", "status": "shipped"},
}

@app.route("/orders/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = ORDERS.get(order_id)

    # 404 Not Found: Resource không tồn tại
    if order is None:
        return jsonify({"error": "not found"}), 404

    # 409 Conflict: Vi phạm quy tắc (đã giao hàng thì không cho hủy)
    if order["status"] in ("shipped", "delivered"):
        return jsonify({"error": "cannot delete shipped order"}), 409

    # 204 No Content: Xóa thành công, phản hồi không chứa body
    ORDERS.pop(order_id, None)
    return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)