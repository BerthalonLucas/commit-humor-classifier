# 🤖 Classificateur d'Humour pour Messages de Commit

Ce package contient un classificateur d'humour basé sur EuroBERT-210m pour analyser si un message de commit est drôle ou pas.

**🔄 Nouveau** : Le modèle est maintenant téléchargé automatiquement depuis **Hugging Face** au premier usage !

## 📦 Contenu du Package

```
commit-humor-classifier/
├── commit_humor_classifier.py    # Script principal tout-en-un
├── eurobert_full/               # Modèle téléchargé automatiquement
├── requirements.txt             # Dépendances Python
├── setup.py                     # Script d'installation
└── README_PORTABLE.md           # Ce fichier
```

> 💡 **Note** : Le dossier `eurobert_full/` est créé automatiquement lors du premier téléchargement du modèle depuis Hugging Face (~420MB).

## 🚀 Installation Rapide

### 1. Prérequis
- Python 3.7+
- pip installé
- Connexion internet (pour le téléchargement initial du modèle)

### 2. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 3. Test rapide (téléchargement automatique du modèle)

```bash
python commit_humor_classifier.py "gcc et moi c'est compliqué"
```

> 💡 **Note** : Au premier usage, le modèle sera téléchargé automatiquement depuis Hugging Face. Cela peut prendre quelques minutes selon votre connexion.

## 📖 Utilisation

### Mode Simple
```bash
python commit_humor_classifier.py "Mon message de commit"
```

### Mode Interactif
```bash
python commit_humor_classifier.py --interactive
```

### Mode Batch (depuis un fichier)
```bash
python commit_humor_classifier.py --batch messages.txt
```

### Options avancées
```bash
python commit_humor_classifier.py --seuil 0.6 "Mon message"
python commit_humor_classifier.py --model autre_modele/ "Mon message"
```

## 🎯 Exemples

### Messages drôles détectés :
- "gcc et moi c'est compliqué" → DRÔLE (73%)
- "Add cat gifs because why not" → PAS DRÔLE (28%)
- "supprime tous les bugs (lol)" → PAS DRÔLE (60%)

### Mode interactif :
```
🎯 Mode interactif - Tapez 'quit' pour quitter
==================================================

📝 Message de commit : gcc et moi c'est compliqué
   → 😄 DRÔLE (prob: 0.730)

📝 Message de commit : fix typo in README
   → 😄 DRÔLE (prob: 0.738)

📝 Message de commit : quit
👋 Au revoir !
```

## 🔧 Architecture Technique

### Modèle utilisé
- **Base** : EuroBERT-210m (modèle pré-entraîné européen)
- **Fine-tuning** : LoRA (Low-Rank Adaptation) sur dataset de commits
- **Classes** : Classification binaire (drôle/pas drôle)
- **Format** : Modèle fusionné prêt pour inférence

### Structure des dossiers
```
eurobert_full/
├── config.json              # Configuration du modèle
├── pytorch_model.bin         # Poids du modèle
├── tokenizer_config.json     # Configuration du tokenizer
├── tokenizer.json           # Tokenizer compilé
└── vocab.txt                # Vocabulaire
```

## 📊 Performance

- **Précision** : Optimisée pendant le fine-tuning
- **Seuil par défaut** : 0.5 (ajustable via --seuil)
- **Temps d'inférence** : ~100ms par message (GPU)
- **Mémoire** : ~1GB VRAM (GPU) ou ~2GB RAM (CPU)

## 🛠️ Dépannage

### Erreur de téléchargement du modèle
```bash
# Vérifiez votre connexion internet
ping huggingface.co

# Téléchargement manuel si nécessaire
python -c "
from huggingface_hub import snapshot_download
snapshot_download('shadow-commits/eurobert-commit-humor-classifier', local_dir='eurobert_full')
"
```

### Erreur "Modèle introuvable"
```bash
# Vérifiez que le dossier eurobert_full existe après téléchargement
ls -la eurobert_full/

# Forcer le re-téléchargement si corrompu
rm -rf eurobert_full/
python commit_humor_classifier.py "test"
```

### Erreur de dépendances
```bash
# Réinstallez les dépendances
pip install --upgrade -r requirements.txt

# Spécifiquement pour Hugging Face Hub
pip install --upgrade huggingface_hub
```

### Performance lente
```bash
# Vérifiez la disponibilité du GPU
python -c "import torch; print(torch.cuda.is_available())"
```

## 🔄 Mise à jour du seuil

Pour optimiser les résultats, vous pouvez ajuster le seuil :

```bash
# Seuil plus strict (moins de messages classés drôles)
python commit_humor_classifier.py --seuil 0.7 "Mon message"

# Seuil plus permissif (plus de messages classés drôles)
python commit_humor_classifier.py --seuil 0.3 "Mon message"
```

## 📝 Format des fichiers batch

Pour le mode batch, créez un fichier texte avec un message par ligne :

```txt
fix typo in README
gcc et moi c'est compliqué
Add cat gifs because why not
Implement user authentication
```

## 🚚 Déploiement

### Sur une nouvelle machine :
1. Copiez tout le dossier
2. Installez Python 3.7+
3. Exécutez : `pip install -r requirements.txt`
4. Testez : `python commit_humor_classifier.py "test"`

### En tant que service :
Le script peut être intégré dans des hooks Git, des CI/CD, ou des bots Discord/Slack.

## 📈 Métriques du modèle

- **Époque d'arrêt** : Early stopping activé
- **Optimiseur** : AdamW
- **Scheduler** : Linear warmup + decay
- **Technique** : LoRA avec r=16, alpha=32

## 🎪 Cas d'usage

- **Hooks Git** : Validation automatique des messages
- **Code review** : Détection d'humour dans les PR
- **Statistiques** : Analyse des patterns d'équipe
- **Bots** : Intégration Discord/Slack

---

**Auteur** : Assistant IA  
**Version** : 1.0  
**Date** : 2025  
**Licence** : MIT