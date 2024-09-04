import requests
from bs4 import BeautifulSoup
import PyPDF2
import io
import sqlite3
from datetime import datetime
import re
import os

def get_database_path():
    home_dir = os.path.expanduser("~")
    db_dir = os.path.join(home_dir, ".onwut")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "onwut_data.db")
    return db_path

def scrape_all_data():
    # データベースのパスを取得
    db_path = get_database_path()

    # SQLiteデータベースに接続
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reports
                      (title TEXT, date TEXT, url TEXT, content TEXT, source TEXT)''')

    data_entries = []

    # データソース1
    url1 = 'https://www.meti.go.jp/statistics/tyo/iip/kako_press.html'
    source1 = '経済産業省'
    response1 = requests.get(url1)
    response1.raise_for_status()
    soup1 = BeautifulSoup(response1.content, 'lxml')
    reference_links = soup1.find_all('a', href=lambda href: href and '/reference/' in href)
    base_url1 = 'https://www.meti.go.jp/statistics/tyo/iip/'

    for link in reference_links:
        pdf_url = base_url1 + link['href']
        match = re.search(r'b\d{4}_(\d{6})', link['href'])
        if match:
            year_month = match.group(1)
            year = int(year_month[:4])
            month = int(year_month[4:])
            file_date = datetime(year, month, 1)
            pdf_response = requests.get(pdf_url)
            pdf_response.raise_for_status()
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_response.content))
            pdf_text = ""
            for page in range(len(pdf_reader.pages)):
                pdf_text += pdf_reader.pages[page].extract_text()
            formatted_date = f"{file_date.year}-{file_date.month:02}"
            data_entries.append(("鉱工業生産", formatted_date, pdf_url, pdf_text, source1))

    # データソース2
    main_url = 'https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200531&tstat=000000110001&cycle=1&tclass1=000001040276&tclass2=000001040277&tclass3val=0'
    source2 = 'e-Stat'
    response2 = requests.get(main_url)
    response2.raise_for_status()
    soup2 = BeautifulSoup(response2.content, 'lxml')
    month_links = soup2.select('ul.stat-cycle_ul_other a.stat-item_child')
    base_url2 = 'https://www.e-stat.go.jp'

    for link in month_links:
        month_url = base_url2 + link['href']
        month_response = requests.get(month_url)
        month_response.raise_for_status()
        month_soup = BeautifulSoup(month_response.content, 'lxml')

        publish_date_tag = month_soup.find('span', class_='stat-sp', string='公開（更新）日  ')
        if publish_date_tag:
            publish_date = publish_date_tag.find_next_sibling(string=True).strip()
            title = f"{publish_date} 労働力調査"
        else:
            publish_date = "公開日が見つかりませんでした"
            title = f"不明 労働力調査"

        pdf_link_tag = month_soup.find('a', class_='stat-dl_icon stat-icon_2 stat-icon_format js-dl stat-download_icon_left')
        if pdf_link_tag:
            pdf_url = base_url2 + pdf_link_tag['href']
            pdf_response = requests.get(pdf_url)
            pdf_response.raise_for_status()
            pdf_file = io.BytesIO(pdf_response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_text = ""
            for page in range(len(pdf_reader.pages)):
                pdf_text += pdf_reader.pages[page].extract_text()
            formatted_date = datetime.now().strftime('%Y-%m')
            data_entries.append((title, formatted_date, pdf_url, pdf_text, source2))

    # 日付順にソートしてデータベースに保存
    data_entries.sort(key=lambda x: x[1])
    cursor.executemany('''INSERT INTO reports (title, date, url, content, source)
                          VALUES (?, ?, ?, ?, ?)''', data_entries)

    conn.commit()
    conn.close()
    print(f"すべてのデータが取得され、データベースに日付順で保存されました: {db_path}")

if __name__ == "__main__":
    scrape_all_data()
