import os
from werkzeug.utils import secure_filename

def safe_path(base_dir, filename):
    filename = secure_filename(filename)
    path = os.path.abspath(os.path.join(base_dir, filename))

    if not path.startswith(os.path.abspath(base_dir)):
        raise PermissionError("Chemin interdit")

    if not os.path.exists(path):
        raise FileNotFoundError("Fichier inexistant")

    return path
