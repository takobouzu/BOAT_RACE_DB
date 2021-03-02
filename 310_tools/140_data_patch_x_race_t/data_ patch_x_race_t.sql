/*
【システム】BOAT_RACE_DB2
【ファイル】data_ patch_x_race_t.sql
【機能仕様】テーブル[x_race_t]の[event_date]に[初日]が設定されてない場合に、[初日]を設定する
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.03.02 ver 1.00
*/
UPDATE x_race_t
SET  event_date = '初日'
WHERE
event_date = '';