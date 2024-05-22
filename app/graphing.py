import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphingCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Graphing Calculator")
        self.root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        # Create main frames
        self.input_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.graph_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.graph_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Create input elements
        ttk.Label(self.input_frame, text="Enter function f(x):").grid(
            column=0,
            row=0,
            sticky=tk.W,
        )
        self.function_entry = ttk.Entry(self.input_frame, width=40)
        self.function_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))

        ttk.Label(self.input_frame, text="X-axis Min:").grid(
            column=0, row=1, sticky=tk.W
        )
        self.x_min_entry = ttk.Entry(self.input_frame, width=10)
        self.x_min_entry.grid(column=1, row=1, sticky=tk.W)

        ttk.Label(self.input_frame, text="X-axis Max:").grid(
            column=2, row=1, sticky=tk.W
        )
        self.x_max_entry = ttk.Entry(self.input_frame, width=10)
        self.x_max_entry.grid(column=3, row=1, sticky=tk.W)

        ttk.Button(self.input_frame, text="Plot", command=self.plot_graph).grid(
            column=4, row=0, rowspan=2, sticky=(tk.W, tk.E)
        )

        for child in self.input_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.function_entry.focus()

        # Create matplotlib figure
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def plot_graph(self):
        function_str = self.function_entry.get()
        x_min_str = self.x_min_entry.get()
        x_max_str = self.x_max_entry.get()

        try:
            x_min = float(x_min_str)
            x_max = float(x_max_str)
        except ValueError:
            messagebox.showerror(
                "Invalid input", "X-axis min and max must be valid numbers."
            )
            return

        if x_min >= x_max:
            messagebox.showerror(
                "Invalid input", "X-axis min must be less than X-axis max."
            )
            return

        try:
            x = np.linspace(x_min, x_max, 400)
            y = eval(function_str, {"__builtins__": None, "x": x, "np": np})

            self.ax.clear()
            self.ax.plot(x, y, label=f"f(x) = {function_str}")
            self.ax.set_title(f"Graph of {function_str}")
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("f(x)")
            self.ax.legend()
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while plotting the function: {e}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphingCalculator(root)
    root.mainloop()
