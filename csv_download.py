import codecs
import os
import pandas
import requests
import time
import csv

def download_files(url,file_dir):
    """
    Web上のファイルデータをダウンロード
    
    Parameters:
    url(String): ダウンロードURL
    file_dir(String): ファイルのあるディレクトリ
    """

    #Web上のファイルデータをダウンロード
    response = requests.get(url)
    time.sleep(1)   #ダウンロードに要する時間を確保する（ファイルの重さに応じて調整。1GBにつき1秒）

    #HTTP Responseのエラーチェック
    try:
        response_status = response.raise_for_status()
    except Exception as exc:
        print("Error:{}".format(exc))
    
    
    # HTTP Responseが正常な場合は下記実行
    if response_status == None:

        #open()関数にwbを渡し、バイナリ書き込みモードで新規ファイル生成
        file = open(file_dir,"wb")

        #各チャンクをwrite()関数でローカルファイルに書き込む
        for chunk in response.iter_content(100000):
            file.write(chunk)

        #ファイルを閉じる
        file.close()
        print("ダウンロード・ファイル保存完了")

def convert_utf8(sjis_path, utf8_path1, utf8_path2):
    """
    CSVをSJISからUTF8に変換する
    
    Parameters:
    sjis_path(String): SJISのCSVパス(変換元)
    utf8_path1(String): UTF-8のCSVパス(変換先)
    utf8_path2(String): UTF-8のCSVパス(変換先)
    """

    filein  = codecs.open(sjis_path, "r", "shift_jis")
    fileout1 = codecs.open(utf8_path1, "w", "utf-8")
    fileout2 = codecs.open(utf8_path2, "w", "utf-8")

    for row in filein:
        fileout1.write(row)
        fileout2.write(row)
    
    filein.close()
    fileout1.close()
    fileout2.close()

def delete_columns(utf8_path1, utf8_path2):
    """
    CSVの特定のカラムを削除
    
    Parameters:
    utf8_path1(String): UTF-8のCSVパス(convert_utf8のutf8_path1)
    utf8_path2(String): UTF-8のCSVパス(convert_utf8のutf8_path2)
    """
    df1 = pandas.read_csv(utf8_path1)
    df1.drop(df1.columns[[2,3,4]], axis=1, inplace=True)
    df1.to_csv(utf8_path1, index=False)

    df2 = pandas.read_csv(utf8_path2)
    df2.drop(df2.columns[[1,3,4]], axis=1, inplace=True)
    df2.to_csv(utf8_path2, index=False)

# CSVファイルの内容を読み込み、ダウンロードや加工を行う（パスはまじめにやるなら考えるべきだが趣味なのでべた書き）
os.chdir("C:\\Users\\XXXX\\OneDrive\\ドキュメント\\python")
chunksize = 1
reader = pandas.read_csv('toshinList.csv', chunksize=chunksize, encoding='utf-8')
for chunk in reader:
    shohin = chunk["銘柄"].values[0]
    url =  chunk["CSVのURL"].values[0]
    file_dir = "C:\\Users\\XXXX\\OneDrive\\ドキュメント\\python\\csv\\" + chunk["銘柄コード"].values[0] +".csv"
    utf_dir1 = "C:\\Users\\XXXX\\OneDrive\\ドキュメント\\python\\utf8_base\\" + chunk["銘柄コード"].values[0] +".csv"
    utf_dir2 = "C:\\Users\\XXXX\\OneDrive\\ドキュメント\\python\\utf8_asset\\" + chunk["銘柄コード"].values[0] +".csv"
    
    print(shohin)
    download_files(url,file_dir)
    convert_utf8(file_dir,utf_dir1,utf_dir2)
    delete_columns(utf_dir1,utf_dir2)