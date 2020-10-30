# Python - scraping

This program check the stock by scraping with Python.

If you register the command to exec this script with cron or a similar service, you can check the stock.

If you use cron ...

1. exec `crontab -e`

2. register the exec command. "*/5" means execute the command every 5 minutes.
```
# min hour day month week command
*/5 * * * * python3 scraping.py
```


References:

- [ニンテンドースイッチの入荷をGmailで教えてくれるbotを作ってみた。(Python スクレイピング)*無料](https://note.com/yuta_ebayer/n/n13a62b327cfc)
- [Pythonで文字列を検索（〜を含むか判定、位置取得、カウント）](https://note.nkmk.me/python-str-search/)
- [Pythonで現在の日時を取得して指定のフォーマットの文字列に変換する](https://tonari-it.com/python-datetime-now/)
- [Pythonでファイルの読み込み、書き込み（作成・追記）](https://note.nkmk.me/python-file-io-open-with/)
- [Beautiful Soup Documentation - find](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find)
- [Pythonで一定時間ごとに処理を実行する](https://qiita.com/kurogelee/items/0e5fd8b6a1d1f169179a)
- [Pythonでメール(gmail)を送信できない場合の解決法](https://www.gocca.work/python-mailerror/)
- [初心者向けcronの使い方](https://qiita.com/tossh/items/e135bd063a50087c3d6a)
