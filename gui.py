import os
import img2pdf
import re
import tkinter as tk
from tkinter import filedialog, messagebox


def dir_text_file(extension):
    img_ext = f".{extension.strip('.')}"
    webp_files = [x for x in dir_list if x.endswith(img_ext)]
    sort_files = sorted(webp_files, key=lambda x: int(x.split(".")[0]))  # Sort images by numbers

    # Store the list of image files in a text file
    with open("img_files.txt", "w") as file:
        for item in sort_files:
            file.write(item + "\n")

    messagebox.showinfo("Info", "Files stored in img_files.txt")


def img_to_pdf(dpi, img_extension):
    img_ext = f".{img_extension.strip('.')}"
    webp_files = [x for x in dir_list if x.endswith(img_ext)]
    sort_files = sorted(webp_files, key=lambda x: int(x.split(".")[0]))  # Sort images by numbers

    if not sort_files:
        messagebox.showwarning("Warning", "No images found with the provided extension.")
        return

    # Convert images to PDF with compression (adjust DPI)
    pdf_bytes = img2pdf.convert([os.path.join(path, img) for img in sort_files], dpi=dpi)

    # Save the PDF to a file
    pdf_file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], title="Save PDF File"
    )
    if pdf_file_path:
        with open(pdf_file_path, "wb") as pdf_file:
            pdf_file.write(pdf_bytes)
        messagebox.showinfo("Success", "Images converted to PDF successfully.")
    else:
        messagebox.showinfo("Info", "PDF conversion canceled.")


def natural_sort_key(s):
    # Custom sort key function for natural sorting
    return [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', s)]


def normal_image_to_pdf(extension):
    img_ext = f".{extension.strip('.')}"
    webp_files = [x for x in sorted(dir_list, key=natural_sort_key) if x.endswith(img_ext)]

    if not webp_files:
        messagebox.showwarning("Warning", "No images found with the provided extension.")
        return

    pdf_bytes = img2pdf.convert([os.path.join(path, img) for img in webp_files], dpi=300)

    # Save the PDF to a file
    pdf_file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], title="Save PDF File"
    )
    if pdf_file_path:
        with open(pdf_file_path, "wb") as pdf_file:
            pdf_file.write(pdf_bytes)
        messagebox.showinfo("Success", "Images converted to PDF successfully.")
    else:
        messagebox.showinfo("Info", "PDF conversion canceled.")


def select_image_directory():
    global path, dir_list
    path = filedialog.askdirectory(title="Select Image Directory")
    if path:
        dir_list = os.listdir(path)
        directory_label.config(text=path)


def on_convert_click():
    selected_option = radio_var.get()
    extension = extension_entry.get()

    if not path:
        messagebox.showwarning("Warning", "Please select an image directory.")
        return

    if selected_option == 1:
        dir_text_file(extension)
    elif selected_option == 2:
        dpi_options = {
            1: 72,
            2: 150,
            3: 300,
        }
        selected_dpi = dpi_options.get(dpi_var.get())
        if not selected_dpi:
            messagebox.showwarning("Warning", "Please select a DPI option.")
            return
        img_to_pdf(selected_dpi, extension)
    elif selected_option == 3:
        normal_image_to_pdf(extension)


if __name__ == "__main__":
    path = ""
    dir_list = []

    root = tk.Tk()
    root.title("Image To PDF Maker")
    root.geometry("400x400")

    radio_var = tk.IntVar()
    radio_var.set(1)  # Set default option to 1

    extension_label = tk.Label(root, text="Enter Image Extension ex(.png):")
    extension_label.pack()

    extension_entry = tk.Entry(root)
    extension_entry.pack()

    radio_frame = tk.Frame(root)
    radio_frame.pack()

    radio_label = tk.Label(radio_frame, text="Select Conversion Option:")
    radio_label.pack()

    dir_radio = tk.Radiobutton(radio_frame, text="Testing Text File", variable=radio_var, value=1)
    dir_radio.pack(anchor="w")

    pdf_radio = tk.Radiobutton(radio_frame, text="PDF Conversion", variable=radio_var, value=2)
    pdf_radio.pack(anchor="w")

    dpi_var = tk.IntVar()
    dpi_var.set(1)  # Set default DPI option to 1

    dpi_frame = tk.Frame(radio_frame)
    dpi_frame.pack()

    screen_radio = tk.Radiobutton(dpi_frame, text="Screen (72 DPI)", variable=dpi_var, value=1)
    screen_radio.pack(anchor="w")

    ebook_radio = tk.Radiobutton(dpi_frame, text="Ebook (150 DPI)", variable=dpi_var, value=2)
    ebook_radio.pack(anchor="w")

    prepress_radio = tk.Radiobutton(dpi_frame, text="Prepress (300 DPI)", variable=dpi_var, value=3)
    prepress_radio.pack(anchor="w")

    normal_radio = tk.Radiobutton(radio_frame, text="Normal Conversion", variable=radio_var, value=3)
    normal_radio.pack(anchor="w")

    select_dir_button = tk.Button(root, text="Select Image Directory", command=select_image_directory)
    select_dir_button.pack()

    directory_label = tk.Label(root, text="")
    directory_label.pack()

    convert_button = tk.Button(root, text="Convert", command=on_convert_click)
    convert_button.pack()

    root.mainloop()
