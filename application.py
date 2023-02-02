from flask import Flask 
import sys
from flask import Flask, session, render_template, redirect, request, url_for 

from cal_pir import cal_apt_pir # city + addr, size 입력 받음 
from cal_consume import user_consume 
from cal_dsr import calDSR
from cal_loan import calLOAN
from cal_apt_price import calAPTprice

application = Flask(__name__)

user = {'name': '사용정보를 입력하세요', 'gender':0, 'age':0, 'grade':0, 'employ': 0, 'job':'', 'income':0, 'spend':0, 'asset':0, 'spend':0}  # 사용자 정보 저장 
apt = { 'apt_city': '', 'apt_addr': '', 'apt_name':' ', 'apt_size': 0, 'apt_price': 2430 , 'loan':0} # 아파트 정보 저장 

# 메인페이지 
@application.route("/")
def main():
    return render_template("index.html" )

# 사용자 정보 입력 
@application.route("/quote")
def quote():
            
    return render_template("get-a-quote.html")

# Q&A , 유튜브 링크 
@application.route("/service")
def service():
    return render_template("service.html")

# 사고싶은 아파트 정보 처리 
@application.route("/contact", methods=['GET','POST'])
def contact():
    # apt = { 'addr':"서울특별시 강남구 삼성로 212" , 'price':'20억' } 
    # user = { 'name':'김민지', 'gender': 'M' , 'age':25, 'grade':4, 'employ': 0, 'income':3 } 
    # 사용자 입력 받는 것 : 이름, 성별, 나이, 학력수준, 취업여부, 소득수준 
    
    apt_day = [] 
    apt_pir = [] 
    avg_pir = []
    
    year = 2022
    buy_year = 2022 
    
     # 값 입력 받으면 여기로 
    if request.method == 'POST' or 'GET': 
        # name gender age grade employ car income
        user['name'] = request.form['name']
        gender = request.form['gender']
        if gender == '남' : user['gender'] = 0 
        else : user['gender'] = 1
            
        user['age'] = request.form['age']
        user['grade'] = request.form['grade'] 
        user['employ'] = request.form['employ'] 
        user['job'] = request.form['job']
        user['income'] = int(request.form['income'])
        
        user['spend'] = int(user_consume(user)[0])
        user['asset'] = request.form['asset']  # 현재 저축 금액 
        
        buy_apt = calAPTprice(user) 
        
        apt['apt_city'] = request.form['apt-city']  # apt-city apt-addr apt-name 
        apt['apt_addr'] = request.form['apt-addr'] 
        apt['apt_name'] = request.form['apt-name'] 
        apt['apt_size'] = request.form['apt-size'] 
        
        
        # PIR 계산 
        apt_pir_data, avg_pir_data, apt_price = cal_apt_pir( apt['apt_city'] + " " + apt['apt_addr'] , float(apt['apt_size']))
        
        apt_day = [] 
        apt_pir = [] 
        avg_pir = [] 
        
        year = 2016
        apt['loan'] = apt_price[0]-int(user['asset']) 
        buy_year =  apt['loan'] // ( int(user['income']) - int(user['spend']) )  # 필요 기간 
        
        for i in apt_pir_data : 
            apt_day.append(str(i[0]))
            apt_pir.append(i[1])
            if int(str(i[0])[:4]) == year:
                avg_pir.append(avg_pir_data[str(year)])
            else : 
                year += 1 
                avg_pir.append(avg_pir_data[str(year)])
                
       # if request.method == 'GET': 
            

    return render_template("contact.html", user=user, apt=apt, buy_apt=buy_apt, 
                           apt_day=apt_day, apt_pir=apt_pir, avg_pir=avg_pir, year=year+buy_year, buy_year=buy_year )


# 아파트 검색 처리 (User 정보 없음)
@application.route("/contactAPT", methods=['GET','POST'])
def contactAPT():
    # apt = { 'addr':"서울특별시 강남구 삼성로 212" , 'price':'20억' } 
    
    apt_day = [] 
    apt_pir = [] 
    avg_pir = []

    aptname = request.form['aptname']
    print("아파트이름:", aptname)
    aptname = aptname.split(' ')
    
    apt_addr = ''
    
    for i in range(len(aptname)-1):
        apt_addr += aptname[i] 
        if i < len(aptname)-2 :
            apt_addr += ' '
            
    apt_name = aptname[-1]
        
    # PIR 계산 
    apt_pir_data, avg_pir_data, apt_price = cal_apt_pir( apt_addr )

    apt_day = [] 
    apt_pir = [] 
    avg_pir = [] 

    year = 2016
    
    print(apt_pir_data)
    
    for i in apt_pir_data : 
        apt_day.append(str(i[0]))
        apt_pir.append(i[1])
        
        while int(str(i[0])[:4]) != year:
            year += 1 
        print(year, int(str(i[0])[:4]))
        avg_pir.append(avg_pir_data[str(year)])
        print(avg_pir_data[str(year)])
        # else : 
        #     year += 1 
        #     avg_pir.append(avg_pir_data[year-2016])
            

    return render_template("contactAPT.html", apt_addr=apt_addr,apt_name=apt_name, apt_day=apt_day, apt_pir=apt_pir, avg_pir=avg_pir)


# DSR 페이지 
@application.route("/DSR", methods=['GET','POST'])
def dsr():
    
    dsr = calDSR(user,apt['loan'])   # 'year_real_return' 'year_interest_return' 'year_total' 'dsr'
    
    if int(dsr['dsr'].split(".")[0]) > 40 :  # 대출 불가능 
        comm = "DSR이 초과되어 추가 대출이 어렵습니다!"
    else : 
        comm = "대출이 가능합니다!"

    return render_template("DSR.html" , user=user, dsr=dsr, comm=comm, apt_loan=apt['loan'] )

# DSR2 페이지 
@application.route("/DSR2", methods=['GET','POST'])
def dsr2():
    
        # 값 입력 받으면 여기로 
    if request.method == 'POST' : 
        
        dsr = calDSR(user,apt['loan'])  
        
        if int(dsr['dsr'].split(".")[0]) > 40 :  # 대출 불가능 
            comm = "DSR이 초과돼 추가 대출이 어렵습니다!"
        else : 
            comm = "대출이 가능합니다!"
        
        loan = {} 
        loan['income'] = request.form['loan_income']
        loan['price'] = request.form['loan_price']
        loan['rate'] = request.form['loan_rate'] 
        loan['period'] = request.form['loan_period'] 
        
        loan_table, loan_month = calLOAN(loan)
        loan_len = len(loan_table)
        
       #  loan_result = calDSR( loan, loan['price'], loan['rate'], loan['period'])
    
    return render_template("DSR2.html", user=user, dsr=dsr, comm=comm , apt_loan=apt['loan'], loan=loan, loan_table=loan_table, loan_month=loan_month, loan_len=loan_len)

# 리츠 페이지 
@application.route("/Reits")
def reits():
    return render_template("Reits.html" )

# 모델 소개 페이지 
@application.route("/model")
def model():
    return render_template("model.html" )


# 모델 소개 페이지 
@application.route("/search")
def search():
    return render_template("search.html" )


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port="8080")
