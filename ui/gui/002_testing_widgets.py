#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk


class MyFrame(tk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.selected_value = tk.StringVar()
        self.displayed_value = tk.StringVar()
        self.displayed_value.set('<empty>')
        combobox = ttk.Combobox(
            self, textvariable=self.selected_value,
            values=['hello world', 'hey you', 'howdy ?']
        )
        select_btn = ttk.Button(self, text='Go', command=self.on_select)
        display_lbl = ttk.Label(self, textvariable=self.displayed_value)
        combobox.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        select_btn.grid(row=0, column=2, sticky=tk.E)
        display_lbl.grid(row=1, column=0, columnspan=3)

    def on_select(self) -> None:
        if self.selected_value.get().strip():
            self.displayed_value.set(self.selected_value.get())
        else:
            self.displayed_value.set('<empty>')

class MyApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('Testing widgets')
        # self.geometry('800x600')
        self.resizable(width=False, height=False)
        MyFrame(self).grid(sticky=(tk.E + tk.W + tk.N + tk.S))
        self.columnconfigure(0, weight=1)


def main() -> None:
    app = MyApp()
    app.mainloop()

if __name__ == '__main__':
    main()
