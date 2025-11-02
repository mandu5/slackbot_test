# 🔧 URL 검증 문제 해결

## 문제 발견

**잘못된 URL**: 
```
https://0ygtneavt5.execute-api.ap-southeast-2.amazonaws.com/prod
```

**올바른 URL**: 
```
https://0ygtneavt5.execute-api.ap-southeast-2.amazonaws.com/prod/slack/events
```

**차이점**: `/slack/events` 경로가 누락되었습니다!

---

## 해결 방법

### Step 1: Slack Event Subscriptions에서 올바른 URL 입력

1. **Slack API Dashboard 접속**
   - https://api.slack.com/apps
   - 앱 선택

2. **Event Subscriptions 메뉴**
   - Request URL 필드에 **정확한 URL 입력**:
   ```
   https://0ygtneavt5.execute-api.ap-southeast-2.amazonaws.com/prod/slack/events
   ```
   
   ⚠️ **중요**: 마지막에 `/slack/events`가 반드시 포함되어야 합니다!

3. **"Save Changes" 클릭**

---

## 확인 사항

### API Gateway 설정 확인

다음이 모두 설정되어 있어야 합니다:

1. **리소스 구조**:
   ```
   / (root)
   └── /slack
       └── /events (POST 메서드)
   ```

2. **POST /slack/events 메서드**:
   - Integration type: Lambda Function
   - **Use Lambda Proxy integration**: ✅ 체크됨
   - Lambda Function: `slackbot-chatops`

3. **API 배포**:
   - Deployment stage: `prod`
   - 배포 완료 확인

---

## 테스트 방법

### API Gateway 직접 테스트

터미널에서 다음 명령어로 테스트:

```bash
curl -X POST \
  https://0ygtneavt5.execute-api.ap-southeast-2.amazonaws.com/prod/slack/events \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test123456"}'
```

**예상 응답**: `test123456` (challenge 값 그대로 반환)

### Lambda 함수 직접 테스트

1. **Lambda Console 접속**
   - https://console.aws.amazon.com/lambda/
   - `slackbot-chatops` 함수 선택

2. **Test 탭 → 새 테스트 이벤트**
   ```json
   {
     "headers": {},
     "body": "{\"type\":\"url_verification\",\"challenge\":\"test123456\"}"
   }
   ```

3. **"Test" 클릭**
   - ✅ Response: `{"statusCode": 200, "body": "test123456"}`

---

## 체크리스트

- [ ] API Gateway URL에 `/slack/events` 경로가 포함되어 있는지 확인
- [ ] Slack Event Subscriptions에서 올바른 전체 URL 입력
- [ ] API Gateway에서 `/slack/events` 리소스가 존재하는지 확인
- [ ] POST 메서드가 Lambda와 연결되어 있는지 확인
- [ ] Lambda Proxy Integration이 활성화되어 있는지 확인
- [ ] API가 `prod` stage에 배포되어 있는지 확인

---

## 문제가 계속되는 경우

### 1. CloudWatch Logs 확인

Lambda Console → Monitor → View CloudWatch Logs

다음 로그가 보여야 합니다:
```
INFO Received event: {...}
INFO URL verification challenge received: ...
```

### 2. API Gateway 설정 재확인

1. API Gateway Console 접속
2. API 선택 → Resources 확인
3. `/slack/events` → POST 메서드 확인
4. Integration Request → Lambda Proxy integration 활성화 확인

### 3. Lambda 함수 재배포

```bash
cd lambda
./deploy.sh
```

Lambda Console에서 ZIP 파일 업로드

---

## 정확한 URL 형식

**템플릿**:
```
https://{api-id}.execute-api.{region}.amazonaws.com/{stage}/slack/events
```

**예시**:
```
https://0ygtneavt5.execute-api.ap-southeast-2.amazonaws.com/prod/slack/events
```

**구성 요소**:
- `0ygtneavt5`: API ID
- `ap-southeast-2`: 리전
- `prod`: Deployment stage
- `/slack/events`: 리소스 경로

---

**올바른 URL로 다시 시도해보세요! 🚀**

