import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import numpy as np
import os


Image.MAX_IMAGE_PIXELS = None

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Wüdcutt')
        self.root.geometry("1024x1024")  # Set default siz
        self.root.minsize(600, 400)  # Minimum size of the window

        style = ttk.Style()
        style.theme_use('clam')  # or 'alt', 'default', 'classic', 'vista', 'xpnative'

        # Tab Control
        tab_control = ttk.Notebook(root)
        
        # Tab 1
        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='Threshold Adjuster')
        self.setup_tab1(tab1)

        # Tab 2
        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab2, text='Transparency Converter')
        self.setup_tab2(tab2)
        
        # Tab 3 (Macro Tab)
        tab3 = ttk.Frame(tab_control)
        tab_control.add(tab3, text='Macro')
        self.setup_tab3(tab3)
        
        tab_control.pack(expand=1, fill="both")


    def setup_tab1(self, frame):
        
        button_frame = tk.Frame(frame)
        button_frame.pack(fill='x')

        slider_frame = tk.Frame(frame)
        slider_frame.pack(fill='x')

        preview_frame = tk.Frame(frame)
        preview_frame.pack(fill='x')
        
        load_button = tk.Button(button_frame, text='Load Image', command=lambda: self.load_image(self.image_label))
        load_button.pack(side='left', padx=10, pady=10)

        self.threshold_slider = tk.Scale(slider_frame, from_=0, to=255, orient='horizontal', label='Adjust Threshold')
        self.threshold_slider.pack(side='left', padx=10, pady=10, fill='x', expand=True)
        self.threshold_slider.bind('<B1-Motion>', self.adjust_threshold)
        frame.bind('<Left>', self.decrease_threshold)
        frame.bind('<Right>', self.increase_threshold)

        save_button = tk.Button(button_frame, text='Save Image', command=self.save_image)
        save_button.pack(side='left', padx=10, pady=10)

        self.image_label = tk.Label(preview_frame)
        self.image_label.pack(fill='both', expand=True)

    def setup_tab2(self, frame):
        
        button_frame = tk.Frame(frame)
        button_frame.pack(fill='x')

        preview_frame = tk.Frame(frame)
        preview_frame.pack(fill='x')

        load_button = tk.Button(button_frame, text='Load Image', command=lambda: self.load_image(self.image_label_tab2))
        load_button.pack(side='left', padx=10, pady=10)

        save_button = tk.Button(button_frame, text='Save Image', command=self.save_image)
        save_button.pack(side='left', padx=10, pady=10)

        self.image_label_tab2 = tk.Label(preview_frame)
        self.image_label_tab2.pack()
        
    def setup_tab3(self, frame):
        
        button_frame = tk.Frame(frame)
        button_frame.pack(fill='x')

        path_frame = tk.Frame(frame)
        path_frame.pack(fill='x')

        preview_frame = tk.Frame(frame)
        preview_frame.pack(fill='x')
        
        load_button = tk.Button(button_frame, text='Load Image', command=lambda: self.load_image(self.image_label_tab3))
        load_button.pack(side='left', padx=10, pady=10)

        # Add a label and text entry for the save directory
        label = tk.Label(path_frame, text="Save directory:")
        label.pack(side='left', padx=(10, 2))

        self.save_directory_entry = tk.Entry(path_frame, width=50)
        self.save_directory_entry.pack(side='left', expand=True, fill='x', padx=(0, 10))
        self.save_directory_entry.insert(0, "C:\\Users\\Tristan\\Desktop\\Albrecht Durer-20240418T150257Z-001\\Albrecht Durer\\The Four Horsemen\\Macro")

        macro_button = tk.Button(button_frame, text='Save Images', command=self.save_macro_images)
        macro_button.pack(side='left', padx=10, pady=10)

        self.image_label_tab3 = tk.Label(preview_frame)
        self.image_label_tab3.pack()

    def save_macro_images(self):
        # Get the directory from the text entry field
        save_directory = self.save_directory_entry.get().strip()
        if not save_directory:
            tk.messagebox.showerror("Error", "Save directory must not be empty.")
            return

        if self.original_img is not None:
            # Check if the directory exists, and if not, attempt to create it
            if not os.path.exists(save_directory):
                try:
                    os.makedirs(save_directory)  # Attempt to create the directory
                except OSError as e:
                    tk.messagebox.showerror("Error", f"Failed to create directory: {e}")
                    return

            for threshold in range(0, 255, 5):  # From 100 to 200, every 5 steps
                img_array = np.array(self.original_img)
                img_array = np.where(img_array > threshold, 255, 0)
                processed_img = Image.fromarray(np.uint8(img_array))
                file_name = f"threshold_{threshold}.png"
                file_path = os.path.join(save_directory, file_name)
                try:
                    processed_img.save(file_path)  # Save directly to the specified directory
                except Exception as e:
                    tk.messagebox.showerror("Error", f"Failed to save image {file_name}: {e}")
                    continue
    
    def load_image(self, display_label):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.original_img = Image.open(file_path)
        self.original_img = ImageOps.exif_transpose(self.original_img)
        self.original_img = ImageOps.grayscale(self.original_img)
        self.thresholded_img = self.original_img.copy()
        self.update_preview(self.original_img, display_label)

    def adjust_threshold(self, event):
        if self.original_img is not None:
            img_array = np.array(self.original_img)
            threshold = self.threshold_slider.get()
            img_array = np.where(img_array > threshold, 255, 0)
            self.thresholded_img = Image.fromarray(np.uint8(img_array))
            self.update_preview(self.thresholded_img, self.image_label)

    def decrease_threshold(self, event):
        if self.threshold_slider.get() > 0:
            self.threshold_slider.set(self.threshold_slider.get() - 1)
            self.adjust_threshold(event)

    def increase_threshold(self, event):
        if self.threshold_slider.get() < 255:
            self.threshold_slider.set(self.threshold_slider.get() + 1)
            self.adjust_threshold(event)

    def update_preview(self, img, label):
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        max_size = (int(window_width * 0.90), int(window_height * 0.90))

        img_copy = img.copy()
        img_copy.thumbnail(max_size, Image.Resampling.LANCZOS)

        photo = ImageTk.PhotoImage(img_copy)
        label.config(image=photo)
        label.image = photo  # Keep a reference to prevent garbage collection

    def save_image(self):
        if self.thresholded_img is not None:
            self.thresholded_img.save(filedialog.asksaveasfilename(defaultextension=".png"))

    def on_resize(self, event):
        # Update the slider width and preview when resizing
        if self.original_img:
            self.update_preview(self.original_img, self.image_label)

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
