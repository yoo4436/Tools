import os
from pypdf import PdfReader, PdfWriter

def split_pdf(input_pdf_path, output_dir):
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)
    
    # 💡 防呆機制：如果這個輸出資料夾不存在，程式會自動幫你建立，不會報錯
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for page_num in range(total_pages):
        writer = PdfWriter()
        current_page = reader.pages[page_num]
        writer.add_page(current_page)
        
        # 💡 這裡將「資料夾路徑」和「新檔名」拼起來
        # 拼出來會長這樣：C:\Users\denny.ye\Desktop\郁智康\page_1.pdf
        output_filename = f"系統權限異動申請表-20260-{page_num + 1}.pdf"
        full_output_path = os.path.join(output_dir, output_filename)
        
        with open(full_output_path, "wb") as output_file:
            writer.write(output_file)
            
        print(f"已成功導出至：{full_output_path}")

if __name__ == "__main__":
    # 設定好你的輸入路徑與輸出資料夾
    target_dir = r"C:\Users\denny.ye\Desktop\郁智康"
    input_file = os.path.join(target_dir, "權限異動.pdf")
    
    # 執行時，把「檔案路徑」和「要存去的資料夾路徑」都傳進去
    split_pdf(input_file, target_dir)