# 🤗 Guide d'Upload sur Hugging Face

Ce guide vous explique comment publier votre modèle `eurobert_full` sur Hugging Face Hub.

## 📋 Prérequis

1. **Compte Hugging Face** : Créez un compte sur [huggingface.co](https://huggingface.co)
2. **Token d'accès** : Obtenez votre token depuis [Settings > Access Tokens](https://huggingface.co/settings/tokens)

## 🔧 Installation

### 1. Installer les dépendances

```bash
# Méthode automatique
python install_hf_dependencies.py

# Ou méthode manuelle
pip install huggingface_hub transformers torch datasets
```

### 2. Connexion à Hugging Face

```bash
huggingface-cli login
```

Entrez votre token quand demandé.

## 🚀 Upload du Modèle

### 1. Test du modèle (optionnel)

```bash
# Vérifier que le modèle se charge correctement
python upload_to_hf.py --test_only
```

### 2. Upload sur Hugging Face

```bash
# Upload public
python upload_to_hf.py --repo_name votre-nom/eurobert-commit-humor

# Upload privé
python upload_to_hf.py --repo_name votre-nom/eurobert-commit-humor --private
```

## 📖 Exemples d'Usage

### Upload Simple

```bash
python upload_to_hf.py --repo_name shadow-dev/eurobert-commit-humor
```

### Upload avec Options

```bash
# Spécifier un chemin de modèle différent
python upload_to_hf.py --model_path eurobert_full_v2 --repo_name shadow-dev/eurobert-commit-humor-v2

# Upload privé avec token explicite
python upload_to_hf.py --repo_name shadow-dev/eurobert-commit-humor --private --token hf_xxxxx
```

## 📝 Noms de Repository Recommandés

- `votre-nom/eurobert-commit-humor`
- `votre-nom/commit-humor-classifier`
- `votre-nom/eurobert-git-humor`
- `votre-nom/french-commit-humor`

## 🎯 Après l'Upload

### 1. Vérifier sur Hugging Face

Votre modèle sera disponible sur : `https://huggingface.co/votre-nom/nom-du-modele`

### 2. Utiliser le Modèle

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Charger depuis Hugging Face
tokenizer = AutoTokenizer.from_pretrained("votre-nom/eurobert-commit-humor", trust_remote_code=True)
model = AutoModelForSequenceClassification.from_pretrained("votre-nom/eurobert-commit-humor", trust_remote_code=True)

# Fonction de classification
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
result, confidence = classify_commit("gcc et moi c'est compliqué")
print(f"Résultat: {result} (confiance: {confidence:.3f})")
```

### 3. Utiliser avec Pipeline

```python
from transformers import pipeline

classifier = pipeline("text-classification", model="votre-nom/eurobert-commit-humor", trust_remote_code=True)
result = classifier("fix: gcc et moi c'est compliqué")
print(result)
```

## 🛠️ Troubleshooting

### Erreur de Connexion

```bash
# Vérifier la connexion
huggingface-cli whoami

# Se reconnecter
huggingface-cli login
```

### Erreur de Permissions

```bash
# Vérifier les permissions du token
# Le token doit avoir les permissions "write"
```

### Erreur de Modèle

```bash
# Tester le modèle localement
python upload_to_hf.py --test_only

# Vérifier la structure du modèle
ls -la eurobert_full/
```

### Erreur d'Upload

```bash
# Forcer la création du repo
python upload_to_hf.py --repo_name votre-nom/eurobert-commit-humor --force
```

## 📊 Fichiers Uploadés

Le script upload automatiquement :

- `config.json` - Configuration du modèle
- `model.safetensors` - Poids du modèle
- `tokenizer.json` - Tokenizer
- `tokenizer_config.json` - Configuration du tokenizer
- `special_tokens_map.json` - Tokens spéciaux
- `configuration_eurobert.py` - Configuration personnalisée
- `modeling_eurobert.py` - Modèle personnalisé
- `README.md` - Documentation générée automatiquement

## 🔄 Mise à Jour du Modèle

Pour mettre à jour un modèle existant :

```bash
# Même commande, les fichiers seront remplacés
python upload_to_hf.py --repo_name votre-nom/eurobert-commit-humor
```

## 📈 Métriques et Évaluation

Après l'upload, vous pouvez :

1. **Ajouter des métriques** dans la model card
2. **Créer des exemples** d'utilisation
3. **Documenter les performances** sur vos datasets
4. **Ajouter des citations** appropriées

## 🎪 Partage et Collaboration

- **Repository public** : Visible par tous
- **Repository privé** : Visible uniquement par vous
- **Organisations** : Partageable avec votre équipe
- **Discussions** : Activez les discussions pour feedback

## 📄 Licence

N'oubliez pas de spécifier la licence dans la model card (défaut : MIT).

## 🏆 Bonnes Pratiques

1. **Nom explicite** : Utilisez un nom clair pour votre modèle
2. **Documentation** : Ajoutez des exemples d'utilisation
3. **Versioning** : Utilisez des tags pour les versions
4. **Tests** : Testez toujours avant l'upload
5. **Métadonnées** : Remplissez les informations du modèle

---

**Bon upload ! 🚀**

Pour toute question, consultez la [documentation officielle Hugging Face](https://huggingface.co/docs/hub/repositories-getting-started).