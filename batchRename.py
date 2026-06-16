import os
from tkinter import filedialog, messagebox
import customtkinter as ctk

# 設定外觀與主題
ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("blue") 

# 全域變數
selected_files = []
# 用來記錄上一次改名的歷史紀錄，格式為：[(新路徑1, 舊路徑1), (新路徑2, 舊路徑2), ...]
rename_history = []

def select_files():
    global selected_files
    files = filedialog.askopenfilenames(
        title="請選擇要重新命名的檔案 (可多選)",
        filetypes=[("All Files", "*.*")]
    )
    if files:
        selected_files = list(files)
        text_preview.delete("1.0", "end")
        for f in selected_files:
            text_preview.insert("end", f"{os.path.basename(f)}\n")
        lbl_status.configure(text=f"已選取 {len(selected_files)} 個檔案", text_color="#0078D7")

def run_rename():
    global selected_files, rename_history
    if not selected_files:
        messagebox.showwarning("警告", "請先選擇要處理的檔案！")
        return
        
    prefix = entry_prefix.get()
    suffix = entry_suffix.get()
    
    if not prefix and not suffix:
        messagebox.showwarning("警告", "請至少輸入前綴或後綴其中一種！")
        return

    success_count = 0
    error_count = 0
    
    # 每次開始新改名時，先清空上一次的歷史紀錄
    rename_history = []

    for file_path in selected_files:
        if os.path.exists(file_path):
            dir_name = os.path.dirname(file_path)      
            base_name = os.path.basename(file_path)    
            file_name, file_ext = os.path.splitext(base_name) 
            
            new_base_name = f"{prefix}{file_name}{suffix}{file_ext}"
            new_file_path = os.path.join(dir_name, new_base_name)
            
            # 如果新舊名稱完全一樣，就跳過不做
            if file_path == new_file_path:
                continue
                
            try:
                os.rename(file_path, new_file_path)
                # 成功改名後，記錄下來（注意：復原時是要從 新路徑 改回 舊路徑）
                rename_history.append((new_file_path, file_path))
                success_count += 1
            except Exception:
                error_count += 1

    messagebox.showinfo("處理完成", f"重新命名結束！\n成功：{success_count} 個\n失敗：{error_count} 個")
    
    # 重新命名成功後，啟用「還原」按鈕
    if rename_history:
        btn_undo.configure(state="normal", fg_color="#D9534F", hover_color="#C9302C")
    
    # 清空選擇列表與預覽，方便下一波操作
    selected_files = []
    text_preview.delete("1.0", "end")
    lbl_status.configure(text="尚未選取檔案", text_color="gray")

# 新增：還原上一步的邏輯
def undo_rename():
    global rename_history
    if not rename_history:
        messagebox.showwarning("提示", "目前沒有可以還原的紀錄！")
        return
        
    undo_success = 0
    undo_error = 0
    
    # 從最新的紀錄開始倒回去改名字
    for new_path, old_path in rename_history:
        try:
            if os.path.exists(new_path):
                os.rename(new_path, old_path)
                undo_success += 1
        except Exception:
            undo_error += 1
            
    messagebox.showinfo("還原完成", f"已執行還原！\n成功還原：{undo_success} 個檔案")
    
    # 還原後清空歷史紀錄，並禁用還原按鈕
    rename_history = []
    btn_undo.configure(state="disabled", fg_color="gray")

# ================= 建立 CustomTkinter 視窗 =================
root = ctk.CTk()
root.title("檔案批次重新命名工具 (內建復原功能)")
root.geometry("600x520")
root.resizable(False, False)

# 1. 選擇檔案區
btn_browse = ctk.CTkButton(root, text="選取檔案 (可多選)", width=150, corner_radius=8, command=select_files)
btn_browse.pack(pady=15)

lbl_status = ctk.CTkLabel(root, text="尚未選取檔案", font=("Arial", 12), text_color="gray")
lbl_status.pack()

# 2. 檔案預覽區
lbl_preview = ctk.CTkLabel(root, text="已選取的檔案清單預覽：", font=("Arial", 12, "bold"))
lbl_preview.pack(anchor="w", padx=40, pady=(10, 2))

text_preview = ctk.CTkTextbox(root, width=520, height=150, corner_radius=8)
text_preview.pack(pady=5)

# 3. 命名參數設定區
frame_settings = ctk.CTkFrame(root, fg_color="transparent")
frame_settings.pack(pady=15)

lbl_prefix = ctk.CTkLabel(frame_settings, text="加前綴 (Prefix):", font=("Arial", 12))
lbl_prefix.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_prefix = ctk.CTkEntry(frame_settings, width=150, corner_radius=8, placeholder_text="例如: CE-102-1 ")
entry_prefix.grid(row=0, column=1, padx=5, pady=5)

lbl_suffix = ctk.CTkLabel(frame_settings, text="加後綴 (Suffix):", font=("Arial", 12))
lbl_suffix.grid(row=0, column=2, padx=10, pady=5, sticky="e")
entry_suffix = ctk.CTkEntry(frame_settings, width=150, corner_radius=8, placeholder_text="例如: -已確認")
entry_suffix.grid(row=0, column=3, padx=5, pady=5)

# 4. 按鈕控制區（放一左一右，排版更好看）
frame_buttons = ctk.CTkFrame(root, fg_color="transparent")
frame_buttons.pack(pady=20)

# 執行改名按鈕 (藍色)
btn_run = ctk.CTkButton(
    frame_buttons, 
    text="開始批次重新命名", 
    fg_color="#0078D7",      
    hover_color="#005A9E",   
    height=42,
    width=180,
    corner_radius=20,
    font=("Arial", 14, "bold"),
    command=run_rename
)
btn_run.grid(row=0, column=0, padx=15)

# 復原按鈕 (平常是灰色的不能點，只有在剛改完名後會變成紅色可點擊)
btn_undo = ctk.CTkButton(
    frame_buttons, 
    text="↩ 還原上一步", 
    fg_color="gray",      
    state="disabled",
    height=42,
    width=150,
    corner_radius=20,
    font=("Arial", 14, "bold"),
    command=undo_rename
)
btn_undo.grid(row=0, column=1, padx=15)

root.mainloop()