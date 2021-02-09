echo 開始 `date`
echo 開始 t_index `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import /home/pi/BOAT_RACE_DB/210_csv/t_index.csv t_index"
echo 終了 `date`
