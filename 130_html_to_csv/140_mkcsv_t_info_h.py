'''
【システム】BOAT_RACE_DB2
【ファイル】140_mkcsv_t_info_h.py
【機能仕様】直前情報HTMLファイルからレース情報タイトルテーブル「t_info_h」のインポートCSVファイルを作成する
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.02.01 ver 1.00
'''
import os
import datetime
from bs4 import BeautifulSoup
#インストールディレクトの定義
BASE_DIR = '/home/pi/BOAT_RACE_DB'

'''
【関　数】mkcsv_t_info_h
【機　能】直前HTMLファイルから直前情報ヘッダテーブル「t_info_h」のインポートCSVファイルを作成する
【引　数】なし
【戻り値】なし
'''
def mkcsv_t_info_h():
    print('直前情報ヘッダテーブル「t_info_h」のインポートCSVファイル　開始')
    in_path  = BASE_DIR + '/200_html/last_info'
    out_file = BASE_DIR + '/210_csv/t_info_h.csv'
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
                t_info_h_yyyymmdd           = ''    #開催日付
                t_info_h_pool_code          = ''    #場コード
                t_info_h_race_no            = ''    #レース番号
                t_info_h_temperature        = ''    #気温
                t_info_h_weather            = ''    #天候区分
                t_info_h_wind_speed         = ''    #風速
                t_info_h_water_temperature  = ''    #水温
                t_info_h_wave_height        = ''    #波高
                t_info_h_wind               = ''    #風向区分
                #HTMLファイルからcsvレコード項目を抽出
                soup = BeautifulSoup(html, 'html.parser')

                #開催日付の抽出
                t_info_h_yyyymmdd = item[0:8]
                #場コードの抽出
                t_info_h_pool_code = item[8:10]
                #レース番号
                t_info_h_race_no  = item[10:12]

                #気温の抽出
                n = 0
                for tag1 in soup.find_all('span'):
                    if 'weather1_bodyUnitLabelData' in str(tag1):
                        n = n + 1
                        if n == 1:
                            wk_arry = str(tag1).split('>')
                            t_info_h_temperature = str(wk_arry[1])
                            t_info_h_temperature = t_info_h_temperature.replace('</span','')
                            t_info_h_temperature = t_info_h_temperature.replace('℃','')
            
                #天候区分の抽出
                n = 0
                for tag1 in soup.find_all('span'):        
                    if 'weather1_bodyUnitLabelTitle' in str(tag1):
                        n = n + 1
                        if n == 2:
                            wk_arry = str(tag1).split('>')
                            t_info_h_weather = str(wk_arry[1])
                            t_info_h_weather = t_info_h_weather.replace('</span','')
                            break

                #風速の抽出
                n = 0
                for tag1 in soup.find_all('span'):
                    if 'weather1_bodyUnitLabelData' in str(tag1):
                        n = n + 1
                        if n == 2:
                            wk_arry = str(tag1).split('>')
                            t_info_h_wind_speed = str(wk_arry[1])
                            t_info_h_wind_speed = t_info_h_wind_speed.replace('</span','')
                            t_info_h_wind_speed = t_info_h_wind_speed.replace('m','')
                            break
                
                #水温の抽出
                n = 0
                for tag1 in soup.find_all('span'):
                    if 'weather1_bodyUnitLabelData' in str(tag1):
                        n = n + 1
                        if n == 3:
                            wk_arry = str(tag1).split('>')
                            t_info_h_water_temperature = str(wk_arry[1])
                            t_info_h_water_temperature = t_info_h_water_temperature.replace('</span','')
                            t_info_h_water_temperature = t_info_h_water_temperature.replace('℃','')
                            break

                #波高の抽出
                n = 0
                for tag1 in soup.find_all('span'):
                    if 'weather1_bodyUnitLabelData' in str(tag1):
                        n = n + 1
                        if n == 4:
                            wk_arry = str(tag1).split('>')
                            t_info_h_wave_height = str(wk_arry[1])
                            t_info_h_wave_height = t_info_h_wave_height.replace('</span','')
                            t_info_h_wave_height = t_info_h_wave_height.replace('cm','')
                            break

                #風向区分の抽出
                t_info_h_wind = '不明'
                for tag1 in soup.find_all('p'):
                    if 'weather1_bodyUnitImage is-wind' in str(tag1):
                        if '"weather1_bodyUnitImage is-wind1"' in str(tag1):
                            t_info_h_wind = '左直'
                            break
                        if '"weather1_bodyUnitImage is-wind2"' in str(tag1):
                            t_info_h_wind = '追左'
                            break
                        if '"weather1_bodyUnitImage is-wind3"' in str(tag1):
                            t_info_h_wind = '追左'
                            break
                        if '"weather1_bodyUnitImage is-wind4"' in str(tag1):
                            t_info_h_wind = '追左'
                            break    
                        if '"weather1_bodyUnitImage is-wind5"' in str(tag1):
                            t_info_h_wind = '追直'
                            break
                        if '"weather1_bodyUnitImage is-wind6"' in str(tag1):
                            t_info_h_wind = '追右'
                            break
                        if '"weather1_bodyUnitImage is-wind7"' in str(tag1):
                            t_info_h_wind = '追右'
                            break
                        if '"weather1_bodyUnitImage is-wind8"' in str(tag1):
                            t_info_h_wind = '追右'
                            break
                        if '"weather1_bodyUnitImage is-wind9"' in str(tag1):
                            t_info_h_wind = '右直'
                            break
                        if '"weather1_bodyUnitImage is-wind10"' in str(tag1):
                            t_info_h_wind = '向左'
                            break
                        if '"weather1_bodyUnitImage is-wind11"' in str(tag1):
                            t_info_h_wind = '向左'
                            break
                        if '"weather1_bodyUnitImage is-wind12"' in str(tag1):
                            t_info_h_wind = '向左'
                            break
                        if '"weather1_bodyUnitImage is-wind13"' in str(tag1):
                            t_info_h_wind = '向直'
                            break
                        if '"weather1_bodyUnitImage is-wind14"' in str(tag1):
                            t_info_h_wind = '無風'
                            break
                        if '"weather1_bodyUnitImage is-wind15"' in str(tag1):
                            t_info_h_wind = '向右'
                            break
                        if '"weather1_bodyUnitImage is-wind16"' in str(tag1):
                            t_info_h_wind = '向右'
                            break
                        if '"weather1_bodyUnitImage is-wind17"' in str(tag1):
                            t_info_h_wind = '無風'
                            break

                #レコードの組み立て
                t_info_h_outrec = ''
                t_info_h_outrec = t_info_h_outrec + '"'  + t_info_h_yyyymmdd + '"'      #開催日付
                t_info_h_outrec = t_info_h_outrec + ',"' + t_info_h_pool_code + '"'     #場コード
                t_info_h_outrec = t_info_h_outrec + ',"' + t_info_h_race_no + '"'       #レース番号
                t_info_h_outrec = t_info_h_outrec + ',' + t_info_h_temperature          #気温
                t_info_h_outrec = t_info_h_outrec + ',"' + t_info_h_weather + '"'       #天候区分
                t_info_h_outrec = t_info_h_outrec + ',' + t_info_h_wind_speed           #風速
                t_info_h_outrec = t_info_h_outrec + ',' + t_info_h_water_temperature    #水温
                t_info_h_outrec = t_info_h_outrec + ',' + t_info_h_wave_height          #波高
                t_info_h_outrec = t_info_h_outrec + ',"' + t_info_h_wind + '"'          #風向区分
                #CSVレコードファイル出力
                fw.write(t_info_h_outrec + '\n')
    fw.close()
    print('直前情報ヘッダーテーブル「t_info_h」のインポートCSVファイル　完了')

#主処理
mkcsv_t_info_h() #直前情報ヘッダーテーブル「t_info_h」のインポートCSVファイルを作成
