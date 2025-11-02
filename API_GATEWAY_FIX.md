# 🚨 API Gateway 설정 문제 해결

## 문제 분석

`Missing Authentication Token` 오류는 다음을 의미합니다:
1. `/slack/events` 리소스가 생성되지 않았거나
2. POST 메서드가 설정되지 않았거나
3. API가 배포되지 않았거나

---

## 해결 방법: API Gateway 재설정

### Step 1: API Gateway 리소스 확인 및 생성

1. **API Gateway Console 접속**
   - https://console.aws.amazon.com/apigateway/
   - API 선택 (또는 새로 생성)

2. **리소스 구조 확인**
   - 왼쪽 Resources 메뉴에서 확인
   - 다음 구조가 있어야 함:
     ```
     /
     └── /slack
         └── /events
     ```

3. **리소스가 없다면 생성**:

   **a) `/slack` 리소스 생성**
   - Resources에서 `/` 선택
   - Actions → Create Resource
   - Resource Path: `slack`
   - Enable CORS: ❌ (체크 안 함)
   - "Create Resource" 클릭

   **b) `/events` 리소스 생성**
   - Resources에서 `/slack` 선택
   - Actions → Create Resource
   - Resource Path: `events`
   - Enable CORS: ❌ (체크 안 함)
   - "Create Resource" 클릭

### Step 2: POST 메서드 생성 및 Lambda 연동

1. **POST 메서드 생성**
   - Resources에서 `/slack/events` 선택
   - Actions → Create Method → **POST** 선택
   - "Save" 클릭

2. **Lambda 함수 연동**
   - Integration type: **Lambda Function**
   - ✅ **Use Lambda Proxy integration** (반드시 체크!)
   - Lambda Function: `slackbot-chatops` 입력
   - "Save" 클릭
   - 권한 부여 팝업에서 "OK" 클릭

### Step 3: API 배포

1. **Resources 메뉴로 돌아가기**

2. **Actions → Deploy API**
   - Deployment stage: `prod` 선택
     - `prod`가 없다면: "Create Stage" → Stage name: `prod` → "Create Stage"
   - "Deploy" 클릭

3. **Invoke URL 확인**
   - 배포 후 표시되는 Invoke URL 복사
   - 형식: `https://{api-id}.execute-api.{region}.amazonaws.com/prod`
   - **전체 URL**: 위 URL + `/slack/events`
     ```
     https://0ygtneavt5.execute-api.ap-southeast-2.amazonaws.com/prod/slack/events
     ```

### Step 4: 테스트

터미널에서 테스트:

```bash
curl -X POST \
  https://0ygtneavt5.execute-api.ap-southeast-2.amazonaws.com/prod/slack/events \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test123456"}'
```

**성공 응답**: `test123456`
**실패 응답**: `{"message":"Missing Authentication Token"}` 또는 다른 오류

---

## 확인 체크리스트

다음이 모두 완료되어야 합니다:

### API Gateway 설정
- [ ] `/slack` 리소스 생성됨
- [ ] `/slack/events` 리소스 생성됨
- [ ] `/slack/events`에 POST 메서드 생성됨
- [ ] POST 메서드가 Lambda 함수(`slackbot-chatops`)와 연동됨
- [ ] **Lambda Proxy Integration 활성화됨** (중요!)
- [ ] API가 `prod` stage에 배포됨

### Lambda 함수
- [ ] Lambda 함수 `slackbot-chatops`가 생성되어 있음
- [ ] 최신 코드가 배포되어 있음 (URL 검증 수정 포함)
- [ ] 환경 변수 설정 완료:
  - `SLACK_SIGNING_SECRET`
  - `GITHUB_PERSONAL_ACCESS_TOKEN`
  - `GITHUB_ID`
  - `GITHUB_REPO`

---

## 단계별 스크린샷 가이드

### 1. 리소스 생성 확인

```
API Gateway Console → Resources
├── / (root)
└── /slack
    └── /events ← 이게 있어야 함
```

### 2. POST 메서드 확인

```
/slack/events 선택 → Methods
└── POST ← 이게 있어야 함
    └── Integration Request
        └── Integration type: Lambda Function
        └── Use Lambda Proxy integration: ✅
        └── Lambda Function: slackbot-chatops
```

### 3. 배포 확인

```
Actions → Deploy API
└── Deployment stage: prod ← 선택됨
└── Invoke URL: https://...amazonaws.com/prod ← 표시됨
```

---

## 빠른 해결 방법

### 방법 1: API Gateway 설정 재확인 (5분)

1. API Gateway Console 접속
2. Resources 메뉴에서 리소스 구조 확인
3. POST 메서드가 있는지 확인
4. Lambda 연동이 되어 있는지 확인
5. API 배포 확인

### 방법 2: 새로 시작 (10분)

기존 설정이 복잡하다면:

1. **새 API 생성**
   - API Gateway Console → "Create API"
   - REST API → Build
   - API 이름: `slackbot-api`
   - "Create API" 클릭

2. **리소스 및 메서드 생성** (위 Step 1-3 반복)

3. **Slack URL 업데이트**
   - 새 Invoke URL로 변경

---

## 테스트 성공 확인

다음 명령어로 테스트 성공 시:

```bash
$ curl -X POST https://0ygtneavt5.execute-api.ap-southeast-2.amazonaws.com/prod/slack/events \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test123456"}'

test123456  ← 이게 나와야 함
```

**이제 Slack Event Subscriptions에서 URL 검증이 성공합니다!**

---

## 다음 단계

테스트 성공 후:

1. Slack API Dashboard → Event Subscriptions
2. Request URL: `https://0ygtneavt5.execute-api.ap-southeast-2.amazonaws.com/prod/slack/events`
3. "Save Changes" 클릭
4. ✅ "URL verified" 확인

---

**API Gateway 설정을 다시 확인해보세요! 🚀**

