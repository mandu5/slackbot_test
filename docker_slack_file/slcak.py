from config import config
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests

app = App(token=config['SLACK_BOT_TOKEN'])
github_token = config['GITHUB_PERSONAL_ACCESS_TOKEN']  # GitHub 개인 액세스 토큰 가져오기
github_id = config['GITHUB_ID']
github_repo = config.get('GITHUB_REPO', 'slackbot_test')  # Repository 이름 (기본값: slackbot_test)

@app.message("")
def message_deploy(message, say):
    """
    슬랙 메시지를 감지하여 배포 트리거를 처리합니다.
    멘션을 포함한 메시지도 처리할 수 있도록 개선했습니다.
    """
    # 메시지 텍스트 가져오기
    message_text = message.get('text', '')
    
    # 멘션 제거 (예: <@U123456> 형태)
    # 멘션 패턴 제거
    cleaned_text = re.sub(r'<@[A-Z0-9]+>', '', message_text).strip()
    
    # 배포 키워드 감지 (유연한 매칭)
    deploy_keywords = ['자동 배포 시작', '배포 시작', 'CRM develop deploy', 'deploy']
    is_deploy_message = any(keyword in cleaned_text for keyword in deploy_keywords)
    
    if is_deploy_message:
        say(f"<@{message['user']}>에 의해 자동 배포 시작")    
        
        # GitHub API 엔드포인트 및 인증 정보 설정
        url = f'https://api.github.com/repos/{github_id}/{github_repo}/dispatches'
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'token {github_token}',
        }

        # POST 요청 데이터 설정
        payload = {
            'event_type': 'dev_deploy',
            'client_payload': {
                'message': cleaned_text,
                'original_message': message_text,
                'user': message['user'],
                'tag': 'v1.0'  # 테깅 정보를 추가
            }
        }

        # POST 요청 보내기 (Authorization header 사용)
        response = requests.post(url, headers=headers, json=payload)

        # 응답 확인 
        if response.status_code == 204:
            say('✅ GitHub Actions workflow가 성공적으로 트리거되었습니다.')
        else:
            error_msg = f'❌ GitHub API 요청 실패. 상태 코드: {response.status_code}'
            say(error_msg)
            if response.text:
                say(f'에러 내용: {response.text[:200]}')  # 에러 메시지 일부만 표시

if __name__ == '__main__':
    # 토큰 확인
    if not config['SLACK_BOT_TOKEN'] or not config['SLACK_APP_TOKEN']:
        print("⚠️  경고: SLACK_BOT_TOKEN 또는 SLACK_APP_TOKEN이 설정되지 않았습니다.")
        print("환경 변수를 확인해주세요.")
    
    SocketModeHandler(app, config['SLACK_APP_TOKEN']).start()