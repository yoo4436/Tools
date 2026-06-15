# 🧰 Denny's Dev Toolbox (個人專屬實用工具箱)

這裡是我在日常開發與練習過程中，為了自動化解決特定需求而編寫的各種輕量小工具。
本儲存庫採用「多功能工具箱」概念維護，未來將陸續更新與擴充更多實用程式！

---

## 🚀 快速下載通道

為了方便使用，所有工具皆已透過 **GitHub Releases** 打包為獨立的免安裝執行檔（`.exe` 壓縮包）。你不需要安裝 Python 環境即可直接使用！

* 👉 **([前往 Release 頁面下載最新版工具](https://github.com/yoo4436/Tools/releases))**

---

## 🛠️ 工具清單 (Tools Summary)

### 1. 📄 PDF 頁面自動切割工具 (`splitPDFComplete.py`)
* **主要用途**：內建現代化 GUI 介面，支援自由設定前綴檔名，將大型 PDF 無損拆分為單頁檔案。
* **開發依賴**：`customtkinter`, `pypdf`
* **詳細說明與舊版載點**：可參閱 `v1.0` 發佈說明。

---

## 💻 本地二次開發

如果你想直接執行原始碼，或對現有程式碼進行優化，請先在本機安裝所有相依套件：

```bash
pip install customtkinter pypdf
