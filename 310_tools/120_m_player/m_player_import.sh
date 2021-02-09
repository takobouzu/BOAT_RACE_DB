echo 開始 m_player.csv `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import  /home/pi/BOAT_RACE_DB/310_tools/120_m_player/m_player.csv m_player"
echo 終了 `date`
