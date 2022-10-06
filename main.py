import numpy as np
import pandas as pd
import mysql.connector as sq
import matplotlib.pyplot as pl
con=sq.connect(host='localhost',user='root',passwd='1234',database='mark3',charset='utf8')

cap=float(input("Enter your capital for investment : "))
time_input=float(input("Enter the time of investment in stock market(to the nearest multiple of 10) : "))
int1=np.round(time_input)
float1=time_input-np.round(time_input)
n=((float1)/0.10)+(int1-9)*6+1
n1=int(np.round(n))
#print(int1)
#print(float1)
#print(n1)


stock_cursor=con.cursor()
stock_cursor.execute("Select distinct stock_code from shares_d")
stock_names=stock_cursor.fetchall()

table_cursor=con.cursor()
table_cursor.execute("Select * from shares_d")
data=table_cursor.fetchall()
#Use data[0][1] to obtain time

count_cursor=con.cursor()
count_cursor.execute("Select count(*) from shares_d where stock_code='wipro'")
count=count_cursor.fetchall()
c=count[0][0]
time=[]
for i in range(c):
    x=data[i][1]
    time+=[x]
#time list ready

stocks=[]
for j in range(len(stock_names)):
    y=stock_names[j][0]
    stocks+=[y]
#stocks list ready


L1=[]
for i in range(c):
    p=data[i][2]
    L1+=[p]

L2=[]
for i in range(c,c*2):
    p=data[i][2]
    L2+=[p]

L3=[]
for i in range(c*2,c*3):
    p=data[i][2]
    L3+=[p]

L4=[]
for i in range(c*3,c*4):
    p=data[i][2]
    L4+=[p]

L5=[]
for i in range(c*4,c*5):
    p=data[i][2]
    L5+=[p]

L6=[]
for i in range(c*5,c*6):
    p=data[i][2]
    L6+=[p]

L7=[]
for i in range(c*6,c*7):
    p=data[i][2]
    L7+=[p]

L8=[]
for i in range(c*7,c*8):
    p=data[i][2]
    L8+=[p]

L9=[]
for i in range(c*8,c*9):
    p=data[i][2]
    L9+=[p]

Df1=pd.DataFrame([L1,L2,L3,L4,L5,L6,L7,L8,L9],index=stocks,columns=time)
Df2=Df1.iloc[:,:n1]
#Df2 created successfully

Df3=Df2.mean(axis=1)      #DataFrame storing average value till time t
Df4=Df2.iloc[:,n1-1:]     #Value at time=t
Df5=Df2.iloc[:,n1-2:n1-1] #at t-10
'''print(Df5)
Df4.rename(columns={time_input:time_input-0.10},inplace=True)
print(Df4)
'''
lst=[]
for i,j in Df5.iterrows():
   x=j[0]
   lst+=[float(x)]

lst1=[]
for i,j in Df4.iterrows():
   x=j[0]
   lst1+=[float(x)]

#lst_predicted=(2*lst1-lst)/2
lst_predicted=[]
for i in range(len(lst)):
    x=(2*lst1[i]-lst[i])
    lst_predicted+=[x]


'''Df5=pd.DataFrame(lst,index=stocks,columns=[time_input])
print(Df5)

    
Df6=(2*Df4-Df5)/2      #Predicted value
difference=Df6-Df3        #DataFrame storing difference in avg and predicted_value
'''
status=[]
for k in range(n1-1,171,c):
    z=data[k][3]
    status+=[z]     

Df7=pd.DataFrame([lst_predicted,status],columns=stocks,index=['price','Status'])    #Status of each stock
Df8=Df7.T
lst3=[]
for i in Df8.iterrows():
    if i[1][1]=='o':
        j=0.99*float(i[1][0])
        lst3+=[np.round(j,2)]
    if i[1][1]=='n':
        j=float(i[1][0])
        lst3+=[np.round(j,2)]
    if i[1][1]=='u':
        j=1.01*float(i[1][0])
        lst3+=[np.round(j,2)]
#print(lst3)
Df_penultimate=pd.DataFrame([((np.array(lst3)-np.array(lst1))/(np.array(lst1))),status],columns=stocks,index=['price','Status'])    #Change made here
#print(Df_penultimate)
Df_new=pd.DataFrame([lst1,status],columns=stocks,index=['price','Status'])

Df_final=Df_penultimate.T       #Final price difference

Df=Df_final.sort_values(by='price',ascending=False)

Df=Df.head(3)
count=0
stock_o=[]
stock_n=[]
for i in Df.iterrows(): 
    x=i[1][1]
    if x=='o':
        count+=1
        y=i[1].name
        stock_o+=[y]
    else:
        y=i[1].name
        stock_n+=[y]
den=count/3+(3-count)*2/3
num=count/3
fraction_o=num/den
if len(stock_o)!=0:
    cap_1=np.round(fraction_o*cap/len(stock_o),2)
else:
    cap_1=0
if len(stock_n)!=0:
    cap_2=np.round((1-fraction_o)*cap/len(stock_n),2)
else:
    cap_2=0


print("\tINVESTMENT PLAN")
print("=="*20)
for i in stock_o:
    print(i+" : "+str(cap_1))
for i in stock_n:
    print(i+" : "+str(cap_2))

print("\tESTIMATED RETURNS")
print("=="*20)

for i in Df.iterrows():
    if i[1][1]=='o':
        print(i[0]+" : "+str(np.round(i[1][0],2)*cap_1))
    else:
        print(i[0]+" : "+str(np.round(i[1][0],2)*cap_2))


print("\tRISK CALUCLATION")
print('=='*20)

risk=fraction_o*20+(1-fraction_o)*5
print("The risk % in this transaction is : "+str(risk)+" % ")



#####                      SHARE PLOTTING WORK BEGINS FROM HERE         ######



Df_plot=Df2.T
#print(Df_plot.columns)
#print(stock_o)
#print(stock_n)
legend=[]
for i in range(9):
    for j in range(len(stock_o)):
        if Df_plot.columns[i]==stock_o[j]:
            #print(Df_plot.columns[i])
            legend+=[Df_plot.columns[i]]
            colour_str='#'+str(20+9*i)+str(99-9*i)+str(99-9*i)
            a=Df_plot.iloc[:,i:i+1]
            b=Df_plot.index
            pl.xlabel('Time')
            pl.ylabel('Price')
            #pl.legend([Df_plot.columns[i]],loc="lower right")
            pl.plot(b,a,color=colour_str)
            #pl.show()
            #print(a)
    for j in range(len(stock_n)):
        if Df_plot.columns[i]==stock_n[j]:
            #print(Df_plot.columns[i])
            legend+=[Df_plot.columns[i]]
            colour_str='#'+str(20+9*i)+str(99-9*i)+str(99-9*i)
            a=Df_plot.iloc[:,i:i+1]
            b=Df_plot.index
            pl.xlabel('Time')
            pl.ylabel('Price')
            #pl.legend([Df_plot.columns[i]],loc="lower right")
            pl.plot(b,a,color=colour_str)
            #pl.show()
pl.legend(legend,loc="lower right")
pl.show()

      
con.close()
        
        
        
    









    
