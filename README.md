Web Media Downloader (yt‑dlp GUI)
A fast, simple, and powerful GUI for yt‑dlp, supporting 1500+ websites.
Download audio, video, playlists, and more — without touching the command line.

✨ Features
✔️ Download audio (MP3), best video + audio, video‑only, or best audio without conversion

✔️ Built‑in filename template builder (Title, Uploader, Date, ID, Playlist Index)

✔️ Metadata embedding (thumbnail, metadata, subtitles when available)

✔️ Quality selector (best, 1080p, 720p, 480p, 360p)

✔️ Supports multiple URLs (one per line or comma‑separated)

✔️ Live progress display (percent, speed, ETA)

✔️ Cancel downloads safely

✔️ Auto‑detects and handles playlists

✔️ Clean, responsive Tkinter GUI

✔️ Works with 1500+ sites supported by yt‑dlp

📥 Installation
1. Install Python
Download Python 3.10+ from:
https://www.python.org/downloads/

Make sure to check “Add Python to PATH” during installation.

2. Install yt‑dlp
Open Command Prompt and run:

Code
pip install -U yt-dlp

3. Install FFmpeg (required for MP3 + merging)
Download FFmpeg from:
https://www.gyan.dev/ffmpeg/builds/

Extract it, then add the bin folder to your Windows PATH.

4. Run the App
Download or clone this repository:

You can rename to a .pyw file for a one click GUI 

If you are stuck like I once did. ask an AI or youtube on how to add things to path.


🧠 How It Works
This GUI wraps yt‑dlp and exposes the most useful features:

Builds a filename template automatically based on checkboxes

Maps friendly download modes to yt‑dlp format strings

Uses FFmpeg post‑processors for MP3 extraction

Embeds metadata, thumbnails, and subtitles when available

Runs downloads in a background thread to keep the UI responsive

Provides real‑time progress updates via yt‑dlp hooks



📄 License
MIT License
(Free and do whatever you want)

👤 Author
SigmaSonix Labs  

Built with Python + yt‑dlp
