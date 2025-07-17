#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Script de Déploiement - Classificateur d'Humour de Commits
============================================================

Script pour déployer et distribuer le classificateur d'humour.
Permet de créer des packages, des archives et de préparer la distribution.

Utilisation:
    python deploy.py --package          # Créer un package portable
    python deploy.py --archive          # Créer une archive ZIP
    python deploy.py --clean            # Nettoyer les fichiers temporaires
    python deploy.py --all              # Tout faire

Auteur: Assistant IA
Version: 1.0
Date: 2025
"""

import os
import sys
import shutil
import zipfile
import argparse
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

class DeploymentManager:
    """Gestionnaire de déploiement pour le classificateur d'humour."""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.deploy_dir = self.project_root / "deploy"
        self.package_dir = self.deploy_dir / "package"
        self.archive_dir = self.deploy_dir / "archives"
        
        # Fichiers essentiels à inclure
        self.essential_files = [
            "commit_humor_classifier.py",
            "process_commits_json.py",
            "install.py",
            "requirements.txt",
            "README.md",
            ".gitignore"
        ]
        
        # Fichiers optionnels
        self.optional_files = [
            "test_installation.py",
            "HUGGINGFACE_GUIDE.md",
            "REFUSION_GUIDE.md",
            "upload_to_hf.py",
            "deploy_package.py"
        ]
        
        # Dossiers à exclure
        self.exclude_dirs = [
            "__pycache__",
            ".git",
            "deploy",
            "eurobert_full",
            "models",
            "checkpoints",
            "logs",
            "temp",
            ".vscode",
            ".idea"
        ]
        
        # Extensions à exclure
        self.exclude_extensions = [
            ".pyc",
            ".pyo",
            ".log",
            ".tmp",
            ".cache",
            ".bin",
            ".safetensors",
            ".pt",
            ".pth"
        ]
    
    def print_status(self, message: str, status: str = "INFO") -> None:
        """Affiche un message de statut."""
        emoji_map = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "WORKING": "🔄"
        }
        emoji = emoji_map.get(status, "📝")
        print(f"{emoji} {message}")
    
    def create_directories(self) -> None:
        """Crée les répertoires de déploiement."""
        self.print_status("Création des répertoires de déploiement...", "WORKING")
        
        for directory in [self.deploy_dir, self.package_dir, self.archive_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            self.print_status(f"Répertoire créé: {directory.name}", "SUCCESS")
    
    def should_exclude_file(self, file_path: Path) -> bool:
        """Détermine si un fichier doit être exclu."""
        # Vérifier l'extension
        if file_path.suffix.lower() in self.exclude_extensions:
            return True
        
        # Vérifier les dossiers parents
        for part in file_path.parts:
            if part in self.exclude_dirs:
                return True
        
        # Vérifier les fichiers temporaires
        if file_path.name.startswith('.'):
            return True
        
        # Vérifier les fichiers de résultats
        if any(pattern in file_path.name.lower() for pattern in ['_results', '_output', '_processed']):
            return True
        
        return False
    
    def copy_project_files(self) -> None:
        """Copie les fichiers du projet vers le package."""
        self.print_status("Copie des fichiers du projet...", "WORKING")
        
        copied_files = 0
        skipped_files = 0
        
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file() and not self.should_exclude_file(file_path):
                # Calculer le chemin relatif
                relative_path = file_path.relative_to(self.project_root)
                target_path = self.package_dir / relative_path
                
                # Créer le répertoire parent si nécessaire
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copier le fichier
                try:
                    shutil.copy2(file_path, target_path)
                    copied_files += 1
                except Exception as e:
                    self.print_status(f"Erreur lors de la copie de {relative_path}: {e}", "WARNING")
                    skipped_files += 1
            else:
                skipped_files += 1
        
        self.print_status(f"Fichiers copiés: {copied_files}, ignorés: {skipped_files}", "SUCCESS")
    
    def create_deployment_info(self) -> None:
        """Crée un fichier d'information de déploiement."""
        self.print_status("Création des informations de déploiement...", "WORKING")
        
        deployment_info = {
            "project_name": "Classificateur d'Humour de Commits",
            "version": "1.0.0",
            "deployment_date": datetime.now().isoformat(),
            "description": "Classificateur d'humour pour messages de commit basé sur EuroBERT",
            "model_info": {
                "base_model": "EuroBERT-210m",
                "optimization": "Optuna",
                "accuracy": {
                    "global": "85.3%",
                    "funny": "82.9%"
                },
                "threshold": 0.35
            },
            "requirements": {
                "python": ">=3.8",
                "torch": ">=1.9.0",
                "transformers": ">=4.20.0",
                "huggingface_hub": ">=0.10.0"
            },
            "installation": {
                "quick_start": "python install.py",
                "test": "python test_installation.py",
                "usage": "python commit_humor_classifier.py"
            },
            "features": [
                "Classification d'humour en temps réel",
                "Traitement de fichiers JSON",
                "Installation automatique des dépendances",
                "Support CPU et GPU",
                "Interface en ligne de commande",
                "Mode batch et interactif"
            ]
        }
        
        info_file = self.package_dir / "deployment_info.json"
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(deployment_info, f, indent=2, ensure_ascii=False)
        
        self.print_status(f"Informations sauvegardées: {info_file.name}", "SUCCESS")
    
    def create_quick_start_script(self) -> None:
        """Crée un script de démarrage rapide."""
        self.print_status("Création du script de démarrage rapide...", "WORKING")
        
        quick_start_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Démarrage Rapide - Classificateur d'Humour
============================================

Script de démarrage rapide pour installer et tester le classificateur.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Exécute une commande et affiche le résultat."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} réussi")
            return True
        else:
            print(f"❌ {description} échoué: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de {description}: {e}")
        return False

