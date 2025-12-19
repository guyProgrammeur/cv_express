import uvicorn
import base64
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# --- INITIALISATION ---
app = FastAPI(title="CV Express API")

# Permettre les connexions (CORS) - Utile si tu testes depuis différents endroits
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration de Jinja2 pour trouver les templates HTML
env = Environment(loader=FileSystemLoader('templates'))


# --- MODÈLES DE DONNÉES (Ce qu'on attend de Tally/n8n) ---
# Ces classes définissent la structure exacte du JSON que tu dois envoyer

class Experience(BaseModel):
    poste: str = "Poste non défini"
    entreprise: str = "Entreprise non définie"
    debut: str = ""
    fin: str = ""
    description: str = ""

class Formation(BaseModel):
    diplome: str
    ecole: str
    annee: str

class CVRequest(BaseModel):
    # Infos Perso
    prenom: str
    nom: str
    email: str
    telephone: str
    adresse: str = "Kinshasa, RDC"
    titre_job: str = "Professionnel"
    profil_resume: str = ""
    
    # URL de la photo (envoyée par Tally)
    photo_url: Optional[str] = None
    
    # Listes (Si vide, on met une liste vide par défaut)
    competences: List[str] = []
    langues: List[str] = []
    experiences: List[Experience] = []
    formations: List[Formation] = []


# --- FONCTION UTILITAIRE : GESTION IMAGE ---
def download_image_as_base64(url: str):
    """
    Télécharge l'image depuis l'URL Tally et la convertit en texte (Base64).
    C'est INDISPENSABLE pour que WeasyPrint puisse l'imprimer sans erreur.
    """
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            # On convertit les bytes de l'image en chaine base64
            encoded_string = base64.b64encode(response.content).decode("utf-8")
            # On retourne le format prêt pour le HTML <img src="...">
            return f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e:
        print(f"Erreur téléchargement image: {e}")
    
    return None # Si ça échoue, on renvoie rien


# --- ENDPOINT API ---
@app.post("/generate-cv")
async def generate_cv(data: CVRequest):
    try:
        print(f"Demande reçue pour : {data.prenom} {data.nom}")

        # 1. Traitement de la photo
        final_photo_code = None
        if data.photo_url:
            final_photo_code = download_image_as_base64(data.photo_url)

        # 2. Chargement du Template HTML
        template = env.get_template('cv_master.html')

        # 3. Remplissage du HTML avec les données (Rendering)
        html_content = template.render(
            prenom=data.prenom,
            nom=data.nom,
            email=data.email,
            telephone=data.telephone,
            adresse=data.adresse,
            titre_job=data.titre_job,
            profil_resume=data.profil_resume,
            competences=data.competences,
            langues=data.langues,
            experiences=data.experiences,
            formations=data.formations,
            photo_url=final_photo_code  # On passe le code Base64 ici
        )

        pdf_file = HTML(string=html_content).write_pdf()

        # 5. Renvoi du PDF au client (n8n ou navigateur)
        filename = f"CV_{data.prenom}_{data.nom}.pdf".replace(" ", "_")
        
        return Response(
            content=pdf_file,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        print(f"ERREUR CRITIQUE: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur de génération: {str(e)}")

# --- LANCEMENT SERVEUR ---
if __name__ == "__main__":
    # Reload=True permet de redémarrer le serveur quand tu modifies le code
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)