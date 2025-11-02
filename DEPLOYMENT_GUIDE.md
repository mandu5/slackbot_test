# Slackbot 서버 배포 가이드

## 📌 현재 상황 설명

**핵심 포인트**: Slackbot은 **항상 실행 중**이어야 Slack 메시지를 받을 수 있습니다.

- **GitHub Actions → Slack**: 웹훅으로 전송되므로 항상 작동 ✅ (이미 작동 중)
- **Slack → Slackbot**: `slack.py`가 실행 중이어야 메시지를 감지할 수 있음 ⚠️

현재 `Socket Mode`를 사용하므로, Slackbot 프로세스가 어딘가에서 실행되어야 합니다.

---

## 🚀 배포 옵션

### 옵션 1: 클라우드 서버에 Docker 배포 (권장)

#### AWS EC2 예시

```bash
# 1. EC2 인스턴스에 접속
ssh -i your-key.pem ec2-user@your-ec2-ip

# 2. Docker 설치 (아직 없다면)
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# 3. 프로젝트 클론 또는 파일 업로드
git clone https://github.com/mandu5/slackbot_test.git
cd slackbot_test/docker_slack_file

# 4. Docker 이미지 빌드
docker build -t slackbot .

# 5. 환경 변수 설정 및 컨테이너 실행
docker run -d \
  --name slackbot \
  --restart always \
  -e SLACK_BOT_TOKEN="xoxb-your-bot-token" \
  -e SLACK_APP_TOKEN="xapp-your-app-token" \
  -e GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your-github-token" \
  -e GITHUB_ID="mandu5" \
  -e GITHUB_REPO="slackbot_test" \
  slackbot

# 6. 로그 확인
docker logs -f slackbot
```

#### GCP / Azure도 동일한 방식으로 가능

#### 환경 변수는 Secrets Manager 사용 권장

```bash
# AWS Secrets Manager 예시
aws secretsmanager create-secret \
  --name slackbot/secrets \
  --secret-string '{"SLACK_BOT_TOKEN":"xoxb-...","SLACK_APP_TOKEN":"xapp-..."}'

# Docker에서 Secrets Manager 사용
docker run -d \
  --name slackbot \
  -e SLACK_BOT_TOKEN=$(aws secretsmanager get-secret-value --secret-id slackbot/secrets --query SecretString --output text | jq -r .SLACK_BOT_TOKEN) \
  slackbot
```

### 옵션 2: 클라우드 PaaS 사용

#### Heroku 배포

```bash
# 1. Heroku CLI 설치 후 로그인
heroku login

# 2. 앱 생성
heroku create your-slackbot-app

# 3. 환경 변수 설정
heroku config:set SLACK_BOT_TOKEN=xoxb-your-token
heroku config:set SLACK_APP_TOKEN=xapp-your-token
heroku config:set GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your-token
heroku config:set GITHUB_ID=mandu5
heroku config:set GITHUB_REPO=slackbot_test

# 4. 배포
cd docker_slack_file
git subtree push --prefix docker_slack_file heroku main

# 또는 Procfile 생성
echo "python slack.py" > Procfile
git push heroku main
```

#### Railway 배포

```bash
# Railway CLI 설치
npm i -g @railway/cli

# 배포
railway login
railway init
railway up
```

#### Render.com 배포

1. Render 대시보드에서 새 Web Service 생성
2. Dockerfile 경로: `docker_slack_file/dockerfile`
3. 환경 변수 설정
4. 배포

### 옵션 3: 기존 서버에 systemd로 실행

```bash
# 1. 서버에 프로젝트 배포
cd /opt
git clone https://github.com/mandu5/slackbot_test.git
cd slackbot_test/docker_slack_file

# 2. Python 가상환경 설정
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # requirements.txt 생성 필요

# 3. systemd 서비스 파일 생성
sudo nano /etc/systemd/system/slackbot.service
```

**`/etc/systemd/system/slackbot.service`** 내용:

```ini
[Unit]
Description=Slackbot Service
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/opt/slackbot_test/docker_slack_file
Environment="SLACK_BOT_TOKEN=xoxb-your-token"
Environment="SLACK_APP_TOKEN=xapp-your-token"
Environment="GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your-token"
Environment="GITHUB_ID=mandu5"
Environment="GITHUB_REPO=slackbot_test"
ExecStart=/opt/slackbot_test/docker_slack_file/venv/bin/python slack.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 4. 서비스 시작
sudo systemctl daemon-reload
sudo systemctl enable slackbot
sudo systemctl start slackbot

# 5. 상태 확인
sudo systemctl status slackbot
sudo journalctl -u slackbot -f
```

---

## 🔄 대안: HTTP 엔드포인트 방식으로 변경

Socket Mode 대신 HTTP 엔드포인트를 사용하면:
- **장점**: 서버리스 환경(예: Cloud Functions, Lambda)에서 실행 가능
- **단점**: 공개 URL 필요, HTTPS 필수, 코드 변경 필요

현재는 Socket Mode가 더 간단하므로, **서버에 배포하는 옵션 1을 권장**합니다.

---

## ✅ 배포 후 확인 사항

1. **Slackbot 실행 확인**:
   ```bash
   docker ps | grep slackbot
   # 또는
   systemctl status slackbot
   ```

2. **로그 확인**:
   ```bash
   docker logs -f slackbot
   # 또는
   journalctl -u slackbot -f
   ```

3. **Slack에서 테스트**:
   - Slack 채널에서 `@SoftBank_Bot 자동 배포 시작` 메시지 전송
   - 봇이 응답하는지 확인
   - GitHub Actions에서 `dev_deploy.yml` 워크플로우가 트리거되는지 확인

---

## 📝 요약

- ✅ **GitHub Actions → Slack**: 이미 작동 중 (웹훅)
- ⚠️ **Slack → GitHub Actions**: Slackbot을 서버에 배포해야 함
- 🚀 **배포 방법**: Docker 컨테이너 또는 systemd 서비스로 실행
- 🔄 **권장**: 클라우드 서버(EC2, GCP, Azure) 또는 PaaS(Heroku, Railway, Render)

---

## 🆘 문제 해결

### Slackbot이 메시지를 받지 못하는 경우

1. **프로세스 실행 확인**:
   ```bash
   ps aux | grep slack.py
   docker ps | grep slackbot
   ```

2. **네트워크 연결 확인**:
   - 방화벽에서 Slack API(api.slack.com) 접근 허용 확인
   - WebSocket 연결이 가능한지 확인

3. **토큰 확인**:
   - Socket Mode 활성화 확인
   - App-Level Token이 올바른지 확인

4. **로그 확인**:
   ```bash
   docker logs slackbot
   # 또는 실행 중인 프로세스의 출력 확인
   ```

