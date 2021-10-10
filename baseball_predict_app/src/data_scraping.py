import requests
from bs4 import BeautifulSoup
import sqlite3

# 데이터베이스 파일과 연결
conn = sqlite3.connect('./baseball_predict_app/src/baseballDB.db')
cur = conn.cursor()

# KBO 공식 홈페이지
kbo_url = 'https://www.koreabaseball.com/'

def team_rank_table():
    """ 팀 순위 테이블 """
    # 순위 페이지 불러오기
    ranking_url = 'TeamRank/TeamRank.aspx'
    page_rank = requests.get(kbo_url+ranking_url)
    soup_rank = BeautifulSoup(page_rank.content, 'html.parser')

    rank_element = soup_rank.find_all('table', class_ = 'tData')

    # 테이블 삭제 초기화
    cur.execute("""DROP TABLE IF EXISTS KBO_RANK""")

    # KBO_RANK 테이블 생성
    rank_columns = rank_element[0].select('tr > th')
    sql_create_table_KBO_RANK = f"""
    CREATE TABLE IF NOT EXISTS KBO_RANK
    (
        {rank_columns[0].text} INT,
        {rank_columns[1].text} STR,
        {rank_columns[2].text} INT,
        {rank_columns[3].text} INT,
        {rank_columns[4].text} INT,
        {rank_columns[5].text} INT,
        {rank_columns[6].text} FLOAT,
        {rank_columns[7].text} FLOAT,
        {rank_columns[8].text} STR,
        {rank_columns[9].text} STR,
        {rank_columns[10].text} STR,
        {rank_columns[11].text} STR
    );
    """
    cur.execute(sql_create_table_KBO_RANK)

    # 데이터 삽입
    sql_insert_KBO_RANK = f"""
    INSERT INTO KBO_RANK
    (
        {rank_columns[0].text},
        {rank_columns[1].text},
        {rank_columns[2].text},
        {rank_columns[3].text},
        {rank_columns[4].text},
        {rank_columns[5].text},
        {rank_columns[6].text},
        {rank_columns[7].text},
        {rank_columns[8].text},
        {rank_columns[9].text},
        {rank_columns[10].text},
        {rank_columns[11].text}
    )
    VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    rank_data = rank_element[0].select('tbody > tr')
    rank_value_list = []
    for tr in rank_data:
        tmp = []
        for td in tr.find_all('td'):
            tmp.append(td.text)
        rank_value_list.append(tmp)

    cur.executemany(sql_insert_KBO_RANK, tuple(rank_value_list) )
    return conn.commit()

def hitter_table():
    """ 팀 타자 기록 테이블 """
    # 팀 타자 기록 페이지 불러오기
    hitter_url = 'Record/Team/Hitter/Basic1.aspx'
    page_hitter = requests.get(kbo_url+hitter_url)
    soup_hitter = BeautifulSoup(page_hitter.content, 'html.parser')

    hitter_element = soup_hitter.find_all('table', class_ = 'tData tt')

    # 테이블 삭제 초기화
    cur.execute("""DROP TABLE IF EXISTS KBO_HITTER""")

    # KBO_HITTER 테이블 생성
    hitter_columns = hitter_element[0].select('tr > th')
    two_base = hitter_columns[8].text
    three_base = hitter_columns[9].text

    sql_create_table_KBO_HITTER = f"""
    CREATE TABLE IF NOT EXISTS KBO_HITTER
    (
        {hitter_columns[0].text} INT,
        {hitter_columns[1].text} STR,
        {hitter_columns[2].text} FLOAT,
        {hitter_columns[3].text} INT,
        {hitter_columns[4].text} INT,
        {hitter_columns[5].text} INT,
        {hitter_columns[6].text} INT,
        {hitter_columns[7].text} INT,
        "{hitter_columns[8].text}" INT,
        "{hitter_columns[9].text}" INT,
        {hitter_columns[10].text} INT,
        {hitter_columns[11].text} INT,
        {hitter_columns[12].text} INT,
        {hitter_columns[13].text} INT,
        {hitter_columns[14].text} INT
    );
    """
    cur.execute(sql_create_table_KBO_HITTER)

    # 데이터 삽입
    sql_insert_KBO_HITTER = f"""
    INSERT INTO KBO_HITTER
    (
            {hitter_columns[0].text},
            {hitter_columns[1].text},
            {hitter_columns[2].text},
            {hitter_columns[3].text},
            {hitter_columns[4].text},
            {hitter_columns[5].text},
            {hitter_columns[6].text},
            {hitter_columns[7].text},
            "{hitter_columns[8].text}",
            "{hitter_columns[9].text}",
            {hitter_columns[10].text},
            {hitter_columns[11].text},
            {hitter_columns[12].text},
            {hitter_columns[13].text},
            {hitter_columns[14].text}
    )
    VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    hitter_data = hitter_element[0].select('tbody > tr')
    hitter_value_list = []
    for tr in hitter_data:
        tmp = []
        for td in tr.find_all('td'):
            tmp.append(td.text)
        hitter_value_list.append(tmp)

    cur.executemany(sql_insert_KBO_HITTER, tuple(hitter_value_list) )
    return conn.commit()

