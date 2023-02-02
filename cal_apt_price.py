import pandas as pd
import matplotlib.pyplot as plt

def calAPTprice(user):
    
    # 강남구, 얼마 이하 아파트 찾기 
    
    save = int(user['income']) - int(user['spend'])
    asset = [ int(user['asset'])+save*10, int(user['asset'])+save*20, int(user['asset'])+save*30 ]

    df_pir = pd.read_csv("./static/data/2021_pir.csv")
    df_pir.drop_duplicates(['시군구', '단지명']) 
    df_pir.drop(['평균 가구 처분가능소득 (만 원)', '평균 PIR' ], axis = 1 )
    
    res_apt = [] 
    
    for i in range(3):
        tmp_list = df_pir[(df_pir['거래금액(만원)']<= asset[i])].values.tolist() # 거래 금액 
        tmp_list.sort( key=lambda x : -x[5] )  # 금액 기준으로 sort 
        
        addr = tmp_list[i][0]
        apt = tmp_list[i][1]
        size = tmp_list[i][2]
        price = tmp_list[i][5]
        year = tmp_list[i][7]
        faddr = addr + ' ' + apt # 전체 이름
        print(faddr)
        res_apt.append([asset[i],addr,apt,size,price,year,faddr])

    return res_apt
    
    # 시군구	단지명 	전용면적(㎡)	계약년월	계약일	거래금액(만원)	층	건축년도
# calAPTprice({'income':4000, 'asset':5000, 'spend':2300})