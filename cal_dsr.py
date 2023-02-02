import requests
import json 

def calDSR(user, money, rate=5.4, period=360):
    service_url = "http://calcapi.fran.kr/v1/newdti"

    clientID = "wlsmscjswp"
    clientSecret = "eA7A1544389b3bCbcadB0c01649398D087"

    req_url = service_url + "?clientID=" + clientID + "&clientSecret=" + clientSecret + "&firstYearMethod=Y&yIncome=" + str(user['income']) \
    +"&loanType[0]=mortgage&repayType[0]=iSame&rate[0]=" + str(rate) + "&amountTotal[0]=" + str(money) + "&amountRemain[0]=" + str(money) \
    +"&periodTotal[0]=" + str(period) + "&periodRemain[0]=" + str(period)
    
    res = requests.get(req_url) 

    res_text= res.text
    res_json = json.loads(res_text)
    
    dsr= {} 
    dsr['year_real_return'] = res_json['data'][5]['금액']  # 연 원금 상환액 
    dsr['year_interest_return'] = res_json['data'][6]['금액']  # 연 이자 상환액 
    dsr['year_total'] = res_json['data'][7]['금액']  # 연간 대출 + 이자 상환액
    dsr['dsr'] = res_json['data'][-1]["금액"][:-1]
    
    return dsr 
    
res = calDSR({'income':6000}, 10000)
print(res)