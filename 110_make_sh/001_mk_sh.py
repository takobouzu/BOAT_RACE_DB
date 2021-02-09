'''
【システム】BOAT_RACE_DB2
【ファイル】001_mk_sh.py
【機能仕様】ボートレースオフィシャルサイトから関連情報が格納されたHTMLファイルをダウンロードするシェルを生成する
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.02.01 ver 1.00
'''
import os
import datetime
from bs4 import BeautifulSoup
#インストールディレクトの定義
BASE_DIR = '/home/pi/BOAT_RACE_DB'

'''
【関　数】mk_tenken_sh
【機　能】前検データ・ダウンロードシェル生成
【引　数】なし
【戻り値】なし
'''
def mk_tenken_sh():
    print("==>前検データ・ダウンロードシェル生成　開始")
    in_path  = BASE_DIR + '/200_html/yesterday'
    out_file = BASE_DIR + '/120_get_html_sh/001_tenken.sh'
    fw = open(out_file, 'w')
    fw.write('#【システム】BOAT_RACE_DB2\n')
    fw.write('#【ファイル】001_tenken.sh\n')
    fw.write('#【機能仕様】ボートレースオフィシャルサイトから前検データが格納されたHTMLファイルをダウンロードする\n')
    fw.write('#【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3\n')
    fw.write('#【生成日付】' + str(datetime.datetime.now()) + '\n')
    for item in os.listdir(path=in_path):
        if item != '.html' and item != '.DS_Store':
            in_file = in_path + '/' + item
            fb = open(in_file, 'r')
            html = fb.read()
            fb.close()
            #初日の判定
            soup = BeautifulSoup(html, 'html.parser')
            for tag1 in soup.find_all('tbody'):
                if '初日' in str(tag1):
                    for tag2 in str(tag1).splitlines():
                        if '/owpc/pc/race/raceindex' in tag2:
                            #前検データ格納URLの生成
                            wk_arry = str(tag2).split('?')
                            wk_arry = str(wk_arry[1]).split('"')
                            wk_str = str(wk_arry[0]).replace('amp;','')
                            wk_arry = wk_str.split('&')
                            wk_poolcode = str(wk_arry[0]).replace('jcd=','')
                            wk_yyyymmdd = str(wk_arry[1]).replace('hd=', '')
                            wk_url = 'https://www.boatrace.jp/owpc/pc/race/rankingmotor?' + wk_str
                            #前検データのダウンロードコマンドの生成
                            outrec = "curl '" + wk_url + "' -o " + BASE_DIR + '/200_html/tenken/'  + wk_poolcode + '_' + wk_yyyymmdd + '.html'
                            fw.write(outrec + '\n')
    fw.close()
    print("==>前検データ・ダウンロードシェル生成　完了")

'''
【関　数】mk_race_table_sh
【機　能】出走表データ・ダウンロードシェル生成
【引　数】なし
【戻り値】なし
'''
def mk_race_table_sh():
    print("==>出走表データ・ダウンロードシェル生成　開始")
    in_path  = BASE_DIR + '/200_html/yesterday'
    out_file = BASE_DIR + '/120_get_html_sh/002_race_table.sh'
    fw = open(out_file, 'w')
    fw.write('#【システム】BOAT_RACE_DB2\n')
    fw.write('#【ファイル】002_race_table.sh\n')
    fw.write('#【機能仕様】ボートレースオフィシャルサイトから出走表データが格納されたHTMLファイルをダウンロードする\n')
    fw.write('#【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3\n')
    fw.write('#【生成日付】' + str(datetime.datetime.now()) + '\n')
    for item in os.listdir(path=in_path):
        if item != '.html':
            in_file = in_path + '/' + item
            fb = open(in_file, 'r')
            html = fb.read()
            fb.close()
            soup = BeautifulSoup(html, 'html.parser')
            for tag1 in soup.find_all('tbody'):
                for tag2 in str(tag1).splitlines():
                    if '/owpc/pc/race/racelist' in tag2:
                        wk_arry = str(tag2).split(';')
                        wk_poolcode = wk_arry[1].replace('&amp','')
                        wk_poolcode = wk_poolcode.replace('jcd=','')
                        wk_yyyymmdd = wk_arry[2].replace('">出走表</a></li>','')
                        wk_yyyymmdd = wk_yyyymmdd.replace('hd=','')
                        base_url = 'https://www.boatrace.jp/owpc/pc/race/racelist?rno=@raceno&jcd=@poolcode&hd=@yyyymmdd'
                        base_html = BASE_DIR + '/200_html/race_table/' + '@yyyymmdd@poolcode@raceno.html'
                        n = 0
                        for i in range(12):
                            n = n + 1
                            wk_url = base_url
                            wk_url = wk_url.replace('@raceno', str(n))
                            wk_url = wk_url.replace('@poolcode', wk_poolcode)
                            wk_url = wk_url.replace('@yyyymmdd', wk_yyyymmdd)
                            wk_html = base_html
                            wk_html = wk_html.replace('@yyyymmdd', wk_yyyymmdd)
                            wk_html = wk_html.replace('@poolcode', wk_poolcode)
                            wk_html = wk_html.replace('@raceno', '%02d' % (n))
                            #出走表データ・ダウンロードコマンド生成
                            outrec = "curl '" + wk_url + "' -o " + wk_html
                            fw.write(outrec + '\n')
    fw.close()
    print("==>出走表データ・ダウンロードシェル生成　完了")

