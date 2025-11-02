# Atlas Platform - CI/CD Pipeline

GitHub Actions 기반의 자동화된 CI/CD 파이프라인과 Slack ChatOps를 통한 배포 시스템입니다.

## 🏗️ 아키텍처 개요

### 파이프라인 플로우

```
1. CI Pipeline (Push to main)
   main 브랜치 push
   → ci-build-and-request.yml 트리거
   → Docker 이미지 빌드
   → Slack 알림 발송

2. ChatOps Integration
   Slack에서 "@SoftBank_Bot 자동 배포 시작" 메시지 전송
   → Slackbot이 GitHub API repository_dispatch 호출
   → dev_deploy.yml 워크플로우 트리거
   → Docker 이미지 빌드 및 배포 시뮬레이션
   → Slack 완료 알림

3. CD Pipeline (Approval-based)
   승인 버튼 클릭 또는 repository_dispatch
   → cd-deploy-on-approval.yml 트리거
   → 배포 프로세스 실행 (Terraform 시뮬레이션)
   → 최종 Slack 알림
```

## 📁 프로젝트 구조

```
.
├── .github/
│   └── workflows/
│       ├── test.yml                    # 기본 테스트 워크플로우
│       ├── ci-build-and-request.yml    # CI: Docker 빌드 및 승인 요청
│       ├── dev_deploy.yml              # ChatOps 트리거 배포
│       └── cd-deploy-on-approval.yml   # 승인 기반 프로덕션 배포
├── docker_slack_file/
│   ├── slack.py                        # Slack 봇 메인 코드
│   ├── config.py                       # 환경 변수 설정
│   └── dockerfile                      # Slackbot Docker 이미지
├── Dockerfile                          # CI 테스트용 최소 Dockerfile
└── README.md
```

## 🔧 설정 방법

### 1. GitHub Secrets 설정

다음 Secrets를 GitHub 저장소 설정에서 추가해야 합니다:

| Secret 이름 | 설명 | 필수 |
|------------|------|------|
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL | ✅ |
| `SLACK_BOT_TOKEN` | Slack Bot User OAuth Token (xoxb-...) | 선택 |
| `SLACK_CHANNEL_ID` | Slack 채널 ID (C... 형태) | 선택 |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | GitHub Personal Access Token (repo 권한) | ✅ |

**Slack Webhook URL 확인 방법:**
```bash
# 현재 작동하는 Webhook URL 예시
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Hello, World!"}' \
  https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

**GitHub Personal Access Token 생성:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. `repo` 권한 체크
3. 토큰 생성 후 GitHub Secrets에 추가

### 2. Slack 앱 설정

#### Socket Mode 활성화
1. [Slack API](https://api.slack.com/apps) 접속
2. 앱 선택 → Socket Mode 메뉴
3. "Enable Socket Mode" 활성화
4. App-Level Token 생성 (권한: `connections:write`)
5. 토큰을 `SLACK_APP_TOKEN` 환경 변수로 설정

#### Event Subscriptions 설정
1. Event Subscriptions 메뉴 → Enable Events
2. Subscribe to bot events:
   - `message.channels`
   - `message.groups`
   - `message.im`
   - `message.mpim`

#### OAuth & Permissions
1. Bot Token Scopes 추가:
   - `chat:write`
   - `channels:history`
   - `groups:history`
   - `im:history`
   - `mpim:history`
2. "Install to Workspace" 클릭
3. Bot User OAuth Token (`xoxb-...`)을 복사하여 `SLACK_BOT_TOKEN` 환경 변수로 설정

#### 채널 ID 확인
1. Slack 채널 열기
2. 채널 정보 (오른쪽 상단 ⓘ) → 하단 "Integrations" → "Channel ID" 확인

### 3. Slackbot 로컬 실행

```bash
cd docker_slack_file

# 환경 변수 설정
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
export SLACK_APP_TOKEN="xapp-your-app-token"
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your-github-token"
export GITHUB_ID="your-github-username"
export GITHUB_REPO="slackbot_test"

# Python 패키지 설치
pip install slack_bolt requests

# 실행
python slack.py
```

### 4. Docker로 Slackbot 실행

```bash
cd docker_slack_file

# Docker 이미지 빌드
docker build -t slackbot .

# Docker 컨테이너 실행
docker run -d \
  -e SLACK_BOT_TOKEN="xoxb-your-bot-token" \
  -e SLACK_APP_TOKEN="xapp-your-app-token" \
  -e GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your-github-token" \
  -e GITHUB_ID="your-github-username" \
  -e GITHUB_REPO="slackbot_test" \
  --name slackbot \
  slackbot
```

## 🚀 사용 방법

### CI 파이프라인 테스트

```bash
# main 브랜치에 푸시하면 자동으로 트리거됨
git push origin main
```

GitHub Actions에서 다음이 실행됩니다:
1. Docker 이미지 빌드
2. Slack 알림 발송 (배포 승인 요청)

### ChatOps 배포

Slack 채널에서 다음 메시지 전송:

```
@SoftBank_Bot 자동 배포 시작
```

또는:

```
@SoftBank_Bot 배포 시작
```

Slackbot이 GitHub Actions 워크플로우를 트리거하여 배포 프로세스를 시작합니다.

### 수동 배포 트리거 테스트

```bash
# GitHub API를 직접 호출하여 테스트
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/YOUR_USERNAME/slackbot_test/dispatches \
  -d '{
    "event_type": "dev_deploy",
    "client_payload": {
      "message": "자동 배포 시작",
      "user": "test_user",
      "tag": "v1.0"
    }
  }'
