import sqlite3

def data_select_KBO_RANK():
    # 데이터베이스 파일과 연결
    conn = sqlite3.connect('./baseball_predict_app/src/baseballDB.db')
    cur = conn.cursor()

    sql_select = """
    SELECT *
    FROM KBO_RANK
    """

    cur.execute(sql_select)
    fetch = cur.fetchall()
    return fetch