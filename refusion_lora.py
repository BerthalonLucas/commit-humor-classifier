#!/usr/bin/env python3
"""
Script de refusion LoRA pour le classifieur d'humour de commits

Ce script permet de fusionner facilement un nouveau modèle LoRA entraîné
avec le modèle de base EuroBERT pour créer un nouveau modèle complet.

Usage:
    python refusion_lora.py --lora_path chemin/vers/modele_lora [--output_path nouveau_modele]

Exemple:
    python refusion_lora.py --lora_path ../eurobert_peft_v4 --output_path eurobert_full_v2
"""

import argparse
import os
import sys
import shutil
from pathlib import Path

try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    from peft import PeftModel
except ImportError as e:
    print(f"❌ Erreur d'importation : {e}")
    print("Assurez-vous d'avoir installé les dépendances avec : pip install -r requirements.txt")
    sys.exit(1)

def check_lora_model(lora_path):
    """Vérifie que le modèle LoRA existe et est valide"""
    if not os.path.exists(lora_path):
        print(f"❌ Le chemin {lora_path} n'existe pas")
        return False
    
    # Vérifier la présence des fichiers essentiels
    required_files = ['adapter_config.json', 'adapter_model.safetensors']
    for file in required_files:
        if not os.path.exists(os.path.join(lora_path, file)):
            print(f"❌ Fichier manquant : {file}")
            return False
    
    print(f"✅ Modèle LoRA trouvé : {lora_path}")
    return True

def fuse_lora_model(lora_path, output_path, base_model="jplu/eurobert-base-cased"):
    """Fusionne le modèle LoRA avec le modèle de base"""
    print(f"\n🔄 Début de la fusion LoRA...")
    print(f"   • Modèle de base : {base_model}")
    print(f"   • Modèle LoRA : {lora_path}")
    print(f"   • Sortie : {output_path}")
    
    try:
        # Charger le modèle de base
        print("\n📥 Chargement du modèle de base...")
        base_model_obj = AutoModelForSequenceClassification.from_pretrained(
            base_model, 
            num_labels=2,
            trust_remote_code=True
        )
        
        # Charger le tokenizer
        print("🔤 Chargement du tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
        
        # Charger le modèle LoRA
        print("🔧 Chargement du modèle LoRA...")
        peft_model = PeftModel.from_pretrained(base_model_obj, lora_path)
        
        # Fusionner les modèles
        print("⚙️ Fusion en cours...")
        merged_model = peft_model.merge_and_unload()
        
        # Sauvegarder le modèle fusionné
        print(f"💾 Sauvegarde vers {output_path}...")
        os.makedirs(output_path, exist_ok=True)
        merged_model.save_pretrained(output_path)
        tokenizer.save_pretrained(output_path)
        
        print(f"✅ Fusion terminée avec succès !")
        print(f"   Nouveau modèle disponible dans : {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la fusion : {e}")
        return False

def backup_current_model(current_path):
    """Crée une sauvegarde du modèle actuel"""
    if os.path.exists(current_path):
        backup_path = f"{current_path}_backup"
        counter = 1
        while os.path.exists(backup_path):
            backup_path = f"{current_path}_backup_{counter}"
            counter += 1
        
        print(f"📦 Sauvegarde du modèle actuel : {backup_path}")
        shutil.copytree(current_path, backup_path)
        return backup_path
    return None

def main():
    parser = argparse.ArgumentParser(
        description="Refusion d'un modèle LoRA avec EuroBERT pour le classifieur d'humour"
    )
    parser.add_argument(
        "--lora_path", 
        required=True, 
        help="Chemin vers le modèle LoRA à fusionner"
    )
    parser.add_argument(
        "--output_path", 
        default="eurobert_full_new",
        help="Chemin de sortie pour le modèle fusionné (défaut: eurobert_full_new)"
    )
    parser.add_argument(
        "--base_model",
        default="jplu/eurobert-base-cased",
        help="Modèle de base à utiliser (défaut: jplu/eurobert-base-cased)"
    )
    parser.add_argument(
        "--replace_current",
        action="store_true",
        help="Remplace le modèle actuel (eurobert_full) par le nouveau"
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Crée une sauvegarde du modèle actuel avant remplacement"
    )
    
    args = parser.parse_args()
    
    print("🔄 Script de refusion LoRA")
    print("=" * 50)
    
    # Vérifier le modèle LoRA
    if not check_lora_model(args.lora_path):
        sys.exit(1)
    
    # Fusionner le modèle
    if not fuse_lora_model(args.lora_path, args.output_path, args.base_model):
        sys.exit(1)
    
    # Gestion du remplacement
    if args.replace_current:
        current_model_path = "eurobert_full"
        
        if args.backup:
            backup_path = backup_current_model(current_model_path)
            if backup_path:
                print(f"✅ Sauvegarde créée : {backup_path}")
        
        if os.path.exists(current_model_path):
            print(f"🔄 Remplacement de {current_model_path}...")
            shutil.rmtree(current_model_path)
        
        shutil.move(args.output_path, current_model_path)
        print(f"✅ Modèle remplacé avec succès !")
        print(f"   Le nouveau modèle est maintenant dans : {current_model_path}")
    
    print("\n🎉 Processus terminé avec succès !")
    print(f"   Vous pouvez maintenant utiliser le nouveau modèle avec :")
    print(f"   python commit_humor_classifier.py --text 'votre message de test'")

if __name__ == "__main__":
    main()