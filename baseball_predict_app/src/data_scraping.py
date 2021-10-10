import requests
from bs4 import BeautifulSoup
import sqlite3

# 데이터베이스 파일과 연결
conn = sqlite3.connect('./baseball_predict_app/src/baseballDB.db')
cur = conn.cursor()

# 순위 페이지 불러오기
kbo_url = 'https://www.koreabaseball.com/'
ranking_url = 'TeamRank/TeamRank.aspx'
page_rank = requests.get(kbo_url+ranking_url)
soup_rank = BeautifulSoup(page_rank.content, 'html.parser')

rank_element = soup_rank.find_all('table', class_ = 'tData')

# 테이블 삭제 초기화
cur.execute("""DROP TABLE KBO_RANK""")

# 테이블 생성
sql_create_table_KBO_RANK = f"""
CREATE TABLE IF NOT EXISTS KBO_RANK
(
    {rank_element[0].select('tr > th')[0].text} INT,
    {rank_element[0].select('tr > th')[1].text} STR,
    {rank_element[0].select('tr > th')[2].text} INT,
    {rank_element[0].select('tr > th')[3].text} INT,
    {rank_element[0].select('tr > th')[4].text} INT,
    {rank_element[0].select('tr > th')[5].text} INT,
    {rank_element[0].select('tr > th')[6].text} FLOAT,
    {rank_element[0].select('tr > th')[7].text} FLOAT,
    {rank_element[0].select('tr > th')[8].text} STR,
    {rank_element[0].select('tr > th')[9].text} STR,
    {rank_element[0].select('tr > th')[10].text} STR,
    {rank_element[0].select('tr > th')[11].text} STR
);
"""
cur.execute(sql_create_table_KBO_RANK)

# 테이블 삽입
sql_insert_KBO_RANK = f"""
INSERT INTO KBO_RANK
(
    {rank_element[0].select('tr > th')[0].text},
    {rank_element[0].select('tr > th')[1].text},
    {rank_element[0].select('tr > th')[2].text},
    {rank_element[0].select('tr > th')[3].text},
    {rank_element[0].select('tr > th')[4].text},
    {rank_element[0].select('tr > th')[5].text},
    {rank_element[0].select('tr > th')[6].text},
    {rank_element[0].select('tr > th')[7].text},
    {rank_element[0].select('tr > th')[8].text},
    {rank_element[0].select('tr > th')[9].text},
    {rank_element[0].select('tr > th')[10].text},
    {rank_element[0].select('tr > th')[11].text}
)
VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

rank_value_list = []
for tr in rank_element[0].select('tbody > tr'):
    tmp = []
    for td in tr.find_all('td'):
        tmp.append(td.text)
    rank_value_list.append(tmp)


cur.executemany(sql_insert_KBO_RANK, tuple(rank_value_list) )
conn.commit()