import os
import json
from tkinter import filedialog, messagebox
import customtkinter as ctk

# 設定外觀與主題
ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("blue") 

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
INTERNAL_DIR = os.path.join(CURRENT_DIR, "_internal")
HISTORY_FILE = os.path.join(INTERNAL_DIR, ".rename_history.json")

selected_files = []

def ensure_internal_dir():
    if not os.path.exists(INTERNAL_DIR):
        os.makedirs(INTERNAL_DIR)

def save_history_to_file(history_data):
    try:
        ensure_internal_dir()
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"儲存歷史紀錄失敗: {e}")

def load_history_from_file():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def delete_history_file():
    if os.path.exists(HISTORY_FILE):
        try:
            os.remove(HISTORY_FILE)
        except Exception as e:
            print(f"刪除紀錄檔失敗: {e}")

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
    global selected_files
    if not selected_files:
        messagebox.showwarning("警告", "請先選擇要處理的檔案！")
        return
        
    prefix = entry_prefix.get()
    suffix = entry_suffix.get()
    find_str = entry_find.get()
    replace_str = entry_replace.get()
    
    # 檢查防呆：如果什麼功能都沒填，就提出警告
    if not prefix and not suffix and not find_str:
        messagebox.showwarning("警告", "請至少輸入前綴、後綴或要取代的文字！")
        return

    success_count = 0
    error_count = 0
    current_rename_history = []

    for file_path in selected_files:
        if os.path.exists(file_path):
            dir_name = os.path.dirname(file_path)      
            base_name = os.path.basename(file_path)    
            file_name, file_ext = os.path.splitext(base_name) 
            
            # 核心取代邏輯：如果填了「尋找文字」，就執行取代
            if find_str:
                file_name = file_name.replace(find_str, replace_str)
            
            # 組合新檔名（前綴 + 處理後的檔名 + 後綴 + 副檔名）
            new_base_name = f"{prefix}{file_name}{suffix}{file_ext}"
            new_file_path = os.path.join(dir_name, new_base_name)
            
            if file_path == new_file_path:
                continue
                
            try:
                os.rename(file_path, new_file_path)
                current_rename_history.append([new_file_path, file_path])
                success_count += 1
            except Exception:
                error_count += 1

    messagebox.showinfo("處理完成", f"重新命名結束！\n成功：{success_count} 個\n失敗：{error_count} 個")
    
    if current_rename_history:
        save_history_to_file(current_rename_history)
        btn_undo.configure(state="normal", fg_color="#D9534F", hover_color="#C9302C")
    
    selected_files = []
    text_preview.delete("1.0", "end")
    lbl_status.configure(text="尚未選取檔案", text_color="gray")
    
    # 清空輸入框（選填，若想保留輸入可註解掉）
    entry_find.delete(0, "end")
    entry_replace.delete(0, "end")

def undo_rename():
    rename_history = load_history_from_file()
    
    if not rename_history:
        messagebox.showwarning("提示", "目前沒有可以還原的紀錄！")
        btn_undo.configure(state="disabled", fg_color="gray")
        return
        
    confirm = messagebox.askyesno("確認還原", f"您確定要將這 {len(rename_history)} 個檔案還原為上一步的名稱嗎？")
    if not confirm:
        return

    undo_success = 0
    restored_names = []
    
    for new_path, old_path in rename_history:
        try:
            if os.path.exists(new_path):
                os.rename(new_path, old_path)
                undo_success += 1
                restored_names.append(os.path.basename(old_path))
        except Exception:
            pass
            
    text_preview.delete("1.0", "end")
    text_preview.insert("end", "--- 已成功還原以下檔案的名稱 ---\n")
    for name in restored_names:
        text_preview.insert("end", f"{name}\n")
        
    lbl_status.configure(text=f"已成功還原 {undo_success} 個檔案", text_color="#23b074")
    messagebox.showinfo("還原完成", f"已執行還原！\n成功還原：{undo_success} 個檔案")
    
    delete_history_file()
    btn_undo.configure(state="disabled", fg_color="gray")

def check_existing_history():
    if os.path.exists(HISTORY_FILE):
        btn_undo.configure(state="normal", fg_color="#D9534F", hover_color="#C9302C")

# ================= 建立 CustomTkinter 視窗 =================
root = ctk.CTk()
root.title("檔案批次重新命名工具 v1.2")
root.geometry("620x580") # 稍微拉高視窗以容納新欄位
root.resizable(False, False)

# 1. 選擇檔案區
btn_browse = ctk.CTkButton(root, text="選取檔案 (可多選)", width=150, corner_radius=8, command=select_files)
btn_browse.pack(pady=15)

lbl_status = ctk.CTkLabel(root, text="尚未選取檔案", font=("Arial", 12), text_color="gray")
lbl_status.pack()

# 2. 檔案預覽區
lbl_preview = ctk.CTkLabel(root, text="檔案清單預覽 / 還原狀態顯示：", font=("Arial", 12, "bold"))
lbl_preview.pack(anchor="w", padx=40, pady=(10, 2))

text_preview = ctk.CTkTextbox(root, width=540, height=140, corner_radius=8)
text_preview.pack(pady=5)

# 3. 命名參數設定區（包含舊功能與新功能）
frame_settings = ctk.CTkFrame(root, fg_color="transparent")
frame_settings.pack(pady=10)

# --- 功能：加前後綴 ---
lbl_prefix = ctk.CTkLabel(frame_settings, text="加前綴 (Prefix):", font=("Arial", 12))
lbl_prefix.grid(row=0, column=0, padx=10, pady=8, sticky="e")
entry_prefix = ctk.CTkEntry(frame_settings, width=150, corner_radius=8, placeholder_text="不加請留空")
entry_prefix.grid(row=0, column=1, padx=5, pady=8)

lbl_suffix = ctk.CTkLabel(frame_settings, text="加後綴 (Suffix):", font=("Arial", 12))
lbl_suffix.grid(row=0, column=2, padx=10, pady=8, sticky="e")
entry_suffix = ctk.CTkEntry(frame_settings, width=150, corner_radius=8, placeholder_text="不加請留空")
entry_suffix.grid(row=0, column=3, padx=5, pady=8)

# --- 功能：文字取代區 (Find & Replace) ---
lbl_find = ctk.CTkLabel(frame_settings, text="搜尋文字 (Find):", font=("Arial", 12, "bold"), text_color="#D9534F")
lbl_find.grid(row=1, column=0, padx=10, pady=8, sticky="e")
entry_find = ctk.CTkEntry(frame_settings, width=150, corner_radius=8, placeholder_text="例如: CE-102-1")
entry_find.grid(row=1, column=1, padx=5, pady=8)

lbl_replace = ctk.CTkLabel(frame_settings, text="取代為 (Replace):", font=("Arial", 12, "bold"), text_color="#23b074")
lbl_replace.grid(row=1, column=2, padx=10, pady=8, sticky="e")
entry_replace = ctk.CTkEntry(frame_settings, width=150, corner_radius=8, placeholder_text="例如: CE-106-3")
entry_replace.grid(row=1, column=3, padx=5, pady=8)


# 4. 按鈕控制區
frame_buttons = ctk.CTkFrame(root, fg_color="transparent")
frame_buttons.pack(pady=20)

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

check_existing_history()

root.mainloop()