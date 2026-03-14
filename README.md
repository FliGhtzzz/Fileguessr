# File Guessr 📂🔍

一個基於 **本地 AI (Ollama + Gemma 3 4B)** 與 **Elasticsearch** 的強大檔案搜尋工具。
你可以使用自然語言（例如：「紅色的跑車」、「上週的預算報告」）來搜尋電腦中的檔案，不再需要死記硬背檔名。

## ✨ 特色功能

- 🧠 **本地 AI 驅動**: 使用 `gemma3:4b` 模型，所有資料都在本地處理，隱私安全無虞。
- 🔍 **模糊搜尋**: 打錯字也能找到！Elasticsearch 提供強大的模糊匹配。
- 🖼️ **圖片理解**: 自動分析圖片內容並生成描述，讓圖片也能用文字搜尋。
- 📂 **快速定位**: 搜尋結果可一鍵打開檔案所在的 Windows 資料夾。
- ⚡ **智能排序**: Elasticsearch 多欄位加權 + BM25 相關性排序。
- 📂 **動態監控**: 自動偵測資料夾變更（新增/修改檔案），即時更新搜尋索引。
- 🚀 **一鍵部署**: 內附 `setup.bat` 與 `run.bat` 腳本，Windows 用戶可輕鬆安裝使用。

## 📋 系統需求

- **Windows 10/11**
- **Python 3.10+** (推薦 3.11)
- **Ollama** (需安裝並執行中)
  - 請至 [ollama.com](https://ollama.com/) 下載安裝
  - 安裝後執行 `ollama pull gemma3:4b` 下載模型
- **Elasticsearch 8.x+** (需安裝並執行中)
  - 請至 [elastic.co](https://www.elastic.co/downloads/elasticsearch) 下載
  - 解壓縮後執行 `bin\elasticsearch.bat` 啟動服務
  - 預設位址: `http://localhost:9200`

## 🚀 快速開始 (Windows)

為了確保程式正常運行，請按照以下順序操作：

1. **首次使用**：雙擊執行 **`setup.bat`**。
   - 這會自動建立虛擬環境、安裝套件，並嘗試偵測/配置你的 Elasticsearch。
2. **日常啟動**：雙擊執行 **`run.bat`** 或桌面的捷徑。
   - 這會檢查 Elasticsearch 與 Ollama 狀態，完成後會**自動關閉** CMD 視窗，並在系統托盤（右下角）運行服務。
   - 隨後會自動打開瀏覽器 `http://127.0.0.1:8000`。
3. **管理介面**：程式啟動後會在系統右下角托盤顯示圖示，可右鍵點擊「開啟網頁」、「重啟服務」或「退出」。

## 🛠️ 常見問題排除 (Troubleshooting)

### 1. 搜尋不到結果？
- **確認 Ollama 狀態**：在終端機執行 `ollama list`，確認 `gemma3:4b` 已下載且服務正在運行。
- **重新索引**：若檔案有大幅變動，可在 Settings 頁面點擊「Clear Index」後重新加入資料夾。
- **檢查日誌**：點擊網頁介面下方的「AI 引擎日誌」查看有無報錯。

### 2. 資料夾選擇器（Folder Picker）沒反應？
- **檢查視窗焦點**：有時選擇器視窗會彈在主瀏覽器視窗後方，請檢查工具列。
- **管理員權限**：若嘗試索引系統保護的資料夾，請嘗試以管理員身分點擊 `run.bat`。

### 3. Elasticsearch 連線失敗？
- 請確保你已手動下載並啟動 Elasticsearch。
- 預設位址應為 `http://localhost:9200`。如果是使用 HTTPS 且啟動了安全性（Security），請在 `setup.bat` 期間提供正確的 `elastic` 密碼。

## 📄 授權

MIT License
