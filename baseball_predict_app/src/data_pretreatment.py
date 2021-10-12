import sqlite3
import pandas as pd
from re import findall

# import sys

# if 'google.colab' in sys.modules:
#     # Install packages in Colab
#     !pip install category_encoders==2.*


def pretreatment():
    # 데이터베이스 파일과 연결
    conn = sqlite3.connect('./baseball_predict_app/src/baseballDB.db')

    sql_select_record = """
    SELECT *
    FROM KBO_RECORD
    """

    sql_select_hitter = """
    SELECT *
    FROM KBO_HITTER
    """

    sql_select_pitcher = """
    SELECT *
    FROM KBO_PITCHER
    """

    df_record = pd.read_sql(sql_select_record, conn)
    df_hitter = pd.read_sql(sql_select_hitter, conn)
    df_pitcher = pd.read_sql(sql_select_pitcher, conn)

    # 정상적으로 진행된 경기만
    condition = (df_record['비고'] == '-') & (df_record['경기'].str.contains('롯데'))
    real_record = df_record[condition].copy()
    real_record.reset_index(inplace = True, drop = True)
    record = real_record.loc[:,['시간','경기','구장']].copy()
    
    train_record = record[:-14].copy()
    predict_record = record[-14:].copy()
    predict_record.reset_index(inplace=True, drop=True)

    # 경기 결과의 스코어, 팀으로 나누기
    pre_score = []
    sub_score = []
    pre_team = []
    sub_team = []
    # 이전 경기 결과
    for x in train_record['경기']:
        pre_score.append(findall("\d+", x)[0])
        sub_score.append(findall("\d+", x)[1])

        remove_score = ''.join([i for i in x if not i.isdigit()])
        pre_team.append(remove_score.split('vs')[0])
        sub_team.append(remove_score.split('vs')[1])

    pre_team_pred = []
    sub_team_pred = []
    # 예측
    for y in predict_record['경기']:
        remove_score = ''.join([i for i in y if not i.isdigit()])
        pre_team_pred.append(remove_score.split('vs')[0])
        sub_team_pred.append(remove_score.split('vs')[1])

    train_record.loc[:,'Away_score'] = pre_score
    train_record.loc[:,'Home_score'] = sub_score
    train_record.loc[:,'Away'] = pre_team
    train_record.loc[:,'Home'] = sub_team

    predict_record.loc[:,'Away'] = pre_team_pred
    predict_record.loc[:,'Home'] = sub_team_pred

    # 스코어 형변환
    train_record.loc[:,'Away_score'] = pd.to_numeric(train_record['Away_score'])
    train_record.loc[:,'Home_score'] = pd.to_numeric(train_record['Home_score'])

    # 무승부 제거
    condition = (train_record.loc[:,'Away_score'] == train_record.loc[:,'Home_score'])
    train_record = train_record[~condition]

    train_record.drop(['경기'], inplace=True, axis=1)
    predict_record.drop(['경기'], inplace=True, axis=1)

    # 롯데가 이겼을 경우
    c1 = (train_record['Away_score'] < train_record['Home_score']) & (train_record['구장'] == '사직')
    c2 = (train_record['Away_score'] > train_record['Home_score']) & (train_record['구장'] != '사직')
    condition = c1 | c2

    # 승리시 1, 패배시 0
    train_record.loc[:,'결과'] = condition
    train_record.loc[:,'결과'] = train_record.loc[:,'결과'].map(lambda x : 1 if x else 0)
    train_record.reset_index(inplace=True, drop=True)

    # 상대팀과의 타자 스탯 차이
    hitter = []
    for x in train_record.iterrows():
        c1 = df_hitter['팀명'] == x[1]['Away']
        c2 = df_hitter['팀명'] == x[1]['Home']

        hitter_condition = df_hitter[c1|c2].iloc[:,1:]

        hitter_condition.reset_index(inplace=True, drop=True)

        c_index = hitter_condition['팀명'] == '롯데'
        lotte_index = hitter_condition[c_index].index[0]
        other_index = hitter_condition[~c_index].index[0]

        hitter_condition = hitter_condition.reindex(index=[other_index, lotte_index])

        hitter_record = hitter_condition.iloc[:,1:].diff()
        hitter_record.drop(other_index, inplace=True)
        hitter_record.rename(columns={'R':'Hitter.R', 'H':'Hitter.H', 'HR':'Hitter.HR'}, inplace=True)

        hitter_list = list(hitter_record.loc[lotte_index])
        hitter_list[0] = round(hitter_list[0], 5)

        hitter.append(hitter_list)

    hitter_pred = []
    for y in predict_record.iterrows():
        c1 = df_hitter['팀명'] == y[1]['Away']
        c2 = df_hitter['팀명'] == y[1]['Home']

        hitter_condition = df_hitter[c1|c2].iloc[:,1:]

        hitter_condition.reset_index(inplace=True, drop=True)

        c_index = hitter_condition['팀명'] == '롯데'
        lotte_index = hitter_condition[c_index].index[0]
        other_index = hitter_condition[~c_index].index[0]

        hitter_condition = hitter_condition.reindex(index=[other_index, lotte_index])

        hitter_record = hitter_condition.iloc[:,1:].diff()
        hitter_record.drop(other_index, inplace=True)
        hitter_record.rename(columns={'R':'Hitter.R', 'H':'Hitter.H', 'HR':'Hitter.HR'}, inplace=True)

        hitter_list = list(hitter_record.loc[lotte_index])
        hitter_list[0] = round(hitter_list[0], 5)

        hitter_pred.append(hitter_list)

    # 타자 기록 추가
    hitter_add = pd.DataFrame(hitter, columns=hitter_record.columns)
    hitter_add_pred = pd.DataFrame(hitter_pred, columns=hitter_record.columns)

    train_hitter = pd.concat([train_record,hitter_add],axis=1)
    predict_hitter = pd.concat([predict_record,hitter_add_pred],axis=1)

    # 상대팀과의 투수 스탯 차이
    pitcher = []
    for x in train_record.iterrows():
        c1 = df_pitcher['팀명'] == x[1]['Away']
        c2 = df_pitcher['팀명'] == x[1]['Home']

        pitcher_condition = df_pitcher[c1|c2].iloc[:,1:]
        pitcher_condition.drop(['IP','G'], axis=1, inplace=True)

        pitcher_condition.reset_index(inplace=True, drop=True)

        c_index = pitcher_condition['팀명'] == '롯데'
        lotte_index = pitcher_condition[c_index].index[0]
        other_index = pitcher_condition[~c_index].index[0]

        pitcher_condition = pitcher_condition.reindex(index=[other_index, lotte_index])
        pitcher_record = pitcher_condition.iloc[:,1:].diff()
        pitcher_record.drop(other_index, inplace=True)
        pitcher_record.rename(columns={'H':'Pitcher.H', 'R':'Pitcher.R', 'HR':'Pitcher.HR'}, inplace=True)

        pitcher_list = list(pitcher_record.loc[lotte_index])
        pitcher_list[0] = round(pitcher_list[0], 5)
        pitcher_list[5] = round(pitcher_list[5], 5)
        pitcher_list[13] = round(pitcher_list[13], 5)

        pitcher.append(pitcher_list)

    pitcher_pred = []
    for y in predict_record.iterrows():
        c1 = df_pitcher['팀명'] == y[1]['Away']
        c2 = df_pitcher['팀명'] == y[1]['Home']

        pitcher_condition = df_pitcher[c1|c2].iloc[:,1:]
        pitcher_condition.drop(['IP','G'], axis=1, inplace=True)

        pitcher_condition.reset_index(inplace=True, drop=True)

        c_index = pitcher_condition['팀명'] == '롯데'
        lotte_index = pitcher_condition[c_index].index[0]
        other_index = pitcher_condition[~c_index].index[0]

        pitcher_condition = pitcher_condition.reindex(index=[other_index, lotte_index])
        pitcher_record = pitcher_condition.iloc[:,1:].diff()
        pitcher_record.drop(other_index, inplace=True)
        pitcher_record.rename(columns={'H':'Pitcher.H', 'R':'Pitcher.R', 'HR':'Pitcher.HR'}, inplace=True)

        pitcher_list = list(pitcher_record.loc[lotte_index])
        pitcher_list[0] = round(pitcher_list[0], 5)
        pitcher_list[5] = round(pitcher_list[5], 5)
        pitcher_list[13] = round(pitcher_list[13], 5)

        pitcher_pred.append(pitcher_list)

    # 투수 기록 추가
    pitcher_add = pd.DataFrame(pitcher, columns=pitcher_record.columns)
    pitcher_add_pred = pd.DataFrame(pitcher_pred, columns=pitcher_record.columns)

    train_hitter_pitcher = pd.concat([train_hitter,pitcher_add],axis=1)
    predict_hitter_pitcher = pd.concat([predict_hitter,pitcher_add_pred],axis=1)

    train_hitter_pitcher.drop(['Away_score','Home_score'], axis=1, inplace=True)

    train_hitter_pitcher.loc[:,'win or lose'] = train_hitter_pitcher.loc[:,'결과']
    train_hitter_pitcher.drop(['결과'], axis=1, inplace=True)

    X_train = train_hitter_pitcher.iloc[:,:-1].copy()
    y_train = train_hitter_pitcher.loc[:,'win or lose'].copy()

    X_test = predict_hitter_pitcher.copy()
    return X_train, y_train, X_test, real_record[-14:]

    