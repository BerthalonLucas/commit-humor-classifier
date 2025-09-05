#!/usr/bin/env python3
"""
🌐 Application Web Locale - Affichage des Commits Drôles
=======================================================

Cette application lit périodiquement un fichier JSON de commits et
affiche ceux jugés drôles par le modèle existant dans une interface Web.
"""

import os
import json
import threading
import time
import logging
from hashlib import md5
from datetime import datetime
from typing import List, Dict

from flask import Flask, jsonify, render_template

from commit_humor_classifier import CommitHumorClassifier

app = Flask(__name__)

# Liste des commits drôles déjà détectés
FUNNY_COMMITS: List[Dict] = []
# Ensemble des IDs de commits déjà traités
PROCESSED_IDS = set()
# Chemin du fichier JSON à surveiller
JSON_FILE = os.environ.get("COMMITS_JSON", "commits.json")
# Intervalle de rafraîchissement (secondes)
UPDATE_INTERVAL = 60
# Mode debug activé/désactivé via variable d'environnement
DEBUG_MODE = os.environ.get("DEBUG_PREDICTIONS", "false").lower() == "true"

# Configuration du logging pour le debug
logger = None
if DEBUG_MODE:
    # Configuration spécifique pour éviter les conflits avec Flask
    logger = logging.getLogger('commit_debug')
    logger.setLevel(logging.INFO)
    
    # Créer un handler pour la console si pas déjà présent
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - DEBUG - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False  # Éviter la duplication avec le logger root

# Initialisation du classificateur
classifier = CommitHumorClassifier(seuil=0.65)
classifier.load_model()

# Message de confirmation du mode debug
if DEBUG_MODE and logger:
    logger.info("🐛 Mode debug activé - Les prédictions seront loggées")


def get_commit_id(commit: Dict) -> str:
    """Retourne un identifiant unique pour le commit."""
    if "sha" in commit:
        return commit["sha"]
    content = f"{commit.get('message', '')}{commit.get('author', {}).get('date', '')}"
    return md5(content.encode()).hexdigest()


def read_commits() -> List[Dict]:
    """Lit le fichier JSON et renvoie la liste de commits."""
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            commits = json.load(f)
            if isinstance(commits, list):
                return commits
    except Exception:
        pass
    return []


def update_commits_loop() -> None:
    """Boucle de mise à jour périodique."""
    while True:
        commits = read_commits()
        for commit in commits:
            cid = get_commit_id(commit)
            if cid in PROCESSED_IDS:
                continue
            message = commit.get("message", "").strip()
            if not message:
                PROCESSED_IDS.add(cid)
                continue
            try:
                result = classifier.predict(message)
                # Log de debug sur une seule ligne
                if DEBUG_MODE and logger:
                    status = "FUNNY" if result["is_funny"] else "NORMAL"
                    logger.info(f"PREDICTION: [{status}] P={result['probability']:.3f} | {message[:80]}{'...' if len(message) > 80 else ''}")
            except Exception as e:
                # En cas d'erreur de prédiction, on ignore le commit
                if DEBUG_MODE and logger:
                    logger.error(f"PREDICTION ERROR: {str(e)[:50]} | {message[:50]}{'...' if len(message) > 50 else ''}")
                PROCESSED_IDS.add(cid)
                continue
            if result["is_funny"]:
                FUNNY_COMMITS.append({
                    "id": cid,
                    "message": message,
                    "probability": result["probability"],
                    "date": commit.get("author", {}).get("date", datetime.now().isoformat())
                })
            PROCESSED_IDS.add(cid)
        time.sleep(UPDATE_INTERVAL)


def start_background_thread():
    thread = threading.Thread(target=update_commits_loop, daemon=True)
    thread.start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/funny_commits")
def funny_commits():
    # On renvoie les commits drôles les plus récents en premier
    commits = sorted(FUNNY_COMMITS, key=lambda x: x["date"], reverse=True)
    return jsonify(commits)


if __name__ == "__main__":
    start_background_thread()
    app.run(host="0.0.0.0", port=5000, debug=False)
