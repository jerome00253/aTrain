#!/bin/bash

# --- Configuration ---
# Adresse de votre registre
DOCKER_REGISTRY="hub.jerome00253.ovh"
# Votre nom d'utilisateur
DOCKER_USER="jerome"
IMAGE_NAME="atrain-web"
TAG="latest"

# --- Script ---
FULL_IMAGE_NAME="$DOCKER_REGISTRY/$DOCKER_USER/$IMAGE_NAME:$TAG"

echo "🚀 Début du déploiement pour $FULL_IMAGE_NAME"

# 0. Connexion au registre (si nécessaire)
echo "🔒 Vérification de la connexion au registre..."
if ! docker system info | grep -q "$DOCKER_REGISTRY"; then
    echo "🔑 Connexion au registre $DOCKER_REGISTRY..."
    docker login "$DOCKER_REGISTRY" -u "$DOCKER_USER"
    if [ $? -ne 0 ]; then
        echo "❌ Échec de la connexion au registre. Arrêt."
        exit 1
    fi
fi

# 1. Build de l'image
echo "📦 Build de l'image Docker..."
docker build -t "$IMAGE_NAME" .

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors du build. Arrêt."
    exit 1
fi

# 2. Tag de l'image
echo "🏷️  Tagage de l'image..."
docker tag "$IMAGE_NAME" "$FULL_IMAGE_NAME"

# 3. Push vers Docker Hub
echo "☁️  Push vers Docker Hub..."
docker push "$FULL_IMAGE_NAME"

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors du push. Assurez-vous d'être connecté (docker login)."
    exit 1
fi

echo "✅ Déploiement terminé avec succès !"
echo "Vous pouvez maintenant utiliser l'image : $FULL_IMAGE_NAME"
