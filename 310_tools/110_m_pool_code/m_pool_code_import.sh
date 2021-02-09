echo 開始 m_pool_code.csv `date`
sqlite3 -separator , /home/pi/BOAT_RACE_DB/230_db/boatrace.db ".import  /home/pi/BOAT_RACE_DB/310_tools/110_m_pool_code/m_pool_code.csv m_pool_code"
echo 終了 `date`
