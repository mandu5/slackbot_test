# 🏆 SoftBank Hackathon 2025: 최적 전략 가이드

## 🎯 핵심 전략: Lambda 기반 ChatOps (서버 없이 최대 점수)

**왜 Lambda인가?**
1. ✅ **서버 없음** - AWS Free Tier로 무료
2. ✅ **클라우드 활용 점수 (30점)** - "서버리스" = 과하지 않게, 적절한 규모
3. ✅ **빠른 구현** - Socket Mode 대신 HTTP Events API 사용
4. ✅ **해커톤 요구사항 완벽 부합** - "ChatOps Engineer (Bot): AWS Lambda + API Gateway"

---

## 🚀 3단계 구현 전략

### Phase 1: Lambda ChatOps 봇 (최우선 - 현재 진행)

**목표**: Socket Mode → Lambda HTTP Events API로 변경

**장점**:
- ✅ 서버 없이 작동 (AWS Free Tier)
- ✅ 항상 실행 중 (서버리스)
- ✅ 해커톤 요구사항 100% 부합
- ✅ Slack 버튼 인터랙션 가능 (재미 요소)

**구현 단계**:
1. Slack Events API 엔드포인트 생성
2. Lambda 함수 작성 (Python)
3. API Gateway 연동
4. Slack 앱 설정 변경 (Socket Mode → HTTP)

### Phase 2: ECS Fargate + Terraform (인프라 점수)

**목표**: Terraform으로 ECS 인프라 코드화

**구현 단계**:
1. Terraform으로 ECS Cluster 생성
2. ECS Task Definition (Fargate)
3. CodeDeploy Application/Deployment Group
4. DynamoDB Table (데이터 지속성)
5. GitHub Actions에 Terraform 적용 단계 추가

### Phase 3: Grafana 연동 (완성도 점수)

**목표**: DynamoDB 데이터 시각화

**구현 단계**:
1. AWS Managed Grafana 설정
2. DynamoDB 데이터 소스 연결
3. 대시보드 생성
4. 배포 성공 시 Grafana 스냅샷 전송 (Slack)

---

## 📊 점수별 전략 상세

### [30점] 클라우드 활용 수준

**전략**: Lambda + ECS Fargate + Terraform

```
✅ Lambda (ChatOps 봇) - 서버리스, 적절한 규모
✅ ECS Fargate (앱 배포) - 컨테이너 오케스트레이션
✅ Terraform (IaC) - 인프라 코드화 증명
✅ DynamoDB (데이터) - 서버리스 데이터베이스
✅ CodeDeploy - 블루/그린 배포
```

**증명 방법**:
- Terraform 코드를 보여주며 "모든 인프라를 코드로 관리" 증명
- AWS 콘솔에서 Lambda, ECS, DynamoDB를 라이브로 보여줌

### [30점] 완성도 및 데모 시연

**전략**: ChatOps → CodeDeploy → Grafana 플로우

**데모 순서**:
1. `git push` → GitHub Actions CI 완료
2. Slack에서 "승인 버튼" 표시 (Lambda가 생성)
3. 심사위원에게 "Yes 버튼을 눌러주세요" 요청 (인터랙션)
4. AWS CodeDeploy 콘솔에서 블루/그린 배포 진행 보여주기
5. 배포 성공 후 Grafana 스냅샷이 Slack에 전송되는 것 보여주기
6. Grafana 대시보드에서 DynamoDB 데이터가 실시간으로 업데이트되는 것 보여주기

**핵심 포인트**:
- ✅ 배포 플로우가 정상 동작함
- ✅ 데이터의 지속성 (DynamoDB)
- ✅ 데이터의 획득 (Grafana)

### [30점] 팀 개발

**전략**: GitOps + ChatOps = 팀워크 증명

**구현**:
1. **GitHub Wiki ADR**: 모든 기술 결정을 문서화
   - "왜 Socket Mode 대신 Lambda를 선택했는가?"
   - "왜 k8s 대신 ECS를 선택했는가?"
   - "왜 Terraform을 사용하는가?"

