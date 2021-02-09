'''
【システム】BOAT_RACE_DB2
【ファイル】200_mkcsv_x_race_t.py
【機能仕様】本日レース一覧HTMLファイルから出走表タイトルテーブル「x_race_t」のインポートCSVファイルを作成する
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.02.01 ver 1.00
'''
import os
import datetime
from bs4 import BeautifulSoup
#インストールディレクトの定義
BASE_DIR = '/home/pi/BOAT_RACE_DB'

'''
【関　数】mkcsv_t_race_t
【機　能】本日レース一覧HTMLファイルから出走表タイトルテーブル「x_race_t」のインポートCSVファイルを作成
【引　数】なし
【戻り値】なし
'''
def mkcsv_x_race_t():
    print('出走表タイトルテーブル「x_race_t」のインポートCSVファイル　開始')
    
    grade_class_arry = ['is-ippan is-rookie__3rdadd', 'is-ippan is-venus', 'is-ippan', 'is-G1a is-lady', 'is-G1b is-lady', 'is-G2a is-lady', 'is-G2b is-lady', 'is-G3a is-lady', 'is-G3b is-lady','is-SGa ', 'is-SGb', 'is-G1a', 'is-G1b', 'is-G2a', 'is-G2b', 'is-G3a', 'is-G3b']
    grade_name_arry = ['一般・若手', '一般・女子', '一般', 'Ｇ１・女子', 'Ｇ１・女子', 'Ｇ２・女子', 'Ｇ２・女子', 'Ｇ３・女子', 'Ｇ３・女子','ＳＧ', 'ＳＧ', 'Ｇ１', 'Ｇ１', 'Ｇ２', 'Ｇ２', 'Ｇ３', 'Ｇ３']
    holding_class_arry = ['is-nighter', 'is-morning', 'is-summer']
    holding_name_arry = ['ナイター', 'モーニング', 'サマータイム']
    event_date_name_arry = ['初日日','１日目','２日目','３日目','４日目','５日目','最終日']

    in_path  = BASE_DIR + '/200_html/today'
    out_file = BASE_DIR + '/210_csv/x_race_t.csv'
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
                for tag1 in soup.find_all('tbody'):
                    #CSVレコードフィールドの初期化
                    t_race_t_yyyymmdd = ''      #開催日付
                    t_race_t_pool_code  = ''    #場コード
                    t_race_t_pool_name = ''     #場名
                    t_race_t_grade = ''         #グレード
                    t_race_t_holding = ''       #開催時間帯区分
                    t_race_t_title = ''         #レースタイトル
                    t_race_t_event_date = ''    #開催日
                    t_race_t_situation =  ''    #進行状況
                    #HTMLファイルからcsvレコード項目を抽出
                    #開催日付の抽出
                    t_race_t_yyyymmdd = item.replace('.html', '')
                    #場コードの抽出
                    for tag2 in str(tag1).splitlines():
                        if 'is-arrow1 is-fBold is-fs15' in str(tag2):
                            for tag3 in str(tag2).split('<'):
                                if '/static_extra/pc/images/text_place1' in str(tag3):
                                    wk_arry = str(tag3).split(' ')
                                    t_race_t_pool_code = str(wk_arry[3])
                                    t_race_t_pool_code = t_race_t_pool_code.replace('src="/static_extra/pc/images/text_place1_', '')
                                    t_race_t_pool_code = t_race_t_pool_code.replace('.png"', '')
                    #場名の抽出
                    for tag2 in str(tag1).splitlines():
                        if 'is-arrow1 is-fBold is-fs15' in str(tag2):
                            for tag3 in str(tag2).split('<'):
                                if '/static_extra/pc/images/text_place1' in str(tag3):
                                    wk_arry = str(tag3).split(' ')
                                    t_race_t_pool_name = str(wk_arry[1])
                                    t_race_t_pool_name = t_race_t_pool_name.replace('alt="', '')
                                    t_race_t_pool_name = t_race_t_pool_name.replace('&gt;"', '')
                    #グレードの抽出
                    n = 0
                    t_race_t_grade = '不明'
                    for wk_grade_class in grade_class_arry:
                        if str(wk_grade_class) in str(tag1):
                            t_race_t_grade = grade_name_arry[n]
                        n = n + 1
                    #開催時間帯区分の抽出
                    n = 0
                    t_race_t_holding = '通常'
                    for wk_holding_class in holding_class_arry:
                        if str(wk_holding_class) in tag1:
                            t_race_t_holding = holding_name_arry[n]
                        n = n + 1
                    #レースタイトルの抽出
                    for tag2 in str(tag1).splitlines():
                        if '/owpc/pc/race/raceindex' in str(tag2):
                            wk_arry = str(tag2).split('<')
                            wk_arry = str(wk_arry[2]).split('>') 
                            t_race_t_title = wk_arry[1]
                    #開催日の抽出
                    for wk_event_date_name in event_date_name_arry:
                        if str(wk_event_date_name) in str(tag1):
                            t_race_t_event_date = wk_event_date_name
                    #進行状況の抽出
                    t_race_t_situation = "-"
                    #print(tag1)
                    if '<td class="is-p10-10 is-attentionColor1" colspan="3">' in str(tag1):
                        for tag2 in str(tag1).splitlines():
                            if '<td class="is-p10-10 is-attentionColor1" colspan="3">' in str(tag2):
                                wk_arry = str(tag2).split('>')
                                wk_arry = str(wk_arry[1]).split('<')
                                t_race_t_situation = str(wk_arry[0])
                    #CSVレコードの生成
                    t_race_t_outrec = ''
                    t_race_t_outrec = t_race_t_outrec + '"' + t_race_t_yyyymmdd + '"'    #開催日付
                    t_race_t_outrec = t_race_t_outrec + ',"' + t_race_t_pool_code + '"'  #場コード
                    t_race_t_outrec = t_race_t_outrec + ',"' + t_race_t_pool_name + '"'  #場名
                    t_race_t_outrec = t_race_t_outrec + ',"' + t_race_t_grade + '"'      #グレード
                    t_race_t_outrec = t_race_t_outrec + ',"' + t_race_t_holding + '"'    #開催時間帯区分
                    t_race_t_outrec = t_race_t_outrec + ',"' + t_race_t_title + '"'      #レースタイトル
                    t_race_t_outrec = t_race_t_outrec + ',"' + t_race_t_event_date + '"' #開催日
                    t_race_t_outrec = t_race_t_outrec + ',"' + t_race_t_situation + '"'  #進行状況
                    #CSVレコードファイル出力
                    fw.write(t_race_t_outrec + '\n')
    fw.close()
    print('出走表タイトルテーブル「x_race_t」のインポートCSVファイル　完了')

#主処理
mkcsv_x_race_t() #出走表タイトルテーブル「t_race_t」のインポートCSVファイルを作成
