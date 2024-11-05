import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import tkinter.simpledialog as simpledialog

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Sorting Visualizer")
        self.root.geometry("900x700")
        self.root.config(bg="#87CEEB")  # Sky blue background color

        self.array = []
        self.bars = []
        self.speed = 100  # Default speed (ms)

        # Add a project title label at the top
        project_title_label = tk.Label(root, text="Number Sorting Visualizer", font=("Helvetica", 30, "bold"), bg="#87CEEB")
        project_title_label.pack(pady=10)

        # Create a frame for the canvas and button section
        main_frame = tk.Frame(root, bg="#87CEEB")
        main_frame.pack(pady=20)

        # Create canvas for drawing bars
        self.canvas = tk.Canvas(main_frame, width=900, height=500, highlightthickness=0, bg="#E0F7FA")
        self.canvas.grid(row=0, column=0, padx=10)

        # Frame for sorting buttons
        button_frame = tk.Frame(main_frame, bg="#87CEEB")
        button_frame.grid(row=1, column=0, pady=10)

        # Create sorting buttons with colors and bold black text
        sorting_buttons = [
            ("Generate Numbers", self.generate_numbers, "#FF5733"),
            ("Input Numbers", self.input_numbers, "#33FF57"),
            ("Bubble Sort Asc", lambda: self.bubble_sort(ascending=True), "#3357FF"),
            ("Bubble Sort Desc", lambda: self.bubble_sort(ascending=False), "#F3FF33"),
            ("Selection Sort Asc", lambda: self.selection_sort(ascending=True), "#FF33A1"),
            ("Selection Sort Desc", lambda: self.selection_sort(ascending=False), "#33FFF9"),
            ("Quick Sort Asc", lambda: self.quick_sort(ascending=True), "#FF8C33"),
            ("Quick Sort Desc", lambda: self.quick_sort(ascending=False), "#33FF8C"),
            ("Merge Sort Asc", lambda: self.merge_sort(ascending=True), "#C70039"),
            ("Merge Sort Desc", lambda: self.merge_sort(ascending=False), "#900C3F"),
            ("Insertion Sort Asc", lambda: self.insertion_sort(ascending=True), "#581845"),
            ("Insertion Sort Desc", lambda: self.insertion_sort(ascending=False), "#FFC300"),
            ("Reset", self.reset, "#DAF7A6"),
        ]

        # Add speed control buttons
        speed_buttons = [
            ("Speed: Slow", lambda: self.set_speed(200), "#FF33E8"),
            ("Speed: Normal", lambda: self.set_speed(100), "#33FFF6"),
            ("Speed: Fast", lambda: self.set_speed(50), "#FFC300"),
        ]

        # Place sorting buttons in a grid layout
        for index, (text, command, color) in enumerate(sorting_buttons):
            btn = tk.Button(button_frame, text=text, command=command, bg=color, fg="black", font=("Helvetica", 10, "bold"))
            btn.grid(row=index // 4, column=index % 4, padx=5, pady=5, sticky="ew")

        # Place speed control buttons
        for index, (text, command, color) in enumerate(speed_buttons):
            btn = tk.Button(button_frame, text=text, command=command, bg=color, fg="black", font=("Helvetica", 10, "bold"))
            btn.grid(row=2, column=index, padx=5, pady=5, sticky="ew")

        # Configure button frame to expand evenly
        for i in range(4):  # 4 columns for sorting buttons
            button_frame.columnconfigure(i, weight=1)
        for i in range(3):  # 3 columns for speed buttons
            button_frame.columnconfigure(i, weight=1)

    def set_speed(self, speed):
        """Set the speed for sorting visualization."""
        self.speed = speed

    def generate_numbers(self):
        """Generate a new set of random numbers."""
        self.array = [random.randint(10, 100) for _ in range(30)]
        self.draw_bars()

    def input_numbers(self):
        """Allow the user to input custom numbers."""
        input_str = simpledialog.askstring("Input Numbers", "Enter numbers separated by commas:")
        if input_str:
            try:
                self.array = list(map(int, input_str.split(",")))
                self.draw_bars()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers separated by commas.")

    def draw_bars(self):
        """Draw the bars representing the sorting array."""
        if not self.canvas or not self.array:  # Ensure canvas and array are valid
            return
        self.canvas.delete("all")
        self.bars = []

        bar_width = 900 // len(self.array)
        for i, value in enumerate(self.array):
            x0 = i * bar_width + 5
            y0 = 500 - value * 4
            x1 = x0 + bar_width - 2
            y1 = 500
            bar_color = self.get_bar_color(value)
            bar = self.canvas.create_rectangle(x0, y0, x1, y1, fill=bar_color, outline="black")
            self.bars.append(bar)
            # Display the bar value
            self.canvas.create_text((x0 + x1) / 2, y0 - 10, text=str(value), fill="black", font=("Helvetica", 8))

    def get_bar_color(self, value):
        """Get a color based on the value of the bar."""
        if value < 30:
            return "#4CAF50"  # Green for low values
        elif value < 60:
            return "#FFC107"  # Amber for mid values
        else:
            return "#F44336"  # Red for high values

    def update_bars(self, indices):
        """Update the colors of the bars during sorting."""
        if not self.canvas or not self.bars:  # Ensure canvas and bars are valid
            return
        for index in indices:
            if 0 <= index < len(self.bars):  # Ensure index is within bounds
                self.canvas.itemconfig(self.bars[index], fill="purple")
        self.root.update()
        time.sleep(self.speed / 1000)  # Convert ms to seconds

    def bubble_sort(self, ascending=True):
        """Perform bubble sort and visualize the sorting process."""
        if not self.array:
            messagebox.showinfo("Empty Array", "Please generate numbers or input custom numbers.")
            return
        n = len(self.array)
        for i in range(n):
            for j in range(0, n - i - 1):
                self.update_bars([j, j + 1])
                if (ascending and self.array[j] > self.array[j + 1]) or (not ascending and self.array[j] < self.array[j + 1]):
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.draw_bars()
        self.update_bars(range(n))  # Final update to show sorted array

    def selection_sort(self, ascending=True):
        """Perform selection sort and visualize the sorting process."""
        if not self.array:
            messagebox.showinfo("Empty Array", "Please generate numbers or input custom numbers.")
            return
        n = len(self.array)
        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                self.update_bars([min_index, j])
                if (ascending and self.array[j] < self.array[min_index]) or (not ascending and self.array[j] > self.array[min_index]):
                    min_index = j
            self.array[i], self.array[min_index] = self.array[min_index], self.array[i]
            self.draw_bars()
        self.update_bars(range(n))  # Final update to show sorted array

    def insertion_sort(self, ascending=True):
        """Perform insertion sort and visualize the sorting process."""
        if not self.array:
            messagebox.showinfo("Empty Array", "Please generate numbers or input custom numbers.")
            return
        n = len(self.array)
        for i in range(1, n):
            key = self.array[i]
            j = i - 1
            while j >= 0 and ((ascending and self.array[j] > key) or (not ascending and self.array[j] < key)):
                self.update_bars([j, j + 1])
                self.array[j + 1] = self.array[j]
                j -= 1
            self.array[j + 1] = key
            self.draw_bars()
        self.update_bars(range(n))  # Final update to show sorted array

    def quick_sort(self, ascending=True):
        """Perform quick sort and visualize the sorting process."""
        if not self.array:
            messagebox.showinfo("Empty Array", "Please generate numbers or input custom numbers.")
            return
        self._quick_sort(0, len(self.array) - 1, ascending)
        self.update_bars(range(len(self.array)))  # Final update to show sorted array

    def _quick_sort(self, low, high, ascending):
        """Helper function for quick sort."""
        if low < high:
            pi = self.partition(low, high, ascending)
            self._quick_sort(low, pi - 1, ascending)
            self._quick_sort(pi + 1, high, ascending)

    def partition(self, low, high, ascending):
        """Partition function for quick sort."""
        pivot = self.array[high]
        i = low - 1
        for j in range(low, high):
            self.update_bars([i + 1, j])
            if (ascending and self.array[j] < pivot) or (not ascending and self.array[j] > pivot):
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
                self.draw_bars()
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        self.draw_bars()
        return i + 1

    def merge_sort(self, ascending=True):
        """Perform merge sort and visualize the sorting process."""
        if not self.array:
            messagebox.showinfo("Empty Array", "Please generate numbers or input custom numbers.")
            return
        self._merge_sort(0, len(self.array) - 1, ascending)
        self.update_bars(range(len(self.array)))  # Final update to show sorted array

    def _merge_sort(self, left, right, ascending):
        """Helper function for merge sort."""
        if left < right:
            mid = (left + right) // 2
            self._merge_sort(left, mid, ascending)
            self._merge_sort(mid + 1, right, ascending)
            self.merge(left, mid, right, ascending)

    def merge(self, left, mid, right, ascending):
        """Merge function for merge sort."""
        left_copy = self.array[left:mid + 1]
        right_copy = self.array[mid + 1:right + 1]

        left_index, right_index = 0, 0
        sorted_index = left

        while left_index < len(left_copy) and right_index < len(right_copy):
            self.update_bars([sorted_index])
            if (ascending and left_copy[left_index] <= right_copy[right_index]) or (not ascending and left_copy[left_index] >= right_copy[right_index]):
                self.array[sorted_index] = left_copy[left_index]
                left_index += 1
            else:
                self.array[sorted_index] = right_copy[right_index]
                right_index += 1
            sorted_index += 1
            self.draw_bars()

        while left_index < len(left_copy):
            self.update_bars([sorted_index])
            self.array[sorted_index] = left_copy[left_index]
            left_index += 1
            sorted_index += 1
            self.draw_bars()

        while right_index < len(right_copy):
            self.update_bars([sorted_index])
            self.array[sorted_index] = right_copy[right_index]
            right_index += 1
            sorted_index += 1
            self.draw_bars()

    def reset(self):
        """Reset the visualizer and clear the array."""
        self.array = []
        self.bars = []  # Clear the bar list as well
        if self.canvas:  # Check if the canvas still exists
            self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    visualizer = SortingVisualizer(root)
    root.mainloop()
