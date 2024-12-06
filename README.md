# Bello

## 開發環境

- Windows 11

- Python: 3.10.9

  - psycopg2: 2.9.10
  - python-dotenv: 1.0.1
  - tabulate: 0.9.0

- PostgreSQL: 16.6

## 使用方法
- 將.env.example 複製一份並改名為 .env 後填入相關資訊
- 安裝相關套件 
    ```bash
    pip install -r requirements.txt
    ```
- 使用sql file `init_bello_db.sql` 復原資料庫
    ```bash
    psql -U <username> -f init_bello_db.sql
    ```

先執行 `server.py` 啟動伺服器：

```bash
python .\server.py 
```

再透過 `client.py` 向伺服器連線：

```bash
python .\client.py 
```



## 程式說明

1. **`./server.py`**
   - 包含伺服器端的主要功能。
   - 在連接資料庫後，透過 socket 建立監聽服務，接收來自客戶端的連線請求。
   - 每當接收到一個客戶端連線，會啟動一個獨立的執行緒（thread）處理該連線，確保伺服器能並行處理多個客戶端。
2. **`./client.py`**
   - 包含客戶端的主要功能。
   - 持續從伺服器接收訊息並顯示於終端機。
   - 使用 Tag 標籤處理不同類型的伺服器回應
3. **`./DB_utils.py`**
   - 封裝與資料庫相關的功能，包含資料庫連線管理與查詢操作。
4. **`./action` 資料夾**
   - 基於抽象類別 `Action` 實現
   - 主要功能：
     * 用戶管理（註冊、登入）
     * 個人資料維護
     * 聚會管理
     * 即時通訊
5. **`./role` 資料夾**
   - 基於 `Role` 基礎類別
   - 實現三種角色：
     * 訪客 (Visitor)：登入、註冊功能
     * 用戶 (User)：完整聚會功能
     * 管理員 (Admin)：系統管理功能