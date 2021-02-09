'''
【システム】BOAT_RACE_DB2
【ファイル】130_mkcsv_t_race_d.py
【機能仕様】出走表HTMLファイルから出走表明細テーブル「t_tace_d」のインポートCSVファイルを作成する
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.02.01 ver 1.00
'''
import os
import datetime
from bs4 import BeautifulSoup
#インストールディレクトの定義
BASE_DIR = '/home/pi/BOAT_RACE_DB'

'''
【関　数】mkcsv_t_tace_d
【機　能】出走表HTMLファイルから出走表明細テーブル「t_tace_d」のインポートCSVファイルを作成する
【引　数】なし
【戻り値】なし
'''
def mkcsv_t_tace_d():
    print('出走表明細テーブル「t_tace_d」のインポートCSVファイル　開始')
    in_path  = BASE_DIR + '/200_html/race_table'
    out_file = BASE_DIR + '/210_csv/t_race_d.csv'
    fw = open(out_file, 'w')
    for item in os.listdir(path=in_path):
        if item != '.html' and item != '.DS_Store':
            in_file = in_path + '/' + item
            print("==> 処理中[%s]" % (in_file))
            fb = open(in_file, 'r')
            html = fb.read()
            fb.close()
            #データ存在チェック
            flg = 0
            if 'データがありません。' in html:
                flg = 1
            if flg == 0:
                #CSVレコードフィールドの初期化(共通項目)
                t_race_d_yyyymmdd = ''                  #開催日付
                t_race_d_pool_code = ''                 #場コード
                t_race_d_race_no = ''                   #レース番号
                t_race_d_pool_name = ''                 #場名
                #HTMLファイルからcsvレコード項目を抽出
                soup = BeautifulSoup(html, 'html.parser')
                
                #開催日付の抽出
                t_race_d_yyyymmdd = item[0:8]
                #場コードの抽出
                t_race_d_pool_code = item[8:10]
                #レース番号
                t_race_d_race_no  = item[10:12]

                #場名の抽出
                for tag1 in soup.find_all('img'):
                    if '/static_extra/pc/images/text_place2' in str(tag1):
                        for tag2 in str(tag1).splitlines():
                            if '/static_extra/pc/images/text_place2' in str(tag2):
                                wk_arry = str(tag2).split(' ')
                                t_race_d_pool_name = str(wk_arry[1])
                                t_race_d_pool_name = t_race_d_pool_name.replace('alt="','')
                                t_race_d_pool_name = t_race_d_pool_name.replace('"','')   
                #選手単位の明細項目の抽出
                for tag1 in soup.find_all('tbody'):
                    if 'is-fs12' in str(tag1):
                        #CSVレコードフィールドの初期化(選手単位項目)
                        t_race_d_entry_no = ''                  #枠番
                        t_race_d_player_no = ''                 #登録番号
                        t_race_d_plyaer_name = ''               #選手名
                        t_race_d_class = ''                     #級別
                        t_race_d_area = ''                      #支部
                        t_race_d_player_native_place  = ''      #出身地
                        t_race_d_age = ''                       #年齢
                        t_race_d_body_weight = ''               #体重
                        t_race_d_flying_count  = ''             #フライング回数
                        t_race_d_lost_count = ''                #出遅れ回数
                        t_race_d_st = ''                        #平均スタートタイミング
                        t_race_d_nationwide_win_rate = ''       #全国勝率
                        t_race_d_nationwide_double_rate = ''    #全国二連率
                        t_race_d_nationwide_triple_rate = ''    #全国三連率
                        t_race_d_local_win_rate = ''            #当地勝率
                        t_race_d_local_double_rate = ''         #当地二連率
                        t_race_d_local_triple_rate = ''         #当地三連率
                        t_race_d_motor_no = ''                  #モーター番号
                        t_race_d_motor_double_rate = ''         #モーター二連率
                        t_race_d_motor_triple_rate = ''         #モーター三連率
                        t_race_d_boat_no = ''                   #ボート番号
                        t_race_d_boat_double_rate = ''          #ボート二連率
                        t_race_d_boat_triple_rate  = ''         #ボート三連率    

                        #選手単位の明細項目の抽出(枠番)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 3:
                                if '<td class="is-boatColor1 is-fs14" rowspan="4">' in str(tag2):
                                    t_race_d_entry_no = '1'    
                                if '<td class="is-boatColor2 is-fs14" rowspan="4">' in str(tag2):
                                    t_race_d_entry_no = '2'
                                if '<td class="is-boatColor3 is-fs14" rowspan="4">' in str(tag2):
                                    t_race_d_entry_no = '3'   
                                if '<td class="is-boatColor4 is-fs14" rowspan="4">' in str(tag2):
                                    t_race_d_entry_no = '4'    
                                if '<td class="is-boatColor5 is-fs14" rowspan="4">' in str(tag2):
                                    t_race_d_entry_no = '5'
                                if '<td class="is-boatColor6 is-fs14" rowspan="4">' in str(tag2):
                                    t_race_d_entry_no = '6'
                                break

                        #選手単位の明細項目の抽出(登録番号)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n =  n + 1
                            if n == 9:
                                t_race_d_player_no = str(tag2).strip()
                                break
                        
                        #選手単位の明細項目の抽出(選手名)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 13:
                                wk_arry = str(tag2).split('>')
                                t_race_d_plyaer_name = wk_arry[1]
                                t_race_d_plyaer_name = t_race_d_plyaer_name.replace('</a>','')
                                t_race_d_plyaer_name = t_race_d_plyaer_name.replace('</a','')
                                t_race_d_plyaer_name = t_race_d_plyaer_name.replace('　','')    
                                break

                        #選手単位の明細項目の抽出(級別)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n =  n + 1
                            if n == 10:
                                wk_arry = str(tag2).split('>')
                                t_race_d_class = str(wk_arry[1])
                                t_race_d_class = t_race_d_class.replace('</span','')
                                break  

                        #選手単位の明細項目の抽出(支部)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 16:
                                wk_arry = str(tag2).strip().split('/')
                                t_race_d_area = str(wk_arry[0])
                                break

                        #選手単位の明細項目の抽出(出身地)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 16:
                                wk_arry = str(tag2).strip().split('/')
                                t_race_d_player_native_place = str(wk_arry[1])
                                break

                        #選手単位の明細項目の抽出(年齢)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 17:
                                wk_arry = str(tag2).strip().split('歳')
                                t_race_d_age = str(wk_arry[0])
                                t_race_d_age = t_race_d_age.replace('<br/>','')
                                break

                        #選手単位の明細項目の抽出(体重)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 17:
                                wk_arry = str(tag2).strip().split('歳')
                                t_race_d_body_weight = str(wk_arry[1])
                                t_race_d_body_weight = t_race_d_body_weight.replace('/','')
                                t_race_d_body_weight = t_race_d_body_weight.replace('kg','')
                                break

                        #選手単位の明細項目の抽出(フライング回数)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 21:
                                t_race_d_flying_count = str(tag2).strip()
                                t_race_d_flying_count = t_race_d_flying_count.replace('F','')
                                break

                        #選手単位の明細項目の抽出(出遅れ回数)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 22:
                                t_race_d_lost_count = str(tag2).strip()
                                t_race_d_lost_count = t_race_d_lost_count.replace('<br/>L','')
                                break

                        #選手単位の明細項目の抽出(平均スタートタイミング)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 23:
                                t_race_d_st = str(tag2).strip()
                                t_race_d_st = t_race_d_st.replace('<br/>','')
                                break

                        #選手単位の明細項目の抽出(全国勝率)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 26:
                                t_race_d_nationwide_win_rate = str(tag2).strip()
                                break

                        #選手単位の明細項目の抽出(全国二連率)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 27:
                                t_race_d_nationwide_double_rate = str(tag2).strip()
                                t_race_d_nationwide_double_rate = t_race_d_nationwide_double_rate.replace('<br/>','')
                                break

                        #選手単位の明細項目の抽出(全国三連率)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 28:
                                t_race_d_nationwide_triple_rate = str(tag2).strip()
                                t_race_d_nationwide_triple_rate = t_race_d_nationwide_triple_rate.replace('<br/>','')
                                break

                        #選手単位の明細項目の抽出(当地勝率)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 31:
                                t_race_d_local_win_rate = str(tag2).strip()
                                break

                        #選手単位の明細項目の抽出(当地二連率)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 32:
                                t_race_d_local_double_rate = str(tag2).strip()
                                t_race_d_local_double_rate = t_race_d_local_double_rate.replace('<br/>','')
                                break
                        
                        #選手単位の明細項目の抽出(当地三連率)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 33:
                                t_race_d_local_triple_rate = str(tag2).strip()
                                t_race_d_local_triple_rate = t_race_d_local_triple_rate.replace('<br/>','')
                                break
                        
                        #選手単位の明細項目の抽出(モーター番号)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 36:
                                t_race_d_motor_no = str(tag2).strip()
                                break
                        
                        #選手単位の明細項目の抽出(モーター二連率)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 37:
                                t_race_d_motor_double_rate = str(tag2).strip()
                                t_race_d_motor_double_rate = t_race_d_motor_double_rate.replace('<br/>','')
                                break
                        
                        #選手単位の明細項目の抽出(モーター三連率)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 38:
                                t_race_d_motor_triple_rate = str(tag2).strip()
                                t_race_d_motor_triple_rate = t_race_d_motor_triple_rate.replace('<br/>','')
                                break
                        
                        #選手単位の明細項目の抽出(ボート番号)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 41:
                                t_race_d_boat_no = str(tag2).strip()
                                break
                        
                        #選手単位の明細項目の抽出(ボート二連率)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 42:
                                t_race_d_boat_double_rate = str(tag2).strip()
                                t_race_d_boat_double_rate = t_race_d_boat_double_rate.replace('<br/>','')
                                break
                        
                        #選手単位の明細項目の抽出(ボート三連率) 
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 43:
                                t_race_d_boat_triple_rate = str(tag2).strip()
                                t_race_d_boat_triple_rate = t_race_d_boat_triple_rate.replace('<br/>','')
                                break 
                        #CSVレコードの生成
                        t_race_d_outrec = ''
                        t_race_d_outrec = t_race_d_outrec + '"' + t_race_d_yyyymmdd + '"'               #開催日付
                        t_race_d_outrec = t_race_d_outrec + ',"' + t_race_d_pool_code + '"'             #場コード
                        t_race_d_outrec = t_race_d_outrec + ',"' + t_race_d_race_no + '"'               #レース番号
                        t_race_d_outrec = t_race_d_outrec + ',"' + t_race_d_entry_no + '"'              #枠番
                        t_race_d_outrec = t_race_d_outrec + ',"' + t_race_d_pool_name + '"'             #場名
                        t_race_d_outrec = t_race_d_outrec + ',"' + t_race_d_player_no + '"'             #登録番号
                        t_race_d_outrec = t_race_d_outrec + ',"' + t_race_d_plyaer_name + '"'           #選手名
                        t_race_d_outrec = t_race_d_outrec + ',"' + t_race_d_class + '"'                 #級別
                        t_race_d_outrec = t_race_d_outrec + ',"' + t_race_d_area + '"'                  #支部
                        t_race_d_outrec = t_race_d_outrec + ',"' + t_race_d_player_native_place + '"'   #出身地
                        t_race_d_outrec = t_race_d_outrec + ',' + t_race_d_age                          #年齢
                        t_race_d_outrec = t_race_d_outrec + ',' + t_race_d_body_weight                  #体重
                        t_race_d_outrec = t_race_d_outrec + ',' + t_race_d_flying_count                 #フライング回数
                        t_race_d_outrec = t_race_d_outrec + ',' + t_race_d_lost_count                   #出遅れ回数
                        t_race_d_outrec = t_race_d_outrec + ',' + t_race_d_st                           #平均スタートタイミング
                        t_race_d_outrec = t_race_d_outrec + ',' + t_race_d_nationwide_win_rate          #全国勝率
                        t_race_d_outrec = t_race_d_outrec + ',' + t_race_d_nationwide_double_rate       #全国二連率
                        t_race_d_outrec = t_race_d_outrec + ',' + t_race_d_nationwide_triple_rate       #全国三連率
                        t_race_d_outrec = t_race_d_outrec + ',' + t_race_d_local_win_rate               #当地勝率
                        t_race_d_outrec = t_race_d_outrec + ',' + t_race_d_local_double_rate            #当地二連率
                        t_race_d_outrec = t_race_d_outrec + ',' + t_race_d_local_triple_rate            #当地三連率
                        t_race_d_outrec = t_race_d_outrec + ',"' + t_race_d_motor_no + '"'              #モーター番号
                        t_race_d_outrec = t_race_d_outrec + ',' + t_race_d_motor_double_rate            #モーター二連率
                        t_race_d_outrec = t_race_d_outrec + ',' + t_race_d_motor_triple_rate            #モーター三連率
                        t_race_d_outrec = t_race_d_outrec + ',"' + t_race_d_boat_no + '"'               #ボート番号
                        t_race_d_outrec = t_race_d_outrec + ',' + t_race_d_boat_double_rate             #ボート二連率
                        t_race_d_outrec = t_race_d_outrec + ',' + t_race_d_boat_triple_rate             #ボート三連率
                        #CSVレコードファイル出力
                        fw.write(t_race_d_outrec + '\n')
    fw.close()
    print('出走表明細テーブル「t_tace_d」のインポートCSVファイル　完了')

#主処理
mkcsv_t_tace_d() #出走表テーブル「t_tace_d」のインポートCSVファイルを作成
