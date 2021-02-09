'''
【システム】BOAT_RACE_DB2
【ファイル】160_mkcsv_t_info_p.py
【機能仕様】直前情報HTMLファイルから直前情報部品交換テーブル「t_info_p」のインポートCSVファイルを作成する
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.02.01 ver 1.00
'''
import os
import datetime
from bs4 import BeautifulSoup
#インストールディレクトの定義
BASE_DIR = '/home/pi/BOAT_RACE_DB'

'''
【関　数】mkcsv_t_info_p
【機　能】直前HTMLファイルから直前情報部品交換テーブル「t_info_p」のインポートCSVファイルを作成する
【引　数】なし
【戻り値】なし
'''
def mkcsv_t_info_p():
    print('直前情報部品テーブル「t_info_p」のインポートCSVファイル　開始')
    in_path  = BASE_DIR + '/200_html/last_info'
    out_file = BASE_DIR + '/210_csv/t_info_p.csv'
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
                t_info_p_yyyymmdd = ''      #開催日付
                t_info_p_pool_code = ''     #場コード
                t_info_p_race_no = ''       #レース番号
                #HTMLファイルからcsvレコード項目を抽出
                soup = BeautifulSoup(html, 'html.parser')
                
                #開催日付の抽出
                t_info_p_yyyymmdd = item[0:8]
                #場コードの抽出
                t_info_p_pool_code = item[8:10]
                #レース番号
                t_info_p_race_no  = item[10:12]
  
                #選手単位の明細項目の抽出
                base_count = 0
                for tag1 in soup.find_all('tbody'):
                    if 'is-fs12' in str(tag1):
                        base_count = base_count + 1
                        #CSVレコードフィールドの初期化(選手単位項目)
                        t_info_p_entry_no = ''        #枠番
                        t_info_p_motor_no = ''        #モーター番号
                        t_info_p_parts   = ''         #部品交換区分

                        #選手単位の明細項目の抽出(枠番)
                        t_info_p_entry_no = str(base_count)
                        #選手単位の明細項目の抽出(交換部品)
                        parts_flg = 0
                        parts_list = []
                        n = 0
                        for tag2 in str(tag1).splitlines():
                            n = n + 1
                            if  n == 9 and ('新' in str(tag2)): 
                                parts_flg = 1 
                                parts_list.append('ペラ')
                            if 'label4 is-type1' in str(tag2):
                                parts_flg = 1
                                wk_arry = str(tag2).split('>')
                                wk_arry = str(wk_arry[2]).split('<')
                                wk = str(wk_arry[0]).strip()
                                parts_list.append(wk)
                        #部品交換有りの場合はCSVレコードを生成・出力する
                        if parts_flg == 1:
                            #選手単位の明細項目の抽出(モーター番号)
                            in_file2 = BASE_DIR + '/200_html/race_table/' + item
                            fb2 = open(in_file2, 'r')
                            html2 = fb2.read()
                            fb2.close()
                            n = 0
                            soup2 = BeautifulSoup(html2, 'html.parser')
                            for tag11 in soup2.find_all('tbody',class_='is-fs12'):
                                n = n + 1
                                if int(t_info_p_entry_no) == n:
                                    wk_arry = str(tag11).splitlines()
                                    t_info_p_motor_no = str(wk_arry[35]).strip()
                                    for wk_parts in parts_list:
                                        #CSVレコードの生成
                                        t_info_p_outrec = ''
                                        t_info_p_outrec = t_info_p_outrec + '"' + t_info_p_yyyymmdd  + '"'       #開催日付
                                        t_info_p_outrec = t_info_p_outrec + ',"' + t_info_p_pool_code + '"'      #場コード
                                        t_info_p_outrec = t_info_p_outrec + ',"' + t_info_p_race_no   + '"'      #レース番号
                                        t_info_p_outrec = t_info_p_outrec + ',"' + t_info_p_entry_no + '"'       #枠番
                                        t_info_p_outrec = t_info_p_outrec + ',"' + t_info_p_motor_no + '"'      #モーター番号
                                        t_info_p_outrec = t_info_p_outrec + ',"' + wk_parts   + '"'              #部品交換区分
                                        #CSVレコードファイル出力
                                        fw.write(t_info_p_outrec + '\n')
    fw.close()
    print('直前情報部品交換「t_info_p」のインポートCSVファイル　完了')

#主処理
mkcsv_t_info_p() #直前情報部品交換テーブル「t_info_p」のインポートCSVファイルを作成
