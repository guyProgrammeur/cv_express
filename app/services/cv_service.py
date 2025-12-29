import uuid, os
from werkzeug.utils import secure_filename
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from .payment_service import validate_payment
from .token_service import generate_token
from flask import current_app

env = Environment(loader=FileSystemLoader("app/templates"))

def generate_cvs(data):
    if not validate_payment(data.get("transaction_id")):
        return {"success": False, "error": "Paiement invalide"}

    templates = [
        ("master", "cv_master.html", "Modèle Classique"),
        ("modern", "cv_master4.html", "Modèle Moderne"),
        ("design", "cv_modern.html", "Modèle Créatif")
    ]

    documents = []
    base = secure_filename(
        f"{data['identite'].get('prenom','')}_{data['identite'].get('nom','')}"
    )

    for tpl_id, tpl_file, name in templates:
        filename = f"CV_{base}_{tpl_id}_{uuid.uuid4().hex[:6]}.pdf"
        path = os.path.join(current_app.config["OUTPUT_DIR"], filename)

        html = env.get_template(tpl_file).render(**data)
        HTML(string=html).write_pdf(path)

        documents.append({
            "id": tpl_id,
            "name": name,
            "download_url": f"/download?token={generate_token(filename, data['transaction_id'])}"
        })

    return {"success": True, "documents": documents}
