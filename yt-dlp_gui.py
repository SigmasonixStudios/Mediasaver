# update yt_dlp if out of date


import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import yt_dlp
import threading
import os

class YTDLP_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Mdedia Downloader V260215")
        self.root.geometry("640x720")
        self.root.resizable(True, True)

        self.download_thread = None
        self.stop_event = threading.Event()

        # Metadata variables
        self.embed_metadata_var = tk.BooleanVar(value=True)
        self.embed_thumbnail_var = tk.BooleanVar(value=True)
        self.embed_subs_var = tk.BooleanVar(value=False)

        # Filename checkbox variables
        self.chk_title_var = tk.BooleanVar(value=True)
        self.chk_uploader_var = tk.BooleanVar(value=True)
        self.chk_date_var = tk.BooleanVar(value=False)
        self.chk_id_var = tk.BooleanVar(value=False)
        self.chk_playlist_idx_var = tk.BooleanVar(value=False)

        self.create_widgets()

        # Apply initial template from checkboxes
        self.update_template_from_checkboxes()

    def create_widgets(self):
        # ── URL(s) ───────────────────────────────────────────────
        tk.Label(self.root, text="Insert URL(s) insdie me here (one per line or comma) works with 1500+ sites:").pack(pady=(10, 2), anchor="w", padx=10)

        self.url_text = scrolledtext.ScrolledText(self.root, height=6, width=90, wrap=tk.WORD)
        self.url_text.pack(padx=10, pady=5)

        # ── Output Folder ────────────────────────────────────────
        frame_folder = tk.Frame(self.root)
        frame_folder.pack(fill="x", padx=10, pady=8)

        tk.Label(frame_folder, text="Save to folder:").pack(side="left")

        self.folder_var = tk.StringVar(value=os.path.expanduser("~/Desktop"))
        tk.Entry(frame_folder, textvariable=self.folder_var, width=60).pack(side="left", padx=8)

        tk.Button(frame_folder, text="Browse...", command=self.browse_folder).pack(side="left", padx=(8, 4))

        # New Clear URL button right beside Browse
        tk.Button(frame_folder, text="Clear URL", command=self.clear_url, width=10, bg="#e0e0e0").pack(side="left", padx=4)

        # ── Filename Template Section ────────────────────────────
        frame_name = tk.LabelFrame(self.root, text="Filename Template", padx=12, pady=10)
        frame_name.pack(fill="x", padx=10, pady=10)

        # Checkboxes - Row 1
        chk_row1 = tk.Frame(frame_name)
        chk_row1.pack(fill="x", pady=4)

        tk.Checkbutton(chk_row1, text="Title", variable=self.chk_title_var, command=self.update_template_from_checkboxes).pack(side="left", padx=12)
        tk.Checkbutton(chk_row1, text="Uploader / Artist", variable=self.chk_uploader_var, command=self.update_template_from_checkboxes).pack(side="left", padx=12)
        tk.Checkbutton(chk_row1, text="Video ID", variable=self.chk_id_var, command=self.update_template_from_checkboxes).pack(side="left", padx=12)

        # Checkboxes - Row 2
        chk_row2 = tk.Frame(frame_name)
        chk_row2.pack(fill="x", pady=4)

        tk.Checkbutton(chk_row2, text="Upload Date (YYYYMMDD)", variable=self.chk_date_var, command=self.update_template_from_checkboxes).pack(side="left", padx=12)
        tk.Checkbutton(chk_row2, text="Playlist Index (if playlist)", variable=self.chk_playlist_idx_var, command=self.update_template_from_checkboxes).pack(side="left", padx=12)

        # Template entry
        self.template_var = tk.StringVar()
        tk.Entry(frame_name, textvariable=self.template_var, width=70, font=("Consolas", 10)).pack(pady=8, fill="x")

        tk.Label(frame_name, text="Check boxes to build template or edit manually").pack(anchor="w", pady=2)

        # ── Download Mode (Dropdown) ─────────────────────────────
        frame_mode = tk.Frame(self.root)
        frame_mode.pack(fill="x", padx=10, pady=8)

        tk.Label(frame_mode, text="Download mode:").pack(side="left")
        self.mode_var = tk.StringVar(value="audio_mp3")
        mode_options = [
            "Audio only (MP3 ~320kbps)",
            "Best video + audio (merged)",
            "Best video only",
            "Audio best quality (no conversion)"
        ]
        self.mode_combo = ttk.Combobox(frame_mode, textvariable=self.mode_var, values=mode_options, state="readonly", width=35)
        self.mode_combo.pack(side="left", padx=10)
        self.mode_combo.bind("<<ComboboxSelected>>", self.toggle_options)

        # ── Video Quality Preference (Dropdown) ──────────────────
        frame_quality = tk.Frame(self.root)
        frame_quality.pack(fill="x", padx=10, pady=8)

        tk.Label(frame_quality, text="Video quality preference:").pack(side="left")
        self.quality_var = tk.StringVar(value="best")
        quality_options = ["best", "1080p", "720p", "480p", "360p"]
        self.quality_combo = ttk.Combobox(frame_quality, textvariable=self.quality_var, values=quality_options, state="readonly", width=15)
        self.quality_combo.pack(side="left", padx=10)

        # ── Metadata Options (Checkboxes) ────────────────────────
        frame_meta = tk.LabelFrame(self.root, text="Metadata & Embedding Options(If Available)", padx=10, pady=8)
        frame_meta.pack(fill="x", padx=10, pady=10)

        tk.Checkbutton(frame_meta, text="Embed metadata", variable=self.embed_metadata_var).pack(anchor="w")
        tk.Checkbutton(frame_meta, text="Embed thumbnail (cover art)", variable=self.embed_thumbnail_var).pack(anchor="w")
        tk.Checkbutton(frame_meta, text="Embed subtitles", variable=self.embed_subs_var).pack(anchor="w")

        # Initial state
        self.toggle_options(None)

        # ── Status & Progress ────────────────────────────────────
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self.root, textvariable=self.status_var, fg="blue", wraplength=750).pack(pady=12)

        self.progress_var = tk.StringVar(value="")
        tk.Label(self.root, textvariable=self.progress_var, font=("Arial", 10)).pack()

        # ── Buttons 
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        self.download_btn = tk.Button(btn_frame, text="Download", command=self.start_download, width=15, bg="#4CAF50", fg="white")
        self.download_btn.pack(side="left", padx=25)

        self.cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.stop_download, state="disabled", width=15, bg="#f44336", fg="white")
        self.cancel_btn.pack(side="left", padx=25)

        tk.Button(btn_frame, text="Quit", command=self.root.quit, width=10).pack(side="left", padx=25)
        tk.Button(btn_frame, text="Help", command=self.show_help_window, width=10, bg="#2196F3", fg="white").pack(side="left", padx=25)

    def clear_url(self):
        self.url_text.delete("1.0", tk.END)
        self.status_var.set("URL field cleared")

    def update_template_from_checkboxes(self):
        parts = []

        if self.chk_title_var.get():
            parts.append("%(title)s")
        if self.chk_uploader_var.get():
            parts.append("%(uploader)s")
        if self.chk_date_var.get():
            parts.append("%(upload_date)s")
        if self.chk_id_var.get():
            parts.append("%(id)s")
        if self.chk_playlist_idx_var.get():
            parts.append("%(playlist_index)s - ")

        if not parts:
            template = "%(title)s.%(ext)s"
        else:
            joined = " - ".join([p for p in parts if p]).strip(" - ")
            template = f"{joined}.%(ext)s"

        self.template_var.set(template)

    def toggle_options(self, event):
        mode_text = self.mode_var.get()
        is_video_mode = mode_text in ["Best video + audio (merged)", "Best video only"]

        if is_video_mode:
            self.quality_combo.config(state="readonly")
        else:
            self.quality_combo.config(state="disabled")
            self.quality_var.set("best")

        if mode_text.startswith("Audio"):
            self.embed_subs_var.set(False)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def progress_hook(self, d):
        if self.stop_event.is_set():
            raise yt_dlp.utils.DownloadCancelled("Download stopped")

        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '?%')
            speed = d.get('_speed_str', '?')
            eta = d.get('_eta_str', '?')
            self.progress_var.set(f"{percent}   {speed}   ETA: {eta}")
            self.root.update_idletasks()
        elif d['status'] == 'finished':
            self.progress_var.set("Download finished, now post-processing...")
        elif d['status'] == 'error':
            self.progress_var.set("Error occurred.")

    def start_download(self):
        urls_input = self.url_text.get("1.0", tk.END).strip()
        if not urls_input:
            self.status_var.set("Put least one URL inside me!")
            self.progress_var.set("")

            return

        urls = [u.strip() for u in urls_input.replace(',', '\n').splitlines() if u.strip()]

        outtmpl = os.path.join(self.folder_var.get(), self.template_var.get())

        mode_text = self.mode_var.get()
        mode_map = {
            "Audio only (MP3 ~320kbps)": "audio_mp3",
            "Best video + audio (merged)": "best_merged",
            "Best video only": "best_video",
            "Audio best quality (no conversion)": "audio_best"
        }
        mode = mode_map.get(mode_text, "audio_mp3")

        format_str = "bestvideo+bestaudio/best"
        postprocessors = []

        if mode == "audio_mp3":
            format_str = "bestaudio/best"
            postprocessors = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }]
        elif mode == "best_video":
            format_str = "bestvideo"
        elif mode == "audio_best":
            format_str = "bestaudio/best"

        if mode in ["best_merged", "best_video"] and self.quality_var.get() != "best":
            q = self.quality_var.get()
            height_map = {"1080p": 1080, "720p": 720, "480p": 480, "360p": 360}
            h = height_map.get(q, 1080)
            format_str = f"bestvideo[height<={h}]+bestaudio/best[height<={h}]"

        ydl_opts = {
            'format': format_str,
            'outtmpl': outtmpl,
            'progress_hooks': [self.progress_hook],
            'postprocessors': postprocessors,
            'continuedl': True,
            'quiet': False,
            'no_warnings': False,
        }

        if self.embed_metadata_var.get():
            ydl_opts['embedmetadata'] = True
        if self.embed_thumbnail_var.get():
            ydl_opts['embedthumbnail'] = True
        if self.embed_subs_var.get():
            ydl_opts['writesubtitles'] = True
            ydl_opts['embedsubtitles'] = True
            ydl_opts['subtitleslangs'] = ['all']

        self.status_var.set("Downloading...")
        self.download_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.progress_var.set("")
        self.stop_event.clear()

        def run_download():
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(urls)
                if not self.stop_event.is_set():
                    self.status_var.set("Download completed successfully!")
                    
            except yt_dlp.utils.DownloadCancelled:
                self.status_var.set("Download cancelled by user.")
            except Exception as e:
                self.status_var.set(f"Error: {str(e)}")
                
            finally:
                self.download_btn.config(state="normal")
                self.cancel_btn.config(state="disabled")
                self.progress_var.set("")

        self.download_thread = threading.Thread(target=run_download, daemon=True)
        self.download_thread.start()

    def stop_download(self):
        if self.download_thread and self.download_thread.is_alive():
            self.stop_event.set()
            self.status_var.set("Cancelling... (may take a moment)")
            self.cancel_btn.config(state="disabled")

    def show_help_window(self):
        help_win = tk.Toplevel(self.root)
        help_win.title("Help")
        help_win.geometry("580x520")
        help_win.resizable(False, False)
        help_win.transient(self.root)   # stays on top of main window
        help_win.grab_set()             # modal-like focus

        tk.Label(help_win, text="Troubleshooting", font=("Arial", 14, "bold")).pack(pady=10)

        text = scrolledtext.ScrolledText(help_win, wrap=tk.WORD, font=("Arial", 11), height=20, width=65)
        text.pack(padx=15, pady=10, fill="both", expand=True)

        help_message = """\
This downloader uses yt-dlp 

Work with over over 1500 webistes

Most problems happen because YouTube frequently changes its website.
When that happens, downloads fail with errors like:
• "Unable to extract uploader id"
• "Signature extraction failed"
• "HTTP Error 403"
• No formats available
• Or just "download failed"

you need to Update yt-dlp:

1. Open Command Prompt (search "cmd" in Windows Start menu)
2. Type this command and press Enter:

   pip install -U yt-dlp

   (or if that doesn't work, try:)
   python -m pip install -U yt-dlp

3. Wait until it says "Successfully installed..." or "Requirement already satisfied"
4. Close and restart this program (double-click your .bat or .pyw file again)

Other quick checks:
• Make sure ffmpeg is installed (needed for MP3 conversion and merging video+audio)
  → Download from: https://www.gyan.dev/ffmpeg/builds/
  → Extract and add the "bin" folder to your Windows PATH
• Try a different URL — some videos are age-restricted or private
• If still stuck: Copy the exact error from the status bar and search it + "yt-dlp" on Google

Enjoy downloading!
Made with yt-dlp — https://github.com/yt-dlp/yt-dlp

By SigmaSonix Labs
"""

        text.insert(tk.END, help_message)
        text.config(state="disabled")  # read-only

        tk.Button(help_win, text="Close", command=help_win.destroy, width=10).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = YTDLP_GUI(root)
    root.mainloop()