# Lambda ChatOps Bot

AWS Lambda를 사용한 Slack Events API 기반 ChatOps 봇입니다.

## 🎯 해커톤 요구사항 부합

- ✅ **"ChatOps Engineer (Bot): AWS Lambda + API Gateway"** 완벽 구현
- ✅ 서버리스 (서버 없이 작동)
- ✅ AWS Free Tier로 무료
- ✅ 항상 실행 중 (가용성 높음)

## 📁 파일 구조

```
lambda/
  ├── slack_events.py      # Lambda 핸들러 (메인 함수)
  ├── requirements.txt     # Python 의존성
  └── README.md            # 이 파일
```

## 🚀 배포 방법

### 1. Lambda 함수 생성

```bash
# ZIP 파일 생성
cd lambda
pip install -r requirements.txt -t .
zip -r lambda_function.zip .

# AWS CLI로 배포 (또는 AWS Console 사용)
aws lambda create-function \
  --function-name slackbot-chatops \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
  --handler slack_events.lambda_handler \
  --zip-file fileb://lambda_function.zip \
  --timeout 30 \
  --environment Variables="{
    SLACK_SIGNING_SECRET=your-signing-secret,
    GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your-token,
    GITHUB_ID=mandu5,
    GITHUB_REPO=slackbot_test
  }"
```

### 2. API Gateway 설정

```bash
# API Gateway REST API 생성 (또는 AWS Console에서)
# 엔드포인트: POST /slack/events
# Lambda 함수와 연동
```

### 3. Slack 앱 설정

1. **Socket Mode 비활성화**
   - Slack API Dashboard → Socket Mode → 비활성화

2. **Event Subscriptions 활성화**
   - Event Subscriptions → Enable Events
   - Request URL: `https://your-api-gateway-url/slack/events`
   - Subscribe to bot events:
     - `message.channels`
     - `message.groups`

3. **OAuth & Permissions**
   - Bot Token Scopes (기존과 동일):
     - `chat:write`
     - `channels:history`
     - `groups:history`

## 🔧 환경 변수

Lambda 함수에 다음 환경 변수를 설정해야 합니다:

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `SLACK_SIGNING_SECRET` | Slack 앱 Signing Secret | `slack-dashboard`에서 복사 |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | GitHub Personal Access Token | `ghp_...` |
| `GITHUB_ID` | GitHub 사용자명 | `mandu5` |
| `GITHUB_REPO` | GitHub 레포지토리 | `slackbot_test` |

## 🧪 테스트

### 로컬 테스트

```python
# test_lambda.py
import json
from slack_events import lambda_handler

event = {
    'headers': {
        'x-slack-signature': 'v0=...',
        'x-slack-request-timestamp': str(int(time.time()))
    },
    'body': json.dumps({
        'type': 'event_callback',
        'event': {
            'type': 'message',
            'text': '자동 배포 시작',
            'user': 'U123456',
            'bot_id': None
        }
    })
}

result = lambda_handler(event, None)
print(result)
```

### Lambda 테스트 (AWS Console)

1. AWS Lambda Console → 함수 선택
2. "Test" 탭 → 새 테스트 이벤트 생성
3. 다음 JSON 사용:

```json
{
  "headers": {
    "x-slack-signature": "v0=test",
    "x-slack-request-timestamp": "1234567890"
  },
  "body": "{\"type\":\"event_callback\",\"event\":{\"type\":\"message\",\"text\":\"자동 배포 시작\",\"user\":\"U123456\"}}"
}
```

## 📊 작동 흐름

```
1. Slack 사용자가 "자동 배포 시작" 메시지 전송
   ↓
2. Slack Events API → API Gateway
   ↓
3. API Gateway → Lambda 함수
   ↓
4. Lambda 함수 검증 및 처리
   ↓
5. GitHub API repository_dispatch 호출
   ↓
6. GitHub Actions 워크플로우 트리거
   ↓
7. 배포 프로세스 시작
```

## 🔍 디버깅

### CloudWatch Logs 확인

```bash
aws logs tail /aws/lambda/slackbot-chatops --follow
```

### Lambda 함수 로그

AWS Console → Lambda → 함수 → Monitor → CloudWatch Logs

## ✅ Socket Mode 대비 장점

| 항목 | Socket Mode | Lambda (HTTP Events) |
|------|-------------|----------------------|
| 서버 필요 | ✅ 필요 | ❌ 불필요 |
| 비용 | 서버 비용 | AWS Free Tier 무료 |
| 가용성 | 서버 가동 필요 | 항상 실행 중 |
| 해커톤 요구사항 | ❌ 부합 안 됨 | ✅ 완벽 부합 |
| 버튼 인터랙션 | ✅ 가능 | ✅ 가능 |

## 🎯 다음 단계

1. ✅ Lambda 함수 배포 완료
2. ✅ API Gateway 설정 완료
3. ✅ Slack 앱 Event Subscriptions 설정 완료
4. ⬜ 테스트: Slack 메시지 → Lambda → GitHub Actions
5. ⬜ Slack 버튼 인터랙션 추가 (승인 버튼)

