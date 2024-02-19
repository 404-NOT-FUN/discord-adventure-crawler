# Discord Adventure 爬蟲

透過爬蟲自動輸入 `/adventure` 指令並參加討伐

 - ## 如何安裝

    **※ 需要 >=3.8, <3.13 版本的 Python**

    Clone 這個專案，或是直接下載壓縮檔:

    ```sh
    git clone git@github.com:404-NOT-FUN/discord-adventure-crawler.git
    ```

    安裝執行環境:

    ```sh
    # 切換到專案目錄下
    cd .\discord-adventure-crawler\

    # 安裝 Poetry 環境管理套件
    pip install poetry

    # 安裝專案需要的套件
    poetry install
    ```

 - ## 如何使用
   直接執行 `run.bat` 或透過以下指令:

    ```sh
    # 切換到專案目錄下
    cd .\discord-adventure-crawler\

    # 執行主程式
    poetry run python main.py
    ```

 - ## 如何打包專案為執行檔，以便在沒有安裝Python的環境下執行
   透過以下指令:

    ```sh
    # 切換到專案目錄下
    cd .\discord-adventure-crawler\

    # 打包
    pyinstaller -D --add-data "config.example.json;./" -n DcCrawler .\main.py
    ```

 - ## Config 參數說明
   - url
      - 使用指令的頻道 URL
   - wait_seconds
      - 到達目標url畫面前的最長等待時間，若超過時間就會重整頁面
         - 限用整數
   - retry
      - 最高重整次數，超過後便會結束瀏覽器
         - 限用整數
   - inprivate
      - 是否用無痕開啟分頁
         - true/false
   - send_msg
      - 是否要送出 `/adventure` 指令
         - true/false

 - ## 常見問題

    **Q: 打包後無法執行**

    **A:** 