import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pypdf import PdfReader, PdfWriter


def select_file():
    # 💡 這裡修改了！篩選器改成只抓 PDF 檔案，讓操作更直覺
    file_path = filedialog.askopenfilename(
        title="請選擇要切割的 PDF 檔案",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

def select_output_dir():
    # 讓使用者可以自由選擇切好的檔案要存去哪裡
    dir_path = filedialog.askdirectory(title="請選擇輸出資料夾")
    if dir_path:
        entry_output_dir.delete(0, tk.END)
        entry_output_dir.insert(0, dir_path)

def run_process():
    input_file = entry_file_path.get()
    output_dir = entry_output_dir.get()
    prefix_name = entry_prefix_name.get()
    
    # 基本防呆檢查
    if not input_file:
        messagebox.showwarning("警告", "請先選擇輸入的 PDF 檔案！")
        return
    if not output_dir:
        messagebox.showwarning("警告", "請選擇輸出資料夾！")
        return
    if not prefix_name:
        messagebox.showwarning("警告", "請輸入輸出的檔案前綴名稱！")
        return

    try:
        # ====== 這裡完全融入你原本 splitPDF.py 的核心邏輯 ======
        reader = PdfReader(input_file)
        total_pages = len(reader.pages)
        
        # 如果輸出資料夾不存在就建立
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 開始逐頁切割
        for page_num in range(total_pages):
            writer = PdfWriter()
            current_page = reader.pages[page_num]
            writer.add_page(current_page)
            
            # 根據使用者輸入的前綴與頁碼動態生成檔名
            output_filename = f"{prefix_name}-{page_num + 1}.pdf"
            full_output_path = os.path.join(output_dir, output_filename)
            
            with open(full_output_path, "wb") as output_file:
                writer.write(output_file)
        # ====================================================
        
        # 成功提示
        messagebox.showinfo("成功", f"PDF 切割完成！\n共切出 {total_pages} 頁，已存至指定資料夾。")
        
    except Exception as e:
        messagebox.showerror("錯誤", f"處理 PDF 時發生錯誤：\n{str(e)}")

# ================= 建立 UI 視窗 =================
root = tk.Tk()
root.title("PDF 頁面自動切割工具")
root.geometry("520x250")
root.resizable(False, False) # 固定視窗大小

# 1. 選擇輸入 PDF 檔案
lbl_file = tk.Label(root, text="選擇 PDF 檔案:")
lbl_file.grid(row=0, column=0, padx=10, pady=15, sticky="e")

entry_file_path = tk.Entry(root, width=38)
entry_file_path.grid(row=0, column=1, padx=5, pady=15)

btn_browse_file = tk.Button(root, text="瀏覽...", command=select_file)
btn_browse_file.grid(row=0, column=2, padx=5, pady=15)

# 2. 選擇輸出資料夾
lbl_dir = tk.Label(root, text="輸出資料夾:")
lbl_dir.grid(row=1, column=0, padx=10, pady=10, sticky="e")

entry_output_dir = tk.Entry(root, width=38)
entry_output_dir.grid(row=1, column=1, padx=5, pady=10)

btn_browse_dir = tk.Button(root, text="瀏覽...", command=select_output_dir)
btn_browse_dir.grid(row=1, column=2, padx=5, pady=10)

# 3. 輸入輸出檔名錶綴（取代原本寫死的 "系統權限異動申請表-20260"）
lbl_prefix = tk.Label(root, text="輸出檔名前綴:")
lbl_prefix.grid(row=2, column=0, padx=10, pady=10, sticky="e")

entry_prefix_name = tk.Entry(root, width=25)
entry_prefix_name.grid(row=2, column=1, padx=5, pady=10, sticky="w")

# 4. 開始切割按鈕
btn_run = tk.Button(root, text="開始切割 PDF", command=run_process, bg="#0078D7", fg="white", font=("Arial", 11, "bold"), width=15, height=1)
btn_run.grid(row=3, column=1, pady=20)

# 啟動視窗迴圈
root.mainloop()