def pitcher_table():
    """ 팀 투수 기록 테이블 """
    # 팀 타자 기록 페이지 불러오기
    pitcher_url = 'Record/Team/Pitcher/Basic1.aspx'
    page_pitcher = requests.get(kbo_url+pitcher_url)
    soup_pitcher = BeautifulSoup(page_pitcher.content, 'html.parser')

    pitcher_element = soup_pitcher.find_all('table', class_ = 'tData tt')

    # 테이블 삭제 초기화
    cur.execute("""DROP TABLE IF EXISTS KBO_PITCHER""")

    # KBO_PITCHER 테이블 생성
    pitcher_columns = pitcher_element[0].select('tr > th')
    sql_create_table_KBO_PITCHER = f"""
    CREATE TABLE IF NOT EXISTS KBO_PITCHER
    (
        {pitcher_columns[0].text} INT,
        {pitcher_columns[1].text} STR,
        {pitcher_columns[2].text} FLOAT,
        {pitcher_columns[3].text} INT,
        {pitcher_columns[4].text} INT,
        {pitcher_columns[5].text} INT,
        {pitcher_columns[6].text} INT,
        {pitcher_columns[7].text} INT,
        {pitcher_columns[8].text} FLOAT,
        {pitcher_columns[9].text} STR,
        {pitcher_columns[10].text} INT,
        {pitcher_columns[11].text} INT,
        {pitcher_columns[12].text} INT,
        {pitcher_columns[13].text} INT,
        {pitcher_columns[14].text} INT,
        {pitcher_columns[15].text} INT,
        {pitcher_columns[16].text} INT,
        {pitcher_columns[17].text} FLOAT
    );
    """
    cur.execute(sql_create_table_KBO_PITCHER)

    # 데이터 삽입
    sql_insert_KBO_PITCHER = f"""
    INSERT INTO KBO_PITCHER
    (
        {pitcher_columns[0].text},
        {pitcher_columns[1].text},
        {pitcher_columns[2].text},
        {pitcher_columns[3].text},
        {pitcher_columns[4].text},
        {pitcher_columns[5].text},
        {pitcher_columns[6].text},
        {pitcher_columns[7].text},
        {pitcher_columns[8].text},
        {pitcher_columns[9].text},
        {pitcher_columns[10].text},
        {pitcher_columns[11].text},
        {pitcher_columns[12].text},
        {pitcher_columns[13].text},
        {pitcher_columns[14].text},
        {pitcher_columns[15].text},
        {pitcher_columns[16].text},
        {pitcher_columns[17].text}
    )
    VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    pitcher_data = pitcher_element[0].select('tbody > tr')
    pitcher_value_list = []
    for tr in pitcher_data:
        tmp = []
        for td in tr.find_all('td'):
            tmp.append(td.text)
        pitcher_value_list.append(tmp)

    cur.executemany(sql_insert_KBO_PITCHER, tuple(pitcher_value_list) )
    return conn.commit()

def defense_table():
    """ 팀 수비 기록 테이블 """
    # 팀 수비 기록 페이지 불러오기
    defense_url = 'Record/Team/Defense/Basic.aspx'
    page_defense = requests.get(kbo_url+defense_url)
    soup_defense = BeautifulSoup(page_defense.content, 'html.parser')

    defense_element = soup_defense.find_all('table', class_ = 'tData tt')

    # 테이블 삭제 초기화
    cur.execute("""DROP TABLE IF EXISTS KBO_DEFENSE""")

    # KBO_DEFENSE 테이블 생성
    defense_columns = defense_element[0].select('tr > th')
    sql_create_table_KBO_DEFENSE = f"""
    CREATE TABLE IF NOT EXISTS KBO_DEFENSE
    (
        {defense_columns[0].text} INT,
        {defense_columns[1].text} STR,
        {defense_columns[2].text} INT,
        {defense_columns[3].text} INT,
        {defense_columns[4].text} INT,
        {defense_columns[5].text} INT,
        {defense_columns[6].text} INT,
        {defense_columns[7].text} INT,
        {defense_columns[8].text} FLOAT,
        {defense_columns[9].text} INT,
        {defense_columns[10].text} INT,
        {defense_columns[11].text} INT,
        "{defense_columns[12].text}" FLOAT
    );
    """
    cur.execute(sql_create_table_KBO_DEFENSE)

    # 데이터 삽입
    sql_insert_KBO_DEFENSE = f"""
    INSERT INTO KBO_DEFENSE
    (
        {defense_columns[0].text},
        {defense_columns[1].text},
        {defense_columns[2].text},
        {defense_columns[3].text},
        {defense_columns[4].text},
        {defense_columns[5].text},
        {defense_columns[6].text},
        {defense_columns[7].text},
        {defense_columns[8].text},
        {defense_columns[9].text},
        {defense_columns[10].text},
        {defense_columns[11].text},
        "{defense_columns[12].text}"
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    defense_data = defense_element[0].select('tbody > tr')
    defense_value_list = []
    for tr in defense_data:
        tmp = []
        for td in tr.find_all('td'):
            tmp.append(td.text)
        defense_value_list.append(tmp)

    cur.executemany(sql_insert_KBO_DEFENSE, tuple(defense_value_list) )
    return conn.commit()

def runner_table():
    """ 팀 주루 기록 테이블 """
    # 팀 주루 기록 페이지 불러오기
    runner_url = 'Record/Team/Runner/Basic.aspx'
    page_runner = requests.get(kbo_url+runner_url)
    soup_runner = BeautifulSoup(page_runner.content, 'html.parser')

    runner_element = soup_runner.find_all('table', class_ = 'tData tt')

    # 테이블 삭제 초기화
    cur.execute("""DROP TABLE IF EXISTS KBO_RUNNER""")

    # KBO_RUNNER 테이블 생성
    runner_columns = runner_element[0].select('tr > th')
    sql_create_table_KBO_RUNNER = f"""
    CREATE TABLE IF NOT EXISTS KBO_RUNNER
    (
        {runner_columns[0].text} INT,
        {runner_columns[1].text} STR,
        {runner_columns[2].text} INT,
        {runner_columns[3].text} INT,
        {runner_columns[4].text} INT,
        {runner_columns[5].text} INT,
        "{runner_columns[6].text}" FLOAT,
        {runner_columns[7].text} INT,
        {runner_columns[8].text} INT
    );
    """
    cur.execute(sql_create_table_KBO_RUNNER)

    # 데이터 삽입
    sql_insert_KBO_RUNNER = f"""
    INSERT INTO KBO_RUNNER
    (
        {runner_columns[0].text},
        {runner_columns[1].text},
        {runner_columns[2].text},
        {runner_columns[3].text},
        {runner_columns[4].text},
        {runner_columns[5].text},
        "{runner_columns[6].text}",
        {runner_columns[7].text},
        {runner_columns[8].text}
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    runner_data = runner_element[0].select('tbody > tr')
    runner_value_list = []
    for tr in runner_data:
        tmp = []
        for td in tr.find_all('td'):
            tmp.append(td.text)
        runner_value_list.append(tmp)

    cur.executemany(sql_insert_KBO_RUNNER, tuple(runner_value_list) )
    return conn.commit()

team_rank_table()
hitter_table()
pitcher_table()
defense_table()
runner_table()