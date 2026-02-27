import gradio as gr
import ffmpeg
import os
import tempfile

def universal_mac_converter(input_file):
    if input_file is None:
        return None
    
    # Get the original filename and extension
    input_path = input_file.name
    base_name = os.path.basename(input_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    
    # Create output path in a temporary directory
    output_path = os.path.join(tempfile.gettempdir(), f"mac_ready_{file_name_without_ext}.mp4")

    try:
        # Re-encode video to Mac-standard format
        (
            ffmpeg
            .input(input_path)
            .output(output_path, 
                    vcodec='libx264',    # Widely compatible video codec
                    pix_fmt='yuv420p',   # Essential pixel format for Mac QuickLook
                    acodec='aac',        # Mac standard audio codec
                    audio_bitrate='192k',
                    movflags='faststart', # Move MOOV atom to the beginning for instant playback/trimming
                    vf='scale=trunc(iw/2)*2:trunc(ih/2)*2' # Ensure even dimensions for libx264
            )
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return output_path
    except ffmpeg.Error as e:
        error_message = e.stderr.decode() if e.stderr else str(e)
        return f"Error during conversion: {error_message}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🎬 Universal Mac Video Fixer")
    gr.Markdown("Convert any video to a standard MP4 format that supports **Mac QuickLook & Trim**.")
    
    with gr.Row():
        file_input = gr.File(label="Upload Video (MKV, AVI, MP4, etc.)")
    
    convert_btn = gr.Button("Convert to Mac Standard Format", variant="primary")
    
    with gr.Row():
        file_output = gr.File(label="Download Converted File")

    convert_btn.click(universal_mac_converter, inputs=file_input, outputs=file_output)

if __name__ == "__main__":
    demo.launch()
