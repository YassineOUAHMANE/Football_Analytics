import streamlit as st
import tempfile
import subprocess
import os

st.set_page_config(page_title="Soccer Analyzer", layout="wide")
st.title("⚽ Soccer Match Analyzer")

with st.sidebar:
    st.header("Configuration")
    enable_passes = st.checkbox("Enable pass detection", value=True)
    enable_possession = st.checkbox("Enable possession tracking", value=False)
    uploaded_file = st.file_uploader("Upload video", type=["mp4"])
    model_file = st.file_uploader("Upload ball detection model (.pt)", type=["pt"])

if uploaded_file and model_file:
    # Save uploaded files to temp
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
        tmp_video.write(uploaded_file.read())
        video_path = tmp_video.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pt") as tmp_model:
        tmp_model.write(model_file.read())
        model_path = tmp_model.name

    # Build command to run run.py
    command = ["python", "run.py", "--video", video_path, "--model", model_path]
    if enable_passes:
        command.append("--passes")
    if enable_possession:
        command.append("--possession")

    st.write("🚀 Processing video, please wait...")

    # Call run.py
    try:
        subprocess.run(command, check=True)
        output_path = "videos/output.mp4"  # or wherever run.py saves it
        st.success("✅ Video processing complete!")

        # Download processed video
        with open(output_path, "rb") as f:
            st.download_button("📥 Download result video", f, file_name="processed_video.mp4")
    except subprocess.CalledProcessError as e:
        st.error("❌ Failed to process the video.")
        st.error(str(e))
