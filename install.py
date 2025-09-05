#!/usr/bin/env python3
"""
🔧 Script d'Installation Automatique - Classificateur d'Humour pour Commits
=======================================================================

Ce script détecte automatiquement votre configuration hardware et installe
les dépendances appropriées pour le classificateur d'humour.

Usage:
    python install.py
    python install.py --force-cpu  # Force l'installation CPU même si GPU détecté
    python install.py --gpu-only   # Force l'installation GPU (échoue si pas de GPU)

Auteur: Assistant IA
Version: 1.0
"""

import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path

def print_header():
    """Affiche l'en-tête du script"""
    print("\n" + "="*70)
    print("🤖 INSTALLATION - CLASSIFICATEUR D'HUMOUR POUR COMMITS")
    print("="*70)
    print("🔍 Détection automatique du hardware...\n")

def detect_gpu():
    """Détecte la présence d'un GPU NVIDIA compatible CUDA"""
    try:
        # Vérifier si nvidia-smi est disponible
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ GPU NVIDIA détecté")
            print(f"   📊 Informations GPU:")
            # Extraire les infos basiques du GPU
            lines = result.stdout.split('\n')
            for line in lines:
                if 'NVIDIA' in line and 'Driver Version' in line:
                    print(f"   {line.strip()}")
                    break
            return True
        else:
            print("❌ Aucun GPU NVIDIA détecté")
            return False
    except FileNotFoundError:
        print("❌ nvidia-smi non trouvé - Aucun GPU NVIDIA détecté")
        return False
    except Exception as e:
        print(f"⚠️  Erreur lors de la détection GPU: {e}")
        return False

def detect_system_info():
    """Détecte les informations système"""
    print(f"💻 Système: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"🏗️  Architecture: {platform.machine()}")
    
    # Vérifier la version de Python
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ requis")
        return False
    else:
        print("✅ Version Python compatible")
    
    return True

def install_package(package, description=""):
    """Installe un package avec pip"""
    try:
        print(f"📦 Installation de {package}...")
        if description:
            print(f"   📝 {description}")
        
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ {package} installé avec succès")
            return True
        else:
            print(f"❌ Erreur lors de l'installation de {package}")
            print(f"   Détails: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'installation de {package}: {e}")
        return False

def check_package_installed(package):
    """Vérifie si un package est déjà installé"""
    try:
        __import__(package.replace("-", "_"))
        return True
    except ImportError:
        return False

def install_base_dependencies(force_cpu=True):
    """Installe les dépendances de base"""
    print("\n🔧 Installation des dépendances de base...")

    base_packages = [
        ("transformers", "Bibliothèque Hugging Face Transformers"),
        ("huggingface_hub", "Client Hugging Face Hub"),
        ("datasets", "Gestion des datasets"),
        ("safetensors", "Format de sauvegarde sécurisé"),
        ("numpy", "Calculs numériques"),
        ("requests", "Requêtes HTTP")
    ]

    # N'installer accelerate que si force_cpu n'est pas activé
    if not force_cpu:
        base_packages.insert(3, ("accelerate", "Accélération des modèles"))

    success = True
    for package, description in base_packages:
        if check_package_installed(package):
            print(f"✅ {package} déjà installé")
        else:
            if not install_package(package, description):
                success = False

    return success

def install_pytorch_gpu():
    """Installe PyTorch avec support GPU"""
    print("\n🚀 Installation de PyTorch avec support GPU...")
    
    # PyTorch avec CUDA (version stable)
    pytorch_gpu_cmd = "torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121"
    
    try:
        print("📦 Installation de PyTorch GPU (CUDA 12.1)...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install"] + pytorch_gpu_cmd.split(),
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ PyTorch GPU installé avec succès")
            return True
        else:
            print("❌ Erreur lors de l'installation de PyTorch GPU")
            print("🔄 Tentative d'installation CPU...")
            return install_pytorch_cpu()
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("🔄 Tentative d'installation CPU...")
        return install_pytorch_cpu()

def install_pytorch_cpu():
    """Installe PyTorch version CPU uniquement"""
    print("\n💻 Installation de PyTorch version CPU...")
    
    pytorch_cpu_cmd = "torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu"
    
    try:
        print("📦 Installation de PyTorch CPU...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install"] + pytorch_cpu_cmd.split(),
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ PyTorch CPU installé avec succès")
            return True
        else:
            print("❌ Erreur lors de l'installation de PyTorch CPU")
            print(f"   Détails: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_installation():
    """Teste l'installation en important les modules principaux"""
    print("\n🧪 Test de l'installation...")
    
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__} importé")
        
        # Test GPU si disponible
        if torch.cuda.is_available():
            print(f"✅ CUDA disponible - {torch.cuda.device_count()} GPU(s) détecté(s)")
            print(f"   📊 GPU actuel: {torch.cuda.get_device_name(0)}")
        else:
            print("💻 Mode CPU (pas de GPU CUDA disponible)")
        
        import transformers
        print(f"✅ Transformers {transformers.__version__} importé")
        
        from huggingface_hub import __version__ as hf_version
        print(f"✅ Hugging Face Hub {hf_version} importé")
        
        print("\n🎉 Installation réussie !")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False



def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Installation automatique du classificateur d'humour")
    parser.add_argument("--force-cpu", action="store_true", help="Force l'installation CPU")
    parser.add_argument("--gpu-only", action="store_true", help="Force l'installation GPU")
    parser.add_argument("--skip-test", action="store_true", help="Ignore les tests d'installation")
    
    args = parser.parse_args()
    
    print_header()
    
    # Détection du système
    if not detect_system_info():
        print("❌ Système non compatible")
        sys.exit(1)
    
    print()
    
    # Détection GPU
    has_gpu = detect_gpu() and not args.force_cpu
    
    if args.gpu_only and not has_gpu:
        print("❌ --gpu-only spécifié mais aucun GPU détecté")
        sys.exit(1)
    
    print()
    
    # Installation des dépendances de base
    if not install_base_dependencies(args.force_cpu):
        print("❌ Échec de l'installation des dépendances de base")
        sys.exit(1)
    
    # Installation de PyTorch
    if has_gpu or args.gpu_only:
        pytorch_success = install_pytorch_gpu()
    else:
        pytorch_success = install_pytorch_cpu()
    
    if not pytorch_success:
        print("❌ Échec de l'installation de PyTorch")
        sys.exit(1)
    
    # Test de l'installation
    if not args.skip_test:
        if not test_installation():
            print("❌ Les tests d'installation ont échoué")
            sys.exit(1)
    
    print("\n" + "="*70)
    print("🎉 INSTALLATION TERMINÉE AVEC SUCCÈS !")
    print("="*70)
    print("\n📖 Étapes suivantes:")
    print("   1. Configurez la variable d'environnement COMMITS_JSON:")
    print("      Windows: set COMMITS_JSON=chemin/vers/votre/fichier.json")
    print("      Linux/Mac: export COMMITS_JSON=chemin/vers/votre/fichier.json")
    print("   2. Installez Flask: pip install flask")
    print("   3. Lancez l'interface web: python web_app.py")
    print("   4. Ouvrez http://localhost:5000 dans votre navigateur")
    print("\n💡 Le modèle sera téléchargé automatiquement au premier usage (~420MB)")
    print("\n📚 Consultez README.md pour plus d'informations")

if __name__ == "__main__":
    main()