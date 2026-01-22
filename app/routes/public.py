from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from app.db import (
    get_db_connection,
    messages_collection,
    projects_collection,
    certificates_collection
)


public_routes = Blueprint('public_routes', __name__)


# 🎯 save contact message
@public_routes.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()

        if not data:   # ✅ FIX 2
            return jsonify({
                "success": False,
                "message": "No JSON data received"
            }), 400

        messages_collection.insert_one({
            "name": data.get("name"),
            "email": data.get("email"),
            "message": data.get("message"),
            "created_at": datetime.utcnow(),
            "is_read": False
        })

        return jsonify({
            "success": True,
            "message": "Message sent successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# 🎯 get projects
@public_routes.route('/projects', methods=['GET'])
def get_projects():
    data = list(projects_collection.find())
    for p in data:
        p["_id"] = str(p["_id"])
    return jsonify(data), 200


# 🎯 get certificates
@public_routes.route('/certificates', methods=['GET'])
def get_certificates():
    data = list(certificates_collection.find())
    for c in data:
        c["_id"] = str(c["_id"])
    return jsonify(data), 200
