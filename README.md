# 🎬 Re.encoding_to_mac

> **모든 영상을 Mac 네이티브 환경(QuickLook, QuickTime)에 최적화된 포맷으로 재인코딩하는 도구입니다.**

이 프로젝트는 Mac에서 영상 미리보기(스페이스바)를 통한 '다듬기(Trim)' 기능이 작동하지 않거나, 특정 영상이 재생되지 않는 문제를 해결하기 위해 시작되었습니다.

---

## 🧐 왜 이 프로젝트가 필요한가요? (Study Topics)

많은 영상 파일(특히 블랙박스, 구형 캠코더, 오픈소스 컨테이너)이 Mac에서 제대로 작동하지 않는 이유는 다음과 같습니다.

1. **비표준 인덱스:** 영상의 재생 정보(MOOV)가 파일 끝에 있어 퀵타임이 즉시 읽지 못함.
2. **색상 포맷 불일치:** Mac 시스템이 선호하는 `yuv420p`가 아닌 다른 방식의 픽셀 포맷 사용.
3. **컨테이너 호환성:** `mkv`, `avi` 등 Mac OS가 기본적으로 지원하지 않는 포맷.

이 도구는 **FFmpeg**을 활용하여 위 문제들을 해결하고, Mac 하드웨어 가속에 최적화된 표준 MP4를 생성합니다.

## 🛠 주요 기술 스택
- **Language:** Python 3.14 (Virtual Environment)
- **Engine:** FFmpeg with `h264_videotoolbox` (Hardware Acceleration)
- **UI:** Gradio (Web-based Interface)

## 🚀 주요 기능
- **초고속 하드웨어 가속:** Mac의 미디어 엔진을 사용하여 초당 수백 프레임의 변환 속도 제공.
- **Mac 표준 최적화:** `yuv420p` 픽셀 포맷 및 `faststart` 인덱싱 자동 적용.
- **일괄 변환(Batch Processing):** 여러 파일을 동시에 드래그 앤 드롭하여 한 번에 변환 가능.

## 🚀 설치 및 실행 방법

### 1. FFmpeg 설치 (필수)
```bash
brew install ffmpeg


import gradio as gr
import ffmpeg
import os
import tempfile

def universal_mac_converter(input_file):
    if input_file is None:
        return None
    
    output_path = os.path.join(tempfile.gettempdir(), f"mac_ready_{os.path.basename(input_file.name)}")
    if not output_path.endswith('.mp4'):
        output_path = os.path.splitext(output_path)[0] + ".mp4"

    try:
        # 모든 영상을 Mac 표준으로 강제 재인코딩
        (
            ffmpeg
            .input(input_file.name)
            .output(output_path, 
                    vcodec='libx264',    # 가장 범용적인 비디오 코덱
                    pix_fmt='yuv420p',   # Mac 미리보기 필수 픽셀 포맷
                    acodec='aac',        # Mac 표준 오디오 코덱
                    audio_bitrate='192k',
                    movflags='faststart', # 즉시 다듬기 가능하게 인덱스 이동
                    vf='scale=trunc(iw/2)*2:trunc(ih/2)*2' # 홀수 해상도 방지
            )
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return output_path
    except ffmpeg.Error as e:
        return f"Error: {e.stderr.decode()}"

# Gradio UI 개선
with gr.Blocks() as demo:
    gr.Markdown("# 🎬 Universal Mac Video Fixer")
    gr.Markdown("어떤 영상이든 **Mac QuickLook & Trim**이 가능한 표준 MP4로 변환합니다.")
    
    file_input = gr.File(label="영상 파일 업로드 (MKV, AVI, MP4 등)")
    convert_btn = gr.Button("Mac 표준 포맷으로 변환")
    file_output = gr.File(label="변환된 파일 다운로드")

    convert_btn.click(universal_mac_converter, inputs=file_input, outputs=file_output)

demo.launch()