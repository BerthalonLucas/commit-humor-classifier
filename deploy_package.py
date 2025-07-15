#!/usr/bin/env python3
"""
🚀 Script de déploiement du Classificateur d'Humour pour Commits
=====================================================

Ce script crée un package portable complet ready-to-use.
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_deployment_package():
    """Crée un package de déploiement complet"""
    
    # Nom du package
    package_name = "commit-humor-classifier-portable"
    
    # Fichiers essentiels à inclure
    essential_files = [
        "commit_humor_classifier.py",
        "requirements.txt", 
        "README_PORTABLE.md",
        "setup.py",
        "test_messages.txt"
    ]
    
    # Dossiers essentiels (le modèle sera téléchargé depuis Hugging Face)
    essential_dirs = [
        # "eurobert_full" - plus nécessaire, téléchargé automatiquement
    ]
    
    print("🚀 Création du package de déploiement...")
    print("=" * 50)
    
    # Créer le dossier de package
    if os.path.exists(package_name):
        shutil.rmtree(package_name)
    os.makedirs(package_name)
    
    # Copier les fichiers essentiels
    print("📁 Copie des fichiers essentiels...")
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, package_name)
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (manquant)")
    
    # Copier les dossiers essentiels
    print("\n📂 Copie des dossiers essentiels...")
    for dir_name in essential_dirs:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, os.path.join(package_name, dir_name))
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ❌ {dir_name}/ (manquant)")
    
    # Créer un script de démarrage Windows
    print("\n🔧 Création des scripts de démarrage...")
    
    # Script Windows (.bat)
    windows_script = f"""@echo off
echo 🤖 Classificateur d'Humour pour Commits
echo =====================================
echo.

REM Vérification de Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    pause
    exit /b 1
)

REM Installation des dépendances
echo 📦 Installation des dépendances...
pip install -r requirements.txt

REM Test du modèle (téléchargement automatique depuis Hugging Face)
echo.
echo 🧪 Test du modèle (téléchargement automatique si nécessaire)...
python commit_humor_classifier.py "Test de déploiement"

echo.
echo ✅ Installation terminée !
echo.
echo 📖 Usage:
echo    python commit_humor_classifier.py "Mon message"
echo    python commit_humor_classifier.py --interactive
echo    python commit_humor_classifier.py --batch test_messages.txt
echo.
pause
"""
    
    with open(os.path.join(package_name, "INSTALL.bat"), "w", encoding="utf-8") as f:
        f.write(windows_script)
    
    # Script Unix/Linux (.sh)
    unix_script = f"""#!/bin/bash
echo "🤖 Classificateur d'Humour pour Commits"
echo "====================================="
echo

# Vérification de Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Installation des dépendances
echo "📦 Installation des dépendances..."
pip3 install -r requirements.txt

# Test du modèle (téléchargement automatique depuis Hugging Face)
echo
echo "🧪 Test du modèle (téléchargement automatique si nécessaire)..."
python3 commit_humor_classifier.py "Test de déploiement"

echo
echo "✅ Installation terminée !"
echo
echo "📖 Usage:"
echo "   python3 commit_humor_classifier.py 'Mon message'"
echo "   python3 commit_humor_classifier.py --interactive"
echo "   python3 commit_humor_classifier.py --batch test_messages.txt"
echo
"""
    
    with open(os.path.join(package_name, "install.sh"), "w", encoding="utf-8") as f:
        f.write(unix_script)
    
    # Rendre le script Unix exécutable
    os.chmod(os.path.join(package_name, "install.sh"), 0o755)
    
    # Créer un fichier d'instructions rapides
    quick_start = f"""🚀 DÉMARRAGE RAPIDE
==================

1. 📦 Installation des dépendances :
   
   Windows: Double-cliquez sur INSTALL.bat
   Linux/Mac: ./install.sh
   
   Ou manuellement: pip install -r requirements.txt

2. 🧪 Test rapide :
   
   python commit_humor_classifier.py "gcc et moi c'est compliqué"

3. 📖 Usage complet :
   
   Voir README_PORTABLE.md pour tous les modes d'utilisation

4. 🔧 Dépannage :
   
   - Vérifiez que Python 3.7+ est installé
   - Vérifiez votre connexion internet pour le téléchargement du modèle
   - Installez les dépendances manuellement si nécessaire
   - Le modèle sera téléchargé automatiquement depuis Hugging Face au premier usage

✅ Prêt à l'emploi !
"""
    
    with open(os.path.join(package_name, "QUICK_START.txt"), "w", encoding="utf-8") as f:
        f.write(quick_start)
    
    print("   ✅ INSTALL.bat (Windows)")
    print("   ✅ install.sh (Linux/Mac)")
    print("   ✅ QUICK_START.txt")
    
    # Créer une archive ZIP
    print(f"\n📦 Création de l'archive {package_name}.zip...")
    with zipfile.ZipFile(f"{package_name}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_name):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_name)
                zipf.write(file_path, arcname)
    
    # Statistiques
    print(f"\n📊 Statistiques du package:")
    print(f"   📁 Dossier: {package_name}/")
    print(f"   📦 Archive: {package_name}.zip")
    
    # Taille du package
    total_size = 0
    for root, dirs, files in os.walk(package_name):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    
    print(f"   📏 Taille: {total_size / (1024*1024):.1f} MB")
    
    zip_size = os.path.getsize(f"{package_name}.zip")
    print(f"   📦 Archive ZIP: {zip_size / (1024*1024):.1f} MB")
    
    print(f"\n✅ Package créé avec succès !")
    print(f"   🎯 Prêt pour déploiement sur n'importe quelle machine")
    print(f"   📂 Décompressez {package_name}.zip et lancez INSTALL.bat")
    
    return package_name

if __name__ == "__main__":
    create_deployment_package()