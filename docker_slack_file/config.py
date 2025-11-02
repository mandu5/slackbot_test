import os

config = {
    'SLACK_BOT_TOKEN': os.getenv('SLACK_BOT_TOKEN', ''),  # 봇 토큰 (환경 변수에서 읽음)
    'SLACK_APP_TOKEN': os.getenv('SLACK_APP_TOKEN', ''),  # 앱 토큰 (App-Level Tokens, 환경 변수에서 읽음)
    'GITHUB_PERSONAL_ACCESS_TOKEN': os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN', ''),  # 깃헙 access token (환경 변수에서 읽음)
    'GITHUB_ID': os.getenv('GITHUB_ID', 'mandu5')  # 깃헙 계정 (환경 변수 또는 기본값)
}