'''
【システム】BOAT_RACE_DB2
【ファイル】170_mkcsv_t_result_h.py
【機能仕様】レース結果ヘッダHTMLファイルからレース情報タイトルテーブル「t_result_h」のインポートCSVファイルを作成する
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.02.01 ver 1.00
'''
import os
import datetime
from bs4 import BeautifulSoup
#インストールディレクトの定義
BASE_DIR = '/home/pi/BOAT_RACE_DB'

'''
【関　数】mkcsv_t_result_h
【機　能】レース結果ヘッダーファイルから直前情報ヘッダテーブル「t_result_h」のインポートCSVファイルを作成する
【引　数】なし
【戻り値】なし
'''
def mkcsv_t_result_h():
    print('レース結果ヘッダヘッダテーブル「t_result_h」のインポートCSVファイル　開始')
    in_path  = BASE_DIR + '/200_html/result'
    out_file = BASE_DIR + '/210_csv/t_result_h.csv'
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
                t_result_h_yyyymmdd = '' #開催日付
                t_result_h_pool_code = '' #場コード
                t_result_h_race_no = '' #レース番号
                t_result_h_temperature = '' #気温
                t_result_h_weather = '' #天候
                t_result_h_wind_speed = '' #風速
                t_result_h_water_temperature = '' #水温
                t_result_h_wave_height = '' #波高
                t_result_h_wind = '' #風向
                t_result_h_return = '' #返還
                t_result_h_decisive_factor = '' #決まり手
                t_result_h_remarks = '' #備考
                t_result_h_kiatu = '' #気圧
                t_result_h_situdo = '' #湿度
                #HTMLファイルからcsvレコード項目を抽出
                soup = BeautifulSoup(html, 'html.parser')

                #開催日付
                t_result_h_yyyymmdd = item[0:8]

                #場コード
                t_result_h_pool_code = item[8:10]

                #レース番号
                t_result_h_race_no  = item[10:12]

                #投票締切時刻
                t_result_h_scheduled_deadline = ''
                n = 0
                for tag1 in soup.find_all('td'):
                    if ':' in str(tag1):
                        for tag2 in str(tag1).splitlines():
                            if '<td class="">' in str(tag2):
                                n = n + 1
                                if n == int(t_result_h_race_no):
                                    t_result_h_scheduled_deadline = str(tag2)
                                    t_result_h_scheduled_deadline = t_result_h_scheduled_deadline.replace('<td class="">', '')
                                    t_result_h_scheduled_deadline = t_result_h_scheduled_deadline.replace('</td>', '')
                                    t_result_h_scheduled_deadline = t_result_h_scheduled_deadline[0:4] + '0'
                #気温
                n = 0
                for tag1 in soup.find_all('span'):
                    if 'weather1_bodyUnitLabelData' in str(tag1):
                        n = n + 1
                        if n == 1:
                            wk_arry = str(tag1).split('>')
                            t_result_h_temperature = str(wk_arry[1])
                            t_result_h_temperature = t_result_h_temperature.replace('</span','')
                            t_result_h_temperature = t_result_h_temperature.replace('℃','')
                            t_result_h_temperature = t_result_h_temperature.strip()
                            break

                #天候
                n = 0
                for tag1 in soup.find_all('span'):        
                    if 'weather1_bodyUnitLabelTitle' in str(tag1):
                        n = n + 1
                        if n == 2:
                            wk_arry = str(tag1).split('>')
                            t_result_h_weather = str(wk_arry[1])
                            t_result_h_weather = t_result_h_weather.replace('</span','')
                            t_result_h_weather = t_result_h_weather.strip()
                            break

                #風速
                n = 0
                for tag1 in soup.find_all('span'):
                    if 'weather1_bodyUnitLabelData' in str(tag1):
                        n = n + 1
                        if n == 2:
                            wk_arry = str(tag1).split('>')
                            t_result_h_wind_speed = str(wk_arry[1])
                            t_result_h_wind_speed = t_result_h_wind_speed.replace('</span','')
                            t_result_h_wind_speed = t_result_h_wind_speed.replace('m','')
                            t_result_h_wind_speed = t_result_h_wind_speed.strip()
                            break

                #水温
                n = 0
                for tag1 in soup.find_all('span'):
                    if 'weather1_bodyUnitLabelData' in str(tag1):
                        n = n + 1
                        if n == 3:
                            wk_arry = str(tag1).split('>')
                            t_result_h_water_temperature = str(wk_arry[1])
                            t_result_h_water_temperature = t_result_h_water_temperature.replace('</span','')
                            t_result_h_water_temperature = t_result_h_water_temperature.replace('℃','')
                            t_result_h_water_temperature = t_result_h_water_temperature.strip()
                            break

                #波高
                n = 0
                for tag1 in soup.find_all('span'):
                    if 'weather1_bodyUnitLabelData' in str(tag1):
                        n = n + 1
                        if n == 4:
                            wk_arry = str(tag1).split('>')
                            t_result_h_wave_height = str(wk_arry[1])
                            t_result_h_wave_height = t_result_h_wave_height.replace('</span','')
                            t_result_h_wave_height = t_result_h_wave_height.replace('cm','')
                            t_result_h_wave_height = t_result_h_wave_height.strip()
                            break

                #風向
                t_result_h_wind = '不明'
                for tag1 in soup.find_all('p'):
                    if 'weather1_bodyUnitImage is-wind' in str(tag1):
                        if '"weather1_bodyUnitImage is-wind1"' in str(tag1):
                            t_result_h_wind = '左直'
                            break
                        if '"weather1_bodyUnitImage is-wind2"' in str(tag1):
                            t_result_h_wind = '追左'
                            break
                        if '"weather1_bodyUnitImage is-wind3"' in str(tag1):
                            t_result_h_wind = '追左'
                            break
                        if '"weather1_bodyUnitImage is-wind4"' in str(tag1):
                            t_result_h_wind = '追左'
                            break    
                        if '"weather1_bodyUnitImage is-wind5"' in str(tag1):
                            t_result_h_wind = '追直'
                            break
                        if '"weather1_bodyUnitImage is-wind6"' in str(tag1):
                            t_result_h_wind = '追右'
                            break
                        if '"weather1_bodyUnitImage is-wind7"' in str(tag1):
                            t_result_h_wind = '追右'
                            break
                        if '"weather1_bodyUnitImage is-wind8"' in str(tag1):
                            t_result_h_wind = '追右'
                            break
                        if '"weather1_bodyUnitImage is-wind9"' in str(tag1):
                            t_result_h_wind = '右直'
                            break
                        if '"weather1_bodyUnitImage is-wind10"' in str(tag1):
                            t_result_h_wind = '向左'
                            break
                        if '"weather1_bodyUnitImage is-wind11"' in str(tag1):
                            t_result_h_wind = '向左'
                            break
                        if '"weather1_bodyUnitImage is-wind12"' in str(tag1):
                            t_result_h_wind = '向左'
                            break
                        if '"weather1_bodyUnitImage is-wind13"' in str(tag1):
                            t_result_h_wind = '向直'
                            break
                        if '"weather1_bodyUnitImage is-wind14"' in str(tag1):
                            t_result_h_wind = '無風'
                            break
                        if '"weather1_bodyUnitImage is-wind15"' in str(tag1):
                            t_result_h_wind = '向右'
                            break
                        if '"weather1_bodyUnitImage is-wind16"' in str(tag1):
                            t_result_h_wind = '向右'
                            break
                        if '"weather1_bodyUnitImage is-wind17"' in str(tag1):
                            t_result_h_wind = '無風'
                            break             

                #返還
                n = 0
                for tag1 in soup.find_all("div ", class_="grid_unit"):
                    n = n + 1
                    if n == 6:
                        for tag2 in str(tag1).splitlines():
                            if 'numberSet1_number is-type' in str(tag2):
                                wk_arry = str(tag2).split('>')
                                wk = str(wk_arry[1]).replace('</span', '')
                                t_result_h_return = t_result_h_return + wk         
                t_result_h_return = '' #返還

                #決まり手
                n = 0
                for tag1 in soup.find_all("div", class_="grid_unit"):
                    n = n + 1
                    if n == 6:
                        for tag2 in str(tag1).splitlines():
                            if 'is-fs16' in str(tag2):
                                wk_arry = str(tag2).split('>')
                                wk = str(wk_arry[1]).replace('</td', '')
                                t_result_h_decisive_factor = wk 

                #備考
                n = 0
                for tag1 in soup.find_all("table", class_="is-h201__3rdadd"):
                    for tag2 in str(tag1).splitlines():
                        if 'is-fs16' in str(tag2):
                            wk_arry = str(tag2).split('>')
                            wk = str(wk_arry[1]).replace('/td', '')
                            wk = wk.strip()
                            t_result_h_remarks = wk             

                #気圧 湿度
                amedasu_file  = BASE_DIR + '/200_html/kiatu/' +  t_result_h_pool_code + '_'  + t_result_h_yyyymmdd + '.html'
                fb2 = open(amedasu_file, 'r')
                html2 = fb2.read()
                fb2.close()
                soup2 = BeautifulSoup(html2, 'html.parser')
                for tag1 in soup2.find_all('tr'):
                    if 'text-align:right;' in str(tag1):
                        kiatu_flg = 0
                        n = 0
                        wk_arry = str(tag1).split('>')
                        for tag2 in wk_arry:
                            n = n + 1
                            if n == 3:
                                wk_time = str(tag2).replace('</td', '')
                                if wk_time == t_result_h_scheduled_deadline:
                                    kiatu_flg = 1
                            if n == 5 and kiatu_flg == 1:
                                t_result_h_kiatu =  str(tag2).replace('</td', '')
                            if n == 13 and kiatu_flg == 1:
                                t_result_h_situdo = str(tag2).replace('</td', '')

                #レコードの組み立て
                t_result_h_outrec = ''
                t_result_h_outrec = t_result_h_outrec + '"' + t_result_h_yyyymmdd + '"'         #開催日付
                t_result_h_outrec = t_result_h_outrec + ',"' + t_result_h_pool_code + '"'       #場コード
                t_result_h_outrec = t_result_h_outrec + ',"' + t_result_h_race_no + '"'         #レース番号
                t_result_h_outrec = t_result_h_outrec + ',' + t_result_h_temperature            #気温
                t_result_h_outrec = t_result_h_outrec + ',"' + t_result_h_weather + '"'         #天候
                t_result_h_outrec = t_result_h_outrec + ',' + t_result_h_wind_speed;            #風速
                t_result_h_outrec = t_result_h_outrec + ',' + t_result_h_water_temperature      #水温
                t_result_h_outrec = t_result_h_outrec + ',' + t_result_h_wave_height            #波高
                t_result_h_outrec = t_result_h_outrec + ',"' + t_result_h_wind + '"'            #風向
                t_result_h_outrec = t_result_h_outrec + ',"' + t_result_h_return + '"'          #返還
                t_result_h_outrec = t_result_h_outrec + ',"' + t_result_h_decisive_factor + '"' #決まり手
                t_result_h_outrec = t_result_h_outrec + ',"' + t_result_h_remarks + '"'         #備考
                t_result_h_outrec = t_result_h_outrec + ',' + t_result_h_kiatu                  #気圧
                t_result_h_outrec = t_result_h_outrec + ',' + t_result_h_situdo                #湿度

                #CSVレコードファイル出力
                fw.write(t_result_h_outrec + '\n')
    fw.close()
    print('直前情報ヘッダーテーブル「t_result_h」のインポートCSVファイル　完了')

#主処理
mkcsv_t_result_h() #直前情報ヘッダーテーブル「t_result_h」のインポートCSVファイルを作成
