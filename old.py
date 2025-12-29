import os
import uuid
import logging
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from werkzeug.utils import secure_filename

# Configuration de base
app = Flask(__name__)
CORS(app)

# Dossiers de configuration
TEMPLATE_DIR = './templates'
OUTPUT_DIR = 'generated_cvs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configuration de Jinja2 (plus efficace pour la prod)
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Logging pour le suivi en production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- LOGIQUE MÉTIER ---

def generate_cv_pdf(data, output_path, template_name):
    """Génère un PDF à partir d'un template spécifique"""
    try:
        template = jinja_env.get_template(template_name)
        # On passe directement le dictionnaire de données
        html_content = template.render(**data)
        
        # Génération du PDF avec WeasyPrint
        HTML(string=html_content, encoding='utf-8').write_pdf(output_path)
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la génération ({template_name}): {str(e)}")
        return False

def validate_transaction(transaction_id):
    """Logique de validation de paiement (à connecter à votre DB/API)"""
    return len(str(transaction_id)) >= 6

def process_cv_request(cv_data, transaction_id):
    if not validate_transaction(transaction_id):
        return {'success': False, 'error': 'Paiement non validé'}

    templates = [
        {"id": "master", "file": "cv_master.html", "name": "Modèle Classique"},
        {"id": "modern", "file": "cv_master4.html", "name": "Modèle Moderne"},
        {"id": "design", "file": "cv_modern.html", "name": "Modèle Créatif"}
    ]

    documents = []
    unique_id = uuid.uuid4().hex[:8]
    base_name = secure_filename(
        f"{cv_data['identite'].get('prenom','')}_{cv_data['identite'].get('nom','')}"
    )

    for tpl in templates:
        filename = f"CV_{base_name}_{tpl['id']}_{unique_id}.pdf"
        path = os.path.join(OUTPUT_DIR, filename)

        if generate_cv_pdf(cv_data, path, tpl['file']):
            documents.append({
                "id": tpl["id"],
                "name": tpl["name"],
                "download_url": f"/download/{filename}"
            })

    if not documents:
        return {'success': False, 'error': 'Aucun document généré'}

    return {
        'success': True,
        'message': 'Les 3 modèles ont été générés',
        'documents': documents
    }

# --- ROUTES API ---

@app.route('/api/generate-cv', methods=['POST'])
def generate_cv_api():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Données JSON manquantes'}), 400

        # On prépare les données proprement
        cv_data = {
            'identite': data.get('identite', {}),
            'accroche': data.get('accroche', ''),
            'etudes': data.get('etudes', []),
            'experiences_pro': data.get('experiences_pro', []),
            'competences': data.get('competences', {}),
            'formations_certifications': data.get('formations_certifications', []),
            'publications_travaux': data.get('publications_travaux', []),
            'centres_interet': data.get('centres_interet', []),
            'qualites_humaines': data.get('qualites_humaines', []),
            'personnes_reference': data.get('personnes_reference', []),
            'signature': data.get('signature', {})
        }
        
        transaction_id = data.get('transaction_id', '')
        
        # Lancement du processus
        result = process_cv_request(cv_data, transaction_id)
        
        if result['success']:
            return jsonify(result), 200
        return jsonify(result), 402 # Payment Required ou Forbidden

    except Exception as e:
        logger.critical(f"Crash API: {str(e)}")
        return jsonify({'success': False, 'error': 'Erreur interne du serveur'}), 500

@app.route('/download/<filename>')
def download_cv(filename):
    """Téléchargement sécurisé des fichiers générés"""
    # secure_filename empêche l'accès à d'autres dossiers via ../
    safe_name = secure_filename(filename)
    filepath = os.path.abspath(os.path.join(OUTPUT_DIR, safe_name))
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({'success': False, 'error': 'Fichier expiré ou inexistant'}), 404

# --- RUN ---

if __name__ == '__main__':
    # En prod, utilisez Gunicorn ou Waitress au lieu de app.run
    app.run(debug=True, port=5000, host='0.0.0.0')