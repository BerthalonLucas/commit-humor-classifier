# 🤖 Classificateur d'Humour pour Messages de Commit

Un classificateur d'humour basé sur **EuroBERT-210m** pour analyser si un message de commit Git est drôle ou pas.

---

## ⚡ Installation Rapide (Pour Exam à 42)

### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd commit-humor-classifier
```

### 2. Créer un environnement virtuel
```bash
# Windows
python -m venv .venv

# Linux/Mac
python3 -m venv .venv
```
> 💡 L'environnement virtuel évite d'installer les packages ailleurs que pour ce projet.

### 3. Activer l'environnement virtuel
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 4. Installer les dépendances
```bash
# ⚠️ ATTENTION : Si vous n'avez pas de GPU ou peu d'espace disque, utilisez OBLIGATOIREMENT :
python install.py --force-cpu

# Sinon, installation normale (télécharge +5Go de packages NVIDIA) :
python install.py
```
> 🚨 **WARNING** : Sans le flag `--force-cpu`, le package `accelerate` installera automatiquement les packages NVIDIA qui font plus de 5Go ! Utilisez `--force-cpu` si vous n'avez pas de GPU ou peu d'espace.

### 5. Configurer le fichier de commits
```bash
# Windows
set COMMITS_JSON=chemin/vers/votre/fichier.json

# Linux/Mac
export COMMITS_JSON=chemin/vers/votre/fichier.json
```

### 6. Installer Flask
```bash
pip install flask
```

### 7. Lancer l'interface web
```bash
python web_app.py
```
> 🌐 Ouvrez http://localhost:5000 pour voir les commits drôles s'afficher !

### 8. Interface web avec mode debug des prédictions
```bash
set DEBUG_PREDICTIONS=true
python web_app.py
```

> 🚨 **AVERTISSEMENT** : Il est fortement recommandé d'activer le mode debug et d'effectuer un test initial avec d'anciens fichiers JSON de commits pour vérifier le bon fonctionnement du système.

Voici un exemple des messages de logs en mode debug :

```bash
2025-09-05 08:28:36,153 - DEBUG - PREDICTION: [NORMAL] P=0.020 | oui
2025-09-05 08:28:36,171 - DEBUG - PREDICTION: [NORMAL] P=0.136 | f ?
2025-09-05 08:28:36,192 - DEBUG - PREDICTION: [FUNNY] P=0.848 | comment je me suis loupe sur l'exo deux la loose vrm
```

### 9. Message de fin

> ⚠️ **NOTE IMPORTANTE** : Pour simplifier l'utilisation, il est recommandé de placer le fichier JSON directement dans le répertoire "commit-humor-classifier". Veuillez noter qu'un délai de 30 secondes à 1 minute est normal après l'ajout du fichier JSON - ce temps est nécessaire pour charger le modèle, analyser le fichier et traiter les messages un par un.


**✅ C'est tout ! L'installation pour un examen à 42 cette partie suffit.**

---

## 📚 Documentation Complète

**🎯 Performance** : 85.3% précision globale, 82.9% précision "funny"
**🔄 Nouveau** : Installation automatique avec détection hardware + traitement JSON en temps réel !

### 🚀 Installation Automatique Avancée

```bash
# Installation intelligente (détecte GPU/CPU automatiquement)
python install.py

# Force CPU même si GPU détecté
python install.py --force-cpu

# Force GPU (échoue si pas de GPU)
python install.py --gpu-only

# Interface web (après installation de Flask)
python web_app.py

# Interface web avec mode debug des prédictions
set DEBUG_PREDICTIONS=true
python web_app.py
```

## ⚡ Démarrage Rapide

```bash
# Test rapide (téléchargement automatique du modèle)
python commit_humor_classifier.py "gcc et moi c'est compliqué"

# Configurer la variable d'environnement pour le JSON
# set COMMITS_JSON=chemin/vers/votre/commits.json
```

> 💡 **Note** : Au premier usage, le modèle sera téléchargé automatiquement depuis Hugging Face (~420MB) et fusionné dans le dossier `eurobert_full/`. Une connexion internet est requise uniquement pour ce téléchargement initial.

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
python commit_humor_classifier.py --batch votre_fichier.txt
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

### Variables d'Environnement

| Variable | Description | Valeur par défaut | Exemple |
|----------|-------------|-------------------|----------|
| `COMMITS_JSON` | Chemin vers le fichier JSON de commits | `commits.json` | `set COMMITS_JSON=data/commits.json` |
| `DEBUG_PREDICTIONS` | Active le logging des prédictions du modèle | `false` | `set DEBUG_PREDICTIONS=true` |

> 💡 **Mode Debug** : Quand `DEBUG_PREDICTIONS=true`, chaque prédiction est loggée sur une seule ligne avec le statut (FUNNY/NORMAL), la probabilité et un extrait du message.

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
│   └── web_app.py                    # Interface web Flask
├── 🎨 Interface Web
│   └── templates/
│       └── index.html                # Template de l'interface web
├── 🤖 Modèle
│   └── eurobert_full/                # Modèle fusionné (généré automatiquement)
├── 📁 Configuration
│   ├── requirements.txt              # Dépendances Python
│   ├── config.json                   # Configuration du projet
│   ├── commits.json                  # Fichier de commits (exemple)
│   └── .gitignore                    # Fichiers ignorés
├── 🔧 Scripts Utilitaires
│   ├── deploy.py                     # Script de déploiement et création d'archives
│   └── update.py                     # Script de mise à jour automatique
└── 📚 Documentation
    └── README.md                     # Documentation principale
```

> 💡 **Note** : Le dossier `eurobert_full/` contient le modèle fusionné prêt à l'emploi et est créé automatiquement lors de la première utilisation du classificateur.

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

### Création de Packages

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

Le script `deploy.py` permet de créer des packages portables et des archives ZIP pour faciliter la distribution du projet.

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
- **Mise à jour automatique** : Script `update.py` pour maintenir à jour
- **Configuration centralisée** : Fichier `config.json` pour la personnalisation

### 📺 Application Web Locale

Une petite application Flask permet d'afficher en grand les commits
jugés drôles en temps réel. Le fichier JSON surveillé est relu toutes
les minutes et seuls les nouveaux messages sont classifiés.

```bash
# Installation des dépendances supplémentaires
pip install Flask

# Lancement (utilise commits.json par défaut)
python web_app.py
```

Définissez la variable d'environnement `COMMITS_JSON` pour indiquer un
autre fichier. Ouvrez ensuite `http://localhost:5000` pour consulter la
liste mise à jour.

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
- `process_commits_json.py` : Traitement des fichiers JSON de commits
- `web_app.py` : Interface web Flask
- `eurobert_full/` : Modèle fusionné prêt à l'emploi (généré automatiquement)
- `deploy.py` : Création de packages portables

## 🔍 Métadonnées du Modèle

- **Modèle** : EuroBERT-210m
- **Tokenizer** : Compatible BERT
- **Classes** : [PAS DRÔLE, DRÔLE]
- **Seuil par défaut** : 0.7
- **Format** : PyTorch + Transformers

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