# Guide de Refusion LoRA

Ce guide explique comment refusionner facilement un nouveau modèle LoRA après un nouvel entraînement.

## Contexte

Après avoir entraîné un nouveau modèle LoRA (par exemple avec des données supplémentaires ou des hyperparamètres différents), vous devez le fusionner avec le modèle de base EuroBERT pour créer un modèle complet utilisable.

## Utilisation du Script de Refusion

### Commande de base

```bash
python refusion_lora.py --lora_path chemin/vers/nouveau_modele_lora
```

### Exemples d'utilisation

#### 1. Fusion simple avec un nouveau nom
```bash
python refusion_lora.py --lora_path ../eurobert_peft_v4 --output_path eurobert_full_v2
```

#### 2. Remplacement du modèle actuel avec sauvegarde
```bash
python refusion_lora.py --lora_path ../eurobert_peft_v4 --replace_current --backup
```

#### 3. Utilisation d'un modèle de base différent
```bash
python refusion_lora.py --lora_path ../eurobert_peft_v4 --base_model "jplu/eurobert-base-cased" --output_path eurobert_custom
```

## Options disponibles

| Option | Description | Exemple |
|--------|-------------|---------|
| `--lora_path` | Chemin vers le modèle LoRA (obligatoire) | `../eurobert_peft_v4` |
| `--output_path` | Nom du modèle fusionné (défaut: eurobert_full_new) | `eurobert_full_v2` |
| `--base_model` | Modèle de base à utiliser (défaut: jplu/eurobert-base-cased) | `jplu/eurobert-base-cased` |
| `--replace_current` | Remplace le modèle actuel (eurobert_full) | Flag |
| `--backup` | Crée une sauvegarde avant remplacement | Flag |

## Workflow recommandé

### 1. Après un nouvel entraînement

```bash
# Activer l'environnement virtuel
..\dataset_env\Scripts\activate

# Fusionner le nouveau modèle LoRA
python refusion_lora.py --lora_path ../eurobert_peft_v4 --output_path eurobert_full_test

# Tester le nouveau modèle
python commit_humor_classifier.py --text "test message" --model_path eurobert_full_test
```

### 2. Si le test est satisfaisant

```bash
# Remplacer le modèle actuel avec sauvegarde
python refusion_lora.py --lora_path ../eurobert_peft_v4 --replace_current --backup

# Tester le modèle remplacé
python commit_humor_classifier.py --text "test message"
```

### 3. Test sur un jeu de données

```bash
# Évaluer les performances sur les messages de test
python commit_humor_classifier.py --batch test_commits_evaluation.txt
```

## Vérifications automatiques

Le script effectue automatiquement les vérifications suivantes :

- ✅ Existence du modèle LoRA
- ✅ Présence des fichiers requis (`adapter_config.json`, `adapter_model.safetensors`)
- ✅ Chargement des modèles et tokenizers
- ✅ Fusion et sauvegarde

## Gestion des erreurs

### Erreur : "Fichier manquant"
```
❌ Fichier manquant : adapter_config.json
```
**Solution :** Vérifiez que le chemin vers le modèle LoRA est correct et que l'entraînement s'est terminé correctement.

### Erreur : "Erreur lors de la fusion"
```
❌ Erreur lors de la fusion : ...
```
**Solution :** Vérifiez que le modèle LoRA est compatible avec le modèle de base utilisé.

## Structure des fichiers

```
commit-humor-classifier/
├── refusion_lora.py          # Script de refusion
├── eurobert_full/            # Modèle actuel
├── eurobert_full_backup/     # Sauvegarde automatique
├── eurobert_full_new/        # Nouveau modèle fusionné
└── test_commits_evaluation.txt
```

## Conseils

1. **Toujours tester** un nouveau modèle avant de remplacer l'actuel
2. **Utiliser --backup** lors du remplacement pour pouvoir revenir en arrière
3. **Garder une trace** des versions avec des noms explicites
4. **Tester sur les données d'évaluation** pour détecter l'overfitting

## Exemple complet

```bash
# Activer l'environnement
..\dataset_env\Scripts\activate

# Fusionner le nouveau modèle
python refusion_lora.py --lora_path ../eurobert_peft_v4 --output_path eurobert_full_v4

# Tester le nouveau modèle
python commit_humor_classifier.py --text "fix bug in production" --model_path eurobert_full_v4

# Si satisfaisant, remplacer l'actuel
python refusion_lora.py --lora_path ../eurobert_peft_v4 --replace_current --backup

# Évaluer les performances
python commit_humor_classifier.py --batch test_commits_evaluation.txt