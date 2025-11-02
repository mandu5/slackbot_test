#!/bin/bash
# Slackbot 로컬 테스트 스크립트

echo "=== Slackbot 로컬 테스트 준비 ==="
echo ""

# 환경 변수 확인
if [ -z "$SLACK_BOT_TOKEN" ] || [ -z "$SLACK_APP_TOKEN" ] || [ -z "$GITHUB_PERSONAL_ACCESS_TOKEN" ]; then
    echo "❌ 필수 환경 변수가 설정되지 않았습니다."
    echo ""
    echo "다음 환경 변수를 설정해주세요:"
    echo "  export SLACK_BOT_TOKEN='xoxb-your-bot-token'"
    echo "  export SLACK_APP_TOKEN='xapp-your-app-token'"
    echo "  export GITHUB_PERSONAL_ACCESS_TOKEN='ghp_your-github-token'"
    echo "  export GITHUB_ID='mandu5'"
    echo "  export GITHUB_REPO='slackbot_test'"
    echo ""
    echo "설정 후 다시 실행:"
    echo "  cd docker_slack_file && python3 slack.py"
    exit 1
fi

echo "✅ 환경 변수 확인 완료"
echo ""
echo "Slackbot 시작 중..."
echo "종료하려면 Ctrl+C를 누르세요"
echo ""

cd docker_slack_file
python3 slack.py

