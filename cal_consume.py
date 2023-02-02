import joblib
import seaborn as sns
from pandas import Series, DataFrame


def user_consume(user): 

    load_model = joblib.load('./static/model/comsume.pkl')

    df_before = dict() 
    df_before['성별'] = user['gender']
    df_before['나이'] = int(user['age'])
                            
    grade_list = [ '무학','초등학교 졸업','중학교 졸업','고등학교 졸업','대학교 2년제 졸업','대학교 4년제 졸업','석사','박사' ]
    df_before['학력코드'] = 1 # default 무학 
    for g in grade_list : 
        if user['grade'] == g :
            df_before['학력코드'] = grade_list.index(g) + 1 
    
    if user['employ'] == 'O' : 
        df_before['취업'] = 1
    else : df_before['취업'] = 0 
    
    # 직업군(관리자,전문가,사무직,서비스직,판매직,농업,기술자,기계조립,단순노동)
    
    job_list = [ '관리자','전문가','사무직','서비스직','판매직','농업','기술자','기계조립','단순노동' ]
    df_before['직업코드'] = 1 # default 관리자
    for j in job_list : 
        if user['job'] == j :
            df_before['직업코드'] = job_list.index(j) + 1 
            
    df_before['소득구간코드'] = int(user['income']) * 10000
    
    df_after = DataFrame(df_before, index = [0])

    # 불러온 모델로 예측하기
    result = load_model.predict(df_after)
    print(df_after)
    print(result)
    
    return result // 10000 