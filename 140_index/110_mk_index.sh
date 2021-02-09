#【システム】BOAT_RACE_DB2
#【ファイル】110_mk_index.sh
#【機能仕様】ボートレース関連指数算出スクリプトの起動
#【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
#【来　　歴】2021.02.01 ver 1.00

#インストールディレクトリ
BASE_DIR=/home/pi/BOAT_RACE_DB
#成績用に昨日のレース一覧をダウンロード
#Mac OS
#YESTERDAY=`date -v -1d "+%Y%m%d"`
#Raspbian OS 10.4
YESTERDAY=`date --date '1 day ago' "+%Y%m%d"`
python3 $BASE_DIR/140_index/100_mk_index.py $YESTERDAY $YESTERDAY


