import tkinter as tk
from tkinter import filedialog, messagebox
import os
import cv2
import numpy as np

class ImageBrowser:
    def __init__(self, root, points_per_image=3, zoom_factor=1.5):
        self.root = root
        self.root.title("JPG Image Clicker")

        self.folder_path = ""
        self.image_paths = []
        self.current_image_index = 0
        self.points_per_image = points_per_image  # 每张图片需要标记的点数
        self.clicks = {}  # 保存每个图片的点击点
        self.zoom_factor = zoom_factor  # 放大缩小因子
        self.scale_factor = 1.0  # 当前缩放比例
        self.image_label = tk.Label(root, text="", font=("Arial", 12))
        self.image_label.pack()

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.prev_button = tk.Button(root, text="Previous", command=self.show_previous_image)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(root, text="Next", command=self.show_next_image)
        self.next_button.pack(side=tk.RIGHT)

        self.open_button = tk.Button(root, text="Open Folder", command=self.open_folder)
        self.open_button.pack()

        self.zoom_in_button = tk.Button(root, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT)

        self.zoom_out_button = tk.Button(root, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.RIGHT)

        self.output_dir = "txtoutput"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def open_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.image_paths = [os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path) if f.lower().endswith(".jpg")]
            self.current_image_index = 0
            self.clicks = {}  # 初始化点击记录
            self.load_image()

    def load_image(self):
        if self.image_paths:
            image_path = self.image_paths[self.current_image_index]
            image = cv2.imread(image_path)
            self.show_image(image, image_path)

    def show_image(self, img, path):
        self.image_label.config(text=os.path.basename(path))
        img_name = os.path.basename(path)

        # Check if the image has already been processed
        if self.is_image_processed(img_name):
            messagebox.showinfo("Info", f"Data for {img_name} has already been extracted.")
            self.show_next_image()
            return

        # Resize the image based on the current scale factor
        new_width = int(img.shape[1] * self.scale_factor)
        new_height = int(img.shape[0] * self.scale_factor)
        resized_img = cv2.resize(img, (new_width, new_height))

        self.photo = tk.PhotoImage(master=self.root, data=cv2.imencode('.png', resized_img)[1].tobytes())
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        # Set mouse callback for the image window
        cv2.imshow('Image', resized_img)
        cv2.setMouseCallback('Image', lambda event, x, y, flags, param: self.mouse_callback(event, x, y, img_name))

    def mouse_callback(self, event, x, y, img_name):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Convert scaled coordinates to original coordinates
            x_original = int(x / self.scale_factor)
            y_original = int(y / self.scale_factor)
            if img_name not in self.clicks:
                self.clicks[img_name] = []
            self.clicks[img_name].append((x_original, y_original))
            print(f"Clicked at ({x_original}, {y_original}) on {img_name}")
            if len(self.clicks[img_name]) >= self.points_per_image:
                self.save_points(img_name)
                self.show_next_image()

    def save_points(self, img_name):
        # 每张图片的点数据保存到不同的文件中
        for i in range(self.points_per_image):
            output_file = os.path.join(self.output_dir, f"points_{i + 1}.txt")
            with open(output_file, "a") as file:
                if len(self.clicks[img_name]) > i:
                    point = self.clicks[img_name][i]
                    file.write(f"{img_name}, {point[0]}, {point[1]}\n")
        print(f"Saved points for {img_name} to points_1.txt, points_2.txt, points_3.txt")

    def is_image_processed(self, img_name):
        """Check if the image has already been processed."""
        for i in range(self.points_per_image):
            output_file = os.path.join(self.output_dir, f"points_{i + 1}.txt")
            if os.path.exists(output_file):
                with open(output_file, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        if line.startswith(img_name + ","):
                            return True
        return False

    def show_previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_image()

    def show_next_image(self):
        if self.current_image_index < len(self.image_paths) - 1:
            self.current_image_index += 1
            self.load_image()

    def zoom_in(self):
        self.scale_factor *= self.zoom_factor
        self.load_image()

    def zoom_out(self):
        self.scale_factor /= self.zoom_factor
        self.load_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageBrowser(root, points_per_image=3, zoom_factor=1.5)
    root.mainloop()