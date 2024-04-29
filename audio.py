import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
import ttkthemes
import os
import threading

def download_video():
    url = entry.get()
    thread = threading.Thread(target=download, args=(url,))
    thread.start()

def download(url):
    try:
        youtube = YouTube(url, on_progress_callback=progress_func)
        streams = youtube.streams.filter(only_audio=True)
        stream = streams.first()
        if stream is None:
            messagebox.showerror("Error", "No audio stream available")
            return
        progress_bar.pack(pady=20)
        root.update()  # Update the GUI to display the progress bar

        # Get the video title and create a folder with the video's name in the "Downloads" folder
        video_title = youtube.title
        video_folder = os.path.join(os.path.expanduser("~/Downloads"), video_title)
        os.makedirs(video_folder, exist_ok=True)

        # Save the downloaded file in the video's folder
        file_path = stream.download(video_folder)
        file_name = os.path.basename(file_path)

        progress_bar.pack_forget()
        messagebox.showinfo("Download Complete", f"Audio '{video_title}' downloaded successfully as '{file_name}' in the folder '{video_folder}'")
    except Exception as e:
        progress_bar.pack_forget()
        messagebox.showerror("Error", str(e))

def progress_func(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_var.set(percentage_of_completion)
    progress_bar['value'] = percentage_of_completion

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

download_button = tk.Button(root, text="Download Audio", command=download_video)
download_button.pack(pady=20)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate", variable=progress_var)

root.mainloop()