def main():
    print("🎯 Démarrage Rapide - Classificateur d'Humour")
    print("=" * 50)
    
    # Vérifier Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} détecté")
    
    # Installation
    if not run_command("python install.py", "Installation des dépendances"):
        print("⚠️ Problème d'installation, continuons quand même...")
    
    # Test
    if run_command("python test_installation.py --quick", "Test rapide"):
        print("\n🎉 Installation réussie !")
        print("\n📚 Prochaines étapes:")
        print("   • python commit_humor_classifier.py --help")
        print("   • python process_commits_json.py --help")
        print("   • Consultez README.md pour plus d'informations")
    else:
        print("\n⚠️ Des problèmes ont été détectés")
        print("   • Consultez README.md pour le dépannage")
        print("   • Exécutez: python test_installation.py --verbose")

if __name__ == "__main__":
    main()
'''
        
        quick_start_file = self.package_dir / "quick_start.py"
        with open(quick_start_file, 'w', encoding='utf-8') as f:
            f.write(quick_start_content)
        
        self.print_status(f"Script créé: {quick_start_file.name}", "SUCCESS")
    
    def create_archive(self, archive_name: str = None) -> Path:
        """Crée une archive ZIP du package."""
        if not archive_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"commit-humor-classifier_{timestamp}.zip"
        
        archive_path = self.archive_dir / archive_name
        
        self.print_status(f"Création de l'archive: {archive_name}", "WORKING")
        
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in self.package_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(self.package_dir)
                    zipf.write(file_path, arcname)
        
        # Calculer la taille
        size_mb = archive_path.stat().st_size / (1024 * 1024)
        self.print_status(f"Archive créée: {archive_name} ({size_mb:.1f} MB)", "SUCCESS")
        
        return archive_path
    
    def clean_deployment(self) -> None:
        """Nettoie les fichiers de déploiement."""
        self.print_status("Nettoyage des fichiers de déploiement...", "WORKING")
        
        if self.deploy_dir.exists():
            shutil.rmtree(self.deploy_dir)
            self.print_status("Fichiers de déploiement supprimés", "SUCCESS")
        else:
            self.print_status("Aucun fichier de déploiement à nettoyer", "INFO")
    
    def verify_essential_files(self) -> bool:
        """Vérifie que tous les fichiers essentiels sont présents."""
        self.print_status("Vérification des fichiers essentiels...", "WORKING")
        
        missing_files = []
        for file_name in self.essential_files:
            file_path = self.project_root / file_name
            if not file_path.exists():
                missing_files.append(file_name)
        
        if missing_files:
            self.print_status(f"Fichiers manquants: {', '.join(missing_files)}", "ERROR")
            return False
        else:
            self.print_status("Tous les fichiers essentiels sont présents", "SUCCESS")
            return True
    
    def create_package(self) -> bool:
        """Crée un package complet."""
        self.print_status("Création du package de déploiement...", "WORKING")
        
        # Vérifier les fichiers essentiels
        if not self.verify_essential_files():
            return False
        
        # Créer les répertoires
        self.create_directories()
        
        # Copier les fichiers
        self.copy_project_files()
        
        # Créer les fichiers additionnels
        self.create_deployment_info()
        self.create_quick_start_script()
        
        self.print_status("Package créé avec succès", "SUCCESS")
        return True

def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(description="Script de déploiement du classificateur d'humour")
    parser.add_argument('--package', action='store_true', help="Créer un package portable")
    parser.add_argument('--archive', action='store_true', help="Créer une archive ZIP")
    parser.add_argument('--clean', action='store_true', help="Nettoyer les fichiers temporaires")
    parser.add_argument('--all', action='store_true', help="Effectuer toutes les opérations")
    parser.add_argument('--output', '-o', help="Nom de l'archive de sortie")
    
    args = parser.parse_args()
    
    if not any([args.package, args.archive, args.clean, args.all]):
        parser.print_help()
        return
    
    # Initialiser le gestionnaire
    manager = DeploymentManager()
    
    print("🚀 Script de Déploiement - Classificateur d'Humour")
    print("=" * 55)
    
    try:
        # Nettoyage
        if args.clean or args.all:
            manager.clean_deployment()
        
        # Création du package
        if args.package or args.archive or args.all:
            if not manager.create_package():
                print("❌ Échec de la création du package")
                sys.exit(1)
        
        # Création de l'archive
        if args.archive or args.all:
            archive_path = manager.create_archive(args.output)
            print(f"\n📦 Archive disponible: {archive_path}")
        
        print("\n✅ Déploiement terminé avec succès !")
        
    except KeyboardInterrupt:
        print("\n⚠️ Déploiement interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur lors du déploiement: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()