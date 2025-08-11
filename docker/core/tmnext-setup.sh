#!/bin/bash
set -e

# === CONFIG ===
REPO_URL="https://github.com/aaran-software/cloudxis.git"
REPO_DIR="cloudxis"
DOCKER_COMPOSE_FILE="docker/cloud/clients/tmnext-in.yml"
HOST_FOLDER="/home/cloud/tmnext_in"
CONTAINER_NAME="tmnext_in"
USERNAME="devops"

# === 1. Clone repo (latest commit only) ===
if [ ! -d "$REPO_DIR" ]; then
    echo "📥 Cloning latest commit from $REPO_URL..."
    git clone --depth 1 "$REPO_URL" "$REPO_DIR" || { echo "❌ Failed to clone repo"; exit 1; }
else
    echo "🔄 Repo already exists, pulling latest changes..."
    cd "$REPO_DIR"
    git fetch --depth 1 origin
    git reset --hard origin/main
    cd ..
fi

# === 2. Create target folder if missing ===
if [ ! -d "$HOST_FOLDER" ]; then
    echo "📂 Creating folder: $HOST_FOLDER"
    mkdir -p "$HOST_FOLDER"
fi

# === 3. Fix permissions on host ===
echo "🔑 Fixing host folder permissions..."
chown -R "$(id -u):$(id -g)" "$HOST_FOLDER"

# === 4. Start container ===
echo "🚀 Starting container..."
cd "$REPO_DIR"
docker compose -f "$DOCKER_COMPOSE_FILE" up -d

# === 5. Fix permissions inside container ===
echo "🔧 Fixing permissions inside container..."
docker exec -u root "$CONTAINER_NAME" chown -R "$USERNAME":"$USERNAME" /home/devops/cloud

echo "✅ Done! Container $CONTAINER_NAME is running."
