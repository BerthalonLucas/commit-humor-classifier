# 🤖 Classificateur d'Humour pour Messages de Commit

Un classificateur d'humour basé sur **EuroBERT-210m** optimisé avec **Optuna** pour analyser si un message de commit Git est drôle ou pas.

**🎯 Performance** : 85.3% précision globale, 82.9% précision "funny"
**🔄 Nouveau** : Installation automatique avec détection hardware + traitement JSON en temps réel !

## 🚀 Installation Automatique

```bash
# Installation intelligente (détecte GPU/CPU automatiquement)
python install.py

# Force CPU même si GPU détecté
python install.py --force-cpu

# Force GPU (échoue si pas de GPU)
python install.py --gpu-only

# Démarrage rapide (pour les nouveaux utilisateurs)
python quick_start.py
```

## ⚡ Démarrage Rapide

```bash
# Test rapide (téléchargement automatique du modèle)
python commit_humor_classifier.py "gcc et moi c'est compliqué"

# Test de l'installation
python test_installation.py
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

### Traitement de Commits JSON
```bash
# Traiter un fichier JSON de commits (format exam-2024-09-13.json)
python process_commits_json.py commits.json

# Sauvegarder les résultats
python process_commits_json.py commits.json --output results.json

# Mode surveillance (traite les nouveaux commits en temps réel)
python process_commits_json.py commits.json --watch --interval 5

# Afficher les statistiques détaillées
python process_commits_json.py commits.json --stats
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
├── 🚀 Scripts Principaux
│   ├── commit_humor_classifier.py    # Classificateur principal
│   ├── process_commits_json.py       # Traitement JSON en temps réel
│   ├── install.py                    # Installation automatique
│   └── quick_start.py                # Démarrage rapide pour nouveaux utilisateurs
├── 🧪 Tests et Validation
│   ├── test_installation.py          # Test d'installation (généré auto)
│   ├── test_commits_evaluation.txt   # Messages de test
│   └── test_messages.txt             # Exemples de test
├── 📁 Modèle et Configuration
│   ├── eurobert_full/                # Modèle téléchargé (créé auto)
│   ├── requirements.txt              # Dépendances Python
│   └── .gitignore                    # Fichiers ignorés
├── 🔧 Scripts Utilitaires
│   ├── deploy.py                     # Script de déploiement et création d'archives
│   ├── update.py                     # Script de mise à jour automatique
│   └── config.json                   # Configuration du projet
├── 📦 Déploiement
│   ├── deployment_info.json          # Informations de déploiement
│   └── deploy/                       # Dossier de déploiement (créé auto)
└── 📚 Documentation
    └── README.md                     # Documentation principale
```

> 💡 **Note** : Le dossier `eurobert_full/` et `test_installation.py` sont créés automatiquement.

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

### Déploiement Automatique

```bash
# Créer un package portable complet
python deploy.py --package

# Créer une archive ZIP pour distribution
python deploy.py --archive

# Créer package + archive + nettoyage
python deploy.py --all

# Nettoyer les fichiers temporaires
python deploy.py --clean
```

### Installation Manuelle
```bash
pip install -e .
```

### Distribution

Le script `deploy.py` crée automatiquement :
- Un package portable dans `deploy/package/`
- Une archive ZIP dans `deploy/archives/`
- Un script de démarrage rapide `quick_start.py`
- Les informations de déploiement `deployment_info.json`

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

### 🔄 Temps Réel
- **Surveillance de commits** : Traitement automatique des nouveaux commits JSON
- **Hooks Git** : Validation automatique des messages
- **CI/CD Pipeline** : Intégration dans les workflows
- **Monitoring** : Surveillance continue des repositories

### 📊 Analyse et Statistiques
- **Code Review** : Détection d'humour dans les PR
- **Statistiques d'équipe** : Analyse des patterns d'humour
- **Rapports** : Génération de métriques sur l'humour
- **Dashboards** : Visualisation des tendances
- **Tendances** : Évolution de l'humour dans le temps

### 🤖 Intégrations et Automatisation
- **Bots** : Discord/Slack/Teams/Mattermost
- **APIs** : Endpoints REST pour classification
- **Webhooks** : Traitement automatique des événements Git
- **Microservices** : Service de classification dédié

### Distribution et Déploiement
- **Packages portables** : Distribution facile via `deploy.py`
- **Archives ZIP** : Partage simplifié
- **Installation automatique** : Déploiement en un clic
- **Démarrage rapide** : Script `quick_start.py` pour nouveaux utilisateurs
- **Mise à jour automatique** : Script `update.py` pour maintenir à jour
- **Configuration centralisée** : Fichier `config.json` pour la personnalisation

## 📋 Format JSON Supporté

Le script `process_commits_json.py` supporte le format JSON standard des commits :

```json
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
    "message": "gcc et moi c'est compliqué"
  }
]
```

### 📤 Format de Sortie

Les résultats incluent la classification d'humour :

```json
{
  "sha": "d505efb38b3e24e06923be4333a7c3fd874a1856",
  "message": "gcc et moi c'est compliqué",
  "humor_classification": {
    "message": "gcc et moi c'est compliqué",
    "is_funny": true,
    "confidence": 0.847,
    "label": "DRÔLE",
    "processed_at": "2025-01-27T10:30:45.123456"
  }
}
```

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

## 🔄 Maintenance et Mises à Jour

### Mise à Jour Automatique

```bash
# Vérifier les mises à jour disponibles
python update.py --check

# Mise à jour complète (dépendances + modèle)
python update.py

# Mise à jour des dépendances uniquement
python update.py --dependencies

# Mise à jour du modèle uniquement
python update.py --model

# Forcer la mise à jour
python update.py --force
```

### Configuration

Le fichier `config.json` permet de personnaliser :
- Paramètres du modèle
- URLs de téléchargement
- Seuils de classification
- Options de performance

### Sauvegarde

Le script de mise à jour crée automatiquement des sauvegardes dans `backup/` avant toute modification.

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