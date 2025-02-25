import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading

# Sorting algorithm (Bubble Sort with yield for step updates)
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            yield

class SortingVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Real-Time Sorting Progress Visualizer")
        self.master.geometry("800x600")

        self.is_paused = False
        self.is_running = False
        self.sort_thread = None

        # GUI Layout
        self.setup_widgets()

    def setup_widgets(self):
        # Input Frame
        frame_input = tk.Frame(self.master, padx=10, pady=10)
        frame_input.pack(fill=tk.X)

        tk.Label(frame_input, text="Enter comma-separated input:").pack(side=tk.LEFT)
        self.entry_array = tk.Entry(frame_input, width=50)
        self.entry_array.pack(side=tk.LEFT, padx=10)

        # Algorithm Selection Frame
        frame_algorithms = tk.Frame(self.master, padx=10, pady=10)
        frame_algorithms.pack(fill=tk.X)

        self.var_bubble = tk.BooleanVar()
        tk.Checkbutton(frame_algorithms, text="Bubble Sort", variable=self.var_bubble).pack(anchor='w')

        # Control Buttons
        frame_controls = tk.Frame(self.master, padx=10, pady=10)
        frame_controls.pack()

        self.btn_start = tk.Button(frame_controls, text="Start", command=self.start_sorting, bg="green", fg="white")
        self.btn_start.pack(side=tk.LEFT, padx=5)

        self.btn_pause = tk.Button(frame_controls, text="Pause", command=self.toggle_pause, bg="yellow")
        self.btn_pause.pack(side=tk.LEFT, padx=5)

        self.btn_reset = tk.Button(frame_controls, text="Reset", command=self.reset_plot, bg="red", fg="white")
        self.btn_reset.pack(side=tk.LEFT, padx=5)

        # Plot Frame
        self.frame_plot = tk.Frame(self.master, padx=10, pady=10)
        self.frame_plot.pack(fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_plot)
        self.canvas.get_tk_widget().pack()
        self.bar = None

    def start_sorting(self):
        if self.is_running:
            messagebox.showinfo("Sorting in Progress", "Sorting is already running.")
            return

        input_values = self.entry_array.get()
        if not input_values.strip():
            messagebox.showwarning("Input Error", "Please enter an array of numbers.")
            return

        try:
            self.arr = [int(x.strip()) for x in input_values.split(",")]
        except ValueError:
            messagebox.showerror("Input Error", "Enter valid integers separated by commas.")
            return

        if not self.var_bubble.get():
            messagebox.showinfo("No Algorithm Selected", "Please select an algorithm.")
            return

        self.reset_plot(clear_only=True)
        self.is_running = True
        self.is_paused = False

        # Start sorting in a separate thread to avoid freezing the GUI
        self.sort_thread = threading.Thread(target=self.run_sorting, daemon=True)
        self.sort_thread.start()

    def run_sorting(self):
        sort_gen = bubble_sort(self.arr.copy())
        self.ax.set_title("Real-Time Execution Progress")
        self.ax.set_ylim(0, 5)
        self.ax.set_ylabel("Execution Time (seconds)")

        if not self.bar:
            self.bar = self.ax.bar(["Bubble Sort"], [0], color='green')

        start_time = time.perf_counter()
        
        for _ in sort_gen:
            if not self.is_running:
                break  # Exit if reset is clicked
            
            while self.is_paused:
                time.sleep(0.1)  # Wait while paused

            elapsed = time.perf_counter() - start_time
            self.bar[0].set_height(elapsed)
            self.canvas.draw()
            time.sleep(0.05)  # Control the update speed

        if self.is_running:
            final_time = time.perf_counter() - start_time
            self.bar[0].set_height(final_time)
            self.canvas.draw()
            messagebox.showinfo("Sorting Completed", f"Execution Time: {final_time:.4f} seconds")

        self.is_running = False

    def toggle_pause(self):
        if not self.is_running:
            messagebox.showinfo("Info", "Start the sorting first.")
            return

        self.is_paused = not self.is_paused
        self.btn_pause.config(text="Resume" if self.is_paused else "Pause")

    def reset_plot(self, clear_only=False):
        self.is_running = False
        self.is_paused = False

        if self.sort_thread and self.sort_thread.is_alive():
            self.sort_thread.join(timeout=0.1)

        self.ax.clear()
        self.bar = None
        self.ax.set_title("Real-Time Execution Progress")
        self.ax.set_ylim(0, 5)
        self.ax.set_ylabel("Execution Time (seconds)")
        self.canvas.draw()

        if not clear_only:
            messagebox.showinfo("Reset", "Plot has been reset.")

# Initialize and run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
