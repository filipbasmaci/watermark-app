import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont


def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        load_image(file_path)


def load_image(file_path):
    global img, img_display, img_path, resized_img
    img_path = file_path
    img = Image.open(file_path)

    max_width, max_height = 800, 600
    img.thumbnail((max_width, max_height))

    img_display = ImageTk.PhotoImage(img)
    resized_img = img.copy()

    canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
    canvas.config(scrollregion=canvas.bbox(tk.ALL))


def add_watermark():
    global img_display_watermarked

    if img is None:
        messagebox.showerror("Error", "Please select an image first")
        return

    watermark_text = watermark_entry.get()
    if not watermark_text:
        messagebox.showerror("Error", "Please enter a watermark text")
        return

    draw = ImageDraw.Draw(resized_img)
    font = ImageFont.truetype("arial.ttf", 36)
    width, height = resized_img.size
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    position = (width - text_width - 10, height - text_height - 10)
    draw.text(position, watermark_text, (255, 255, 255), font=font)

    img_display_watermarked = ImageTk.PhotoImage(resized_img)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_display_watermarked)
    canvas.config(scrollregion=canvas.bbox(tk.ALL))


def save_image():
    if resized_img is None:
        messagebox.showerror("Error", "Please select an image first")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
    if save_path:
        resized_img.save(save_path)
        messagebox.showinfo("Image Saved", "Your watermarked image has been saved successfully.")


root = tk.Tk()
root.title("Watermarking Application")

img = None
img_path = None
resized_img = None

frame = tk.Frame(root)
frame.pack(pady=20)

canvas = tk.Canvas(frame, width=800, height=600, bg="grey")
canvas.pack(side=tk.LEFT)

scroll_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scroll_y.pack(side=tk.RIGHT, fill="y")

canvas.configure(yscrollcommand=scroll_y.set)

controls_frame = tk.Frame(root)
controls_frame.pack(pady=10)

select_btn = tk.Button(controls_frame, text="Select Image", command=select_image)
select_btn.grid(row=0, column=0, padx=5)

watermark_entry = tk.Entry(controls_frame)
watermark_entry.grid(row=0, column=1, padx=5)

add_watermark_btn = tk.Button(controls_frame, text="Add Watermark", command=add_watermark)
add_watermark_btn.grid(row=0, column=2, padx=5)

save_btn = tk.Button(controls_frame, text="Save Image", command=save_image)
save_btn.grid(row=0, column=3, padx=5)

root.mainloop()
