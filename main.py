import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from Algorithms import lzw, huffman, rle, zip_algo, bz2_algo, lzma_algo, bmp_algo
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
from PIL import Image
import zipfile

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class CompressionApp:
    def __init__(self, master):
        self.master = master
        master.title("User-Driven File Compression System")
        master.geometry("440x480")
        master.resizable(False, False)
        master.configure(bg="#eaf6fb")  # Light blue background

        # Header
        header = tk.Label(master, text="User-Driven File Compression System", font=("Segoe UI", 18, "bold"), bg="#eaf6fb", fg="#0b3954")
        header.pack(pady=(18, 8))

        # Main frame
        main_frame = ttk.Frame(master, padding=18, style="Custom.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Compression Choices Frame (always at the top) ---
        self.choices_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        self.choices_frame.pack(fill="x", pady=(0, 7))

        self.label = ttk.Label(self.choices_frame, text="Select Compression Level:", font=("Segoe UI", 11), background="#eaf6fb")
        self.label.pack(anchor="w", pady=(0, 7))

        # Compression level for non-BMP
        self.level_var = tk.StringVar(value="High")
        self.high_radio = ttk.Radiobutton(self.choices_frame, text="High", variable=self.level_var, value="High", style="Custom.TRadiobutton")
        self.low_radio = ttk.Radiobutton(self.choices_frame, text="Low", variable=self.level_var, value="Low", style="Custom.TRadiobutton")
        self.optimal_radio = ttk.Radiobutton(self.choices_frame, text="Optimal", variable=self.level_var, value="Optimal", style="Custom.TRadiobutton")
        self.high_radio.pack(anchor="w", side="left")
        self.low_radio.pack(anchor="w", side="left")
        self.optimal_radio.pack(anchor="w", side="left")

        # Move size labels frame after the radio buttons and make it separate from choices_frame
        self.size_labels_frame = ttk.Frame(main_frame, style="Custom.TFrame")  # Changed parent to main_frame
        self.size_labels_frame.pack(fill="x", pady=(0, 7))

        # Create size labels with better visibility
        label_style = {"background": "#eaf6fb", "font": ("Segoe UI", 10)}
        self.input_size_label = ttk.Label(self.size_labels_frame, text="Input size: --", **label_style)
        self.input_size_label.pack(anchor="w", padx=5, pady=2)
        
        self.high_est_label = ttk.Label(self.size_labels_frame, text="High: --", **label_style)
        self.high_est_label.pack(anchor="w", padx=5, pady=2)
        
        self.low_est_label = ttk.Label(self.size_labels_frame, text="Low: --", **label_style)
        self.low_est_label.pack(anchor="w", padx=5, pady=2)
        
        self.optimal_est_label = ttk.Label(self.size_labels_frame, text="Optimal: --", **label_style)
        self.optimal_est_label.pack(anchor="w", padx=5, pady=2)

        # BMP compression options (hidden by default)
        self.bmp_option_var = tk.StringVar(value="Low")
        self.bmp_options_frame = ttk.Frame(self.choices_frame, style="Custom.TFrame")
        self.bmp_low_radio = ttk.Radiobutton(self.bmp_options_frame, text="Low (Lossless, PNG)", variable=self.bmp_option_var, value="Low", style="Custom.TRadiobutton", command=self.update_bmp_label)
        self.bmp_high_radio = ttk.Radiobutton(self.bmp_options_frame, text="High (Lossy, JPEG)", variable=self.bmp_option_var, value="High", style="Custom.TRadiobutton", command=self.update_bmp_label)
        self.bmp_label = ttk.Label(self.bmp_options_frame, text="Low (Lossless)", font=("Segoe UI", 10, "italic"), background="#eaf6fb")
        self.bmp_options_frame.pack_forget()

        self.file_path = ""

        # Select Input File button first
        self.select_file_button = ttk.Button(main_frame, text="Select Input File", command=self.select_file, style="Select.TButton")
        self.select_file_button.pack(pady=(0, 12), fill="x")
        ToolTip(self.select_file_button, "Browse and select a file to compress.")

        # Compress button below input file button
        self.compress_button = ttk.Button(main_frame, text="Compress File", command=self.compress_file, style="Compress.TButton")
        self.compress_button.pack(pady=(0, 12), fill="x")
        ToolTip(self.compress_button, "Compress the selected file using the chosen algorithm.")

        # Decompress button below compress button
        self.decompress_button = ttk.Button(main_frame, text="Decompress File", command=self.decompress_file, style="Select.TButton")
        self.decompress_button.pack(pady=(0, 12), fill="x")
        ToolTip(self.decompress_button, "Decompress a previously compressed file.")

        # Drag-and-drop label below decompress button
        self.dnd_label = tk.Label(main_frame, text="Or drag and drop a file here", relief="ridge", width=40, height=2, bg="#eaf6fb", font=("Segoe UI", 10))
        self.dnd_label.pack(pady=14)
        self.dnd_label.drop_target_register(DND_FILES)
        self.dnd_label.dnd_bind('<<Drop>>', self.drop_file)
        self.dnd_label.bind("<Enter>", self.on_dnd_enter)
        self.dnd_label.bind("<Leave>", self.on_dnd_leave)

        # Status bar 
        self.status_var = tk.StringVar(value="Ready")
        status_frame = tk.Frame(master, bg="#d1eaf5", height=24)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar = tk.Label(
            status_frame,
            textvariable=self.status_var,
            anchor="w",
            font=("Segoe UI", 10, "italic"),
            bg="#d1eaf5",
            fg="#0b3954",
            padx=10,
            pady=2,
            bd=0
        )
        self.status_bar.pack(fill=tk.BOTH, expand=True)

    def on_dnd_enter(self, event):
        pass

    def on_dnd_leave(self, event):
        pass

    def set_status(self, message):
        self.status_var.set(message)
        self.master.update_idletasks()

    def select_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[
                ("All Supported", "*.txt *.pdf *.doc *.docx *.jpg *.jpeg *.png *.bmp"),
                ("Text files", "*.txt"),
                ("PDF files", "*.pdf"),
                ("Word files", "*.doc *.docx"),
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("All files", "*.*"),
            ]
        )
        if self.file_path:
            messagebox.showinfo("Selected File", f"Selected file: {self.file_path}")
            self.set_status(f"Selected file: {self.file_path}")
            self.update_size_labels()  # <-- update size labels
            if self.file_path.lower().endswith(".bmp"):
                self.show_bmp_options()
            else:
                self.hide_bmp_options()

    def update_size_labels(self):
        if not self.file_path or not os.path.isfile(self.file_path):
            self.input_size_label.config(text="Input size: --")
            self.high_est_label.config(text="High: --")
            self.low_est_label.config(text="Low: --")
            self.optimal_est_label.config(text="Optimal: --")
            return
            
        size = os.path.getsize(self.file_path)
        ext = os.path.splitext(self.file_path)[1].lower()
        
        # Set compression ratios based on file type
        if ext == '.txt':
            high_ratio = 0.06    # LZW
            low_ratio = 0.4       # Huffman  
            optimal_ratio = 0.2 # RLE
        elif ext in ['.pdf', '.doc', '.docx']:
            high_ratio = 0.70    # LZMA
            low_ratio = 0.85     # ZIP
            optimal_ratio = 0.75 # BZ2
        elif ext in ['.jpg', '.jpeg']:
            high_ratio = 0.85    # Already compressed
            low_ratio = 0.95     
            optimal_ratio = 0.90
        elif ext == '.png':
            high_ratio = 0.60
            low_ratio = 0.80
            optimal_ratio = 0.70
        elif ext == '.bmp':
            high_ratio = 0.25    # JPEG conversion
            low_ratio = 0.40     # PNG conversion
            optimal_ratio = 0.35
        else:
            high_ratio = 0.50    # default ZIP
            low_ratio = 0.70
            optimal_ratio = 0.60

        self.input_size_label.config(text=f"Input size: {self.format_size(size)}")
        self.high_est_label.config(text=f"High: ~{self.format_size(int(size * high_ratio))}")
        self.low_est_label.config(text=f"Low: ~{self.format_size(int(size * low_ratio))}")
        self.optimal_est_label.config(text=f"Optimal: ~{self.format_size(int(size * optimal_ratio))}")

    def format_size(self, size):
        # Human-readable file size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def drop_file(self, event):
        self.file_path = event.data.strip('{}')
        messagebox.showinfo("Selected File", f"Selected file: {self.file_path}")
        self.set_status(f"Selected file: {self.file_path}")
        self.update_size_labels()  # Add this line to update sizes on drop
        if self.file_path.lower().endswith(".bmp"):
            self.show_bmp_options()
        else:
            self.hide_bmp_options()

    def update_bmp_label(self):
        if self.bmp_option_var.get() == "Low":
            self.bmp_label.config(text="Low (Lossless)")
        else:
            self.bmp_label.config(text="High (Lossy)")

    def show_bmp_options(self):
        # Hide non-BMP radios
        self.high_radio.pack_forget()
        self.low_radio.pack_forget()
        self.optimal_radio.pack_forget()
        
        # Hide compression size labels for BMP
        self.input_size_label.pack_forget()
        self.high_est_label.pack_forget()
        self.low_est_label.pack_forget()
        self.optimal_est_label.pack_forget()
        
        # Show BMP radios in the same place
        self.bmp_options_frame.pack(fill="x", pady=(0, 7))
        self.bmp_low_radio.pack(anchor="w")
        self.bmp_high_radio.pack(anchor="w")
        self.bmp_label.pack(anchor="w", pady=(4, 0))
        self.update_bmp_label()

    def hide_bmp_options(self):
        self.bmp_options_frame.pack_forget()
        self.bmp_low_radio.pack_forget()
        self.bmp_high_radio.pack_forget()
        self.bmp_label.pack_forget()
        
        # Show non-BMP radios in the same place
        self.high_radio.pack(anchor="w")
        self.low_radio.pack(anchor="w")
        self.optimal_radio.pack(anchor="w")
        
        # Show compression size labels again
        self.input_size_label.pack(anchor="w", padx=5, pady=2)
        self.high_est_label.pack(anchor="w", padx=5, pady=2)
        self.low_est_label.pack(anchor="w", padx=5, pady=2)
        self.optimal_est_label.pack(anchor="w", padx=5, pady=2)

    def compress_file(self):
        if not self.file_path:
            messagebox.showwarning("No File Selected", "Please select an input file.")
            self.set_status("No file selected.")
            return

        # Special handling for BMP
        if self.file_path.lower().endswith(".bmp"):
            option = self.bmp_option_var.get()
            ext = "png" if option == "Low" else "jpg"
            filetypes = [("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All files", "*.*")]
            output_path = filedialog.asksaveasfilename(
                title="Save Converted Image As",
                defaultextension=f".{ext}",
                filetypes=filetypes
            )
            if not output_path:
                self.set_status("No save location selected.")
                return
            try:
                self.set_status("Converting...")
                img = Image.open(self.file_path)
                if option == "Low":
                    img.save(output_path, "PNG")
                else:
                    img = img.convert("RGB")
                    img.save(output_path, "JPEG", quality=85)
                messagebox.showinfo("Success", f"Image converted and saved to {output_path}")
                self.set_status(f"Image converted to {output_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                self.set_status("Conversion failed.")
            return

        # --- Existing logic for other files below ---
        level = self.level_var.get()
        algo, ext = self.get_algo_and_ext(self.file_path, level)

        filetypes = [(f"{ext.upper()} files", f"*.{ext}"), ("All files", "*.*")]
        output_path = filedialog.asksaveasfilename(
            title="Save Compressed File As",
            defaultextension=f".{ext}",
            filetypes=filetypes
        )
        if not output_path:
            self.set_status("No save location selected.")
            return

        try:
            self.set_status("Compressing...")
            algo.compress(self.file_path, output_path)
            messagebox.showinfo("Success", f"File compressed successfully to {output_path}")
            self.set_status(f"File compressed to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.set_status("Compression failed.")

        if self.file_path.lower().endswith(".bmp"):
            # Show BMP options (you can use a StringVar or similar for user choice)
            # For example, let's assume you use self.bmp_option_var ("Low" or "High")
            option = getattr(self, "bmp_option_var", None)
            if option is None:
                # fallback: default to Low if not set
                mode = "Low"
            else:
                mode = self.bmp_option_var.get()
            ext = "png" if mode == "Low" else "jpg"
            filetypes = [("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All files", "*.*")]
            output_path = filedialog.asksaveasfilename(
                title="Save Converted Image As",
                defaultextension=f".{ext}",
                filetypes=filetypes
            )
            if not output_path:
                self.set_status("No save location selected.")
                return
            try:
                self.set_status("Converting...")
                bmp_algo.compress(self.file_path, output_path, mode=mode)
                messagebox.showinfo("Success", f"Image converted and saved to {output_path}")
                self.set_status(f"Image converted to {output_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                self.set_status("Conversion failed.")
            return

    def decompress_file(self):
        compressed_path = filedialog.askopenfilename(
            title="Select Compressed File",
            filetypes=[
                ("All Supported", "*.lzw *.huff *.rle *.zip *.bz2 *.xz"),
                ("LZW Compressed", "*.lzw"),
                ("Huffman Compressed", "*.huff"),
                ("RLE Compressed", "*.rle"),
                ("ZIP Archive", "*.zip"),
                ("BZIP2 Archive", "*.bz2"),
                ("LZMA Archive", "*.xz"),
                ("All files", "*.*"),
                
            ]
        )
        if not compressed_path:
            self.set_status("No compressed file selected.")
            return

        ext = os.path.splitext(compressed_path)[1].lower()
        # Map extension to algorithm and default output extension
        algo_map = {
            ".lzw": (lzw, ".txt"),
            ".huff": (huffman, ".txt"),
            ".rle": (rle, ".txt"),
            ".zip": (zip_algo, None),    # Will extract original file(s)
            ".bz2": (bz2_algo, ".pdf"),  # Could be .pdf or .doc, user may rename
            ".xz": (lzma_algo, ".pdf"),  # Could be .pdf or .doc, user may rename
        }

        if ext not in algo_map:
            messagebox.showerror("Error", "Unsupported compressed file format.")
            self.set_status("Unsupported file format.")
            return

        algo, default_ext = algo_map[ext]

        if ext == ".zip":
            extract_dir = filedialog.askdirectory(title="Select Folder to Extract Files")
            if not extract_dir:
                self.set_status("No extraction folder selected.")
                return
            try:
                self.set_status("Decompressing...")
                algo.decompress(compressed_path, extract_dir)
                messagebox.showinfo("Success", f"Files extracted to {extract_dir}")
                self.set_status(f"Files extracted to {extract_dir}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                self.set_status("Decompression failed.")
        else:
            save_path = filedialog.asksaveasfilename(
                title="Save Decompressed File As",
                defaultextension=default_ext,
                filetypes=[("All files", "*.*")]
            )
            if not save_path:
                self.set_status("No save location selected.")
                return
            try:
                self.set_status("Decompressing...")
                algo.decompress(compressed_path, save_path)
                messagebox.showinfo("Success", f"File decompressed to {save_path}")
                self.set_status(f"File decompressed to {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                self.set_status("Decompression failed.")

    def get_algo_and_ext(self, file_path, level):
        ext = os.path.splitext(file_path)[1].lower()
        # TXT files
        if ext == ".txt":
            if level == "High":
                return lzw, "lzw"
            elif level == "Low":
                return huffman, "huff"
            elif level == "Optimal":
                return rle, "rle"
        # PDF/DOC files
        elif ext in [".pdf", ".doc", ".docx"]:
            if level == "High":
                return lzma_algo, "xz"
            elif level == "Low":
                return zip_algo, "zip"
            elif level == "Optimal":
                return bz2_algo, "bz2"
        # Images (always use ZIP)
        elif ext in [".jpg", ".jpeg", ".png", ".bmp"]:
            return zip_algo, "zip"
        # Default fallback (use ZIP)
        else:
            return zip_algo, "zip"

def compress(input_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        arcname = os.path.basename(input_path)  # preserve original filename
        zipf.write(input_path, arcname=arcname)

def decompress(zip_path, extract_dir):
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_dir)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    style = ttk.Style(root)
    style.theme_use('clam')  # Use a modern theme

    # Custom styles for full background color
    style.configure("Custom.TFrame", background="#eaf6fb")
    style.configure("Custom.TRadiobutton", background="#eaf6fb")
    style.configure("TLabel", background="#eaf6fb")
    style.configure("TStatusbar", background="#eaf6fb")

    # Compress Button Style (Green, static)
    style.configure(
        "Compress.TButton",
        font=("Segoe UI", 10, "bold"),
        padding=8,
        borderwidth=0,
        relief="flat"
    )
    style.map(
        "Compress.TButton",
        background=[("active", "#66bb6a"), ("!active", "#66bb6a")],  # Static green
        foreground=[("active", "#0b3954"), ("!active", "#0b3954")]
    )

    # Select Button Style (Blue, static)
    style.configure(
        "Select.TButton",
        font=("Segoe UI", 10, "bold"),
        padding=8,
        borderwidth=0,
        relief="flat"
    )
    style.map(
        "Select.TButton",
        background=[("active", "#42a5f5"), ("!active", "#42a5f5")],  # Static blue
        foreground=[("active", "#ffffff"), ("!active", "#ffffff")]
    )

    app = CompressionApp(root)
    root.mainloop()