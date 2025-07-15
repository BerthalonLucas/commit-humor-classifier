# 🤖 Classificateur d'Humour pour Messages de Commit

Un classificateur d'humour basé sur **EuroBERT-210m** fine-tuné avec **LoRA** pour analyser si un message de commit Git est drôle ou pas.

**🔄 Nouveau** : Le modèle est maintenant téléchargé automatiquement depuis **Hugging Face** au premier usage !

## 🚀 Démarrage Rapide

```bash
# Installation des dépendances
pip install -r requirements.txt

# Test rapide (téléchargement automatique du modèle)
python commit_humor_classifier.py "gcc et moi c'est compliqué"
```

> 💡 **Note** : Au premier usage, le modèle sera téléchargé automatiquement depuis Hugging Face (~420MB). Une connexion internet est requise uniquement pour ce téléchargement initial.

## 📖 Utilisation

### Mode Simple
```bash
python commit_humor_classifier.py "Mon message de commit"
```

### Mode Interactif  
```bash
python commit_humor_classifier.py --interactive
```

### Mode Batch
```bash
python commit_humor_classifier.py --batch test_messages.txt
```

### Options Avancées
```bash
python commit_humor_classifier.py --seuil 0.6 "Mon message"
python commit_humor_classifier.py --help
```

## 🎯 Exemples de Résultats

```bash
$ python commit_humor_classifier.py "gcc et moi c'est compliqué"
📝 'gcc et moi c'est compliqué'
   → 😄 DRÔLE (prob: 0.730)

$ python commit_humor_classifier.py "fix typo in README"  
📝 'fix typo in README'
   → 😄 DRÔLE (prob: 0.738)

$ python commit_humor_classifier.py "Add cat gifs because why not"
📝 'Add cat gifs because why not'
   → 😐 PAS DRÔLE (prob: 0.280)
```

## 🏗️ Architecture

- **Modèle Base** : EuroBERT-210m (210M paramètres)
- **Fine-tuning** : LoRA (Low-Rank Adaptation) 
- **Dataset** : Messages de commit annotés (drôle/pas drôle)
- **Classification** : Binaire avec seuil ajustable
- **Inférence** : Pipeline Transformers optimisé

## 📦 Structure du Projet

```
commit-humor-classifier/
├── commit_humor_classifier.py    # Script principal
├── eurobert_full/               # Modèle téléchargé (créé automatiquement)
├── refusion_lora.py             # Script de refusion LoRA
├── requirements.txt             # Dépendances
├── setup.py                     # Installation
├── test_commits_evaluation.txt  # Messages de test
├── deploy_package.py            # Script de déploiement
├── REFUSION_GUIDE.md            # Guide de refusion
└── README.md                    # Documentation
```

> 💡 **Note** : Le dossier `eurobert_full/` est créé automatiquement lors du premier téléchargement du modèle depuis Hugging Face.

## 🔧 Prérequis

- Python 3.7+
- PyTorch 1.9+
- Transformers 4.20+
- Hugging Face Hub 0.16+
- Connexion internet (pour le téléchargement initial)
- CUDA recommandé (optionnel)

## 📈 Performance

- **Temps d'inférence** : ~100ms par message (GPU)
- **Mémoire** : ~1GB VRAM (GPU) / ~2GB RAM (CPU)
- **Précision** : Optimisée avec early stopping

## 🚚 Déploiement

### Installation Automatique
```bash
python deploy_package.py
```

### Installation Manuelle
```bash
pip install -e .
```

### Utilisation en tant que module
```python
from commit_humor_classifier import CommitHumorClassifier

# Utilisation avec téléchargement automatique depuis Hugging Face
classifier = CommitHumorClassifier()
classifier.load_model()
result = classifier.predict("Mon message de commit")
print(result)

# Utilisation avec ID de modèle personnalisé
classifier = CommitHumorClassifier(
    model_path="mon_modele_local",
    model_id="mon-utilisateur/mon-modele-hf"
)
classifier.load_model()
result = classifier.predict("Mon message de commit")
print(result)
```

