__IF__ a GUI is going to be developed for OCP5, here's a first analysis of the requirements for Tkinter.

1. Creating an app inheriting from `tk.Tk`
2. For simple text like welcome words and product's fiche, choose a `tk.Frame` with a simple `ttk.Text`
3. For every list of values, use a `ttk.Combobox`
