from flask import Flask, jsonify, request
from flasgger import Swagger
from datetime import datetime

app = Flask(__name__)
app.config['SWAGGER'] = {'openapi': '3.0.3'}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'openapi',
            "route": '/openapi.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}

swagger = Swagger(app, config=swagger_config, template_file='openapi.yaml')

# Database
tasks_db = []
current_id = 1

def is_valid_date(date_str):
    """Kiểm tra dueDate có đúng định dạng YYYY-MM-DD không"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@app.route('/v1/tasks', methods=['GET'])
def list_tasks():
    return jsonify(tasks_db), 200

@app.route('/v1/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks_db:
        if task["id"] == task_id:
            return jsonify(task), 200
    return jsonify({"description": "Không tìm thấy resource"}), 404

@app.route('/v1/tasks', methods=['POST'])
def create_task():
    global current_id
    data = request.json or {}
    
    # 1. Validate Enum
    if "priority" in data and data["priority"] not in ["low", "normal", "high"]:
        return jsonify({"description": "Priority không hợp lệ (chỉ nhận low, normal, high)", "status": 422}), 422
        
    # 2. Validate Date
    if "dueDate" in data and data["dueDate"] is not None:
        if not is_valid_date(data["dueDate"]):
            return jsonify({"description": "dueDate phải theo định dạng YYYY-MM-DD (VD: 2026-09-13)", "status": 422}), 422
        
    new_task = {
        "id": current_id,
        "title": data.get("title", "New Task"),
        "status": "open",
        "priority": data.get("priority", "normal"),
        "dueDate": data.get("dueDate", None),
        "assigneeId": data.get("assigneeId", None)
    }
    
    tasks_db.append(new_task)
    current_id += 1
    return jsonify(new_task), 201

@app.route('/v1/tasks/<int:task_id>', methods=['PATCH'])
def patch_task(task_id):
    data = request.json or {}
    
    # 1. Validate Enum
    if "status" in data and data["status"] not in ["open", "done"]:
        return jsonify({"description": "Status không hợp lệ (chỉ nhận open, done)", "status": 422}), 422
    if "priority" in data and data["priority"] not in ["low", "normal", "high"]:
        return jsonify({"description": "Priority không hợp lệ (chỉ nhận low, normal, high)", "status": 422}), 422
        
    # 2. Validate Date
    if "dueDate" in data and data["dueDate"] is not None:
        if not is_valid_date(data["dueDate"]):
            return jsonify({"description": "dueDate phải theo định dạng YYYY-MM-DD (VD: 2026-09-13)", "status": 422}), 422

    for task in tasks_db:
        if task["id"] == task_id:
            if "title" in data:
                task["title"] = data["title"]
            if "priority" in data:
                task["priority"] = data["priority"]
            if "status" in data:
                task["status"] = data["status"]
            if "dueDate" in data:
                task["dueDate"] = data["dueDate"]
            if "assigneeId" in data:
                task["assigneeId"] = data["assigneeId"]
            return jsonify(task), 200
            
    return jsonify({"description": "Không tìm thấy resource", "status": 404}), 404

@app.route('/v1/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks_db
    tasks_db = [task for task in tasks_db if task["id"] != task_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)