```

## 📊 워크플로우 설명

### test.yml
- **트리거**: main 브랜치 push
- **기능**: 기본 워크플로우 동작 확인
- **용도**: CI/CD 파이프라인 기본 테스트

### ci-build-and-request.yml
- **트리거**: main 브랜치 push
- **기능**:
  - Docker 이미지 빌드
  - Slack 알림 발송 (배포 승인 요청)
- **출력**: Docker 이미지 태그

### dev_deploy.yml
- **트리거**: `repository_dispatch` (event_type: `dev_deploy`)
- **기능**:
  - Slack 메시지 파싱
  - Docker 이미지 빌드
  - 배포 시뮬레이션
  - Slack 완료/실패 알림
- **트리거 방법**: Slackbot 또는 GitHub API 직접 호출

### cd-deploy-on-approval.yml
- **트리거**: `repository_dispatch` (event_type: `deploy-approval`)
- **기능**:
  - 프로덕션 배포 프로세스 시뮬레이션
  - Terraform 인프라 배포 시뮬레이션
  - 헬스 체크 시뮬레이션
  - Slack 최종 알림
- **참고**: 실제 AWS 인프라가 없으므로 시뮬레이션만 수행

## 🔍 문제 해결

### GitHub Actions 실패

**문제**: 워크플로우가 실패함
- **해결**: GitHub Actions 탭에서 로그 확인
- **확인 사항**:
  - Secrets가 올바르게 설정되었는지
  - Dockerfile이 존재하는지
  - Slack Webhook URL이 유효한지

### Slackbot이 반응하지 않음

**문제**: Slack 메시지에 봇이 응답하지 않음
- **확인 사항**:
  1. `SLACK_BOT_TOKEN` 및 `SLACK_APP_TOKEN` 환경 변수 확인
  2. Socket Mode가 활성화되었는지 확인
  3. Event Subscriptions에서 `message.channels` 등이 구독되어 있는지 확인
  4. 봇이 채널에 초대되었는지 확인
  5. Docker 컨테이너 로그 확인: `docker logs slackbot`

### repository_dispatch가 트리거되지 않음

**문제**: Slackbot이 GitHub API를 호출했지만 워크플로우가 실행되지 않음
- **확인 사항**:
  1. `GITHUB_PERSONAL_ACCESS_TOKEN`이 올바른지 확인 (repo 권한 필요)
  2. GitHub 저장소 이름이 올바른지 확인 (`GITHUB_ID/GITHUB_REPO`)
  3. `event_type`이 워크플로우의 `types`와 일치하는지 확인
  4. GitHub Actions → "Workflow permissions"에서 "Read and write permissions" 체크

### Docker 빌드 실패

**문제**: GitHub Actions에서 Docker 빌드가 실패함
- **해결**:
  1. Dockerfile이 루트 디렉토리에 있는지 확인
  2. Dockerfile 구문 오류 확인
  3. Docker Buildx가 올바르게 설정되었는지 확인

## 🧪 테스트 체크리스트

- [ ] `test.yml` 워크플로우가 성공적으로 실행됨
- [ ] `ci-build-and-request.yml`에서 Docker 이미지 빌드 성공
- [ ] `ci-build-and-request.yml`에서 Slack 알림 발송 성공
- [ ] Slackbot이 메시지를 수신하고 응답함
- [ ] Slackbot이 `repository_dispatch` API 호출 성공
- [ ] `dev_deploy.yml`이 repository_dispatch로 트리거됨
- [ ] `dev_deploy.yml`이 Docker 이미지 빌드 성공
- [ ] 모든 워크플로우가 GitHub Actions에서 성공 상태 표시

## 📝 추가 개발 계획

### 향후 구현 예정

1. **AWS 인프라 연동**
   - ECS on Fargate 배포
   - CodeDeploy Blue/Green 배포
   - ALB Target Group 전환

2. **Terraform IaC**
   - ECS Service, Task Definition
   - CodeDeploy Application, Deployment Group
   - DynamoDB Table
   - AWS Managed Grafana

3. **고급 ChatOps 기능**
   - `terraform plan` 결과 Slack 리포팅
   - `/platform rollback [version]` 명령어
   - Grafana 차트 스냅샷 리포팅

4. **모니터링 및 관찰성**
   - DynamoDB 데이터 시각화
   - Grafana 대시보드 연동
   - 배포 메트릭 수집

## 📚 참고 자료

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Slack Bolt Framework](https://slack.dev/bolt-python/)
- [GitHub API - Repository Dispatches](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [Slack API Documentation](https://api.slack.com/)

## 🤝 기여

이슈나 풀 리퀘스트를 환영합니다!

## 📄 라이선스

이 프로젝트는 SoftBank Hackathon 2025를 위한 프로토타입입니다.
