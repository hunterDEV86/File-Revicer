import tkinter as tk
from tkinter import filedialog, messagebox
import requests

# آدرس API که قبلاً ساخته‌اید
API_URL = "http://127.0.0.1:5000/upload"

def upload_file():
    # دریافت فایل و متن از رابط کاربری
    file_path = file_entry.get()
    caption = caption_entry.get()

    if not file_path:
        messagebox.showerror("Error", "Please select a file!")
        return

    try:
        # ارسال فایل و متن به API
        with open(file_path, 'rb') as file:
            files = {'file': file}
            data = {'caption': caption}
            response = requests.post(API_URL, files=files, data=data)

        if response.status_code == 200:
            messagebox.showinfo("Success", "File and caption sent successfully!")
        else:
            messagebox.showerror("Error", f"Failed to send file: {response.text}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def browse_file():
    # باز کردن دیالوگ برای انتخاب فایل
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

# ایجاد پنجره اصلی
root = tk.Tk()
root.title("Telegram File Uploader")

# ایجاد و چیدمان ویجت‌ها
tk.Label(root, text="File:").grid(row=0, column=0, padx=10, pady=10)
file_entry = tk.Entry(root, width=50)
file_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Caption:").grid(row=1, column=0, padx=10, pady=10)
caption_entry = tk.Entry(root, width=50)
caption_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="Upload", command=upload_file).grid(row=2, column=1, pady=20)

# اجرای حلقه اصلی
root.mainloop()
