# MeetScribe 📝
Turn any meeting audio into Transcript + Tasks + Decisions + Follow-ups. 
No API keys. No cloud. Runs fully on your PC with Qwen2.5-7B.

### Features
- **Whisper Small**: Offline speech-to-text transcription
- **Qwen2.5-7B-Instruct**: Smart action extraction ~90% accuracy
- **Auto-Categorize**: Tasks, Decisions, Follow-ups with checkboxes
- **SQLite DB**: All meetings saved locally in meetings.db
- **Email Summary**: Copy-paste summary for attendees
- **100% Private**: Nothing leaves your computer

### Installation

1. **Clone and setup**

git clone <your-repo>
cd MeetScribe
python -m venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

2. *Install Dependencies*
pip install -r requirements.txt
Note: First run will auto-download Qwen2.5-7B ∼4.7GB and Whisper Small ∼500MB. Needs internet once.

3. *Install FFMPEG* - Required for .mp3 and .m4a files
Download: https://ffmpeg.org and add to PATH
Or just upload .wav files to skip this

### Usage
streamlit run app.py
1. Open http://localhost:8501
2. Upload a .wav/.mp3/.m4a meeting recording
3. Get Transcript + Actions instantly
4. All data auto-saves to meetings.db
5. Email Results

### System Requirements
| Minimum | Recommended
**RAM** | 8GB | 16GB
**GPU** | CPU Only ~25s per meeting | Nvidia 8GB+ VRAM ~5s
**Disk** | 10GB Free | 10GB Free
**OS** | Windows 10+ / Mac / Linux | Windows 10+ / Mac / Linux

### Privacy
Everything runs 100% locally. No data is sent to OpenAI, Google, or any cloud service.

### Troubleshooting
*Error: torch CUDA out of memory* 
Change `device_map="auto"` to `device_map="cpu"` in app.py to force CPU

*Error: FFMPEG not found*
Install ffmpeg or upload .wav files only

*Qwen is slow on first run*
Normal. It's downloading 4.7GB. After that it loads from cache.

*JSON Parse Error*
Qwen usually returns clean JSON. If it fails, check the transcript length > 20 chars

---
Built using Qwen2.5-7B-Instruct
