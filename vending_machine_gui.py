import tkinter as tk
from tkinter import scrolledtext


class VendingMachineGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Anything Vending Machine Controller")

        orders_frame = tk.Frame(self.window, padx=10, pady=10)
        orders_frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(orders_frame, text="Past Orders:").grid(row=0, column=0)

        self.past_orders_display = scrolledtext.ScrolledText(orders_frame,
                                                             width=40,
                                                             height=8,
                                                             background='black',
                                                             foreground='white',
                                                             font="Helvetica 12")
        self.past_orders_display.grid(row=1, column=0)

        tk.Label(orders_frame, text="\nCurrent Order:").grid(row=2, column=0)

        self.current_order_display = tk.Entry(orders_frame,
                                              width=40,
                                              foreground='white',
                                              background='black',
                                              font="Helvetica 12")
        self.current_order_display.grid(row=3, column=0)

        self.past_orders_display.configure(state='disabled')
        button = tk.Button(text="Sound 1", width=25, height=5)
        button.grid(row=0, column=1)

    def run(self):
        self.window.mainloop()

    def get_current_order_text(self):
        return self.current_order_display.get()

    def update_current_order(self, new_current_order_text):
        self.current_order_display.delete(0, tk.END)
        self.current_order_display.insert(tk.END, new_current_order_text)

    def append_past_order(self, new_past_order_text):
        self.past_orders_display.configure(state='normal')
        self.past_orders_display.insert(tk.END, new_past_order_text + "\n")
        self.past_orders_display.yview(tk.END)
        self.past_orders_display.configure(state='disabled')
