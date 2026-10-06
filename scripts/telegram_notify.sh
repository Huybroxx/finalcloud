#!/usr/bin/env bash
set -e

STATUS="${1:-success}"
BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-8534508997:AAHQJAvD1fYrMdSQPyoq4rK-0WozMeIJYvQ}"
CHAT_ID="${TELEGRAM_CHAT_ID:-5487033876}"

if [ -z "$CHAT_ID" ]; then
    echo "WARNING: TELEGRAM_CHAT_ID is not configured. Skipping Telegram notification."
    exit 0
fi

if [ "$STATUS" = "success" ]; then
    ICON="✅"
    TITLE="<b>GitLab CI/CD: Pipeline Succeeded!</b>"
else
    ICON="❌"
    TITLE="<b>GitLab CI/CD: Pipeline Failed!</b>"
fi

TEXT="$ICON $TITLE

📦 <b>Project:</b> ${CI_PROJECT_PATH:-Nhatle911/cloudfinal}
🌿 <b>Branch:</b> <code>${CI_COMMIT_REF_NAME:-main}</code>
📝 <b>Commit:</b> <code>${CI_COMMIT_SHORT_SHA:-HEAD}</code> - ${CI_COMMIT_TITLE:-N/A}
👤 <b>Author:</b> ${GITLAB_USER_NAME:-${CI_COMMIT_AUTHOR:-N/A}}
🔗 <a href=\"${CI_PIPELINE_URL:-#}\">View Pipeline on GitLab</a>"

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d chat_id="${CHAT_ID}" \
    -d parse_mode="HTML" \
    -d disable_web_page_preview="true" \
    -d text="${TEXT}" > /dev/null

echo "Telegram notification sent successfully (${STATUS})."