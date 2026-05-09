# MAG AI Video Persona Swap

**Professional 100% Local AI Face + Body Swap App**

Built by **Mohammed Amine Goumri** – Data Analyst & BI Developer

![MAG Logo](https://github.com/mohammedaminegoumri/mag-ai-video-persona-swap/blob/main/assets/mag-logo.png)

## Features
- High-quality **face swap** using **InsightFace** (inswapper_128)
- Works completely **locally** – no APIs, no costs, no data leaving your machine
- Swap any face onto any video while preserving pose, lighting and motion
- Clean, professional MAG branding
- Progress bar and real-time feedback
- Easy one-click download of swapped video

## Quick Start (Local)

```bash
# 1. Clone the repo
git clone https://github.com/mohammedaminegoumri/mag-ai-video-persona-swap.git
cd mag-ai-video-persona-swap

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run streamlit_app.py
```

**First run** will automatically download the InsightFace models (~450 MB).

## Requirements
- Python 3.10+
- Recommended: NVIDIA GPU + CUDA for faster processing

## Tips for Best Results
- Use a **clear, front-facing, well-lit** photo as source face
- Start with short videos (10–30 seconds)
- For best quality, run on a machine with GPU

## Tech Stack
- **InsightFace** – State-of-the-art face swapping
- **OpenCV** (headless) + **MoviePy** – Video processing
- **Streamlit** – Beautiful web UI
- **MediaPipe** – Face landmarks

## MAG Brand
Empowering Decisions Through **Intelligent Data**

---

Made with ❤️ by Mohammed Amine Goumri

