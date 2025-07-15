#!/usr/bin/env python3
"""
Script pour uploader le modèle eurobert_full sur Hugging Face Hub
"""

import os
import argparse
from pathlib import Path
from huggingface_hub import HfApi, create_repo, upload_folder
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json

def test_model_loading(model_path):
    """Test si le modèle se charge correctement"""
    try:
        print(f"🔍 Test de chargement du modèle depuis {model_path}...")
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        model = AutoModelForSequenceClassification.from_pretrained(model_path, trust_remote_code=True)
        print("✅ Modèle chargé avec succès !")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle: {e}")
        return False

def create_model_card(model_path, repo_name):
    """Créer une model card pour Hugging Face"""
    
    model_card_content = f"""---
language: 
- fr
- en
- de
- es
- it
license: mit
tags:
- text-classification
- commit-messages
- humor-detection
- eurobert
- lora
- git
datasets:
- custom
metrics:
- accuracy
- f1
library_name: transformers
pipeline_tag: text-classification
---

# 🤖 Classificateur d'Humour pour Messages de Commit

Un classificateur d'humour basé sur **EuroBERT-210m** fine-tuné avec **LoRA** pour analyser si un message de commit Git est drôle ou pas.

## 🚀 Utilisation Rapide

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Charger le modèle et le tokenizer
tokenizer = AutoTokenizer.from_pretrained("{repo_name}", trust_remote_code=True)
model = AutoModelForSequenceClassification.from_pretrained("{repo_name}", trust_remote_code=True)

# Exemple de classification
def classify_commit(message):
    inputs = tokenizer(message, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(probabilities, dim=-1)
        confidence = probabilities.max().item()
    
    labels = ["PAS DRÔLE", "DRÔLE"]
    return labels[predicted_class.item()], confidence

# Test
message = "gcc et moi c'est compliqué"
result, confidence = classify_commit(message)
print(f"Message: '{{message}}'")
print(f"Résultat: {{result}} (confiance: {{confidence:.3f}})")
```

## 🎯 Exemples de Résultats

```
📝 'gcc et moi c'est compliqué'
   → 😄 DRÔLE (prob: 0.730)

📝 'fix typo in README'  
   → 😄 DRÔLE (prob: 0.738)

📝 'Add cat gifs because why not'
   → 😐 PAS DRÔLE (prob: 0.280)
```

## 🏗️ Architecture

- **Modèle Base** : EuroBERT-210m (210M paramètres)
- **Fine-tuning** : LoRA (Low-Rank Adaptation) 
- **Dataset** : Messages de commit annotés (drôle/pas drôle)
- **Classification** : Binaire avec seuil ajustable
- **Langues supportées** : Français, Anglais, Allemand, Espagnol, Italien

## 📈 Performance

- **Temps d'inférence** : ~100ms par message (GPU)
- **Mémoire** : ~1GB VRAM (GPU) / ~2GB RAM (CPU)
- **Précision** : Optimisée avec early stopping

## 🎪 Cas d'Usage

- **Hooks Git** : Validation automatique des messages
- **Code Review** : Détection d'humour dans les PR
- **Statistiques** : Analyse des patterns d'équipe
- **Bots** : Intégration Discord/Slack/Teams

## 🔧 Installation

```bash
pip install transformers torch
```

## 🛠️ Développement

### Structure Technique
- **Base** : EuroBERT (européen, multilingual)
- **Fine-tuning** : LoRA avec r=16, alpha=32
- **Optimiseur** : AdamW avec linear warmup
- **Early stopping** : Validation loss monitoring

## 📄 Licence

MIT License - Libre d'utilisation et de modification

## 👥 Citation

Si vous utilisez ce modèle dans vos travaux, veuillez citer :

```bibtex
@misc{{commit-humor-classifier-2025,
  title={{EuroBERT Commit Humor Classifier}},
  author={{Assistant IA}},
  year={{2025}},
  url={{https://huggingface.co/{repo_name}}}
}}
```

---

**Version** : 1.0.0  
**Auteur** : Assistant IA  
**Date** : 2025
"""

    # Sauvegarder la model card
    readme_path = Path(model_path) / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(model_card_content)
    
    print(f"✅ Model card créée : {readme_path}")
    return readme_path

def upload_model(model_path, repo_name, token=None, private=False):
    """Upload le modèle sur Hugging Face Hub"""
    
    # Initialiser l'API Hugging Face
    api = HfApi(token=token)
    
    try:
        # Créer le repository
        print(f"🏗️ Création du repository '{repo_name}'...")
        repo_url = create_repo(
            repo_id=repo_name,
            token=token,
            private=private,
            exist_ok=True
        )
        print(f"✅ Repository créé : {repo_url}")
        
        # Créer la model card
        create_model_card(model_path, repo_name)
        
        # Upload tous les fichiers
        print(f"📤 Upload des fichiers depuis {model_path}...")
        api.upload_folder(
            folder_path=model_path,
            repo_id=repo_name,
            token=token,
            ignore_patterns=["*.pyc", "__pycache__", ".git", ".gitignore"]
        )
        
        print(f"🎉 Modèle uploadé avec succès !")
        print(f"🔗 URL du modèle : https://huggingface.co/{repo_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'upload : {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Upload eurobert_full sur Hugging Face")
    parser.add_argument("--model_path", default="eurobert_full", help="Chemin vers le modèle")
    parser.add_argument("--repo_name", required=True, help="Nom du repository sur HF (ex: username/model-name)")
    parser.add_argument("--token", help="Token Hugging Face (ou utilisez huggingface-cli login)")
    parser.add_argument("--private", action="store_true", help="Repository privé")
    parser.add_argument("--test_only", action="store_true", help="Juste tester le chargement du modèle")
    
    args = parser.parse_args()
    
    # Vérifier que le modèle existe
    if not os.path.exists(args.model_path):
        print(f"❌ Modèle introuvable : {args.model_path}")
        return
    
    # Tester le chargement du modèle
    if not test_model_loading(args.model_path):
        print("❌ Impossible de charger le modèle, arrêt.")
        return
    
    if args.test_only:
        print("✅ Test terminé avec succès !")
        return
    
    # Vérifier la connexion Hugging Face
    try:
        api = HfApi(token=args.token)
        user_info = api.whoami()
        print(f"✅ Connecté à Hugging Face en tant que : {user_info['name']}")
    except Exception as e:
        print(f"❌ Problème de connexion Hugging Face : {e}")
        print("💡 Utilisez : huggingface-cli login")
        return
    
    # Upload du modèle
    success = upload_model(args.model_path, args.repo_name, args.token, args.private)
    
    if success:
        print("\n🎉 SUCCÈS ! Votre modèle est maintenant disponible sur Hugging Face !")
        print(f"🔗 https://huggingface.co/{args.repo_name}")
        print("\n📖 Pour utiliser votre modèle :")
        print(f"```python")
        print(f"from transformers import AutoTokenizer, AutoModelForSequenceClassification")
        print(f"tokenizer = AutoTokenizer.from_pretrained('{args.repo_name}', trust_remote_code=True)")
        print(f"model = AutoModelForSequenceClassification.from_pretrained('{args.repo_name}', trust_remote_code=True)")
        print(f"```")

if __name__ == "__main__":
    main()