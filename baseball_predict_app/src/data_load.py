import sqlite3
from baseball_predict_app.src import data_pretreatment

# 순위 데이터
def data_select_KBO_RANK():
    # 데이터베이스 파일과 연결
    conn = sqlite3.connect('./baseball_predict_app/src/baseballDB.db')
    cur = conn.cursor()

    url_name = "팀 순위"
    sql_select = """
    SELECT *
    FROM KBO_RANK
    """

    cur.execute(sql_select)
    fetch = cur.fetchall()
    return fetch, url_name

# 타자 데이터
def data_select_KBO_HITTER():
    # 데이터베이스 파일과 연결
    conn = sqlite3.connect('./baseball_predict_app/src/baseballDB.db')
    cur = conn.cursor()

    url_name = "타자 기록"
    sql_select = """
    SELECT *
    FROM KBO_HITTER
    """

    cur.execute(sql_select)
    fetch = cur.fetchall()
    return fetch, url_name

# 투수 데이터
def data_select_KBO_PITCHER():
    # 데이터베이스 파일과 연결
    conn = sqlite3.connect('./baseball_predict_app/src/baseballDB.db')
    cur = conn.cursor()

    url_name = "투수 기록"
    sql_select = """
    SELECT *
    FROM KBO_PITCHER
    """

    cur.execute(sql_select)
    fetch = cur.fetchall()
    return fetch, url_name

# 수비 데이터
def data_select_KBO_DEFENSE():
    # 데이터베이스 파일과 연결
    conn = sqlite3.connect('./baseball_predict_app/src/baseballDB.db')
    cur = conn.cursor()

    url_name = "수비 기록"
    sql_select = """
    SELECT *
    FROM KBO_DEFENSE
    """

    cur.execute(sql_select)
    fetch = cur.fetchall()
    return fetch, url_name

# 주루 데이터
def data_select_KBO_RUNNER():
    # 데이터베이스 파일과 연결
    conn = sqlite3.connect('./baseball_predict_app/src/baseballDB.db')
    cur = conn.cursor()

    url_name = "주루 기록"
    sql_select = """
    SELECT *
    FROM KBO_RUNNER
    """

    cur.execute(sql_select)
    fetch = cur.fetchall()
    return fetch, url_name

# 경기 결과 및 일정 데이터
def data_select_KBO_RESULT():
    # 데이터베이스 파일과 연결
    conn = sqlite3.connect('./baseball_predict_app/src/baseballDB.db')
    cur = conn.cursor()

    url_name = "경기 결과"
    sql_select = """
    SELECT *
    FROM KBO_RECORD
    """

    cur.execute(sql_select)
    fetch = cur.fetchall()
    return fetch, url_name

def data_select_KBO_PREDICT():
    conn = sqlite3.connect('./baseball_predict_app/src/baseballDB.db')
    cur = conn.cursor()

    sql_select = """
    SELECT *
    FROM PREDICT
    """
    cur.execute(sql_select)
    fetch = cur.fetchall()

    X_train, y_train, X_test, predict_record = data_pretreatment.pretreatment()
    return predict_record, fetch