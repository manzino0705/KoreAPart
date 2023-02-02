# 사용자 정보 입력 받아 소비 금액 예측 해서 return 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

import joblib
import seaborn as sns
from pandas import Series, DataFrame

# # 한글 , 마이너스 부호 깨짐 방지용 
plt.rc('font', family='NanumGothicCoding')
sns.set(font="NanumGothicCoding",#"NanumGothicCoding", 
       rc={"axes.unicode_minus":False}, # 마이너스 부호 깨짐 현상 해결
       style='darkgrid')

# # 데이터 불러오기 
df_consume = pd.read_csv("./static/model/consume_data.csv")
df_consume = df_consume[:48901]

# # 필요한 컬럼만 추출 
df_consume = df_consume[['성별', '나이', '학력코드', '취업', '직업코드', '소득구간코드', '소비지출코드']] 

# # One Hot Encoding으로 범주형 변수 가변수화 진행 
# df_consume = pd.get_dummies(df_consume, columns=['학력코드']) # 학력 코드 별로 원핫 인코딩 적용
# df_consume = pd.get_dummies(df_consume, columns=['직업코드'])

# # AI 모델링 진행 
# # target : 소비지출코드
y = df_consume['소비지출코드'].values 
x = df_consume.drop(columns=['소비지출코드']).values

# # 데이터 Set 나누기 (Train:Test = 8:2)
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)

# # 스케일러 호출
scaler = MinMaxScaler()

# # 스케일링 (Train, Test)
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# #boosting - XGBoost 
# # !pip install xgboost

# # 라이브러리 임포트
from xgboost import XGBRegressor

# # 모델 불러오기
xgb_model = XGBRegressor(n_estimators = 1000, learning_rate = 0.01, random_state = 42)   
# # 모델 학습하기
xgb_model.fit(x_train, y_train)

# # 예측하기
xgb_predict = xgb_model.predict(x_test)

#model 저장
joblib.dump(xgb_model,'./static/model/comsume.pkl')

# load_model = joblib.load('./static/model/comsume.pkl')

# test = {'성별':1, '나이':29, '학력코드':3, '취업':1, '직업코드':4, '소득구간코드': 50000000 } 
# # 학력코드, 
# test_df = DataFrame(test, index = [0])

# # 불러온 모델로 예측하기
# re = load_model.predict(test_df)

# print(re)

