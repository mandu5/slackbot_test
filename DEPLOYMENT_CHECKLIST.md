# ✅ Lambda ChatOps 배포 체크리스트

**해커톤 1등 전략: 서버리스 ChatOps 브릿지 구축**

---

## 🎯 목표

**"AWS Lambda + API Gateway"로 ChatOps 브릿지 구축하여:**

- ✅ 서버 없이 작동 (서버리스)
- ✅ "적절한 규모" 점수 (30점) 획득
- ✅ Terraform 플랫폼 통합 (30점) 증명
- ✅ 안정성 및 확장성 확보

---

## 📋 배포 체크리스트

### Phase 1: Lambda 함수 준비 (5분)

- [ ] `lambda/` 디렉토리로 이동
- [ ] `./deploy.sh` 실행
- [ ] `lambda_function.zip` 파일 생성 확인
- [ ] 파일 크기가 10MB 이하인지 확인

### Phase 2: AWS Lambda 함수 생성 (10분)

- [ ] AWS Lambda Console 접속: https://console.aws.amazon.com/lambda/
- [ ] "Create function" 클릭
- [ ] Function name: `slackbot-chatops` 입력
- [ ] Runtime: Python 3.11 선택
- [ ] Architecture: x86_64 선택
- [ ] "Create function" 클릭

**코드 업로드:**

- [ ] Code 탭 → "Upload from" → ".zip file" 선택
- [ ] `lambda_function.zip` 파일 업로드
- [ ] Handler: `slack_events.lambda_handler` 입력
- [ ] "Save" 클릭

**환경 변수 설정:**

- [ ] Configuration 탭 → Environment variables → Edit
- [ ] 다음 변수 추가:
  ```
  SLACK_SIGNING_SECRET=your-signing-secret (Slack 앱에서 복사)
  GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your-token (GitHub에서 생성)
  GITHUB_ID=mandu5
  GITHUB_REPO=slackbot_test
  ```
- [ ] "Save" 클릭

**타임아웃 설정:**

- [ ] Configuration → General configuration → Edit
- [ ] Timeout: 30 seconds
- [ ] Memory: 128 MB (기본값)
- [ ] "Save" 클릭

**권한 설정 (IAM Role):**

- [ ] Configuration → Permissions
- [ ] Execution role에 다음 정책이 있는지 확인:
  - `AWSLambdaBasicExecutionRole` (CloudWatch Logs)
- [ ] 필요시 "Edit" 클릭하여 권한 추가

### Phase 3: API Gateway 설정 (10분)

- [ ] API Gateway Console 접속: https://console.aws.amazon.com/apigateway/
- [ ] "Create API" → "REST API" → "Build" 클릭

**리소스 생성:**

- [ ] API 이름: `slackbot-api` (또는 원하는 이름)
- [ ] "Create API" 클릭

**리소스 및 메서드 설정:**

- [ ] Actions → Create Resource
- [ ] Resource Path: `slack`
- [ ] Enable CORS: ❌ (체크 안 함)
- [ ] "Create Resource" 클릭

- [ ] `slack` 리소스 선택 → Actions → Create Resource
- [ ] Resource Path: `events`
- [ ] Enable CORS: ❌
- [ ] "Create Resource" 클릭

**POST 메서드 생성:**

- [ ] `events` 리소스 선택 → Actions → Create Method → POST 선택
- [ ] Integration type: Lambda Function
- [ ] Use Lambda Proxy integration: ✅ 체크
- [ ] Lambda Function: `slackbot-chatops` 입력
- [ ] "Save" 클릭
- [ ] 권한 부여 팝업에서 "OK" 클릭

**API 배포:**

- [ ] Actions → Deploy API
- [ ] Deployment stage: `prod` 선택 (또는 "Create Stage")
- [ ] "Deploy" 클릭
- [ ] **Invoke URL 복사**: `https://xxxxx.execute-api.region.amazonaws.com/prod/slack/events`
- [ ] 이 URL을 메모장에 저장 (다음 단계에서 필요)

### Phase 4: Slack 앱 설정 변경 (5분)

- [ ] Slack API Dashboard 접속: https://api.slack.com/apps
- [ ] 앱 선택 (SoftBank_Bot)

**Socket Mode 비활성화:**

- [ ] Socket Mode 메뉴 클릭
- [ ] "Disable Socket Mode" 클릭 (이미 비활성화되어 있으면 패스)
<!-- 
**Event Subscriptions 활성화:**
- [ ] Event Subscriptions 메뉴 클릭
- [ ] "Enable Events" 토글 ON
- [ ] Request URL: Phase 3에서 복사한 API Gateway URL 입력
  ```
  https://xxxxx.execute-api.region.amazonaws.com/prod/slack/events
  ```
- [ ] "Save Changes" 클릭
- [ ] ✅ "URL verified" 확인 (자동으로 검증됨)

**Bot Events 구독:**

