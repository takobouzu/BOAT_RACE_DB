'''
【システム】BOAT_RACE_DB2
【ファイル】000_mkcsv_tenken.py
【機能仕様】前検HTMLファイルから前検テーブル「t_tenken」のインポートCSVファイルを作成する
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.02.01 ver 1.00
'''
import os
import datetime
from bs4 import BeautifulSoup
#インストールディレクトの定義
BASE_DIR = '/home/pi/BOAT_RACE_DB'

'''
【関　数】mkcsv_t_tenken
【機　能】前検HTMLファイルからレースタイトル「t_tenken」のインポートCSVファイルを作成
【引　数】なし
【戻り値】なし
'''
def mkcsv_t_tenken():
    print('前検テーブル「t_tenken」のインポートCSVファイル　開始')
    

    in_path  = BASE_DIR + '/200_html/tenken'
    out_file = BASE_DIR + '/210_csv/t_tenken.csv'
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
                soup = BeautifulSoup(html, 'html.parser')
                t_tenken_yyyy = item[3:7]                  #開催年
                t_tenken_yyyymmdd = item[3:11]             #開催年月日
                t_tenken_pool_code = item[0:2]             #場コード

                t_tenken_title = '' #レースタイトル
                for tag1 in soup.find_all('h2', class_='heading2_titleName'):
                    wk_arry = str(tag1).split('>')
                    wk_arry = str(wk_arry[1]).split('<')
                    t_tenken_title = str(wk_arry[0])

                for tag1 in soup.find_all('tbody'):
                    if '/owpc/pc/data/racersearch/profile?toban=' in str(tag1):
                        t_tenken_motor_no = ''              #モーター番号
                        t_tenken_rank = ''                  #前検タイムランク
                        t_tenken_player_no = ''             #登録番号
                        t_tenken_plyaer_name = ''           #選手名
                        t_tenken_class = ''                 #級別
                        t_tenken_motor_double_rate = ''     #モーター二連率
                        t_tenken_boat_no = ''               #ボート番号
                        t_tenken_boat_double_rate = ''      #ボート二連率
                        t_tenken_time  = ''                 #タイム
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if n == 14:
                                wk_arry = str(tag2).split('>')
                                wk_arry = str(wk_arry[1]).split('<')
                                t_tenken_motor_no = str(wk_arry[0])              #モーター番号
                            if n == 3:
                                wk_arry = str(tag2).split('>')
                                wk_arry = str(wk_arry[1]).split('<')
                                t_tenken_rank =str(wk_arry[0])                   #前検タイムランク
                            if n == 5:
                                wk_arry = str(tag2).split('>')
                                wk_arry = str(wk_arry[1]).split('<')
                                t_tenken_player_no = str(wk_arry[0])             #登録番号
                            if n == 11:
                                wk_arry = str(tag2).split('>')
                                wk_arry = str(wk_arry[1]).split('<')
                                t_tenken_plyaer_name = str(wk_arry[0])             #選手名
                                t_tenken_plyaer_name = t_tenken_plyaer_name.replace('　','')
                            if n == 13:
                                wk_arry = str(tag2).split('>')
                                wk_arry = str(wk_arry[1]).split('<')
                                t_tenken_class = str(wk_arry[0])                    #級別
                            if n == 15:
                                wk_arry = str(tag2).split('>')
                                wk_arry = str(wk_arry[1]).split('<')
                                t_tenken_motor_double_rate = str(wk_arry[0])        #モーター二連率
                                t_tenken_motor_double_rate = t_tenken_motor_double_rate.replace('%','')
                            if n == 16:
                                wk_arry = str(tag2).split('>')
                                wk_arry = str(wk_arry[1]).split('<')
                                t_tenken_boat_no = str(wk_arry[0])                  #ボート番号
                            if n == 17:
                                wk_arry = str(tag2).split('>')
                                wk_arry = str(wk_arry[1]).split('<')
                                t_tenken_boat_double_rate = str(wk_arry[0])         #ボート二連率
                                t_tenken_boat_double_rate = t_tenken_boat_double_rate.replace('%','')
                            if n == 18:
                                wk_arry = str(tag2).split('>')
                                wk_arry = str(wk_arry[1]).split('<')
                                t_tenken_time  = str(wk_arry[0])                   #タイム
                        #CSVレコードの生成
                        outrec = ''                
                        outrec = outrec + '"' + t_tenken_yyyy + '"'                 #開催年
                        outrec = outrec + ',"' + t_tenken_yyyymmdd + '"'            #開催年月日
                        outrec = outrec + ',"' + t_tenken_pool_code + '"'           #場コード
                        outrec = outrec + ',"' + t_tenken_title + '"'               #レースタイトル
                        outrec = outrec + ',"' + t_tenken_motor_no + '"'            #モーター番号
                        outrec = outrec + ',' + t_tenken_rank                       #前検タイムランク
                        outrec = outrec + ',"' + t_tenken_player_no + '"'           #登録番号
                        outrec = outrec + ',"' + t_tenken_plyaer_name + '"'         #選手名
                        outrec = outrec + ',"' + t_tenken_class + '"'               #級別
                        outrec = outrec + ',' + t_tenken_motor_double_rate          #モーター二連率
                        outrec = outrec + ',"' + t_tenken_boat_no + '"'             #ボート番号
                        outrec = outrec + ',' + t_tenken_boat_double_rate           #ボート二連率
                        outrec = outrec + ',' + t_tenken_time                       #タイム
                        #CSVレコードファイル出力
                        fw.write(outrec + '\n')
    fw.close()
    print('前検テーブル「t_tenken」のインポートCSVファイル　完了')

#主処理
mkcsv_t_tenken() #前検テーブル「t_tenken」のインポートCSVファイルを作成
