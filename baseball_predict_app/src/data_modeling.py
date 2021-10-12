from baseball_predict_app.src import data_pretreatment

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

learning()    