'''
【関　数】mk_result_sh
【機　能】成績データ・ダウンロードシェル生成
【引　数】なし
【戻り値】なし
'''
def mk_result_sh():
    print("==>成績データ・ダウンロードシェル生成　開始")
    in_path  = BASE_DIR + '/200_html/yesterday'
    out_file = BASE_DIR + '/120_get_html_sh/003_result.sh'
    fw = open(out_file, 'w')
    fw.write('#【システム】BOAT_RACE_DB2\n')
    fw.write('#【ファイル】003_result.sh\n')
    fw.write('#【機能仕様】ボートレースオフィシャルサイトから成績データが格納されたHTMLファイルをダウンロードする\n')
    fw.write('#【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3\n')
    fw.write('#【生成日付】' + str(datetime.datetime.now()) + '\n')
    for item in os.listdir(path=in_path):
        if item != '.html':
            in_file = in_path + '/' + item
            fb = open(in_file, 'r')
            html = fb.read()
            fb.close()
            soup = BeautifulSoup(html, 'html.parser')
            for tag1 in soup.find_all('tbody'):
                for tag2 in str(tag1).splitlines():
                    if '/owpc/pc/race/raceresult' in tag2:
                        wk_arry = str(tag2).split(';')
                        wk_poolcode = wk_arry[1].replace('&amp','')
                        wk_poolcode = wk_poolcode.replace('jcd=','')
                        wk_yyyymmdd = wk_arry[2].replace('">結果</a></li>','')
                        wk_yyyymmdd = wk_yyyymmdd.replace('hd=','')
                        base_url = 'https://www.boatrace.jp/owpc/pc/race/raceresult?rno=@raceno&jcd=@poolcode&hd=@yyyymmdd'
                        base_html = BASE_DIR + '/200_html/result/' + '@yyyymmdd@poolcode@raceno.html'
                        n = 0
                        for i in range(12):
                            n = n + 1
                            wk_url = base_url
                            wk_url = wk_url.replace('@raceno', str(n))
                            wk_url = wk_url.replace('@poolcode', wk_poolcode)
                            wk_url = wk_url.replace('@yyyymmdd', wk_yyyymmdd)
                            wk_html = base_html
                            wk_html = wk_html.replace('@yyyymmdd', wk_yyyymmdd)
                            wk_html = wk_html.replace('@poolcode', wk_poolcode)
                            wk_html = wk_html.replace('@raceno', '%02d' % (n))
                            #出走表データ・ダウンロードコマンド生成
                            outrec = "curl '" + wk_url + "' -o " + wk_html
                            fw.write(outrec + '\n')
    fw.close()
    print("==>成績データ・ダウンロードシェル生成　完了")

