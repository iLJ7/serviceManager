import tkinter as tk

app = tk.Tk()
app.geometry('1000x500')
top = tk.Frame(app)
bottom = tk.Frame(app)
top.pack(side=tk.TOP, pady=(20, 0))
bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

b = tk.Button(app, text="Enter", width=10, height=2)
c = tk.Button(app, text="Clear", width=10, height=2)
b.pack(in_=top, side=tk.LEFT)
c.pack(in_=top, side=tk.LEFT)

text = tk.Text(app, width=35, height=15)
scrollbar = tk.Scrollbar(app)
text.config(yscrollcommand=scrollbar.set)
scrollbar.pack(in_=bottom, side=tk.RIGHT, fill=tk.Y)
text.pack(in_=bottom, side=tk.LEFT, fill=tk.BOTH, expand=True)

app.mainloop()