## 🎪 Cas d'Usage

- **Hooks Git** : Validation automatique des messages
- **Code Review** : Détection d'humour dans les PR
- **Statistiques** : Analyse des patterns d'équipe
- **Bots** : Intégration Discord/Slack/Teams

## 🛠️ Développement

### Structure Technique
- **Base** : EuroBERT (européen, multilingual)
- **Fine-tuning** : LoRA avec r=16, alpha=32
- **Optimiseur** : AdamW avec linear warmup
- **Early stopping** : Validation loss monitoring

### Fichiers Techniques
- `commit_humor_classifier.py` : Classe principale + CLI
- `eurobert_full/` : Modèle fusionné prêt à l'emploi
- `deploy_package.py` : Création de package portable

## 🔍 Métadonnées du Modèle

- **Modèle** : EuroBERT-210m
- **Tokenizer** : Compatible BERT
- **Classes** : [PAS DRÔLE, DRÔLE]
- **Seuil par défaut** : 0.7
- **Format** : PyTorch + Transformers

## 🔄 Refusion LoRA

### Intégration automatique après nouvel entraînement

Le projet inclut un script de refusion automatique pour intégrer facilement un nouveau modèle LoRA après un entraînement :

```bash
# Activer l'environnement virtuel
..\dataset_env\Scripts\activate

# Fusionner un nouveau modèle LoRA
python refusion_lora.py --lora_path ../eurobert_peft_v4 --output_path eurobert_full_v2

# Tester le nouveau modèle
python commit_humor_classifier.py --text "test message" --model_path eurobert_full_v2

# Si satisfaisant, remplacer l'actuel avec sauvegarde
python refusion_lora.py --lora_path ../eurobert_peft_v4 --replace_current --backup
```

### Options du script de refusion

| Option | Description | Exemple |
|--------|-------------|---------|
| `--lora_path` | Chemin vers le modèle LoRA (obligatoire) | `../eurobert_peft_v4` |
| `--output_path` | Nom du modèle fusionné | `eurobert_full_v2` |
| `--replace_current` | Remplace le modèle actuel | Flag |
| `--backup` | Crée une sauvegarde avant remplacement | Flag |

**📖 Consultez [`REFUSION_GUIDE.md`](REFUSION_GUIDE.md) pour le guide complet**

### Workflow recommandé

1. **Entraîner** un nouveau modèle LoRA avec `optimize_eurobert_final.py`
2. **Fusionner** avec `refusion_lora.py`
3. **Tester** sur les données d'évaluation
4. **Remplacer** le modèle actuel si satisfaisant

## 🐛 Dépannage

### Erreurs Courantes
```bash
# Erreur de téléchargement du modèle
# Vérifiez votre connexion internet
ping huggingface.co

# Modèle introuvable après téléchargement
ls -la eurobert_full/

# Dépendances manquantes
pip install --upgrade -r requirements.txt

# Problème GPU
python -c "import torch; print(torch.cuda.is_available())"

# Problème avec Hugging Face Hub
pip install --upgrade huggingface_hub
```

### Téléchargement Manuel
Si le téléchargement automatique échoue, vous pouvez télécharger manuellement :
```bash
# Avec Python
python -c "
from huggingface_hub import snapshot_download
snapshot_download('shadow-commits/eurobert-commit-humor-classifier', local_dir='eurobert_full')
"

# Ou forcer le re-téléchargement
rm -rf eurobert_full/
python commit_humor_classifier.py 'test'
```

## 📄 Licence

MIT License - Libre d'utilisation et de modification

## 👥 Contribution

Les contributions sont bienvenues ! Créez une issue ou une pull request.

---

**Version** : 1.0.0  
**Auteur** : Assistant IA  
**Date** : 2025