'''
【システム】BOAT_RACE_DB2
【ファイル】200_mkcsv_t_odds.py
【機能仕様】オッズファイルからオッズテーブル「t_odds」のインポートCSVファイルを作成する
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.02.01 ver 1.00
'''
import os
import datetime
from bs4 import BeautifulSoup
#インストールディレクトの定義
BASE_DIR = '/home/pi/BOAT_RACE_DB'

'''
【関　数】mkcsv_t_odds
【機　能】オッズHTMLファイルからオッズテーブル「t_odds」のインポートCSVファイルを作成する
【引　数】なし
【戻り値】なし
'''
def mkcsv_t_odds():
    print('オッズテーブル「t_odds」のインポートCSVファイル　開始')
    focus_list = []

    focus_list.append('1-2-3'); focus_list.append('2-1-3'); focus_list.append('3-1-2'); focus_list.append('4-1-2'); focus_list.append('5-1-2'); focus_list.append('6-1-2')
    focus_list.append('1-2-4'); focus_list.append('2-1-4'); focus_list.append('3-1-4'); focus_list.append('4-1-3'); focus_list.append('5-1-3'); focus_list.append('6-1-3')
    focus_list.append('1-2-5'); focus_list.append('2-1-5'); focus_list.append('3-1-5'); focus_list.append('4-1-5'); focus_list.append('5-1-4'); focus_list.append('6-1-4')
    focus_list.append('1-2-6'); focus_list.append('2-1-6'); focus_list.append('3-1-6'); focus_list.append('4-1-6'); focus_list.append('5-1-6'); focus_list.append('6-1-5')

    focus_list.append('1-3-2'); focus_list.append('2-3-1'); focus_list.append('3-2-1'); focus_list.append('4-2-1'); focus_list.append('5-2-1'); focus_list.append('6-2-1')
    focus_list.append('1-3-4'); focus_list.append('2-3-4'); focus_list.append('3-2-4'); focus_list.append('4-2-3'); focus_list.append('5-2-3'); focus_list.append('6-2-3')
    focus_list.append('1-3-5'); focus_list.append('2-3-5'); focus_list.append('3-2-5'); focus_list.append('4-2-5'); focus_list.append('5-2-4'); focus_list.append('6-2-4')
    focus_list.append('1-3-6'); focus_list.append('2-3-6'); focus_list.append('3-2-6'); focus_list.append('4-2-6'); focus_list.append('5-2-6'); focus_list.append('6-2-5')

    focus_list.append('1-4-2'); focus_list.append('2-4-1'); focus_list.append('3-4-1'); focus_list.append('4-3-1'); focus_list.append('5-3-1'); focus_list.append('6-3-1')
    focus_list.append('1-4-3'); focus_list.append('2-4-3'); focus_list.append('3-4-2'); focus_list.append('4-3-2'); focus_list.append('5-3-2'); focus_list.append('6-3-2')
    focus_list.append('1-4-5'); focus_list.append('2-4-5'); focus_list.append('3-4-5'); focus_list.append('4-3-5'); focus_list.append('5-3-4'); focus_list.append('6-3-4')
    focus_list.append('1-4-6'); focus_list.append('2-4-6'); focus_list.append('3-4-6'); focus_list.append('4-3-6'); focus_list.append('5-3-6'); focus_list.append('6-3-5')

    focus_list.append('1-5-2'); focus_list.append('2-5-1'); focus_list.append('3-5-1'); focus_list.append('4-5-1'); focus_list.append('5-4-1'); focus_list.append('6-4-1')
    focus_list.append('1-5-3'); focus_list.append('2-5-3'); focus_list.append('3-5-2'); focus_list.append('4-5-2'); focus_list.append('5-4-2'); focus_list.append('6-4-2')
    focus_list.append('1-5-4'); focus_list.append('2-5-4'); focus_list.append('3-5-4'); focus_list.append('4-5-3'); focus_list.append('5-4-3'); focus_list.append('6-4-3')
    focus_list.append('1-5-6'); focus_list.append('2-5-6'); focus_list.append('3-5-6'); focus_list.append('4-5-6'); focus_list.append('5-4-6'); focus_list.append('6-4-5')

    focus_list.append('1-6-2'); focus_list.append('2-6-1'); focus_list.append('3-6-1'); focus_list.append('4-6-1'); focus_list.append('5-6-1'); focus_list.append('6-5-1')
    focus_list.append('1-6-3'); focus_list.append('2-6-3'); focus_list.append('3-6-2'); focus_list.append('4-6-2'); focus_list.append('5-6-2'); focus_list.append('6-5-2')
    focus_list.append('1-6-4'); focus_list.append('2-6-4'); focus_list.append('3-6-4'); focus_list.append('4-6-3'); focus_list.append('5-6-3'); focus_list.append('6-5-3')
    focus_list.append('1-6-5'); focus_list.append('2-6-5'); focus_list.append('3-6-5'); focus_list.append('4-6-5'); focus_list.append('5-6-4'); focus_list.append('6-5-4')


    in_path  = BASE_DIR + '/200_html/odds_3t'
    out_file = BASE_DIR + '/210_csv/t_odds.csv'
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
            if '※ 該当レースは中止になりました。' in html:
                flg = 1
            if flg == 0:
                #CSVレコードフィールドの初期化(共通項目)
                t_odds_yyyymmdd = ''      #開催日付
                t_odds_pool_code = ''     #場コード
                t_odds_race_no = ''       #レース番号
                t_odds_ticket_type = ''   #券種

                #HTMLファイルからcsvレコード項目を抽出
                soup = BeautifulSoup(html, 'html.parser')
                
                #開催日付の抽出
                t_odds_yyyymmdd = item[0:8]
                #場コードの抽出
                t_odds_pool_code = item[8:10]
                #レース番号
                t_odds_race_no  = item[10:12]

                #券種
                t_odds_ticket_type = '三連単'

                #オッズの取得
                base_count = 0
                for tag1 in soup.find_all('td', class_='oddsPoint'):
                    #オッズの抽出
                    wk_arry = str(tag1).split('>')
                    wk_arry = str(wk_arry[1]).split('<')
                    t_odds_odds = str(wk_arry[0]).strip()
                    #組番の抽出
                    t_odds_focus  = focus_list[base_count]

                    #CSVレコードの生成
                    t_odds_outrec = ''
                    t_odds_outrec = t_odds_outrec + '"' +  t_odds_yyyymmdd + '"'      #開催日付
                    t_odds_outrec = t_odds_outrec + ',"' + t_odds_pool_code + '"'     #場コード
                    t_odds_outrec = t_odds_outrec + ',"' + t_odds_race_no + '"'       #レース番号
                    t_odds_outrec = t_odds_outrec + ',"' + t_odds_ticket_type + '"'   #券種
                    t_odds_outrec = t_odds_outrec + ',"' + t_odds_focus + '"'         #組番
                    t_odds_outrec = t_odds_outrec + ',' +  t_odds_odds                #オッズ

                    #CSVレコードファイル出力
                    if t_odds_odds != '欠場':
                        fw.write(t_odds_outrec + '\n')
                    
                    #カウンターをインクリメント
                    base_count = base_count + 1
    fw.close()
    print('オッズテーブル「t_odds」のインポートCSVファイル　完了')

#主処理
mkcsv_t_odds() #オッズテーブル「t_odds」のインポートCSVファイルを作成
