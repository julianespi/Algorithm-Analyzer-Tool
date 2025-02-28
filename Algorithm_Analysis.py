import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading
import random

# ------------------- Sorting Algorithm Generators -------------------

# Bubble Sort Generator (yields after each inner loop iteration)
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            yield

# Merge Sort Generator (yields after each merge step)
def merge_sort_gen(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        yield from merge_sort_gen(left_half)
        yield from merge_sort_gen(right_half)
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
            yield
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
            yield
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
            yield

# Quick Sort Generator (in-place using Lomuto partition scheme)
def quick_sort_gen(arr, low, high):
    if low < high:
        partition_gen = partition(arr, low, high)
        try:
            while True:
                next(partition_gen)
                yield
        except StopIteration as e:
            pivot_index = e.value
        yield from quick_sort_gen(arr, low, pivot_index - 1)
        yield from quick_sort_gen(arr, pivot_index + 1, high)

# Partition generator using Lomuto scheme that yields after each swap.
def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            yield
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    yield
    return i + 1

# ------------------- Radix Sort Generators (with reduced yield frequency) -------------------

def counting_sort_gen(arr, exp, yield_interval=200):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
        if (i + 1) % yield_interval == 0:
            yield
    yield

    for i in range(1, 10):
        count[i] += count[i - 1]
    yield

    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        if (n - i) % yield_interval == 0:
            yield
    yield

    for i in range(n):
        arr[i] = output[i]
        if (i + 1) % yield_interval == 0:
            yield
    yield

def lsd_radix_sort_gen(arr, yield_interval=200):
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        yield from counting_sort_gen(arr, exp, yield_interval)
        exp *= 10
        yield

def msd_radix_helper_gen(arr, digit_place, yield_interval=200):
    if len(arr) <= 1 or digit_place < 0:
        yield
        return
    buckets = [[] for _ in range(10)]
    for i, num in enumerate(arr):
        digit = (num // (10 ** digit_place)) % 10
        buckets[digit].append(num)
        if (i + 1) % yield_interval == 0:
            yield
    yield

    sorted_arr = []
    for bucket in buckets:
        if bucket:
            yield from msd_radix_helper_gen(bucket, digit_place - 1, yield_interval)
        sorted_arr.extend(bucket)
        yield
    for i in range(len(arr)):
        arr[i] = sorted_arr[i]
        if (i + 1) % yield_interval == 0:
            yield
    yield

def msd_radix_sort_gen(arr, yield_interval=200):
    max_num = max(arr)
    max_digits = len(str(max_num))
    yield from msd_radix_helper_gen(arr, max_digits - 1, yield_interval)

# ------------------- Linear Search Generator -------------------

def linear_search_gen(arr, target):
    indices = []
    for i, value in enumerate(arr):
        if value == target:
            indices.append(i)
        yield  # Yield after checking each element
    return indices  # Return the list of indices via StopIteration.value

# ------------------- Tkinter Sorting & Searching Visualizer -------------------

class SortingVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Real-Time Sorting & Searching Visualizer")
        self.master.geometry("800x600")
        self.is_paused = False
        self.is_running = False
        self.sort_threads = []  # One thread per algorithm/search
        self.bars = None
        self.setup_widgets()

    def setup_widgets(self):
        # Input Frame
        frame_input = tk.Frame(self.master, padx=10, pady=10)
        frame_input.pack(fill=tk.X)
        tk.Label(frame_input, text="Enter comma-separated numbers:").pack(side=tk.LEFT)
        self.entry_array = tk.Entry(frame_input, width=50)
        self.entry_array.pack(side=tk.LEFT, padx=10)

        # Algorithm Selection Frame
        frame_algorithms = tk.Frame(self.master, padx=10, pady=10)
        frame_algorithms.pack(fill=tk.X)
        self.var_bubble = tk.BooleanVar()
        tk.Checkbutton(frame_algorithms, text="Bubble Sort", variable=self.var_bubble).pack(anchor='w')
        self.var_merge = tk.BooleanVar()
        tk.Checkbutton(frame_algorithms, text="Merge Sort", variable=self.var_merge).pack(anchor='w')
        self.var_quick = tk.BooleanVar()
        tk.Checkbutton(frame_algorithms, text="Quick Sort", variable=self.var_quick).pack(anchor='w')
        self.var_lsd_radix = tk.BooleanVar()
        tk.Checkbutton(frame_algorithms, text="LSD Radix Sort", variable=self.var_lsd_radix).pack(anchor='w')
        self.var_msd_radix = tk.BooleanVar()
        tk.Checkbutton(frame_algorithms, text="MSD Radix Sort", variable=self.var_msd_radix).pack(anchor='w')
        self.var_linear_search = tk.BooleanVar()
        tk.Checkbutton(frame_algorithms, text="Linear Search", variable=self.var_linear_search).pack(anchor='w')

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

    def start_sorting(self):
        if self.is_running:
            messagebox.showinfo("Sorting/Searching in Progress", "A process is already running.")
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

        # Check that at least one algorithm/search is selected
        if not (self.var_bubble.get() or self.var_merge.get() or self.var_quick.get() or 
                self.var_lsd_radix.get() or self.var_msd_radix.get() or self.var_linear_search.get()):
            messagebox.showinfo("No Process Selected", "Please select at least one algorithm/search.")
            return

        # Prepare generators and corresponding labels/colors for the selected processes.
        self.sort_tasks = []  # Each element: (process name, generator)
        labels = []
        colors = []

        if self.var_bubble.get():
            labels.append("Bubble")
            colors.append("green")
            self.sort_tasks.append(("Bubble", bubble_sort(self.arr.copy())))
        if self.var_merge.get():
            labels.append("Merge Sort")
            colors.append("blue")
            self.sort_tasks.append(("Merge", merge_sort_gen(self.arr.copy())))
        if self.var_quick.get():
            labels.append("Quick Sort")
            colors.append("orange")
            arr_copy = self.arr.copy()
            self.sort_tasks.append(("Quick", quick_sort_gen(arr_copy, 0, len(arr_copy) - 1)))
        if self.var_lsd_radix.get():
            labels.append("LSD Radix")
            colors.append("purple")
            self.sort_tasks.append(("LSD Radix", lsd_radix_sort_gen(self.arr.copy())))
        if self.var_msd_radix.get():
            labels.append("MSD Radix")
            colors.append("cyan")
            self.sort_tasks.append(("MSD Radix", msd_radix_sort_gen(self.arr.copy())))
        if self.var_linear_search.get():
            # Choose a random target from the array.
            target = random.choice(self.arr.copy())
            labels.append(f"LS ({target})")
            colors.append("brown")
            self.sort_tasks.append(("Linear Search", linear_search_gen(self.arr.copy(), target)))

        # Reset and set up the plot with one bar per selected process.
        self.ax.clear()
        self.ax.set_title("Real-Time Execution Progress")
        self.ax.set_ylim(0, 5)  # Initial limit; will auto-adjust if needed
        self.ax.set_ylabel("Execution Time (seconds)")
        self.bars = self.ax.bar(labels, [0] * len(labels), color=colors)
        self.canvas.draw()

        self.is_running = True
        self.sort_threads = []

        # Create and start a thread for each selected process.
        for i, (proc_name, gen) in enumerate(self.sort_tasks):
            t = threading.Thread(target=self.run_sorting_algorithm, args=(proc_name, gen, i), daemon=True)
            self.sort_threads.append(t)
            t.start()

    def run_sorting_algorithm(self, proc_name, gen, bar_index):
        start_time = time.perf_counter()
        paused_time = 0
        result = None
        while True:
            try:
                next(gen)
            except StopIteration as e:
                result = e.value  # For Linear Search, this contains the found indices.
                break

            while self.is_paused:
                time.sleep(0.1)
                paused_time += 0.1

            elapsed = time.perf_counter() - start_time - paused_time
            self.bars[bar_index].set_height(elapsed)

            # Dynamically adjust y-axis limit if needed.
            current_ylim = self.ax.get_ylim()[1]
            if elapsed > current_ylim:
                new_ylim = elapsed * 1.1
                self.ax.set_ylim(0, new_ylim)
            self.canvas.draw_idle()
            time.sleep(0.05)

        final_time = time.perf_counter() - start_time - paused_time
        self.bars[bar_index].set_height(final_time)
        current_ylim = self.ax.get_ylim()[1]
        if final_time > current_ylim:
            self.ax.set_ylim(0, final_time * 1.1)
        self.canvas.draw_idle()
        # Show final message; for Linear Search include the indices found.
        if proc_name == "Linear Search":
            if result:
                msg = f"{proc_name} Execution Time: {final_time:.4f} sec\nTarget found at indices: {result}"
            else:
                msg = f"{proc_name} Execution Time: {final_time:.4f} sec\nTarget not found."
        else:
            msg = f"{proc_name} Execution Time: {final_time:.4f} sec"
        messagebox.showinfo("Process Completed", msg)

    def toggle_pause(self):
        if not self.is_running:
            messagebox.showinfo("Info", "Start a process first.")
            return
        self.is_paused = not self.is_paused
        self.btn_pause.config(text="Resume" if self.is_paused else "Pause")

    def reset_plot(self, clear_only=False):
        self.is_running = False
        self.is_paused = False

        if self.sort_threads:
            for t in self.sort_threads:
                if t.is_alive():
                    t.join(timeout=0.1)
            self.sort_threads = []

        self.ax.clear()
        self.bars = None
        self.ax.set_title("Real-Time Execution Progress")
        self.ax.set_ylim(0, 5)
        self.ax.set_ylabel("Execution Time (seconds)")
        self.canvas.draw()

        if not clear_only:
            messagebox.showinfo("Reset", "Plot has been reset.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
