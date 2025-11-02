from config import config
import re
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests
import os

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Slack 앱 초기화
app = App(token=config['SLACK_BOT_TOKEN'])

# GitHub 설정
github_token = config['GITHUB_PERSONAL_ACCESS_TOKEN']
github_id = config['GITHUB_ID']
github_repo = config.get('GITHUB_REPO', 'slackbot_test')

# 설정 검증
if not github_token:
    logger.error("GITHUB_PERSONAL_ACCESS_TOKEN이 설정되지 않았습니다!")
if not github_id:
    logger.error("GITHUB_ID가 설정되지 않았습니다!")

@app.message("")
def message_deploy(message, say):
    """
    슬랙 메시지를 감지하여 배포 트리거를 처리합니다.
    멘션을 포함한 메시지도 처리할 수 있도록 개선했습니다.
    """
    try:
        # 메시지 텍스트 가져오기
        message_text = message.get('text', '')
        user_id = message.get('user', 'unknown')
        
        logger.info(f"Received message from user {user_id}: {message_text}")
        
        # 멘션 제거 (예: <@U123456> 형태)
        cleaned_text = re.sub(r'<@[A-Z0-9]+>', '', message_text).strip()
        
        # 배포 키워드 감지 (유연한 매칭)
        deploy_keywords = ['자동 배포 시작', '배포 시작', 'CRM develop deploy', 'deploy', '배포']
        is_deploy_message = any(keyword.lower() in cleaned_text.lower() for keyword in deploy_keywords)
        
        if is_deploy_message:
            logger.info(f"Deploy keyword detected in message: {cleaned_text}")
            say(f"<@{user_id}>에 의해 자동 배포 시작")    
            
            # GitHub API 엔드포인트 및 인증 정보 설정
            url = f'https://api.github.com/repos/{github_id}/{github_repo}/dispatches'
            
            # GitHub API 인증 방식: Bearer token 사용 (더 최신 방식)
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': f'Bearer {github_token}',
                'Content-Type': 'application/json',
            }

            # POST 요청 데이터 설정
            payload = {
                'event_type': 'dev_deploy',
                'client_payload': {
                    'message': cleaned_text,
                    'original_message': message_text,
                    'user': user_id,
                    'tag': f'v{github_repo}-{os.getenv("GITHUB_RUN_NUMBER", "manual")}'
                }
            }

            logger.info(f"Triggering GitHub repository_dispatch: {url}")
            logger.debug(f"Payload: {payload}")

            # POST 요청 보내기
            response = requests.post(url, headers=headers, json=payload, timeout=10)

            # 응답 확인 
            if response.status_code == 204:
                logger.info("GitHub repository_dispatch triggered successfully")
                say('✅ GitHub Actions workflow가 성공적으로 트리거되었습니다.\n배포 프로세스가 시작되었습니다.')
            else:
                logger.error(f"GitHub API request failed: {response.status_code} - {response.text}")
                error_msg = f'❌ GitHub API 요청 실패. 상태 코드: {response.status_code}'
                say(error_msg)
                
                # 에러 상세 정보
                if response.text:
                    error_detail = response.text[:300]
                    logger.error(f"Error details: {error_detail}")
                    # GitHub API 에러 메시지가 너무 길면 요약만 보여줌
                    if 'message' in response.json():
                        say(f'에러: {response.json().get("message", "Unknown error")}')
                    else:
                        say(f'에러 내용: {error_detail[:100]}...')
        else:
            logger.debug(f"Message does not contain deploy keywords: {cleaned_text}")
            
    except Exception as e:
        logger.exception(f"Error processing message: {e}")
        say(f'❌ 배포 트리거 중 오류가 발생했습니다: {str(e)}')

@app.error
def error_handler(error, body, logger):
    """
    Slack 앱 에러 핸들러
    """
    logger.error(f"Slack app error: {error}")
    logger.error(f"Error body: {body}")

if __name__ == '__main__':
    # 토큰 확인
    if not config['SLACK_BOT_TOKEN']:
        logger.error("SLACK_BOT_TOKEN이 설정되지 않았습니다. 환경 변수를 확인해주세요.")
        exit(1)
    
    if not config['SLACK_APP_TOKEN']:
        logger.error("SLACK_APP_TOKEN이 설정되지 않았습니다. 환경 변수를 확인해주세요.")
        exit(1)
    
    if not github_token:
        logger.error("GITHUB_PERSONAL_ACCESS_TOKEN이 설정되지 않았습니다. 환경 변수를 확인해주세요.")
        exit(1)
    
    logger.info("Starting Slack bot...")
    logger.info(f"GitHub repository: {github_id}/{github_repo}")
    
    try:
        SocketModeHandler(app, config['SLACK_APP_TOKEN']).start()
    except Exception as e:
        logger.exception(f"Failed to start Slack bot: {e}")
        exit(1)