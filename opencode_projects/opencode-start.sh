#!/bin/bash
if [ -z "$1" ]; then
  echo "⚠️ Usage: ./opencode-start.sh <project_name>"
  exit 1
fi

PROJECT_NAME=$1
# הנתיב החדש בתוך ה-devlog!
PROJECT_DIR="/home/razik/Documents/learning_projects/devlog/opencode_projects/$PROJECT_NAME"
SANDBOX_DIR="/home/razik/Documents/learning_projects/devlog/opencode_projects/_sandbox"

echo "🚀 Starting OpenCode project: $PROJECT_NAME"

if [ -d "$PROJECT_DIR" ]; then
  echo "✅ Project directory exists: $PROJECT_NAME"
else
  echo "📁 Creating new project directory..."
  mkdir -p "$PROJECT_DIR"
  echo "📄 Creating basic .gitignore..."
  cat << 'EOF' > "$PROJECT_DIR/.gitignore"
__pycache__/
.env
.venv/
*.log
EOF
fi

# יצירת התיקיות בסנדבוקס אם לא קיימות
mkdir -p "$SANDBOX_DIR/opencode_config"
mkdir -p "$SANDBOX_DIR/jupyter"
mkdir -p "$SANDBOX_DIR/vscode"

echo "🐳 Launching isolated Docker environment..."

docker run -it --rm \
  --name "sandbox-opencode-env-${PROJECT_NAME}" \
  --gpus all \
  --network host \
  --env HOST_UID=$(id -u) \
  --env HOST_GID=$(id -g) \
  -v "$PROJECT_DIR:/workspace" \
  -v "$SANDBOX_DIR/opencode_config:/home/opencode/.opencode" \
  -w /workspace \
  opencode-env:latest \
  bash