2. **GitOps**: 모든 인프라 변경은 PR로
   - Terraform 코드 리뷰
   - GitHub Actions 워크플로우 리뷰

3. **ChatOps**: 배포는 Slack에서만
   - 팀원들이 모두 Slack에서 승인/롤백 가능
   - 모든 배포 이력이 Slack에 기록됨

**증명 방법**:
- 발표 시 GitHub Wiki ADR 페이지를 보여주며 "대안 검토 과정" 설명
- Slack 채널을 보여주며 "팀원들이 모두 참여하는 ChatOps 시스템" 증명

### [10점] 재미 요소 및 독창성

**전략**: 인터랙티브 ChatOps + Grafana 시각화

**구현**:
1. **Slack 버튼 인터랙션**:
   - 승인 버튼 (Lambda가 생성)
   - 롤백 버튼
   - 상태 조회 버튼

2. **Grafana 스냅샷**:
   - 배포 성공 시 Grafana 대시보드 이미지를 Slack에 전송
   - BGM/GIF 추가 (선택)

3. **Slash Commands**:
   - `/platform status` - 현재 배포 상태
   - `/platform rollback` - 긴급 롤백

---

## 🔧 구현 로드맵 (1주일)

### Day 1-2: Lambda ChatOps 봇 (최우선)

```
✅ Socket Mode → Lambda HTTP Events API 변경
✅ Lambda 함수 작성
✅ API Gateway 연동
✅ Slack 앱 설정 변경
✅ 테스트: Slack 메시지 → Lambda → GitHub API
```

**파일 구조**:
```
lambda/
  ├── slack_events.py          # Lambda 핸들러
  ├── github_client.py         # GitHub API 호출
  └── requirements.txt
```

### Day 3-4: Terraform 인프라

```
✅ ECS Cluster (Fargate)
✅ ECS Task Definition
✅ CodeDeploy Application/Deployment Group
✅ DynamoDB Table
✅ GitHub Actions에 terraform apply 단계 추가
```

**파일 구조**:
```
terraform/
  ├── main.tf
  ├── variables.tf
  ├── ecs.tf
  ├── codedeploy.tf
  ├── dynamodb.tf
  └── outputs.tf
```

### Day 5-6: Grafana 연동

```
✅ AWS Managed Grafana 설정
✅ DynamoDB 데이터 소스 연결
✅ 대시보드 생성
✅ 배포 성공 시 Grafana 스냅샷 전송 로직
```

### Day 7: 통합 테스트 및 문서화

```
✅ 전체 플로우 테스트
✅ GitHub Wiki ADR 작성
✅ README 업데이트
✅ 발표 준비
```

---

## 💡 현재 → Lambda 전환 방법

### 현재 구조 (Socket Mode)
```
Slack → SocketModeHandler → slack.py (항상 실행 필요)
```

### 목표 구조 (Lambda HTTP)
```
Slack → API Gateway → Lambda → GitHub API
```

### 전환 단계

1. **Lambda 함수 생성**:
   - `lambda/slack_events.py` 작성
   - Slack Events API 검증 로직
   - GitHub repository_dispatch 호출 로직

2. **API Gateway 설정**:
   - Lambda와 연동
   - Slack URL 검증 엔드포인트
   - 이벤트 수신 엔드포인트

3. **Slack 앱 설정 변경**:
   - Socket Mode 비활성화
   - Event Subscriptions → Request URL에 API Gateway URL 입력
   - 이벤트 구독 활성화

---

## 📝 ADR (Architecture Decision Records) 예시

GitHub Wiki에 다음 내용을 작성:

### ADR-001: ChatOps 구현 방식 선택

**상황**: Slack 메시지를 받아 GitHub Actions를 트리거하는 방법 선택

**대안**:
1. Socket Mode + EC2/ECS 항상 실행
2. Lambda + HTTP Events API

**결정**: Lambda + HTTP Events API 선택

**이유**:
- 서버리스이므로 비용 없음 (AWS Free Tier)
- 항상 실행 중이므로 가용성 높음
- 해커톤 요구사항("Lambda + API Gateway") 부합
- Slack 버튼 인터랙션 구현 용이

