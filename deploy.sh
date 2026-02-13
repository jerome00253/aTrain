#!/bin/bash

# --- Configuration ---
# Adresse de votre registre (laisser vide pour Docker Hub officiel)
DOCKER_REGISTRY=""
# Votre nom d'utilisateur Docker Hub
DOCKER_USER="jerome00253"
IMAGE_NAME="atrain-web"
TAG="latest"

# --- Script ---
if [ -z "$DOCKER_REGISTRY" ]; then
    FULL_IMAGE_NAME="$DOCKER_USER/$IMAGE_NAME:$TAG"
else
    FULL_IMAGE_NAME="$DOCKER_REGISTRY/$DOCKER_USER/$IMAGE_NAME:$TAG"
fi

echo "🚀 Début du déploiement pour $FULL_IMAGE_NAME"

# 0. Connexion au registre (si nécessaire)
if [ -n "$DOCKER_REGISTRY" ]; then
    echo "🔒 Vérification de la connexion au registre $DOCKER_REGISTRY..."
    if ! docker system info | grep -q "$DOCKER_REGISTRY"; then
        echo "🔑 Connexion au registre $DOCKER_REGISTRY..."
        docker login "$DOCKER_REGISTRY" -u "$DOCKER_USER"
    fi
else
    echo "🔒 Vérification de la connexion à Docker Hub..."
    # Pour Docker Hub, on vérifie simplement si on est loggé
    if ! docker system info | grep -q "Username: $DOCKER_USER"; then
        echo "🔑 Merci de vous connecter à votre compte Docker Hub ($DOCKER_USER) :"
        docker login -u "$DOCKER_USER"
    fi
fi

if [ $? -ne 0 ]; then
    echo "❌ Échec de la connexion. Arrêt."
    exit 1
fi

# 1. Build de l'image
echo "📦 Build de l'image Docker..."
docker build --build-arg BUILD_ID=$(date +%s) -t "$IMAGE_NAME" .

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
