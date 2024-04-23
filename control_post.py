from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import os
import pandas
import time
import pywinauto

def post_chart(title, file_name):
    """
    特定のタイトルとCSVでwordpressのチャートを新規作成
    
    Parameters:
    title(String): チャートのタイトル
    file_name(String): ファイル名（フルパス）
    """

    #windows + r で C:\Program Files\Google\Chrome\Application\chrome.exe -remote-debugging-port=9000を実行してから実行すること
    #wordpressにはログインしてある前提
    #すでに開いているブラウザを取得
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9000")
    driver = webdriver.Chrome(options=options)

    #ブラウザにアクセス
    driver.get('https://funding.se-piyopiyo.com/wp-admin/post-new.php?post_type=m-chart')
    #描画を待つ
    time.sleep(3)

    #チャートタイトル
    driver.find_element(By.ID ,"title").send_keys(title)
    time.sleep(0.5)

    #ファイルを選ぶをクリック
    element= driver.find_element(By.LINK_TEXT, "ファイルを選ぶ")
    element.click()

    #ファイル選択ダイアログにアクセス
    #ダイアログタイトルを手掛かりにwindowを探す
    findWindow = lambda: pywinauto.findwindows.find_windows(title='開く')[0]
    dialog = pywinauto.timings.wait_until_passes(5, 1, findWindow)
    pwa_app = pywinauto.Application()
    pwa_app.connect(handle=dialog)
    window = pwa_app['開く']

    #ファイル名入力→選択（ファイル名の欄にフルパス）
    tb = window[u"ファイル名(&N):"]
    if tb.is_enabled():
         tb.click()
         edit = window.Edit4
         edit.set_focus()
         edit.type_keys(file_name + '%O',with_spaces=True)
    time.sleep(3)

    #インポートボタンをクリックしCSVを取り込む
    element= driver.find_element(By.LINK_TEXT, "インポート")
    element.click()
    time.sleep(3)

    #チャートの種類（プルダウン）
    select = Select(driver.find_element(By.ID ,"m-chart-type"))
    select.select_by_index(2)
    time.sleep(3)

    #Show labelのチェックボックスを外す
    checkbox_elem1 = driver.find_element(By.ID ,"m-chart-labels")
    if checkbox_elem1.is_selected(): 
      checkbox_elem1.click()
    time.sleep(0.5)

    #凡例を表示のチェックボックスを外す
    checkbox_elem2 = driver.find_element(By.ID ,"m-chart-legend")
    if checkbox_elem2.is_selected(): 
      checkbox_elem2.click()
    time.sleep(0.5)

    #縦軸のタイトルは固定
    driver.find_element(By.ID ,"m-chart-y-title").send_keys("（百万円）")
    time.sleep(0.5)

    #noindexを設定する
    checkbox_elem3 = driver.find_element(By.ID ,"the_page_noindex_1")
    if not checkbox_elem3.is_selected(): 
      checkbox_elem3.click()
    time.sleep(0.5)

    #トップに移動
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(2)

    #公開ボタンをクリック
    element= driver.find_element(By.ID, "publish")
    element.click()
    time.sleep(3)

# CSVファイルの内容を読み込みチャートを作成
os.chdir("C:\\Users\\XXXX\\OneDrive\\ドキュメント\\python")
chunksize = 1
reader = pandas.read_csv('toshinList.csv', chunksize=chunksize, encoding='utf-8')

#基準価格→純資産総額の順で作成
for chunk in reader:
    url =  chunk["CSVのURL"].values[0]
    utf_dir1 = "C:\\Users\\XXXX\\OneDrive\\ドキュメント\\python\\utf8_base\\" + chunk["銘柄コード"].values[0] +".csv"
    utf_dir2 = "C:\\Users\\XXXX\\OneDrive\\ドキュメント\\python\\utf8_asset\\" + chunk["銘柄コード"].values[0] +".csv"
    
    #基準価格
    shohin = chunk["銘柄"].values[0] + "_基準価格"
    print(shohin + "を作成中")
    post_chart(shohin, utf_dir1)

    #純資産総額
    time.sleep(2)
    shohin = chunk["銘柄"].values[0] + "_純資産総額"
    print(shohin + "を作成中")
    post_chart(shohin, utf_dir2)
