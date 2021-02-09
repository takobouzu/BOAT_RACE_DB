#【システム】BOAT_RACE_DB2
#【ファイル】delete.sh
#【機能仕様】HTMLダウンロードフォルダを削除して再作成する
#【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
#【来　　歴】2021.02.01 ver 1.00

BASE_DIR=/home/pi/BOAT_RACE_DB

#成績用
rm -fr $BASE_DIR/200_html/kiatu
rm -fr $BASE_DIR/200_html/last_info
rm -fr $BASE_DIR/200_html/odds_3t
rm -fr $BASE_DIR/200_html/race_table
rm -fr $BASE_DIR/200_html/result
rm -fr $BASE_DIR/200_html/tenken
rm -fr $BASE_DIR/200_html/yesterday
mkdir $BASE_DIR/200_html/kiatu
mkdir $BASE_DIR/200_html/last_info
mkdir $BASE_DIR/200_html/odds_3t
mkdir $BASE_DIR/200_html/race_table
mkdir $BASE_DIR/200_html/result
mkdir $BASE_DIR/200_html/tenken
mkdir $BASE_DIR/200_html/yesterday

#当日予想用
rm -fr $BASE_DIR/200_html/today
rm -fr $BASE_DIR/200_html/x_race_table
mkdir $BASE_DIR/200_html/today
mkdir $BASE_DIR/200_html/x_race_table