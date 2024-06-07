import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class VideoApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        # Captura as dimensões da câmera e reduz para 75% do tamanho original
        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH) * 0.75)
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT) * 0.75)

        # Layout
        self.frame1 = tk.Frame(window)
        self.frame1.pack(side=tk.LEFT, padx=10, pady=10)

        self.frame2 = tk.Frame(window)
        self.frame2.pack(side=tk.LEFT, padx=10, pady=10)

        self.frame3 = tk.Frame(window)
        self.frame3.pack(side=tk.RIGHT, padx=10, pady=10)

        # Label "Sem catarata"
        self.label_no_filter = tk.Label(self.frame1, text="Sem catarata")
        self.label_no_filter.pack()

        # Canvas para a captura sem filtros
        self.canvas_no_filter = tk.Canvas(self.frame1, width=self.width, height=self.height)
        self.canvas_no_filter.pack()

        # Label "Com catarata"
        self.label_with_filter = tk.Label(self.frame2, text="Com catarata")
        self.label_with_filter.pack()

        # Canvas para a captura com filtros
        self.canvas_with_filter = tk.Canvas(self.frame2, width=self.width, height=self.height)
        self.canvas_with_filter.pack()

        # Label "Controles"
        self.label_controls = tk.Label(self.frame3, text="Controles")
        self.label_controls.pack()

        # Controle deslizante para ajustar a quantidade de embaçamento Gaussiano
        self.gaussian_var = tk.IntVar()
        ttk.Label(self.frame3, text="Gaussian Blur").pack()
        self.gaussian_scale = ttk.Scale(self.frame3, from_=0, to_=20, orient='horizontal', variable=self.gaussian_var)
        self.gaussian_scale.pack()
        self.gaussian_label = tk.Label(self.frame3, text="0")
        self.gaussian_label.pack()

        # Controle deslizante para ajustar a quantidade de embaçamento Mediano
        self.median_var = tk.IntVar()
        ttk.Label(self.frame3, text="Median Blur").pack()
        self.median_scale = ttk.Scale(self.frame3, from_=0, to_=20, orient='horizontal', variable=self.median_var)
        self.median_scale.pack()
        self.median_label = tk.Label(self.frame3, text="0")
        self.median_label.pack()

        # Controle deslizante para ajustar a quantidade de embaçamento Bilateral
        self.bilateral_var = tk.IntVar()
        ttk.Label(self.frame3, text="Bilateral Blur").pack()
        self.bilateral_scale = ttk.Scale(self.frame3, from_=0, to_=20, orient='horizontal', variable=self.bilateral_var)
        self.bilateral_scale.pack()
        self.bilateral_label = tk.Label(self.frame3, text="0")
        self.bilateral_label.pack()

        # Controle deslizante para ajustar a quantidade de embaçamento Simples
        self.blur_var = tk.IntVar()
        ttk.Label(self.frame3, text="Simple Blur").pack()
        self.blur_scale = ttk.Scale(self.frame3, from_=0, to_=20, orient='horizontal', variable=self.blur_var)
        self.blur_scale.pack()
        self.blur_label = tk.Label(self.frame3, text="0")
        self.blur_label.pack()

        # Atualiza a interface periodicamente
        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.resize(frame, (self.width, self.height))
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self.photo_no_filter = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            self.canvas_no_filter.create_image(0, 0, image=self.photo_no_filter, anchor=tk.NW)

            gaussian_amount = self.gaussian_var.get()
            median_amount = self.median_var.get()
            bilateral_amount = self.bilateral_var.get()
            blur_amount = self.blur_var.get()

            self.gaussian_label.config(text=str(gaussian_amount))
            self.median_label.config(text=str(median_amount))
            self.bilateral_label.config(text=str(bilateral_amount))
            self.blur_label.config(text=str(blur_amount))

            frame_with_filters = frame_rgb.copy()

            if gaussian_amount > 0:
                frame_with_filters = cv2.GaussianBlur(frame_with_filters, (gaussian_amount * 2 + 1, gaussian_amount * 2 + 1), 0)
            if median_amount > 0:
                frame_with_filters = cv2.medianBlur(frame_with_filters, median_amount * 2 + 1)
            if bilateral_amount > 0:
                frame_with_filters = cv2.bilateralFilter(frame_with_filters, bilateral_amount * 2 + 1, 75, 75)
            if blur_amount > 0:
                frame_with_filters = cv2.blur(frame_with_filters, (blur_amount * 2 + 1, blur_amount * 2 + 1))

            self.photo_with_filter = ImageTk.PhotoImage(image=Image.fromarray(frame_with_filters))
            self.canvas_with_filter.create_image(0, 0, image=self.photo_with_filter, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root, "Video App com Filtros de Embaçamento Combinados")