'''
【関　数】mk_last_info_sh
【機　能】展示データ・ダウンロードシェル生成
【引　数】なし
【戻り値】なし
'''
def mk_last_info_sh():
    print("==>展示データ・ダウンロードシェル生成　開始")
    in_path  = BASE_DIR + '/200_html/yesterday'
    out_file = BASE_DIR + '/120_get_html_sh/004_last_info.sh'
    fw = open(out_file, 'w')
    fw.write('#【システム】BOAT_RACE_DB2\n')
    fw.write('#【ファイル】004_last_info.sh\n')
    fw.write('#【機能仕様】ボートレースオフィシャルサイトから展示データが格納されたHTMLファイルをダウンロードする\n')
    fw.write('#【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3\n')
    fw.write('#【生成日付】' + str(datetime.datetime.now()) + '\n')
    for item in os.listdir(path=in_path):
        if item != '.html':
            in_file = in_path + '/' + item
            fb = open(in_file, 'r')
            html = fb.read()
            fb.close()
            soup = BeautifulSoup(html, 'html.parser')
            for tag1 in soup.find_all('tbody'):
                for tag2 in str(tag1).splitlines():
                    if '/owpc/pc/race/beforeinfo' in tag2:
                        wk_arry = str(tag2).split(';')
                        wk_poolcode = wk_arry[1].replace('&amp','')
                        wk_poolcode = wk_poolcode.replace('jcd=','')
                        wk_yyyymmdd = wk_arry[2].replace('">直前情報</a></li>','')
                        wk_yyyymmdd = wk_yyyymmdd.replace('hd=','')
                        base_url = 'https://www.boatrace.jp/owpc/pc/race/beforeinfo?rno=@raceno&jcd=@poolcode&hd=@yyyymmdd'
                        base_html = BASE_DIR + '/200_html/last_info/' + '@yyyymmdd@poolcode@raceno.html'
                        n = 0
                        for i in range(12):
                            n = n + 1
                            wk_url = base_url
                            wk_url = wk_url.replace('@raceno', str(n))
                            wk_url = wk_url.replace('@poolcode', wk_poolcode)
                            wk_url = wk_url.replace('@yyyymmdd', wk_yyyymmdd)
                            wk_html = base_html
                            wk_html = wk_html.replace('@yyyymmdd', wk_yyyymmdd)
                            wk_html = wk_html.replace('@poolcode', wk_poolcode)
                            wk_html = wk_html.replace('@raceno', '%02d' % (n))
                            #展示データ・ダウンロードコマンド生成
                            outrec = "curl '" + wk_url + "' -o " + wk_html
                            fw.write(outrec + '\n')
    fw.close()
    print("==>展示データ・ダウンロードシェル生成　完了")

'''
【関　数】mk_odds_3t_sh
【機　能】三連単オッズ・ダウンロードシェル生成
【引　数】なし
【戻り値】なし
'''
def mk_odds_3t_sh():
    print("==>三連単オッズ・ダウンロードシェル生成　開始")
    in_path  = BASE_DIR + '/200_html/yesterday'
    out_file = BASE_DIR + '/120_get_html_sh/005_odds_3t.sh'
    fw = open(out_file, 'w')
    fw.write('#【システム】BOAT_RACE_DB2\n')
    fw.write('#【ファイル】005_odds_3t.sh\n')
    fw.write('#【機能仕様】ボートレースオフィシャルサイトから三連単オッズが格納されたHTMLファイルをダウンロードする\n')
    fw.write('#【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3\n')
    fw.write('#【生成日付】' + str(datetime.datetime.now()) + '\n')
    for item in os.listdir(path=in_path):
        if item != '.html':
            in_file = in_path + '/' + item
            fb = open(in_file, 'r')
            html = fb.read()
            fb.close()
            soup = BeautifulSoup(html, 'html.parser')
            for tag1 in soup.find_all('tbody'):
                for tag2 in str(tag1).splitlines():
                    if '/owpc/pc/race/odds3t' in tag2:
                        wk_arry = str(tag2).split(';')
                        wk_poolcode = wk_arry[1].replace('&amp','')
                        wk_poolcode = wk_poolcode.replace('jcd=','')
                        wk_yyyymmdd = wk_arry[2].replace('">オッズ</a></li>','')
                        wk_yyyymmdd = wk_yyyymmdd.replace('hd=','')
                        base_url = 'https://www.boatrace.jp/owpc/pc/race/odds3t?rno=@raceno&jcd=@poolcode&hd=@yyyymmdd'
                        base_html = BASE_DIR + '/200_html/odds_3t/' + '@yyyymmdd@poolcode@raceno.html'
                        n = 0
                        for i in range(12):
                            n = n + 1
                            wk_url = base_url
                            wk_url = wk_url.replace('@raceno', str(n))
                            wk_url = wk_url.replace('@poolcode', wk_poolcode)
                            wk_url = wk_url.replace('@yyyymmdd', wk_yyyymmdd)
                            wk_html = base_html
                            wk_html = wk_html.replace('@yyyymmdd', wk_yyyymmdd)
                            wk_html = wk_html.replace('@poolcode', wk_poolcode)
                            wk_html = wk_html.replace('@raceno', '%02d' % (n))
                            #三連単オッズ・ダウンロードコマンド生成
                            outrec = "curl '" + wk_url + "' -o " + wk_html
                            fw.write(outrec + '\n')
    fw.close()
    print("==>三連単オッズ・ダウンロードシェル生成　完了")
    
