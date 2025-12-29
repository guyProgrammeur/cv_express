from flask import Blueprint, request, jsonify
from ..services.cv_service import generate_cvs

cv_bp = Blueprint("cv", __name__)

@cv_bp.route("/generate-cv", methods=["POST"])
def generate_cv():
    data = request.get_json()
    if not data:
        return jsonify(success=False, error="JSON manquant"), 400

    result = generate_cvs(data)
    return jsonify(result), (200 if result["success"] else 402)
