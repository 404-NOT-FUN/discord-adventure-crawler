- ## Setup
    ```poetry install```

- ## Build
    ```pyinstaller --add-data "config.ini;.\config.ini" .\DcCrawler.py -F --exclude-module _bootlocale```
