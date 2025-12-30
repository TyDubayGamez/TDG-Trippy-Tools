import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk, ImageDraw
import re
import math

class TDG_PFP_QR:
    def __init__(self, root):
        self.root = root
        self.root.title("TDG QR - Stretched to Fit PFP")
        self.root.geometry("500x800")
        self.root.configure(bg="#050811")

        self.header = tk.Label(
            root, text="TDG LIVE QR", font=("Arial", 28, "bold"),
            fg="#00d2ff", bg="#050811", pady=20
        )
        self.header.pack()

        self.label = tk.Label(
            root, text="ENTER LINK (SAFE-OVAL AUTO-RESIZE):", 
            font=("Arial", 10, "bold"), fg="#a0aec0", bg="#050811"
        )
        self.label.pack()

        self.input_text = tk.StringVar()
        self.input_text.trace_add("write", self.update_preview)
        
        self.entry = tk.Entry(
            root, textvariable=self.input_text, font=("Arial", 14),
            bg="#1a1f2e", fg="white", insertbackground="white",
            relief="flat", borderwidth=10
        )
        self.entry.pack(pady=10, padx=40, fill="x")

        self.qr_label = tk.Label(root, bg="#050811")
        self.qr_label.pack(pady=20)

        self.download_btn = tk.Button(
            root, text="DOWNLOAD STRETCHED PFP", command=self.download_qr,
            font=("Arial", 12, "bold"), bg="#9d50bb", fg="white",
            activebackground="#00d2ff", relief="flat", padx=20, pady=10
        )
        self.download_btn.pack(side="bottom", pady=40)

        self.update_preview()

    def generate_safe_pfp(self, data, width=2560, height=1440):
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=1)
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        safe_width = int(width / math.sqrt(2))
        safe_height = int(height / math.sqrt(2))

        qr_stretched = qr_img.resize((safe_width, safe_height), Image.Resampling.LANCZOS)

        canvas = Image.new('RGB', (width, height), (255, 255, 255))
        
        paste_x = (width - safe_width) // 2
        paste_y = (height - safe_height) // 2
        canvas.paste(qr_stretched, (paste_x, paste_y))
        
        return canvas

    def update_preview(self, *args):
        data = self.input_text.get()
        if not data:
            data = " " 

        full_res = self.generate_safe_pfp(data, 800, 450)
        
        display_img = full_res.resize((400, 225), Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(display_img)
        self.qr_label.config(image=self.tk_img)

    def download_qr(self):
        data = self.input_text.get()
        if not data:
            messagebox.showwarning("Error", "Please enter a link first!")
            return

        clean_name = re.sub(r'^https?://', '', data)
        clean_name = re.sub(r'[\/:*?"<>|]', '_', clean_name)[:15]

        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg")],
            initialfile=f"{clean_name}_StretchedPFP.jpg"
        )
        
        if file_path:
            final_img = self.generate_safe_pfp(data)
            final_img.save(file_path, "JPEG", quality=95)
            messagebox.showinfo("Success", "Stretched Safe PFP Saved!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TDG_PFP_QR(root)
    root.mainloop()