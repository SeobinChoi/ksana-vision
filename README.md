# 🤖 BLIP Camera Captioning System

실시간 카메라 피드를 BLIP AI 모델로 분석하여 이미지 캡션을 생성하는 시스템입니다.

## ✨ 주요 기능

- **실시간 이미지 캡션 생성**: BLIP/BLIP-2 모델 사용
- **듀얼 스크린 디스플레이**: 카메라 피드 + 캡션 텍스트
- **중국 고전 문서 스타일**: 수직 텍스트 레이아웃
- **2K 해상도 지원**: 2560x1440 고해상도 디스플레이
- **커스텀 폰트**: Acumin Variable Concept 폰트 사용
- **FIFO 캡션 관리**: 자동 캡션 순환 및 관리

## 🎨 디스플레이 특징

- **검은 배경**에 **흰 글자**
- **공백 → 하이픈** 자동 변환
- **오른쪽에서 왼쪽** 컬럼 배치 (중국 고전 문서 스타일)
- **새 캡션**이 **오른쪽**에 추가
- **화면 가득 차면** **왼쪽부터 자동 삭제**

## 🚀 설치 및 실행

### 1. 가상환경 활성화
```bash
source blip_env/bin/activate
```

### 2. 기본 실행 (듀얼 스크린)
```bash
python blip_camera_main.py --dual-screen --interval 3
```

### 3. 다른 실행 옵션
```bash
# BLIP-2 모델 사용 (더 정확하지만 느림)
python blip_camera_main.py --dual-screen --blip2 --interval 5

# 단일 카메라 창만 표시
python blip_camera_main.py --show-camera --interval 3

# 시스템 상태 확인
python blip_camera_main.py --status
```

## ⚙️ 설정 조정

`dual_screen_display.py` 파일의 상단에서 설정값을 조정할 수 있습니다:

```python
# ================================
# DISPLAY SETTINGS - 수정 가능한 설정들
# ================================
WINDOW_WIDTH = 2560        # 화면 너비 (2K: 2560, 4K: 3840)
WINDOW_HEIGHT = 1440       # 화면 높이 (2K: 1440, 4K: 2160)
FONT_SIZE = 24             # 글자 크기
FONT_PATH = "/Users/xavi/Desktop/real_code/2025ATC/assets/fonts/Acumin Variable Concept.ttf"

# 텍스트 레이아웃 설정
COLUMN_WIDTH = 10          # 컬럼 간격 (가로 간격)
CHAR_SPACING = 2           # 글자 간격 (세로 여백)
MAX_CAPTIONS = 200         # 최대 저장 캡션 수
```

### 설정 예시:
```python
# 4K 해상도로 변경
WINDOW_WIDTH = 3840
WINDOW_HEIGHT = 2160

# 글자 간격을 넓게
CHAR_SPACING = 5

# 컬럼 간격을 넓게
COLUMN_WIDTH = 50

# 글자 크기를 키우기
FONT_SIZE = 32
```

## 📁 프로젝트 구조

```
2025ATC/
├── blip_camera_main.py      # 메인 실행 파일
├── blip_model.py            # BLIP 모델 관리
├── camera_manager.py        # 카메라 관리
├── caption_engine.py        # 캡션 엔진 (메인 오케스트레이터)
├── dual_screen_display.py   # 듀얼 스크린 디스플레이
├── dual_screen_demo.py      # 데모 스크립트
├── requirements.txt         # 의존성 패키지
└── assets/
    └── fonts/
        └── Acumin Variable Concept.ttf  # 커스텀 폰트
```

## 🎮 사용법

### 기본 명령어
- `--dual-screen`: 듀얼 스크린 모드 활성화
- `--show-camera`: 단일 카메라 창 표시
- `--interval N`: 캡션 생성 간격 (초)
- `--blip2`: BLIP-2 모델 사용
- `--camera N`: 카메라 인덱스 (기본: 0)
- `--status`: 시스템 상태 확인

### 종료 방법
- 화면에서 `q` 키 누르기
- 터미널에서 `Ctrl+C` 누르기

## 🔧 기술 스택

- **Python 3.8+**
- **PyTorch**: AI 모델 실행
- **HuggingFace Transformers**: BLIP 모델
- **OpenCV**: 카메라 및 이미지 처리
- **PIL (Pillow)**: 이미지 및 폰트 렌더링
- **NumPy**: 수치 연산

## 📋 요구사항

- macOS (MPS 지원) 또는 CUDA 지원 GPU
- 카메라 권한
- 인터넷 연결 (초기 모델 다운로드)

## 🎯 특징

### AI 모델
- **BLIP**: 빠르고 가벼운 기본 모델
- **BLIP-2**: 더 정확하지만 큰 모델

### 디스플레이
- **수직 레이아웃**: 중국 고전 문서 스타일
- **실시간 업데이트**: 새 캡션이 오른쪽에 추가
- **자동 관리**: FIFO 방식으로 캡션 순환

### 성능
- **2K 해상도**: 고품질 디스플레이
- **최적화**: MPS/CUDA 자동 감지
- **메모리 관리**: 자동 캡션 정리

## 🐛 문제 해결

### 카메라가 열리지 않는 경우
```bash
# 다른 카메라 인덱스 시도
python blip_camera_main.py --dual-screen --camera 1
python blip_camera_main.py --dual-screen --camera 2
```

### 폰트가 로드되지 않는 경우
- `assets/fonts/Acumin Variable Concept.ttf` 파일 경로 확인
- 기본 폰트로 자동 대체됨

### 성능이 느린 경우
```bash
# BLIP-2 대신 BLIP 사용
python blip_camera_main.py --dual-screen --interval 5
```

## 📝 라이선스

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다.

## 🤝 기여

버그 리포트나 기능 요청은 이슈로 등록해주세요.

---

**🎉 즐거운 AI 캡션 생성 되세요!**