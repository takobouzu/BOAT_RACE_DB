'''
【システム】BOAT_RACE_DB2
【ファイル】180_mkcsv_t_result_odds.py
【機能仕様】レース結果HTMLファイルからレース結果オッズテーブル「t_result_odds」のインポートCSVファイルを作成する
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.02.01 ver 1.00
'''
import re
import os
import datetime
from bs4 import BeautifulSoup
#インストールディレクトの定義
BASE_DIR = '/home/pi/BOAT_RACE_DB'

'''
【関　数】mkcsv_t_result_odds
【機　能】レース結果HTMLファイルからレース結果オッズテーブル「t_result_odds」のインポートCSVファイルを作成する
【引　数】なし
【戻り値】なし
'''
def mkcsv_t_result_odds():
    print('レース結果オッズテーブル「t_result_odds」のインポートCSVファイル　開始')
    in_path  = BASE_DIR + '/200_html/result'
    out_file = BASE_DIR + '/210_csv/t_result_odds.csv'
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
                t_result_oods_yyyymmdd = ''     #開催日付
                t_result_oods_pool_code = ''    #場コード
                t_result_oods_race_no = ''      #レース番号

                #HTMLファイルからcsvレコード項目を抽出
                soup = BeautifulSoup(html, 'html.parser')
                
                #開催日付の抽出
                t_result_oods_yyyymmdd = item[0:8]
                #場コードの抽出
                t_result_oods_pool_code = item[8:10]
                #レース番号
                t_result_oods_race_no  = item[10:12]

                tag1 = soup.find_all('div', class_='grid_unit')
                soup = BeautifulSoup(str(tag1[2]), 'html.parser')
                n = 0
                for tag1 in soup.find_all('tr', class_='is-p3-0'):
                    n = n + 1
                    focus_list = []
                    t_result_oods_ticket_type = ''    #区分
                    t_result_oods_focus = ''          #組番
                    t_result_oods_dividend = ''       #払戻金
                    t_result_oods_popularity = ''     #人気
                    nn = 0
                    for tag2 in str(tag1).splitlines():
                        nn = nn + 1
                        if 'numberSet1_number' in str(tag2):
                            #組番を抽出
                            wk = str(tag2)
                            wk = wk.strip()
                            wk = wk.replace('-->','')
                            wk = wk.replace('<!--','')
                            wk_arry = wk.split('>')
                            wk_arry = str(wk_arry[1]).split('<')
                            focus_list.append(str(wk_arry[0]))
                        if 'is-payout1' in str(tag2):
                            #払い戻しを抽出
                            wk = str(tag2)
                            wk = wk.strip()
                            wk = wk.replace('¥','')
                            wk = wk.replace(',','')
                            wk_arry = wk.split('>')
                            wk_arry = str(wk_arry[2]).split('<')
                            t_result_oods_dividend  = str(wk_arry[0])
                        #人気を抽出
                        m = re.match(r"<td>([1-9][0-9][0-9]|[1-9][0-9]|[1-9])</td>", str(tag2))
                        if m: 
                            wk = str(tag2)
                            wk = wk.strip()
                            wk_arry = wk.split('>')
                            wk_arry = str(wk_arry[1]).split('<')
                            t_result_oods_popularity  = str(wk_arry[0])
                    #組番が存在する場合、CSVレコードを生成、ファイル出力
                    if len(focus_list) > 0:
                        if n == 1 or n == 2:
                            t_result_oods_ticket_type = '三連単'
                            t_result_oods_focus = focus_list[0] + "-" + focus_list[1] + "-" + focus_list[2]
                        if n == 3 or n == 4:
                            t_result_oods_ticket_type = '三連複'
                            t_result_oods_focus = focus_list[0] + "=" + focus_list[1] + "=" + focus_list[2]
                        if n == 5 or n == 6:
                            t_result_oods_ticket_type = '二連単'
                            t_result_oods_focus = focus_list[0] + "-" + focus_list[1]
                        if n == 7 or n == 8:
                            t_result_oods_ticket_type = '二連複'
                            t_result_oods_focus = focus_list[0] + "=" + focus_list[1]
                        if n == 9 or n == 10 or n == 11 or n == 12 or n == 13:
                            t_result_oods_ticket_type = '拡連複'
                            t_result_oods_focus = focus_list[0] + "=" + focus_list[1]
                        if n == 14 or n == 15:
                            t_result_oods_ticket_type = '単勝'
                            t_result_oods_focus = focus_list[0]
                        if n == 16 or n == 17 or n == 18:
                            t_result_oods_ticket_type = '複勝'
                            t_result_oods_focus = focus_list[0]                                   
                        #CSVレコードの生成                
                        t_result_oods_outrec = ''
                        t_result_oods_outrec = t_result_oods_outrec + '"' + t_result_oods_yyyymmdd + '"'        #開催日付
                        t_result_oods_outrec = t_result_oods_outrec + ',"' + t_result_oods_pool_code + '"'      #場コード
                        t_result_oods_outrec = t_result_oods_outrec + ',"' + t_result_oods_race_no + '"'        #レース番号
                        t_result_oods_outrec = t_result_oods_outrec + ',"' + t_result_oods_ticket_type + '"'    #区分
                        t_result_oods_outrec = t_result_oods_outrec + ',"' + t_result_oods_focus + '"'          #組番
                        t_result_oods_outrec = t_result_oods_outrec + ',' + t_result_oods_dividend              #払戻金
                        t_result_oods_outrec = t_result_oods_outrec + ',' + t_result_oods_popularity            #人気
                        #CSVレコードファイル出力
                        fw.write(t_result_oods_outrec + '\n')

    fw.close()
    print('レース結果オッズ「t_result_odds」のインポートCSVファイル　完了')

#主処理
mkcsv_t_result_odds() #レース結果オッズテーブル「t_result_odds」のインポートCSVファイルを作成
