#!/usr/bin/env python3
"""
📊 Processeur de Commits JSON - Classificateur d'Humour
=====================================================

Script pour traiter des fichiers JSON contenant des commits et classifier
leur humour en temps réel ou en batch.

Format JSON attendu (comme exam-2024-09-13.json):
[
    {
        "sha": "d505efb38b3e24e06923be4333a7c3fd874a1856",
        "repo": {
            "org": "exam-2024-09-13",
            "name": "oligrien_c-piscine-exam-01_exam_13h27m03s",
            "full_name": "exam-2024-09-13/oligrien_c-piscine-exam-01_exam_13h27m03s"
        },
        "author": {
            "name": "Exam 42",
            "email": "exam-no-reply@42.fr",
            "date": "2024-09-13T18:00:03+02:00"
        },
        "committer": {
            "name": "Exam 42",
            "email": "exam-no-reply@42.fr",
            "date": "2024-09-13T18:00:03+02:00"
        },
        "message": "t"
    }
]

Usage:
    python process_commits_json.py commits.json
    python process_commits_json.py commits.json --output results.json
    python process_commits_json.py commits.json --watch  # Mode surveillance
    python process_commits_json.py commits.json --stats  # Affiche les statistiques

Auteur: Assistant IA
Version: 1.0
"""

import os
import sys
import json
import argparse
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import hashlib

# Import du classificateur
try:
    from commit_humor_classifier import CommitHumorClassifier
except ImportError:
    print("❌ Erreur: commit_humor_classifier.py non trouvé")
    print("   Assurez-vous d'être dans le bon répertoire")
    sys.exit(1)

