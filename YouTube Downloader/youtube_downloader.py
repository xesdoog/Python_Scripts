import os
import tkinter
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label, OptionMenu
from pathlib import Path
from pytube import YouTube
from threading import Thread
from time import sleep


OUTPUT_PATH   = Path(__file__).parent
ASSETS_PATH   = OUTPUT_PATH / Path(r"assets")
DOWNLOAD_PATH = './Downloads'
RESOLUTIONS   = ["Resolution",
                 "144p", 
                 "240p",
                 "360p",
                 "480p",
                 "720p",
                 "1080p",
                 "1440p",
                 "2160p",
                 ]
                 

window       = Tk()
entryContent = tkinter.StringVar()
titleVar     = tkinter.StringVar()
resVar       = tkinter.StringVar()
feedbackVar  = tkinter.StringVar()
resVar.set(RESOLUTIONS[0])


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def grab_title():
    global title
    try:
        link = entryContent.get()
        title = YouTube(link).title
        if title != None:
            titleVar.set("Video:  " + title)
    
    except Exception:
        if link == "":
            titleVar.set("")
        else:
            titleVar.set("Please enter a valid YouTube link.")


def title_thread():
    Thread(target = grab_title, daemon = True).start()


def on_enter(widget):
    global link
    link = entryContent.get()
    title_thread()


def set_res(resolution: str):
    global user_res
    user_res = resolution
    link = entryContent.get()
    try:

        if link != None:

            if RESOLUTIONS.index(user_res) > 5:
                feedbackVar.set(
                    "WARNING!\nResolutions higher than 720p will download the video without sound."
                    )

            else:
                feedbackVar.set("")

    except Exception:
        feedbackVar.set("")


def in_progress(stream, chunk, bytes_remaining):
    feedbackVar.set("Downloading.")
    sleep(0.5)
    feedbackVar.set("Downloading..")
    sleep(0.5)
    feedbackVar.set("Downloading...")
    sleep(0.5)
    feedbackVar.set("Downloading ..")
    sleep(0.5)
    feedbackVar.set("Downloading  .")
    sleep(0.5)
    feedbackVar.set("Downloading")
    sleep(0.5)


def on_complete(stream, file_path):
    feedbackVar.set("Done!")
    sleep(3)
    feedbackVar.set("")

def download_func():
    try:
        title_thread()
        link = entryContent.get()
        yt = YouTube(link, on_progress_callback = in_progress, on_complete_callback = on_complete)

        if RESOLUTIONS.index(user_res) != 0:
            print('yes')
            stream = yt.streams.filter(res = user_res, file_extension = 'mp4', progressive = True).first()
        else:
            stream = yt.streams.get_highest_resolution(progressive = True)

        if stream == None:
            stream = yt.streams.get_highest_resolution()

        if not os.path.exists(DOWNLOAD_PATH):
            os.makedirs(DOWNLOAD_PATH)
        
        stream.download(DOWNLOAD_PATH)
    except Exception as e:
        feedbackVar.set("An error has occured! Please try again in a few seconds.")
        print(e)
        sleep(3)
        feedbackVar.set("")


def download_thread():
    Thread(target = download_func, daemon = True).start()


window.geometry("480x300")
window.configure(bg = "#FFFFFF")
window.title("YouTube Downloader")
window.iconbitmap(relative_to_assets('ytd_icon.ico'))


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 300,
    width = 480,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

banner = PhotoImage(
    file = relative_to_assets("banner.png"))
image_2 = canvas.create_image(
    240.0,
    43.0,
    image = banner
)

yt_logo = PhotoImage(
    file = relative_to_assets("yt_logo.png"))
image_3 = canvas.create_image(
    41.0,
    35.0,
    image = yt_logo
)

canvas.create_text(
    67.0,
    21.0,
    anchor = "nw",
    text = "YouTube Downloader",
    fill = "#FFFFFF",
    font = ("Roboto", 25 * -1)
)

searchBar = Entry(
    bd = 0,
    bg = "#DBD8D8",
    fg = "#000716",
    highlightthickness = 0,
    textvariable = entryContent
)

searchBar.place(
    x = 22.0,
    y = 110.0,
    width = 410.0,
    height = 35.0
)
searchBar.bind('<Return>', on_enter)

searchBar_img = PhotoImage(
    file=relative_to_assets("searchBar.png"))
entry_bg_1 = canvas.create_image(
    228.0,
    126.0,
    image = searchBar_img
)

vid_title = Label(master = window,
                  textvariable = titleVar,
                  ).place(
                x = 20.0,
                y = 160.0)

link_icon = PhotoImage(
    file=relative_to_assets("link_icon.png"))
image_1 = canvas.create_image(
    459.0,
    126.0,
    image = link_icon
)

button_image_1 = PhotoImage(
    file=relative_to_assets("download_btn.png"))

download_btn = Button(
    image=button_image_1,
    borderwidth = 0,
    highlightthickness = 0,
    command = download_thread,
    relief = "flat"
)
download_btn.place(
    x = 100.0,
    y = 202.0,
    width = 139.0,
    height = 56.0
)

resMenu = OptionMenu(window,
                     resVar,
                     *RESOLUTIONS,
                     command = set_res
                     ).place(x = 270.0,
                             y = 210.0
                             )

feedback_text = Label(master = window,
                  textvariable = feedbackVar,
                  ).place(
                x = 20.0,
                y = 260.0)

window.resizable(False, False)
window.mainloop()