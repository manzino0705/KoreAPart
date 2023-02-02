import pandas as pd
import matplotlib.pyplot as plt

def cal_apt_pir(addr, size=0):
    
    apt_list=[]
    avg_pir={'2016':0, '2017':0, '2018':0, '2019':0, '2020':0,'2021':0}
    apt_price = 0 
    
    for i in range(2016, 2022, 1):
        # 데이터 불러오기 
        df_pir = pd.read_csv("./static/data/"+str(i)+"_pir.csv")

        # size 입력 안받으면, 
        if size == 0 :
            if df_pir[(df_pir['시군구']==addr) & (df_pir['전용면적(㎡)']==size)].values.tolist() == []: 
                get_size = df_pir[(df_pir['시군구']==addr)][['전용면적(㎡)']].values.tolist() # 거래 금액 
                if get_size != [] :
                    size = sorted(get_size)[0]
                    size = float(size[0])
                    print(size)
                    

        # XX 년도 PIR , 거래 금액 
        tmp_list = df_pir[(df_pir['시군구']==addr) & (df_pir['전용면적(㎡)']==size)][['계약년월', 'PIR']].values.tolist() # 거래 금액 
        
        if tmp_list == [] : continue 
            
        for t in tmp_list : apt_list.append( [ str(t[0])[:6],t[1] ]) 

        # 연도별 X구 PIR 
        # avg_pir.append(df_pir['평균 PIR'][0])
        avg_pir[str(i)]=df_pir['평균 PIR'][0]

        apt_price = df_pir[(df_pir['계약년월']==tmp_list[-1][0]) & (df_pir['PIR']==tmp_list[-1][1])][['거래금액(만원)']].values.tolist() # 거래 금액 
        apt_price_result = apt_price[0]
        # print(apt_price_result)
    
    # print(avg_pir)
    return apt_list, avg_pir , apt_price_result

# apt = { 'apt_city':  '서울특별시 강남구' ,'apt_addr': '개포로 264', 'apt_size': 0 } 
# apt_pir_data, avg_pir, apt_price = cal_apt_pir( apt['apt_city'] + " " + apt['apt_addr'] , apt['apt_size'] )

# print(apt_pir_data)
# print(avg_pir)
# print(apt['apt_city'] + " " + apt['apt_addr'])
# print(apt_price) # 만원 단위 
