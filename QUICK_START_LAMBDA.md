# 🚀 Lambda ChatOps 빠른 시작 가이드

**해커톤 최적 전략**: 서버 없이 Lambda로 ChatOps 구현 (최대 점수)

---

## ⚡ 30분 안에 배포하기

### Step 1: Lambda 함수 ZIP 생성 (5분)

```bash
cd lambda

# 의존성 설치
pip install -r requirements.txt -t .

# ZIP 파일 생성
zip -r lambda_function.zip . -x "*.pyc" -x "__pycache__/*"
```

### Step 2: AWS Lambda 함수 생성 (10분)

#### AWS Console 방법:

1. **Lambda Console 접속**
   - https://console.aws.amazon.com/lambda/
   - "Create function" 클릭

2. **함수 설정**
   - Function name: `slackbot-chatops`
   - Runtime: Python 3.11
   - Architecture: x86_64

3. **코드 업로드**
   - "Upload from" → ".zip file"
   - `lambda_function.zip` 업로드
   - Handler: `slack_events.lambda_handler`

4. **환경 변수 설정**
   - Configuration → Environment variables
   - 다음 변수 추가:
     ```
     SLACK_SIGNING_SECRET=your-signing-secret
     GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your-token
     GITHUB_ID=mandu5
     GITHUB_REPO=slackbot_test
     ```

5. **타임아웃 설정**
   - Configuration → General configuration → Edit
   - Timeout: 30 seconds

### Step 3: API Gateway 설정 (10분)

#### REST API 생성:

1. **API Gateway Console 접속**
   - https://console.aws.amazon.com/apigateway/
   - "Create API" → "REST API" → "Build"

2. **리소스 생성**
   - Actions → Create Resource
   - Resource Path: `slack`
   - Enable CORS: ❌

3. **하위 리소스 생성**
   - `slack` 선택 → Actions → Create Resource
   - Resource Path: `events`
   - Enable CORS: ❌

4. **메서드 생성**
   - `events` 선택 → Actions → Create Method → POST
   - Integration type: Lambda Function
   - Lambda Function: `slackbot-chatops`
   - Enable Lambda Proxy Integration: ✅

5. **API 배포**
   - Actions → Deploy API
   - Deployment stage: `prod` (또는 새로 생성)
   - **Invoke URL 복사**: `https://xxxxx.execute-api.region.amazonaws.com/prod/slack/events`

### Step 4: Slack 앱 설정 변경 (5분)

1. **Slack API Dashboard 접속**
   - https://api.slack.com/apps
   - 앱 선택

2. **Socket Mode 비활성화**
   - Socket Mode → Disable Socket Mode

3. **Event Subscriptions 활성화**
   - Event Subscriptions → Enable Events
   - Request URL: `https://xxxxx.execute-api.region.amazonaws.com/prod/slack/events` (Step 3에서 복사한 URL)
   - "Save Changes" 클릭 → URL 검증 자동 진행

4. **Bot Events 구독**
   - Subscribe to bot events:
     - `message.channels` 추가
     - `message.groups` 추가
   - "Save Changes" 클릭

5. **Signing Secret 복사**
   - Basic Information → App Credentials → Signing Secret
   - Lambda 함수 환경 변수에 `SLACK_SIGNING_SECRET`로 추가

---

## ✅ 테스트

### 1. Lambda 함수 테스트

```bash
# URL 검증 테스트 이벤트
aws lambda invoke \
  --function-name slackbot-chatops \
  --payload '{"body":"{\"type\":\"url_verification\",\"challenge\":\"test123\"}"}' \
  response.json

cat response.json
```

### 2. Slack 메시지 테스트

1. Slack 채널에서: `@SoftBank_Bot 자동 배포 시작`
2. CloudWatch Logs 확인:
   ```bash
   aws logs tail /aws/lambda/slackbot-chatops --follow
   ```
