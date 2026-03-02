# 🎬 바이브코딩 스터디 기록 - Re.encoding_to_mac

### 1. 이번 주 활동 한 줄 요약
Mac 퀵룩(QuickLook) 및 다듬기(Trim) 기능에 최적화된 동영상 재인코딩 도구 개발.

### 2. 프로젝트 핵심 내용
- **Mac 표준 최적화:** `yuv420p` 픽셀 포맷과 `movflags=faststart`를 적용하여 Mac 네이티브 환경에서 즉시 미리보기 및 편집이 가능하도록 변환.
- **Gradio 기반 UI:** 비전문가도 드래그 앤 드롭으로 쉽게 사용할 수 있는 웹 인터페이스 제공.

### 3. 재현 가능 가이드
- **실행 단계:**
  1. `brew install ffmpeg` 설치.
  2. `pip install gradio ffmpeg-python`.
  3. `python app.py` 실행 후 영상 업로드.
- **핵심 코드:** `ffmpeg.output` 내 `vcodec='libx264'`, `pix_fmt='yuv420p'`, `movflags='faststart'` 설정.

### 4. 다음 주 목표 (Action Item)
- [ ] `h264_videotoolbox`를 활용한 Mac 하드웨어 가속 인코딩 연동.
- [ ] 여러 파일을 한 번에 변환할 수 있는 일괄 처리(Batch) 기능 추가.
