# 🎬 Mac Native Video Re-encoding Project (Gradio)

이 프로젝트는 모든 동영상 파일(MKV, AVI, 비표준 MP4 등)을 macOS의 **QuickLook(미리보기)**, **QuickTime Player**, 그리고 **Trim(다듬기)** 기능에 완벽하게 호환되도록 재인코딩하는 도구입니다.

## 🎯 프로젝트 목표
- macOS 시스템에서 별도의 코덱 설치 없이 영상 미리보기 및 재생 지원.
- 스페이스바(QuickLook)를 통한 즉각적인 영상 다듬기(Trim) 기능 활성화.
- 블랙박스, 구형 기기 영상 등 비표준 인덱스 및 색상 포맷 문제 해결.

## 🛠 기술 스택
- **Language:** Python 3.14 (Virtual Environment)
- **Library:** 
  - `gradio`: 사용자 친화적인 웹 기반 UI 제공.
  - `ffmpeg-python`: FFmpeg 엔진을 파이썬에서 제어.
- **Engine:** FFmpeg (Apple Silicon 가속 지원 확인)

## ⚙️ 주요 변환 로직 (FFmpeg 설정)
macOS 네이티브 환경 최적화를 위해 다음 설정을 강제합니다:

1.  **비디오 코덱 (`vcodec='h264_videotoolbox'`):** macOS 전용 하드웨어 가속 인코더를 사용하여 초고속 변환 지원. (기본 H.264 대비 수 배 이상 빠름)
2.  **색상 표준 (`pix_fmt='yuv420p'`):** macOS QuickLook 및 Apple 기기 재생을 위한 필수 표준 픽셀 포맷.
3.  **오디오 표준 (`acodec='aac'`):** 표준 AAC 오디오 스트림 생성 (192k 비트레이트).
4.  **인덱스 최적화 (`movflags='faststart'`):** MOOV 원자(atom)를 파일 시작 부분으로 이동시켜, 영상 전체를 읽기 전에도 즉각적인 재생 및 다듬기(Trim) 기능 활성화.
5.  **해상도 보정 (`vf='scale=...`):** H.264 인코딩 시 홀수 해상도로 인한 오류를 방지하기 위해 짝수 해상도로 자동 보정.

## 🚀 주요 개선 사항 (Pro 버전)
- **일괄 변환 기능:** 여러 파일을 한 번에 업로드하여 순차적으로 자동 변환.
- **처리 상태 알림:** 각 파일별 성공/실패 여부를 실시간으로 텍스트박스에 표시.
- **임시 파일 관리:** 변환 시 고유 타임스탬프를 부여하여 파일 충돌 방지.

## 🚀 실행 방법
가상환경이 활성화된 상태에서 다음 명령어를 입력합니다:

```bash
./.venv/bin/python app.py
```

실행 후 브라우저에서 `http://127.0.0.1:7860`으로 접속하여 영상을 업로드하고 변환할 수 있습니다.

## 📂 파일 구조
- `app.py`: Gradio UI 및 변환 로직 메인 스크립트.
- `.venv/`: 프로젝트 전용 파이썬 가상환경.
- `README.md`: 프로젝트 개요 및 배경 지식.
- `IMPLEMENTATION_GUIDE.md`: 현재 작업 내용 정리 (본 파일).
