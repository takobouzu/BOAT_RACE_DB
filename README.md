# BOAT_RACE_DB

BOAT_RACE_DBは、[BOATRACEオフィシャルサイト](https://www.boatrace.jp/)から、ボートレースに関する情報をスクレイピングして、データーベースを構築するpython3スクリプトである。

# 目次

- [動作環境](#動作環境)
- [インストールと初期設定](#インストールと初期設定)
- [データ検索方法](#データ検索方法)
- [スクリプトファイル構造・データベーステーブル構造および活用方法や検索SQLサンプル等はWikiに掲載](https://github.com/takobouzu/BOAT_RACE_DB/wiki)
- [バグフィックスとエンハンス](#バグフィックスとエンハンス)
- [ライセンス](#ライセンス)

# 動作環境

Python3とSQLite3が動作するLinux系OSで動作する。Windows系OSでも、ファイル拡張子「.sh」のシェルスクリプトをPowerShellなどに書き換えることで動作させることが可能である。

筆者はRaspberry Pi 4 Model B/8GB(Raspbian OS)で運用している。

Raspberry Piで構築したデーターベースをMac mini(macOS)とiPad(iOS)でデーター分析及び予想に活用している。

## Raspbian OSにおける動作環境

| OS/パッケージ      | バージョン | 用途                   |
| ------------------ | ---------- | ---------------------- |
| Raspbian OS        | 12.3.1     | OS                     |
| python3            | 3.7.3      | python3本体            |
| beautifulsoup4     | 4.7.1      | python3 HTMLパーサー   |
| python-dateutil    | 2.8.1      | python3 日付ライブラリ |
| sqlite3            | 3.27.2     | SQLite3 データーベース |

## mac OSにおける動作環境
| OS/パッケージ         | バージョン | 用途                   |
| --------------------- | ---------- | ---------------------- |
| macOS 11.1            | 11.1       | OS                     |
| python3               | 3.9.1      | python3本体            |
| beautifulsoup4        | 4.9.3      | python3 HTMLパーサー   |
| python-dateutil       | 2.8.1      | python3 日付ライブラリ |
| DB Browser for SQLite | 3.12.0     | SQLite3クライアント    |
| sqlite3               | 3.32.3     | SQLite3 データーベース |

# インストールと初期設定
Raspberry Pi 4 Model B/8GB(Raspbian OS)で運用する前提で、インストールおよび初期設定を記載する。
macOSで運用する際の相違点は別途記載する。

## リポジトリーをcloneする。
ディレクトリ /home/pi直下にリポジトリーをcloneする。

```
git clone https://github.com/takobouzu/BOAT_RACE_DB.git
```

## 各フォルダーの配下に格納されているファイル「gitkeep」を削除する。

## crontabにBOATRACEオフィシャルサイトからデーターを取り込むスクリプトをスケジューリングする。
コマンド「crontab -e」で定義ファイルを起動して下記の設定を追加する。

午前08時00分にデーター取込スクリプトを起動する定義。
```
00 08 * * * sh /home/pi/BOAT_RACE_DB/000_sh/000_get_data.sh
```
※リポジトリーのclone先を/home/pi以外に設定した場合は、crontabの定義をインストール先のパスに変更し、各スクリプトに定義している「BASE_DIR=/home/pi」の定義を変更する。

## macOSで使用する場合の相違点

Raspbian OSとmacOSでは、dateコマンドのオプションが異なるため、dateコマンドを使用しているファイル「/home/pi/BOAT_RACE_DB/100_get_race_list/001_get_race_list.sh」のdateコマンドを書き換える必要がある。

| Raspbian OS   | macOS             |
| ------------- | ---------------- |
|YESTERDAY=`date --date '1 day ago' "+%Y%m%d"`|YESTERDAY=`date -v -1d "+%Y%m%d"`|
|TODAY=`date --date '0 day ago' "+%Y%m%d"`    |TODAY=`date -v -0d "+%Y%m%d"`|

## 場コードマスタ登録
スクリプト「/home/pi/BOAT_RACE_DB/310_tools/110_m_pool_code/m_pool_code_import.sh」を実行して、場コードマスタをデーターベースに登録する。

## 選手マスタ登録
スクリプト「/home/pi/BOAT_RACE_DB/310_tools/120_m_player/m_player_import.sh」を実行して、選手マスタをデーターベースに登録する。


# データ検索方法

DB Browser for SQLiteで、./200_db/boatrace.dbをオープン後に、タブ[Execute SQL]を選択して、SQLを入力後に実行することでデータ検索できる。

SQLite3をサポートしているライブラリやドライバーを使うことで、EXCELやプログラミング言語からもデータ検索が可能である。

![DB Browser for SQLite](https://user-images.githubusercontent.com/24547343/82280700-6c70d980-99ca-11ea-937d-0517dbba0967.jpg)

# バグフィックスとエンハンス

バグフィックスとエンハンスバグフィックスとエンハンスバグフィックスとエンハンスに関しては、()


# ライセンス

MIT License.

Copyright (c) 2021 蛸坊主/たこぼうず
