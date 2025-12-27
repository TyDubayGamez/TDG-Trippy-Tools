import tkinter as tk
from tkinter import filedialog
import qrcode
from PIL import Image, ImageTk
import io

class LiveQR_TDG:
    def __init__(self, root):
        self.root = root
        self.root.title("LiveQR by TDG")
        self.root.geometry("500x700")
        self.root.configure(bg="#050811")

        self.header = tk.Label(
            root, text="TDG LIVE QR", font=("Arial", 28, "bold"),
            fg="#00d2ff", bg="#050811", pady=20
        )
        self.header.pack()

        self.label = tk.Label(
            root, text="ENTER TEXT OR LINK BELOW:", 
            font=("Arial", 10, "bold"), fg="#a0aec0", bg="#050811"
        )
        self.label.pack()

        self.input_text = tk.StringVar()
        self.input_text.trace_add("write", self.update_qr)
        
        self.entry = tk.Entry(
            root, textvariable=self.input_text, font=("Arial", 14),
            bg="#1a1f2e", fg="white", insertbackground="white",
            relief="flat", borderwidth=10
        )
        self.entry.pack(pady=10, padx=40, fill="x")

        self.qr_label = tk.Label(root, bg="#050811")
        self.qr_label.pack(pady=30)

        self.download_btn = tk.Button(
            root, text="DOWNLOAD PNG", command=self.download_png,
            font=("Arial", 12, "bold"), bg="#9d50bb", fg="white",
            activebackground="#00d2ff", relief="flat", padx=20, pady=10
        )
        self.download_btn.pack(side="bottom", pady=40)

        self.current_img = None
        self.update_qr()

    def update_qr(self, *args):
        data = self.input_text.get()
        if not data:
            data = "Waiting for input..."

        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        
        self.current_img = qr.make_image(fill_color="black", back_color="white")
        
        preview_img = self.current_img.resize((300, 300), Image.NEAREST)
        self.tk_img = ImageTk.PhotoImage(preview_img)
        
        self.qr_label.config(image=self.tk_img)

    def download_png(self):
        if self.current_img:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                initialfile="TDG_QR_Code.png"
            )
            if file_path:
                self.current_img.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = LiveQR_TDG(root)
    root.mainloop()