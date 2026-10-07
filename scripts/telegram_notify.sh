#!/usr/bin/env bash
set -e

STATUS="${1:-success}"
BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-8534508997:AAHQJAvD1fYrMdSQPyoq4rK-0WozMeIJYvQ}"
CHAT_ID="${TELEGRAM_CHAT_ID:-5487033876}"

if [ -z "$CHAT_ID" ]; then
    echo "WARNING: TELEGRAM_CHAT_ID is not configured. Skipping Telegram notification."
    exit 0
fi

if [ -n "$GITHUB_ACTIONS" ]; then
    CI_PLATFORM="GitHub Actions"
    PROJECT_NAME="${GITHUB_REPOSITORY:-Huybroxx/finalcloud}"
    BRANCH_NAME="${GITHUB_REF_NAME:-main}"
    COMMIT_HASH="${GITHUB_SHA:0:7}"
    COMMIT_MSG="$(git log -1 --pretty=%s 2>/dev/null || echo 'N/A')"
    AUTHOR_NAME="${GITHUB_ACTOR:-N/A}"
    PIPELINE_URL="${GITHUB_SERVER_URL:-https://github.com}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"
else
    CI_PLATFORM="GitLab CI"
    PROJECT_NAME="${CI_PROJECT_PATH:-Nhatle911/cloudfinal}"
    BRANCH_NAME="${CI_COMMIT_REF_NAME:-main}"
    COMMIT_HASH="${CI_COMMIT_SHORT_SHA:-HEAD}"
    COMMIT_MSG="${CI_COMMIT_TITLE:-N/A}"
    AUTHOR_NAME="${GITLAB_USER_NAME:-${CI_COMMIT_AUTHOR:-N/A}}"
    PIPELINE_URL="${CI_PIPELINE_URL:-#}"
fi

if [ "$STATUS" = "success" ]; then
    ICON="✅"
    TITLE="<b>${CI_PLATFORM}: Pipeline Succeeded!</b>"
else
    ICON="❌"
    TITLE="<b>${CI_PLATFORM}: Pipeline Failed!</b>"
fi

TEXT="$ICON $TITLE

📦 <b>Project:</b> ${PROJECT_NAME}
🌿 <b>Branch:</b> <code>${BRANCH_NAME}</code>
📝 <b>Commit:</b> <code>${COMMIT_HASH}</code> - ${COMMIT_MSG}
👤 <b>Author:</b> ${AUTHOR_NAME}
🔗 <a href=\"${PIPELINE_URL}\">View Pipeline Details</a>"

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d chat_id="${CHAT_ID}" \
    -d parse_mode="HTML" \
    -d disable_web_page_preview="true" \
    -d text="${TEXT}" > /dev/null

echo "Telegram notification sent successfully (${STATUS})."