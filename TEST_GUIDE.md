# 테스트 가이드

## 단계별 테스트 절차

### ✅ 단계 1: GitHub Actions 워크플로우 실행 확인

**완료됨**: 커밋 702dcc2가 GitHub에 푸시되었습니다.

**확인 방법**:
1. GitHub 저장소로 이동: https://github.com/mandu5/slackbot_test
2. "Actions" 탭 클릭
3. 다음 워크플로우들이 실행되었는지 확인:
   - ✅ `test.yml` - 기본 테스트 (성공해야 함)
   - ✅ `CI Build and Request Approval` - Docker 빌드 (성공해야 함)

**예상 결과**:
- `test.yml`: "Hello World! The workflow is ALIVE!" 메시지 출력
- `ci-build-and-request.yml`: Docker 이미지 빌드 성공, Slack 알림 발송

**문제 발생 시**:
- 워크플로우 로그를 확인하여 에러 메시지 확인
- GitHub Secrets 설정 확인:
  - `SLACK_WEBHOOK_URL` (필수)
  - `SLACK_BOT_TOKEN` (선택)
  - `GITHUB_PERSONAL_ACCESS_TOKEN` (필수)

---

### 단계 2: Slackbot 로컬 실행 테스트

**필수 환경 변수 설정**:

```bash
export SLACK_BOT_TOKEN='xoxb-your-bot-token'
export SLACK_APP_TOKEN='xapp-your-app-token'
export GITHUB_PERSONAL_ACCESS_TOKEN='ghp_your-github-token'
export GITHUB_ID='mandu5'
export GITHUB_REPO='slackbot_test'
```

**실행 방법**:

방법 1: 테스트 스크립트 사용
```bash
./test_slackbot.sh
```

방법 2: 직접 실행
```bash
cd docker_slack_file
python3 slack.py
```

**예상 출력**:
```
INFO - Starting Slack bot...
INFO - GitHub repository: mandu5/slackbot_test
```

**테스트 방법**:
1. Slack 채널에서 봇에게 메시지 전송
2. 봇이 메시지를 받고 응답하는지 확인
3. "배포 시작" 키워드가 포함된 메시지에 대해 GitHub API 호출 확인

---

### 단계 3: 전체 파이프라인 테스트 (Slack → GitHub Actions)

**테스트 시나리오**:

1. **Slack에서 배포 트리거**
   ```
   @SoftBank_Bot 자동 배포 시작
   ```
   또는
   ```
   @SoftBank_Bot 배포 시작
   ```

2. **예상 동작 순서**:
   - Slackbot이 메시지 수신
   - Slackbot이 GitHub API `repository_dispatch` 호출
   - `dev_deploy.yml` 워크플로우 트리거됨
   - GitHub Actions에서 Docker 이미지 빌드 시작
   - 빌드 완료 후 Slack 알림 발송

3. **확인 사항**:
   - ✅ Slack에서 봇 응답 확인
   - ✅ GitHub Actions에서 `dev_deploy.yml` 실행 확인
   - ✅ Docker 빌드 성공 확인
   - ✅ Slack 완료 알림 확인

**수동 테스트 (GitHub API 직접 호출)**:

```bash
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/mandu5/slackbot_test/dispatches \
  -d '{
    "event_type": "dev_deploy",
    "client_payload": {
      "message": "자동 배포 시작",
      "user": "test_user",
      "tag": "v1.0"
    }
  }'
```

**예상 응답**: HTTP 204 (No Content) - 성공

---

## 문제 해결

### GitHub Actions가 실행되지 않는 경우

1. **워크플로우 권한 확인**:
   - 저장소 Settings → Actions → General
   - "Workflow permissions" → "Read and write permissions" 선택

2. **Secrets 확인**:
   - 저장소 Settings → Secrets and variables → Actions
   - 필수 Secrets가 모두 설정되어 있는지 확인

### Slackbot이 메시지를 받지 못하는 경우

1. **Socket Mode 확인**:
   - Slack API 대시보드에서 Socket Mode 활성화 확인
   - App-Level Token이 생성되어 있는지 확인

2. **Event Subscriptions 확인**:
   - `message.channels` 이벤트가 구독되어 있는지 확인
   - 봇이 채널에 초대되어 있는지 확인

3. **토큰 확인**:
   - Bot Token과 App Token이 올바른지 확인
   - 토큰 권한(Scopes)이 올바른지 확인

### repository_dispatch가 트리거되지 않는 경우

1. **GitHub Token 권한 확인**:
   - Personal Access Token에 `repo` 권한이 있는지 확인

2. **저장소 이름 확인**:
   - `GITHUB_ID`와 `GITHUB_REPO`가 올바른지 확인

3. **event_type 확인**:
   - 호출하는 `event_type`이 워크플로우의 `types`와 일치하는지 확인

---

## 다음 단계

모든 테스트가 성공하면:
1. ✅ GitHub Actions 워크플로우가 자동으로 실행됨
2. ✅ Slackbot이 메시지를 받고 응답함
3. ✅ 전체 파이프라인이 정상 작동함

이제 프로덕션 환경에 배포할 준비가 되었습니다!

