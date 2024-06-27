import tkinter as tk
import platform


class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        # create a frame (self)
        super().__init__(parent)

        self.canvas = tk.Canvas(self, borderwidth=0)

        # place a frame on the canvas, this frame will hold the child widgets
        self.view_port = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        # add view port frame to canvas
        self.canvas_window = self.canvas.create_window((4, 4), window=self.view_port, anchor="nw", tags="self.view_port")

        self.view_port.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.view_port.bind('<Enter>', self.on_enter)
        self.view_port.bind('<Leave>', self.on_leave)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=event.width)

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window)

    def on_mouse_wheel(self, event):
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    def on_enter(self, event):
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)
            self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def on_leave(self, event):
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")
