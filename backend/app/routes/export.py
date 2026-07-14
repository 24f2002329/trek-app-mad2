import os
from flask import Blueprint, jsonify, send_from_directory, g
from app.utils.decorators import token_required
from app.tasks.export import export_user_history_csv

export_bp = Blueprint("export", __name__, url_prefix="/api/user")

@export_bp.route("/export-history", methods=["POST"])
@token_required
def trigger_export():
    user_id = g.current_user.id
    # Trigger task asynchronously
    task = export_user_history_csv.delay(user_id)
    return jsonify({
        "message": "Export started",
        "task_id": task.id
    }), 202

@export_bp.route("/export-status/<task_id>", methods=["GET"])
@token_required
def get_export_status(task_id):
    from celery.result import AsyncResult
    res = AsyncResult(task_id)
    
    if res.state == "SUCCESS":
        result = res.result
        return jsonify({
            "status": "SUCCESS",
            "result": result
        })
    elif res.state == "FAILURE":
        return jsonify({
            "status": "FAILURE",
            "error": str(res.info)
        })
    else:
        return jsonify({
            "status": res.state
        })

@export_bp.route("/download-export/<filename>", methods=["GET"])
@token_required
def download_export(filename):
    # Security check: User can only download their own export file
    expected_prefix = f"user_{g.current_user.id}_"
    if not filename.startswith(expected_prefix) or ".." in filename:
        return jsonify({"message": "Access Denied"}), 403
        
    export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "exports")
    return send_from_directory(export_dir, filename, as_attachment=True)