### ADR-002: 컨테이너 오케스트레이션 선택

**상황**: 앱 배포를 위한 컨테이너 플랫폼 선택

**대안**:
1. Kubernetes (EKS)
2. ECS on Fargate

**결정**: ECS on Fargate 선택

**이유**:
- "과하지도 부족하지도 않은 적절한 규모" 요구사항 부합
- k8s는 과함 (너무 무거움)
- Lambda는 부족함 (컨테이너 배포 불가)
- ECS Fargate는 완벽한 균형

---

## 🎤 발표 전략 (5분)

### [1분] 설계 문서

1. **GitHub Wiki ADR 페이지 보여주기**
   - "우리는 Lambda와 Socket Mode를 비교 검토하여 Lambda를 선택했습니다"
   - "k8s와 ECS를 비교하여 ECS를 선택했습니다"

2. **Terraform 코드 보여주기**
   - "모든 인프라는 Terraform 코드로 관리되어 설계 문서화되었습니다"

### [4분] 라이브 데모

1. **GitHub Actions CI** (30초)
   - `git push` 실행
   - GitHub Actions에서 Docker 빌드 완료 확인

2. **Slack 승인 버튼** (1분) ⭐ 재미 요소
   - Slack에서 "배포 준비 완료" 메시지 확인
   - 심사위원에게 **"Yes 버튼을 눌러주시겠습니까?"** 요청
   - 버튼 클릭 → Lambda 트리거 확인

3. **AWS CodeDeploy** (1분)
   - AWS 콘솔에서 CodeDeploy 블루/그린 배포 진행 보여주기
   - 트래픽 전환 과정 시연

4. **Grafana 스냅샷** (1분)
   - 배포 성공 후 Slack에 Grafana 이미지 전송되는 것 보여주기
   - Grafana 대시보드에서 DynamoDB 데이터 실시간 업데이트 보여주기

5. **롤백 시연** (30초, 시간 남으면)
   - `/platform rollback` 명령어 실행
   - 이전 버전으로 롤백되는 것 보여주기

---

## ✅ 체크리스트

### 클라우드 활용 (30점)
- [ ] Lambda 함수로 ChatOps 봇 구현
- [ ] ECS Fargate로 앱 배포
- [ ] Terraform으로 모든 인프라 코드화
- [ ] DynamoDB로 데이터 지속성
- [ ] CodeDeploy로 블루/그린 배포

### 완성도 (30점)
- [ ] ChatOps → CodeDeploy → Grafana 플로우 완성
- [ ] 배포 플로우가 정상 동작
- [ ] DynamoDB에 데이터 저장 (지속성)
- [ ] Grafana에서 데이터 조회 (획득)

### 팀 개발 (30점)
- [ ] GitHub Wiki ADR 작성 (대안 검토)
- [ ] Terraform 코드 리뷰 프로세스
- [ ] GitOps로 인프라 변경 관리
- [ ] ChatOps로 팀원 모두 참여

### 재미 요소 (10점)
- [ ] Slack 버튼 인터랙션
- [ ] Grafana 스냅샷 전송
- [ ] Slash Commands 구현

---

## 🚨 치명적인 함정 회피

### ❌ 함정 1: Payload 앱 개발에 시간 소모
- ✅ 해결: 1~2시간만 투자, 나머지는 "Mechanism(배포 플랫폼)"에 집중

### ❌ 함정 2: 팀 개발 무시
- ✅ 해결: 모든 기술 결정을 ADR로 문서화, GitOps/ChatOps 사용 증명

### ❌ 함정 3: Socket Mode 고집 (서버 필요)
- ✅ 해결: Lambda로 전환 (서버 없이 작동)

---

## 🎯 최종 목표

**"기술력" + "인간성" = 함께 일하고 싶은 엔지니어**

- ✅ 기술력: Lambda + ECS + Terraform + Grafana (전문성)
- ✅ 인간성: GitOps + ChatOps = 팀워크 증명
- ✅ 완성도: 전체 플로우가 라이브로 작동
- ✅ 재미: 인터랙티브한 ChatOps 경험

**이 전략으로 1등을 차지합니다! 🏆**