class CommitProcessor:
    """Processeur de commits JSON avec classification d'humour"""
    
    def __init__(self, model_path="eurobert_full", model_id="LBerthalon/eurobert-commit-humor", seuil=0.7):
        """
        Initialise le processeur
        
        Args:
            model_path (str): Chemin local vers le modèle
            model_id (str): ID du modèle sur Hugging Face
            seuil (float): Seuil de classification
        """
        self.classifier = CommitHumorClassifier(model_path, model_id, seuil)
        self.processed_commits = set()  # Cache des commits déjà traités
        self.stats = {
            "total_processed": 0,
            "funny_count": 0,
            "not_funny_count": 0,
            "start_time": datetime.now()
        }
    
    def load_model(self):
        """Charge le modèle de classification"""
        print("🤖 Chargement du modèle de classification...")
        return self.classifier.load_model()
    
    def load_commits_json(self, file_path: str) -> List[Dict[str, Any]]:
        """Charge les commits depuis un fichier JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                commits = json.load(f)
            
            if not isinstance(commits, list):
                raise ValueError("Le fichier JSON doit contenir une liste de commits")
            
            print(f"📂 {len(commits)} commits chargés depuis {file_path}")
            return commits
            
        except FileNotFoundError:
            print(f"❌ Fichier non trouvé: {file_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ Erreur JSON: {e}")
            return []
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            return []
    
    def get_commit_id(self, commit: Dict[str, Any]) -> str:
        """Génère un ID unique pour un commit"""
        # Utilise le SHA si disponible, sinon un hash du contenu
        if 'sha' in commit:
            return commit['sha']
        else:
            # Créer un hash basé sur le message et les métadonnées
            content = f"{commit.get('message', '')}{commit.get('author', {}).get('date', '')}"
            return hashlib.md5(content.encode()).hexdigest()
    
    def extract_message(self, commit: Dict[str, Any]) -> str:
        """Extrait le message du commit"""
        return commit.get('message', '').strip()
    
    def classify_commit(self, commit: Dict[str, Any]) -> Dict[str, Any]:
        """Classifie un commit et retourne les résultats enrichis"""
        commit_id = self.get_commit_id(commit)
        message = self.extract_message(commit)
        
        if not message:
            return {
                **commit,
                'humor_classification': {
                    'message': '',
                    'is_funny': False,
                    'confidence': 0.0,
                    'error': 'Message vide'
                }
            }
        
        try:
            # Classification
            result = self.classifier.predict(message)
            
            # Mise à jour des statistiques
            self.stats['total_processed'] += 1
            if result['is_funny']:
                self.stats['funny_count'] += 1
            else:
                self.stats['not_funny_count'] += 1
            
            # Marquer comme traité
            self.processed_commits.add(commit_id)
            
            return {
                **commit,
                'humor_classification': {
                    'message': message,
                    'is_funny': result['is_funny'],
                    'confidence': result['confidence'],
                    'label': result['label'],
                    'processed_at': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            print(f"❌ Erreur lors de la classification de {commit_id}: {e}")
            return {
                **commit,
                'humor_classification': {
                    'message': message,
                    'is_funny': False,
                    'confidence': 0.0,
                    'error': str(e)
                }
            }
    
    def process_commits(self, commits: List[Dict[str, Any]], skip_processed=True) -> List[Dict[str, Any]]:
        """Traite une liste de commits"""
        results = []
        
        print(f"\n🔄 Traitement de {len(commits)} commits...")
        
        for i, commit in enumerate(commits, 1):
            commit_id = self.get_commit_id(commit)
            
            # Skip si déjà traité
            if skip_processed and commit_id in self.processed_commits:
                continue
            
            print(f"\r📊 Progression: {i}/{len(commits)} ({i/len(commits)*100:.1f}%)", end="", flush=True)
            
            classified_commit = self.classify_commit(commit)
            results.append(classified_commit)
            
            # Affichage du résultat
            humor = classified_commit['humor_classification']
            if not humor.get('error'):
                emoji = "😄" if humor['is_funny'] else "😐"
                print(f"\n   {emoji} '{humor['message'][:50]}...' → {humor['label']} ({humor['confidence']:.3f})")
        
        print(f"\n✅ Traitement terminé: {len(results)} nouveaux commits traités")
        return results
    
    def save_results(self, results: List[Dict[str, Any]], output_path: str):
        """Sauvegarde les résultats dans un fichier JSON"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"💾 Résultats sauvegardés dans {output_path}")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            return False
    
    def print_stats(self):
        """Affiche les statistiques de traitement"""
        duration = datetime.now() - self.stats['start_time']
        
        print("\n" + "="*50)
        print("📊 STATISTIQUES DE TRAITEMENT")
        print("="*50)
        print(f"📈 Total traité: {self.stats['total_processed']} commits")
        print(f"😄 Drôles: {self.stats['funny_count']} ({self.stats['funny_count']/max(1,self.stats['total_processed'])*100:.1f}%)")
        print(f"😐 Pas drôles: {self.stats['not_funny_count']} ({self.stats['not_funny_count']/max(1,self.stats['total_processed'])*100:.1f}%)")
        print(f"⏱️  Durée: {duration}")
        if self.stats['total_processed'] > 0:
            rate = self.stats['total_processed'] / duration.total_seconds()
            print(f"🚀 Vitesse: {rate:.2f} commits/seconde")
        print("="*50)
    
    def watch_file(self, file_path: str, output_path: str = None, interval: int = 5):
        """Surveille un fichier et traite les nouveaux commits"""
        print(f"👁️  Mode surveillance activé pour {file_path}")
        print(f"🔄 Vérification toutes les {interval} secondes")
        print("   Appuyez sur Ctrl+C pour arrêter\n")
        
        last_size = 0
        
        try:
            while True:
                if os.path.exists(file_path):
                    current_size = os.path.getsize(file_path)
                    
                    if current_size != last_size:
                        print(f"\n📝 Changement détecté dans {file_path}")
                        
                        commits = self.load_commits_json(file_path)
                        if commits:
                            new_results = self.process_commits(commits, skip_processed=True)
                            
                            if new_results and output_path:
                                # Charger les résultats existants
                                existing_results = []
                                if os.path.exists(output_path):
                                    try:
                                        with open(output_path, 'r', encoding='utf-8') as f:
                                            existing_results = json.load(f)
                                    except:
                                        pass
                                
                                # Ajouter les nouveaux résultats
                                all_results = existing_results + new_results
                                self.save_results(all_results, output_path)
                        
                        last_size = current_size
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Surveillance arrêtée")
            self.print_stats()

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Processeur de commits JSON avec classification d'humour",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python process_commits_json.py exam-2024-09-13.json
  python process_commits_json.py commits.json --output results.json
  python process_commits_json.py commits.json --watch --interval 10
  python process_commits_json.py commits.json --stats
        """
    )
    
    parser.add_argument("input_file", help="Fichier JSON contenant les commits")
    parser.add_argument("-o", "--output", help="Fichier de sortie pour les résultats")
    parser.add_argument("-w", "--watch", action="store_true", help="Mode surveillance du fichier")
    parser.add_argument("-i", "--interval", type=int, default=5, help="Intervalle de surveillance (secondes)")
    parser.add_argument("-s", "--stats", action="store_true", help="Affiche les statistiques détaillées")
    parser.add_argument("--seuil", type=float, default=0.7, help="Seuil de classification (défaut: 0.7)")
    parser.add_argument("--model-path", default="eurobert_full", help="Chemin vers le modèle local")
    parser.add_argument("--model-id", default="LBerthalon/eurobert-commit-humor", help="ID du modèle Hugging Face")
    
    args = parser.parse_args()
    
    # Vérifier que le fichier d'entrée existe
    if not os.path.exists(args.input_file):
        print(f"❌ Fichier non trouvé: {args.input_file}")
        sys.exit(1)
    
    # Initialiser le processeur
    processor = CommitProcessor(
        model_path=args.model_path,
        model_id=args.model_id,
        seuil=args.seuil
    )
    
    # Charger le modèle
    if not processor.load_model():
        print("❌ Impossible de charger le modèle")
        sys.exit(1)
    
    # Mode surveillance
    if args.watch:
        output_path = args.output or f"{Path(args.input_file).stem}_results.json"
        processor.watch_file(args.input_file, output_path, args.interval)
        return
    
    # Traitement normal
    commits = processor.load_commits_json(args.input_file)
    if not commits:
        print("❌ Aucun commit à traiter")
        sys.exit(1)
    
    # Traiter les commits
    results = processor.process_commits(commits, skip_processed=False)
    
    # Sauvegarder si demandé
    if args.output:
        processor.save_results(results, args.output)
    
    # Afficher les statistiques
    if args.stats or not args.output:
        processor.print_stats()
        
        # Afficher quelques exemples
        print("\n🎯 Exemples de classification:")
        funny_examples = [r for r in results if r['humor_classification'].get('is_funny', False)][:3]
        not_funny_examples = [r for r in results if not r['humor_classification'].get('is_funny', True)][:3]
        
        if funny_examples:
            print("\n😄 Messages drôles:")
            for example in funny_examples:
                humor = example['humor_classification']
                print(f"   • '{humor['message'][:60]}...' ({humor['confidence']:.3f})")
        
        if not_funny_examples:
            print("\n😐 Messages pas drôles:")
            for example in not_funny_examples:
                humor = example['humor_classification']
                print(f"   • '{humor['message'][:60]}...' ({humor['confidence']:.3f})")

if __name__ == "__main__":
    main()