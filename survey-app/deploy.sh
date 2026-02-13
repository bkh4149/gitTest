#!/bin/bash
# さくらサーバーへのデプロイスクリプト
#
# 初回セットアップ:
#   1. サーバーにリポジトリをクローン
#   2. python3 -m venv venv && source venv/bin/activate
#   3. pip install -r survey-app/requirements.txt
#   4. このスクリプト内のパスを環境に合わせて修正
#   5. systemd サービスファイルを配置: sudo cp survey-app.service /etc/systemd/system/
#   6. sudo systemctl enable survey-app && sudo systemctl start survey-app

set -euo pipefail

APP_DIR="/var/www/survey-app"
VENV_DIR="${APP_DIR}/venv"

echo "==> Pulling latest code..."
cd "${APP_DIR}"
git pull origin master

echo "==> Installing dependencies..."
source "${VENV_DIR}/bin/activate"
pip install -r survey-app/requirements.txt

echo "==> Restarting application..."
sudo systemctl restart survey-app

echo "==> Deploy complete!"
