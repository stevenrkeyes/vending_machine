import os
from pathlib import Path
import tkinter as tk
from tkinter import scrolledtext

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from scrolled_frame import ScrollFrame

# Initialize pygame mixer for playing sound files
pygame.mixer.init()


# Function to play sound
def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


class VendingMachineGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Anything Vending Machine Controller")

        self._create_orders_display()

        self._create_soundboard()

        # Bind spacebar to marking an order complete
        self.window.bind('<space>', lambda e: self.move_current_order_to_past_orders())

        self._move_window_to_front()

    def _move_window_to_front(self):
        self.window.attributes('-topmost', True)
        self.window.update()
        self.window.attributes('-topmost', False)

    def _create_orders_display(self):
        orders_frame = tk.Frame(self.window, padx=10, pady=10)
        orders_frame.pack(side="left")

        tk.Label(orders_frame, text="Past Orders:").grid(row=0, column=0)

        self.past_orders_display = scrolledtext.ScrolledText(orders_frame,
                                                             width=40,
                                                             height=16,
                                                             background='black',
                                                             foreground='white',
                                                             font="Helvetica 12")
        self.past_orders_display.grid(row=1, column=0)

        tk.Label(orders_frame, text="\nCurrent Orders:").grid(row=2, column=0)

        self.current_orders_display = scrolledtext.ScrolledText(orders_frame,
                                                                width=40,
                                                                height=8,
                                                                background='black',
                                                                foreground='white',
                                                                font="Helvetica 12")
        self.current_orders_display.grid(row=3, column=0)

        tk.Label(orders_frame, text="Tap space to mark oldest order complete.").grid(row=4, column=0)

        self.past_orders_display.configure(state='disabled')
        self.current_orders_display.configure(state='disabled')

    def _create_soundboard(self):
        soundboard_frame = tk.Frame(self.window)

        sounds_folder = "sounds"
        if not os.path.exists(sounds_folder):
            print(f"Directory '{sounds_folder}' not found.")
            return

        # Hard coded so that these come first in the gui
        subfolders = ['sounds\\start of order',
                      'sounds\\middle of order']

        additional_subfolders = [f.path for f in os.scandir(sounds_folder) if f.is_dir()]
        additional_subfolders = [folder for folder in additional_subfolders if folder not in subfolders]
        subfolders = subfolders + additional_subfolders

        for column, subfolder in enumerate(subfolders):
            scrollable_frame = ScrollFrame(soundboard_frame)

            subfolder_name = os.path.basename(subfolder)

            tk.Label(scrollable_frame.view_port, text=subfolder_name).pack()

            for file in os.listdir(subfolder):
                file_path = os.path.join(subfolder, file)
                filename_without_extension = Path(file).stem
                if os.path.isfile(file_path):
                    button = tk.Button(scrollable_frame.view_port,
                                       text=filename_without_extension,
                                       command=lambda f=file_path: play_sound(f),
                                       width=20,
                                       height=3)
                    button.pack(pady=5)

            scrollable_frame.pack(side="left", expand=True, fill='both')

        soundboard_frame.pack(side="left", expand=True, fill='both')

    def run(self):
        self.window.mainloop()

    def add_new_order(self, new_current_order_text):
        self.current_orders_display.configure(state='normal')
        self.current_orders_display.insert(tk.END, new_current_order_text + "\n")
        self.current_orders_display.yview(tk.END)
        self.current_orders_display.configure(state='disabled')

    def move_current_order_to_past_orders(self):
        # Move the oldest current order to the past orders

        self.current_orders_display.configure(state='normal')
        # The oldest order is on line 1
        oldest_order = self.current_orders_display.get("1.0", "2.0")
        self.current_orders_display.delete("1.0", "2.0")
        self.current_orders_display.configure(state='disabled')

        self.past_orders_display.configure(state='normal')
        self.past_orders_display.insert(tk.END, oldest_order)
        self.past_orders_display.yview(tk.END)
        self.past_orders_display.configure(state='disabled')
