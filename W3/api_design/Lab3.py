import base64
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# Dữ liệu giả lập
orders_db = [
    {"id": 1, "status": "paid", "customer_id": 101, "total": 150.0},
    {"id": 2, "status": "pending", "customer_id": 102, "total": 200.0},
    {"id": 3, "status": "paid", "customer_id": 101, "total": 50.0},
    {"id": 4, "status": "cancelled", "customer_id": 103, "total": 300.0},
    {"id": 5, "status": "paid", "customer_id": 104, "total": 120.0},
    {"id": 6, "status": "pending", "customer_id": 101, "total": 75.0},
    {"id": 7, "status": "paid", "customer_id": 102, "total": 400.0},
]

def encode_cursor(order_id):
    return base64.b64encode(str(order_id).encode('utf-8')).decode('utf-8')

def decode_cursor(cursor):
    try:
        return int(base64.b64decode(cursor).decode('utf-8'))
    except Exception:
        raise ValueError("Cursor không hợp lệ hoặc bị hỏng")

@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        # 1. Lọc
        status = request.args.get('status')
        customer_id = request.args.get('customer_id')
        
        filtered_orders = orders_db
        if status:
            filtered_orders = [o for o in filtered_orders if o['status'] == status]
        if customer_id:
            filtered_orders = [o for o in filtered_orders if str(o['customer_id']) == customer_id]
        
        # # 2. Sắp xếp 
        # sort_field = request.args.get('sort', 'id')
        # reverse = False
        # if sort_field.startswith('-'):
        #     reverse = True
        #     sort_field = sort_field[1:]
        
        # if sort_field in ['id', 'status', 'customer_id', 'total']:
        #     filtered_orders.sort(key=lambda x: x[sort_field], reverse=reverse)

        
        # 2. Sắp xếp (Hỗ trợ Sort bằng Composite Key)
        sort_field = request.args.get('sort', 'id')
        reverse = sort_field.startswith('-')
        sort_key = sort_field[1:] if reverse else sort_field
        
        if sort_key not in ['id', 'status', 'customer_id', 'total']:
            sort_key = 'id'
        
        # Sắp xếp ưu tiên field yêu cầu, tie-breaker là 'id' để đảm bảo tính ổn định
        filtered_orders.sort(key=lambda x: (x[sort_key], x['id']), reverse=reverse)

        # 3. Phân trang bằng Cursor
        cursor = request.args.get('cursor')
        limit = int(request.args.get('limit', 5))
        
        start_idx = 0
        if cursor:
            last_id = decode_cursor(cursor)
            for i, order in enumerate(filtered_orders):
                if order['id'] == last_id:
                    start_idx = i + 1
                    break

        paginated_orders = filtered_orders[start_idx:start_idx + limit]

        # Tạo next_cursor nếu còn dữ liệu
        next_cursor = None
        if len(filtered_orders) > start_idx + limit:
            last_item = paginated_orders[-1]
            next_cursor = encode_cursor(last_item['id'])

        # 4. Trích xuất trường
        fields = request.args.get('fields')
        if fields:
            field_list = fields.split(',')
            valid_keys = {"id", "status", "customer_id", "total"}
            
            for f in field_list:
                if f not in valid_keys:
                    return make_response(jsonify({
                        "type": "about:blank",
                        "title": "Bad Request",
                        "detail": f"Trường dữ liệu '{f}' không tồn tại.",
                        "status": 400,
                        "instance": request.path
                    }), 400, {'Content-Type': 'application/problem+json'})

            result = [{k: v for k, v in o.items() if k in field_list} for o in paginated_orders]
        else:
            result = paginated_orders

        return jsonify({
            "data": result,
            "pagination": {
                "next_cursor": next_cursor,
                "limit": limit
            }
        }), 200

    except ValueError as e:
        # Xử lý lỗi Cursor hỏng
        return make_response(jsonify({
            "type": "about:blank",
            "title": "Bad Request",
            "detail": str(e),
            "status": 400,
            "instance": request.path
        }), 400, {'Content-Type': 'application/problem+json'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)