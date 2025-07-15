#!/usr/bin/env python3
"""
Script de test du modèle avant upload sur Hugging Face
"""

import os
import sys
from pathlib import Path
import json

def test_model_structure():
    """Vérifier la structure du modèle"""
    print("🔍 Vérification de la structure du modèle...")
    
    model_path = Path("eurobert_full")
    
    required_files = {
        "config.json": "Configuration du modèle",
        "model.safetensors": "Poids du modèle",
        "tokenizer.json": "Tokenizer",
        "tokenizer_config.json": "Configuration du tokenizer",
        "special_tokens_map.json": "Tokens spéciaux",
        "configuration_eurobert.py": "Configuration personnalisée",
        "modeling_eurobert.py": "Modèle personnalisé"
    }
    
    missing_files = []
    
    for file, description in required_files.items():
        file_path = model_path / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✅ {file} ({size:,} bytes) - {description}")
        else:
            missing_files.append(file)
            print(f"❌ {file} - {description}")
    
    if missing_files:
        print(f"\n❌ Fichiers manquants : {', '.join(missing_files)}")
        return False
    
    print("✅ Tous les fichiers requis sont présents")
    return True

def test_config_validity():
    """Vérifier la validité de la configuration"""
    print("\n🔍 Vérification de la configuration...")
    
    config_path = Path("eurobert_full/config.json")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Vérifier les champs essentiels
        required_fields = [
            "model_type",
            "num_hidden_layers",
            "hidden_size",
            "num_attention_heads",
            "vocab_size"
        ]
        
        for field in required_fields:
            if field in config:
                print(f"✅ {field}: {config[field]}")
            else:
                print(f"❌ Champ manquant : {field}")
                return False
        
        # Vérifier auto_map
        if "auto_map" in config:
            print("✅ auto_map configuré pour les classes personnalisées")
            for key, value in config["auto_map"].items():
                print(f"   {key}: {value}")
        else:
            print("⚠️  auto_map non configuré")
        
        print("✅ Configuration valide")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de la configuration : {e}")
        return False

def test_model_loading():
    """Tester le chargement du modèle"""
    print("\n🔍 Test de chargement du modèle...")
    
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        
        # Charger le tokenizer
        print("📥 Chargement du tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained("eurobert_full", trust_remote_code=True)
        print(f"✅ Tokenizer chargé - Vocabulaire : {tokenizer.vocab_size}")
        
        # Charger le modèle
        print("📥 Chargement du modèle...")
        model = AutoModelForSequenceClassification.from_pretrained("eurobert_full", trust_remote_code=True)
        print(f"✅ Modèle chargé - Paramètres : {model.num_parameters():,}")
        
        # Test d'inférence simple
        print("🧪 Test d'inférence...")
        test_message = "gcc et moi c'est compliqué"
        inputs = tokenizer(test_message, return_tensors="pt", truncation=True, padding=True)
        
        import torch
        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            confidence = probabilities.max().item()
        
        print(f"✅ Inférence réussie - Confiance : {confidence:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement : {e}")
        return False

def test_huggingface_compatibility():
    """Tester la compatibilité avec Hugging Face"""
    print("\n🔍 Test de compatibilité Hugging Face...")
    
    try:
        # Vérifier que les dépendances sont installées
        import huggingface_hub
        print(f"✅ huggingface_hub version : {huggingface_hub.__version__}")
        
        import transformers
        print(f"✅ transformers version : {transformers.__version__}")
        
        # Vérifier la connexion
        from huggingface_hub import HfApi
        api = HfApi()
        try:
            user_info = api.whoami()
            print(f"✅ Connecté à Hugging Face : {user_info['name']}")
        except Exception:
            print("⚠️  Non connecté à Hugging Face (utilisez : huggingface-cli login)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Dépendance manquante : {e}")
        return False

def main():
    print("🧪 Test du modèle avant upload sur Hugging Face")
    print("=" * 60)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not Path("eurobert_full").exists():
        print("❌ Dossier 'eurobert_full' introuvable")
        print("💡 Assurez-vous d'être dans le répertoire commit-humor-classifier")
        return
    
    tests = [
        ("Structure du modèle", test_model_structure),
        ("Configuration", test_config_validity),
        ("Chargement du modèle", test_model_loading),
        ("Compatibilité Hugging Face", test_huggingface_compatibility)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 Test : {test_name}")
        if test_func():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Résultats : {passed} ✅ réussis, {failed} ❌ échoués")
    
    if failed == 0:
        print("🎉 Tous les tests sont passés ! Votre modèle est prêt pour l'upload.")
        print("\n🚀 Étapes suivantes :")
        print("1. python quick_upload_hf.py")
        print("2. ou python upload_to_hf.py --repo_name votre-nom/eurobert-commit-humor")
    else:
        print("❌ Certains tests ont échoué. Corrigez les problèmes avant l'upload.")
        print("📖 Consultez HUGGINGFACE_GUIDE.md pour plus d'aide")

if __name__ == "__main__":
    main()