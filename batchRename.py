import os
from tkinter import filedialog, messagebox
import customtkinter as ctk

# 設定外觀與主題
ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("blue") 

# 全域變數，用來儲存使用者選取的檔案路徑清單
selected_files = []

def select_files():
    global selected_files
    # 💡 注意這裡使用 askopenfilenames (複數)，允許使用者一次選取多個檔案
    files = filedialog.askopenfilenames(
        title="請選擇要重新命名的檔案 (可多選)",
        filetypes=[("All Files", "*.*")]
    )
    if files:
        selected_files = list(files)
        # 更新介面上的預覽文字框
        text_preview.delete("1.0", "end")
        for f in selected_files:
            text_preview.insert("end", f"{os.path.basename(f)}\n")
        lbl_status.configure(text=f"已選取 {len(selected_files)} 個檔案", text_color="#0078D7")

def run_rename():
    global selected_files
    if not selected_files:
        messagebox.showwarning("警告", "請先選擇要處理的檔案！")
        return
        
    prefix = entry_prefix.get()
    suffix = entry_suffix.get()
    
    # 如果前後綴都沒填，就不用浪費時間跑了
    if not prefix and not suffix:
        messagebox.showwarning("警告", "請至少輸入前綴或後綴其中一種！")
        return

    success_count = 0
    error_count = 0

    for file_path in selected_files:
        if os.path.exists(file_path):
            dir_name = os.path.dirname(file_path)      # 取得資料夾路徑
            base_name = os.path.basename(file_path)    # 取得完整檔名 (例如: text.txt)
            file_name, file_ext = os.path.splitext(base_name) # 切開檔名與副檔名 (text, .txt)
            
            # 💡 核心改名邏輯：新檔名 = 前綴 + 原檔名 + 後綴 + 副檔名
            new_base_name = f"{prefix}{file_name}{suffix}{file_ext}"
            new_file_path = os.path.join(dir_name, new_base_name)
            
            try:
                os.rename(file_path, new_file_path)
                success_count += 1
            except Exception:
                error_count += 1

    messagebox.showinfo("處理完成", f"重新命名結束！\n成功：{success_count} 個\n失敗：{error_count} 個")
    
    # 處理完後清空列表與預覽
    selected_files = []
    text_preview.delete("1.0", "end")
    lbl_status.configure(text="尚未選取檔案", text_color="gray")
    entry_prefix.delete(0, "end")
    entry_suffix.delete(0, "end")

# ================= 建立 CustomTkinter 視窗 =================
root = ctk.CTk()
root.title("檔案批次重新命名工具")
root.geometry("600x480")
root.resizable(False, False)

# 1. 選擇檔案區
btn_browse = ctk.CTkButton(root, text="選取檔案 (可多選)", width=150, corner_radius=8, command=select_files)
btn_browse.pack(pady=15)

lbl_status = ctk.CTkLabel(root, text="尚未選取檔案", font=("Arial", 12), text_color="gray")
lbl_status.pack()

# 2. 檔案預覽區 (多行文字方塊)
lbl_preview = ctk.CTkLabel(root, text="已選取的檔案清單預覽：", font=("Arial", 12, "bold"))
lbl_preview.pack(anchor="w", padx=40, pady=(10, 2))

text_preview = ctk.CTkTextbox(root, width=520, height=150, corner_radius=8)
text_preview.pack(pady=5)

# 3. 命名參數設定區 (用一個內嵌框架排版，看起來更整齊)
frame_settings = ctk.CTkFrame(root, fg_color="transparent")
frame_settings.pack(pady=15)

lbl_prefix = ctk.CTkLabel(frame_settings, text="加前綴 (Prefix):", font=("Arial", 12))
lbl_prefix.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_prefix = ctk.CTkEntry(frame_settings, width=150, corner_radius=8, placeholder_text="例如: 2026XXXX ")
entry_prefix.grid(row=0, column=1, padx=5, pady=5)

lbl_suffix = ctk.CTkLabel(frame_settings, text="加後綴 (Suffix):", font=("Arial", 12))
lbl_suffix.grid(row=0, column=2, padx=10, pady=5, sticky="e")
entry_suffix = ctk.CTkEntry(frame_settings, width=150, corner_radius=8, placeholder_text="例如: -2026XXXX")
entry_suffix.grid(row=0, column=3, padx=5, pady=5)

# 4. 開始執行按鈕
btn_run = ctk.CTkButton(
    root, 
    text="開始批次重新命名", 
    fg_color="#0078D7",      
    hover_color="#005A9E",   
    height=42,
    width=200,
    corner_radius=20,        # 經典漂亮膠囊型按鈕
    font=("Arial", 14, "bold"),
    command=run_rename
)
btn_run.pack(pady=20)

root.mainloop()