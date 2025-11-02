# 🔧 URL 검증 문제 해결 가이드

## 문제 상황

Slack Event Subscriptions에서 다음 오류 발생:
```
Your URL didn't respond with the value of the challenge parameter.
```

## 원인

Lambda 함수가 URL 검증 요청을 제대로 처리하지 못함:
1. URL 검증 요청을 서명 검증 전에 처리해야 함
2. API Gateway 헤더가 대소문자 변환 가능
3. Challenge 값을 문자열로 정확히 반환해야 함

## 해결 방법

### Step 1: 수정된 Lambda 함수 재배포

```bash
cd lambda

# ZIP 파일 재생성
./deploy.sh

# 또는 수동으로:
pip install -r requirements.txt -t .
zip -r lambda_function.zip . -x "*.pyc" -x "__pycache__/*" -x "*.md" -x "deploy.sh"
```

### Step 2: AWS Lambda Console에서 업데이트

1. **Lambda Console 접속**
   - https://console.aws.amazon.com/lambda/
   - `slackbot-chatops` 함수 선택

2. **코드 업로드**
   - Code 탭 → "Upload from" → ".zip file"
   - 새로 생성한 `lambda_function.zip` 업로드
   - "Save" 클릭

3. **배포 확인**
   - Functions 코드가 업데이트되었는지 확인

### Step 3: Lambda 함수 테스트

1. **Lambda Console → Test 탭**
2. **새 테스트 이벤트 생성**
   - Event name: `test-url-verification`
   - Event JSON:
   ```json
   {
     "headers": {},
     "body": "{\"type\":\"url_verification\",\"challenge\":\"test123456\"}"
   }
   ```
3. **"Test" 클릭**
4. **결과 확인**
   - ✅ Response: `{"statusCode": 200, "body": "test123456"}`
   - ✅ Execution result: succeeded

### Step 4: Slack Event Subscriptions 재시도

1. **Slack API Dashboard 접속**
   - https://api.slack.com/apps
   - 앱 선택

2. **Event Subscriptions**
   - Event Subscriptions 메뉴 클릭
   - Request URL에 API Gateway URL 입력:
     ```
     https://xxxxx.execute-api.region.amazonaws.com/prod/slack/events
     ```
   - "Save Changes" 클릭
   - ✅ **"URL verified"** 확인 (자동으로 검증됨)

---

## 수정된 내용

### 주요 변경사항

1. **URL 검증을 먼저 처리**
   ```python
   # Body를 먼저 파싱
   body = json.loads(body_str)
   
   # URL 검증 요청은 검증 전에 처리
   if body.get('type') == 'url_verification':
       challenge = body.get('challenge')
       return {
           'statusCode': 200,
           'body': challenge  # challenge 값 그대로 반환
       }
   ```

2. **헤더 대소문자 처리**
   ```python
   def get_header_value(headers: Dict[str, Any], key: str) -> str:
       # API Gateway는 헤더를 소문자로 변환할 수 있음
       # 대소문자 무시하고 헤더 값 가져오기
   ```

3. **서명 검증 개선**
   - Body 문자열을 원본 그대로 사용하여 검증
   - 타임스탬프 검증 강화

---

## 테스트 방법

### 로컬 테스트 (선택사항)

```python
# test_lambda.py
import json
from slack_events import lambda_handler

# URL 검증 테스트
event = {
    'headers': {},
    'body': json.dumps({
        'type': 'url_verification',
        'challenge': 'test123456'
    })
}

result = lambda_handler(event, None)
print(result)
# 예상 결과: {'statusCode': 200, 'body': 'test123456'}
```

### CloudWatch Logs 확인

Lambda 함수가 실행되면 다음 로그가 나타나야 함:

```
INFO Received event: {...}
INFO URL verification challenge received: test123456
```

---

## 문제 해결 체크리스트

- [ ] Lambda 함수 코드 업데이트 완료
- [ ] ZIP 파일 재생성 완료
- [ ] Lambda Console에서 코드 업로드 완료
- [ ] Lambda 테스트 이벤트로 URL 검증 성공 확인
- [ ] Slack Event Subscriptions에서 "URL verified" 확인

---

## 예상 결과

배포 완료 후:
- ✅ Lambda 함수가 URL 검증 요청을 정상 처리
- ✅ Slack Event Subscriptions에서 "URL verified" 확인
- ✅ Bot Events 구독 가능

---

## 추가 문제가 있는 경우

1. **CloudWatch Logs 확인**
   - Lambda Console → Monitor → View CloudWatch Logs
   - 에러 메시지 확인

2. **API Gateway 설정 확인**
   - Lambda Proxy Integration이 활성화되어 있는지
   - POST 메서드가 올바르게 설정되어 있는지

3. **환경 변수 확인**
   - `SLACK_SIGNING_SECRET`이 설정되어 있는지 (일반 이벤트용)

---

**이제 다시 배포하고 테스트해보세요! 🚀**

