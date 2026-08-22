Web Media Downloader (yt‑dlp GUI)

A fast, simple, and powerful GUI for yt‑dlp, supporting 1500+ websites.
Download audio, video, playlists, and more — without touching the command line.

✨ Features
✔️ Download audio (MP3), best video + audio, video‑only, or best audio without conversion

✔️ Built‑in filename template builder (Title, Uploader, Date, ID, Playlist Index)

✔️ Metadata embedding (thumbnail, metadata, subtitles when available)

✔️ Optional browser cookies or cookies.txt support for 403 / sign-in issues

✔️ YouTube fallback client selector for stubborn 403 errors

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

Code: 
pip install -U yt-dlp

3. Install FFmpeg (required for MP3 + merging)
   
Download FFmpeg from:
https://www.gyan.dev/ffmpeg/builds/

Extract it, then add the bin folder to your Windows PATH.

4. Run the App
Download or clone this repository:

You can rename to a .pyw file for a one click GUI 

If you are stuck like I once did. ask an AI or youtube on how to add things to path.

🍪 Fixing Cookie / HTTP 403 Errors

Some sites, especially YouTube, may block anonymous downloads or require cookies
from a signed-in browser session.

Try these in order:

1. Update yt-dlp:

Code:
pip install -U yt-dlp

2. Restart the app.

3. In the app, tick "Use cookies from browser" and choose the browser where you
   are already signed in.

4. If that fails because the browser cookie database is locked, close the browser
   and try again.

5. If you run the app on a different machine than your browser, export a
   cookies.txt file from the browser machine and select that file in the app.

6. Try the YouTube fallback dropdown:

   - Start with Auto
   - Try Default + web embedded for cookie/sign-in problems
   - Try Web embedded only if the first fallback still gives 403

Note: only download content you have the right to access and keep.


🧠 How It Works
This GUI wraps yt‑dlp and exposes the most useful features:

Builds a filename template automatically based on checkboxes

Maps friendly download modes to yt‑dlp format strings

Uses FFmpeg post‑processors for MP3 extraction

Embeds metadata, thumbnails, and subtitles when available

Can pass browser cookies or a cookies.txt file to yt-dlp

Can switch YouTube player clients when a site-side 403 workaround changes

Runs downloads in a background thread to keep the UI responsive

Provides real‑time progress updates via yt‑dlp hooks

I don't intent to make an EXE file for this. its easier to update the script. 


📄 License
MIT License
(Free and do whatever you want)

👤 Author
SigmaSonixStudios

Built with Python + yt‑dlp
