# This Youtube Video Downloader have A Advance Progress Bar with Speed , Time , Size And Stable Speed Download (✅)
import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
import ttkthemes
import os
import threading
import time

class CustomProgressBar:
    def __init__(self, root):
        self.root = root
        self.progress = tk.DoubleVar()

        self.progress_window = tk.Toplevel(root)
        self.progress_window.title("Download Progress")
        self.progress_window.geometry("400x150")

        self.progress_label = tk.Label(self.progress_window, text="Progress: 0%")
        self.progress_label.pack(pady=10)

        self.progress_bar = ttk.Progressbar(self.progress_window, orient="horizontal", length=200, mode="determinate", variable=self.progress)
        self.progress_bar.pack(pady=20)

        self.speed_label = tk.Label(self.progress_window, text="Speed: 0 B/s")
        self.speed_label.pack(pady=5)

        self.remaining_label = tk.Label(self.progress_window, text="Remaining Time: --:--:--")
        self.remaining_label.pack(pady=5)

        self.remaining_size_label = tk.Label(self.progress_window, text="Remaining Size: 0 MB")
        self.remaining_size_label.pack(pady=5)

    def update_progress(self, bytes_downloaded, total_size, start_time):
        percentage = (bytes_downloaded / total_size) * 100
        self.progress.set(percentage)
        self.progress_label.config(text=f"Progress: {percentage:.2f}%")

        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            speed_bytes = bytes_downloaded / elapsed_time
            speed_mb = speed_bytes / (1024 * 1024)
            self.speed_label.config(text=f"Speed: {speed_mb:.2f} MB/s")

            remaining_time = (total_size - bytes_downloaded) / speed_bytes
            minutes, seconds = divmod(remaining_time, 60)
            hours, minutes = divmod(minutes, 60)
            self.remaining_label.config(text=f"Remaining Time: {int(hours)}:{int(minutes)}:{int(seconds)}")

            remaining_size = total_size - bytes_downloaded
            remaining_size_mb = remaining_size / (1024 * 1024)
            self.remaining_size_label.config(text=f"Remaining Size: {remaining_size_mb:.2f} MB")

        self.progress_window.update_idletasks()

def download_video():
    url = entry.get()
    try:
        start_time = time.time()
        youtube = YouTube(url, on_progress_callback=lambda stream, chunk, bytes_remaining: progress_bar.update_progress(stream.filesize - bytes_remaining, stream.filesize, start_time))
        streams = youtube.streams.filter(adaptive=True, mime_type='video/webm')
        #* For 4k Use Webm Formate 
        #streams = youtube.streams.filter(adaptive=True, mime_type='video/webm')
        stream = None
        if resolution.get() == "4K":
            stream = next((s for s in streams if s.resolution == "2160p"), None)
        else:
            stream = next((s for s in streams if s.resolution == resolution.get()), None)
        if stream is None:
            messagebox.showerror("Error", "No stream available in the selected resolution")
            return

        # Get the video title and create a folder with the video's name in the "Downloads" folder
        video_title = youtube.title
        video_folder = os.path.join(os.path.expanduser("~/Downloads"), "Videos", video_title)
        os.makedirs(video_folder, exist_ok=True)

        # Create a custom progress bar
        global progress_bar
        progress_bar = CustomProgressBar(root)

        threading.Thread(target=download_thread, args=(stream, video_folder, video_title, stream.filesize, start_time, progress_bar)).start()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def download_audio():
    url = entry.get()
    try:
        start_time = time.time()
        youtube = YouTube(url, on_progress_callback=lambda stream, chunk, bytes_remaining: progress_bar.update_progress(stream.filesize - bytes_remaining, stream.filesize, start_time))
        audio_stream = youtube.streams.get_audio_only()

        # Get the video title and create a folder with the video's name in the "Downloads" folder
        audio_title = youtube.title
        audio_folder = os.path.join(os.path.expanduser("~/Downloads"), "Audios", audio_title)
        os.makedirs(audio_folder, exist_ok=True)

        # Create a custom progress bar
        global progress_bar
        progress_bar = CustomProgressBar(root)

        threading.Thread(target=download_thread, args=(audio_stream, audio_folder, audio_title, audio_stream.filesize, start_time, progress_bar)).start()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def download_thread(stream, folder, title, total_size, start_time, progress_bar):
    file_path = stream.download(folder)
    file_name = os.path.basename(file_path)

    messagebox.showinfo("Download Complete", f"{title} downloaded successfully as '{file_name}' in the folder '{folder}'")
    progress_bar.progress_window.destroy()

root = tk.Tk()

# Set the theme
style = ttkthemes.ThemedStyle(root)
style.set_theme("arc")  # Use the "arc" theme as a base for the custom style

# Configure the style to create a dark-looking GUI
style.configure("TButton", font=("Helvetica", 12), padding=10, relief="flat", borderwidth=0, compound="center")
style.map("TButton", foreground=[("active", "white"), ("pressed", "white"), ("!disabled", "black")], background=[("active", "#303030"), ("pressed", "#424242"), ("!disabled", "#212121")])
style.configure("TLabel", font=("Helvetica", 12), padding=10, relief="flat", borderwidth=0, compound="center")
style.map("TLabel", foreground=[("active", "white"), ("pressed", "white"), ("!disabled", "black")], background=[("active", "#303030"), ("pressed", "#424242"), ("!disabled", "#212121")])
style.configure("TEntry", font=("Helvetica", 12), padding=10, relief="flat", borderwidth=0)
style.map("TEntry", foreground=[("active", "white"), ("pressed", "white"), ("!disabled", "black")], background=[("active", "#303030"), ("pressed", "#424242"), ("!disabled", "#212121")], fieldbackground=[("active", "#303030"), ("pressed", "#424242"), ("!disabled", "#212121")])
style.configure("TOptionMenu", font=("Helvetica", 12), padding=10, relief="flat", borderwidth=0)
style.map("TOptionMenu", foreground=[("active", "white"), ("pressed", "white"), ("!disabled", "black")], background=[("active", "#303030"), ("pressed", "#424242"), ("!disabled", "#212121")])
style.configure("TProgressbar", thickness=10)
style.map("TProgressbar", foreground=[("active", "#303030"), ("pressed", "#424242"), ("!disabled", "#212121")], background=[("active", "white"), ("pressed", "white"), ("!disabled", "black")])

root.title("YouTube Video Downloader")
root.geometry("500x400")
root.configure(bg="#212121")  # Set the background color of the root window

label = tk.Label(root, text="Enter YouTube Video URL:")
label.pack(pady=20)

entry = tk.Entry(root, width=70)
entry.pack(pady=20)

resolution_label = tk.Label(root, text="Choose video resolution:")
resolution_label.pack(pady=20)

resolution = tk.StringVar(root)
resolution.set("720p")  # default resolution

resolution_menu = tk.OptionMenu(root, resolution, "144p", "240p", "360p", "480p", "720p", "1080p", "4K")
resolution_menu.pack(pady=20)

download_video_button = tk.Button(root, text="Download Video", command=download_video)
download_video_button.pack(pady=20)

download_audio_button = tk.Button(root, text="Download Audio", command=download_audio)
download_audio_button.pack(pady=20)

root.mainloop()
