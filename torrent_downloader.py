import time
import tkinter as tk
from tkinter import filedialog
import libtorrent as lt


chosen_dir = ""

def on_entry_click(event):
    """Event handler for the magnet URL entry box click event."""
    if magnet_url_box.get() == "Enter/Paste your Magnet URL here":
        magnet_url_box.delete(0, "end")
        magnet_url_box.configure(foreground="black")

def on_focusout(event):
    """Event handler for the magnet URL entry box focus out event."""
    if magnet_url_box.get() == "":
        magnet_url_box.insert(0, "Enter/Paste your Magnet URL here")
        magnet_url_box.configure(foreground="gray")

def select_directory():
    """Opens a directory selection dialog and sets the chosen directory."""
    global chosen_dir
    chosen_dir = filedialog.askdirectory()
    if chosen_dir:
        directory_label.configure(text="Choosen Directory: " + chosen_dir)
    return chosen_dir

def select_torrent():
    """Opens a file selection dialog for choosing a torrent file."""
    global chosen_dir
    chosen_torrent = filedialog.askopenfilename(filetypes=[("Torrent Files", "*.torrent")])
    if chosen_torrent:
        torrent_label.configure(text="Selected Torrent File: " + chosen_torrent)
        chosen_dir = select_directory()

def submit_value():
    """Starts the download process using the provided magnet URL or selected torrent file."""
    global chosen_dir
    if not chosen_dir:
        chosen_dir = select_directory()
        if not chosen_dir:
            return
    button.config(state="disabled")
    value = magnet_url_box.get()
    ses = lt.session()
    params = {
        'save_path': select_directory()
    }
    link = value
    handle = lt.add_magnet_uri(ses, link, params)
    while not handle.has_metadata():
        time.sleep(1)
    while handle.status().state != lt.torrent_status.seeding:
        s = handle.status()
        state_str = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating']
        
        progress_label.config(text='%.2f%% complete (downloaded %d of %d bytes) - %s' %
                              (s.progress * 100, s.total_wanted, s.total_wanted, state_str[s.state]))
        download_speed_label.config(text='Download Speed: %.2f kB/s' % (s.download_payload_rate / 1000))
        upload_speed_label.config(text='Upload Speed: %.2f kB/s' % (s.upload_payload_rate / 1000))
        seeds_label.config(text='Seeds: %d' % s.num_seeds)
        window.update()
        time.sleep(1)
    button.config(state="normal")
    completion_message = "Download completed."
    completion_label = tk.Label(window, text=completion_message)
    completion_label.pack()
window = tk.Tk()
window.configure(bg="#F0F0F0")
window.tk_setPalette(background="#F0F0F0", foreground="#333333")
license_text = """

Prototype License Agreement

This product is a prototype and is provided "as is" without any warranty of any kind, 
express or implied. The use of this product is at your own risk. 

By using this software, you acknowledge and agree that:

1. This product is not a final release and may contain errors, bugs, or defects.
2. The functionality, features, and performance of this product may change without notice.
3. The developers and contributors of this product shall not be liable for any damages 
   arising from the use or inability to use this product.
4. You will provide feedback, suggestions, and bug reports to the developers to help 
   improve this product.

Author: Ambusher
Created on: 2023
Created with: Python

"""
window.title("Ambush Torrent Download Client")
window.geometry("900x500")
window.resizable(0, 0)
magnet_frame = tk.Frame(window)
magnet_frame.pack(pady=10)
magnet_url_label = tk.Label(magnet_frame, text="Magnet URL:")
magnet_url_label.pack(side="left")
magnet_url_box = tk.Entry(magnet_frame, width=40)
magnet_url_box.insert(0, "Enter/Paste your Magnet URL here")
magnet_url_box.bind("<FocusIn>", on_entry_click)
magnet_url_box.bind("<FocusOut>", on_focusout)
magnet_url_box.pack(side="left")
button_frame = tk.Frame(window)
button_frame.pack(pady=10)
directory_button = tk.Button(button_frame, text="Choose Directory", command=select_directory)
directory_button.pack(side="left")
directory_label = tk.Label(button_frame, text="Choosen Directory:", wraplength=100)
directory_label.pack(side="left")
torrent_button = tk.Button(button_frame, text="Import Torrent", command=select_torrent)
torrent_button.pack(side="left")
torrent_label = tk.Label(button_frame, text="Selected Torrent File: None", wraplength=100)
torrent_label.pack(side="left")
button = tk.Button(button_frame, text="Download", command=submit_value, width=10)
button.pack(side="left")
progress_label = tk.Label(window, text='')
progress_label.pack()
download_speed_label = tk.Label(window, text='')
download_speed_label.pack()
upload_speed_label = tk.Label(window, text='')
upload_speed_label.pack()
seeds_label = tk.Label(window, text='')
seeds_label.pack()
license_label = tk.Label(window, text=license_text, wraplength=600, justify="center")
license_label.pack(side="bottom", pady=5)
window.mainloop()