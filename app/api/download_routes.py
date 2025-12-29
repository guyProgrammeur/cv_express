from flask import Blueprint, request, send_file, jsonify, current_app
from itsdangerous import BadSignature, SignatureExpired
from ..services.token_service import verify_token
from ..utils.file_utils import safe_path

download_bp = Blueprint("download", __name__)

@download_bp.route("/download")
def download():
    token = request.args.get("token")
    if not token:
        return jsonify(error="Token manquant"), 401

    try:
        data = verify_token(token)
        filepath = safe_path(
            current_app.config["OUTPUT_DIR"],
            data["filename"]
        )

        return send_file(filepath, as_attachment=True)

    except SignatureExpired:
        return jsonify(error="Lien expiré"), 410
    except BadSignature:
        return jsonify(error="Lien invalide"), 403
