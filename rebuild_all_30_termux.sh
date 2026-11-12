#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

APP_ROOT="${1:-${SERVO_APP_ROOT:-../SERVO-DEUTSCH-B2-7.2.0}}"

if ! command -v pkg >/dev/null 2>&1; then
  echo "Ce script doit être exécuté dans Termux."
  exit 1
fi

if ! command -v python >/dev/null 2>&1; then
  pkg install -y python
fi

if ! command -v ffmpeg >/dev/null 2>&1 || ! command -v ffprobe >/dev/null 2>&1; then
  pkg install -y ffmpeg
fi

if [ ! -d "$APP_ROOT/app/src/main/java/com/servo/deutschb2" ]; then
  echo "Dépôt de l'application introuvable : $APP_ROOT"
  echo "Indique le bon chemin : bash rebuild_all_30_termux.sh /chemin/SERVO-DEUTSCH-B2-7.2.0"
  exit 1
fi

python -m pip install --upgrade edge-tts
python rebuild_all_30_from_app.py --app-root "$APP_ROOT" --all

echo
echo "Terminé : 30 archives ZIP et leurs manifestes sont dans ./output/"
echo "Contrôle le fichier ./output/audio-build-report.json avant publication."
