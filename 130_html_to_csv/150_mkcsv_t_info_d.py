'''
【システム】BOAT_RACE_DB2
【ファイル】140_mkcsv_t_info_d.py
【機能仕様】直前情報HTMLファイルから直前情報明細テーブル「t_info_d」のインポートCSVファイルを作成する
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.02.01 ver 1.00
'''
import os
import datetime
from bs4 import BeautifulSoup
#インストールディレクトの定義
BASE_DIR = '/home/pi/BOAT_RACE_DB'

'''
【関　数】mkcsv_t_info_d
【機　能】直前HTMLファイルから直前情報明細テーブル「t_info_d」のインポートCSVファイルを作成する
【引　数】なし
【戻り値】なし
'''
def mkcsv_t_info_d():
    print('直前情報明細テーブル「t_info_d」のインポートCSVファイル　開始')
    in_path  = BASE_DIR + '/200_html/last_info'
    out_file = BASE_DIR + '/210_csv/t_info_d.csv'
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
                t_info_d_yyyymmdd = ''  #開催日付
                t_info_d_pool_code = '' #場コード
                t_info_d_race_no  = ''  #レース番号
                #HTMLファイルからcsvレコード項目を抽出
                soup = BeautifulSoup(html, 'html.parser')
                
                #開催日付の抽出
                t_info_d_yyyymmdd = item[0:8]
                #場コードの抽出
                t_info_d_pool_code = item[8:10]
                #レース番号
                t_info_d_race_no  = item[10:12]

                #場名の抽出
                for tag1 in soup.find_all('img'):
                    if '/static_extra/pc/images/text_place2' in str(tag1):
                        for tag2 in str(tag1).splitlines():
                            if '/static_extra/pc/images/text_place2' in str(tag2):
                                wk_arry = str(tag2).strip().split(' ')
                                t_race_d_pool_name = str(wk_arry[1])
                                t_race_d_pool_name = t_race_d_pool_name.replace('alt="','')
                                t_race_d_pool_name = t_race_d_pool_name.replace('"','')   
                #選手単位の明細項目の抽出
                base_count = 0
                for tag1 in soup.find_all('tbody'):
                    if 'is-fs12' in str(tag1):
                        base_count = base_count + 1
                        #CSVレコードフィールドの初期化(選手単位項目)
                        t_info_d_entry_no = ''          #枠番
                        t_info_d_body_weight = ''       #体重
                        t_info_d_adjusted_weight = ''   #調整重量
                        t_info_d_rehearsal_time = ''    #展示タイム
                        t_info_d_tilt = ''              #チルト
                        t_info_d_start_course = ''      #スタート展示コース
                        t_info_d_flying = ''            #フライング区分
                        t_info_d_start_time = ''        #スタート展示タイム率

                        #選手単位の明細項目の抽出(枠番)
                        t_info_d_entry_no = str(base_count)
                      
                        #選手単位の明細項目の抽出(体重)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n =  n + 1
                            if n == 6:
                                wk_arry = str(tag2).strip().split('>')
                                t_info_d_body_weight = str(wk_arry[1])
                                t_info_d_body_weight = t_info_d_body_weight.replace('</td','')
                                t_info_d_body_weight = t_info_d_body_weight.replace('kg','')
                                t_info_d_body_weight = t_info_d_body_weight.strip()
                                break                  

                        #選手単位の明細項目の抽出(調整重量)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n =  n + 1
                            if n == 22:
                                wk_arry = str(tag2).strip().split('>')
                                t_info_d_adjusted_weight = str(wk_arry[1]).replace('</td','')
                                break 
                    
                        #選手単位の明細項目の抽出(展示タイム)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n =  n + 1
                            if n == 7:
                                wk_arry = str(tag2).strip().split('>')
                                t_info_d_rehearsal_time = str(wk_arry[1]).replace('</td','')
                                break 
                        
                        #選手単位の明細項目の抽出(チルト)
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n =  n + 1
                            if n == 8:
                                wk_arry = str(tag2).strip().split('>')
                                t_info_d_tilt = str(wk_arry[1]).replace('</td','')
                                break 
                        
                        #選手単位の明細項目の抽出(スタート展示コース)
                        n = 0
                        for tag2 in soup.find_all('span'):
                            if 'table1_boatImage1Number' in str(tag2):
                                n = n + 1
                                wk_arry = str(tag2).strip().split('>')
                                wk_str = str(wk_arry[1]).replace('</span','')
                                if t_info_d_entry_no == wk_str:
                                    t_info_d_start_course = str(n)
                        
                        #選手単位の明細項目の抽出(フライング区分_スタート展示タイム)
                        n = 0
                        for tag2 in soup.find_all('span'):
                            if 'table1_boatImage1Time' in str(tag2):
                                n = n + 1
                                wk_arry = str(tag2).strip().split('>')
                                wk_str = str(wk_arry[1]).replace('</span','')
                                if t_info_d_start_course == str(n):
                                    if 'F' in wk_str:
                                        t_info_d_flying = 'F'
                                        t_info_d_start_time = wk_str.replace('F','')
                                    else:
                                        t_info_d_flying = ' '
                                        t_info_d_start_time = wk_str                                     

                        #CSVレコードの生成
                        t_info_d_outrec = ''
                        t_info_d_outrec = t_info_d_outrec + '"' + t_info_d_yyyymmdd + '"'   #開催日付
                        t_info_d_outrec = t_info_d_outrec + ',"' + t_info_d_pool_code + '"' #場コード
                        t_info_d_outrec = t_info_d_outrec + ',"' + t_info_d_race_no + '"'   #レース番号
                        t_info_d_outrec = t_info_d_outrec + ',"' + t_info_d_entry_no + '"'  #枠番
                        t_info_d_outrec = t_info_d_outrec + ',' + t_info_d_body_weight      #体重
                        t_info_d_outrec = t_info_d_outrec + ',' + t_info_d_adjusted_weight  #調整重量
                        t_info_d_outrec = t_info_d_outrec + ',' + t_info_d_rehearsal_time   #展示タイム
                        t_info_d_outrec = t_info_d_outrec + ',' + t_info_d_tilt             #チルト
                        t_info_d_outrec = t_info_d_outrec + ',' + t_info_d_start_course     #スタート展示コース
                        t_info_d_outrec = t_info_d_outrec + ',"' + t_info_d_flying + '"'    #フライング区分0: なし　1: フライング2: 出遅れ
                        t_info_d_outrec = t_info_d_outrec + ',' + t_info_d_start_time       #スタート展示タイム

                        #CSVレコードファイル出力
                        if t_info_d_body_weight != '':
                            fw.write(t_info_d_outrec + '\n')
    fw.close()
    print('直前情報明細「t_info_d」のインポートCSVファイル　完了')

#主処理
mkcsv_t_info_d() #直前情報明細テーブル「t_info_d」のインポートCSVファイルを作成
