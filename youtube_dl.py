import tkinter as tk
from tkinter import *
from customtkinter import *
import os
from pytube import YouTube

class App:
    def __init__(self):
        self.app = Tk()
        self.setup_main_window()
        self.create_header_frame()
        self.create_bottom_frame()

    def setup_main_window(self):
        self.app.geometry("{}x{}+0+0".format(self.app.winfo_screenwidth(), self.app.winfo_screenheight()))

    def create_header_frame(self):
        header_frame = CTkFrame(master=self.app, fg_color="#F2F2F2", corner_radius=30)
        header_frame.pack(side="top", pady=20, padx=30)

        self.create_container_frame(header_frame)

    def create_container_frame(self, master):
        container_frame1 = CTkFrame(master=master, width=400, height=100, fg_color="white", corner_radius=30)
        container_frame1.pack(pady=20, padx=30)

        self.create_red_frame(container_frame1)
        self.create_white_frame(container_frame1)

    def create_red_frame(self, master):
        red_frame = CTkFrame(master=master, height=100, fg_color="#F50101", corner_radius=30)
        red_frame.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=5)

        yt_label1 = CTkLabel(master=red_frame, text="YouTube", font=("Arial", 40), text_color="white")
        yt_label1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def create_white_frame(self, master):
        white_frame = CTkFrame(master=master, width=250, height=100, fg_color="white", corner_radius=30)
        white_frame.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=5)

        yt_label2 = CTkLabel(master=white_frame, text="Downloader", font=("Arial", 40), text_color="black")
        yt_label2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def create_bottom_frame(self):
        bottom_frame = CTkFrame(master=self.app, fg_color="white")
        bottom_frame.pack(side="bottom", fill="both", expand=True)

        self.create_url_entry(bottom_frame)
        self.create_folder_entry(bottom_frame)
        self.create_options_menu(bottom_frame)
        self.create_download_button(bottom_frame)

    def create_url_entry(self, master):
        self.url_entry = CTkEntry(
            master, 
            width=900, 
            height=74, 
            corner_radius=50, 
            font=("Arial", 30),
            placeholder_text="Video URL"
        )
        self.url_entry.pack(pady=30, padx=30)

    def create_folder_entry(self, master):
        self.folder_entry = CTkEntry(
            master, 
            width=900, 
            height=74,
            corner_radius=50, 
            font=("Arial", 30),
            placeholder_text="Folder Directory"
        )
        self.folder_entry.pack(pady=(0, 30), padx=30)

    def option_menu_callback(self, choice):
        link = self.url_entry.get()
        destination = self.folder_entry.get()
        audio_only = choice == ".mp3 (audio format)"
        
        if link and destination:
            try:
                title = self.download_youtube_video(link, destination, audio_only)
                print(f"Downloaded: {title}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Please provide both the video URL and the destination folder.")

    def create_options_menu(self, master):
        self.options = CTkOptionMenu(
            master=master,
            width=900, 
            height=56, 
            corner_radius=15,
            font=("Arial", 30),
            fg_color="#F9F9FA",
            button_color="#F9F9FA",
            text_color="#9BA0A5",
            button_hover_color="#C0BDBD",
            dropdown_font=("Arial", 30),
            state="normal",
            values=[".mp3 (audio format)", ".mp4 (video format)"],
            command=self.option_menu_callback
        )
        self.options.pack(pady=(0, 30), padx=30)

    def download_button_pressed(self):
        choice = self.options.get()
        self.option_menu_callback(choice)

    def create_download_button(self, master):
        button = CTkButton(
            master,
            width=338, 
            height=85, 
            corner_radius=15, 
            text="Download", 
            fg_color="#F50101", 
            font=("Arial", 30),
            hover_color="#D61D1D",
            command=self.download_button_pressed
        )
        button.pack(padx=30)

    def download_youtube_video(self, link, destination, audio_only=False):
        """Downloads a YouTube video to the specified destination directory.

        Args:
            link: The YouTube video URL.
            destination: The destination directory.
            audio_only: Whether to download the audio only.

        Returns:
            The title of the downloaded video.
        """

        yt = YouTube(link)

        if audio_only:
            video = yt.streams.filter(only_audio=True).first()
        else:
            video = yt.streams.get_highest_resolution()

        out_file = video.download(output_path=destination)

        if audio_only:
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)

        return yt.title

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
