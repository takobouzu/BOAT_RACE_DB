#【システム】BOAT_RACE_DB2
#【ファイル】000_get_dash.sh
#【機能仕様】ボートレースオフィシャルサイトから１日分のボートレース関連情報を取得してデータベースに格納する
#【引　　数】なし
#【戻 り 値】なし
#【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
#【来　　歴】2021.02.01 ver 1.00

#インストールディレクトリ
BASE_DIR=/home/pi/BOAT_RACE_DB

#過去にボートレースオフィシャルサイトからダウンロードした、HMTLファイルを削除する
sh $BASE_DIR/200_html/delete.sh

#ボートレースオフィシャルサイトからレース一覧をダウンロードする
sh $BASE_DIR/100_get_race_list/001_get_race_list.sh

#ボートレースオフィシャルサイトからボートレース関連情報が格納されたHTMLファイルをダウンロードするスクリプトを生成する
python3 $BASE_DIR/110_make_sh/001_mk_sh.py

#ボートレース関連情報が格納されたHTMLファイルをダウンロードする。
sh $BASE_DIR/120_get_html_sh/001_tenken.sh
sh $BASE_DIR/120_get_html_sh/002_race_table.sh
sh $BASE_DIR/120_get_html_sh/003_result.sh
sh $BASE_DIR/120_get_html_sh/004_last_info.sh
sh $BASE_DIR/120_get_html_sh/005_odds_3t.sh
sh $BASE_DIR/120_get_html_sh/006_kiatu.sh
sh $BASE_DIR/120_get_html_sh/x01_race_table.sh

#ボートレース関連情報が格納されたHTMLファイルからDBインポート用のCSVファイルを作成する

python3 $BASE_DIR/130_html_to_csv/000_mkcsv_t_tenken.py
python3 $BASE_DIR/130_html_to_csv/100_mkcsv_t_race_t.py
python3 $BASE_DIR/130_html_to_csv/110_mkcsv_t_race_h.py
python3 $BASE_DIR/130_html_to_csv/130_mkcsv_t_race_d.py
python3 $BASE_DIR/130_html_to_csv/140_mkcsv_t_info_h.py
python3 $BASE_DIR/130_html_to_csv/150_mkcsv_t_info_d.py
python3 $BASE_DIR/130_html_to_csv/160_mkcsv_t_info_p.py
python3 $BASE_DIR/130_html_to_csv/170_mkcsv_t_result_h.py
python3 $BASE_DIR/130_html_to_csv/180_mkcsv_t_result_d.py
python3 $BASE_DIR/130_html_to_csv/190_mkcsv_t_result_odds.py
python3 $BASE_DIR/130_html_to_csv/200_mkcsv_t_odds.py
python3 $BASE_DIR/130_html_to_csv/300_mkcsv_x_race_t.py
python3 $BASE_DIR/130_html_to_csv/310_mkcsv_x_race_h.py
python3 $BASE_DIR/130_html_to_csv/320_mkcsv_x_race_d.py

#DBインポート用のCSVファイルをSQLite3にインポートする
sh $BASE_DIR/150_import_sh/db_import.sh

#ボート関連指数算出
sh $BASE_DIR/140_index/110_mk_index.sh

#ボート関連指数算出CSV インポート
sh $BASE_DIR/150_import_sh/index_import.sh




