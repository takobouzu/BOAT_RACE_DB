'''
【システム】BOAT_RACE_DB2
【ファイル】100_mk_index.py
【機能仕様】ボートレース関連指数を算出して、インポートファイル[t_index.csv]を作成する
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.02.01 ver 1.00
'''
import sys
import os
from dateutil import relativedelta
from datetime import datetime as dt
import sqlite3

#インストールディレクトの定義
BASE_DIR = '/home/pi/BOAT_RACE_DB'
#データベースファイルの定義
BASE_DB  = BASE_DIR + '/230_db/boatrace.db'
#出力ファイルの定義
CSV_FILE = BASE_DIR + '/210_csv/t_index.csv'

START_DATE = sys.argv[1] #算出開始年月日
END_DATE   = sys.argv[2] #算出終了年月日

'''
【関　数】mkcsv_t_index
【機　能】ボートレース関連指数テーブル「t_index」のインポートCSVファイルを作成
【引　数】なし
【戻り値】なし
'''
def mkcsv_t_index():
    print('ボートレース関連指数テーブル「t_index」のインポートCSVファイルを作成 開始')
    print('算出開始年月日 %s 算出終了年月日 %s' % (START_DATE, END_DATE))
    fw = open(CSV_FILE, 'w')
    conn = sqlite3.connect(BASE_DB)
    cur = conn.cursor()
   
    #算出開始年月日から算出終了年月日までの成績データの読み込み
    wk_sql1 = ""
    wk_sql1 = wk_sql1 + "SELECT "
    wk_sql1 = wk_sql1 + "t_result_d.yyyymmdd, "
    wk_sql1 = wk_sql1 + "t_result_d.pool_code, "
    wk_sql1 = wk_sql1 + "t_result_d.race_no, "
    wk_sql1 = wk_sql1 + "t_result_d.entry_no, "
    wk_sql1 = wk_sql1 + "t_race_d.player_no, "
    wk_sql1 = wk_sql1 + "t_race_d.motor_no, "
    wk_sql1 = wk_sql1 + "t_race_t.title "
    wk_sql1 = wk_sql1 + "FROM t_result_d,t_race_d,t_race_t "
    wk_sql1 = wk_sql1 + "WHERE "
    wk_sql1 = wk_sql1 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd "
    wk_sql1 = wk_sql1 + "AND t_race_d.pool_code = t_result_d.pool_code "
    wk_sql1 = wk_sql1 + "AND t_race_d.race_no = t_result_d.race_no "
    wk_sql1 = wk_sql1 + "AND t_race_d.entry_no = t_result_d.entry_no "
    wk_sql1 = wk_sql1 + "AND t_race_t.yyyymmdd = t_result_d.yyyymmdd "
    wk_sql1 = wk_sql1 + "AND t_race_t.pool_code = t_result_d.pool_code "
    wk_sql1 = wk_sql1 + "AND t_result_d.yyyymmdd BETWEEN '" + START_DATE + "' AND '" + END_DATE + "' "
    #指数算出対象件数算出
    zan_count = 0
    for row1 in cur.execute(wk_sql1):
        zan_count = zan_count + 1
    for row1 in cur.execute(wk_sql1):
        print("指数算出残数 %d" % (zan_count))
        #レコード項目初期化
        t_index_yyyymmdd = ''                           #開催日付
        t_index_pool_code = ''                          #場コード
        t_index_race_no = ''                            #レース番号
        t_index_entry_no = ''                           #枠番
        t_index_player_no = ''                          #選手登録番号
        t_index_motor_no = ''                           #モーター番号
        t_index_ability = ''                            #能力
        t_index_st = ''                                 #平均ST
        t_index_ability_count = ''                      #能力算出対象レース数
        t_index_ability2 = ''                           #直近能力
        t_index_st2 = ''                                #直近平均ST
        t_index_ability2_count = ''                     #直近能力算出対象
        t_index_rate_win_motor = ''                     #モーター能力
        t_index_motor_hensa = ''                        #モーター偏差  
        t_index_rate_win_count = ''                     #モーター能力算出対象レース数
        t_index_motor_count1 = ''                       #モーター能力算出対象レース数（１コース）
        t_index_motor_count2 = ''                       #モーター能力算出対象レース数（２コース）
        t_index_motor_count3 = ''                       #モーター能力算出対象レース数（３コース）
        t_index_motor_count4 = ''                       #モーター能力算出対象レース数（４コース）
        t_index_motor_count5 = ''                       #モーター能力算出対象レース数（５コース）
        t_index_motor_count6 = ''                       #モーター能力算出対象レース数（６コース）
        t_index_rate_win_motor_course1 = ''             #モーター能力（１コース）
        t_index_rate_win_motor_course2 = ''             #モーター能力（２コース）
        t_index_rate_win_motor_course3 = ''             #モーター能力（３コース）
        t_index_rate_win_motor_course4 = ''             #モーター能力（４コース）
        t_index_rate_win_motor_course5 = ''             #モーター能力（５コース）
        t_index_rate_win_motor_course6 = ''             #モーター能力（６コース）
        t_index_course_count_1 = ''                     #出走数（１コース）
        t_index_ability_course_1 = ''                   #能力値（１コース）
        t_index_sinnyu_course_1 = ''                    #進入偏差（１コース）
        t_index_nige_win_count_course_1 = ''            #逃げ切り勝ち数（１コース）
        t_index_nige_win_rate_course_1 = ''             #逃げ切り勝ち率（１コース）
        t_index_makuri_lost_count_course_1 = ''         #まくられ数（１コース）
        t_index_makuri_lost_rate_course_1 = ''          #まくられ率（１コース）
        t_index_sashi_lost_count_course_1 = ''          #差され数（１コース）
        t_index_sashi_lost_rate_course_1 = ''           #差され率（１コース）
        t_index_course_count_2 = ''                     #出走数（２コース）
        t_index_ability_course_2 = ''                   #能力値（２コース）
        t_index_sinnyu_course_2 = ''                    #進入偏差（２コース）
        t_index_nige_lost_count_course_2 = ''           #逃し数（２コース）
        t_index_nige_lost_rate_course_2 = ''            #逃し率（２コース）
        t_index_makuri_win_count_course_2 = ''          #まくり数（２コース）
        t_index_makuri_win_rate_course_2 = ''           #まくり率（２コース）
        t_index_sashi_win_count_course_2 = ''           #差し数（２コース）
        t_index_sashi_win_rate_course_2 = ''            #差し率（２コース）
        t_index_course_count_3 = ''                     #出走数（３コース）
        t_index_ability_course_3 = ''                   #能力値（３コース）
        t_index_sinnyu_course_3 = ''                    #進入偏差（３コース）
        t_index_makuri_win_count_course_3 = ''          #まくり数（３コース）
        t_index_makuri_win_rate_course_3 = ''           #まくり率（３コース）
        t_index_sashi_win_count_course_3 = ''           #差し数（３コース）
        t_index_sashi_win_rate_course_3 = ''            #差し率（３コース）
        t_index_course_count_4 = ''                     #出走数（４コース）
        t_index_ability_course_4 = ''                   #能力値（４コース）
        t_index_sinnyu_course_4 = ''                    #進入偏差（４コース）
        t_index_makuri_win_count_course_4 = ''          #まくり数（４コース）
        t_index_makuri_win_rate_course_4 = ''           #まくり率（４コース）
        t_index_sashi_win_count_course_4 = ''           #差し数（４コース）
        t_index_sashi_win_rate_course_4 = ''            #差し率（４コース）
        t_index_course_count_5 = ''                     #出走数（５コース）
        t_index_ability_course_5 = ''                   #能力値（５コース）
        t_index_sinnyu_course_5 = ''                    #進入偏差（５コース）
        t_index_makuri_win_count_course_5 = ''          #まくり数（５コース）
        t_index_makuri_win_rate_course_5 = ''           #まくり率（５コース）
        t_index_sashi_win_count_course_5 = ''           #差し数（５コース）
        t_index_sashi_win_rate_course_5 = ''            #差し率（５コース）
        t_index_course_count_6 = ''                     #出走数（６コース）
        t_index_ability_course_6 = ''                   #能力値（６コース）
        t_index_sinnyu_course_6 = ''                    #進入偏差（６コース）
        t_index_makuri_win_count_course_6 = ''          #まくり数（６コース）
        t_index_makuri_win_rate_course_6 = ''           #まくり率（６コース）
        t_index_sashi_win_count_course_6 = ''           #差し数（６コース）
        t_index_sashi_win_rate_course_6 = ''            #差し率（６コース）

        #出走データの転記
        t_index_yyyymmdd = str(row1[0])     #開催日付 t_index_yyyymmdd
        t_index_pool_code = str(row1[1])    #場コード t_index_pool_code
        t_index_race_no = str(row1[2])      #レース番号 t_index_race_no
        t_index_entry_no = str(row1[3])     #枠番 t_index_entry_no
        t_index_player_no = str(row1[4])    #選手登録番号 t_index_player_no
        t_index_motor_no = str(row1[5])     #モーター番号 t_index_motor_no


        #2年前の日付算出
        wk_day    = dt.strptime(t_index_yyyymmdd , '%Y%m%d')
        wk_day = wk_day - relativedelta.relativedelta(years=2)
        wk_day730 = wk_day.strftime('%Y%m%d') #2年前の日付


        #過去１２開催の競走成績から選手の能力値と平均STを算出する
        #能力 t_index_ability
        #平均ST t_index_st 
        #能力算出対象レース数 t_index_ability_count
        

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd, t_race_t.title,t_race_h.race_name,t_result_d.course,t_result_d.ranking "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_t,t_race_h,t_race_d,t_result_d "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_race_d.player_no = '" + t_index_player_no + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_day730 + "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "

        wk_title = str(row1[6])  #今節のタイトル
        wk_kaisai_max = 12       #過去に遡る節数の上限
        wk_date12 = ''           #１２節前の日付
        wk_kaisai_count = 0 

        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            if str(row2[1]) != wk_title:
                wk_title = str(row2[1])
                wk_kaisai_count = wk_kaisai_count + 1
                if wk_kaisai_count > wk_kaisai_max:
                    break
                wk_date12 = str(row2[0])
        
        wk_ability = 0.0    #能力値集計用
        scount = 0          #出走回数集計用
        wk_st = 0.0         #平均ST集計用
        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd, t_race_t.title, t_race_t.grade,t_race_h.race_name,t_result_d.course,t_result_d.ranking, t_result_d.flying ,t_result_d.start_time "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_t,t_race_h,t_race_d,t_result_d "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_race_d.player_no = '" + t_index_player_no + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_date12 + "' AND '" + t_index_yyyymmdd + "' "
        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            scount = scount + 1
            if (str(row2[2]) == '一般・若手') or (str(row2[2]) == '一般・女子') or (str(row2[2]) == '一般') or (str(row2[2]) == 'Ｇ３・女子') or (str(row2[2]) == 'Ｇ３'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) == '１':
                        wk_ability = wk_ability  + 65.0
                    if str(row2[5]) == '２':
                        wk_ability = wk_ability  + 63.0
                    if str(row2[5]) == '３':
                        wk_ability = wk_ability  + 59.0
                    if str(row2[5]) == '４':
                        wk_ability = wk_ability  + 56.0
                    if str(row2[5]) == '５':
                        wk_ability = wk_ability  + 53.0
                    if str(row2[5]) == '６':
                        wk_ability = wk_ability  + 50.0
                else:
                    if str(row2[5]) == '１':
                        wk_ability = wk_ability  + 60.0
                    if str(row2[5]) == '２':
                        wk_ability = wk_ability  + 58.0
                    if str(row2[5]) == '３':
                        wk_ability = wk_ability  + 55.0
                    if str(row2[5]) == '４':
                        wk_ability = wk_ability  + 50.0
                    if str(row2[5]) == '５':
                        wk_ability = wk_ability  + 40.0
                    if str(row2[5]) == '６':
                        wk_ability = wk_ability  + 30.0
            if (str(row2[2]) == 'Ｇ２・女子') or (str(row2[2]) == 'Ｇ２'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) ==  '１':
                        wk_ability = wk_ability  + 80.0
                    if str(row2[5]) ==  '２':
                        wk_ability = wk_ability  + 78.0
                    if str(row2[5]) ==  '３':
                        wk_ability = wk_ability  + 74.0
                    if str(row2[5]) ==  '４':
                        wk_ability = wk_ability  + 71.0
                    if str(row2[5]) ==  '５':
                        wk_ability = wk_ability  + 68.0
                    if str(row2[5]) ==  '６':
                        wk_ability = wk_ability  + 65.0
                else:
                    if str(row2[5]) ==  '１':
                        wk_ability = wk_ability  + 70.0
                    if str(row2[5]) ==  '２':
                        wk_ability = wk_ability  + 67.0
                    if str(row2[5]) ==  '３':
                        wk_ability = wk_ability  + 62.0
                    if str(row2[5]) ==  '４':
                        wk_ability = wk_ability  + 58.0
                    if str(row2[5]) ==  '５':
                        wk_ability = wk_ability  + 54.0
                    if str(row2[5]) ==  '６':
                        wk_ability = wk_ability  + 50.0
            if (str(row2[2]) == 'Ｇ１・女子') or (str(row2[2]) == 'Ｇ１')  or (str(row2[2]) == 'ＳＧ'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) ==  '１':
                        wk_ability = wk_ability  + 100.0
                    if str(row2[5]) ==  '２':
                        wk_ability = wk_ability  + 98.0
                    if str(row2[5]) ==  '３':
                        wk_ability = wk_ability  + 94.0
                    if str(row2[5]) ==  '４':
                        wk_ability = wk_ability  + 91.0
                    if str(row2[5]) ==  '５':
                        wk_ability = wk_ability  + 88.0
                    if str(row2[5]) ==  '６':
                        wk_ability = wk_ability  + 85.0
                else:
                    if str(row2[5]) ==  '１':
                        wk_ability = wk_ability  + 85.0
                    if str(row2[5]) ==  '２':
                        wk_ability = wk_ability  + 82.0
                    if str(row2[5]) ==  '３':
                        wk_ability = wk_ability  + 77.0
                    if str(row2[5]) ==  '４':
                        wk_ability = wk_ability  + 73.0
                    if str(row2[5]) ==  '５':
                        wk_ability = wk_ability  + 69.0
                    if str(row2[5]) ==  '６':
                        wk_ability = wk_ability  + 65.0
            #平均ST算出
            if (str(row2[5]) != 'Ｌ') and (str(row2[5]) != '欠') and (str(row2[6]) != 'L') and (str(row2[6]) != 'F'):
                wk_st = wk_st + float(row2[7])  
        if scount != 0:
            wk_ability = wk_ability / scount
            wk_st = wk_st / scount
        t_index_ability = '%5.2f' % (wk_ability)
        t_index_st = '%5.2f' % (wk_st)
        t_index_ability_count = '%d' % (scount)


        #直近６開催の選手能力と平均STを算出する。
        #直近能力 t_index_ability2
        #直近平均ST t_index_st2
        #直近能力算出対象 t_index_ability2_count

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd, t_race_t.title,t_race_h.race_name,t_result_d.course,t_result_d.ranking "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_t,t_race_h,t_race_d,t_result_d "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_race_d.player_no = '" + t_index_player_no + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_day730 + "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "

        wk_title = str(row1[6])  #今節のタイトル
        wk_kaisai_max = 6        #過去に遡る節数の上限
        wk_date06 = ''           #６節前の日付
        wk_kaisai_count = 0 

        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            if str(row2[1]) != wk_title:
                wk_title = str(row2[1])
                wk_kaisai_count = wk_kaisai_count + 1
                if wk_kaisai_count > wk_kaisai_max:
                    break
                wk_date06 = str(row2[0])
  
        wk_ability = 0.0    #能力値集計用
        scount = 0          #出走回数集計用
        wk_st = 0.0         #平均ST集計用
        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd, t_race_t.title, t_race_t.grade,t_race_h.race_name,t_result_d.course,t_result_d.ranking, t_result_d.flying ,t_result_d.start_time "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_t,t_race_h,t_race_d,t_result_d "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_race_d.player_no = '" + t_index_player_no + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_date06 + "' AND '" + t_index_yyyymmdd + "' "
        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            scount = scount + 1
            if (str(row2[2]) == '一般・若手') or (str(row2[2]) == '一般・女子') or (str(row2[2]) == '一般') or (str(row2[2]) == 'Ｇ３・女子') or (str(row2[2]) == 'Ｇ３'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) == '１':
                        wk_ability = wk_ability  + 65.0
                    if str(row2[5]) == '２':
                        wk_ability = wk_ability  + 63.0
                    if str(row2[5]) == '３':
                        wk_ability = wk_ability  + 59.0
                    if str(row2[5]) == '４':
                        wk_ability = wk_ability  + 56.0
                    if str(row2[5]) == '５':
                        wk_ability = wk_ability  + 53.0
                    if str(row2[5]) == '６':
                        wk_ability = wk_ability  + 50.0
                else:
                    if str(row2[5]) == '１':
                        wk_ability = wk_ability  + 60.0
                    if str(row2[5]) == '２':
                        wk_ability = wk_ability  + 58.0
                    if str(row2[5]) == '３':
                        wk_ability = wk_ability  + 55.0
                    if str(row2[5]) == '４':
                        wk_ability = wk_ability  + 50.0
                    if str(row2[5]) == '５':
                        wk_ability = wk_ability  + 40.0
                    if str(row2[5]) == '６':
                        wk_ability = wk_ability  + 30.0
            if (str(row2[2]) == 'Ｇ２・女子') or (str(row2[2]) == 'Ｇ２'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) ==  '１':
                        wk_ability = wk_ability  + 80.0
                    if str(row2[5]) ==  '２':
                        wk_ability = wk_ability  + 78.0
                    if str(row2[5]) ==  '３':
                        wk_ability = wk_ability  + 74.0
                    if str(row2[5]) ==  '４':
                        wk_ability = wk_ability  + 71.0
                    if str(row2[5]) ==  '５':
                        wk_ability = wk_ability  + 68.0
                    if str(row2[5]) ==  '６':
                        wk_ability = wk_ability  + 65.0
                else:
                    if str(row2[5]) ==  '１':
                        wk_ability = wk_ability  + 70.0
                    if str(row2[5]) ==  '２':
                        wk_ability = wk_ability  + 67.0
                    if str(row2[5]) ==  '３':
                        wk_ability = wk_ability  + 62.0
                    if str(row2[5]) ==  '４':
                        wk_ability = wk_ability  + 58.0
                    if str(row2[5]) ==  '５':
                        wk_ability = wk_ability  + 54.0
                    if str(row2[5]) ==  '６':
                        wk_ability = wk_ability  + 50.0
            if (str(row2[2]) == 'Ｇ１・女子') or (str(row2[2]) == 'Ｇ１')  or (str(row2[2]) == 'ＳＧ'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) ==  '１':
                        wk_ability = wk_ability  + 100.0
                    if str(row2[5]) ==  '２':
                        wk_ability = wk_ability  + 98.0
                    if str(row2[5]) ==  '３':
                        wk_ability = wk_ability  + 94.0
                    if str(row2[5]) ==  '４':
                        wk_ability = wk_ability  + 91.0
                    if str(row2[5]) ==  '５':
                        wk_ability = wk_ability  + 88.0
                    if str(row2[5]) ==  '６':
                        wk_ability = wk_ability  + 85.0
                else:
                    if str(row2[5]) ==  '１':
                        wk_ability = wk_ability  + 85.0
                    if str(row2[5]) ==  '２':
                        wk_ability = wk_ability  + 82.0
                    if str(row2[5]) ==  '３':
                        wk_ability = wk_ability  + 77.0
                    if str(row2[5]) ==  '４':
                        wk_ability = wk_ability  + 73.0
                    if str(row2[5]) ==  '５':
                        wk_ability = wk_ability  + 69.0
                    if str(row2[5]) ==  '６':
                        wk_ability = wk_ability  + 65.0
            #平均ST算出
            if (str(row2[5]) != 'Ｌ') and (str(row2[5]) != '欠') and (str(row2[6]) != 'L') and (str(row2[6]) != 'F'):
                wk_st = wk_st + float(row2[7])   
        if scount != 0:
            wk_ability = wk_ability / scount
            wk_st = wk_st / scount
        t_index_ability2 = '%5.2f' % (wk_ability)
        t_index_st2 = '%5.2f' % (wk_st)
        t_index_ability2_count = '%d' % (scount)



        #過去６開催の競走成績からモータ能力とモータ偏差を算出する
        #モーター能力 t_index_rate_win_motor
        #モーター偏差  t_index_motor_hensa
        #モーター能力算出対象レース数 t_index_rate_win_count
        #各コースのモータ能力を算出する

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd, t_race_t.title,t_race_h.race_name,t_result_d.course,t_result_d.ranking,t_race_d.motor_double_rate "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_t,t_race_h,t_race_d,t_result_d "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_race_d.pool_code = '" + t_index_pool_code + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.motor_no = '" + t_index_motor_no + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_day730+ "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "

        wk_title = str(row1[6])  #今節のタイトル
        wk_kaisai_max = 6        #過去に遡る節数の上限
        wk_motor_date06 = ''     #過去６節前の日付
        wk_kaisai_count = 0 
        motor_rate_flg = 0 
        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            if (motor_rate_flg == 1) and (float(row2[5]) > 0.0):
                break
            if float(row2[5]) == 0.0:
                motor_rate_flg = 1
            if str(row2[1]) != wk_title:
                wk_title = row2[1]
                wk_kaisai_count = wk_kaisai_count + 1
                if  wk_kaisai_count > wk_kaisai_max:
                    break
                wk_motor_date06 = str(row2[0])

        wk_rate_win_motor = 0.0
        scount = 0

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd, t_race_t.title, t_race_t.grade,t_race_h.race_name,t_result_d.course,t_result_d.ranking,t_race_d.motor_double_rate "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_t,t_race_h,t_race_d,t_result_d "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_race_d.pool_code = '" + t_index_pool_code + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.motor_no = '" + t_index_motor_no + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_motor_date06 + "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "

        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            scount = scount + 1
            if (str(row2[2]) == '一般・若手') or (str(row2[2]) == '一般・女子') or (str(row2[2]) == '一般') or (str(row2[2]) == 'Ｇ３・女子') or (str(row2[2]) == 'Ｇ３'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) == '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 65.0
                    if str(row2[5]) == '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 63.0
                    if str(row2[5]) == '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 59.0
                    if str(row2[5]) == '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 56.0
                    if str(row2[5]) == '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 53.0
                    if str(row2[5]) == '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
                else:
                    if str(row2[5]) == '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 60.0
                    if str(row2[5]) == '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 58.0
                    if str(row2[5]) == '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 55.0
                    if str(row2[5]) == '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
                    if str(row2[5]) == '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 40.0
                    if str(row2[5]) == '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 30.0
            if (str(row2[2]) == 'Ｇ２・女子') or (str(row2[2]) == 'Ｇ２'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) ==  '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 80.0
                    if str(row2[5]) ==  '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 78.0
                    if str(row2[5]) ==  '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 74.0
                    if str(row2[5]) ==  '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 71.0
                    if str(row2[5]) ==  '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 68.0
                    if str(row2[5]) ==  '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 65.0
                else:
                    if str(row2[5]) ==  '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 70.0
                    if str(row2[5]) ==  '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 67.0
                    if str(row2[5]) ==  '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 62.0
                    if str(row2[5]) ==  '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 58.0
                    if str(row2[5]) ==  '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 54.0
                    if str(row2[5]) ==  '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
            if (str(row2[2]) == 'Ｇ１・女子') or (str(row2[2]) == 'Ｇ１')  or (str(row2[2]) == 'ＳＧ'):
                    if '優勝戦' in str(row2[3]):
                        if str(row2[5]) ==  '１':
                            wk_rate_win_motor = wk_rate_win_motor  + 100.0
                        if str(row2[5]) ==  '２':
                            wk_rate_win_motor = wk_rate_win_motor  + 98.0
                        if str(row2[5]) ==  '３':
                            wk_rate_win_motor = wk_rate_win_motor  + 94.0
                        if str(row2[5]) ==  '４':
                            wk_rate_win_motor = wk_rate_win_motor  + 91.0
                        if str(row2[5]) ==  '５':
                            wk_rate_win_motor = wk_rate_win_motor  + 88.0
                        if str(row2[5]) ==  '６':
                            wk_rate_win_motor = wk_rate_win_motor  + 85.0
                    else:
                        if str(row2[5]) ==  '１':
                            wk_rate_win_motor = wk_rate_win_motor  + 85.0
                        if str(row2[5]) ==  '２':
                            wk_rate_win_motor = wk_rate_win_motor  + 82.0
                        if str(row2[5]) ==  '３':
                            wk_rate_win_motor = wk_rate_win_motor  + 77.0
                        if str(row2[5]) ==  '４':
                            wk_rate_win_motor = wk_rate_win_motor  + 73.0
                        if str(row2[5]) ==  '５':
                            wk_rate_win_motor = wk_rate_win_motor  + 69.0
                        if str(row2[5]) ==  '６':
                            wk_rate_win_motor = wk_rate_win_motor  + 65.0
        if scount != 0:
            wk_rate_win_motor = wk_rate_win_motor/ scount
        t_index_rate_win_motor = '%5.2f' % (wk_rate_win_motor)
        t_index_rate_win_count = '%d' % (scount)
        wk = 0.0
        wk = float(t_index_rate_win_motor) - float(t_index_ability2)
        t_index_motor_hensa = '%5.2f' % (wk)


        #過去６開催の競走成績から１コースのモータ能力を算出する
        #モーター能力算出対象レース数（１コース） t_index_motor_count1
        #モーター能力（１コース） t_index_rate_win_motor_course1

        wk_rate_win_motor = 0.0
        scount = 0

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd, t_race_t.title, t_race_t.grade,t_race_h.race_name,t_result_d.course,t_result_d.ranking,t_race_d.motor_double_rate "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_t,t_race_h,t_race_d,t_result_d "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_result_d.course = '1' "
        wk_sql2 = wk_sql2 + "AND t_race_d.pool_code = '" + t_index_pool_code + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.motor_no = '" + t_index_motor_no + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_motor_date06 + "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "

        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            scount = scount + 1
            if (str(row2[2]) == '一般・若手') or (str(row2[2]) == '一般・女子') or (str(row2[2]) == '一般') or (str(row2[2]) == 'Ｇ３・女子') or (str(row2[2]) == 'Ｇ３'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) == '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 65.0
                    if str(row2[5]) == '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 63.0
                    if str(row2[5]) == '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 59.0
                    if str(row2[5]) == '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 56.0
                    if str(row2[5]) == '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 53.0
                    if str(row2[5]) == '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
                else:
                    if str(row2[5]) == '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 60.0
                    if str(row2[5]) == '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 58.0
                    if str(row2[5]) == '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 55.0
                    if str(row2[5]) == '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
                    if str(row2[5]) == '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 40.0
                    if str(row2[5]) == '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 30.0
            if (str(row2[2]) == 'Ｇ２・女子') or (str(row2[2]) == 'Ｇ２'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) ==  '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 80.0
                    if str(row2[5]) ==  '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 78.0
                    if str(row2[5]) ==  '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 74.0
                    if str(row2[5]) ==  '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 71.0
                    if str(row2[5]) ==  '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 68.0
                    if str(row2[5]) ==  '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 65.0
                else:
                    if str(row2[5]) ==  '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 70.0
                    if str(row2[5]) ==  '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 67.0
                    if str(row2[5]) ==  '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 62.0
                    if str(row2[5]) ==  '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 58.0
                    if str(row2[5]) ==  '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 54.0
                    if str(row2[5]) ==  '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
            if (str(row2[2]) == 'Ｇ１・女子') or (str(row2[2]) == 'Ｇ１')  or (str(row2[2]) == 'ＳＧ'):
                    if '優勝戦' in str(row2[3]):
                        if str(row2[5]) ==  '１':
                            wk_rate_win_motor = wk_rate_win_motor  + 100.0
                        if str(row2[5]) ==  '２':
                            wk_rate_win_motor = wk_rate_win_motor  + 98.0
                        if str(row2[5]) ==  '３':
                            wk_rate_win_motor = wk_rate_win_motor  + 94.0
                        if str(row2[5]) ==  '４':
                            wk_rate_win_motor = wk_rate_win_motor  + 91.0
                        if str(row2[5]) ==  '５':
                            wk_rate_win_motor = wk_rate_win_motor  + 88.0
                        if str(row2[5]) ==  '６':
                            wk_rate_win_motor = wk_rate_win_motor  + 85.0
                    else:
                        if str(row2[5]) ==  '１':
                            wk_rate_win_motor = wk_rate_win_motor  + 85.0
                        if str(row2[5]) ==  '２':
                            wk_rate_win_motor = wk_rate_win_motor  + 82.0
                        if str(row2[5]) ==  '３':
                            wk_rate_win_motor = wk_rate_win_motor  + 77.0
                        if str(row2[5]) ==  '４':
                            wk_rate_win_motor = wk_rate_win_motor  + 73.0
                        if str(row2[5]) ==  '５':
                            wk_rate_win_motor = wk_rate_win_motor  + 69.0
                        if str(row2[5]) ==  '６':
                            wk_rate_win_motor = wk_rate_win_motor  + 65.0
        if scount != 0:
            wk_rate_win_motor = wk_rate_win_motor/ scount
        t_index_rate_win_motor_course1 = '%5.2f' % (wk_rate_win_motor)
        t_index_motor_count1 = '%d' % (scount)

        #過去６開催の競走成績から２コースのモータ能力を算出する
        #モーター能力算出対象レース数（２コース） t_index_motor_count2
        #モーター能力（２コース） t_index_rate_win_motor_course2
        wk_rate_win_motor = 0.0
        scount = 0

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd, t_race_t.title, t_race_t.grade,t_race_h.race_name,t_result_d.course,t_result_d.ranking,t_race_d.motor_double_rate "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_t,t_race_h,t_race_d,t_result_d "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_result_d.course = '2' "
        wk_sql2 = wk_sql2 + "AND t_race_d.pool_code = '" + t_index_pool_code + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.motor_no = '" + t_index_motor_no + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_motor_date06 + "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "

        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            scount = scount + 1
            if (str(row2[2]) == '一般・若手') or (str(row2[2]) == '一般・女子') or (str(row2[2]) == '一般') or (str(row2[2]) == 'Ｇ３・女子') or (str(row2[2]) == 'Ｇ３'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) == '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 65.0
                    if str(row2[5]) == '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 63.0
                    if str(row2[5]) == '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 59.0
                    if str(row2[5]) == '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 56.0
                    if str(row2[5]) == '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 53.0
                    if str(row2[5]) == '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
                else:
                    if str(row2[5]) == '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 60.0
                    if str(row2[5]) == '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 58.0
                    if str(row2[5]) == '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 55.0
                    if str(row2[5]) == '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
                    if str(row2[5]) == '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 40.0
                    if str(row2[5]) == '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 30.0
            if (str(row2[2]) == 'Ｇ２・女子') or (str(row2[2]) == 'Ｇ２'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) ==  '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 80.0
                    if str(row2[5]) ==  '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 78.0
                    if str(row2[5]) ==  '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 74.0
                    if str(row2[5]) ==  '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 71.0
                    if str(row2[5]) ==  '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 68.0
                    if str(row2[5]) ==  '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 65.0
                else:
                    if str(row2[5]) ==  '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 70.0
                    if str(row2[5]) ==  '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 67.0
                    if str(row2[5]) ==  '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 62.0
                    if str(row2[5]) ==  '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 58.0
                    if str(row2[5]) ==  '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 54.0
                    if str(row2[5]) ==  '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
            if (str(row2[2]) == 'Ｇ１・女子') or (str(row2[2]) == 'Ｇ１')  or (str(row2[2]) == 'ＳＧ'):
                    if '優勝戦' in str(row2[3]):
                        if str(row2[5]) ==  '１':
                            wk_rate_win_motor = wk_rate_win_motor  + 100.0
                        if str(row2[5]) ==  '２':
                            wk_rate_win_motor = wk_rate_win_motor  + 98.0
                        if str(row2[5]) ==  '３':
                            wk_rate_win_motor = wk_rate_win_motor  + 94.0
                        if str(row2[5]) ==  '４':
                            wk_rate_win_motor = wk_rate_win_motor  + 91.0
                        if str(row2[5]) ==  '５':
                            wk_rate_win_motor = wk_rate_win_motor  + 88.0
                        if str(row2[5]) ==  '６':
                            wk_rate_win_motor = wk_rate_win_motor  + 85.0
                    else:
                        if str(row2[5]) ==  '１':
                            wk_rate_win_motor = wk_rate_win_motor  + 85.0
                        if str(row2[5]) ==  '２':
                            wk_rate_win_motor = wk_rate_win_motor  + 82.0
                        if str(row2[5]) ==  '３':
                            wk_rate_win_motor = wk_rate_win_motor  + 77.0
                        if str(row2[5]) ==  '４':
                            wk_rate_win_motor = wk_rate_win_motor  + 73.0
                        if str(row2[5]) ==  '５':
                            wk_rate_win_motor = wk_rate_win_motor  + 69.0
                        if str(row2[5]) ==  '６':
                            wk_rate_win_motor = wk_rate_win_motor  + 65.0
        if scount != 0:
            wk_rate_win_motor = wk_rate_win_motor/ scount
        t_index_rate_win_motor_course2 = '%5.2f' % (wk_rate_win_motor)
        t_index_motor_count2 = '%d' % (scount)
        
        #過去６開催の競走成績から３コースのモータ能力を算出する
        #モーター能力算出対象レース数（３コース） t_index_motor_count3
        #モーター能力（３コース） t_index_rate_win_motor_course3

        wk_rate_win_motor = 0.0
        scount = 0

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd, t_race_t.title, t_race_t.grade,t_race_h.race_name,t_result_d.course,t_result_d.ranking,t_race_d.motor_double_rate "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_t,t_race_h,t_race_d,t_result_d "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_result_d.course = '3' "
        wk_sql2 = wk_sql2 + "AND t_race_d.pool_code = '" + t_index_pool_code + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.motor_no = '" + t_index_motor_no + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_motor_date06 + "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "

        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            scount = scount + 1
            if (str(row2[2]) == '一般・若手') or (str(row2[2]) == '一般・女子') or (str(row2[2]) == '一般') or (str(row2[2]) == 'Ｇ３・女子') or (str(row2[2]) == 'Ｇ３'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) == '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 65.0
                    if str(row2[5]) == '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 63.0
                    if str(row2[5]) == '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 59.0
                    if str(row2[5]) == '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 56.0
                    if str(row2[5]) == '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 53.0
                    if str(row2[5]) == '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
                else:
                    if str(row2[5]) == '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 60.0
                    if str(row2[5]) == '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 58.0
                    if str(row2[5]) == '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 55.0
                    if str(row2[5]) == '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
                    if str(row2[5]) == '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 40.0
                    if str(row2[5]) == '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 30.0
            if (str(row2[2]) == 'Ｇ２・女子') or (str(row2[2]) == 'Ｇ２'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) ==  '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 80.0
                    if str(row2[5]) ==  '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 78.0
                    if str(row2[5]) ==  '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 74.0
                    if str(row2[5]) ==  '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 71.0
                    if str(row2[5]) ==  '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 68.0
                    if str(row2[5]) ==  '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 65.0
                else:
                    if str(row2[5]) ==  '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 70.0
                    if str(row2[5]) ==  '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 67.0
                    if str(row2[5]) ==  '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 62.0
                    if str(row2[5]) ==  '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 58.0
                    if str(row2[5]) ==  '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 54.0
                    if str(row2[5]) ==  '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
            if (str(row2[2]) == 'Ｇ１・女子') or (str(row2[2]) == 'Ｇ１')  or (str(row2[2]) == 'ＳＧ'):
                    if '優勝戦' in str(row2[3]):
                        if str(row2[5]) ==  '１':
                            wk_rate_win_motor = wk_rate_win_motor  + 100.0
                        if str(row2[5]) ==  '２':
                            wk_rate_win_motor = wk_rate_win_motor  + 98.0
                        if str(row2[5]) ==  '３':
                            wk_rate_win_motor = wk_rate_win_motor  + 94.0
                        if str(row2[5]) ==  '４':
                            wk_rate_win_motor = wk_rate_win_motor  + 91.0
                        if str(row2[5]) ==  '５':
                            wk_rate_win_motor = wk_rate_win_motor  + 88.0
                        if str(row2[5]) ==  '６':
                            wk_rate_win_motor = wk_rate_win_motor  + 85.0
                    else:
                        if str(row2[5]) ==  '１':
                            wk_rate_win_motor = wk_rate_win_motor  + 85.0
                        if str(row2[5]) ==  '２':
                            wk_rate_win_motor = wk_rate_win_motor  + 82.0
                        if str(row2[5]) ==  '３':
                            wk_rate_win_motor = wk_rate_win_motor  + 77.0
                        if str(row2[5]) ==  '４':
                            wk_rate_win_motor = wk_rate_win_motor  + 73.0
                        if str(row2[5]) ==  '５':
                            wk_rate_win_motor = wk_rate_win_motor  + 69.0
                        if str(row2[5]) ==  '６':
                            wk_rate_win_motor = wk_rate_win_motor  + 65.0
        if scount != 0:
            wk_rate_win_motor = wk_rate_win_motor/ scount
        t_index_rate_win_motor_course3 = '%5.2f' % (wk_rate_win_motor)
        t_index_motor_count3 = '%d' % (scount)
        
        #過去６開催の競走成績から４コースのモータ能力を算出する
        #モーター能力算出対象レース数（４コース）t_index_motor_count4
        #モーター能力（４コース）t_index_rate_win_motor_course4
        wk_rate_win_motor = 0.0
        scount = 0

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd, t_race_t.title, t_race_t.grade,t_race_h.race_name,t_result_d.course,t_result_d.ranking,t_race_d.motor_double_rate "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_t,t_race_h,t_race_d,t_result_d "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_result_d.course = '4' "
        wk_sql2 = wk_sql2 + "AND t_race_d.pool_code = '" + t_index_pool_code + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.motor_no = '" + t_index_motor_no + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_motor_date06 + "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "

        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            scount = scount + 1
            if (str(row2[2]) == '一般・若手') or (str(row2[2]) == '一般・女子') or (str(row2[2]) == '一般') or (str(row2[2]) == 'Ｇ３・女子') or (str(row2[2]) == 'Ｇ３'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) == '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 65.0
                    if str(row2[5]) == '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 63.0
                    if str(row2[5]) == '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 59.0
                    if str(row2[5]) == '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 56.0
                    if str(row2[5]) == '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 53.0
                    if str(row2[5]) == '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
                else:
                    if str(row2[5]) == '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 60.0
                    if str(row2[5]) == '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 58.0
                    if str(row2[5]) == '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 55.0
                    if str(row2[5]) == '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
                    if str(row2[5]) == '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 40.0
                    if str(row2[5]) == '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 30.0
            if (str(row2[2]) == 'Ｇ２・女子') or (str(row2[2]) == 'Ｇ２'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) ==  '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 80.0
                    if str(row2[5]) ==  '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 78.0
                    if str(row2[5]) ==  '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 74.0
                    if str(row2[5]) ==  '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 71.0
                    if str(row2[5]) ==  '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 68.0
                    if str(row2[5]) ==  '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 65.0
                else:
                    if str(row2[5]) ==  '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 70.0
                    if str(row2[5]) ==  '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 67.0
                    if str(row2[5]) ==  '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 62.0
                    if str(row2[5]) ==  '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 58.0
                    if str(row2[5]) ==  '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 54.0
                    if str(row2[5]) ==  '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
            if (str(row2[2]) == 'Ｇ１・女子') or (str(row2[2]) == 'Ｇ１')  or (str(row2[2]) == 'ＳＧ'):
                    if '優勝戦' in str(row2[3]):
                        if str(row2[5]) ==  '１':
                            wk_rate_win_motor = wk_rate_win_motor  + 100.0
                        if str(row2[5]) ==  '２':
                            wk_rate_win_motor = wk_rate_win_motor  + 98.0
                        if str(row2[5]) ==  '３':
                            wk_rate_win_motor = wk_rate_win_motor  + 94.0
                        if str(row2[5]) ==  '４':
                            wk_rate_win_motor = wk_rate_win_motor  + 91.0
                        if str(row2[5]) ==  '５':
                            wk_rate_win_motor = wk_rate_win_motor  + 88.0
                        if str(row2[5]) ==  '６':
                            wk_rate_win_motor = wk_rate_win_motor  + 85.0
                    else:
                        if str(row2[5]) ==  '１':
                            wk_rate_win_motor = wk_rate_win_motor  + 85.0
                        if str(row2[5]) ==  '２':
                            wk_rate_win_motor = wk_rate_win_motor  + 82.0
                        if str(row2[5]) ==  '３':
                            wk_rate_win_motor = wk_rate_win_motor  + 77.0
                        if str(row2[5]) ==  '４':
                            wk_rate_win_motor = wk_rate_win_motor  + 73.0
                        if str(row2[5]) ==  '５':
                            wk_rate_win_motor = wk_rate_win_motor  + 69.0
                        if str(row2[5]) ==  '６':
                            wk_rate_win_motor = wk_rate_win_motor  + 65.0
        if scount != 0:
            wk_rate_win_motor = wk_rate_win_motor/ scount
        t_index_rate_win_motor_course4 = '%5.2f' % (wk_rate_win_motor)
        t_index_motor_count4 = '%d' % (scount)
        
        #過去６開催の競走成績から５コースのモータ能力を算出する
        #モーター能力算出対象レース数（５コース） t_index_motor_count5
        #モーター能力（５コース）t_index_rate_win_motor_course5 
        wk_rate_win_motor = 0.0
        scount = 0

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd, t_race_t.title, t_race_t.grade,t_race_h.race_name,t_result_d.course,t_result_d.ranking,t_race_d.motor_double_rate "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_t,t_race_h,t_race_d,t_result_d "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_result_d.course = '5' "
        wk_sql2 = wk_sql2 + "AND t_race_d.pool_code = '" + t_index_pool_code + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.motor_no = '" + t_index_motor_no + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_motor_date06 + "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "

        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            scount = scount + 1
            if (str(row2[2]) == '一般・若手') or (str(row2[2]) == '一般・女子') or (str(row2[2]) == '一般') or (str(row2[2]) == 'Ｇ３・女子') or (str(row2[2]) == 'Ｇ３'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) == '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 65.0
                    if str(row2[5]) == '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 63.0
                    if str(row2[5]) == '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 59.0
                    if str(row2[5]) == '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 56.0
                    if str(row2[5]) == '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 53.0
                    if str(row2[5]) == '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
                else:
                    if str(row2[5]) == '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 60.0
                    if str(row2[5]) == '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 58.0
                    if str(row2[5]) == '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 55.0
                    if str(row2[5]) == '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
                    if str(row2[5]) == '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 40.0
                    if str(row2[5]) == '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 30.0
            if (str(row2[2]) == 'Ｇ２・女子') or (str(row2[2]) == 'Ｇ２'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) ==  '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 80.0
                    if str(row2[5]) ==  '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 78.0
                    if str(row2[5]) ==  '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 74.0
                    if str(row2[5]) ==  '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 71.0
                    if str(row2[5]) ==  '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 68.0
                    if str(row2[5]) ==  '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 65.0
                else:
                    if str(row2[5]) ==  '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 70.0
                    if str(row2[5]) ==  '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 67.0
                    if str(row2[5]) ==  '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 62.0
                    if str(row2[5]) ==  '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 58.0
                    if str(row2[5]) ==  '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 54.0
                    if str(row2[5]) ==  '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
            if (str(row2[2]) == 'Ｇ１・女子') or (str(row2[2]) == 'Ｇ１')  or (str(row2[2]) == 'ＳＧ'):
                    if '優勝戦' in str(row2[3]):
                        if str(row2[5]) ==  '１':
                            wk_rate_win_motor = wk_rate_win_motor  + 100.0
                        if str(row2[5]) ==  '２':
                            wk_rate_win_motor = wk_rate_win_motor  + 98.0
                        if str(row2[5]) ==  '３':
                            wk_rate_win_motor = wk_rate_win_motor  + 94.0
                        if str(row2[5]) ==  '４':
                            wk_rate_win_motor = wk_rate_win_motor  + 91.0
                        if str(row2[5]) ==  '５':
                            wk_rate_win_motor = wk_rate_win_motor  + 88.0
                        if str(row2[5]) ==  '６':
                            wk_rate_win_motor = wk_rate_win_motor  + 85.0
                    else:
                        if str(row2[5]) ==  '１':
                            wk_rate_win_motor = wk_rate_win_motor  + 85.0
                        if str(row2[5]) ==  '２':
                            wk_rate_win_motor = wk_rate_win_motor  + 82.0
                        if str(row2[5]) ==  '３':
                            wk_rate_win_motor = wk_rate_win_motor  + 77.0
                        if str(row2[5]) ==  '４':
                            wk_rate_win_motor = wk_rate_win_motor  + 73.0
                        if str(row2[5]) ==  '５':
                            wk_rate_win_motor = wk_rate_win_motor  + 69.0
                        if str(row2[5]) ==  '６':
                            wk_rate_win_motor = wk_rate_win_motor  + 65.0
        if scount != 0:
            wk_rate_win_motor = wk_rate_win_motor/ scount
        t_index_rate_win_motor_course5 = '%5.2f' % (wk_rate_win_motor)
        t_index_motor_count5 = '%d' % (scount)

        #過去６開催の競走成績から６コースのモータ能力を算出する
        #モーター能力算出対象レース数（６コース） t_index_motor_count6
        #モーター能力（６コース）t_index_rate_win_motor_course6
        wk_rate_win_motor = 0.0
        scount = 0

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd, t_race_t.title, t_race_t.grade,t_race_h.race_name,t_result_d.course,t_result_d.ranking,t_race_d.motor_double_rate "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_t,t_race_h,t_race_d,t_result_d "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_result_d.course = '6' "
        wk_sql2 = wk_sql2 + "AND t_race_d.pool_code = '" + t_index_pool_code + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.motor_no = '" + t_index_motor_no + "' "
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_motor_date06 + "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "

        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            scount = scount + 1
            if (str(row2[2]) == '一般・若手') or (str(row2[2]) == '一般・女子') or (str(row2[2]) == '一般') or (str(row2[2]) == 'Ｇ３・女子') or (str(row2[2]) == 'Ｇ３'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) == '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 65.0
                    if str(row2[5]) == '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 63.0
                    if str(row2[5]) == '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 59.0
                    if str(row2[5]) == '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 56.0
                    if str(row2[5]) == '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 53.0
                    if str(row2[5]) == '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
                else:
                    if str(row2[5]) == '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 60.0
                    if str(row2[5]) == '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 58.0
                    if str(row2[5]) == '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 55.0
                    if str(row2[5]) == '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
                    if str(row2[5]) == '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 40.0
                    if str(row2[5]) == '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 30.0
            if (str(row2[2]) == 'Ｇ２・女子') or (str(row2[2]) == 'Ｇ２'):
                if '優勝戦' in str(row2[3]):
                    if str(row2[5]) ==  '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 80.0
                    if str(row2[5]) ==  '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 78.0
                    if str(row2[5]) ==  '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 74.0
                    if str(row2[5]) ==  '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 71.0
                    if str(row2[5]) ==  '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 68.0
                    if str(row2[5]) ==  '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 65.0
                else:
                    if str(row2[5]) ==  '１':
                        wk_rate_win_motor = wk_rate_win_motor  + 70.0
                    if str(row2[5]) ==  '２':
                        wk_rate_win_motor = wk_rate_win_motor  + 67.0
                    if str(row2[5]) ==  '３':
                        wk_rate_win_motor = wk_rate_win_motor  + 62.0
                    if str(row2[5]) ==  '４':
                        wk_rate_win_motor = wk_rate_win_motor  + 58.0
                    if str(row2[5]) ==  '５':
                        wk_rate_win_motor = wk_rate_win_motor  + 54.0
                    if str(row2[5]) ==  '６':
                        wk_rate_win_motor = wk_rate_win_motor  + 50.0
            if (str(row2[2]) == 'Ｇ１・女子') or (str(row2[2]) == 'Ｇ１')  or (str(row2[2]) == 'ＳＧ'):
                    if '優勝戦' in str(row2[3]):
                        if str(row2[5]) ==  '１':
                            wk_rate_win_motor = wk_rate_win_motor  + 100.0
                        if str(row2[5]) ==  '２':
                            wk_rate_win_motor = wk_rate_win_motor  + 98.0
                        if str(row2[5]) ==  '３':
                            wk_rate_win_motor = wk_rate_win_motor  + 94.0
                        if str(row2[5]) ==  '４':
                            wk_rate_win_motor = wk_rate_win_motor  + 91.0
                        if str(row2[5]) ==  '５':
                            wk_rate_win_motor = wk_rate_win_motor  + 88.0
                        if str(row2[5]) ==  '６':
                            wk_rate_win_motor = wk_rate_win_motor  + 85.0
                    else:
                        if str(row2[5]) ==  '１':
                            wk_rate_win_motor = wk_rate_win_motor  + 85.0
                        if str(row2[5]) ==  '２':
                            wk_rate_win_motor = wk_rate_win_motor  + 82.0
                        if str(row2[5]) ==  '３':
                            wk_rate_win_motor = wk_rate_win_motor  + 77.0
                        if str(row2[5]) ==  '４':
                            wk_rate_win_motor = wk_rate_win_motor  + 73.0
                        if str(row2[5]) ==  '５':
                            wk_rate_win_motor = wk_rate_win_motor  + 69.0
                        if str(row2[5]) ==  '６':
                            wk_rate_win_motor = wk_rate_win_motor  + 65.0
        if scount != 0:
            wk_rate_win_motor = wk_rate_win_motor/ scount
        t_index_rate_win_motor_course6 = '%5.2f' % (wk_rate_win_motor)
        t_index_motor_count6 = '%d' % (scount)

        #コース別能力算出　１コース
        #出走数（１コース）t_index_course_count_1
        #能力値（１コース）t_index_ability_course_1
        #進入偏差（１コース）t_index_sinnyu_course_1
        #逃げ切り勝ち数（１コース）t_index_nige_win_count_course_1
        #逃げ切り勝ち率（１コース）t_index_nige_win_rate_course_1
        #まくられ数（１コース）t_index_makuri_lost_count_course_1
        #まくられ率（１コース）t_index_makuri_lost_rate_course_1
        #差され数（１コース）t_index_sashi_lost_count_course_1
        #差され率（１コース）t_index_sashi_lost_rate_course_1

        wk_course_count_1 = 0.0                 #出走数
        wk_nige_win_count_course_1 = 0          #逃げ勝ち数
        wk_nige_win_rate_course_1 = 0.0         #逃げ勝ち率
        wk_makuri_lost_count_course_1 = 0       #まくられ数
        wk_makuri_lost_rate_course_1 = 0.0      #まくられ率
        wk_sashi_lost_count_course_1 = 0        #差され数
        wk_sashi_lost_rate_course_1 = 0.0       #差され率
        wk_sinnyu_course_1 = 0                  #進入偏差
        wk_ability_course_1 = 0.0               #能力値

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_result_d.course,t_result_d.ranking,t_result_h.decisive_factor, t_result_d.entry_no, t_race_t.grade, t_race_h.race_name "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_d, t_result_d, t_result_h, t_race_t, t_race_h "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_result_h.yyyymmdd = t_race_d.yyyymmdd AND t_result_h.pool_code = t_race_d.pool_code AND t_result_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_result_d.course = '1' "
        wk_sql2 = wk_sql2 + "AND t_race_d.player_no = '" + t_index_player_no + "' "  
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_date12 + "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "
        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            wk_course_count_1 = wk_course_count_1 + 1 #出走数
            wk_sinnyu_course_1 = wk_sinnyu_course_1 + (1 - int(row2[3])) #進入偏差
            if (str(row2[4]) == '一般・若手') or (str(row2[4]) == '一般・女子') or (str(row2[4]) == '一般') or (str(row2[4]) == 'Ｇ３・女子') or (str(row2[4]) == 'Ｇ３'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１':
                            wk_ability_course_1 = wk_ability_course_1  + 65.0
                        if str(row2[1]) == '２':
                            wk_ability_course_1 = wk_ability_course_1  + 63.0
                        if str(row2[1]) == '３':
                            wk_ability_course_1 = wk_ability_course_1  + 59.0
                        if str(row2[1]) == '４':
                            wk_ability_course_1 = wk_ability_course_1  + 56.0
                        if str(row2[1]) == '５':
                            wk_ability_course_1 = wk_ability_course_1  + 53.0
                        if str(row2[1]) == '６':
                            wk_ability_course_1 = wk_ability_course_1  + 50.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_1 =  wk_ability_course_1  + 60.0
                        if str(row2[1]) == '２':
                            wk_ability_course_1 =  wk_ability_course_1  + 58.0
                        if str(row2[1]) == '３':
                            wk_ability_course_1 =  wk_ability_course_1  + 55.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_1 =  wk_ability_course_1  + 50.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_1 =  wk_ability_course_1  + 40.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_1 =  wk_ability_course_1  + 30.0
            if (str(row2[4]) == 'Ｇ２・女子') or (str(row2[4]) == 'Ｇ２'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１': 
                            wk_ability_course_1 =  wk_ability_course_1  + 80.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_1 =  wk_ability_course_1  + 78.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_1 =  wk_ability_course_1  + 74.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_1 =  wk_ability_course_1  + 71.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_1 =  wk_ability_course_1  + 68.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_1 =  wk_ability_course_1  + 65.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_1 =  wk_ability_course_1  + 70.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_1 =  wk_ability_course_1  + 67.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_1 =  wk_ability_course_1  + 62.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_1 =  wk_ability_course_1  + 58.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_1 =  wk_ability_course_1  + 54.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_1 =  wk_ability_course_1  + 50.0
            if (str(row2[4]) == 'Ｇ１・女子') or (str(row2[4]) == 'Ｇ１')  or (str(row2[4]) == 'ＳＧ'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１': 
                            wk_ability_course_1 =  wk_ability_course_1  + 100.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_1 =  wk_ability_course_1  + 98.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_1 =  wk_ability_course_1  + 94.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_1 =  wk_ability_course_1  + 91.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_1 =  wk_ability_course_1  + 88.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_1 =  wk_ability_course_1  + 85.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_1 =  wk_ability_course_1  + 85.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_1 =  wk_ability_course_1  + 82.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_1 =  wk_ability_course_1  + 77.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_1 =  wk_ability_course_1  + 73.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_1 =  wk_ability_course_1  + 69.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_1 =  wk_ability_course_1  + 65.0
            #----------------------------------------------------------------------------------------------------
            if (str(row2[1]) == '１') and (str(row2[2]) == '逃げ'):
                wk_nige_win_count_course_1 = wk_nige_win_count_course_1  + 1 #逃げ勝ち数
            if (str(row2[1]) != '１') and (str(row2[2]) == 'まくり'):
                wk_makuri_lost_count_course_1 = wk_makuri_lost_count_course_1 + 1 #まくられ数
            if (str(row2[1]) != '１') and (str(row2[2]) == '差し'):
                wk_sashi_lost_count_course_1 = wk_sashi_lost_count_course_1 + 1 #差され数
            if (str(row2[1]) != '１') and (str(row2[2]) == 'まくり差し'):
                wk_sashi_lost_count_course_1 = wk_sashi_lost_count_course_1 + 1 #差され数
        if wk_course_count_1 > 0:
            wk_nige_win_rate_course_1 = (wk_nige_win_count_course_1 / wk_course_count_1) * 100.0
            wk_makuri_lost_rate_course_1 = (wk_makuri_lost_count_course_1 / wk_course_count_1) * 100.0
            wk_sashi_lost_rate_course_1 = (wk_sashi_lost_count_course_1 / wk_course_count_1) * 100.0
            wk_sinnyu_course_1 = (wk_sinnyu_course_1 / wk_course_count_1)
            wk_ability_course_1 = (wk_ability_course_1 / wk_course_count_1)
        #-------------------------------------------------------------------------------------------------------
        t_index_course_count_1 = "%d" % (wk_course_count_1)                             #出走数（１コース）
        t_index_ability_course_1 = "%5.2f" % (wk_ability_course_1)                      #能力値（１コース）
        t_index_sinnyu_course_1 = "%5.2f" % (wk_sinnyu_course_1)                           #進入偏差（１コース）
        t_index_nige_win_count_course_1 = "%d" % (wk_nige_win_count_course_1)           #逃げ切り勝ち数（１コース）
        t_index_nige_win_rate_course_1 = "%5.2f" % (wk_nige_win_rate_course_1)          #逃げ切り勝ち率（１コース）
        t_index_makuri_lost_count_course_1 = "%d" % (wk_makuri_lost_count_course_1)     #まくられ数（１コース）
        t_index_makuri_lost_rate_course_1 = "%5.2f" % (wk_makuri_lost_rate_course_1)    #まくられ率（１コース）
        t_index_sashi_lost_count_course_1 = "%d" % (wk_sashi_lost_count_course_1)       #差され数（１コース）
        t_index_sashi_lost_rate_course_1 = "%5.2f" % (wk_sashi_lost_rate_course_1)      #差され率（１コース）

        #コース別能力算出　２コース
        #出走数（２コース）t_index_course_count_2 
        #能力値（２コース）t_index_ability_course_2
        #進入偏差（２コース）t_index_sinnyu_course_2
        #逃し数（２コース）t_index_nige_lost_count_course_2 
        #逃し率（２コース）t_index_nige_lost_rate_course_2
        #まくり数（２コース）_index_makuri_win_count_course_2
        #まくり率（２コース）t_index_makuri_win_rate_course_2
        #差し数（２コース）t_index_sashi_win_count_course_2
        #差し率（２コース）t_index_sashi_win_rate_course_2

        wk_course_count_2 = 0.0                 #出走数
        wk_nige_lost_count_course_2 = 0         #逃がし数
        wk_nige_lost_rate_course_2 = 0.0        #逃がし率
        wk_makuri_win_count_course_2 = 0        #まくり勝ち数
        wk_makuri_win_rate_course_2 = 0.0       #まくり勝ち率
        wk_sashi_win_count_course_2 = 0         #差し勝ち数
        wk_sashi_win_rate_course_2 = 0.0        #差し勝ち率
        wk_sinnyu_course_2 = 0                  #進入偏差
        wk_ability_course_2 = 0.0               #能力値

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_result_d.course,t_result_d.ranking,t_result_h.decisive_factor, t_result_d.entry_no, t_race_t.grade, t_race_h.race_name "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_d, t_result_d, t_result_h, t_race_t, t_race_h "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_result_h.yyyymmdd = t_race_d.yyyymmdd AND t_result_h.pool_code = t_race_d.pool_code AND t_result_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_result_d.course = '2' "
        wk_sql2 = wk_sql2 + "AND t_race_d.player_no = '" + t_index_player_no + "' "  
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_date12 + "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "
        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            wk_course_count_2 = wk_course_count_2 + 1 #出走数
            wk_sinnyu_course_2 = wk_sinnyu_course_2 + (2 - int(row2[3])) #進入偏差
            if (str(row2[4]) == '一般・若手') or (str(row2[4]) == '一般・女子') or (str(row2[4]) == '一般') or (str(row2[4]) == 'Ｇ３・女子') or (str(row2[4]) == 'Ｇ３'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１':
                            wk_ability_course_2 = wk_ability_course_2  + 65.0
                        if str(row2[1]) == '２':
                            wk_ability_course_2 = wk_ability_course_2  + 63.0
                        if str(row2[1]) == '３':
                            wk_ability_course_2 = wk_ability_course_2  + 59.0
                        if str(row2[1]) == '４':
                            wk_ability_course_2 = wk_ability_course_2  + 56.0
                        if str(row2[1]) == '５':
                            wk_ability_course_2 = wk_ability_course_2  + 53.0
                        if str(row2[1]) == '６':
                            wk_ability_course_2 = wk_ability_course_2  + 50.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_2 =  wk_ability_course_2  + 60.0
                        if str(row2[1]) == '２':
                            wk_ability_course_2 =  wk_ability_course_2  + 58.0
                        if str(row2[1]) == '３':
                            wk_ability_course_2 =  wk_ability_course_2  + 55.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_2 =  wk_ability_course_2  + 50.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_2 =  wk_ability_course_2  + 40.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_2 =  wk_ability_course_2  + 30.0
            if (str(row2[4]) == 'Ｇ２・女子') or (str(row2[4]) == 'Ｇ２'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１': 
                            wk_ability_course_2 =  wk_ability_course_2  + 80.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_2 =  wk_ability_course_2  + 78.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_2 =  wk_ability_course_2  + 74.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_2 =  wk_ability_course_2  + 71.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_2 =  wk_ability_course_2  + 68.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_2 =  wk_ability_course_2  + 65.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_2 =  wk_ability_course_2  + 70.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_2 =  wk_ability_course_2  + 67.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_2 =  wk_ability_course_2  + 62.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_2 =  wk_ability_course_2  + 58.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_2 =  wk_ability_course_2  + 54.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_2 =  wk_ability_course_2  + 50.0
            if (str(row2[4]) == 'Ｇ１・女子') or (str(row2[4]) == 'Ｇ１')  or (str(row2[4]) == 'ＳＧ'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１': 
                            wk_ability_course_2 =  wk_ability_course_2  + 100.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_2 =  wk_ability_course_2  + 98.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_2 =  wk_ability_course_2  + 94.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_2 =  wk_ability_course_2  + 91.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_2 =  wk_ability_course_2  + 88.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_2 =  wk_ability_course_2  + 85.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_2 =  wk_ability_course_2  + 85.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_2 =  wk_ability_course_2  + 82.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_2 =  wk_ability_course_2  + 77.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_2 =  wk_ability_course_2  + 73.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_2 =  wk_ability_course_2  + 69.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_2 =  wk_ability_course_2  + 65.0
                #---------------------------------------------------------------------------------------------------- 

                        #----------------------------------------------------------------------------------------------------
            #----------------------------------------------------------------------------------------------------
            if (str(row2[1]) != '１') and (str(row2[2]) == '逃げ'):
                wk_nige_lost_count_course_2 = wk_nige_lost_count_course_2  + 1 #逃し数
            if (str(row2[1]) == '１') and (str(row2[2]) == 'まくり'):
                wk_makuri_win_count_course_2 = wk_makuri_win_count_course_2 + 1 #まくり数
            if (str(row2[1]) == '１') and (str(row2[2]) == '差し'):
                wk_sashi_win_count_course_2 = wk_sashi_win_count_course_2 + 1 #差し数
            if (str(row2[1]) == '１') and (str(row2[2]) == 'まくり差し'):
                wk_sashi_win_count_course_2 = wk_sashi_win_count_course_2 + 1 #差し数
            #----------------------------------------------------------------------------------------------------
        if wk_course_count_2 > 0:
            wk_nige_lost_rate_course_2  = (wk_nige_lost_count_course_2 / wk_course_count_2) * 100.0
            wk_makuri_win_rate_course_2 = (wk_makuri_win_count_course_2 / wk_course_count_2) * 100.0
            wk_sashi_win_rate_course_2  = (wk_sashi_win_count_course_2 / wk_course_count_2) * 100.0
            wk_sinnyu_course_2 = (wk_sinnyu_course_2 / wk_course_count_2)
            wk_ability_course_2 = (wk_ability_course_2 / wk_course_count_2)
        #-------------------------------------------------------------------------------------------------------
        t_index_course_count_2 = '%d' % (wk_course_count_2)                             #出走数（２コース）
        t_index_ability_course_2 = '%5.2f' % (wk_ability_course_2)                      #能力値（２コース）
        t_index_sinnyu_course_2 = '%5.2f' % (wk_sinnyu_course_2)                        #進入偏差（２コース）
        t_index_nige_lost_count_course_2 = '%d' % (wk_nige_lost_count_course_2)      #逃し数（２コース）
        t_index_nige_lost_rate_course_2 = '%5.2f' % (wk_nige_lost_rate_course_2)        #逃し率（２コース）
        t_index_makuri_win_count_course_2 = '%d' % (wk_makuri_win_count_course_2)    #まくり数（２コース）
        t_index_makuri_win_rate_course_2 = '%5.2f' % (wk_makuri_win_rate_course_2)      #まくり率（２コース）
        t_index_sashi_win_count_course_2 = '%d' % (wk_sashi_win_count_course_2)      #差し数（２コース）
        t_index_sashi_win_rate_course_2 = '%5.2f' % (wk_sashi_win_rate_course_2)        #差し率（２コース）
        
        #コース別能力算出　３コース
        #出走数（３コース）t_index_course_count_3
        #能力値（３コース）t_index_ability_course_3
        #進入偏差（３コース）t_index_sinnyu_course_3
        #まくり数（３コース）t_index_makuri_win_count_course_3
        #まくり率（３コース）t_index_makuri_win_rate_course_3
        #差し数（３コース）t_index_sashi_win_count_course_3
        #差し率（３コース）t_index_sashi_win_rate_course_3

        wk_course_count_3 = 0.0                 #出走数
        wk_makuri_win_count_course_3 = 0        #まくり勝ち数
        wk_makuri_win_rate_course_3 = 0.0       #まくり勝ち率
        wk_sashi_win_count_course_3 = 0         #差し勝ち数
        wk_sashi_win_rate_course_3 = 0.0        #差し勝ち率
        wk_sinnyu_course_3 = 0                  #進入偏差
        wk_ability_course_3 = 0.0               #能力値

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_result_d.course,t_result_d.ranking,t_result_h.decisive_factor, t_result_d.entry_no, t_race_t.grade, t_race_h.race_name "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_d, t_result_d, t_result_h, t_race_t, t_race_h "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_result_h.yyyymmdd = t_race_d.yyyymmdd AND t_result_h.pool_code = t_race_d.pool_code AND t_result_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_result_d.course = '3' "
        wk_sql2 = wk_sql2 + "AND t_race_d.player_no = '" + t_index_player_no + "' "  
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_date12 + "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "
        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            wk_course_count_3 = wk_course_count_3 + 1 #出走数
            wk_sinnyu_course_3 = wk_sinnyu_course_3 + (3 - int(row2[3])) #進入偏差
            if (str(row2[4]) == '一般・若手') or (str(row2[4]) == '一般・女子') or (str(row2[4]) == '一般') or (str(row2[4]) == 'Ｇ３・女子') or (str(row2[4]) == 'Ｇ３'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１':
                            wk_ability_course_3 = wk_ability_course_3  + 65.0
                        if str(row2[1]) == '２':
                            wk_ability_course_3 = wk_ability_course_3  + 63.0
                        if str(row2[1]) == '３':
                            wk_ability_course_3 = wk_ability_course_3  + 59.0
                        if str(row2[1]) == '４':
                            wk_ability_course_3 = wk_ability_course_3  + 56.0
                        if str(row2[1]) == '５':
                            wk_ability_course_3 = wk_ability_course_3  + 53.0
                        if str(row2[1]) == '６':
                            wk_ability_course_3 = wk_ability_course_3  + 50.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_3 =  wk_ability_course_3  + 60.0
                        if str(row2[1]) == '２':
                            wk_ability_course_3 =  wk_ability_course_3  + 58.0
                        if str(row2[1]) == '３':
                            wk_ability_course_3 =  wk_ability_course_3  + 55.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_3 =  wk_ability_course_3  + 50.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_3 =  wk_ability_course_3  + 40.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_3 =  wk_ability_course_3  + 30.0
            if (str(row2[4]) == 'Ｇ２・女子') or (str(row2[4]) == 'Ｇ２'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１': 
                            wk_ability_course_3 =  wk_ability_course_3  + 80.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_3 =  wk_ability_course_3  + 78.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_3 =  wk_ability_course_3  + 74.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_3 =  wk_ability_course_3  + 71.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_3 =  wk_ability_course_3  + 68.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_3 =  wk_ability_course_3  + 65.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_3 =  wk_ability_course_3  + 70.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_3 =  wk_ability_course_3  + 67.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_3 =  wk_ability_course_3  + 62.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_3 =  wk_ability_course_3  + 58.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_3 =  wk_ability_course_3  + 54.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_3 =  wk_ability_course_3  + 50.0
            if (str(row2[4]) == 'Ｇ１・女子') or (str(row2[4]) == 'Ｇ１')  or (str(row2[4]) == 'ＳＧ'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１': 
                            wk_ability_course_3 =  wk_ability_course_3  + 100.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_3 =  wk_ability_course_3  + 98.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_3 =  wk_ability_course_3  + 94.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_3 =  wk_ability_course_3  + 91.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_3 =  wk_ability_course_3  + 88.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_3 =  wk_ability_course_3  + 85.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_3 =  wk_ability_course_3  + 85.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_3 =  wk_ability_course_3  + 82.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_3 =  wk_ability_course_3  + 77.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_3 =  wk_ability_course_3  + 73.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_3 =  wk_ability_course_3  + 69.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_3 =  wk_ability_course_3  + 65.0
                #---------------------------------------------------------------------------------------------------- 
            #----------------------------------------------------------------------------------------------------
            if (str(row2[1]) == '１') and (str(row2[2]) == 'まくり'):
                wk_makuri_win_count_course_3 = wk_makuri_win_count_course_3 + 1 #まくり数
            if (str(row2[1]) == '１') and (str(row2[2]) == '差し'):
                wk_sashi_win_count_course_3 = wk_sashi_win_count_course_3 + 1 #差し数
            if (str(row2[1]) == '１') and (str(row2[2]) == 'まくり差し'):
                wk_sashi_win_count_course_3 = wk_sashi_win_count_course_3 + 1 #差し数
            #----------------------------------------------------------------------------------------------------
        if wk_course_count_3 > 0:
            wk_makuri_win_rate_course_3 = (wk_makuri_win_count_course_3 / wk_course_count_3) * 100.0
            wk_sashi_win_rate_course_3  = (wk_sashi_win_count_course_3 / wk_course_count_3) * 100.0
            wk_sinnyu_course_3 = (wk_sinnyu_course_3 / wk_course_count_3)
            wk_ability_course_3 = (wk_ability_course_3 / wk_course_count_3)
        #-------------------------------------------------------------------------------------------------------
        t_index_course_count_3 = '%d' % (wk_course_count_3)                             #出走数（３コース）
        t_index_ability_course_3 = '%5.2f' % (wk_ability_course_3)                      #能力値（３コース）
        t_index_sinnyu_course_3 = '%5.2f' % (wk_sinnyu_course_3)                        #進入偏差（３コース）
        t_index_makuri_win_count_course_3 = '%d' % (wk_makuri_win_count_course_3)       #まくり数（３コース）
        t_index_makuri_win_rate_course_3 = '%5.2f' % (wk_makuri_win_rate_course_3)      #まくり率（３コース）
        t_index_sashi_win_count_course_3 = '%d' % (wk_sashi_win_count_course_3)         #差し数（３コース）
        t_index_sashi_win_rate_course_3 = '%5.2f' % (wk_sashi_win_rate_course_3)        #差し率（３コース）

        #コース別能力算出　４コース
        #出走数（４コース）t_index_course_count_4
        #能力値（４コース）t_index_ability_course_4
        #進入偏差（４コース）t_index_sinnyu_course_4
        #まくり数（４コース）t_index_makuri_win_count_course_4
        #まくり率（４コース）t_index_makuri_win_rate_course_4
        #差し数（４コース）t_index_sashi_win_count_course_4
        #差し率（４コース）t_index_sashi_win_rate_course_4

        wk_course_count_4 = 0.0                 #出走数
        wk_makuri_win_count_course_4 = 0        #まくり勝ち数
        wk_makuri_win_rate_course_4 = 0.0       #まくり勝ち率
        wk_sashi_win_count_course_4 = 0         #差し勝ち数
        wk_sashi_win_rate_course_4 = 0.0        #差し勝ち率
        wk_sinnyu_course_4 = 0                  #進入偏差
        wk_ability_course_4 = 0.0               #能力値

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_result_d.course,t_result_d.ranking,t_result_h.decisive_factor, t_result_d.entry_no, t_race_t.grade, t_race_h.race_name "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_d, t_result_d, t_result_h, t_race_t, t_race_h "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_result_h.yyyymmdd = t_race_d.yyyymmdd AND t_result_h.pool_code = t_race_d.pool_code AND t_result_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_result_d.course = '4' "
        wk_sql2 = wk_sql2 + "AND t_race_d.player_no = '" + t_index_player_no + "' "  
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_date12 + "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "
        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            wk_course_count_4 = wk_course_count_4 + 1 #出走数
            wk_sinnyu_course_4 = wk_sinnyu_course_4 + (4 - int(row2[3])) #進入偏差
            if (str(row2[4]) == '一般・若手') or (str(row2[4]) == '一般・女子') or (str(row2[4]) == '一般') or (str(row2[4]) == 'Ｇ３・女子') or (str(row2[4]) == 'Ｇ３'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１':
                            wk_ability_course_4 = wk_ability_course_4  + 65.0
                        if str(row2[1]) == '２':
                            wk_ability_course_4 = wk_ability_course_4  + 63.0
                        if str(row2[1]) == '３':
                            wk_ability_course_4 = wk_ability_course_4  + 59.0
                        if str(row2[1]) == '４':
                            wk_ability_course_4 = wk_ability_course_4  + 56.0
                        if str(row2[1]) == '５':
                            wk_ability_course_4 = wk_ability_course_4  + 53.0
                        if str(row2[1]) == '６':
                            wk_ability_course_4 = wk_ability_course_4  + 50.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_4 =  wk_ability_course_4  + 60.0
                        if str(row2[1]) == '２':
                            wk_ability_course_4 =  wk_ability_course_4  + 58.0
                        if str(row2[1]) == '３':
                            wk_ability_course_4 =  wk_ability_course_4  + 55.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_4 =  wk_ability_course_4  + 50.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_4 =  wk_ability_course_4  + 40.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_4 =  wk_ability_course_4  + 30.0
            if (str(row2[4]) == 'Ｇ２・女子') or (str(row2[4]) == 'Ｇ２'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１': 
                            wk_ability_course_4 =  wk_ability_course_4  + 80.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_4 =  wk_ability_course_4  + 78.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_4 =  wk_ability_course_4  + 74.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_4 =  wk_ability_course_4  + 71.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_4 =  wk_ability_course_4  + 68.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_4 =  wk_ability_course_4  + 65.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_4 =  wk_ability_course_4  + 70.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_4 =  wk_ability_course_4  + 67.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_4 =  wk_ability_course_4  + 62.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_4 =  wk_ability_course_4  + 58.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_4 =  wk_ability_course_4  + 54.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_4 =  wk_ability_course_4  + 50.0
            if (str(row2[4]) == 'Ｇ１・女子') or (str(row2[4]) == 'Ｇ１')  or (str(row2[4]) == 'ＳＧ'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１': 
                            wk_ability_course_4 =  wk_ability_course_4  + 100.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_4 =  wk_ability_course_4  + 98.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_4 =  wk_ability_course_4  + 94.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_4 =  wk_ability_course_4  + 91.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_4 =  wk_ability_course_4  + 88.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_4 =  wk_ability_course_4  + 85.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_4 =  wk_ability_course_4  + 85.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_4 =  wk_ability_course_4  + 82.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_4 =  wk_ability_course_4  + 77.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_4 =  wk_ability_course_4  + 73.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_4 =  wk_ability_course_4  + 69.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_4 =  wk_ability_course_4  + 65.0
                #---------------------------------------------------------------------------------------------------- 
            #----------------------------------------------------------------------------------------------------
            if (str(row2[1]) == '１') and (str(row2[2]) == 'まくり'):
                wk_makuri_win_count_course_4 = wk_makuri_win_count_course_4 + 1 #まくり数
            if (str(row2[1]) == '１') and (str(row2[2]) == '差し'):
                wk_sashi_win_count_course_4 = wk_sashi_win_count_course_4 + 1 #差し数
            if (str(row2[1]) == '１') and (str(row2[2]) == 'まくり差し'):
                wk_sashi_win_count_course_4 = wk_sashi_win_count_course_4 + 1 #差し数
            #----------------------------------------------------------------------------------------------------
        if wk_course_count_4 > 0:
            wk_makuri_win_rate_course_4 = (wk_makuri_win_count_course_4 / wk_course_count_4) * 100.0
            wk_sashi_win_rate_course_4  = (wk_sashi_win_count_course_4 / wk_course_count_4) * 100.0
            wk_sinnyu_course_4 = (wk_sinnyu_course_4 / wk_course_count_4)
            wk_ability_course_4 = (wk_ability_course_4 / wk_course_count_4)
        #-------------------------------------------------------------------------------------------------------
        t_index_course_count_4 = '%d' % (wk_course_count_4)                             #出走数（４コース）
        t_index_ability_course_4 = '%5.2f' % (wk_ability_course_4)                      #能力値（４コース）
        t_index_sinnyu_course_4 = '%5.2f' % (wk_sinnyu_course_4)                        #進入偏差（４コース）
        t_index_makuri_win_count_course_4 = '%d' % (wk_makuri_win_count_course_4)       #まくり数（４コース）
        t_index_makuri_win_rate_course_4 = '%5.2f' % (wk_makuri_win_rate_course_4)      #まくり率（４コース）
        t_index_sashi_win_count_course_4 = '%d' % (wk_sashi_win_count_course_4)         #差し数（４コース）
        t_index_sashi_win_rate_course_4 = '%5.2f' % (wk_sashi_win_rate_course_4)        #差し率（４コース）

        #コース別能力算出　５コース
        #出走数（５コース）t_index_course_count_5
        #能力値（５コース）t_index_ability_course_5
        #進入偏差（５コース）t_index_sinnyu_course_5
        #まくり数（５コース）t_index_makuri_win_count_course_5
        #まくり率（５コース）t_index_makuri_win_rate_course_5
        #差し数（５コース）t_index_sashi_win_count_course_5
        #差し率（５コース）t_index_sashi_win_rate_course_5

        wk_course_count_5 = 0.0                 #出走数
        wk_makuri_win_count_course_5 = 0        #まくり勝ち数
        wk_makuri_win_rate_course_5 = 0.0       #まくり勝ち率
        wk_sashi_win_count_course_5 = 0         #差し勝ち数
        wk_sashi_win_rate_course_5 = 0.0        #差し勝ち率
        wk_sinnyu_course_5 = 0                  #進入偏差
        wk_ability_course_5 = 0.0               #能力値

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_result_d.course,t_result_d.ranking,t_result_h.decisive_factor, t_result_d.entry_no, t_race_t.grade, t_race_h.race_name "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_d, t_result_d, t_result_h, t_race_t, t_race_h "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_result_h.yyyymmdd = t_race_d.yyyymmdd AND t_result_h.pool_code = t_race_d.pool_code AND t_result_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_result_d.course = '5' "
        wk_sql2 = wk_sql2 + "AND t_race_d.player_no = '" + t_index_player_no + "' "  
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_date12 + "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "
        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            wk_course_count_5 = wk_course_count_5 + 1 #出走数
            wk_sinnyu_course_5 = wk_sinnyu_course_5 + (5 - int(row2[3])) #進入偏差
            if (str(row2[4]) == '一般・若手') or (str(row2[4]) == '一般・女子') or (str(row2[4]) == '一般') or (str(row2[4]) == 'Ｇ３・女子') or (str(row2[4]) == 'Ｇ３'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１':
                            wk_ability_course_5 = wk_ability_course_5  + 65.0
                        if str(row2[1]) == '２':
                            wk_ability_course_5 = wk_ability_course_5  + 63.0
                        if str(row2[1]) == '３':
                            wk_ability_course_5 = wk_ability_course_5  + 59.0
                        if str(row2[1]) == '４':
                            wk_ability_course_5 = wk_ability_course_5  + 56.0
                        if str(row2[1]) == '５':
                            wk_ability_course_5 = wk_ability_course_5  + 53.0
                        if str(row2[1]) == '６':
                            wk_ability_course_5 = wk_ability_course_5  + 50.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_5 =  wk_ability_course_5  + 60.0
                        if str(row2[1]) == '２':
                            wk_ability_course_5 =  wk_ability_course_5  + 58.0
                        if str(row2[1]) == '３':
                            wk_ability_course_5 =  wk_ability_course_5  + 55.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_5 =  wk_ability_course_5  + 50.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_5 =  wk_ability_course_5  + 40.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_5 =  wk_ability_course_5  + 30.0
            if (str(row2[4]) == 'Ｇ２・女子') or (str(row2[4]) == 'Ｇ２'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１': 
                            wk_ability_course_5 =  wk_ability_course_5  + 80.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_5 =  wk_ability_course_5  + 78.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_5 =  wk_ability_course_5  + 74.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_5 =  wk_ability_course_5  + 71.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_5 =  wk_ability_course_5  + 68.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_5 =  wk_ability_course_5  + 65.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_5 =  wk_ability_course_5  + 70.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_5 =  wk_ability_course_5  + 67.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_5 =  wk_ability_course_5  + 62.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_5 =  wk_ability_course_5  + 58.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_5 =  wk_ability_course_5  + 54.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_5 =  wk_ability_course_5  + 50.0
            if (str(row2[4]) == 'Ｇ１・女子') or (str(row2[4]) == 'Ｇ１')  or (str(row2[4]) == 'ＳＧ'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１': 
                            wk_ability_course_5 =  wk_ability_course_5  + 100.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_5 =  wk_ability_course_5  + 98.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_5 =  wk_ability_course_5  + 94.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_5 =  wk_ability_course_5  + 91.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_5 =  wk_ability_course_5  + 88.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_5 =  wk_ability_course_5  + 85.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_5 =  wk_ability_course_5  + 85.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_5 =  wk_ability_course_5  + 82.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_5 =  wk_ability_course_5  + 77.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_5 =  wk_ability_course_5  + 73.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_5 =  wk_ability_course_5  + 69.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_5 =  wk_ability_course_5  + 65.0
                #---------------------------------------------------------------------------------------------------- 
            #----------------------------------------------------------------------------------------------------
            if (str(row2[1]) == '１') and (str(row2[2]) == 'まくり'):
                wk_makuri_win_count_course_5 = wk_makuri_win_count_course_5 + 1 #まくり数
            if (str(row2[1]) == '１') and (str(row2[2]) == '差し'):
                wk_sashi_win_count_course_5 = wk_sashi_win_count_course_5 + 1 #差し数
            if (str(row2[1]) == '１') and (str(row2[2]) == 'まくり差し'):
                wk_sashi_win_count_course_5 = wk_sashi_win_count_course_5 + 1 #差し数
            #----------------------------------------------------------------------------------------------------
        if wk_course_count_5 > 0:
            wk_makuri_win_rate_course_5 = (wk_makuri_win_count_course_5 / wk_course_count_5) * 100.0
            wk_sashi_win_rate_course_5  = (wk_sashi_win_count_course_5 / wk_course_count_5) * 100.0
            wk_sinnyu_course_5 = (wk_sinnyu_course_5 / wk_course_count_5)
            wk_ability_course_5 = (wk_ability_course_5 / wk_course_count_5)
        #-------------------------------------------------------------------------------------------------------
        t_index_course_count_5 = '%d' % (wk_course_count_5)                             #出走数（５コース）
        t_index_ability_course_5 = '%5.2f' % (wk_ability_course_5)                      #能力値（５コース）
        t_index_sinnyu_course_5 = '%5.2f' % (wk_sinnyu_course_5)                        #進入偏差（５コース）
        t_index_makuri_win_count_course_5 = '%d' % (wk_makuri_win_count_course_5)       #まくり数（５コース）
        t_index_makuri_win_rate_course_5 = '%5.2f' % (wk_makuri_win_rate_course_5)      #まくり率（５コース）
        t_index_sashi_win_count_course_5 = '%d' % (wk_sashi_win_count_course_5)         #差し数（５コース）
        t_index_sashi_win_rate_course_5 = '%5.2f' % (wk_sashi_win_rate_course_5)        #差し率（５コース）

        #コース別能力算出　６コース
        #出走数（６コース）t_index_course_count_6 
        #能力値（６コース）t_index_ability_course_6
        #進入偏差（６コース）t_index_sinnyu_course_6
        #まくり数（６コース）t_index_makuri_win_count_course_6
        #まくり率（６コース) t_index_makuri_win_rate_course_6
        #差し数（６コース）t_index_sashi_win_count_course_6
        #差し率（６コース）t_index_sashi_win_rate_course_6

        wk_course_count_6 = 0.0                 #出走数
        wk_makuri_win_count_course_6 = 0        #まくり勝ち数
        wk_makuri_win_rate_course_6 = 0.0       #まくり勝ち率
        wk_sashi_win_count_course_6 = 0         #差し勝ち数
        wk_sashi_win_rate_course_6 = 0.0        #差し勝ち率
        wk_sinnyu_course_6 = 0                  #進入偏差
        wk_ability_course_6 = 0.0               #能力値

        wk_sql2 = ""
        wk_sql2 = wk_sql2 + "SELECT "
        wk_sql2 = wk_sql2 + "t_result_d.course,t_result_d.ranking,t_result_h.decisive_factor, t_result_d.entry_no, t_race_t.grade, t_race_h.race_name "
        wk_sql2 = wk_sql2 + "FROM "
        wk_sql2 = wk_sql2 + "t_race_d, t_result_d, t_result_h, t_race_t, t_race_h "
        wk_sql2 = wk_sql2 + "WHERE "
        wk_sql2 = wk_sql2 + "t_race_d.yyyymmdd = t_result_d.yyyymmdd AND t_race_d.pool_code = t_result_d.pool_code AND t_race_d.race_no = t_result_d.race_no AND t_race_d.entry_no = t_result_d.entry_no "
        wk_sql2 = wk_sql2 + "AND t_result_h.yyyymmdd = t_race_d.yyyymmdd AND t_result_h.pool_code = t_race_d.pool_code AND t_result_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_h.yyyymmdd = t_race_d.yyyymmdd AND t_race_h.pool_code = t_race_d.pool_code AND t_race_h.race_no = t_race_d.race_no "
        wk_sql2 = wk_sql2 + "AND t_race_t.yyyymmdd = t_race_d.yyyymmdd AND t_race_t.pool_code = t_race_d.pool_code "
        wk_sql2 = wk_sql2 + "AND t_result_d.course = '6' "
        wk_sql2 = wk_sql2 + "AND t_race_d.player_no = '" + t_index_player_no + "' "  
        wk_sql2 = wk_sql2 + "AND t_race_d.yyyymmdd  BETWEEN '" + wk_date12 + "' AND '" + t_index_yyyymmdd + "' "
        wk_sql2 = wk_sql2 + "ORDER BY  t_race_d.yyyymmdd DESC "
        cur2 = conn.cursor()
        for row2 in cur2.execute(wk_sql2):
            wk_course_count_6 = wk_course_count_6 + 1 #出走数
            wk_sinnyu_course_6 = wk_sinnyu_course_6 + (6 - int(row2[3])) #進入偏差
            if (str(row2[4]) == '一般・若手') or (str(row2[4]) == '一般・女子') or (str(row2[4]) == '一般') or (str(row2[4]) == 'Ｇ３・女子') or (str(row2[4]) == 'Ｇ３'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１':
                            wk_ability_course_6 = wk_ability_course_6  + 65.0
                        if str(row2[1]) == '２':
                            wk_ability_course_6 = wk_ability_course_6  + 63.0
                        if str(row2[1]) == '３':
                            wk_ability_course_6 = wk_ability_course_6  + 59.0
                        if str(row2[1]) == '４':
                            wk_ability_course_6 = wk_ability_course_6  + 56.0
                        if str(row2[1]) == '５':
                            wk_ability_course_6 = wk_ability_course_6  + 53.0
                        if str(row2[1]) == '６':
                            wk_ability_course_6 = wk_ability_course_6  + 50.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_6 =  wk_ability_course_6  + 60.0
                        if str(row2[1]) == '２':
                            wk_ability_course_6 =  wk_ability_course_6  + 58.0
                        if str(row2[1]) == '３':
                            wk_ability_course_6 =  wk_ability_course_6  + 55.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_6 =  wk_ability_course_6  + 50.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_6 =  wk_ability_course_6  + 40.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_6 =  wk_ability_course_6  + 30.0
            if (str(row2[4]) == 'Ｇ２・女子') or (str(row2[4]) == 'Ｇ２'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１': 
                            wk_ability_course_6 =  wk_ability_course_6  + 80.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_6 =  wk_ability_course_6  + 78.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_6 =  wk_ability_course_6  + 74.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_6 =  wk_ability_course_6  + 71.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_6 =  wk_ability_course_6  + 68.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_6 =  wk_ability_course_6  + 65.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_6 =  wk_ability_course_6  + 70.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_6 =  wk_ability_course_6  + 67.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_6 =  wk_ability_course_6  + 62.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_6 =  wk_ability_course_6  + 58.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_6 =  wk_ability_course_6  + 54.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_6 =  wk_ability_course_6  + 50.0
            if (str(row2[4]) == 'Ｇ１・女子') or (str(row2[4]) == 'Ｇ１')  or (str(row2[4]) == 'ＳＧ'):
                if '優勝戦' in  str(row2[5]):
                        if str(row2[1]) == '１': 
                            wk_ability_course_6 =  wk_ability_course_6  + 100.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_6 =  wk_ability_course_6  + 98.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_6 =  wk_ability_course_6  + 94.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_6 =  wk_ability_course_6  + 91.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_6 =  wk_ability_course_6  + 88.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_6 =  wk_ability_course_6  + 85.0
                else:
                        if str(row2[1]) == '１': 
                            wk_ability_course_6 =  wk_ability_course_6  + 85.0
                        if str(row2[1]) == '２': 
                            wk_ability_course_6 =  wk_ability_course_6  + 82.0
                        if str(row2[1]) == '３': 
                            wk_ability_course_6 =  wk_ability_course_6  + 77.0
                        if str(row2[1]) == '４': 
                            wk_ability_course_6 =  wk_ability_course_6  + 73.0
                        if str(row2[1]) == '５': 
                            wk_ability_course_6 =  wk_ability_course_6  + 69.0
                        if str(row2[1]) == '６': 
                            wk_ability_course_6 =  wk_ability_course_6  + 65.0
                #---------------------------------------------------------------------------------------------------- 
            #----------------------------------------------------------------------------------------------------
            if (str(row2[1]) == '１') and (str(row2[2]) == 'まくり'):
                wk_makuri_win_count_course_6 = wk_makuri_win_count_course_6 + 1 #まくり数
            if (str(row2[1]) == '１') and (str(row2[2]) == '差し'):
                wk_sashi_win_count_course_6 = wk_sashi_win_count_course_6 + 1 #差し数
            if (str(row2[1]) == '１') and (str(row2[2]) == 'まくり差し'):
                wk_sashi_win_count_course_6 = wk_sashi_win_count_course_6 + 1 #差し数
            #----------------------------------------------------------------------------------------------------
        if wk_course_count_6 > 0:
            wk_makuri_win_rate_course_6 = (wk_makuri_win_count_course_6 / wk_course_count_6) * 100.0
            wk_sashi_win_rate_course_6  = (wk_sashi_win_count_course_6 / wk_course_count_6) * 100.0
            wk_sinnyu_course_6 = (wk_sinnyu_course_6 / wk_course_count_6)
            wk_ability_course_6 = (wk_ability_course_6 / wk_course_count_6)
        #-------------------------------------------------------------------------------------------------------
        t_index_course_count_6 = '%d' % (wk_course_count_6)                             #出走数（６コース）
        t_index_ability_course_6 = '%5.2f' % (wk_ability_course_6)                      #能力値（６コース）
        t_index_sinnyu_course_6 = '%5.2f' % (wk_sinnyu_course_6)                        #進入偏差（６コース）
        t_index_makuri_win_count_course_6 = '%d' % (wk_makuri_win_count_course_6)       #まくり数（６コース）
        t_index_makuri_win_rate_course_6 = '%5.2f' % (wk_makuri_win_rate_course_6)      #まくり率（６コース）
        t_index_sashi_win_count_course_6 = '%d' % (wk_sashi_win_count_course_6)         #差し数（６コース）
        t_index_sashi_win_rate_course_6 = '%5.2f' % (wk_sashi_win_rate_course_6)        #差し率（６コース）

        #レコード組立
        outrec = ''
        outrec = outrec       +  '"' + t_index_yyyymmdd + '"'              #開催日付
        outrec = outrec + ',' +  '"' + t_index_pool_code + '"'             #場コード
        outrec = outrec + ',' +  '"' + t_index_race_no + '"'               #レース番号
        outrec = outrec + ',' +  '"' + t_index_entry_no + '"'              #枠番
        outrec = outrec + ',' +  '"' + t_index_player_no + '"'             #選手登録番号
        outrec = outrec + ',' +  '"' + t_index_motor_no + '"'              #モーター番号
        outrec = outrec + ',' +  t_index_ability                           #能力
        outrec = outrec + ',' +  t_index_st                                #平均ST
        outrec = outrec + ',' +  t_index_ability_count                     #能力算出対象レース数
        outrec = outrec + ',' +  t_index_ability2                          #直近能力
        outrec = outrec + ',' +  t_index_st2                               #直近平均ST
        outrec = outrec + ',' +  t_index_ability2_count                    #直近能力算出対象
        outrec = outrec + ',' +  t_index_rate_win_motor                    #モーター能力
        outrec = outrec + ',' +  t_index_motor_hensa                       #モーター偏差     
        outrec = outrec + ',' +  t_index_rate_win_count                    #モーター能力算出対象レース数
        outrec = outrec + ',' +  t_index_motor_count1                      #モーター能力算出対象レース数（１コース）
        outrec = outrec + ',' +  t_index_motor_count2                      #モーター能力算出対象レース数（２コース）
        outrec = outrec + ',' +  t_index_motor_count3                      #モーター能力算出対象レース数（３コース）
        outrec = outrec + ',' +  t_index_motor_count4                      #モーター能力算出対象レース数（４コース）
        outrec = outrec + ',' +  t_index_motor_count5                      #モーター能力算出対象レース数（５コース）
        outrec = outrec + ',' +  t_index_motor_count6                      #モーター能力算出対象レース数（６コース）
        outrec = outrec + ',' +  t_index_rate_win_motor_course1            #モーター能力（１コース）
        outrec = outrec + ',' +  t_index_rate_win_motor_course2            #モーター能力（２コース）
        outrec = outrec + ',' +  t_index_rate_win_motor_course3            #モーター能力（３コース）
        outrec = outrec + ',' +  t_index_rate_win_motor_course4            #モーター能力（４コース）
        outrec = outrec + ',' +  t_index_rate_win_motor_course5            #モーター能力（５コース）
        outrec = outrec + ',' +  t_index_rate_win_motor_course6            #モーター能力（６コース）
        outrec = outrec + ',' +  t_index_course_count_1                    #出走数（１コース）
        outrec = outrec + ',' +  t_index_ability_course_1                  #能力値（１コース）
        outrec = outrec + ',' +  t_index_sinnyu_course_1                   #進入偏差（１コース）
        outrec = outrec + ',' +  t_index_nige_win_count_course_1           #逃げ切り勝ち数（１コース）
        outrec = outrec + ',' +  t_index_nige_win_rate_course_1            #逃げ切り勝ち率（１コース）
        outrec = outrec + ',' +  t_index_makuri_lost_count_course_1        #まくられ数（１コース）
        outrec = outrec + ',' +  t_index_makuri_lost_rate_course_1         #まくられ率（１コース）
        outrec = outrec + ',' +  t_index_sashi_lost_count_course_1         #差され数（１コース）
        outrec = outrec + ',' +  t_index_sashi_lost_rate_course_1          #差され率（１コース）
        outrec = outrec + ',' +  t_index_course_count_2                    #出走数（２コース）
        outrec = outrec + ',' +  t_index_ability_course_2                  #能力値（２コース）
        outrec = outrec + ',' +  t_index_sinnyu_course_2                   #進入偏差（２コース）
        outrec = outrec + ',' +  t_index_nige_lost_count_course_2          #逃し数（２コース）
        outrec = outrec + ',' +  t_index_nige_lost_rate_course_2           #逃し率（２コース）
        outrec = outrec + ',' +  t_index_makuri_win_count_course_2         #まくり数（２コース）
        outrec = outrec + ',' +  t_index_makuri_win_rate_course_2          #まくり率（２コース）
        outrec = outrec + ',' +  t_index_sashi_win_count_course_2          #差し数（２コース）
        outrec = outrec + ',' +  t_index_sashi_win_rate_course_2           #差し率（２コース）
        outrec = outrec + ',' +  t_index_course_count_3                    #出走数（３コース）
        outrec = outrec + ',' +  t_index_ability_course_3                  #能力値（３コース）
        outrec = outrec + ',' +  t_index_sinnyu_course_3                   #進入偏差（３コース）
        outrec = outrec + ',' +  t_index_makuri_win_count_course_3         #まくり数（３コース）
        outrec = outrec + ',' +  t_index_makuri_win_rate_course_3          #まくり率（３コース）
        outrec = outrec + ',' +  t_index_sashi_win_count_course_3          #差し数（３コース）
        outrec = outrec + ',' +  t_index_sashi_win_rate_course_3           #差し率（３コース）
        outrec = outrec + ',' +  t_index_course_count_4                    #出走数（４コース）
        outrec = outrec + ',' +  t_index_ability_course_4                  #能力値（４コース）
        outrec = outrec + ',' +  t_index_sinnyu_course_4                   #進入偏差（４コース）
        outrec = outrec + ',' +  t_index_makuri_win_count_course_4         #まくり数（４コース）
        outrec = outrec + ',' +  t_index_makuri_win_rate_course_4          #まくり率（４コース）
        outrec = outrec + ',' +  t_index_sashi_win_count_course_4          #差し数（４コース）
        outrec = outrec + ',' +  t_index_sashi_win_rate_course_4           #差し率（４コース）
        outrec = outrec + ',' +  t_index_course_count_5                    #出走数（５コース）
        outrec = outrec + ',' +  t_index_ability_course_5                  #能力値（５コース）
        outrec = outrec + ',' +  t_index_sinnyu_course_5                   #進入偏差（５コース）
        outrec = outrec + ',' +  t_index_makuri_win_count_course_5         #まくり数（５コース）
        outrec = outrec + ',' +  t_index_makuri_win_rate_course_5          #まくり率（５コース）
        outrec = outrec + ',' +  t_index_sashi_win_count_course_5          #差し数（５コース）
        outrec = outrec + ',' +  t_index_sashi_win_rate_course_5           #差し率（５コース）
        outrec = outrec + ',' +  t_index_course_count_6                    #出走数（６コース）
        outrec = outrec + ',' +  t_index_ability_course_6                  #能力値（６コース）
        outrec = outrec + ',' +  t_index_sinnyu_course_6                   #進入偏差（６コース）
        outrec = outrec + ',' +  t_index_makuri_win_count_course_6         #まくり数（６コース）
        outrec = outrec + ',' +  t_index_makuri_win_rate_course_6          #まくり率（６コース）
        outrec = outrec + ',' +  t_index_sashi_win_count_course_6          # 差し数（６コース）
        outrec = outrec + ',' +  t_index_sashi_win_rate_course_6           # 差し率（６コース）

        #レコード出力
        fw.write(outrec + '\n')
        #残数インクリメント
        zan_count = zan_count - 1



    print('ボートレース関連指数テーブル「t_index」のインポートCSVファイルを作成 完了')
#主処理
mkcsv_t_index() #ボートレース関連指数テーブル「t_index」のインポートCSVファイルを作成
