import gradio as gr
import ffmpeg
import os
import tempfile
import time

def convert_to_mac_standard(input_files):
    if not input_files:
        return None, "Please upload at least one video file."
    
    output_files = []
    status_messages = []

    # Ensure it's a list even if only one file is uploaded
    if not isinstance(input_files, list):
        input_files = [input_files]

    for i, input_file in enumerate(input_files):
        input_path = input_file.name
        base_name = os.path.basename(input_path)
        file_name_without_ext = os.path.splitext(base_name)[0]
        
        # Output to a temporary directory
        output_path = os.path.join(tempfile.gettempdir(), f"mac_ready_{file_name_without_ext}_{int(time.time())}.mp4")

        try:
            # Re-encode with hardware acceleration (VideoToolbox)
            # Use h264_videotoolbox for high speed on Apple Silicon/Intel Mac
            # Note: pix_fmt='yuv420p' is critical for Mac QuickLook/Trim
            (
                ffmpeg
                .input(input_path)
                .output(output_path, 
                        vcodec='h264_videotoolbox', # Apple Hardware Acceleration
                        b='5M',                     # Target bitrate for quality
                        pix_fmt='yuv420p',           # Standard Mac color format
                        acodec='aac',                # Apple standard audio
                        audio_bitrate='192k',
                        movflags='faststart',        # Instant playback & Trimming support
                        vf='scale=trunc(iw/2)*2:trunc(ih/2)*2' # Fix odd dimensions
                )
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            output_files.append(output_path)
            status_messages.append(f"✅ Success: {base_name}")
        except ffmpeg.Error as e:
            error_details = e.stderr.decode() if e.stderr else str(e)
            status_messages.append(f"❌ Failed: {base_name} - {error_details}")
        except Exception as e:
            status_messages.append(f"⚠️ Error: {str(e)}")

    return output_files, "\n".join(status_messages)

# Gradio UI with modern layout
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🎬 Universal Mac Video Fixer (Pro)
    ### 모든 영상을 Mac 전용 표준 MP4로 변환합니다.
    
    **주요 특징:**
    - **Mac 하드웨어 가속:** `h264_videotoolbox`를 사용하여 초고속 변환.
    - **QuickLook & Trim 완벽 지원:** `faststart` 인덱싱 및 `yuv420p` 색상 포맷 적용.
    - **일괄 변환:** 여러 파일을 한 번에 업로드하여 처리할 수 있습니다.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(
                label="영상 업로드 (MKV, AVI, MOV, MP4 등)", 
                file_count="multiple",
                type="filepath"
            )
            convert_btn = gr.Button("변환 시작 (Mac 최적화)", variant="primary", size="lg")
            
        with gr.Column(scale=1):
            status_output = gr.Textbox(label="처리 상태", lines=5, interactive=False)
            file_output = gr.File(label="다운로드 (변환된 파일)")

    # Action binding
    convert_btn.click(
        fn=convert_to_mac_standard, 
        inputs=file_input, 
        outputs=[file_output, status_output]
    )

    gr.Markdown("""
    ---
    *참고: 변환된 파일은 Mac의 스페이스바(미리보기)를 통해 즉시 다듬기(Trim) 기능을 사용할 수 있습니다.*
    """)

if __name__ == "__main__":
    demo.launch()
