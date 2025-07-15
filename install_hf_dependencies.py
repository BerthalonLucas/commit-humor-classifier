#!/usr/bin/env python3
"""
Script d'installation des dépendances pour l'upload sur Hugging Face
"""

import subprocess
import sys
import os

def install_package(package):
    """Installer un package avec pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_package(package):
    """Vérifier si un package est installé"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def main():
    print("🔧 Installation des dépendances pour Hugging Face...")
    
    # Packages requis
    packages = [
        "huggingface_hub",
        "transformers",
        "torch",
        "datasets"
    ]
    
    for package in packages:
        if check_package(package.replace("-", "_")):
            print(f"✅ {package} déjà installé")
        else:
            print(f"📦 Installation de {package}...")
            if install_package(package):
                print(f"✅ {package} installé avec succès")
            else:
                print(f"❌ Erreur lors de l'installation de {package}")
                return
    
    print("\n🎉 Toutes les dépendances sont installées !")
    print("\n📖 Étapes suivantes :")
    print("1. Connectez-vous à Hugging Face : huggingface-cli login")
    print("2. Uploadez votre modèle : python upload_to_hf.py --repo_name votre-nom/eurobert-commit-humor")

if __name__ == "__main__":
    main()