
def calLOAN(loan): 
# 원금 : T  이자 : R 횟수 : C  월 반환 : M 

    T = int(loan['price']) 
    C = int(loan['period']) 
    R = int(loan['rate']) 
    MR = (R/12)/100
    
    a =  (1+MR)**C -1    
    b = T * (MR) * (1+MR)**C 
    
    month_return = b // a 
     #    M = T * ( J / (1 - (1 + J)-N))
    
    # print(month_return)
    
    # 첫 달 이자 금액 : 총액 * 이자/12 
    # 두 번 째 달 이자 금액 : 총액 - month_return * 이자/12 
    
    loan_table = [] 
    
    for i in range(1,C):
        interest = int( T * MR ) 
        loan_table.append([interest, int(month_return-interest)]) # 이자랑 원금 
        T -= month_return

    return loan_table , int(month_return)

# calLOAN( {'price':10000000, 'period':24, 'rate':5 })
        