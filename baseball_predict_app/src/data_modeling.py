import sys
sys.path.insert(0, 'baseball_predict_app.src')
import data_pretreatment
import sqlite3

def learning():
    X_train, y_train, X_test, test = data_pretreatment.pretreatment()

    from category_encoders import OrdinalEncoder
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.impute import SimpleImputer 
    from sklearn.pipeline import make_pipeline
    from sklearn.model_selection import cross_val_score

    pipe = make_pipeline(
        OrdinalEncoder(), 
        SimpleImputer(), 
        RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=10, oob_score=True)
    )

    pipe.fit(X_train, y_train)
    return pipe.predict(X_test)

# for x in learning():
#     print(x)

def last_predict():
    conn = sqlite3.connect('./baseball_predict_app/src/baseballDB.db')
    cur = conn.cursor()

    cur.execute("""DROP TABLE IF EXISTS PREDICT""")

    sql_create_table_PREDICT = """
    CREATE TABLE IF NOT EXISTS PREDICT
    (
        PRED INT
    );
    """
    cur.execute(sql_create_table_PREDICT)

    # 데이터 삽입
    sql_insert_PREDICT = "INSERT INTO PREDICT (PRED) VALUES (?);"
    #breakpoint()
    for x in learning():
        cur.execute(sql_insert_PREDICT, (int(x),))
    conn.commit()

last_predict()