#【システム】BOAT_RACE_DB2
#【ファイル】001_get_race_list.sh
#【機能仕様】成績用に昨日のレース一覧、予想用に当日のレース一覧をダウンロードする
#【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
#【来　　歴】2021.02.01 ver 1.00

#インストールディレクトリ
BASE_DIR=/home/pi/BOAT_RACE_DB
#成績用に昨日のレース一覧をダウンロード
#Mac OS
#YESTERDAY=`date -v -1d "+%Y%m%d"`
#Raspbian OS 10.4
YESTERDAY=`date --date '1 day ago' "+%Y%m%d"`
curl https://www.boatrace.jp/owpc/pc/race/index?hd=$YESTERDAY -o $BASE_DIR/200_html/yesterday/$YESTERDAY.html
#予想用に当日のレース一覧をダウンロード
#Mac OS
#TODAY=`date -v -0d "+%Y%m%d"` #Mac OS
#Raspbian OS 10.4
TODAY=`date --date '0 day ago' "+%Y%m%d"`
curl https://www.boatrace.jp/owpc/pc/race/index?hd=$TODAY -o $BASE_DIR/200_html/today/$TODAY.html
