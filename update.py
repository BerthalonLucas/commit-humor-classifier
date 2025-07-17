#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 Script de Mise à Jour - Classificateur d'Humour de Commits
============================================================

Script pour mettre à jour le classificateur d'humour, ses dépendances
et télécharger les nouvelles versions du modèle si disponibles.

Utilisation:
    python update.py                    # Mise à jour complète
    python update.py --dependencies     # Mise à jour des dépendances uniquement
    python update.py --model            # Mise à jour du modèle uniquement
    python update.py --check            # Vérifier les mises à jour disponibles
    python update.py --force            # Forcer la mise à jour

Auteur: Assistant IA
Version: 1.0
Date: 2025
"""

import os
import sys
import json
import subprocess
import argparse
import requests
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class UpdateManager:
    """Gestionnaire de mise à jour pour le classificateur d'humeur."""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.config_file = self.project_root / "config.json"
        self.requirements_file = self.project_root / "requirements.txt"
        
        # Charger la configuration
        self.config = self.load_config()
        
        # URLs et informations de mise à jour
        self.update_urls = {
            "huggingface_api": "https://huggingface.co/api/models",
            "pypi_api": "https://pypi.org/pypi",
            "github_releases": "https://api.github.com/repos"
        }
    
    def load_config(self) -> Dict:
        """Charge la configuration du projet."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.get_default_config()
        except Exception as e:
            self.print_status(f"Erreur lors du chargement de la configuration: {e}", "WARNING")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Retourne une configuration par défaut."""
        return {
            "project": {
                "name": "Classificateur d'Humour de Commits",
                "version": "1.0.0"
            },
            "model": {
                "huggingface_repo": "LBerthalon/eurobert-commit-humor"
            },
            "requirements": {
                "torch": ">=1.9.0",
                "transformers": ">=4.20.0",
                "huggingface_hub": ">=0.10.0"
            }
        }
    
    def print_status(self, message: str, status: str = "INFO") -> None:
        """Affiche un message de statut."""
        emoji_map = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "WORKING": "🔄",
            "UPDATE": "🆙"
        }
        emoji = emoji_map.get(status, "📝")
        print(f"{emoji} {message}")
    
    def run_command(self, command: List[str], description: str) -> Tuple[bool, str]:
        """Exécute une commande et retourne le résultat."""
        try:
            self.print_status(f"{description}...", "WORKING")
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                self.print_status(f"{description} réussi", "SUCCESS")
                return True, result.stdout.strip()
            else:
                self.print_status(f"{description} échoué", "ERROR")
                return False, result.stderr.strip()
                
        except Exception as e:
            self.print_status(f"Erreur lors de {description}: {e}", "ERROR")
            return False, str(e)
    
    def check_python_packages_updates(self) -> Dict[str, Dict]:
        """Vérifie les mises à jour disponibles pour les packages Python."""
        self.print_status("Vérification des mises à jour des packages Python...", "WORKING")
        
        updates_available = {}
        
        if not self.requirements_file.exists():
            self.print_status("Fichier requirements.txt non trouvé", "WARNING")
            return updates_available
        
        # Lire les requirements
        with open(self.requirements_file, 'r') as f:
            requirements = f.read().splitlines()
        
        for req in requirements:
            if req.strip() and not req.startswith('#'):
                package_name = req.split('>=')[0].split('==')[0].strip()
                
                try:
                    # Obtenir la version installée
                    success, current_version = self.run_command(
                        [sys.executable, '-c', f'import {package_name}; print({package_name}.__version__)'],
                        f"Vérification de {package_name}"
                    )
                    
                    if success:
                        # Vérifier la dernière version sur PyPI
                        try:
                            response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=10)
                            if response.status_code == 200:
                                data = response.json()
                                latest_version = data['info']['version']
                                
                                if current_version != latest_version:
                                    updates_available[package_name] = {
                                        'current': current_version,
                                        'latest': latest_version,
                                        'update_available': True
                                    }
                                else:
                                    updates_available[package_name] = {
                                        'current': current_version,
                                        'latest': latest_version,
                                        'update_available': False
                                    }
                        except requests.RequestException:
                            self.print_status(f"Impossible de vérifier {package_name} sur PyPI", "WARNING")
                            
                except Exception:
                    self.print_status(f"Package {package_name} non installé", "WARNING")
        
        return updates_available
    
    def check_model_updates(self) -> Dict[str, any]:
        """Vérifie les mises à jour du modèle sur Hugging Face."""
        self.print_status("Vérification des mises à jour du modèle...", "WORKING")
        
        model_info = {
            'update_available': False,
            'current_version': 'local',
            'latest_version': 'unknown'
        }
        
        try:
            repo_id = self.config.get('model', {}).get('huggingface_repo', '')
            if not repo_id:
                self.print_status("Repository Hugging Face non configuré", "WARNING")
                return model_info
            
            # Vérifier les informations du modèle
            response = requests.get(f"https://huggingface.co/api/models/{repo_id}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                last_modified = data.get('lastModified', '')
                
                # Vérifier si le modèle local existe
                local_model_path = self.project_root / "eurobert_full"
                if local_model_path.exists():
                    # Comparer les dates de modification
                    local_mtime = datetime.fromtimestamp(local_model_path.stat().st_mtime)
                    remote_mtime = datetime.fromisoformat(last_modified.replace('Z', '+00:00'))
                    
                    if remote_mtime > local_mtime:
                        model_info['update_available'] = True
                        model_info['latest_version'] = last_modified
                        self.print_status("Mise à jour du modèle disponible", "UPDATE")
                    else:
                        self.print_status("Modèle à jour", "SUCCESS")
                else:
                    model_info['update_available'] = True
                    model_info['latest_version'] = last_modified
                    self.print_status("Modèle non téléchargé localement", "INFO")
            else:
                self.print_status("Impossible de vérifier le modèle sur Hugging Face", "WARNING")
                
        except requests.RequestException as e:
            self.print_status(f"Erreur de connexion à Hugging Face: {e}", "WARNING")
        except Exception as e:
            self.print_status(f"Erreur lors de la vérification du modèle: {e}", "ERROR")
        
        return model_info
    
    def update_dependencies(self, force: bool = False) -> bool:
        """Met à jour les dépendances Python."""
        self.print_status("Mise à jour des dépendances...", "WORKING")
        
        if not self.requirements_file.exists():
            self.print_status("Fichier requirements.txt non trouvé", "ERROR")
            return False
        
        # Commande de mise à jour
        update_command = [
            sys.executable, '-m', 'pip', 'install', '--upgrade',
            '-r', str(self.requirements_file)
        ]
        
        if force:
            update_command.append('--force-reinstall')
        
        success, output = self.run_command(update_command, "Mise à jour des dépendances")
        
        if success:
            self.print_status("Dépendances mises à jour avec succès", "SUCCESS")
        else:
            self.print_status(f"Échec de la mise à jour des dépendances: {output}", "ERROR")
        
        return success
    
    def update_model(self, force: bool = False) -> bool:
        """Met à jour le modèle depuis Hugging Face."""
        self.print_status("Mise à jour du modèle...", "WORKING")
        
        try:
            # Utiliser le script de classification pour télécharger le modèle
            classifier_script = self.project_root / "commit_humor_classifier.py"
            
            if not classifier_script.exists():
                self.print_status("Script de classification non trouvé", "ERROR")
                return False
            
            # Supprimer le modèle local si force est activé
            if force:
                local_model_path = self.project_root / "eurobert_full"
                if local_model_path.exists():
                    import shutil
                    shutil.rmtree(local_model_path)
                    self.print_status("Modèle local supprimé", "INFO")
            
            # Télécharger le modèle
            success, output = self.run_command(
                [sys.executable, str(classifier_script), '--download-only'],
                "Téléchargement du modèle"
            )
            
            if success:
                self.print_status("Modèle mis à jour avec succès", "SUCCESS")
            else:
                self.print_status(f"Échec de la mise à jour du modèle: {output}", "ERROR")
            
            return success
            
        except Exception as e:
            self.print_status(f"Erreur lors de la mise à jour du modèle: {e}", "ERROR")
            return False
    
    def create_backup(self) -> bool:
        """Crée une sauvegarde avant la mise à jour."""
        self.print_status("Création d'une sauvegarde...", "WORKING")
        
        try:
            import shutil
            
            backup_dir = self.project_root / "backup"
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"backup_{timestamp}"
            
            # Sauvegarder les fichiers importants
            important_files = [
                "commit_humor_classifier.py",
                "process_commits_json.py",
                "config.json",
                "requirements.txt"
            ]
            
            backup_path.mkdir(exist_ok=True)
            
            for file_name in important_files:
                file_path = self.project_root / file_name
                if file_path.exists():
                    shutil.copy2(file_path, backup_path / file_name)
            
            self.print_status(f"Sauvegarde créée: {backup_path}", "SUCCESS")
            return True
            
        except Exception as e:
            self.print_status(f"Erreur lors de la sauvegarde: {e}", "ERROR")
            return False
    
    def run_post_update_tests(self) -> bool:
        """Exécute les tests après mise à jour."""
        self.print_status("Exécution des tests post-mise à jour...", "WORKING")
        
        test_script = self.project_root / "test_installation.py"
        
        if not test_script.exists():
            self.print_status("Script de test non trouvé", "WARNING")
            return True  # Pas d'échec si pas de tests
        
        success, output = self.run_command(
            [sys.executable, str(test_script), '--quick'],
            "Tests post-mise à jour"
        )
        
        if success:
            self.print_status("Tests réussis", "SUCCESS")
        else:
            self.print_status(f"Échec des tests: {output}", "ERROR")
        
        return success

def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(description="Script de mise à jour du classificateur d'humour")
    parser.add_argument('--dependencies', action='store_true', help="Mettre à jour les dépendances uniquement")
    parser.add_argument('--model', action='store_true', help="Mettre à jour le modèle uniquement")
    parser.add_argument('--check', action='store_true', help="Vérifier les mises à jour disponibles")
    parser.add_argument('--force', action='store_true', help="Forcer la mise à jour")
    parser.add_argument('--no-backup', action='store_true', help="Ne pas créer de sauvegarde")
    parser.add_argument('--no-tests', action='store_true', help="Ne pas exécuter les tests")
    
    args = parser.parse_args()
    
    # Initialiser le gestionnaire
    manager = UpdateManager()
    
    print("🔄 Script de Mise à Jour - Classificateur d'Humour")
    print("=" * 55)
    
    try:
        # Mode vérification uniquement
        if args.check:
            print("\n📋 Vérification des mises à jour disponibles...")
            
            # Vérifier les packages
            package_updates = manager.check_python_packages_updates()
            if package_updates:
                print("\n📦 Mises à jour de packages disponibles:")
                for package, info in package_updates.items():
                    if info['update_available']:
                        print(f"   • {package}: {info['current']} → {info['latest']}")
            
            # Vérifier le modèle
            model_updates = manager.check_model_updates()
            if model_updates['update_available']:
                print("\n🤖 Mise à jour du modèle disponible")
            
            return
        
        # Créer une sauvegarde
        if not args.no_backup:
            manager.create_backup()
        
        success = True
        
        # Mise à jour des dépendances
        if args.dependencies or (not args.model and not args.dependencies):
            if not manager.update_dependencies(args.force):
                success = False
        
        # Mise à jour du modèle
        if args.model or (not args.model and not args.dependencies):
            if not manager.update_model(args.force):
                success = False
        
        # Tests post-mise à jour
        if not args.no_tests and success:
            if not manager.run_post_update_tests():
                success = False
        
        if success:
            print("\n✅ Mise à jour terminée avec succès !")
            print("\n📚 N'oubliez pas de consulter le README.md pour les nouveautés")
        else:
            print("\n⚠️ Mise à jour terminée avec des erreurs")
            print("   • Consultez les messages ci-dessus")
            print("   • Vérifiez les sauvegardes dans le dossier 'backup'")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Mise à jour interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur lors de la mise à jour: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()