- [ ] Subscribe to bot events 섹션에서:
  - [ ] `message.channels` 추가
  - [ ] `message.groups` 추가
- [ ] "Save Changes" 클릭 -->

**Signing Secret 복사:**

- [ ] Basic Information 메뉴 클릭
- [ ] App Credentials 섹션 → Signing Secret 복사
- [ ] Lambda 함수 환경 변수 `SLACK_SIGNING_SECRET`에 업데이트

**OAuth & Permissions (이미 설정되어 있을 수 있음):**

- [ ] Bot Token Scopes 확인:
  - `chat:write`
  - `channels:history`
  - `groups:history`
- [ ] 부족한 권한이 있으면 추가

### Phase 5: 테스트 (5분)

**Lambda 함수 직접 테스트:**

- [ ] Lambda Console → `slackbot-chatops` 함수 선택
- [ ] Test 탭 → "Create new event"
- [ ] Event name: `test-url-verification`
- [ ] Event JSON:
  ```json
  {
    "body": "{\"type\":\"url_verification\",\"challenge\":\"test123\"}"
  }
  ```
- [ ] "Save" → "Test" 클릭
- [ ] ✅ Response에 `test123`이 포함되어 있는지 확인

**Slack 메시지 테스트:**

- [ ] Slack 채널에서: `@SoftBank_Bot 자동 배포 시작`
- [ ] CloudWatch Logs 확인:
  ```bash
  aws logs tail /aws/lambda/slackbot-chatops --follow
  ```
- [ ] 또는 Lambda Console → Monitor → View CloudWatch Logs
- [ ] ✅ "Received message" 로그 확인
- [ ] ✅ "GitHub repository_dispatch triggered" 로그 확인

**GitHub Actions 확인:**

- [ ] GitHub 저장소 → Actions 탭
- [ ] ✅ `dev_deploy.yml` 워크플로우가 트리거되었는지 확인
- [ ] ✅ 워크플로우가 성공적으로 실행되었는지 확인

---

## 🎯 성공 기준

다음이 모두 확인되면 배포 성공:

1. ✅ Lambda 함수가 정상적으로 배포됨
2. ✅ API Gateway 엔드포인트가 생성되고 Lambda와 연동됨
3. ✅ Slack Event Subscriptions에서 "URL verified" 확인
4. ✅ Slack 메시지 → Lambda → GitHub Actions 플로우 작동
5. ✅ CloudWatch Logs에서 모든 이벤트 로그 확인 가능

---

## 🔧 문제 해결

### URL 검증 실패

**증상**: Slack에서 "URL verification failed"

**해결책**:

1. Lambda 함수 환경 변수 `SLACK_SIGNING_SECRET` 확인
2. API Gateway의 `POST /slack/events` 메서드가 Lambda와 연결되어 있는지 확인
3. Lambda Proxy Integration이 활성화되어 있는지 확인
4. API Gateway가 배포되었는지 확인 (Deployment stage)

### Lambda 타임아웃

**증상**: Lambda 함수 실행 시간 초과

**해결책**:

- Configuration → General configuration → Timeout을 30초로 증가

### GitHub API 호출 실패

**증상**: CloudWatch Logs에 "GitHub API error" 로그

**해결책**:

1. `GITHUB_PERSONAL_ACCESS_TOKEN` 환경 변수 확인
2. Token에 `repo` 권한이 있는지 확인
3. `GITHUB_ID`와 `GITHUB_REPO`가 올바른지 확인

### Lambda 함수가 메시지를 받지 못함

**증상**: Slack 메시지를 보냈는데 Lambda 로그에 아무것도 없음

**해결책**:

1. Event Subscriptions이 활성화되어 있는지 확인
2. Bot Events에 `message.channels`, `message.groups`가 구독되어 있는지 확인
3. 봇이 채널에 초대되어 있는지 확인
4. API Gateway 엔드포인트가 올바른지 확인

---

## 📊 배포 완료 후 확인 사항

- [ ] Lambda 함수 실행 시간이 1초 이하인지 확인
- [ ] CloudWatch Logs에서 에러 없이 정상 로그 확인
- [ ] Slack 메시지 → GitHub Actions 트리거 확인
- [ ] API Gateway 엔드포인트가 HTTPS로 접근 가능한지 확인

---

## 🏆 해커톤 점수 기여

이 배포로 획득할 수 있는 점수:

| 항목          | 점수      | 설명                                         |
| ------------- | --------- | -------------------------------------------- |
| 클라우드 활용 | +15점     | Lambda + API Gateway (서버리스, 적절한 규모) |
| 완성도        | +10점     | ChatOps 플로우 완벽 작동                     |
| 팀 개발       | +10점     | GitOps/ChatOps 증명, Terraform 통합 가능     |
| 재미 요소     | +5점      | 인터랙티브 버튼 가능                         |
| **합계**      | **+40점** |                                              |

---

**다음 단계**: 배포 완료 후 Terraform 코드에 Lambda와 API Gateway 추가 (플랫폼 통합 증명)
