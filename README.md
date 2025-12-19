Parfait, voici un exemple de **README complet et structuré** pour ton projet `cv_express` sur GitHub :

---

# CV Express

Générateur de CV en PDF utilisant **FastAPI**, **Jinja2** et **WeasyPrint**.

---

## Description

`CV Express` est une application web Python qui permet de générer des CV modernes à partir de templates HTML.
Elle utilise **FastAPI** pour le backend, **Jinja2** pour le rendu des templates et **WeasyPrint** pour exporter les CV en PDF.

Le projet inclut plusieurs modèles de CV prêts à l'emploi.

---

## Fonctionnalités

* Génération de CV à partir de templates HTML.
* Export en PDF via WeasyPrint.
* Support de plusieurs modèles de CV (`model1.html`, `model2.html`, …).
* Gestion facile des templates via le dossier `templates`.

---

## Prérequis

* Python 3.9+
* Pip
* FastAPI, Uvicorn, Jinja2, WeasyPrint, Pydantic, Requests, Python-multipart
* GTK Runtime pour WeasyPrint (Windows) : [gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe](https://release-assets.githubusercontent.com/github-production-release-asset/24536695/d850ba58-8e13-47ad-9387-5be188ed8d31?sp=r&sv=2018-11-09&sr=b&spr=https&se=2025-12-11T11%3A04%3A58Z&rscd=attachment%3B+filename%3Dgtk3-runtime-3.24.31-2022-01-04-ts-win64.exe&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2025-12-11T10%3A04%3A22Z&ske=2025-12-11T11:04:58Z&sks=b&skv=2018-11-09&sig=SR%2BZ5UyTLnf94RqNQOR1jaMmSc8d5esD0qhQmdJMCrM%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc2NTQ0OTgwNCwibmJmIjoxNzY1NDQ4MDA0LCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.R6KuJ1A6fp6diSHP_0AcIfDwthY2o00WFYWkC3dtvrw&response-content-disposition=attachment%3B%20filename%3Dgtk3-runtime-3.24.31-2022-01-04-ts-win64.exe&response-content-type=application%2Foctet-stream)

---

## Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/guyProgrammeur/cv_express.git
cd cv_express
```

2. Créer un environnement virtuel :

```bash
python -m venv venv
```

3. Activer l’environnement :

* Windows :

```powershell
.\venv\Scripts\activate
```

* Linux / Mac :

```bash
source venv/bin/activate
```

4. Installer les dépendances :

```bash
pip install -r requirements.txt
```

5. Installer GTK Runtime (Windows uniquement) pour WeasyPrint.

---

## Utilisation

1. Lancer le serveur FastAPI :

```bash
uvicorn main:app --reload
```

2. Ouvrir le navigateur à l’adresse :

```
http://127.0.0.1:8000
```

3. Générer un CV depuis les templates.

---

## Structure du projet

```
cv_express/
├─ templates/          # Templates HTML des CV
│  ├─ cv_master.html
│  ├─ model1.html
│  ├─ model2.html
│  └─ ...
├─ main.py             # Application FastAPI
├─ requirements.txt    # Dépendances Python
├─ README.md           # Documentation
└─ __pycache__/        # Fichiers Python compilés (ignorer)
```

---

## Contributions

Les contributions sont les bienvenues !
Merci de forker le dépôt et soumettre vos pull requests.

---

## Licence

Ce projet est sous licence **MIT**.

