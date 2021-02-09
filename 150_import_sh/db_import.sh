echo 開始 t_info_d `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import /home/pi/BOAT_RACE_DB/210_csv/t_info_d.csv t_info_d"
echo 開始 t_info_h `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import /home/pi/BOAT_RACE_DB/210_csv/t_info_h.csv t_info_h"
echo 開始 t_info_p `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import /home/pi/BOAT_RACE_DB/210_csv/t_info_p.csv t_info_p"
echo 開始 t_odds `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import /home/pi/BOAT_RACE_DB/210_csv/t_odds.csv t_odds"
echo 開始 t_race_d `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import /home/pi/BOAT_RACE_DB/210_csv/t_race_d.csv t_race_d"
echo 開始 t_race_h `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import /home/pi/BOAT_RACE_DB/210_csv/t_race_h.csv t_race_h"
echo 開始 t_race_t `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import /home/pi/BOAT_RACE_DB/210_csv/t_race_t.csv t_race_t"
echo 開始 t_result_d `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import /home/pi/BOAT_RACE_DB/210_csv/t_result_d.csv t_result_d"
echo 開始 t_result_h `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import /home/pi/BOAT_RACE_DB/210_csv/t_result_h.csv t_result_h"
echo 開始 t_result_odds `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import /home/pi/BOAT_RACE_DB/210_csv/t_result_odds.csv t_result_oods"
echo 開始 t_tenken `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import /home/pi/BOAT_RACE_DB/210_csv/t_tenken.csv t_tenken"
echo 開始 x_race_d `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import /home/pi/BOAT_RACE_DB/210_csv/x_race_d.csv x_race_d"
echo 開始 x_race_h `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import /home/pi/BOAT_RACE_DB/210_csv/x_race_h.csv x_race_h"
echo 開始 x_race_t `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import /home/pi/BOAT_RACE_DB/210_csv/x_race_t.csv x_race_t"
echo 終了 `date`