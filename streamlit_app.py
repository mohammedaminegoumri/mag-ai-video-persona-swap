import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
from moviepy.editor import VideoFileClip
import mediapipe as mp
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_model_dir
import torch

st.set_page_config(page_title="MAG AI Video Persona Swap", page_icon="🔄", layout="wide")

# ===================== MAG BRANDING =====================
st.markdown("""
<style>
    .stApp { background-color: #0A2540; color: #ffffff; }
    .stButton>button { background-color: #00C4B4; color: #0A2540; font-weight: bold; }
    .header { color: #00C4B4; }
</style>
""", unsafe_allow_html=True)

st.title("🔄 MAG AI Video Persona Swap")
st.subheader("Face + Body Swap with AI-Generated Personas")
st.caption("**Empowering Decisions Through Intelligent Data** — Mohammed Amine Goumri")

st.markdown("**100% Local • InsightFace Powered • Fully Yours**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Local Settings")
    st.success("✅ Running completely on your machine")
    st.info("InsightFace is now used for professional-grade face swap")
    device = st.selectbox("Device", ["cpu", "cuda"] if torch.cuda.is_available() else ["cpu"])

# ===================== INSIGHTFACE INIT =====================
@st.cache_resource
def load_insightface_models():
    app = FaceAnalysis(name='buffalo_l', providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    app.prepare(ctx_id=0 if device == 'cuda' else -1, det_size=(640, 640))
    swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=True, download_path=get_model_dir())
    return app, swapper

try:
    app, swapper = load_insightface_models()
    st.success("✅ InsightFace models loaded")
except Exception as e:
    st.error(f"Model loading error: {e}")
    st.stop()

# ===================== UPLOADS =====================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Source Person (Face)")
    source_img = st.file_uploader("Upload source face image", type=["jpg", "png", "jpeg"])

with col2:
    st.subheader("Target Video (Body + Motion)")
    target_video = st.file_uploader("Upload target video (MP4)", type=["mp4"])

if source_img and target_video:
    if st.button("🚀 Start InsightFace Persona Swap", type="primary", use_container_width=True):
        with st.spinner("Processing video frame-by-frame with InsightFace... (this may take a while)"):
            # Save files
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as f:
                f.write(source_img.read())
                source_path = f.name
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as f:
                f.write(target_video.read())
                video_path = f.name

            source_face = cv2.imread(source_path)
            source_faces = app.get(source_face)
            if len(source_faces) == 0:
                st.error("No face detected in source image")
                os.unlink(source_path)
                os.unlink(video_path)
                st.stop()
            source_face = source_faces[0]

            cap = cv2.VideoCapture(video_path)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            output_path = "swapped_output.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            progress_bar = st.progress(0)
            frame_count = 0

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # InsightFace swap
                faces = app.get(frame)
                if len(faces) > 0:
                    frame = swapper.get(frame, faces[0], source_face)

                out.write(frame)
                frame_count += 1
                if frame_count % 10 == 0:
                    progress = min(int((frame_count / total_frames) * 100), 100)
                    progress_bar.progress(progress)

            cap.release()
            out.release()

            st.success("✅ InsightFace swap completed successfully!")
            st.video(output_path)

            # Download
            with open(output_path, "rb") as f:
                st.download_button("⬇️ Download Swapped Video", f, file_name="persona_swap_insightface.mp4", mime="video/mp4")

            # Cleanup
            for p in [source_path, video_path, output_path]:
                if os.path.exists(p):
                    os.unlink(p)

st.markdown("---")
st.info("**Pro Tip:** For even better results, use a high-quality source face image and short target video (under 30 seconds for testing).")
st.caption("100% Local • InsightFace + OpenCV • No APIs • Your own code")