'''
【関　数】mk_kiatu_sh
【機　能】気圧データ・ダウンロードシェル生成
【引　数】なし
【戻り値】なし
'''
def mk_kiatu_sh():
    print("==>気圧データ・ダウンロードシェル生成　開始")
    #ボートレース場の最寄りのアメダスURLを登録
    kiatu_url_arry = []
    kiatu_url_arry.append('') #ダミー
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=42&block_no=47624&year=') #前橋地方気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=44&block_no=47662&year=') #東京管区気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=44&block_no=47662&year=') #東京管区気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=44&block_no=47662&year=') #東京管区気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=44&block_no=47662&year=') #東京管区気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=50&block_no=47654&year=') #浜松地方気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=51&block_no=47653&year=') #伊良湖特別地域気象観測所
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=51&block_no=47653&year=') #伊良湖特別地域気象観測所
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=53&block_no=47651&year=') #津地方気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=57&block_no=47616&year=') #福井地方気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=60&block_no=47761&year=') #彦根地方気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=62&block_no=47772&year=') #大阪管区気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=63&block_no=47770&year=') #神戸地方気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=71&block_no=47895&year=') #徳島地方気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=72&block_no=47891&year=') #高松地方気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=66&block_no=47768&year=') #岡山地方気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=67&block_no=47765&year=') #広島地方気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=81&block_no=47784&year=') #山口地方気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=81&block_no=47762&year=') #下関地方気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=82&block_no=47809&year=') #飯塚特別地域気象観測所
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=82&block_no=47809&year=') #飯塚特別地域気象観測所
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=82&block_no=47807&year=') #福岡管区気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=85&block_no=47813&year=') #佐賀地方気象台
    kiatu_url_arry.append('https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=84&block_no=47817&year=') #長崎地方気象台     

    in_path  = BASE_DIR + '/200_html/yesterday'
    out_file = BASE_DIR + '/120_get_html_sh/006_kiatu.sh'

    fw = open(out_file, 'w')
    fw.write('#【システム】BOAT_RACE_DB2\n')
    fw.write('#【ファイル】006_kiatu.sh\n')
    fw.write('#【機能仕様】ボートレース場の最寄りのアメダス気象データが格納されたHTMLファイルをダウンロードする\n')
    fw.write('#【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3\n')
    fw.write('#【生成日付】' + str(datetime.datetime.now()) + '\n')
    for item in os.listdir(path=in_path):
       if item != '.html':
            in_file = in_path + '/' + item
            fb = open(in_file, 'r')
            html = fb.read()
            fb.close()
            soup = BeautifulSoup(html, 'html.parser')
            for tag1 in soup.find_all('tbody'):
                for tag2 in str(tag1).splitlines():
                    if '/owpc/pc/race/racelist' in tag2:
                        wk_arry = str(tag2).split(';')
                        wk_poolcode = wk_arry[1].replace('&amp','')
                        wk_poolcode = wk_poolcode.replace('jcd=','')
                        wk_yyyymmdd = wk_arry[2].replace('">出走表</a></li>','')
                        wk_yyyymmdd = wk_yyyymmdd.replace('hd=','')
                        wk_yyyy = wk_yyyymmdd[0:4]
                        wk_mm = wk_yyyymmdd[4:6]
                        wk_dd = wk_yyyymmdd[6:8]
                        base_url = kiatu_url_arry[int(wk_poolcode)] + '@yyyy&month=@mm&day=@dd&view='
                        base_html = BASE_DIR + '/200_html/kiatu/' + '@poolcode_@yyyymmdd.html'
                        wk_url = base_url
                        wk_url = wk_url.replace('@yyyy', wk_yyyy)
                        wk_url = wk_url.replace('@mm', wk_mm)
                        wk_url = wk_url.replace('@dd', wk_dd)
                        wk_html = base_html
                        wk_html = wk_html.replace('@yyyymmdd', wk_yyyymmdd)
                        wk_html = wk_html.replace('@poolcode', wk_poolcode)
                        #気圧ダウンロードコマンド生成
                        outrec = "curl '" + wk_url + "' -o " + wk_html
                        fw.write(outrec + '\n')
    fw.close()
    print("==>気圧データ・ダウンロードシェル生成　完了")

