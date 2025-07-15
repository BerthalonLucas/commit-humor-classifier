#!/usr/bin/env python3
"""
Script de démarrage rapide pour uploader sur Hugging Face
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Vérifier les prérequis"""
    print("🔍 Vérification des prérequis...")
    
    # Vérifier que le modèle existe
    if not Path("eurobert_full").exists():
        print("❌ Dossier 'eurobert_full' introuvable")
        print("💡 Assurez-vous d'être dans le bon répertoire")
        return False
    
    # Vérifier les fichiers essentiels
    required_files = [
        "eurobert_full/config.json",
        "eurobert_full/model.safetensors",
        "eurobert_full/tokenizer.json"
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Fichier manquant : {file}")
            return False
    
    print("✅ Modèle trouvé et fichiers vérifiés")
    return True

def install_dependencies():
    """Installer les dépendances"""
    print("\n🔧 Installation des dépendances...")
    
    packages = ["huggingface_hub", "transformers", "torch", "datasets"]
    
    for package in packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} déjà installé")
        except ImportError:
            print(f"📦 Installation de {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installé avec succès")
            except subprocess.CalledProcessError:
                print(f"❌ Erreur lors de l'installation de {package}")
                return False
    
    return True

def check_hf_login():
    """Vérifier la connexion Hugging Face"""
    print("\n🔐 Vérification de la connexion Hugging Face...")
    
    try:
        from huggingface_hub import HfApi
        api = HfApi()
        user_info = api.whoami()
        print(f"✅ Connecté en tant que : {user_info['name']}")
        return True
    except Exception as e:
        print("❌ Non connecté à Hugging Face")
        print("💡 Exécutez : huggingface-cli login")
        return False

def get_repo_name():
    """Demander le nom du repository"""
    print("\n📝 Configuration du repository...")
    
    while True:
        repo_name = input("Nom du repository (ex: votre-nom/eurobert-commit-humor): ").strip()
        
        if not repo_name:
            print("❌ Le nom ne peut pas être vide")
            continue
        
        if "/" not in repo_name:
            print("❌ Format requis : nom-utilisateur/nom-modele")
            continue
        
        # Vérifier le format
        parts = repo_name.split("/")
        if len(parts) != 2:
            print("❌ Format requis : nom-utilisateur/nom-modele")
            continue
        
        return repo_name

def main():
    print("🚀 Démarrage rapide pour upload sur Hugging Face")
    print("=" * 50)
    
    # Vérifier les prérequis
    if not check_requirements():
        return
    
    # Installer les dépendances
    if not install_dependencies():
        return
    
    # Vérifier la connexion HF
    if not check_hf_login():
        print("\n📖 Pour vous connecter :")
        print("1. Obtenez votre token sur : https://huggingface.co/settings/tokens")
        print("2. Exécutez : huggingface-cli login")
        print("3. Relancez ce script")
        return
    
    # Demander le nom du repository
    repo_name = get_repo_name()
    
    # Demander si repository privé
    private = input("\nRepository privé ? (y/N): ").lower().startswith('y')
    
    print(f"\n🎯 Configuration :")
    print(f"   Repository : {repo_name}")
    print(f"   Privé : {'Oui' if private else 'Non'}")
    print(f"   Modèle : eurobert_full/")
    
    confirm = input("\nContinuer ? (Y/n): ").lower()
    if confirm.startswith('n'):
        print("❌ Upload annulé")
        return
    
    # Lancer l'upload
    print("\n🚀 Lancement de l'upload...")
    
    cmd = [sys.executable, "upload_to_hf.py", "--repo_name", repo_name]
    if private:
        cmd.append("--private")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n🎉 SUCCESS ! Modèle uploadé avec succès !")
        print(f"🔗 https://huggingface.co/{repo_name}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors de l'upload : {e}")
        print("💡 Consultez HUGGINGFACE_GUIDE.md pour plus d'aide")
    except KeyboardInterrupt:
        print("\n❌ Upload interrompu par l'utilisateur")

if __name__ == "__main__":
    main()