'''
【システム】BOAT_RACE_DB2
【ファイル】180_mkcsv_t_result_d.py
【機能仕様】レース結果HTMLファイルからレース結果明細テーブル「t_result_d」のインポートCSVファイルを作成する
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.02.01 ver 1.00
'''
import os
import datetime
from bs4 import BeautifulSoup
#インストールディレクトの定義
BASE_DIR = '/home/pi/BOAT_RACE_DB'

'''
【関　数】mkcsv_t_result_d
【機　能】直前HTMLファイルからレース結果明細テーブル「t_result_d」のインポートCSVファイルを作成する
【引　数】なし
【戻り値】なし
'''
def mkcsv_t_result_d():
    print('レース結果明細テーブル「t_result_d」のインポートCSVファイル　開始')
    in_path  = BASE_DIR + '/200_html/result'
    out_file = BASE_DIR + '/210_csv/t_result_d.csv'
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
            if 'レース中止' in html:
                flg = 1
            if flg == 0:
                #CSVレコードフィールドの初期化(共通項目)
                t_result_d_yyyymmdd = ''  #開催日付
                t_result_d_pool_code = '' #場コード
                t_result_d_race_no  = ''  #レース番号

                #HTMLファイルからcsvレコード項目を抽出
                soup = BeautifulSoup(html, 'html.parser')
                
                #開催日付の抽出
                t_result_d_yyyymmdd = item[0:8]
                #場コードの抽出
                t_result_d_pool_code = item[8:10]
                #レース番号
                t_result_d_race_no  = item[10:12]

                #選手単位の明細項目の抽出
                base_count = 0
                for tag1 in soup.find_all('tbody'):
                    if '<span class="is-fs18 is-fBold is-lh24__3rdadd"' in str(tag1):
                        base_count = base_count + 1
                        #CSVレコードフィールドの初期化(選手単位項目)
                        t_result_d_entry_no = ''        #枠順
                        t_result_d_ranking  = ''        #順位
                        t_result_d_race_time  = ''      #レースタイム
                        t_result_d_course = ''          #コース
                        t_result_d_flying = ''          #フライング・出遅れ
                        t_result_d_start_time = ''      #スタートタイム
                        t_result_d_decisive_facto = ''  #決まり手

                        #枠順
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 4:
                                wk_arry = str(tag2).split('>')
                                t_result_d_entry_no = str(wk_arry[1]).replace('</td', '')
                                break
                        #順位
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 3:
                                wk_arry = str(tag2).split('>')
                                t_result_d_ranking = str(wk_arry[1]).replace('</td', '')
                                break
                        #レースタイム
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 9:
                                wk_arry = str(tag2).split('>')
                                t_result_d_race_time = str(wk_arry[1]).replace('</td', '')
                                t_result_d_race_time = t_result_d_race_time.strip()
                                t_result_d_race_time = t_result_d_race_time.replace("'",':')
                                t_result_d_race_time = t_result_d_race_time.replace('"',':')
                                break
                        #コース
                        n = 0
                        for tag2 in soup.find_all('span'):
                            if 'table1_boatImage1Number' in str(tag2):
                                n = n + 1
                                wk_arry = str(tag2).strip().split('>')
                                wk_str = str(wk_arry[1]).replace('</span','')
                                if t_result_d_entry_no == wk_str:
                                    t_result_d_course = str(n)
                                    break    
                        #フライング区分_スタート展示タイム
                        n = 0
                        for tag2 in soup.find_all('span', class_='table1_boatImage1TimeInner'):
                            n = n + 1
                            if t_result_d_course == str(n):
                                wk_arry = str(tag2).splitlines()
                                t_result_d_start_time = str(wk_arry[0]).strip()
                                t_result_d_decisive_facto = str(wk_arry[1]).strip()
                                t_result_d_start_time = t_result_d_start_time.replace('<span class="table1_boatImage1TimeInner">','')
                                if 'F' in t_result_d_start_time:
                                    t_result_d_flying = 'F'
                                    t_result_d_start_time = t_result_d_start_time.replace('F', '')
                                else:
                                    if 'L' in t_result_d_start_time:
                                        t_result_d_flying = 'L'
                                        t_result_d_start_time = t_result_d_start_time.replace('L', '')
                                    else:
                                        t_result_d_flying = ' '
                        #CSVレコードの生成
                        t_result_d_outrec = ''
                        t_result_d_outrec = t_result_d_outrec + '"' + t_result_d_yyyymmdd + '"'         #開催日付
                        t_result_d_outrec = t_result_d_outrec + ',"' + t_result_d_pool_code + '"'       #場コード
                        t_result_d_outrec = t_result_d_outrec + ',"' + t_result_d_race_no + '"'         #レース番号
                        t_result_d_outrec = t_result_d_outrec + ',"' + t_result_d_entry_no + '"'        #枠順
                        t_result_d_outrec = t_result_d_outrec + ',"' + t_result_d_ranking + '"'         #順位
                        t_result_d_outrec = t_result_d_outrec + ',"' + t_result_d_race_time + '"'       #レースタイム
                        t_result_d_outrec = t_result_d_outrec + ',' + t_result_d_course                 #コース
                        t_result_d_outrec = t_result_d_outrec + ',"' + t_result_d_flying + '"'          #フライング・出遅れ
                        t_result_d_outrec = t_result_d_outrec + ',' + t_result_d_start_time             #スタートタイム
                        t_result_d_outrec = t_result_d_outrec + ',"' + t_result_d_decisive_facto + '"'  #決まり手

                        #CSVレコードファイル出力
                        fw.write(t_result_d_outrec + '\n')
    fw.close()
    print('レース結果明細「t_result_d」のインポートCSVファイル　完了')

#主処理
mkcsv_t_result_d() #レース結果明細テーブル「t_result_d」のインポートCSVファイルを作成
