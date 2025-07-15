# 🚀 Upload sur Hugging Face - Guide Rapide

## 📋 Résumé des Étapes

1. **Préparer l'environnement**
2. **Tester le modèle**
3. **Se connecter à Hugging Face**
4. **Uploader le modèle**

## 🎯 Méthode Rapide (Recommandée)

```bash
# 1. Tester le modèle
python test_model_before_upload.py

# 2. Upload interactif
python quick_upload_hf.py
```

## 🔧 Méthode Manuelle

```bash
# 1. Installer les dépendances
python install_hf_dependencies.py

# 2. Se connecter à Hugging Face
huggingface-cli login

# 3. Uploader
python upload_to_hf.py --repo_name votre-nom/eurobert-commit-humor
```

## 📁 Scripts Disponibles

| Script | Description | Usage |
|--------|-------------|--------|
| `quick_upload_hf.py` | **Démarrage rapide** | Processus guidé étape par étape |
| `upload_to_hf.py` | Upload principal | Script complet avec options |
| `test_model_before_upload.py` | Tests pré-upload | Vérification avant upload |
| `install_hf_dependencies.py` | Installation | Dépendances HuggingFace |

## 🔗 Liens Utiles

- [Guide détaillé](HUGGINGFACE_GUIDE.md)
- [Hugging Face Hub](https://huggingface.co)
- [Créer un token](https://huggingface.co/settings/tokens)

## ⚡ Commandes Essentielles

```bash
# Test rapide
python test_model_before_upload.py

# Upload facile
python quick_upload_hf.py

# Upload avancé
python upload_to_hf.py --repo_name mon-nom/eurobert-commit-humor --private
```

## 🛠️ Dépannage

### Erreur "Modèle introuvable"
```bash
ls -la eurobert_full/
```

### Erreur "Non connecté à HuggingFace"
```bash
huggingface-cli login
```

### Erreur "Permissions insuffisantes"
Vérifiez que votre token a les permissions "write"

## 📖 Documentation

- **Guide complet** : [HUGGINGFACE_GUIDE.md](HUGGINGFACE_GUIDE.md)
- **Aide générale** : [README.md](README.md)
- **Refusion LoRA** : [REFUSION_GUIDE.md](REFUSION_GUIDE.md)

---

**Bon upload ! 🎉**