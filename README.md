# aTrain (Version Web)

aTrain est un outil open-source permettant la transcription automatique d'entretiens et d'enregistrements audio de manière totalement délocalisée (garantissant la confidentialité et le respect du RGPD).

Il utilise des modèles d'apprentissage automatique de pointe sans jamais envoyer vos données sur le cloud.

## 🚀 Fonctionnalités principales

- **Transcription haute précision** : Utilise l'implémentation `faster-whisper` des modèles Whisper d'OpenAI.
- **Diarisation (Détection des locuteurs)** : Identifie automatiquement qui parle dans l'enregistrement.
- **Confidentialité Totale** : Le traitement est effectué 100% localement sur votre machine ou sur le serveur ou est installé l'application.
- **Interface Web Moderne** : Interface accessible via navigateur grâce à NiceGUI.

## 🐳 Installation via Docker (Docker Hub)

L'image officielle est hébergée sur Docker Hub pour une installation et une mise à jour facilitées.

### 1. Télécharger l'image
```bash
docker pull jerome00253/atrain-web:latest
```

### 2. Lancer avec Docker Compose (Recommandé)
Créez un fichier `docker-compose.yml` :

```yaml
services:
  atrain:
    image: jerome00253/atrain-web:latest
    container_name: atrain-web
    ports:
      - "8088:8088"
    volumes:
      - ./settings:/data/aTrain/settings           # Pour conserver vos paramètres
      - ./models_cache:/data/aTrain/models         # Pour éviter de retélécharger les modèles
      - ./transcriptions:/data/aTrain/transcriptions # Pour récupérer vos résultats
    environment:
      - XDG_DOCUMENTS_DIR=/data
    restart: unless-stopped
```

Puis lancez :
```bash
docker compose up -d
```

L'interface sera accessible sur `http://localhost:8088`.

## 👨‍💻 Auteurs
- **Armin Haberl** (armin.haberl@uni-graz.at)
- **Jürgen Fleiß** (juergen.fleiss@uni-graz.at)
- **Dominik Kowald** (dkowald@know-center.at)
- **Stefan Thalmann** (stefan.thalmann@uni-graz.at)

Développé au **Business Analytics and Data Science-Center** de l'Université de Graz.

## ⚖️ Licence
Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
