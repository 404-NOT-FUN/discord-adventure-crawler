- ## Install poetry
    ```pip install poetry```

- ## Setup
    ```poetry install```

- ## Activate the virtual environment with poetry and run the crawler
    ```poetry run python DcCrawler.py```

- ## Build
    ```pyinstaller --add-data "config.ini;.\config.ini" .\DcCrawler.py -F --exclude-module _bootlocale```
