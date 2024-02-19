<br />
<div align="center">
  <a href="https://github.com/404-NOT-FUN/discord-adventure-crawler">
    <img src="https://images-ext-2.discordapp.net/external/cotEtbF2MnMMuFJQ_RbBItvKPe-d38kRguZ-9-MeYrU/%3Fsize%3D1024/https/cdn.discordapp.com/icons/479923427965403137/a_6345fb6b77bf2070608d4dd4fd3e3b3b.gif?width=591&height=591" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Discord Adventure 爬蟲</h3>

  <p align="center">
    透過爬蟲自動輸入 <strong>/adventure</strong> 指令並參加討伐
    <br />
    <a href="https://github.com/404-NOT-FUN/discord-adventure-crawler/issues">回報問題</a>
    ·
    <a href="https://discord.gg/XXn5udJsPU">Discord</a>
  </p>
</div>

## 開始使用

<details>
<summary>透過原始碼 (需要安裝Python)</summary>

 - ### 如何安裝

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

 - ### 如何使用
   直接執行 `run.bat` 或透過以下指令:

    ```sh
    # 切換到專案目錄下
    cd .\discord-adventure-crawler\

    # 執行主程式
    poetry run python main.py
    ```

 - ### 如何打包專案為執行檔
   透過以下指令:

    ```sh
    # 切換到專案目錄下
    cd .\discord-adventure-crawler\

    # 打包
    pyinstaller --onedir --add-data "config.example.json;./" --add-data "icon.ico;./" --contents-directory "." --icon=icon.ico -n DcCrawler .\main.py
    ```

</details>

<details>
<summary>透過執行檔 (不需要安裝Python, 限Windows環境)</summary>

> **※ 可能會被防毒軟體誤判為惡意程式，請自行設為白名單**

 - ### 如何安裝

    前往<a href="https://github.com/404-NOT-FUN/discord-adventure-crawler/pulls">Release頁面</a>，下載最新的壓縮檔，檔名為DcCrawler.版本號_Windows.zip

 - ### 如何使用
   解壓縮後直接執行資料夾內的 `DcCrawler.exe`

</details>

## Config 參數說明
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

## 常見問題

   **Q: UI 能不能做得好看一點？**

   **A:** 不能，滾。

   **Q: 其他問題**

   **A:** 可以到 <strong><a href="https://discord.gg/XXn5udJsPU">Discord</a></strong> 來詢問。