from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from PIL import ImageTk

from wudcutt.processing import (
    apply_threshold,
    create_transparent_image,
    generate_threshold_series,
    load_image_grayscale,
)


class ImageApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Wudcutt")
        self.root.geometry("1100x950")
        self.root.minsize(700, 500)

        self.original_img = None
        self.thresholded_img = None
        self.transparent_img = None
        self.current_preview_label = None

        style = ttk.Style()
        style.theme_use("clam")

        tabs = ttk.Notebook(root)
        self.threshold_tab = ttk.Frame(tabs)
        self.transparency_tab = ttk.Frame(tabs)
        self.macro_tab = ttk.Frame(tabs)
        tabs.add(self.threshold_tab, text="Threshold Adjuster")
        tabs.add(self.transparency_tab, text="Transparency Converter")
        tabs.add(self.macro_tab, text="Macro")
        tabs.pack(expand=1, fill="both")

        self.setup_threshold_tab()
        self.setup_transparency_tab()
        self.setup_macro_tab()

    def setup_threshold_tab(self):
        button_frame = tk.Frame(self.threshold_tab)
        button_frame.pack(fill="x")
        slider_frame = tk.Frame(self.threshold_tab)
        slider_frame.pack(fill="x")
        preview_frame = tk.Frame(self.threshold_tab)
        preview_frame.pack(fill="both", expand=True)

        tk.Button(button_frame, text="Load Image", command=lambda: self.load_image(self.threshold_label)).pack(side="left", padx=10, pady=10)
        tk.Button(button_frame, text="Save Thresholded Image", command=lambda: self.save_current_image(self.thresholded_img)).pack(side="left", padx=10, pady=10)

        self.threshold_slider = tk.Scale(slider_frame, from_=0, to=255, orient="horizontal", label="Adjust Threshold", command=lambda _value: self.adjust_threshold())
        self.threshold_slider.set(140)
        self.threshold_slider.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        self.threshold_label = tk.Label(preview_frame)
        self.threshold_label.pack(fill="both", expand=True)

    def setup_transparency_tab(self):
        button_frame = tk.Frame(self.transparency_tab)
        button_frame.pack(fill="x")
        preview_frame = tk.Frame(self.transparency_tab)
        preview_frame.pack(fill="both", expand=True)

        tk.Button(button_frame, text="Load Image", command=lambda: self.load_image(self.transparency_label)).pack(side="left", padx=10, pady=10)
        tk.Button(button_frame, text="Preview Transparent", command=self.preview_transparent).pack(side="left", padx=10, pady=10)
        tk.Button(button_frame, text="Save Transparent PNG", command=lambda: self.save_current_image(self.transparent_img)).pack(side="left", padx=10, pady=10)

        help_text = tk.Label(
            button_frame,
            text="White pixels become transparent; darker pixels become solid black.",
        )
        help_text.pack(side="left", padx=10)

        self.transparency_label = tk.Label(preview_frame)
        self.transparency_label.pack(fill="both", expand=True)

    def setup_macro_tab(self):
        button_frame = tk.Frame(self.macro_tab)
        button_frame.pack(fill="x")
        path_frame = tk.Frame(self.macro_tab)
        path_frame.pack(fill="x")
        preview_frame = tk.Frame(self.macro_tab)
        preview_frame.pack(fill="both", expand=True)

        tk.Button(button_frame, text="Load Image", command=lambda: self.load_image(self.macro_label)).pack(side="left", padx=10, pady=10)
        tk.Label(path_frame, text="Save directory:").pack(side="left", padx=(10, 2))

        default_macro_dir = Path.cwd() / "exports" / "macro"
        self.save_directory_entry = tk.Entry(path_frame, width=70)
        self.save_directory_entry.insert(0, str(default_macro_dir))
        self.save_directory_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        tk.Button(path_frame, text="Browse", command=self.choose_macro_directory).pack(side="left", padx=10)
        tk.Button(button_frame, text="Save Threshold Series", command=self.save_macro_images).pack(side="left", padx=10, pady=10)

        self.macro_label = tk.Label(preview_frame)
        self.macro_label.pack(fill="both", expand=True)

    def choose_macro_directory(self):
        selected = filedialog.askdirectory(initialdir=self.save_directory_entry.get() or str(Path.cwd()))
        if selected:
            self.save_directory_entry.delete(0, tk.END)
            self.save_directory_entry.insert(0, selected)

    def load_image(self, display_label: tk.Label):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.tif *.tiff *.webp"), ("All files", "*.*")])
        if not file_path:
            return
        self.original_img = load_image_grayscale(file_path)
        self.thresholded_img = apply_threshold(self.original_img, self.threshold_slider.get())
        self.transparent_img = None
        self.current_preview_label = display_label
        if display_label is self.threshold_label:
            self.update_preview(self.thresholded_img, display_label)
        else:
            self.update_preview(self.original_img, display_label)

    def adjust_threshold(self):
        if self.original_img is None:
            return
        self.thresholded_img = apply_threshold(self.original_img, self.threshold_slider.get())
        self.update_preview(self.thresholded_img, self.threshold_label)

    def preview_transparent(self):
        if self.original_img is None:
            messagebox.showinfo("No image loaded", "Load an image first.")
            return
        base = self.thresholded_img or apply_threshold(self.original_img, self.threshold_slider.get())
        self.transparent_img = create_transparent_image(base)
        self.update_preview(self.transparent_img, self.transparency_label)

    def save_macro_images(self):
        save_directory = self.save_directory_entry.get().strip()
        if not save_directory:
            messagebox.showerror("Error", "Save directory must not be empty.")
            return
        if self.original_img is None:
            messagebox.showinfo("No image loaded", "Load an image first.")
            return

        target_dir = Path(save_directory)
        target_dir.mkdir(parents=True, exist_ok=True)
        for item in generate_threshold_series(self.original_img, start=0, stop=255, step=5):
            item.image.save(target_dir / f"threshold_{item.threshold}.png")
        messagebox.showinfo("Done", f"Saved threshold series to {target_dir}")

    def save_current_image(self, image):
        if image is None:
            messagebox.showinfo("Nothing to save", "Generate or load an image first.")
            return
        target = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("All files", "*.*")])
        if target:
            image.save(target)

    def update_preview(self, img, label: tk.Label):
        window_width = max(self.root.winfo_width(), 800)
        window_height = max(self.root.winfo_height(), 600)
        max_size = (int(window_width * 0.85), int(window_height * 0.75))

        preview = img.copy()
        preview.thumbnail(max_size)
        photo = ImageTk.PhotoImage(preview)
        label.configure(image=photo)
        label.image = photo


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
