echo 開始 m_player.csv `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.dbboatrace.db ".import  /home/pi/BOAT_RACE_DB//110_m_pool_code/m_player_code.csv m_player"
echo 終了 `date`
