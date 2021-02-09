'''
【システム】BOAT_RACE_DB2
【ファイル】110_mkcsv_t_race_h.py
【機能仕様】出走表HTMLファイルからレース情報タイトルテーブル「t_race_h」のインポートCSVファイルを作成する
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.02.01 ver 1.00
'''
import os
import datetime
from bs4 import BeautifulSoup
#インストールディレクトの定義
BASE_DIR = '/home/pi/BOAT_RACE_DB'

'''
【関　数】mkcsv_t_race_h
【機　能】出走表HTMLファイルから出走表ヘッダテーブル「t_race_h」のインポートCSVファイルを作成する
【引　数】なし
【戻り値】なし
'''
def mkcsv_t_race_h():
    print('出走表ヘッダテーブル「t_race_h」のインポートCSVファイル　開始')
    
    grade_class_arry = ['is-ippan is-rookie__3rdadd', 'is-ippan is-venus', 'is-ippan', 'is-G1a is-lady', 'is-G1b is-lady', 'is-G2a is-lady', 'is-G2b is-lady', 'is-G3a is-lady', 'is-G3b is-lady','is-SGa ', 'is-SGb', 'is-G1a', 'is-G1b', 'is-G2a', 'is-G2b', 'is-G3a', 'is-G3b']
    grade_name_arry = ['一般・若手', '一般・女子', '一般', 'Ｇ１・女子', 'Ｇ１・女子', 'Ｇ２・女子', 'Ｇ２・女子', 'Ｇ３・女子', 'Ｇ３・女子','ＳＧ', 'ＳＧ', 'Ｇ１', 'Ｇ１', 'Ｇ２', 'Ｇ２', 'Ｇ３', 'Ｇ３']
    holding_class_arry = ['is-nighter', 'is-morning', 'is-summer']
    holding_name_arry = ['ナイター', 'モーニング', 'サマータイム']
    event_date_name_arry = ['初日日','１日目','２日目','３日目','４日目','５日目','最終日']

    in_path  = BASE_DIR + '/200_html/race_table'
    out_file = BASE_DIR + '/210_csv/t_race_h.csv'
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
                #CSVレコードフィールドの初期化
                t_race_h_yyyymmdd = ''              #開催日付
                t_race_h_pool_code = ''             #場コード
                t_race_h_race_no = ''               #レース番号
                t_race_h_pool_name = ''             #場名
                t_race_h_scheduled_deadline = ''    #レース締切予定時間
                t_race_h_race_name = ''             #レース名
                t_race_h_distance = ''              #距離
                t_race_h_stabilizer = ''            #安定板使用区分
                t_race_h_approach = ''              #進入固定区分
                #HTMLファイルからcsvレコード項目を抽出
                soup = BeautifulSoup(html, 'html.parser')
                #開催日付の抽出
                t_race_h_yyyymmdd = item[0:8]
                #場コードの抽出
                t_race_h_pool_code = item[8:10]
                #レース番号
                t_race_h_race_no  = item[10:12]
                #場名
                for tag1 in soup.find_all('img'):
                    if '/static_extra/pc/images/text_place2' in str(tag1):
                        for tag2 in str(tag1).splitlines():
                            if '/static_extra/pc/images/text_place2' in str(tag2):
                                wk_arry = str(tag2).split(' ')
                                t_race_h_pool_name = str(wk_arry[1])
                                t_race_h_pool_name = t_race_h_pool_name.replace('alt="','')
                                t_race_h_pool_name = t_race_h_pool_name.replace('"','')         
                #レース締切予定時間
                n = 0
                for tag1 in soup.find_all('td'):
                    if ':' in str(tag1):
                        for tag2 in str(tag1).splitlines():
                            if '<td class="">' in str(tag2):
                                n = n + 1
                                if n == int(t_race_h_race_no):
                                    t_race_h_scheduled_deadline = str(tag2)
                                    t_race_h_scheduled_deadline = t_race_h_scheduled_deadline.replace('<td class="">', '')
                                    t_race_h_scheduled_deadline = t_race_h_scheduled_deadline.replace('</td>', '')
                #レース名
                for tag1 in soup.find_all('span'):
                    if 'heading2_titleDetail is-type1' in str(tag1):
                        for tag2 in str(tag1).splitlines():
                            if 'heading2_titleDetail is-type1' in str(tag2):
                                t_race_h_race_name = str(tag2).strip()
                                t_race_h_race_name = t_race_h_race_name.replace('<span class="heading2_titleDetail is-type1">','')
                #距離
                for tag1 in soup.find_all('span'):
                    if 'm' in str(tag1):
                        for tag2 in str(tag1).splitlines():
                            if 'm' in str(tag2):
                                t_race_h_distance = str(tag2)
                                t_race_h_distance = t_race_h_distance.strip()
                                t_race_h_distance = t_race_h_distance.replace('<span>','')
                                t_race_h_distance = t_race_h_distance.replace('</span>','')
                                t_race_h_distance = t_race_h_distance.replace('m','')        
                #安定板使用区分
                for tag1 in soup.find_all('span'):
                    if '安定板使用' in str(tag1):
                        t_race_h_stabilizer = '安定板使用'
                #進入固定区分
                for tag1 in soup.find_all('span'):
                    if '進入固定' in str(tag1):
                        t_race_h_approach = '進入固定'
                #CSVレコードの生成
                t_race_h_outrec = ''
                t_race_h_outrec = t_race_h_outrec + '"' + t_race_h_yyyymmdd + '"'               #開催日付
                t_race_h_outrec = t_race_h_outrec + ',"' + t_race_h_pool_code + '"'             #場コード
                t_race_h_outrec = t_race_h_outrec + ',"' + t_race_h_race_no + '"'               #レース番号
                t_race_h_outrec = t_race_h_outrec + ',"' + t_race_h_pool_name + '"'             #場名
                t_race_h_outrec = t_race_h_outrec + ',"' + t_race_h_scheduled_deadline + '"'    #レース締切予定時間
                t_race_h_outrec = t_race_h_outrec + ',"' + t_race_h_race_name + '"'             #レース名
                t_race_h_outrec = t_race_h_outrec + ',"' + t_race_h_distance + '"'              #距離
                t_race_h_outrec = t_race_h_outrec + ',"' + t_race_h_stabilizer + '"'            #安定板使用区分
                t_race_h_outrec = t_race_h_outrec + ',"' + t_race_h_approach + '"'              #進入固定区分
                #CSVレコードファイル出力
                fw.write(t_race_h_outrec + '\n')
    fw.close()
    print('出走表ヘッダテーブル「t_race_h」のインポートCSVファイル　完了')

#主処理
mkcsv_t_race_h() #レース情報タイトルテーブル「t_race_h」のインポートCSVファイルを作成
