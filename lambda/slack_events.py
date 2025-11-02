"""
AWS Lambda function for Slack Events API
해커톤 요구사항: "ChatOps Engineer (Bot): AWS Lambda + API Gateway"
"""
import json
import os
import hmac
import hashlib
import time
import logging
import requests
from typing import Dict, Any

# 로깅 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 환경 변수
SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET')
GITHUB_TOKEN = os.environ.get('GITHUB_PERSONAL_ACCESS_TOKEN')
GITHUB_ID = os.environ.get('GITHUB_ID', 'mandu5')
GITHUB_REPO = os.environ.get('GITHUB_REPO', 'slackbot_test')


def get_header_value(headers: Dict[str, Any], key: str) -> str:
    """
    API Gateway는 헤더 이름을 소문자로 변환하거나 그대로 유지할 수 있음
    대소문자 무시하고 헤더 값 가져오기
    """
    # 직접 매칭 시도
    if key in headers:
        return headers[key]
    
    # 소문자로 시도
    key_lower = key.lower()
    for header_key, header_value in headers.items():
        if header_key.lower() == key_lower:
            return header_value
    
    return ''


def verify_slack_request(event: Dict[str, Any], body_str: str) -> bool:
    """
    Slack 요청 검증 (보안)
    Slack Events API는 요청이 Slack에서 온 것인지 검증해야 함
    """
    if not SLACK_SIGNING_SECRET:
        logger.warning("SLACK_SIGNING_SECRET not set, skipping verification")
        return True
    
    try:
        headers = event.get('headers', {})
        
        # 헤더에서 서명 및 타임스탬프 추출 (대소문자 무시)
        slack_signature = get_header_value(headers, 'x-slack-signature')
        slack_timestamp = get_header_value(headers, 'x-slack-request-timestamp')
        
        if not slack_signature or not slack_timestamp:
            logger.warning("Missing Slack signature or timestamp")
            return False
        
        # 타임스탬프 검증 (5분 이내)
        try:
            if abs(time.time() - int(slack_timestamp)) > 60 * 5:
                logger.warning("Request timestamp too old")
                return False
        except ValueError:
            logger.warning(f"Invalid timestamp: {slack_timestamp}")
            return False
        
        # 서명 생성
        sig_basestring = f"v0:{slack_timestamp}:{body_str}"
        my_signature = 'v0=' + hmac.new(
            SLACK_SIGNING_SECRET.encode('utf-8'),
            sig_basestring.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # 비교
        return hmac.compare_digest(my_signature, slack_signature)
    except Exception as e:
        logger.error(f"Verification error: {e}")
        return False


def trigger_github_deployment(message_text: str, user_id: str, original_message: str) -> Dict[str, Any]:
    """
    GitHub repository_dispatch 이벤트 트리거
    ChatOps: Slack 메시지 → GitHub Actions 워크플로우 실행
    """
    # 배포 키워드 감지
    deploy_keywords = ['자동 배포 시작', '배포 시작', 'deploy', '배포']
    cleaned_text = message_text.lower().strip()
    is_deploy_message = any(keyword.lower() in cleaned_text for keyword in deploy_keywords)
    
    if not is_deploy_message:
        logger.info(f"Message does not contain deploy keywords: {cleaned_text}")
        return {
            'statusCode': 200,
            'body': json.dumps({'ok': True, 'message': 'No deployment triggered'})
        }
    
    # GitHub API 호출
    url = f'https://api.github.com/repos/{GITHUB_ID}/{GITHUB_REPO}/dispatches'
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'Bearer {GITHUB_TOKEN}',
        'Content-Type': 'application/json',
    }
    
    payload = {
        'event_type': 'dev_deploy',
        'client_payload': {
            'message': cleaned_text,
            'original_message': original_message,
            'user': user_id,
            'tag': f'v{os.environ.get("GITHUB_RUN_NUMBER", "lambda")}'
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 204:
            logger.info(f"GitHub repository_dispatch triggered successfully by user {user_id}")
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'ok': True,
                    'message': f'GitHub Actions workflow triggered by user {user_id}'
                })
            }
        else:
            logger.error(f"GitHub API error: {response.status_code} - {response.text}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'ok': False,
                    'error': f'GitHub API error: {response.status_code}'
                })
            }
    except Exception as e:
        logger.exception(f"Error calling GitHub API: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'ok': False,
                'error': str(e)
            })
        }


def handle_message_event(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Slack 메시지 이벤트 처리
    """
    event = event_data.get('event', {})
    event_type = event.get('type')
    
    if event_type != 'message':
        logger.info(f"Ignoring event type: {event_type}")
        return {
            'statusCode': 200,
            'body': json.dumps({'ok': True})
        }
    
    # 봇 메시지는 무시
    if event.get('bot_id'):
        logger.info("Ignoring bot message")
        return {
            'statusCode': 200,
            'body': json.dumps({'ok': True})
        }
    
    message_text = event.get('text', '')
    user_id = event.get('user', 'unknown')
    
    logger.info(f"Processing message from user {user_id}: {message_text}")
    
    # GitHub deployment 트리거
    result = trigger_github_deployment(message_text, user_id, message_text)
    
    # Slack에 응답 (선택적 - Events API는 즉시 200 응답 필요)
    return result


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda 핸들러
    Slack Events API 요청을 처리
    """
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        # Body 가져오기 (문자열 형태로 보관 - 검증에 필요)
        body_str = event.get('body', '{}')
        
        # Body 파싱
        body = {}
        if isinstance(body_str, str):
            try:
                body = json.loads(body_str)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON body: {body_str}")
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Invalid JSON'})
                }
        
        # URL 검증 (Event Subscriptions 설정 시) - 검증 전에 먼저 처리
        # URL 검증 요청은 검증을 스킵하고 challenge를 바로 반환해야 함
        if body.get('type') == 'url_verification':
            challenge = body.get('challenge')
            if challenge:
                logger.info(f"URL verification challenge received: {challenge}")
                return {
                    'statusCode': 200,
                    'body': challenge  # challenge 값 그대로 반환 (문자열)
                }
            else:
                logger.error("URL verification challenge missing")
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Challenge missing'})
                }
        
        # 일반 이벤트는 서명 검증 필요
        if not verify_slack_request(event, body_str):
            logger.warning("Request verification failed")
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Forbidden'})
            }
        
        # 이벤트 처리
        if body.get('type') == 'event_callback':
            return handle_message_event(body)
        
        # 기타 이벤트는 200 응답 (Slack 요구사항)
        logger.info(f"Unhandled event type: {body.get('type')}")
        return {
            'statusCode': 200,
            'body': json.dumps({'ok': True})
        }
        
    except Exception as e:
        logger.exception(f"Error processing event: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }

