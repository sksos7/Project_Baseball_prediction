from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import sqlite3
from time import sleep

# 데이터베이스 파일과 연결
conn = sqlite3.connect('./baseball_predict_app/src/baseballDB.db')
cur = conn.cursor()

# KBO 공식 홈페이지
kbo_url = 'https://www.koreabaseball.com/'

# 크롬드라이브 접근
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('/Users/sksos/chromedriver_win32/chromedriver.exe', options=options)

""" 경기 기록 테이블 """
# 경기기록 페이지 불러오기
record_url = 'Schedule/Schedule.aspx'
driver.get(kbo_url+record_url)

flag_create_table = 0
key_list = ['04', '05', '06', '07', '08', '09', '10']
for send_key in key_list:
    # '월'을 바꾸면서 데이터를 삽입
    driver.find_element_by_id('ddlMonth').send_keys(send_key)
    sleep(0.5)
    page_record = driver.page_source
    soup_record = BeautifulSoup(page_record, 'html.parser')
    record_element = soup_record.find('div', class_ = 'tbl-type06')

    if flag_create_table == 0:
        # 테이블 삭제 초기화
        cur.execute("""DROP TABLE IF EXISTS KBO_RECORD""")

        # KBO_RECORD 테이블 생성
        record_columns = record_element.select('tr > th')
        sql_create_table_KBO_RECORD = f"""
        CREATE TABLE IF NOT EXISTS KBO_RECORD
        (
            {record_columns[0].text} STR,
            {record_columns[1].text} STR,
            {record_columns[2].text} STR,
            {record_columns[7].text} STR,
            {record_columns[8].text} STR
        );
        """
        cur.execute(sql_create_table_KBO_RECORD)
        flag_create_table = flag_create_table + 1

    # 데이터 삽입
    sql_insert_KBO_RECORD = f"""
    INSERT INTO KBO_RECORD
    (
        {record_columns[0].text},
        {record_columns[1].text},
        {record_columns[2].text},
        {record_columns[7].text},
        {record_columns[8].text}
    )
    VALUES ( ?, ?, ?, ?, ?);
    """

    record_data = record_element.select('tbody > tr')
    record_value_list = []
    for x in record_data:
        tmp = []
        if len(x.find_all('td')) == 8 :
            tmp.append(save)
            tmp.append(x.find_all('td')[0].text)
            tmp.append(x.find_all('td')[1].text)
            tmp.append(x.find_all('td')[6].text)
            tmp.append(x.find_all('td')[7].text)
        else:
            save = x.find_all('td')[0].text
            tmp.append(x.find_all('td')[0].text)
            tmp.append(x.find_all('td')[1].text)
            tmp.append(x.find_all('td')[2].text)
            tmp.append(x.find_all('td')[7].text)
            tmp.append(x.find_all('td')[8].text)

        record_value_list.append(tmp)

    cur.executemany(sql_insert_KBO_RECORD, tuple(record_value_list) )
conn.commit()

driver.close()