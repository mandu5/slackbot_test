from config import config
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests

app = App(token=config['SLACK_BOT_TOKEN'])
github_token = config['GITHUB_PERSONAL_ACCESS_TOKEN']  # GitHub 개인 액세스 토큰 가져오기
github_id = config['GITHUB_ID']

@app.message("CRM develop deploy")
def message_deploy(message, say):
    
    if message['text'] == 'CRM develop deploy':
        say(f"<@{message['user']}>에 의해 CRM 개발서버 배포 시작")    
        # GitHub API 엔드포인트 및 인증 정보 설정
        url = f'https://api.github.com/repos/{github_id}/test/dispatches'
        headers = {
            'Accept': 'application/vnd.github.v3+json',
        }
        auth = (github_id, github_token)  # GitHub 사용자 이름과 개인 액세스 토큰

        # POST 요청 데이터 설정
        payload = {
            'event_type': 'dev_deploy',
            'client_payload': {
                'message': message['text'],
                'tag': 'v1.0'  # 테깅 정보를 추가
            }
        }

        # POST 요청 보내기
        response = requests.post(url, headers=headers, auth=auth, json=payload)

        # 응답 확인 
        if response.status_code == 204:
            say('GitHub Actions workflow가 성공적으로 트리거되었습니다.')
        else:
            say(f'GitHub API 요청 실패. 상태 코드: {response.status_code}')
            say(response.text)
    else :
      say("잘못된 메시지 입니다.")

if __name__ == '__main__':
    SocketModeHandler(app, config['SLACK_APP_TOKEN']).start()