'''
【関　数】mk_x_race_table_sh
【機　能】当日出走表データ・ダウンロードシェル生成
【引　数】なし
【戻り値】なし
'''
def mk_x_race_table_sh():
    print("==>当日出走表データ・ダウンロードシェル生成　開始")
    in_path  = BASE_DIR + '/200_html/today'
    out_file = BASE_DIR + '/120_get_html_sh/x01_race_table.sh'
    fw = open(out_file, 'w')
    fw.write('#【システム】BOAT_RACE_DB2\n')
    fw.write('#【ファイル】x01_race_table.sh\n')
    fw.write('#【機能仕様】ボートレースオフィシャルサイトから当日出走表データが格納されたHTMLファイルをダウンロードする\n')
    fw.write('#【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3\n')
    fw.write('#【生成日付】' + str(datetime.datetime.now()) + '\n')
    for item in os.listdir(path=in_path):
        if item != '.html':
            in_file = in_path + '/' + item
            fb = open(in_file, 'r')
            html = fb.read()
            fb.close()
            soup = BeautifulSoup(html, 'html.parser')
            for tag1 in soup.find_all('tbody'):
                for tag2 in str(tag1).splitlines():
                    if '/owpc/pc/race/racelist' in tag2:
                        wk_arry = str(tag2).split(';')
                        wk_poolcode = wk_arry[1].replace('&amp','')
                        wk_poolcode = wk_poolcode.replace('jcd=','')
                        wk_yyyymmdd = wk_arry[2].replace('">出走表</a></li>','')
                        wk_yyyymmdd = wk_yyyymmdd.replace('hd=','')
                        base_url = 'https://www.boatrace.jp/owpc/pc/race/racelist?rno=@raceno&jcd=@poolcode&hd=@yyyymmdd'
                        base_html = BASE_DIR + '/200_html/x_race_table/' + '@yyyymmdd@poolcode@raceno.html'
                        n = 0
                        for i in range(12):
                            n = n + 1
                            wk_url = base_url
                            wk_url = wk_url.replace('@raceno', str(n))
                            wk_url = wk_url.replace('@poolcode', wk_poolcode)
                            wk_url = wk_url.replace('@yyyymmdd', wk_yyyymmdd)
                            wk_html = base_html
                            wk_html = wk_html.replace('@yyyymmdd', wk_yyyymmdd)
                            wk_html = wk_html.replace('@poolcode', wk_poolcode)
                            wk_html = wk_html.replace('@raceno', '%02d' % (n))
                            #出走表データ・ダウンロードコマンド生成
                            outrec = "curl '" + wk_url + "' -o " + wk_html
                            fw.write(outrec + '\n')
    fw.close()
    print("==>当日出走表データ・ダウンロードシェル生成　完了")

#主処理
print("ダウンロードシェル生成開始")
mk_tenken_sh()          #前検データ・ダウンロードシェル生成
mk_race_table_sh()      #出走表データ・ダウンロードシェル生成
mk_result_sh()          #成績データ・ダウンロードシェル生成
mk_last_info_sh()       #展示データ・ダウンロードシェル生成
mk_odds_3t_sh()         #三連単オッズ・ダウンロードシェル生成
mk_kiatu_sh()           #気圧データ・ダウンロードシェル生成
mk_x_race_table_sh()    #当日出走表データ・ダウンロードシェル生成
print("ダウンロードシェル生成完了")
