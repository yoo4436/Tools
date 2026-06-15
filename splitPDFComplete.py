import os
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter
# 💡 改用 customtkinter 庫：請先在終端機輸入 pip install customtkinter
import customtkinter as ctk

# 設定外觀與主題
ctk.set_appearance_mode("Light")  # 可設定 "System" (跟隨系統), "Dark", "Light"
ctk.set_default_color_theme("blue") # 內建顏色主題: "blue", "green", "dark-blue"

def select_file():
    file_path = filedialog.askopenfilename(
        title="請選擇要切割的 PDF 檔案",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if file_path:
        entry_file_path.delete(0, "end")
        entry_file_path.insert(0, file_path)

def select_output_dir():
    dir_path = filedialog.askdirectory(title="請選擇輸出資料夾")
    if dir_path:
        entry_output_dir.delete(0, "end")
        entry_output_dir.insert(0, dir_path)

def run_process():
    input_file = entry_file_path.get()
    output_dir = entry_output_dir.get()
    prefix_name = entry_prefix_name.get()
    
    if not input_file or not output_dir or not prefix_name:
        messagebox.showwarning("警告", "請確保所有欄位皆已填寫！")
        return

    try:
        reader = PdfReader(input_file)
        total_pages = len(reader.pages)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for page_num in range(total_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num])
            output_filename = f"{prefix_name}-{page_num + 1}.pdf"
            full_output_path = os.path.join(output_dir, output_filename)
            with open(full_output_path, "wb") as f:
                writer.write(f)
        
        messagebox.showinfo("成功", f"PDF 切割完成！共切出 {total_pages} 頁。")
    except Exception as e:
        messagebox.showerror("錯誤", f"發生錯誤：\n{str(e)}")

# ================= 建立 CustomTkinter 視窗 =================
root = ctk.CTk()
root.title("PDF 頁面自動切割工具")
root.geometry("560x260")
root.resizable(False, False)

# 1. 選擇輸入 PDF 檔案
lbl_file = ctk.CTkLabel(root, text="選擇 PDF 檔案:", font=("Arial", 12))
lbl_file.grid(row=0, column=0, padx=15, pady=20, sticky="e")

entry_file_path = ctk.CTkEntry(root, width=260, corner_radius=8) # 💡 輸入框也可以改圓角
entry_file_path.grid(row=0, column=1, padx=5, pady=20)

# 💡 corner_radius=8 就是設定圓角！如果設為 20 就會變成兩頭圓弧的膠囊狀按鈕
btn_browse_file = ctk.CTkButton(root, text="瀏覽...", width=80, corner_radius=8, command=select_file)
btn_browse_file.grid(row=0, column=2, padx=5, pady=20)

# 2. 選擇輸出資料夾
lbl_dir = ctk.CTkLabel(root, text="輸出資料夾:", font=("Arial", 12))
lbl_dir.grid(row=1, column=0, padx=15, pady=10, sticky="e")

entry_output_dir = ctk.CTkEntry(root, width=260, corner_radius=8)
entry_output_dir.grid(row=1, column=1, padx=5, pady=10)

btn_browse_dir = ctk.CTkButton(root, text="瀏覽...", width=80, corner_radius=8, command=select_output_dir)
btn_browse_dir.grid(row=1, column=2, padx=5, pady=10)

# 3. 輸入輸出檔名前綴
lbl_prefix = ctk.CTkLabel(root, text="輸出檔名前綴:", font=("Arial", 12))
lbl_prefix.grid(row=2, column=0, padx=15, pady=10, sticky="e")

entry_prefix_name = ctk.CTkEntry(root, width=200, corner_radius=8)
entry_prefix_name.grid(row=2, column=1, padx=5, pady=10, sticky="w")

# 4. 開始切割按鈕 (使用綠色膠囊形大按鈕)
btn_run = ctk.CTkButton(
    root, 
    text="開始切割 PDF", 
    fg_color="#23b074",      # 按鈕顏色 (綠色)
    hover_color="#1b8a5a",   # 滑鼠移上去的深綠色
    height=40,
    width=180,
    corner_radius=20,        # 💡 數字加大，直接變身超漂亮圓角膠囊按鈕！
    font=("Arial", 14, "bold"),
    command=run_process
)
btn_run.grid(row=3, column=1, pady=20)

root.mainloop()