3. GitHub Actions 확인:
   - GitHub 저장소 → Actions 탭
   - `dev_deploy.yml` 워크플로우가 트리거되었는지 확인

---

## 🔧 문제 해결

### URL 검증 실패

**증상**: Slack에서 "URL verification failed" 오류

**해결**:
1. Lambda 함수의 환경 변수 `SLACK_SIGNING_SECRET` 확인
2. API Gateway의 `POST /slack/events` 메서드가 Lambda와 연결되어 있는지 확인
3. Lambda Proxy Integration이 활성화되어 있는지 확인

### Lambda 타임아웃

**증상**: Lambda 함수가 타임아웃됨

**해결**:
1. Configuration → General configuration → Timeout을 30초로 증가
2. CloudWatch Logs에서 에러 확인

### GitHub API 호출 실패

**증상**: Lambda 로그에 GitHub API 에러

**해결**:
1. `GITHUB_PERSONAL_ACCESS_TOKEN` 환경 변수 확인
2. Token에 `repo` 권한이 있는지 확인
3. `GITHUB_ID`와 `GITHUB_REPO`가 올바른지 확인

---

## 🎯 다음 단계 (고급 기능)

### Slack 버튼 인터랙션 추가

`ci-build-and-request.yml`에서 승인 버튼을 추가하려면:

```yaml
- name: Send Slack Approval Request
  run: |
    curl -X POST -H 'Content-type: application/json' \
      --data '{
        "text": "배포 준비 완료!",
        "blocks": [
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {"type": "plain_text", "text": "✅ 승인"},
                "action_id": "approve_deployment",
                "value": "${{ github.sha }}"
              }
            ]
          }
        ]
      }' \
      ${{ secrets.SLACK_WEBHOOK_URL }}
```

Lambda에서 버튼 클릭 이벤트 처리:

```python
if event.get('type') == 'block_actions':
    action = event.get('actions', [{}])[0]
    if action.get('action_id') == 'approve_deployment':
        # 배포 승인 처리
        trigger_github_deployment(...)
```

---

## 📊 비용

### AWS Free Tier

- ✅ Lambda: 월 100만 요청 무료
- ✅ API Gateway: 월 100만 요청 무료
- ✅ CloudWatch Logs: 월 5GB 무료

**결론**: 해커톤 기간 동안 **완전 무료** 🎉

---

## 🏆 해커톤 점수 기여

이 Lambda 구현으로 획득할 수 있는 점수:

| 항목 | 점수 | 설명 |
|------|------|------|
| 클라우드 활용 | +15점 | Lambda + API Gateway (서버리스) |
| 완성도 | +10점 | ChatOps 플로우 작동 |
| 팀 개발 | +10점 | GitOps/ChatOps 증명 |
| 재미 요소 | +5점 | 인터랙티브 버튼 가능 |
| **합계** | **+40점** | |

---

## 📝 체크리스트

배포 완료 확인:

- [ ] Lambda 함수 생성 완료
- [ ] 환경 변수 설정 완료
- [ ] API Gateway 엔드포인트 생성 완료
- [ ] Slack Event Subscriptions 설정 완료
- [ ] URL 검증 성공
- [ ] Slack 메시지 → Lambda → GitHub Actions 테스트 성공
- [ ] CloudWatch Logs에서 로그 확인 가능

---

## 🚨 중요 참고사항

1. **Lambda 함수는 항상 실행 가능 상태**
   - 서버 관리 불필요
   - 자동 스케일링
   - 고가용성

2. **비용 걱정 없음**
   - AWS Free Tier로 해커톤 기간 동안 무료
   - 트래픽이 많아도 Free Tier 범위 내

3. **해커톤 요구사항 완벽 부합**
   - "ChatOps Engineer (Bot): AWS Lambda + API Gateway" ✅

---

**이제 서버 없이도 ChatOps가 완벽하게 작동합니다! 🎉**

