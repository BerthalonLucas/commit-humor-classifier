#!/usr/bin/env python3
"""
🤖 Classificateur d'Humour pour Messages de Commit
=====================================

Script portable tout-en-un pour classifier si un message de commit est drôle ou pas.
Utilise un modèle EuroBERT-210m fine-tuné avec LoRA.

Usage:
    python commit_humor_classifier.py "Mon message de commit"
    python commit_humor_classifier.py --interactive
    python commit_humor_classifier.py --batch messages.txt

Auteur: Assistant IA
Version: 1.0
"""

import os
import sys
import argparse
from pathlib import Path
import tempfile
import shutil

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    try:
        import torch
        import transformers
        from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
        from huggingface_hub import hf_hub_download, snapshot_download
        print("✅ Toutes les dépendances sont installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante : {e}")
        print("\n🔧 Installation requise :")
        print("pip install torch transformers accelerate huggingface_hub")
        return False

def download_model_from_hf(model_id, local_dir):
    """Télécharge le modèle depuis Hugging Face"""
    try:
        print(f"🔽 Téléchargement du modèle depuis Hugging Face...")
        print(f"   📍 Modèle : {model_id}")
        print(f"   📂 Destination : {local_dir}")
        
        from huggingface_hub import snapshot_download
        
        # Télécharger tous les fichiers du modèle
        snapshot_download(
            repo_id=model_id,
            local_dir=local_dir,
            resume_download=True,
            local_dir_use_symlinks=False
        )
        
        print("✅ Modèle téléchargé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement : {e}")
        print("\n🔧 Vérifiez :")
        print("   - Votre connexion internet")
        print("   - Le nom du modèle sur Hugging Face")
        print("   - Que vous avez les permissions nécessaires")
        return False

class CommitHumorClassifier:
    """Classificateur d'humour pour messages de commit"""
    
    def __init__(self, model_path="eurobert_full", model_id="LBerthalon/eurobert-commit-humor", seuil=0.35):
        """
        Initialise le classificateur
        
        Args:
            model_path (str): Chemin local vers le modèle fusionné
            model_id (str): ID du modèle sur Hugging Face
            seuil (float): Seuil de décision pour la classification
        """
        self.model_path = model_path
        self.model_id = model_id
        self.seuil = seuil
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        
    def load_model(self):
        """Charge le modèle et le tokenizer"""
        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
            
            # Vérifier si le modèle existe localement
            if not os.path.exists(self.model_path):
                print(f"📂 Le modèle local '{self.model_path}' n'existe pas")
                print(f"🔽 Téléchargement depuis Hugging Face...")
                
                if not download_model_from_hf(self.model_id, self.model_path):
                    return False
            else:
                print(f"📂 Modèle local trouvé : {self.model_path}")
            
            print("🔤 Chargement du tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            
            print("🤖 Chargement du modèle...")
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            
            print("🔧 Création du pipeline...")
            self.pipeline = pipeline(
                'text-classification',
                model=self.model,
                tokenizer=self.tokenizer,
                trust_remote_code=True,
                top_k=1
            )
            
            print("✅ Modèle chargé avec succès")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement : {e}")
            return False
    
    def predict(self, text):
        """
        Prédit si un message de commit est drôle ou pas
        
        Args:
            text (str): Le message de commit à analyser
        
        Returns:
            dict: Résultat avec label et probabilité
        """
        if not self.pipeline:
            raise RuntimeError("Le modèle n'est pas chargé. Appelez load_model() d'abord.")
            
        pipeline_result = self.pipeline(text)
        result = pipeline_result[0][0]
        score = result['score']
        
        # Conversion du label et application du seuil
        if result['label'] == 'LABEL_1':
            is_funny = score > self.seuil
            probability = score
        else:
            is_funny = score < (1 - self.seuil)
            probability = 1 - score
        
        return {
            'text': text,
            'is_funny': is_funny,
            'label': 'DRÔLE' if is_funny else 'PAS DRÔLE',
            'probability': probability,
            'raw_score': score,
            'raw_label': result['label']
        }
    
    def predict_batch(self, texts):
        """Prédit pour plusieurs messages"""
        results = []
        for text in texts:
            try:
                result = self.predict(text.strip())
                results.append(result)
            except Exception as e:
                print(f"❌ Erreur pour '{text}': {e}")
                results.append({'text': text, 'error': str(e)})
        return results

def interactive_mode(classifier):
    """Mode interactif"""
    print("\n🎯 Mode interactif - Tapez 'quit' pour quitter")
    print("=" * 50)
    
    while True:
        try:
            text = input("\n📝 Message de commit : ").strip()
            if text.lower() in ['quit', 'q', 'exit']:
                print("👋 Au revoir !")
                break
            
            if not text:
                continue
                
            result = classifier.predict(text)
            emoji = "😄" if result['is_funny'] else "😐"
            print(f"   → {emoji} {result['label']} (prob: {result['probability']:.3f})")
            
        except KeyboardInterrupt:
            print("\n👋 Au revoir !")
            break
        except Exception as e:
            print(f"❌ Erreur : {e}")

def batch_mode(classifier, file_path):
    """Mode batch depuis un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            texts = f.readlines()
        
        print(f"\n📂 Traitement de {len(texts)} messages depuis '{file_path}'")
        print("=" * 50)
        
        results = classifier.predict_batch(texts)
        
        for result in results:
            if 'error' in result:
                print(f"❌ '{result['text']}' : {result['error']}")
            else:
                emoji = "😄" if result['is_funny'] else "😐"
                print(f"📝 '{result['text']}'")
                print(f"   → {emoji} {result['label']} (prob: {result['probability']:.3f})")
                
    except FileNotFoundError:
        print(f"❌ Fichier '{file_path}' introuvable")
    except Exception as e:
        print(f"❌ Erreur lors du traitement : {e}")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Classificateur d'humour pour messages de commit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python commit_humor_classifier.py "fix typo in README"
  python commit_humor_classifier.py --interactive
  python commit_humor_classifier.py --batch messages.txt
  python commit_humor_classifier.py --seuil 0.6 "Mon message"
        """
    )
    
    parser.add_argument('message', nargs='?', help='Message de commit à classifier')
    parser.add_argument('--interactive', '-i', action='store_true', help='Mode interactif')
    parser.add_argument('--batch', '-b', help='Fichier contenant les messages (un par ligne)')
    parser.add_argument('--seuil', '-s', type=float, default=0.35, help='Seuil de décision (défaut: 0.35)')
    parser.add_argument('--model', '-m', default='eurobert_full', help='Chemin local vers le modèle')
    parser.add_argument('--model-id', default='LBerthalon/eurobert-commit-humor', help='ID du modèle sur Hugging Face')
    
    args = parser.parse_args()
    
    # Vérification des dépendances
    if not check_dependencies():
        return 1
    
    # Initialisation du classificateur
    classifier = CommitHumorClassifier(model_path=args.model, model_id=args.model_id, seuil=args.seuil)
    
    if not classifier.load_model():
        return 1
    
    # Modes d'utilisation
    if args.interactive:
        interactive_mode(classifier)
    elif args.batch:
        batch_mode(classifier, args.batch)
    elif args.message:
        result = classifier.predict(args.message)
        emoji = "😄" if result['is_funny'] else "😐"
        print(f"\n📝 '{result['text']}'")
        print(f"   → {emoji} {result['label']} (prob: {result['probability']:.3f})")
    else:
        parser.print_help()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())